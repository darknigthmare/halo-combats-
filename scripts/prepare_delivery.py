from pathlib import Path
import json, hashlib, shutil, csv
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
DATA.mkdir(exist_ok=True)
jobs = json.loads((ROOT / 'work/generation_jobs.json').read_text())
assets = []
for j in jobs['active_candidates']:
    dest = ROOT / 'assets/candidates' / j['output']
    shutil.copy2(j['source_file'], dest)
    with Image.open(dest) as im:
        info = {'width': im.width, 'height': im.height, 'mode': im.mode,
                'alpha_range': im.getchannel('A').getextrema() if im.mode == 'RGBA' else None}
    asset = {k: v for k, v in j.items() if k not in ('source_file', 'imageKey')}
    asset.update(path=str(dest.relative_to(ROOT)), sha256=hashlib.sha256(dest.read_bytes()).hexdigest(), **info)
    assets.append(asset)

manifest = {k: v for k, v in jobs.items() if k != 'active_candidates'}
manifest['active_candidates'] = assets
(DATA / 'asset_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

for source, target in [('roster/roster.json', 'fighters.json'), ('roster/source_registry.json', 'fighter_sources.json'),
                       ('world/bosses.json', 'bosses.json'), ('world/stages.json', 'stages.json'), ('world/sources.json', 'world_sources.json')]:
    shutil.copy2(ROOT / 'work' / source, DATA / target)

# Rapprocher les statuts de conception avec les images effectivement livrées.
by_entity = {a['entity_id']: a for a in assets}
for filename, key in [('fighters.json', 'fighters'), ('bosses.json', 'entities'), ('stages.json', 'stages')]:
    payload = json.loads((DATA / filename).read_text())
    for item in payload[key]:
        if item['id'] in by_entity:
            item['art_status'] = 'candidate'
            item['visual_assets'] = [by_entity[item['id']]['id']]
            item['fidelity_status'] = 'not_certified'
            if isinstance(item.get('status'), dict):
                item['status']['sprite'] = 'candidate_generated'
            if key == 'stages':
                item['independent_layers_generated'] = 0
                item['master_concept_generated'] = True
        elif item['id'] == 'chief_infinite':
            item['status']['sprite'] = 'not_generated_generation_rejected'
        if item['id'] in ('chief_infinite', 'boss_scarab_h3'):
            item['prototype_reference'] = 'prototype/halo_combats_prototype.html'
            item['prototype_scope'] = 'Mécanique partielle indépendante, visuels temporaires, fiche complète non intégrée.'
    (DATA / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2))

fighters = json.loads((DATA / 'fighters.json').read_text())['fighters']
world = json.loads((DATA / 'bosses.json').read_text())['entities']
stages = json.loads((DATA / 'stages.json').read_text())['stages']

# Budgets de dessins proposés. Les poses générées n'équivalent pas à des clips.
clips = [
    ('idle', 8), ('walk_forward', 12), ('walk_backward', 12), ('dash_forward', 8), ('dash_backward', 8),
    ('crouch_enter_exit', 6), ('jump_rise', 6), ('air_fall', 4), ('landing', 4),
    ('guard_high', 4), ('guard_low', 4), ('hurt_high', 5), ('hurt_low', 5), ('hurt_air', 5),
    ('knockdown', 8), ('getup', 8), ('throw_attack', 14), ('throw_receive', 14),
    ('normal_5L', 5), ('normal_5M', 6), ('normal_5H', 8), ('normal_2L', 5), ('normal_2M', 6),
    ('normal_2H', 8), ('normal_3H', 8), ('normal_jL', 5), ('normal_jM', 6), ('normal_jH', 8),
    ('ranged_action', 12), ('ordnance_action', 12), ('special_1', 16), ('special_2', 16),
    ('special_3', 16), ('special_4', 16), ('super', 32), ('taunt', 18), ('intro', 24),
    ('victory_round', 16), ('victory_match', 24), ('defeat_round', 12), ('defeat_match', 18),
    ('finisher_1_attacker', 48), ('finisher_2_attacker', 64), ('outro', 24)
]
queue=[]
for f in fighters:
    for action, budget in clips:
        queue.append({'id':f'{f["id"]}__{action}', 'fighter_id':f['id'], 'action':action,
                      'drawings_budget_per_direction':budget, 'directions':['right','left'],
                      'status':'planned', 'generated_frames':0, 'validated_frames':0,
                      'filename_pattern':f'{f["id"]}_{action}_{{direction}}_{{frame:04d}}.png',
                      'note':'Budget indicatif de dessins, à ajuster à la chorégraphie. Les asymétries sont corrigées dans les deux directions.'})
production = {
    'version':'1.0', 'status':'planning_only', 'simulation_hz':60,
    'clips_per_fighter':len(clips), 'fighters':len(fighters), 'planned_clips':len(queue),
    'drawing_budget_both_directions':sum(x['drawings_budget_per_direction']*2 for x in queue),
    'generated_animation_frames':0, 'validated_animation_frames':0,
    'exclusions':['Réactions de finishers par famille de cible', 'Cinématiques de route en trois plans',
                  'Costumes additionnels', 'Transitions et effets propres aux boss', 'Effets VFX indépendants'],
    'clips':queue
}
(DATA / 'animation_plan.json').write_text(json.dumps(production, ensure_ascii=False, indent=2))
with (DATA / 'animation_plan.csv').open('w', newline='', encoding='utf-8-sig') as fh:
    writer=csv.writer(fh, delimiter=';')
    writer.writerow(['ID','Combattant','Action','Dessins par direction proposés','Directions','Etat','Frames produites','Frames validées'])
    for q in queue:
        writer.writerow([q['id'],q['fighter_id'],q['action'],q['drawings_budget_per_direction'],2,'Prévu',0,0])

counts = {'fighters':len(fighters), 'normals':sum(len(f['normals']) for f in fighters),
          'specials':sum(len(f['specials']) for f in fighters), 'supers':len(fighters),
          'combos':sum(len(f['combos']) for f in fighters), 'finishers':sum(len(f['finishers']) for f in fighters),
          'story_routes':len(fighters), 'boss_encounters':len(world), 'stages':len(stages),
          'planned_parallax_layers':sum(len(s['layers']) for s in stages),
          'active_visual_candidates':len(assets), 'certified_visuals':0, 'animation_clips':0,
          'planned_animation_clips':len(queue),'drawing_budget_both_directions':production['drawing_budget_both_directions']}
(DATA / 'delivery_counts.json').write_text(json.dumps(counts, ensure_ascii=False, indent=2))

lines=['# Etat de production du premier lot', '', 'Version du 19 novembre 2026.', '',
       'La bible et les registres décrivent le contenu prévu. Le prototype permet de tester une partie des mécaniques. Les quatre images du premier lot sont des candidats visuels, sans validation 1 à 1 ni animation finalisée.', '',
       '## Candidats livrés', '', '| Elément | Fichier | Contrôle restant |', '| --- | --- | --- |']
for a in assets:
    lines.append(f'| {a["entity_id"]} | {a["output"]} | {a["qa"]} |')
lines += ['', '## Génération refusée', '',
          'Master Chief Infinite a fait l’objet de deux demandes, dont une pose neutre sans arme. Les deux ont été refusées par le système automatique d’images. Aucun fichier de Chief n’est compté ni remplacé par un dessin technique dans le lot de sprites.', '',
          '## Animation à produire', '',
          f'Le plan propose {len(clips)} clips par combattant, soit {len(queue)} clips. Son budget indicatif atteint {production["drawing_budget_both_directions"]} dessins pour les deux orientations, avant costumes, réactions de finishers, cinématiques de route et VFX. Il s’agit d’un budget de production, pas d’un nombre de fichiers réalisés. Zéro clip finalisé est livré.', '',
          '## Décors à produire', '',
          'Les 24 arènes sont détaillées en 144 couches prévues. Valhalla et Mombasa disposent d’un concept maître. Aucune de ces deux images plates ne constitue un ensemble de six couches séparées. La parallaxe du prototype repose encore sur ses dessins techniques.', '',
          '## Prototype et validation', '',
          'Le prototype autonome comprend entraînement, duel IA et Scarab à trois phases. Les 17 tests de logique Node passent. Le lancement de Chromium a été bloqué par l’environnement avant ouverture de page, donc le rendu navigateur et l’ergonomie tactile restent à vérifier. Le rapport et les scénarios sont conservés dans prototype/qa.', '',
          '## Ordre recommandé pour la suite', '',
          '1. Compléter les références comparatives des quatre candidats et corriger leurs écarts visuels.',
          '2. Obtenir les poses latérales de combat du Chief et de l’Arbiter, puis leurs premiers clips de déplacement et d’attaque.',
          '3. Produire six couches de Valhalla et les modules séparés du Scarab.',
          '4. Intégrer un duel avec sprites, une route narrative et un tournoi local.',
          '5. Etendre le roster en conservant les contrôles de fidélité, de données et de jouabilité.']
(ROOT/'docs/ETAT_PRODUCTION_V1.md').write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps(counts, ensure_ascii=False))
