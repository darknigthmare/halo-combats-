#!/usr/bin/env python3
"""Consolidate the frozen V7 quota interruption without changing art or gameplay.

Default: read-only preview. --apply changes the failure log, delivery counters,
and the two integration fields explicitly authorized for existing PNG display.
Other old asset fields and previous-wave counters are protected. Deferred
requests remain outside the failure log.
"""
from pathlib import Path
import argparse
import copy
import csv
import hashlib
import importlib.util
import json

PROJECT = Path(__file__).resolve().parents[2]
WORK = PROJECT / 'work/wave7'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def canonical_sha(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()

def expected_asset_records(baseline, bindings):
    old_assets = read(WORK / 'baseline_asset_records_v6.json')['active_candidates']
    assert len(old_assets) == baseline['candidate_count'] == 90
    for record, frozen in zip(old_assets, baseline['candidates']):
        assert record['id'] == frozen['id'] and canonical_sha(record) == frozen['metadata_sha256']
    usages = bindings['asset_usages']
    assert len({u['asset_id'] for u in usages}) == len(usages), 'Duplicate asset usage entry'
    by_usage = {u['asset_id']: u for u in usages}
    by_asset = {a['id']: a for a in old_assets}
    assert set(by_usage) == set(by_asset), 'Every existing candidate must be available in the V7 catalog, with no unknown asset'
    expected_usages = {aid: {'catalog'} for aid in by_asset}
    expected_entities = {aid: {a['entity_id']} for aid, a in by_asset.items()}
    with (PROJECT / 'data/characters_visual_inventory.csv').open(encoding='utf-8-sig', newline='') as stream:
        base_rows = list(csv.DictReader(stream))
    assert len(base_rows) == 24
    for fighter in base_rows:
        aid = fighter['preferred_asset_id']
        assert by_asset[aid]['entity_id'] == fighter['entity_id']
        expected_usages[aid].add('combat_neutral')
        guard = fighter.get('preferred_guard_asset_id')
        if guard:
            assert by_asset[guard]['entity_id'] == fighter['entity_id'] and by_asset[guard]['pose_scope'] == 'guard_static'
            expected_usages[guard].add('combat_guard')
    scarab = next(b for b in read(PROJECT / 'data/bosses.json')['entities'] if b['id'] == 'boss_scarab_h3')
    expected_usages[scarab['preferred_visual_asset']].add('boss')
    for aid, asset in by_asset.items():
        if asset['type'] == 'stage_master': expected_usages[aid].add('stage')
    catalog = read(WORK / 'baseline_catalog_v6.json')
    for entry in catalog['entries']:
        if entry.get('reused_visual_asset'):
            assert entry['id'] == 'warden_eternal_h5' and entry['reused_visual_asset'] == 'boss_warden_h5_profile_v01'
            expected_entities[entry['reused_visual_asset']].add(entry['id'])
    allowed = {'catalog', 'combat_neutral', 'combat_guard', 'boss', 'stage'}
    output = []
    for old in old_assets:
        record = copy.deepcopy(old)
        usage = by_usage.get(old['id'])
        if usage:
            assert set(usage) == {'asset_id', 'path', 'usages', 'entity_ids', 'usage_scope'}, 'Unexpected binding usage fields'
            assert usage['path'] == old['path'] and usage['usage_scope'] == 'static_prototype_only'
            assert usage['usages'] and len(usage['usages']) == len(set(usage['usages']))
            assert set(usage['usages']) <= allowed
            assert usage['entity_ids'] and len(usage['entity_ids']) == len(set(usage['entity_ids']))
            assert set(usage['usages']) == expected_usages[old['id']], 'Usage is not justified by the frozen preferred asset selections: ' + old['id']
            assert set(usage['entity_ids']) == expected_entities[old['id']], 'Asset owner or explicit Warden reuse changed: ' + old['id']
            record['integration_status'] = ('prototype_static_display' if set(usage['usages']) - {'catalog'} else 'prototype_catalog_display')
            record['prototype_usage_v7'] = copy.deepcopy(usage)
        output.append(record)
    return old_assets, output

def verify_protected(baseline, manifest, counts):
    originals = baseline['candidates']
    bindings_path = PROJECT / 'data/prototype_asset_bindings_v7.json'
    if bindings_path.exists():
        old_assets, integrated_assets = expected_asset_records(baseline, read(bindings_path))
    else:
        old_assets = read(WORK / 'baseline_asset_records_v6.json')['active_candidates']
        integrated_assets = old_assets
    assert len(manifest['active_candidates']) == len(originals) == 90
    for old, current, old_record, integrated_record in zip(originals, manifest['active_candidates'], old_assets, integrated_assets):
        assert old['id'] == current['id']
        assert current == old_record or current == integrated_record, 'Unauthorized historical asset metadata change: ' + old['id']
        assert digest(PROJECT / old['path']) == old['sha256'], 'Historical PNG changed: ' + old['path']
    failures = manifest['failed_requests']
    assert canonical_sha(failures[:baseline['historical_failures']]) == baseline['prior_failed_requests_sha256']
    for key, old in baseline['prior_counts'].items():
        if key not in {'updated_utc', 'historical_generation_failures_all_waves'}:
            assert counts[key] == old, 'Historical counter modified: ' + key
    fighters = read(PROJECT / 'data/fighters.json')
    protected = copy.deepcopy(fighters)
    for fighter in protected['fighters']:
        if fighter['id'] == 'chief_infinite':
            for key in baseline['registry_structure']['chief_allowed_fields']:
                fighter.pop(key, None)
    assert canonical_sha(protected) == baseline['registry_structure']['fighters_protected_sha256']
    assert canonical_sha(read(PROJECT / 'data/bosses.json')) == baseline['registry_structure']['bosses_protected_sha256']
    catalog = read(PROJECT / 'data/expansion_characters.json')
    assert catalog == read(WORK / 'baseline_catalog_v6.json'), 'No V7 image: extension catalog must stay unchanged'

def prepare():
    baseline = read(WORK / 'baseline_v6.json')
    journal = read(WORK / 'generation_results.json')
    merge_spec = importlib.util.spec_from_file_location('halo_v7_journal_merger', WORK / 'merge_generation_journals.py')
    merger = importlib.util.module_from_spec(merge_spec)
    merge_spec.loader.exec_module(merger)
    reconstructed, problems = merger.collect()
    assert not problems, 'Producer journal coverage or freeze evidence is invalid: ' + str(problems)
    assert set(journal) == set(reconstructed) | {'merged_utc'}, 'Unexpected consolidated journal shape'
    assert all(journal[key] == value for key, value in reconstructed.items()), 'Consolidated records or counts differ from the frozen producer journals'
    manifest_path = PROJECT / 'data/asset_manifest.json'
    counts_path = PROJECT / 'data/delivery_counts.json'
    manifest, counts = read(manifest_path), read(counts_path)
    verify_protected(baseline, manifest, counts)
    for source in journal['source_journals']:
        assert digest(PROJECT / source['path']) == source['sha256'], 'Frozen producer journal changed'
    calls = journal['results']
    deferred = journal['deferred_requests']
    summary = journal['counts']
    assert summary == {
        'planned_targets': 19, 'actual_tool_calls': 7, 'generated_pngs': 0,
        'generation_failures': 7, 'quota_failures': 7, 'moderation_refusals': 0,
        'other_generation_failures': 0, 'deferred_without_call': 12,
    }, 'V7 interruption changed: re-review scope instead of silently changing totals'
    assert all(r['status'] == 'generation_failed' and r['error_class'] == 'usage_limit_reached' and r['tool_called'] is True and r.get('source_path') is None for r in calls)
    assert all(r['tool_called'] is False and r['status'] == 'deferred_global_usage_limit' for r in deferred)
    additions = []
    for index, source in enumerate(calls):
        row = copy.deepcopy(source)
        row['producer_source_journal'] = row.pop('source_journal')
        row['producer_journal_record'] = row.pop('journal_record')
        row.update({'generation_wave': 7, 'source_journal': 'work/wave7/generation_results.json',
                    'journal_record': index, 'failure_category': 'service_quota'})
        additions.append(row)
    old_failures = manifest['failed_requests'][:baseline['historical_failures']]
    existing_suffix = manifest['failed_requests'][baseline['historical_failures']:]
    assert not existing_suffix or existing_suffix == additions, 'Unexpected V7 failure log suffix'
    new_manifest = copy.deepcopy(manifest)
    bindings = read(PROJECT / 'data/prototype_asset_bindings_v7.json')
    old_assets, expected_assets = expected_asset_records(baseline, bindings)
    new_manifest['active_candidates'] = expected_assets
    new_manifest['failed_requests'] = old_failures + additions
    new_manifest['updated_utc'] = journal['merged_utc']
    new_counts = copy.deepcopy(counts)
    new_counts.update({
        'updated_utc': journal['merged_utc'],
        'historical_generation_failures_all_waves': 118,
        'historical_automatic_generation_rejections_all_waves': 111,
        'historical_service_quota_failures_all_waves': 7,
        'visual_candidates_pre_wave7': 90,
        'wave7_planned_generation_targets': 19,
        'wave7_generation_attempts': 7,
        'wave7_successful_generation_attempts': 0,
        'wave7_generation_failures': 7,
        'wave7_service_quota_failures': 7,
        'wave7_automatic_generation_rejections': 0,
        'wave7_other_generation_failures': 0,
        'wave7_deferred_generation_targets_without_attempt': 12,
        'wave7_generated_pngs': 0,
        'wave7_generated_expansion_pngs': 0,
        'wave7_generated_guard_pngs': 0,
        'wave7_unique_expansion_entities_with_new_candidates': 0,
        'wave7_corrected_candidate_images': 0,
        'wave7_prior_pngs_registered_for_static_prototype_use': sum(a.get('integration_status') == 'prototype_static_display' for a in expected_assets),
        'wave7_prior_pngs_registered_for_catalog_only': sum(a.get('integration_status') == 'prototype_catalog_display' for a in expected_assets),
        'wave7_prototype_animation_clips': 0,
    })
    outputs = {manifest_path: encode(new_manifest), counts_path: encode(new_counts)}
    changes = [str(path.relative_to(PROJECT)) for path, data in outputs.items() if path.read_bytes() != data]
    return outputs, changes, summary

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    outputs, changes, summary = prepare()
    if args.apply:
        for path, data in outputs.items():
            if path.read_bytes() != data:
                temporary = path.with_suffix(path.suffix + '.tmp')
                temporary.write_bytes(data)
                temporary.replace(path)
    print(json.dumps({'applied': args.apply, 'changed_files': changes,
                      'counts': summary, 'prior_candidate_records_preserved_except_authorized_integration_fields': 90,
                      'prior_failure_records_preserved': 111}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
