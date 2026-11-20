#!/usr/bin/env python3
"""Capture the verified V6 state before V7 changes; refuses to overwrite evidence."""
from pathlib import Path
import copy, hashlib, importlib.util, json, subprocess

PROJECT = Path(__file__).resolve().parents[2]
WORK = PROJECT / 'work/wave7'
REPO = PROJECT.parent / 'halo_combats_publish'
BASE = '8c4dff83b48611a3439d67e1c15a3e0326b2a1ec'
TREE = '02d1deabd412fe64b4f41473df5c03607ce93ff6'
spec = importlib.util.spec_from_file_location('halo_v6_helpers', PROJECT/'work/wave6/consolidate_wave6.py')
v6 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v6)

def git(*args): return subprocess.check_output(['git', *args], cwd=REPO)
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def write(name, data):
    path = WORK / name
    assert not path.exists(), 'Baseline already exists: ' + name
    path.write_text(v6.json_text(data), encoding='utf-8')

def main():
    WORK.mkdir(exist_ok=True)
    assert git('rev-parse','HEAD').decode().strip() == BASE
    assert git('rev-parse','HEAD^{tree}').decode().strip() == TREE
    assert not git('status','--porcelain').strip()
    rows, differences = [], []
    for raw in git('ls-tree','-rlz','HEAD').split(b'\0'):
        if not raw: continue
        info, path = raw.split(b'\t',1)
        mode, kind, blob, size = info.decode().split(); path = path.decode()
        published = REPO / path
        data = published.read_bytes()
        assert len(data) == int(size)
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == blob
        digest = hashlib.sha256(data).hexdigest()
        rows.append({'path':path,'mode':mode,'type':kind,'git_sha':blob,'bytes':len(data),'sha256':digest})
        source = PROJECT / path
        if not source.is_file() or v6.digest(source) != digest: differences.append(path)
    assert len(rows) == 236
    prior_exclusions = set(read(PROJECT/'work/wave6/baseline_repository_files.json')['source_differences_at_capture'])
    assert set(differences) == prior_exclusions, 'Unexpected divergence between source and published checkout'
    write('baseline_repository_files.json',{'baseline_commit':BASE,'baseline_tree':TREE,'file_count':len(rows),'files':rows,'source_differences_at_capture':differences})
    manifest = read(PROJECT/'data/asset_manifest.json')
    counts = read(PROJECT/'data/delivery_counts.json')
    roster = read(PROJECT/'data/fighters.json')
    catalog = read(PROJECT/'data/expansion_characters.json')
    assert len(manifest['active_candidates']) == 90 and len(manifest['failed_requests']) == 111
    allowed = ['guard_visual_assets','guard_art_status','preferred_guard_asset']
    art_fields = ['new_visual_assets','visual_assets','preferred_visual_asset','art_status']
    baseline = {'generation_wave':7,'baseline_commit':BASE,'candidate_count':90,
        'candidates':[{'id':a['id'],'path':a['path'],'sha256':a['sha256'],'metadata_sha256':v6.canonical_sha(a)} for a in manifest['active_candidates']],
        'prior_counts':counts,'historical_failures':111,'prior_failed_requests_sha256':v6.canonical_sha(manifest['failed_requests']),
        'registry_structure':{'chief_allowed_fields':allowed,'fighters_protected_sha256':v6.canonical_sha(v6.protected_roster(roster,allowed)),
            'bosses_protected_sha256':v6.canonical_sha(read(PROJECT/'data/bosses.json')),
            'neutral_preferences':{f['id']:f.get('preferred_visual_asset') for f in roster['fighters']},
            'chief_original_guard_assets':next(f for f in roster['fighters'] if f['id']=='chief_infinite').get('guard_visual_assets',[])},
        'catalog_art_fields':art_fields,'catalog_entry_ids':[e['id'] for e in catalog['entries']],
        'catalog_protected_metadata_sha256':{e['id']:v6.canonical_sha({k:v for k,v in e.items() if k not in art_fields}) for e in catalog['entries']},
        'missing_extension_ids':[e['id'] for e in catalog['entries'] if not e['visual_assets']],
        'correction_ids':['dinh_infinite'],'target_ids':[e['id'] for e in catalog['entries'] if not e['visual_assets']]+['dinh_infinite','chief_infinite']}
    assert len(baseline['target_ids']) == 19
    write('baseline_v6.json',baseline)
    for name, source in [('baseline_catalog_v6.json',PROJECT/'data/expansion_characters.json'),('README_V6_before_wave7.md',PROJECT/'README.md')]:
        dest = WORK/name
        assert not dest.exists()
        dest.write_bytes(source.read_bytes())
    print(json.dumps({'captured':True,'files':len(rows),'publication_specific_differences':len(differences),'candidates':90,'historical_failures':111,'target_ids':baseline['target_ids']}))

if __name__=='__main__': main()
