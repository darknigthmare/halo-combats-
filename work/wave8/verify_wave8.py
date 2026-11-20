#!/usr/bin/env python3
"""Verify frozen V8 art, accounting, catalog integration and publication scope.

Default: read-only. --write saves evidence. --snapshot-to copies only the
verified V8 delivery into a new immutable snapshot, without touching Git.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import importlib.util
import json
import shutil
from PIL import Image

PROJECT=Path(__file__).resolve().parents[2]
WORK=PROJECT/'work/wave8'
spec=importlib.util.spec_from_file_location('halo_v8_consolidator',WORK/'consolidate_wave8.py')
v8=importlib.util.module_from_spec(spec);spec.loader.exec_module(v8)
CENTRAL=['README.md','README_V8.md','data/asset_manifest.json','data/delivery_counts.json',
    'data/expansion_characters.json','data/characters_visual_inventory_v8.csv',
    'data/prototype_asset_bindings_v8.json','docs/HALO_COMBATS_PERSONNAGES_V8.md',
    'docs/SOURCES_PERSONNAGES_V8.md','prototype/halo_combats_lab_v8.html',
    'prototype/README_V8.md','prototype/lab_v8/app.js','prototype/lab_v8/catalog.js']

def read(rel):return v8.read(PROJECT/rel)

def import_files():
    names=set(CENTRAL)
    for directory in (WORK,PROJECT/'prototype/qa_v8',PROJECT/'assets/characters_wave8'):
        for path in directory.rglob('*'):
            if not path.is_file() or '__pycache__' in path.parts or path.name.endswith(('.pyc','.tmp')):continue
            assert not path.is_symlink()
            if directory==WORK:assert path.suffix.lower() not in {'.png','.jpg','.jpeg','.webp'}, 'Reference images remain outside Git'
            names.add(path.relative_to(PROJECT).as_posix())
    return sorted(names)

def verify():
    baseline=read('work/wave8/baseline_v7.json');repo=read('work/wave8/baseline_repository_files.json')
    manifest=read('data/asset_manifest.json');counts=read('data/delivery_counts.json')
    journal=read('work/wave8/generation_results.json');qa_art=read('work/wave8/qa_wave8.json')
    outputs,changes,generation,plans=v8.prepare()
    assert not changes, 'Consolidation is incomplete: '+str(changes)
    assert generation=={'planned_targets':19,'actual_tool_calls':20,'unique_called_targets':19,
        'generated_pngs':4,'generation_failures':16,'quota_failures':0,'moderation_refusals':15,
        'other_generation_failures':1,'deferred_without_call':0}
    producer_files={row['path']:row['sha256'] for row in journal['source_journals']}
    producer_records={path:read(path)['results'] for path in producer_files}
    for row in journal['results']:
        assert row['source_journal_sha256']==producer_files[row['source_journal']]==v8.digest(PROJECT/row['source_journal'])
        original=producer_records[row['source_journal']][row['journal_record']]
        assert all(row[key]==original[key] for key in ('entity_id','prompt','status'))
        if row.get('previous_source_journal'):
            assert v8.digest(PROJECT/row['previous_source_journal'])==row['previous_source_journal_sha256']
        if 'retry_of_journal_record' in row:
            earlier=producer_records[row['source_journal']][row['retry_of_journal_record']]
            assert earlier['entity_id']==row['entity_id'] and earlier['error_class']=='reference_transport_closed'
            assert earlier['prompt']==row['prompt']
    active=manifest['active_candidates'];fresh=[a for a in active if a.get('generation_wave')==8]
    expected_new={'locke_h5','mickey_odst','skirmisher_champion_reach','bassus_infinite'}
    assert len(active)==len({a['id'] for a in active})==len({a['sha256'] for a in active})==94
    assert {a['entity_id'] for a in fresh}==expected_new and len(fresh)==4
    assert len(manifest['failed_requests'])==counts['historical_generation_failures_all_waves']==134
    cumulative_rejections=sum(v8.is_moderation_rejection(row) for row in manifest['failed_requests'])
    cumulative_quota=sum(row.get('error_class')=='usage_limit_reached' or 'usage_limit_reached' in str(row.get('error','')) for row in manifest['failed_requests'])
    cumulative_other=len(manifest['failed_requests'])-cumulative_rejections-cumulative_quota
    assert cumulative_rejections==counts['historical_automatic_generation_rejections_all_waves']==126
    assert cumulative_quota==counts['historical_service_quota_failures_all_waves']==7
    assert cumulative_other==1 and 134==cumulative_rejections+cumulative_quota+cumulative_other
    central_journal_sha=v8.digest(WORK/'generation_results.json')
    derived=fresh+manifest['failed_requests'][118:]
    assert len(derived)==20
    for row in derived:
        assert row['source_journal']=='work/wave8/generation_results.json'
        assert row['source_journal_sha256']==central_journal_sha
        source=journal['results'][row['journal_record']]
        assert row['entity_id']==source['entity_id'] and row['prompt']==source['prompt']
        assert row['producer_source_journal']==source['source_journal']
        assert row['producer_source_journal_sha256']==source['source_journal_sha256']
        assert row['producer_journal_record']==source['journal_record']
        if 'retry_of_journal_record' in source:
            assert row['producer_retry_of_journal_record']==source['retry_of_journal_record']
            earlier=journal['results'][row['retry_of_journal_record']]
            assert earlier['source_journal']==row['producer_source_journal']
            assert earlier['journal_record']==row['producer_retry_of_journal_record']
            assert earlier['entity_id']==row['entity_id'] and earlier['error_class']=='reference_transport_closed'
    retry=next(row for row in derived if 'producer_retry_of_journal_record' in row)
    assert retry['entity_id']=='grunt_heavy_reach' and retry['journal_record']==19
    assert retry['producer_retry_of_journal_record']==4 and retry['retry_of_journal_record']==16
    assert len(qa_art['reviews'])==4
    assert all(r['central_independent_visual_review'] for r in qa_art['reviews'])
    assert {p.relative_to(PROJECT).as_posix() for p in (PROJECT/'assets').rglob('*.png')}=={a['path'] for a in active}
    for a in active:
        assert v8.digest(PROJECT/a['path'])==a['sha256']
        assert a['fidelity_status']=='not_certified' and a['animation_status']=='not_animated'
    for a in fresh:
        with Image.open(PROJECT/a['path']) as image:
            assert 'A' in image.getbands()
            measured_alpha=list(image.getchannel('A').getextrema())
        assert a['alpha_range']==measured_alpha
        assert measured_alpha[0]==0 and 0<measured_alpha[1]<=255
        assert a['technical_qa']['transparent_pixels']>0 and a['technical_qa']['foreground_pixels_above_threshold']>0
        assert a['visual_review_status']=='reviewed_candidate_with_reservations'
        assert a['visual_review']['preferred_for_scope'] is True
        assert a['prototype_usage_v8']['usages']==['catalog']
        assert a['integration_status']=='prototype_catalog_display'
    catalog=read('data/expansion_characters.json')['entries']
    assert len(catalog)==34 and sum(bool(e['visual_assets']) for e in catalog)==21
    assert counts['expansion_catalog_entries_without_visual']==13
    for e in catalog:
        if e['id'] in expected_new:
            a=next(a for a in fresh if a['entity_id']==e['id']);assert e['preferred_visual_asset']==a['id']
    dinh=next(e for e in catalog if e['id']=='dinh_infinite')
    assert not dinh.get('preferred_visual_asset') and dinh['art_status']=='candidate_requires_correction'
    assert counts['fighter_entities_with_guard_candidate']==23
    assert counts['animation_clips']==counts['certified_visuals']==0
    for name,receipt in read('work/wave8/producer_freeze_receipts.json')['files'].items():
        assert v8.digest(WORK/name)==receipt['sha256'], 'Frozen producer file changed: '+name
    binding=read('data/prototype_asset_bindings_v8.json');prior_binding=read('data/prototype_asset_bindings_v7.json')
    assert binding['wave']==8 and len(binding['assets_index'])==94
    for aid,asset in prior_binding['assets_index'].items():assert binding['assets_index'][aid]==asset, 'Prior runtime asset changed: '+aid
    for group in ('base_fighters','bosses','stages'):assert binding[group]==prior_binding[group]
    usage={name:sum(name in row['usages'] for row in binding['asset_usages']) for name in ('catalog','combat_neutral','combat_guard','boss','stage')}
    assert usage=={'catalog':94,'combat_neutral':24,'combat_guard':23,'boss':1,'stage':2}
    for a in fresh:
        row=next(row for row in binding['asset_usages'] if row['asset_id']==a['id']);assert row==a['prototype_usage_v8']
    qa=read('prototype/qa_v8/results.json')
    assert qa['failed']==0 and qa['passed']>0
    assert qa['status']=='passed_with_browser_not_run'
    browser=qa['browser_validation'];assert browser['status']=='not_run' and browser.get('attempted_by_this_script') is False
    assert browser.get('attempts_v8')==0
    tested={row['path'] for row in qa['tested_files']}
    assert {'prototype/halo_combats_lab_v8.html','prototype/lab_v8/app.js','prototype/lab_v8/catalog.js','data/prototype_asset_bindings_v8.json'}<=tested
    for row in qa['tested_files']:assert v8.digest(PROJECT/row['path'])==row['sha256'], 'A file changed after V8 tests: '+row['path']
    binding_qa=read('work/wave8/prototype_bindings_validation.json')
    assert binding_qa['result']=='pass' and binding_qa['json_bootstrap_parity'] is True
    assert binding_qa['binding_sha256']==v8.digest(PROJECT/'data/prototype_asset_bindings_v8.json')
    assert binding_qa['bootstrap_sha256']==v8.digest(PROJECT/'prototype/lab_v8/catalog.js')
    notes=v8.module('halo_v8_notes',WORK/'write_notes.py').render()
    assert all(path.read_text(encoding='utf-8')==value for path,value in notes.items()), 'Notes differ from final evidence'
    allowed={'README.md','data/asset_manifest.json','data/delivery_counts.json','data/expansion_characters.json'}
    excluded=set(repo['source_differences_at_capture']);assert len(excluded)==17
    immutable=[]
    for row in repo['files']:
        if row['path'] in allowed or row['path'] in excluded:continue
        assert v8.digest(PROJECT/row['path'])==row['sha256'], 'Historical source file changed: '+row['path']
        immutable.append(row['path'])
    names=import_files();assert not excluded.intersection(names)
    assert all((PROJECT/name).is_file() for name in names)
    return {'wave':8,'status':'passed_with_browser_not_run','checked_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'baseline_commit':repo['baseline_commit'],'baseline_tree':repo['baseline_tree'],'generation':generation,
        'new_png_count':4,'new_extension_identities':sorted(expected_new),'current_png_count':94,
        'old_pngs_preserved':90,'old_asset_records_preserved':90,'historical_failures_preserved':118,
        'old_registry_designs_preserved':True,'old_v7_prototype_files_preserved':True,
        'historical_source_files_preserved':len(immutable),'publication_specific_files_preserved':sorted(excluded-{'PUBLICATION_INVENTORY.json','SHA256SUMS.txt'}),
        'global_indexes_to_recompute':['PUBLICATION_INVENTORY.json','SHA256SUMS.txt'],
        'prototype_usage_counts':usage,'prototype_test_report':'prototype/qa_v8/results.json',
        'prototype_test_report_sha256':v8.digest(PROJECT/'prototype/qa_v8/results.json'),
        'prototype_tests_passed':qa['passed'],'prototype_tests_failed':qa['failed'],'prototype_tested_files':qa['tested_files'],
        'browser_validation':browser,'new_extension_gameplay_activations':0,'new_animation_clips':0,
        'central_consolidation_idempotent':True,'generation_journal_sha256':v8.digest(WORK/'generation_results.json'),
        'cumulative_failure_partition':{'moderation_rejections':cumulative_rejections,'service_quota':cumulative_quota,'other_failures':cumulative_other,'total':len(manifest['failed_requests'])},
        'provenance_verified':{'producer_path_sha_pairs':20,'derived_central_and_producer_path_sha_pairs':20,
            'grunt_retry_producer_record':4,'grunt_retry_central_record':16,'frozen_files':len(read('work/wave8/producer_freeze_receipts.json')['files'])},
        'art_qa_sha256':v8.digest(WORK/'qa_wave8.json'),'counts':counts}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');parser.add_argument('--snapshot-to',type=Path);args=parser.parse_args()
    evidence=verify()
    if args.write or args.snapshot_to:(WORK/'verification.json').write_bytes(v8.encode(evidence))
    result={'verified':True,'status':evidence['status'],'generation':evidence['generation'],'prototype_tests_passed':evidence['prototype_tests_passed'],'browser_validation':evidence['browser_validation']}
    if args.snapshot_to:
        target=args.snapshot_to.resolve();assert not target.exists() and PROJECT not in target.parents
        rows=[{'path':name,'bytes':(PROJECT/name).stat().st_size,'sha256':v8.digest(PROJECT/name)} for name in import_files()]
        for row in rows:
            source=PROJECT/row['path'];dest=target/'files'/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
            assert v8.digest(source)==v8.digest(dest)==row['sha256']
        inv={'wave':8,'baseline_commit':evidence['baseline_commit'],'baseline_tree':evidence['baseline_tree'],'file_count':len(rows),'files':rows,
            'counts':evidence['counts'],'verification_status':evidence['status'],'browser_validation':evidence['browser_validation']}
        (target/'FILES_SHA256.json').write_bytes(v8.encode(inv))
        (target/'SHA256SUMS.txt').write_text(''.join(row['sha256']+'  files/'+row['path']+'\n' for row in rows),encoding='utf-8')
        result.update({'snapshot':str(target),'snapshot_files':len(rows),'snapshot_inventory_sha256':v8.digest(target/'FILES_SHA256.json')})
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
