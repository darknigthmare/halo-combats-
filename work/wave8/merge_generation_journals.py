#!/usr/bin/env python3
"""Merge frozen V8 producer evidence; pending requests are never counted as calls.

Default is read-only. --apply requires all producer journals and their matching
freeze receipts. Each successful call must point to its real generated PNG.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import copy
import hashlib
import json

WORK = Path(__file__).resolve().parent
PROJECT = WORK.parents[1]
INPUTS = ('generation_results_root.json', 'generation_results_unsc.json', 'generation_results_aliens.json')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'

def classify_error(row):
    declared = row.get('error_class')
    raw = str(row.get('error', ''))
    if 'usage_limit_reached' in raw:
        assert declared in (None, 'usage_limit_reached'), 'Contradictory quota classification'
        return 'usage_limit_reached'
    if 'moderation_blocked' in raw:
        assert declared in (None, 'moderation_blocked'), 'Contradictory moderation classification'
        return 'moderation_blocked'
    return declared or 'unclassified_generation_error'

def bind_producer(row, source_journal, source_sha256):
    """Keep inherited provenance separate from this frozen producer file."""
    if row.get('source_journal'):
        previous = row.pop('source_journal')
        previous_sha = row.pop('source_journal_sha256', None)
        assert previous_sha and sha(PROJECT / previous) == previous_sha, 'Inherited source path/SHA mismatch'
        assert row.get('previous_source_journal', previous) == previous
        assert row.get('previous_source_journal_sha256', previous_sha) == previous_sha
        row['previous_source_journal'] = previous
        row['previous_source_journal_sha256'] = previous_sha
    else:
        assert 'source_journal_sha256' not in row, 'Source SHA lacks a source path'
    row['source_journal'] = source_journal
    row['source_journal_sha256'] = source_sha256

def collect():
    baseline = read(WORK / 'baseline_v7.json')
    receipts_path = WORK / 'producer_freeze_receipts.json'
    receipts = read(receipts_path).get('files', {}) if receipts_path.exists() else {}
    expected = set(baseline['target_ids'])
    results, deferred, sources, problems = [], [], [], []
    for name in INPUTS:
        path = WORK / name
        if not path.is_file():
            problems.append('Missing producer journal: ' + name)
            continue
        data = read(path)
        if data.get('wave') != 8:
            problems.append('Wrong generation wave: ' + name)
        if data.get('pending_requests'):
            problems.append('Unfinished pending requests: ' + name)
        digest = sha(path)
        if receipts.get(name, {}).get('sha256') != digest:
            problems.append('Missing or mismatched explicit producer freeze: ' + name)
        calls, skips = data.get('results', []), data.get('deferred_requests', [])
        sources.append({'path': 'work/wave8/' + name, 'sha256': digest,
                        'actual_tool_calls': len(calls), 'deferred_without_call': len(skips)})
        for index, original in enumerate(calls):
            row = copy.deepcopy(original)
            if row.get('entity_id') not in expected:
                problems.append('Unexpected generated target: ' + name + ':' + str(index))
            if row.get('status') not in ('generated_candidate', 'generation_failed'):
                problems.append('Unfinished or unknown result: ' + name + ':' + str(index))
            if row.get('tool_called') is not True:
                problems.append('Real call lacks tool_called:true: ' + name + ':' + str(index))
            if not row.get('started_utc') or not row.get('completed_utc'):
                problems.append('Real call lacks timestamps: ' + name + ':' + str(index))
            if not row.get('prompt'):
                problems.append('Real call lacks its prompt: ' + name + ':' + str(index))
            if row.get('status') == 'generated_candidate':
                path_value = row.get('source_path')
                if not path_value or not Path(path_value).is_file():
                    problems.append('Generated PNG source absent: ' + name + ':' + str(index))
            elif row.get('status') == 'generation_failed':
                row['error_class'] = classify_error(row)
                if row.get('source_path') or not row.get('error'):
                    problems.append('Invalid failed result: ' + name + ':' + str(index))
                if row['error_class'] == 'usage_limit_reached' and row.get('http_status') != 429:
                    problems.append('Quota error lacks HTTP 429 evidence: ' + name + ':' + str(index))
            bind_producer(row, 'work/wave8/' + name, digest)
            row['journal_record'] = index
            if 'retry_of_journal_record' in row:
                retry_index = row['retry_of_journal_record']
                assert isinstance(retry_index, int) and 0 <= retry_index < index, 'Invalid producer retry index'
                assert calls[retry_index]['entity_id'] == row['entity_id'], 'Retry points to a different target'
            results.append(row)
        for index, original in enumerate(skips):
            row = copy.deepcopy(original)
            if row.get('entity_id') not in expected or row.get('tool_called') is not False:
                problems.append('Invalid deferred target: ' + name + ':' + str(index))
            if not str(row.get('status', '')).startswith('deferred_') or not row.get('reason'):
                problems.append('Deferral lacks explicit state/reason: ' + name + ':' + str(index))
            if row.get('source_path') or row.get('started_utc') or row.get('completed_utc'):
                problems.append('Deferral incorrectly implies a call/output: ' + name + ':' + str(index))
            bind_producer(row, 'work/wave8/' + name, digest)
            row['deferred_record'] = index
            deferred.append(row)
    called = [r['entity_id'] for r in results]
    skipped = [r['entity_id'] for r in deferred]
    if len(skipped) != len(set(skipped)):
        problems.append('Duplicate deferral for one target')
    if set(called) & set(skipped):
        problems.append('A called target is also counted as deferred')
    missing = sorted(expected - set(called) - set(skipped))
    if missing:
        problems.append('Unaccounted target(s): ' + ', '.join(missing))
    counts = {'planned_targets': len(expected), 'actual_tool_calls': len(results),
              'unique_called_targets': len(set(called)),
              'generated_pngs': sum(r.get('status') == 'generated_candidate' for r in results),
              'generation_failures': sum(r.get('status') == 'generation_failed' for r in results),
              'quota_failures': sum(r.get('error_class') == 'usage_limit_reached' for r in results),
              'moderation_refusals': sum(r.get('error_class') == 'moderation_blocked' for r in results),
              'other_generation_failures': sum(r.get('status') == 'generation_failed' and r.get('error_class') not in ('usage_limit_reached', 'moderation_blocked') for r in results),
              'deferred_without_call': len(deferred)}
    assert counts['actual_tool_calls'] == counts['generated_pngs'] + counts['generation_failures']
    assert counts['generation_failures'] == counts['quota_failures'] + counts['moderation_refusals'] + counts['other_generation_failures']
    return {'wave': 8, 'state': 'frozen_producer_evidence',
            'task': 'Reprise des 17 extensions sans image, de la garde du Major et de la correction de Dinh après la limite de quota V7.',
            'source_journals': sources, 'results': results, 'deferred_requests': deferred,
            'counts': counts}, problems

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    output, problems = collect()
    action = 'read_only'
    if args.apply:
        assert not problems, problems
        assert all(sha(PROJECT / row['path']) == row['sha256'] for row in output['source_journals'])
        path = WORK / 'generation_results.json'
        old = read(path) if path.exists() else None
        if old and all(old.get(key) == value for key, value in output.items()):
            action = 'unchanged'
        else:
            output['merged_utc'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
            temporary = path.with_suffix('.json.tmp')
            temporary.write_text(encode(output), encoding='utf-8')
            temporary.replace(path)
            action = 'written'
    print(encode({'action': action, 'counts': output['counts'], 'problems': problems}))

if __name__ == '__main__':
    main()
