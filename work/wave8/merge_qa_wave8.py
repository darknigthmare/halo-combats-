#!/usr/bin/env python3
"""Merge SHA-bound V8 output reviews and read PNG metrics without editing them."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import copy
import hashlib
import importlib.util
import json

PROJECT = Path(__file__).resolve().parents[2]
WORK = PROJECT / 'work/wave8'
INPUTS = ('qa_root.json', 'qa_unsc.json', 'qa_aliens.json', 'qa_central_reviews.json', 'independent_visual_review_root.json')
spec = importlib.util.spec_from_file_location('halo_v8_png_measurement', PROJECT / 'work/wave4/consolidate_wave4.py')
v4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v4)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def collect():
    receipts = read(WORK / 'producer_freeze_receipts.json')['files']
    journal = read(WORK / 'generation_results.json')
    groups, inputs = {}, []
    for name in INPUTS:
        path = WORK / name
        if not path.is_file():
            assert name in {'qa_central_reviews.json', 'independent_visual_review_root.json'}, 'Required producer QA missing: ' + name
            continue
        digest = sha(path)
        assert receipts.get(name, {}).get('sha256') == digest, 'QA file not explicitly frozen: ' + name
        value = read(path)
        reviews = value.get('reviews', [])
        inputs.append({'path': 'work/wave8/' + name, 'sha256': digest, 'reviews': len(reviews)})
        for original in reviews:
            row = copy.deepcopy(original)
            if not row.get('source_path') and row.get('asset_path'):
                row['source_path'] = str(PROJECT / row['asset_path'])
            assert row.get('entity_id') and row.get('reviewed_utc') and row.get('sha256')
            assert row.get('verdict') in {'candidate_with_reservations', 'candidate_requires_correction'}
            assert isinstance(row.get('notes'), list) and row['notes'] and all(isinstance(n, str) for n in row['notes'])
            source = Path(row['source_path'])
            assert source.is_file() and sha(source) == row['sha256'], 'Reviewed image changed'
            if row.get('reference_path') and row.get('reference_sha256'):
                assert sha(Path(row['reference_path'])) == row['reference_sha256'], 'Independent review reference changed'
            row['review_source'] = 'work/wave8/' + name
            groups.setdefault((row['entity_id'], row['sha256']), []).append(row)
    outputs = []
    for (owner, digest), reviews in sorted(groups.items()):
        source = Path(reviews[0]['source_path'])
        metrics = v4.inspect_png(source)
        correction = any(row['verdict'] == 'candidate_requires_correction' for row in reviews)
        notes = list(dict.fromkeys(note for row in reviews for note in row['notes']))
        followup = list(dict.fromkeys(note for row in reviews for note in row.get('required_followup', [])))
        technical = metrics['technical_qa']
        if not technical['has_alpha'] or not technical['transparent_pixels'] or not technical['foreground_pixels_above_threshold']:
            correction = True
            followup.append('Reproduire une vraie silhouette sur alpha transparent ; aucune retouche automatique des pixels.')
        notes.append(f"Mesure indépendante en lecture seule : {metrics['width']} × {metrics['height']} px, {metrics['mode']}, alpha {metrics['alpha_range']}, {technical['transparent_pixels']} pixels entièrement transparents. Marges au seuil alpha >16 : {technical['canvas_margins_px_above_threshold']}. Contacts du cadre : {technical['edge_contact_pixels_above_threshold']}.")
        followup.extend(technical['warnings'])
        observed = [row['observed_facing'] for row in reviews if row.get('observed_facing')]
        choices = [row['preferred_for_scope'] for row in reviews if 'preferred_for_scope' in row]
        outputs.append({'entity_id': owner, 'source_path': str(source), 'sha256': digest,
            'reviewed_utc': max(row['reviewed_utc'] for row in reviews),
            'verdict': 'candidate_requires_correction' if correction else 'candidate_with_reservations',
            'notes': notes, 'required_followup': list(dict.fromkeys(followup)),
            'preferred_for_scope': bool(choices[-1]) and not correction if choices else False,
            'observed_facing': observed[-1] if observed else 'not_recorded',
            'image_metrics': metrics, 'contributing_reviews': reviews,
            'central_independent_visual_review': any(row['review_source'].endswith(('qa_central_reviews.json', 'independent_visual_review_root.json')) for row in reviews)})
    success_keys = set()
    for row in journal['results']:
        if row['status'] == 'generated_candidate':
            key = row['entity_id'], sha(Path(row['source_path']))
            assert key in groups, 'Generated PNG lacks output review: ' + str(key)
            success_keys.add(key)
    assert success_keys == set(groups), 'Output QA contains an image not returned by a V8 call'
    return {'wave': 8, 'review_policy': 'SHA-bound visual reviews and read-only PNG measurements; no 1:1 certification or animation.',
            'input_reviews': inputs, 'reviews': outputs}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    output = collect()
    path = WORK / 'qa_wave8.json'
    action = 'read_only'
    if args.apply:
        old = read(path) if path.is_file() else None
        if old and all(old.get(key) == value for key, value in output.items()):
            action = 'unchanged'
        else:
            output['merged_utc'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
            path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            action = 'written'
    print(json.dumps({'action': action, 'review_count': len(output['reviews']),
                      'correction_required': sum(r['verdict'] == 'candidate_requires_correction' for r in output['reviews'])}, ensure_ascii=False))

if __name__ == '__main__':
    main()
