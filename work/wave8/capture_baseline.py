#!/usr/bin/env python3
"""Capture the verified V7 delivery before V8 art changes; never overwrite it."""
from pathlib import Path
import hashlib
import json
import subprocess

PROJECT = Path(__file__).resolve().parents[2]
WORK = PROJECT / 'work/wave8'
REPO = PROJECT.parent / 'halo_combats_publish'
BASE = '6c719b3041c04f75f7443135dd1b9f1d638bbe1d'
TREE = 'e1761c27d6e16eb78c34279be7aafec1d48efa27'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical_sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(name, value):
    path = WORK / name
    assert not path.exists(), 'Baseline already exists: ' + name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    WORK.mkdir(exist_ok=True)
    assert git('rev-parse', 'HEAD').decode().strip() == BASE
    assert git('rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    assert not git('status', '--porcelain').strip()
    rows, differences = [], []
    for raw in git('ls-tree', '-rlz', 'HEAD').split(b'\0'):
        if not raw:
            continue
        info, name = raw.split(b'\t', 1)
        mode, kind, blob, size = info.decode().split()
        name = name.decode()
        data = (REPO / name).read_bytes()
        assert len(data) == int(size)
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == blob
        sha = hashlib.sha256(data).hexdigest()
        rows.append({'path': name, 'mode': mode, 'type': kind, 'git_sha': blob, 'bytes': len(data), 'sha256': sha})
        source = PROJECT / name
        if not source.is_file() or digest(source) != sha:
            differences.append(name)
    assert len(rows) == 271
    previous = read(PROJECT / 'work/wave7/baseline_repository_files.json')
    assert set(differences) == set(previous['source_differences_at_capture']), 'Unexpected source/publication divergence'
    write('baseline_repository_files.json', {'baseline_commit': BASE, 'baseline_tree': TREE,
          'file_count': len(rows), 'files': rows, 'source_differences_at_capture': differences})
    manifest = read(PROJECT / 'data/asset_manifest.json')
    counts = read(PROJECT / 'data/delivery_counts.json')
    catalog = read(PROJECT / 'data/expansion_characters.json')
    fighters = read(PROJECT / 'data/fighters.json')
    assert len(manifest['active_candidates']) == 90
    assert len(manifest['failed_requests']) == 118
    missing = [entry['id'] for entry in catalog['entries'] if not entry.get('visual_assets')]
    assert len(missing) == 17
    protected_paths = ['data/fighters.json', 'data/bosses.json', 'data/stages.json',
                       'data/expansion_characters.json', 'data/prototype_asset_bindings_v7.json',
                       'prototype/halo_combats_lab_v7.html', 'prototype/lab_v7/app.js',
                       'prototype/lab_v7/style.css', 'prototype/lab_v7/catalog.js',
                       'prototype/qa_v7/results.json']
    baseline = {'generation_wave': 8, 'baseline_commit': BASE, 'baseline_tree': TREE,
        'candidate_count': 90, 'historical_failures': 118,
        'candidates': [{'id': a['id'], 'path': a['path'], 'sha256': a['sha256'],
                        'metadata_sha256': canonical_sha(a)} for a in manifest['active_candidates']],
        'prior_failed_requests_sha256': canonical_sha(manifest['failed_requests']),
        'prior_counts': counts,
        'registry_file_sha256': {path: digest(PROJECT / path) for path in protected_paths},
        'missing_extension_ids': missing, 'correction_ids': ['dinh_infinite'],
        'target_ids': missing + ['dinh_infinite', 'chief_infinite'],
        'catalog_entry_ids': [entry['id'] for entry in catalog['entries']],
        'catalog_art_fields': ['new_visual_assets', 'visual_assets', 'preferred_visual_asset', 'art_status'],
        'chief_guard_art_fields': ['guard_visual_assets', 'guard_art_status', 'preferred_guard_asset'],
        'neutral_preferences': {entry['id']: entry.get('preferred_visual_asset') for entry in fighters['fighters']},
        'v7_integration_policy': 'All 90 existing active candidate records and PNG bytes remain immutable in V8; new images receive separate records.'}
    write('baseline_v7.json', baseline)
    write('baseline_asset_records_v7.json', {'active_candidates': manifest['active_candidates']})
    for name, path in [('baseline_catalog_v7.json', 'data/expansion_characters.json'),
                       ('baseline_fighters_v7.json', 'data/fighters.json'),
                       ('README_V7_before_wave8.md', 'README.md')]:
        destination = WORK / name
        assert not destination.exists()
        destination.write_bytes((PROJECT / path).read_bytes())
    print(json.dumps({'captured': True, 'files': len(rows), 'source_differences': len(differences),
                      'pngs': 90, 'historical_failures': 118, 'missing_extensions': 17}))

if __name__ == '__main__':
    main()
