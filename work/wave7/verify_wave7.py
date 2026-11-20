#!/usr/bin/env python3
"""Verify V7 conservation, quota accounting and the static prototype snapshot.

Default: read-only. --write saves verification evidence. --snapshot-to freezes
only the explicit V7 publication scope after all available checks have passed.
A blocked browser check is recorded as a limitation, never converted to a pass.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import importlib.util
import json
import shutil

PROJECT = Path(__file__).resolve().parents[2]
WORK = PROJECT / 'work/wave7'
spec = importlib.util.spec_from_file_location('halo_v7_consolidator', WORK / 'consolidate_wave7.py')
v7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v7)
CENTRAL_OUTPUTS = [
    'README.md', 'README_V7.md', 'data/asset_manifest.json', 'data/delivery_counts.json',
    'data/prototype_asset_bindings_v7.json', 'docs/HALO_COMBATS_PERSONNAGES_V7.md',
    'docs/SOURCES_PERSONNAGES_V7.md', 'prototype/halo_combats_lab_v7.html',
    'prototype/README_V7.md', 'prototype/lab_v7/app.js', 'prototype/lab_v7/style.css',
    'prototype/lab_v7/catalog.js',
]

def read(rel):
    return v7.read(PROJECT / rel)

def import_files():
    names = set(CENTRAL_OUTPUTS)
    for directory in (WORK, PROJECT / 'prototype/qa_v7'):
        for path in directory.rglob('*'):
            if not path.is_file() or '__pycache__' in path.parts or path.name.endswith(('.pyc', '.tmp')):
                continue
            assert path.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp'}, 'Reference images and temporary QA screenshots remain outside Git'
            assert not path.is_symlink(), 'Symlink not allowed in snapshot'
            names.add(path.relative_to(PROJECT).as_posix())
    return sorted(names)

def verify():
    baseline = read('work/wave7/baseline_v6.json')
    repo = read('work/wave7/baseline_repository_files.json')
    manifest = read('data/asset_manifest.json')
    counts = read('data/delivery_counts.json')
    bindings = read('data/prototype_asset_bindings_v7.json')
    journal = read('work/wave7/generation_results.json')
    outputs, changes, generation = v7.prepare()
    assert not changes, 'Central consolidation is incomplete or differs from frozen evidence: ' + str(changes)
    originals, expected = v7.expected_asset_records(baseline, bindings)
    assert manifest['active_candidates'] == expected
    assert len(manifest['failed_requests']) == counts['historical_generation_failures_all_waves'] == 118
    active = manifest['active_candidates']
    assert len(active) == len({a['id'] for a in active}) == len({a['sha256'] for a in active}) == 90
    actual_pngs = {p.relative_to(PROJECT).as_posix() for p in (PROJECT / 'assets').rglob('*.png')}
    assert actual_pngs == {a['path'] for a in active}, 'Untracked or missing art PNG in source tree'
    assert not any(a.get('generation_wave') == 7 for a in active)
    for asset in active:
        assert asset['fidelity_status'] == 'not_certified'
        assert asset['animation_status'] == 'not_animated'
    assert len(read('data/fighters.json')['fighters']) == 24
    assert len(read('data/expansion_characters.json')['entries']) == 34
    assert len(read('data/bosses.json')['entities']) == 20
    assert len(read('data/stages.json')['stages']) == 24
    assert counts['expansion_catalog_entries_without_visual'] == 17
    assert counts['fighter_entities_with_guard_candidate'] == 23
    assert counts['certified_visuals'] == counts['animation_clips'] == counts['wave7_generated_pngs'] == 0
    assert counts['wave7_prior_pngs_registered_for_static_prototype_use'] == 50
    assert counts['wave7_prior_pngs_registered_for_catalog_only'] == 40
    usage_counts = {usage: sum(usage in u['usages'] for u in bindings['asset_usages']) for usage in ('catalog', 'combat_neutral', 'combat_guard', 'boss', 'stage')}
    assert usage_counts == {'catalog': 90, 'combat_neutral': 24, 'combat_guard': 23, 'boss': 1, 'stage': 2}
    for filename in ('qa_unsc.json', 'qa_aliens.json'):
        qa = read('work/wave7/' + filename)
        assert qa.get('reviews', []) == [], 'No new PNG exists; candidate visual QA must stay empty'
    receipts = read('work/wave7/producer_freeze_receipts.json')
    for path, receipt in receipts['files'].items():
        assert v7.digest(WORK / path) == receipt['sha256'], 'Frozen producer evidence changed: ' + path
    rebuild = read('work/wave7/central_binding_check.json')
    assert rebuild['exit_code'] == 0
    for row in rebuild['tested_files']:
        assert v7.digest(PROJECT / row['path']) == row['sha256'], 'Binding source changed after the post-integration rebuild check: ' + row['path']
    qa = read('prototype/qa_v7/results.json')
    assert qa['failed'] == 0 and qa['passed'] > 0, 'Prototype logic/data tests did not pass'
    assert qa['status'] in {'passed', 'passed_with_browser_blocked'}
    browser = qa['browser_validation']
    if qa['status'] == 'passed_with_browser_blocked':
        assert browser['status'] == 'blocked' and browser.get('reason'), 'Browser limitation must be explicit'
    else:
        assert browser['status'] == 'passed', 'Unqualified pass requires browser evidence'
    tested = {row['path'] for row in qa['tested_files']}
    required_tested = {'prototype/halo_combats_lab_v7.html', 'prototype/lab_v7/app.js',
                       'prototype/lab_v7/style.css', 'prototype/lab_v7/catalog.js',
                       'data/prototype_asset_bindings_v7.json'}
    assert required_tested <= tested
    for row in qa['tested_files']:
        assert v7.digest(PROJECT / row['path']) == row['sha256'], 'Prototype changed after testing: ' + row['path']
    allowed = set(CENTRAL_OUTPUTS)
    excluded = set(repo['source_differences_at_capture'])
    assert len(excluded) == 17
    immutable = []
    for row in repo['files']:
        if row['path'] in allowed or row['path'] in excluded:
            continue
        assert v7.digest(PROJECT / row['path']) == row['sha256'], 'Historical source file changed: ' + row['path']
        immutable.append(row['path'])
    assert (PROJECT / 'README.md').read_bytes() == (PROJECT / 'README_V7.md').read_bytes()
    imports = import_files()
    assert not excluded.intersection(imports), 'Publication-specific historical file entered import'
    for path in imports:
        assert (PROJECT / path).is_file(), 'Required V7 file missing: ' + path
    return {
        'wave': 7, 'status': qa['status'], 'checked_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'baseline_commit': repo['baseline_commit'], 'baseline_tree': repo['baseline_tree'],
        'generation': generation, 'asset_pngs_preserved_byte_for_byte': 90,
        'historical_asset_records_checked': 90,
        'only_authorized_existing_asset_fields_changed': ['integration_status', 'prototype_usage_v7'],
        'prototype_usage_counts': usage_counts,
        'historical_failures_preserved': 111, 'historical_files_preserved_in_source': len(immutable),
        'historical_publication_specific_exclusions_preserved': sorted(excluded),
        'publication_specific_files_to_preserve_byte_for_byte': sorted(excluded - {'PUBLICATION_INVENTORY.json', 'SHA256SUMS.txt'}),
        'global_publication_indexes_to_recompute': ['PUBLICATION_INVENTORY.json', 'SHA256SUMS.txt'],
        'prototype_qa_report': 'prototype/qa_v7/results.json',
        'prototype_qa_sha256': v7.digest(PROJECT / 'prototype/qa_v7/results.json'),
        'prototype_tested_files': qa['tested_files'], 'browser_validation': browser,
        'counted_new_pngs': 0, 'counted_new_animation_clips': 0,
        'new_base_fighter_records': 0, 'new_extension_gameplay_activations': 0,
        'central_consolidation_idempotent': True,
        'generation_journal_sha256': v7.digest(WORK / 'generation_results.json'),
        'bindings_sha256': v7.digest(PROJECT / 'data/prototype_asset_bindings_v7.json'),
        'post_integration_deterministic_binding_rebuild': 'passed',
        'counts': counts,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--snapshot-to', type=Path)
    args = parser.parse_args()
    evidence = verify()
    if args.write or args.snapshot_to:
        (WORK / 'verification.json').write_bytes(v7.encode(evidence))
    result = {'verified': True, 'status': evidence['status'], 'generation': evidence['generation'],
              'prototype_usage_counts': evidence['prototype_usage_counts'],
              'browser_validation': evidence['browser_validation']}
    if args.snapshot_to:
        destination = args.snapshot_to.resolve()
        assert not destination.exists(), 'Snapshot destination already exists'
        assert PROJECT not in destination.parents, 'Snapshot must be outside the source project'
        names = import_files()
        rows = [{'path': path, 'bytes': (PROJECT / path).stat().st_size,
                 'sha256': v7.digest(PROJECT / path)} for path in names]
        for row in rows:
            source = PROJECT / row['path']
            target = destination / 'files' / row['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            assert v7.digest(target) == row['sha256'] and v7.digest(source) == row['sha256'], 'Source changed while freezing snapshot'
        inventory = {'wave': 7, 'baseline_commit': evidence['baseline_commit'],
                     'baseline_tree': evidence['baseline_tree'], 'file_count': len(rows),
                     'files': rows, 'counts': evidence['counts'],
                     'verification_status': evidence['status'],
                     'browser_validation': evidence['browser_validation']}
        (destination / 'FILES_SHA256.json').write_bytes(v7.encode(inventory))
        (destination / 'SHA256SUMS.txt').write_text(''.join(row['sha256'] + '  files/' + row['path'] + '\n' for row in rows), encoding='utf-8')
        result.update({'snapshot': str(destination), 'snapshot_files': len(rows),
                       'snapshot_inventory_sha256': v7.digest(destination / 'FILES_SHA256.json')})
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
