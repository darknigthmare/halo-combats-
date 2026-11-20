#!/usr/bin/env python3
"""Consolidate frozen V8 images and errors with strict preservation of V1–V7.

Default is a read-only plan. --apply requires complete SHA-bound QA. Generated
PNG bytes are copied without modification; historical art and design stay fixed.
"""
from pathlib import Path
import argparse
import copy
import csv
import hashlib
import importlib.util
import io
import json
import shutil

PROJECT = Path(__file__).resolve().parents[2]
WORK = PROJECT / 'work/wave8'
ART_FIELDS = {'new_visual_assets', 'visual_assets', 'preferred_visual_asset', 'art_status'}
GUARD_FIELDS = {'guard_visual_assets', 'guard_art_status', 'preferred_guard_asset'}
DERIVED_PROVENANCE_FIELDS = {'source_journal_sha256', 'producer_source_journal_sha256',
    'previous_source_journal', 'previous_source_journal_sha256',
    'retry_of_journal_record', 'producer_retry_of_journal_record'}
MUTABLE_COUNTS = {'updated_utc', 'historical_generation_failures_all_waves',
    'historical_automatic_generation_rejections_all_waves',
    'active_visual_candidates', 'active_fighter_pose_candidates', 'active_guard_pose_candidates',
    'fighter_entities_with_guard_candidate', 'fighter_entities_without_guard_candidate',
    'active_expansion_character_pose_candidates', 'expansion_catalog_entries_with_visual',
    'expansion_catalog_entries_without_visual', 'expansion_catalog_entries_with_new_visual',
    'character_catalog_entities_with_visual_including_base',
    'expansion_catalog_entries_with_preferred_visual', 'expansion_catalog_entries_requiring_correction_only'}

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical_sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def is_moderation_rejection(row):
    return (row.get('error_class') == 'moderation_blocked'
        or 'moderation_blocked' in str(row.get('error', ''))
        or (row.get('status') == 'generation_rejected'
            and 'moderation rejection' in str(row.get('reason', '')).lower()))

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

def protect_catalog(current, baseline):
    assert set(current) == set(baseline)
    assert len(current['entries']) == len(baseline['entries']) == 34
    for now, old in zip(current['entries'], baseline['entries']):
        assert {k:v for k,v in now.items() if k not in ART_FIELDS} == {k:v for k,v in old.items() if k not in ART_FIELDS}, 'Extension design changed: ' + old['id']
    assert {k:v for k,v in current.items() if k not in {'entries','updated_utc'}} == {k:v for k,v in baseline.items() if k not in {'entries','updated_utc'}}

def protect_fighters(current, baseline):
    a, b = copy.deepcopy(current), copy.deepcopy(baseline)
    for doc in (a,b):
        for entity in doc['fighters']:
            if entity['id'] == 'chief_infinite':
                for key in GUARD_FIELDS:
                    entity.pop(key, None)
    assert a == b, 'Base fighter design or non-Chief art changed'

def destination(owner, scope, sha, old_assets, reserved):
    stem = owner + ('_guard_right' if scope == 'guard_static' else '_initial_right')
    old_ids = {a['id'] for a in old_assets}
    for version in range(1, 10000):
        aid = f'{stem}_v{version:02d}'
        path = PROJECT / 'assets/characters_wave8' / (aid + '.png')
        if aid in old_ids or (aid in reserved and reserved[aid] != sha):
            continue
        if path.exists() and digest(path) != sha:
            continue
        reserved[aid] = sha
        return aid, path
    raise ValueError('No unused asset version for ' + owner)

def select_preferred(assets, previous=None):
    usable = [a for a in assets if a.get('visual_review_status') != 'reviewed_candidate_requires_correction']
    marked = [a for a in usable if a.get('generation_wave') == 8 and a.get('visual_review',{}).get('preferred_for_scope')]
    assert len(marked) <= 1, 'Several new preferred candidates for the same scope'
    if marked:
        return marked[0]
    prior = next((a for a in usable if a['id'] == previous), None)
    if prior:
        return prior
    # A new image is never preferred merely because it was produced last.
    # Explicitly unselected candidates remain available only for inspection.
    return None

def bind_central(row, index, journal_sha, central_indices):
    """Bind path, hash and index at both producer and central journal levels."""
    row['producer_source_journal'] = row.pop('source_journal')
    row['producer_source_journal_sha256'] = row.pop('source_journal_sha256')
    row['producer_journal_record'] = row.pop('journal_record')
    if 'retry_of_journal_record' in row:
        retry_index = row.pop('retry_of_journal_record')
        row['producer_retry_of_journal_record'] = retry_index
        row['retry_of_journal_record'] = central_indices[(row['producer_source_journal'], retry_index)]
        assert row['retry_of_journal_record'] < index
    row.update({'source_journal':'work/wave8/generation_results.json',
        'source_journal_sha256':journal_sha,'journal_record':index})

def protect_derived_suffix(existing, expected, repair_provenance):
    if not existing or existing == expected:
        return
    assert repair_provenance, 'Existing V8 derived suffix differs; explicit provenance repair is required'
    assert len(existing) == len(expected), 'Provenance repair cannot add or remove a result'
    for old, new in zip(existing, expected):
        changed = {key for key in set(old) | set(new) if old.get(key) != new.get(key)}
        assert changed <= DERIVED_PROVENANCE_FIELDS, 'Provenance repair would change non-provenance fields: ' + str(changed)

def inventory(catalog, fighters, assets, calls):
    by_id = {a['id']:a for a in assets}
    rows = []
    for kind, entries in [('base', fighters['fighters']), ('expansion', catalog['entries'])]:
        for e in entries:
            ids = e.get('visual_assets', []) if kind == 'expansion' else [a['id'] for a in assets if a['entity_id'] == e['id'] and a['type'] == 'fighter_pose']
            preferred = by_id.get(e.get('preferred_visual_asset'), {})
            guard = by_id.get(e.get('preferred_guard_asset'), {})
            rows.append({'entity_id':e['id'], 'name':e['name'], 'roster_scope':kind,
                'game_version':e.get('game_version',e.get('era','')), 'candidate_count':len(ids),
                'preferred_asset_id':preferred.get('id',''), 'relative_path':preferred.get('path',''),
                'sha256':preferred.get('sha256',''), 'observed_facing':preferred.get('observed_facing','not_recorded'),
                'guard_asset_id':guard.get('id',''), 'guard_relative_path':guard.get('path',''),
                'art_status':e.get('art_status','candidate'), 'visual_review_status':preferred.get('visual_review_status','no_preferred_candidate'),
                'all_candidate_ids':' ; '.join(ids), 'all_candidate_paths':' ; '.join(by_id[aid]['path'] for aid in ids),
                'wave8_calls':sum(r['entity_id']==e['id'] for r in calls),
                'wave8_generated_pngs':sum(a.get('generation_wave')==8 and a['entity_id']==e['id'] for a in assets),
                'fidelity_status':'not_certified', 'animation_status':'not_animated',
                'integration_status':preferred.get('integration_status','not_integrated'),
                'gameplay_scope':'shared_partial_prototype' if kind=='base' else 'catalog_only'})
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader();writer.writerows(rows)
    return ('\ufeff'+stream.getvalue()).encode('utf-8')

def prepare(repair_provenance=False):
    baseline = read(WORK/'baseline_v7.json')
    old_assets = read(WORK/'baseline_asset_records_v7.json')['active_candidates']
    old_catalog = read(WORK/'baseline_catalog_v7.json')
    old_fighters = read(WORK/'baseline_fighters_v7.json')
    journal = read(WORK/'generation_results.json')
    merger = module('halo_wave8_merge',WORK/'merge_generation_journals.py')
    reconstructed, problems = merger.collect()
    assert not problems, problems
    assert set(journal) == set(reconstructed)|{'merged_utc'}
    assert all(journal[key] == value for key,value in reconstructed.items()), 'Journal differs from frozen producers'
    generation = journal['counts']
    journal_sha = digest(WORK/'generation_results.json')
    central_indices = {(r['source_journal'], r['journal_record']):i for i,r in enumerate(journal['results'])}
    assert len(central_indices) == len(journal['results'])
    manifest_path, counts_path = PROJECT/'data/asset_manifest.json', PROJECT/'data/delivery_counts.json'
    manifest, counts = read(manifest_path), read(counts_path)
    assert manifest['active_candidates'][:len(old_assets)] == old_assets, 'Historical active records changed'
    for asset,row in zip(old_assets,baseline['candidates']):
        assert asset['id']==row['id'] and canonical_sha(asset)==row['metadata_sha256']
        assert digest(PROJECT/asset['path'])==row['sha256'], 'Historical PNG changed: '+asset['path']
    old_failures=manifest['failed_requests'][:baseline['historical_failures']]
    assert canonical_sha(old_failures)==baseline['prior_failed_requests_sha256']
    for path,expected in baseline['registry_file_sha256'].items():
        if path not in {'data/fighters.json','data/expansion_characters.json'}:
            assert digest(PROJECT/path)==expected, 'Historical registry/prototype changed: '+path
    protect_catalog(read(PROJECT/'data/expansion_characters.json'),old_catalog)
    protect_fighters(read(PROJECT/'data/fighters.json'),old_fighters)
    for key,expected in baseline['prior_counts'].items():
        if key not in MUTABLE_COUNTS:
            assert counts[key]==expected, 'Historical count changed: '+key

    qa = read(WORK/'qa_wave8.json')
    qa_merge = module('halo_wave8_qa', WORK/'merge_qa_wave8.py')
    qa_rebuilt = qa_merge.collect()
    assert set(qa)==set(qa_rebuilt)|{'merged_utc'}
    assert all(qa[key]==value for key,value in qa_rebuilt.items()), 'QA differs from frozen reviews'
    reviews={(r['entity_id'],r['sha256']):r for r in qa['reviews']}
    fresh,failures,plans,reserved=[],[],[],{}
    old_hashes={a['sha256'] for a in old_assets}
    seen=set()
    for index,original in enumerate(journal['results']):
        owner=original['entity_id'];scope='guard_static' if owner=='chief_infinite' else 'initial_character_pose'
        assert original.get('entity_type')==('fighter' if owner=='chief_infinite' else 'expansion_character')
        assert original.get('pose_scope')==scope
        if original['status']=='generation_failed':
            row=copy.deepcopy(original)
            bind_central(row,index,journal_sha,central_indices)
            row.update({'generation_wave':8,
                'failure_category':'service_quota' if row['error_class']=='usage_limit_reached' else 'moderation' if row['error_class']=='moderation_blocked' else 'technical_generation_error'})
            failures.append(row);continue
        source=Path(original['source_path']);sha=digest(source)
        assert sha not in old_hashes and sha not in seen, 'A historical or duplicate PNG is counted as a new generation'
        seen.add(sha)
        review=reviews[(owner,sha)]
        aid,dest=destination(owner,scope,sha,old_assets,reserved)
        candidate=copy.deepcopy(original)
        for key in ('status','error','output_hint'):
            candidate.pop(key,None)
        bind_central(candidate,index,journal_sha,central_indices)
        candidate.update({'id':aid,'entity_id':owner,'type':'fighter_pose' if owner=='chief_infinite' else 'expansion_character_pose',
            'roster_scope':'base' if owner=='chief_infinite' else 'expansion','output':dest.name,
            'path':dest.relative_to(PROJECT).as_posix(),'source_path':str(source),'sha256':sha,
            'generation_wave':8,'source_journal':'work/wave8/generation_results.json','journal_record':index,
            'status':'candidate','fidelity_status':'not_certified','animation_status':'not_animated',
            'integration_status':'prototype_catalog_display','qa':' '.join(review['notes']),
            'visual_review_status':'reviewed_candidate_requires_correction' if review['verdict']=='candidate_requires_correction' else 'reviewed_candidate_with_reservations',
            'visual_review':copy.deepcopy(review),'required_followup':list(dict.fromkeys(review.get('required_followup',[])+['Validation de fidélité aux références du jeu','Animations et déclinaisons','Collisions et intégration au moteur'])),
            'target_facing':original.get('target_facing','right'),'observed_facing':review.get('observed_facing','not_recorded'),
            **review['image_metrics']})
        fresh.append(candidate);plans.append({'asset_id':aid,'entity_id':owner,'source':str(source),'destination':str(dest),'path':candidate['path'],'sha256':sha})
    assert len(fresh)==generation['generated_pngs']
    active=copy.deepcopy(old_assets)+fresh
    catalog,fighters=copy.deepcopy(old_catalog),copy.deepcopy(old_fighters)
    touched={a['entity_id'] for a in fresh}
    for entry in catalog['entries']:
        if entry['id'] not in touched:
            continue
        own=[a for a in active if a['entity_id']==entry['id'] and a['type']=='expansion_character_pose']
        entry['new_visual_assets']=[a['id'] for a in own]
        entry['visual_assets']=[a['id'] for a in own]
        best=select_preferred(own,entry.get('preferred_visual_asset'))
        if best:entry['preferred_visual_asset']=best['id']
        else:entry.pop('preferred_visual_asset',None)
        entry['art_status']='candidate' if best else 'candidate_requires_correction' if all(a.get('visual_review_status')=='reviewed_candidate_requires_correction' for a in own) else 'candidate_no_preferred'
    chief=next(f for f in fighters['fighters'] if f['id']=='chief_infinite')
    if 'chief_infinite' in touched:
        guards=[a for a in active if a['entity_id']=='chief_infinite' and a.get('pose_scope')=='guard_static']
        best=select_preferred(guards,chief.get('preferred_guard_asset'))
        chief.update({'guard_visual_assets':[a['id'] for a in guards],'guard_art_status':'candidate' if best else 'candidate_requires_correction' if all(a.get('visual_review_status')=='reviewed_candidate_requires_correction' for a in guards) else 'candidate_no_preferred'})
        if best:chief['preferred_guard_asset']=best['id']
        else:chief.pop('preferred_guard_asset',None)
    for a in fresh:
        usages=['catalog']
        if a['id']==chief.get('preferred_guard_asset'):
            usages.append('combat_guard');a['integration_status']='prototype_static_display'
        a['prototype_usage_v8']={'asset_id':a['id'],'path':a['path'],'usages':usages,'entity_ids':[a['entity_id']],'usage_scope':'static_prototype_only'}
    if fresh:catalog['updated_utc']=journal['merged_utc']
    protect_catalog(catalog,old_catalog);protect_fighters(fighters,old_fighters)
    existing_new=manifest['active_candidates'][len(old_assets):]
    protect_derived_suffix(existing_new,fresh,repair_provenance)
    existing_failures=manifest['failed_requests'][baseline['historical_failures']:]
    protect_derived_suffix(existing_failures,failures,repair_provenance)
    manifest['active_candidates']=active
    manifest['failed_requests']=old_failures+failures
    old_rejections=sum(is_moderation_rejection(row) for row in old_failures)
    total_rejections=sum(is_moderation_rejection(row) for row in manifest['failed_requests'])
    assert old_rejections==baseline['prior_counts']['historical_automatic_generation_rejections_all_waves']
    assert total_rejections==old_rejections+generation['moderation_refusals']
    manifest['updated_utc']=journal['merged_utc']
    guards=[a for a in active if a.get('pose_scope')=='guard_static' and a['type']=='fighter_pose']
    exts=[a for a in active if a['type']=='expansion_character_pose']
    covered=sum(bool(e['visual_assets']) for e in catalog['entries'])
    manifest.update({'generated_unique_entities':len({a.get('entity_id') or a['id'] for a in active}),
        'generated_guard_entities':len({a['entity_id'] for a in guards}),
        'generated_expansion_entities':len({a['entity_id'] for a in exts}),
        'illustrated_expansion_catalog_entries':covered})
    counts.update({'active_visual_candidates':len(active),
        'active_fighter_pose_candidates':sum(a['type']=='fighter_pose' for a in active),
        'active_guard_pose_candidates':len(guards),'fighter_entities_with_guard_candidate':len({a['entity_id'] for a in guards}),
        'fighter_entities_without_guard_candidate':24-len({a['entity_id'] for a in guards}),
        'active_expansion_character_pose_candidates':len(exts),'expansion_catalog_entries_with_visual':covered,
        'expansion_catalog_entries_without_visual':34-covered,
        'expansion_catalog_entries_with_new_visual':sum(bool(e['new_visual_assets']) for e in catalog['entries']),
        'character_catalog_entities_with_visual_including_base':24+covered,
        'expansion_catalog_entries_with_preferred_visual':sum(bool(e.get('preferred_visual_asset')) for e in catalog['entries']),
        'expansion_catalog_entries_requiring_correction_only':sum(e['art_status']=='candidate_requires_correction' for e in catalog['entries']),
        'visual_candidates_pre_wave8':baseline['candidate_count'],'wave8_planned_targets':generation['planned_targets'],
        'wave8_generation_attempts':generation['actual_tool_calls'],'wave8_unique_requested_targets':generation['unique_called_targets'],
        'wave8_successful_generation_attempts':len(fresh),'wave8_generation_failures':generation['generation_failures'],
        'wave8_quota_failures':generation['quota_failures'],'wave8_moderation_refusals':generation['moderation_refusals'],
        'wave8_other_generation_failures':generation['other_generation_failures'],
        'wave8_deferred_without_call':generation['deferred_without_call'],'wave8_generated_pngs':len(fresh),
        'wave8_generated_expansion_pngs':sum(a['type']=='expansion_character_pose' for a in fresh),
        'wave8_generated_guard_pngs':sum(a.get('pose_scope')=='guard_static' for a in fresh),
        'wave8_generated_correction_pngs':sum(a['entity_id']=='dinh_infinite' for a in fresh),
        'wave8_unique_expansion_entities_with_new_candidates':len({a['entity_id'] for a in fresh if a['type']=='expansion_character_pose'}),
        'historical_generation_failures_all_waves':len(manifest['failed_requests']),
        'historical_automatic_generation_rejections_all_waves':total_rejections,
        'updated_utc':journal['merged_utc']})
    summary={'wave':8,'baseline_commit':baseline['baseline_commit'],'generation':generation,
        'journal_sha256':digest(WORK/'generation_results.json'),'qa_sha256':digest(WORK/'qa_wave8.json'),
        'new_candidate_ids':[a['id'] for a in fresh],'planned_copies':plans,
        'newly_illustrated_extension_ids':[e['id'] for e,old in zip(catalog['entries'],old_catalog['entries']) if e['visual_assets'] and not old['visual_assets']],
        'remaining_missing_extension_ids':[e['id'] for e in catalog['entries'] if not e['visual_assets']],
        'new_candidates_needing_correction':[a['id'] for a in fresh if a['visual_review_status']=='reviewed_candidate_requires_correction'],
        'old_asset_records_unchanged':len(old_assets),'old_pngs_unchanged':len(old_assets),
        'new_extension_gameplay_activations':0,'new_animation_clips':0}
    outputs={manifest_path:encode(manifest),counts_path:encode(counts),WORK/'consolidation_summary.json':encode(summary)}
    if fresh:
        outputs[PROJECT/'data/expansion_characters.json']=encode(catalog)
        outputs[PROJECT/'data/characters_visual_inventory_v8.csv']=inventory(catalog,fighters,active,journal['results'])
        if 'chief_infinite' in touched:
            outputs[PROJECT/'data/fighters.json']=encode(fighters)
    changes=[str(path.relative_to(PROJECT)) for path,data in outputs.items() if not path.exists() or path.read_bytes()!=data]
    return outputs,changes,generation,plans

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--repair-derived-provenance',action='store_true',
        help='Allow only provenance field corrections in existing V8 suffixes, reconstructed from frozen producers')
    args=parser.parse_args()
    outputs,changes,generation,plans=prepare(repair_provenance=args.repair_derived_provenance)
    if args.apply:
        for plan in plans:
            target=Path(plan['destination']);target.parent.mkdir(parents=True,exist_ok=True)
            if not target.exists():shutil.copyfile(plan['source'],target)
            assert digest(target)==plan['sha256']
        for path,data in outputs.items():
            if path.exists() and path.read_bytes()==data:continue
            temporary=path.with_suffix(path.suffix+'.wave8.tmp')
            temporary.write_bytes(data);temporary.replace(path)
    print(encode({'action':'applied' if args.apply else 'read_only','changed_paths':changes,'generation':generation,'png_copies':len(plans)}).decode())

if __name__=='__main__':
    main()
