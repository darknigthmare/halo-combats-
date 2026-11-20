#!/usr/bin/env python3
"""Consolidate V7 real calls and explicit deferrals without inventing attempts.

Read-only by default. --apply requires all three producer journals frozen and
all 19 planned targets accounted for by either a completed call or a deferral.
An HTTP 429 usage_limit_reached is a service quota error, never a safety refusal.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import copy
import hashlib
import json

WORK = Path(__file__).resolve().parent
PROJECT = WORK.parents[1]
INPUTS = ('generation_results_unsc.json', 'generation_results_aliens.json', 'generation_results_root.json')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def error_class(row):
    declared = row.get('error_class')
    error = str(row.get('error', ''))
    if 'usage_limit_reached' in error:
        assert declared in (None, 'usage_limit_reached'), 'Contradictory quota classification'
        return 'usage_limit_reached'
    if 'moderation_blocked' in error:
        assert declared in (None, 'moderation_blocked'), 'Contradictory safety classification'
        return 'moderation_blocked'
    return declared or 'unclassified_generation_error'

def collect():
    baseline = read(WORK / 'baseline_v6.json')
    receipts_path = WORK / 'producer_freeze_receipts.json'
    receipts = read(receipts_path).get('files', {}) if receipts_path.exists() else {}
    expected = set(baseline['target_ids'])
    results, deferred, inputs, problems = [], [], [], []
    for filename in INPUTS:
        path = WORK / filename
        if not path.exists():
            problems.append('Missing producer journal: ' + filename)
            continue
        data = read(path)
        calls = data.get('results', [])
        skipped = data.get('deferred_requests', [])
        inputs.append({'path': 'work/wave7/' + filename, 'sha256': sha(path),
                       'actual_tool_calls': len(calls), 'deferred_without_call': len(skipped)})
        self_frozen = bool(data.get('frozen_utc')) and data.get('state') == 'frozen_global_usage_limit'
        receipted = receipts.get(filename, {}).get('sha256') == sha(path)
        if not self_frozen and not receipted:
            problems.append('Producer journal not frozen after quota stop: ' + filename)
        for i, original in enumerate(calls):
            row = copy.deepcopy(original)
            if row.get('status') not in ('generated_candidate', 'generation_failed'):
                problems.append('Unfinished call: ' + filename + ':' + str(i))
            if row.get('tool_called') is not True:
                problems.append('Call must explicitly state tool_called:true: ' + filename + ':' + str(i))
            if row.get('status') == 'generated_candidate':
                source = Path(row.get('source_path') or '')
                if not source.is_file():
                    problems.append('Generated source absent: ' + str(source))
            elif row.get('status') == 'generation_failed':
                row['error_class'] = error_class(row)
                if row.get('source_path'):
                    problems.append('Failed call claims an image: ' + filename + ':' + str(i))
                if row['error_class'] == 'usage_limit_reached' and row.get('http_status') != 429:
                    problems.append('Quota error missing HTTP 429 evidence: ' + filename + ':' + str(i))
            row['source_journal'] = 'work/wave7/' + filename
            row['journal_record'] = i
            results.append(row)
        for i, original in enumerate(skipped):
            row = copy.deepcopy(original)
            if row.get('status') != 'deferred_global_usage_limit' or row.get('tool_called') is not False:
                problems.append('Invalid deferral state: ' + filename + ':' + str(i))
            if row.get('source_path') or row.get('started_utc') or row.get('completed_utc'):
                problems.append('Deferral must not imply a tool call or image: ' + filename + ':' + str(i))
            row['source_journal'] = 'work/wave7/' + filename
            row['deferred_record'] = i
            deferred.append(row)
    called = [r['entity_id'] for r in results]
    skipped = [r['entity_id'] for r in deferred]
    if len(called) != len(set(called)):
        problems.append('Duplicate V7 call for one target')
    if len(skipped) != len(set(skipped)):
        problems.append('Duplicate deferred target')
    if set(called) & set(skipped):
        problems.append('A target is both called and deferred')
    missing = sorted(expected - set(called) - set(skipped))
    unexpected = sorted((set(called) | set(skipped)) - expected)
    if missing: problems.append('Unaccounted planned targets: ' + ', '.join(missing))
    if unexpected: problems.append('Unexpected targets: ' + ', '.join(unexpected))
    counts = {
        'planned_targets': len(expected),
        'actual_tool_calls': len(results),
        'generated_pngs': sum(r.get('status') == 'generated_candidate' for r in results),
        'generation_failures': sum(r.get('status') == 'generation_failed' for r in results),
        'quota_failures': sum(r.get('error_class') == 'usage_limit_reached' for r in results),
        'moderation_refusals': sum(r.get('error_class') == 'moderation_blocked' for r in results),
        'other_generation_failures': sum(r.get('status') == 'generation_failed' and r.get('error_class') not in ('usage_limit_reached', 'moderation_blocked') for r in results),
        'deferred_without_call': len(deferred),
    }
    assert counts['generation_failures'] == counts['quota_failures'] + counts['moderation_refusals'] + counts['other_generation_failures']
    assert counts['actual_tool_calls'] == counts['generated_pngs'] + counts['generation_failures']
    return {
        'wave': 7,
        'state': 'frozen_global_usage_limit',
        'task': 'Reprendre les 17 extensions sans image, la correction de Dinh et la garde du Major. La limite globale du service a interrompu cette vague : seuls les appels réellement effectués sont comptés.',
        'source_journals': inputs,
        'results': results,
        'deferred_requests': deferred,
        'counts': counts,
    }, problems

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    output, problems = collect()
    if args.apply:
        assert not problems, problems
        assert all(sha(PROJECT / row['path']) == row['sha256'] for row in output['source_journals']), 'Producer journal changed during consolidation'
        path = WORK / 'generation_results.json'
        existing = read(path) if path.exists() else None
        if existing and all(existing.get(k) == v for k, v in output.items()):
            action = 'unchanged'
        else:
            output['merged_utc'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
            temporary = path.with_suffix('.json.tmp')
            temporary.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            temporary.replace(path)
            action = 'written'
    else:
        action = 'read_only'
    print(json.dumps({'action': action, 'counts': output['counts'], 'problems': problems}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
