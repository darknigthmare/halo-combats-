#!/usr/bin/env python3
"""Build the portable V9 catalogue from frozen V8 records and actual V9 outputs.

Run with the managed Python runtime (Pillow). Does not edit any legacy record or PNG.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / 'work/wave9'


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def write(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def urls(value):
    result = []
    def walk(item):
        if isinstance(item, dict):
            for key, child in item.items():
                if key not in ('local_ref', 'previous_local_ref', 'source_path', 'reference_path'):
                    walk(child)
        elif isinstance(item, list):
            for child in item:
                walk(child)
        elif isinstance(item, str) and item.startswith(('https://', 'http://')):
            result.append(item)
    walk(value)
    return list(dict.fromkeys(result))


def title_for(origin):
    text = origin.lower()
    for needle, key in [('infinite', 'infinite'), ('fireteam raven', 'raven'), ('wars 2', 'hw2'), ('wars', 'hw'), ('reach', 'reach'), ('odst', 'odst'), ('halo 5', 'h5'), ('halo 4', 'h4'), ('halo 3', 'h3'), ('halo 2', 'h2'), ('combat evolved', 'ce')]:
        if needle in text:
            return key
    raise ValueError('Unmapped legacy title: ' + origin)


REFERENCE_LABELS = {
    'official_extended_art_available_packet_pending': 'Illustration officielle identifiée ; dossier de vues à compléter.',
    'official_portrait_partial_packet_pending': 'Portrait officiel disponible ; corps entier et détails hors cadre à documenter.',
    'official_screen_depiction_partial_packet_pending': 'Apparition à l’écran identifiée ; vues précises à réunir.',
    'published_location_frame_packet_pending': 'Lieu publié identifié ; cadrage et géométrie à relever.',
    'published_screen_design_packet_pending': 'Design publié identifié ; dossier de références à inspecter.',
    'textual_identity_verified_visual_not_locked': 'Identité textuelle vérifiée ; apparence complète encore à documenter.',
}


def checked_asset(asset):
    path = asset['path']
    p = Path(path)
    assert not p.is_absolute() and '..' not in p.parts and p.suffix.lower() == '.png', path
    source = ROOT / p
    data = source.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    assert sha == asset['sha256'], 'Changed image: ' + path
    with Image.open(source) as im:
        im.verify()
    return asset


def new_asset(attempt, journal):
    path = attempt['path']
    review = attempt.get('review', {})
    notes = list(review.get('matches', [])) + list(review.get('reservations', []))
    if attempt.get('background_review'):
        notes.append(attempt['background_review'])
    result = {
        'id': attempt.get('asset_id') or Path(path).stem,
        'entity_id': attempt['entity_id'],
        'path': path,
        'width': attempt['width'], 'height': attempt['height'],
        'mode': attempt['mode'], 'sha256': attempt['sha256'],
        'alpha_range': attempt.get('alpha_range'),
        'alpha_bbox_threshold16': attempt.get('alpha_bbox_threshold16'),
        'margins_threshold16': attempt.get('margins_threshold16'),
        'observed_facing': review.get('observed_orientation', 'Non documentée'),
        'art_status': attempt.get('art_status', 'candidate'),
        'notes': notes, 'generation_wave': 9, 'journal': journal,
        'reference_urls': urls(attempt.get('sources', attempt.get('references', []))),
        'full_body_visible': attempt.get('full_body_visible'),
        'animation_status': 'not_animated', 'fidelity_1_to_1_certified': False,
        'automatically_mirrored': False,
        'postprocessing': attempt.get('postprocessing', 'none; original PNG bytes'),
    }
    return checked_asset(result)


def build():
    baseline = read('data/prototype_asset_bindings_v8.json')
    research = read('work/wave9/universe_research.json')
    packets = [research]
    if (WORK / 'universe_supplement.json').exists():
        packets.append(read('work/wave9/universe_supplement.json'))
    titles = {}
    sources = {}
    for packet in packets:
        for source in packet.get('sources', []):
            if source['id'] in sources:
                assert sources[source['id']]['url'] == source['url'], source['id']
            sources[source['id']] = source
        for title in packet.get('title_registry', []):
            if title['id'] not in titles:
                titles[title['id']] = dict(title)
    for title in titles.values():
        title['source_urls'] = list(dict.fromkeys(title.get('source_urls', []) + [sources[key]['url'] for key in title.get('source_ids', []) if key in sources]))

    entries = {}
    for group, kind in [('base_fighters', 'character'), ('expansion_characters', 'character'), ('bosses', 'boss'), ('stages', 'stage')]:
        for item in baseline[group]:
            work_id = title_for(item['source_game'])
            work = titles[work_id]
            assets = []
            for variant in item.get('variants', []):
                source = baseline['assets_index'][variant['id']]
                assets.append(checked_asset({
                    'id': source['id'], 'path': source['path'], 'width': source['width'], 'height': source['height'],
                    'sha256': source['sha256'], 'observed_facing': source['observed_facing'],
                    'notes': [source.get('qa', {}).get('summary', '')] + source.get('qa', {}).get('notes', []) + source.get('qa', {}).get('technical_warnings', []),
                    'art_status': source['status'], 'generation_wave': source.get('provenance', {}).get('generation_wave'),
                    'fidelity_1_to_1_certified': False, 'animation_status': 'not_animated', 'automatically_mirrored': False,
                }))
            implementation = 'Fiche consultable ; comportement spécifique et animations à produire.'
            if group == 'base_fighters':
                implementation = 'Sélectionnable dans le laboratoire V8 à mécanique commune ; moveset individuel complet et animations à produire.'
            elif item.get('mechanic_playable'):
                implementation = 'Rencontre mécanique partielle de Scarab disponible dans le laboratoire V8.'
            entries[item['id']] = {
                'id': item['id'], 'name': item['name'], 'category': kind,
                'work_id': work_id, 'work_title': work['title'], 'source_version': item['source_game'],
                'medium': work['medium'], 'continuity': 'core',
                'visual_reference_status': 'Références et réserves conservées depuis la V8 ; vues complémentaires nécessaires.' if assets else 'Identité présente en V8 ; image à produire.',
                'reference_urls': urls(item.get('sources', [])),
                'visual_lock': 'Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.',
                'art_status': item['status'], 'assets': assets, 'preferred_asset_id': item.get('preferred_asset'),
                'related_entity_id': None, 'implementation_status': implementation,
                'notes': ['Entrée héritée de la V8. Les PNG historiques sont conservés octet pour octet.'],
                'catalog_origin': 'V8', 'new_in_wave': False,
            }
    legacy_entry_count = len(entries)
    for packet in packets:
        for item in packet.get('candidates', []):
            assert item['id'] not in entries, 'Duplicate entry: ' + item['id']
            work = titles[item['work_id']]
            raw_ref = item.get('visual_reference_status', item.get('reference_status', ''))
            note = item.get('notes', [])
            note = [note] if isinstance(note, str) else list(note)
            note = [n for n in note if 'visuel non généré par cette tâche' not in n]
            if item.get('boss_role_status'):
                note.append('Rencontre de boss proposée pour Halo Combats ; le rôle de boss et ses règles ne sont pas des faits canoniques.')
            entries[item['id']] = {
                'id': item['id'], 'name': item['name'], 'category': item.get('category', item.get('kind')),
                'work_id': work['id'], 'work_title': work['title'], 'medium': work['medium'],
                'continuity': item.get('continuity', work['continuity']),
                'visual_reference_status': REFERENCE_LABELS.get(raw_ref, raw_ref),
                'source_visual_reference_status': raw_ref,
                'reference_urls': list(dict.fromkeys(item.get('reference_urls', []) + [sources[key]['url'] for key in item.get('source_ids', []) if key in sources])),
                'visual_lock': item.get('visual_lock', item.get('design_lock', '')),
                'art_status': 'missing', 'assets': [], 'preferred_asset_id': None,
                'related_entity_id': item.get('related_entity_id', item.get('existing_entity_id')),
                'implementation_status': 'Fiche de production ; intégration et animations à produire.',
                'notes': note, 'catalog_origin': 'V9', 'new_in_wave': True,
            }
    attempts = []
    new_assets = []
    for journal in ['work/wave9/root_generation.json', 'work/wave9/character_generation.json', 'work/wave9/additional_generation.json']:
        if not (ROOT / journal).exists():
            continue
        for attempt in read(journal)['attempts']:
            attempts.append({'entity_id': attempt['entity_id'], 'status': attempt['status'], 'journal': journal})
            assert attempt['entity_id'] in entries, 'Unbound generation target: ' + attempt['entity_id']
            entry = entries[attempt['entity_id']]
            if attempt['status'] != 'generated':
                entry['notes'].append('Appel V9 sans image livrée ; résultat conservé dans le journal de production.')
                continue
            asset = new_asset(attempt, journal)
            new_assets.append(asset)
            entry['assets'].append(asset)
            entry['preferred_asset_id'] = asset['id']
            entry['art_status'] = asset['art_status']
            entry['visual_reference_status'] = 'Références inspectées et comparées au candidat V9 ; réserves détaillées avec l’image.'
            entry['reference_urls'] = list(dict.fromkeys(entry['reference_urls'] + asset['reference_urls']))
            entry['notes'].append('PNG V9 livré. Pose statique ou master de décor ; animation et fidélité 1:1 non validées.')
    values = list(entries.values())
    # New deliverables first, then missing production targets, then the archive.
    values.sort(key=lambda e: (0 if any(a.get('generation_wave') == 9 for a in e['assets']) else 1 if e['new_in_wave'] else 2, e['category'], e['name'].casefold()))
    for entry in values:
        assert entry['category'] in {'character', 'costume', 'stage', 'boss'}, entry['id']
        assert entry['work_id'] in titles
        assert entry['art_status'] in {'missing', 'candidate', 'needs_correction'}
        if entry['related_entity_id']:
            assert entry['related_entity_id'] in entries, entry['related_entity_id']
        assert all(urlparse(url).scheme in ('http', 'https') for url in entry['reference_urls'])
        assert bool(entry['assets']) == (entry['art_status'] != 'missing'), entry['id']
    all_assets = {asset['id']: asset for entry in values for asset in entry['assets']}
    assert set(baseline['assets_index']) <= set(all_assets), 'Legacy asset omitted'
    assert len(all_assets) == len({asset['path'] for asset in all_assets.values()}), 'Duplicate image path'
    assert len(all_assets) == len(list((ROOT / 'assets').rglob('*.png'))), 'Uncatalogued PNG'
    counts = {
        'entries': len(values), 'legacy_entries': legacy_entry_count, 'new_entries': len(values) - legacy_entry_count,
        'titles': len(titles), 'titles_with_entries': len({e['work_id'] for e in values}),
        'announced_titles': sum(t.get('release_status') == 'announced_not_released' for t in titles.values()),
        'by_category': dict(Counter(e['category'] for e in values)),
        'new_by_category': dict(Counter(e['category'] for e in values if e['new_in_wave'])),
        'unique_png_assets': len(all_assets), 'legacy_png_assets': len(baseline['assets_index']),
        'new_png_assets': len(new_assets), 'illustrated_entries': sum(bool(e['assets']) for e in values),
        'missing_images': sum(not e['assets'] for e in values),
        'generation_calls': len(attempts), 'generation_rejections': sum(a['status'] == 'rejected' for a in attempts),
        'certified_1_to_1_assets': 0, 'new_animation_clips': 0, 'independent_parallax_layers': 0,
    }
    for title in titles.values():
        linked = [e for e in values if e['work_id'] == title['id']]
        title['catalogued_entries'] = len(linked)
        title['illustrated_entries'] = sum(bool(e['assets']) for e in linked)
        title['entity_coverage_status'] = 'partial_backlog_listed' if linked else 'coverage_pending'
    catalogue = {
        'version': 9, 'project': 'Halo Combats', 'updated_on': '2026-11-20',
        'scope': 'Catalogue de production multisuports en expansion ; registre bibliographique non exhaustif.',
        'complete_universe_inventory': False,
        'fidelity_goal': 'Respecter les incarnations 1:1 ; distinguer les zones vérifiées et les détails à documenter.',
        'titles': list(titles.values()), 'entries': values, 'counts': counts,
        'continuity_rules': research['continuity_rules'],
        'sources': list(sources.values()),
        'limitations': [
            'Une œuvre au registre ne signifie pas que tous ses personnages, costumes, lieux ou boss ont été recensés.',
            'Les nouveaux PNG sont statiques ; les images du catalogue ne sont pas de nouveaux personnages jouables.',
            'Blood Gulch et Lockout sont des adaptations de cadrage 2D en un seul plan, sans parallaxe découpée.',
            'Les projets annoncés, les éditions et les épisodes restent identifiables séparément dans le registre.',
        ],
    }
    write('data/universe_catalog_v9.json', catalogue)
    bootstrap = ROOT / 'prototype/universe_v9/catalog.js'
    bootstrap.parent.mkdir(parents=True, exist_ok=True)
    bootstrap.write_text('window.HALO_UNIVERSE_V9 = ' + json.dumps(catalogue, ensure_ascii=False) + ';\n', encoding='utf-8')
    write('data/asset_manifest_v9.json', {'version': 9, 'legacy_manifest': 'data/asset_manifest.json', 'legacy_assets_count': 94, 'new_assets': new_assets, 'all_assets': list(all_assets.values()), 'counts': counts})
    write('work/wave9/catalogue_build_report.json', {'counts': counts, 'attempts': attempts, 'unbound_pngs': [], 'duplicate_ids': [], 'all_legacy_pngs_linked': True})
    lines = ['# Halo Combats — catalogue de production V9', '', 'État du 20 novembre 2026. Recensement en cours, sans prétention d’exhaustivité.', '', f"**{len(values)} fiches**, **{len(titles)} œuvres ou composants**, **{len(all_assets)} PNG liés**.", '', '## Nouvelles fiches', '', '| Catégorie | Nom | Œuvre | Visuel |', '|---|---|---|---|']
    for e in values:
        if e['new_in_wave']:
            lines.append('| ' + ' | '.join(str(v).replace('|', '/') for v in [e['category'], e['name'], e['work_title'], e['art_status']]) + ' |')
    lines += ['', '## Registre des œuvres', '', 'Le nombre de fiches ci-dessous mesure ce qui est catalogué, pas la couverture exhaustive de chaque œuvre.', '', '| Œuvre ou composant | Média | Fiches | Illustrées | Publication |', '|---|---|---:|---:|---|']
    for t in titles.values():
        lines.append('| ' + ' | '.join(str(v).replace('|', '/') for v in [t['title'], t['medium'], t['catalogued_entries'], t['illustrated_entries'], t.get('release_status', '')]) + ' |')
    lines += ['', '## Sources', ''] + [f"- [{s['title']}]({s['url']})" for s in sources.values()]
    (ROOT / 'docs/HALO_COMBATS_CATALOGUE_V9.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps(counts, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    build()
