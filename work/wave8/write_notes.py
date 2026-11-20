#!/usr/bin/env python3
"""Render V8 delivery notes from frozen facts; read-only by default."""
from pathlib import Path
import argparse
import hashlib
import json

PROJECT=Path(__file__).resolve().parents[2]
WORK=PROJECT/'work/wave8'

def read(path):return json.loads(path.read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def md(value):return str(value).replace('|','/').replace('\n',' ')

def urls(value):
    found=[]
    def walk(item):
        if isinstance(item,dict):
            for key,val in item.items():
                if key not in {'prompt','source_path','local_ref','path','asset_path'}:walk(val)
        elif isinstance(item,list):
            for val in item:walk(val)
        elif isinstance(item,str) and item.startswith(('https://','http://')) and item not in found:found.append(item)
    walk(value);return found

def render():
    baseline=read(WORK/'baseline_v7.json');journal=read(WORK/'generation_results.json');c=journal['counts']
    counts=read(PROJECT/'data/delivery_counts.json');summary=read(WORK/'consolidation_summary.json')
    manifest=read(PROJECT/'data/asset_manifest.json');fresh=[a for a in manifest['active_candidates'] if a.get('generation_wave')==8]
    assert len(fresh)==c['generated_pngs']
    catalog=read(PROJECT/'data/expansion_characters.json')['entries'];fighters=read(PROJECT/'data/fighters.json')['fighters']
    names={e['id']:e['name'] for e in catalog+fighters};missing=[e['name'] for e in catalog if not e.get('visual_assets')]
    lab_version=8 if fresh else 7
    new_names=', '.join(names[a['entity_id']] for a in fresh)
    intro=(f"La reprise V8 a produit **{len(fresh)} nouveau(x) PNG candidat(s)**"+(f" : **{new_names}**." if fresh else ".")
        +f" **{c['actual_tool_calls']} appels réels** ont été effectués sur **{c['unique_called_targets']} cibles distinctes**. "
        +f"Les autres résultats comprennent **{c['moderation_refusals']} refus `moderation_blocked`**, **{c['quota_failures']} erreur(s) de quota** et **{c['other_generation_failures']} erreur(s) technique(s)**. Les réponses du service restent conservées exactement.")
    table='\n'.join(['| Mesure | V8 / état courant |','|---|---:|',
        f"| Cibles prévues / distinctes appelées | {c['planned_targets']} / {c['unique_called_targets']} |",
        f"| Appels réellement effectués | {c['actual_tool_calls']} |",f"| Nouveaux PNG | **{len(fresh)}** |",
        f"| Nouvelles identités d’extension illustrées | {len(summary['newly_illustrated_extension_ids'])} |",
        f"| Refus `moderation_blocked` | {c['moderation_refusals']} |",
        f"| Erreurs de quota / autres erreurs techniques | {c['quota_failures']} / {c['other_generation_failures']} |",
        f"| Demandes différées sans appel | {c['deferred_without_call']} |",
        f"| PNG cumulés / anciens PNG conservés | {len(manifest['active_candidates'])} / 90 |",
        f"| Extensions avec image / encore sans image | {34-len(missing)} / {len(missing)} |",
        f"| Gardes de base disponibles | {counts['fighter_entities_with_guard_candidate']} / 24 |",
        '| Nouveaux clips d’animation / certification 1:1 | 0 / 0 |'])
    new_table=['| Personnage | Candidat | Orientation observée | Statut |','|---|---|---|---|']
    for a in fresh:
        new_table.append(f"| {md(names[a['entity_id']])} | [{a['id']}](../{a['path']}) | {md(a.get('observed_facing','non déterminée'))} | {'À corriger' if a['visual_review_status']=='reviewed_candidate_requires_correction' else 'Candidat avec réserves'} |")
    target_table=['| Cible | Objet | Appels | PNG | Résultats |','|---|---|---:|---:|---|']
    for target in baseline['target_ids']:
        calls=[r for r in journal['results'] if r['entity_id']==target];skips=[r for r in journal['deferred_requests'] if r['entity_id']==target]
        purpose='Garde statique' if target=='chief_infinite' else 'Correction des poches' if target=='dinh_infinite' else 'Première image d’extension'
        result=', '.join(dict.fromkeys(r.get('error_class') or r['status'] for r in calls)) if calls else ('Différée sans appel' if skips else 'NON COMPTABILISÉE')
        target_table.append(f"| {md(names[target])} | {purpose} | {len(calls)} | {sum(r['status']=='generated_candidate' for r in calls)} | {md(result)} |")
    attempts=['| Cible | Début UTC | Fin UTC | HTTP | Résultat |','|---|---|---|---:|---|']
    for row in journal['results']:
        attempts.append('| '+' | '.join(md(x) for x in [names[row['entity_id']],row['started_utc'],row['completed_utc'],row.get('http_status') or '—',row.get('error_class') or row['status']])+' |')
    missing_text=', '.join(missing)+'.' if missing else 'Aucune entrée ne reste sans image ; les réserves de QA demeurent.'
    sections=[]
    for a in fresh:
        e=next((e for e in catalog if e['id']==a['entity_id']),next((f for f in fighters if f['id']==a['entity_id']),{}))
        selected=a['id'] in {e.get('preferred_visual_asset'),e.get('preferred_guard_asset')}
        sections.extend([f"### {names[a['entity_id']]}",'',
            f"- Fichier : [{a['path']}](../{a['path']}).",f"- SHA-256 : `{a['sha256']}`.",
            f"- Format : {a['width']} × {a['height']} px, {a['mode']}, alpha {a.get('alpha_range')}.",
            f"- Orientation observée : {a.get('observed_facing','non déterminée')}.",
            f"- Sélection : {'préféré pour sa portée statique' if selected else 'consultable, sans candidat préféré'}.",
            '- Fidélité non certifiée ; aucune animation.','','**Observations de QA :**',''])
        sections.extend('- '+n for n in a['visual_review']['notes'])
        sections.extend(['','**Suite requise :**',''])
        sections.extend('- '+n for n in a.get('required_followup',[]));sections.append('')
    qa_path=PROJECT/'prototype/qa_v8/results.json';qa=read(qa_path) if qa_path.exists() else None
    test_text=(f"Les contrôles ciblés du catalogue V8 consignent **{qa.get('passed',0)} réussites et {qa.get('failed',0)} échec(s)** dans `prototype/qa_v8/results.json`. Ils vérifient les données et le chargement simulé ; ils ne constituent pas un examen des pixels dans un navigateur."
        if qa else "Les contrôles ciblés du catalogue V8 doivent être exécutés avant publication." if fresh else "Le code de jeu reste inchangé. Les 34 tests logiques V7 restent une preuve antérieure et ne sont pas recomptés comme tests V8.")
    integration=("Les nouveaux personnages d’extension sont consultables dans le **catalogue V8**, sans activation de leurs movesets en combat. L’entrée V8 réutilise les mécaniques et le style V7 ; son script est une copie minimale avec libellé et chemin de secours JSON V8. Le laboratoire, les bindings et les résultats V7 restent conservés. Le catalogue embarqué V8 et le JSON contiennent les mêmes données." if fresh else "Le laboratoire V7 reste inchangé ; aucun clone V8 sans nouvel art n’est créé.")
    readme=f"""# Halo Combats — V8 : reprise des personnages manquants

{intro}

{table}

## Images et catalogue

{integration}

Les images produites sont des poses statiques candidates. Les observations de transparence, d’orientation, de marges, de détails extrapolés et d’équipement restent attachées à chaque PNG. Aucune inversion horizontale, retouche ou certification 1:1 n’est appliquée automatiquement.

## Manquants

Les extensions encore sans image sont : {missing_text}

La garde du Major reste absente. Dinh conserve son candidat V6 à corriger, sans visuel préféré. Leurs demandes V8 n’ont pas produit de remplacement.

## Vérification

{test_text}

La validation visuelle interactive reste non réalisée après le blocage navigateur documenté en V7. Les 90 anciens PNG et leurs 90 fiches d’art sont conservés strictement. Les versions et journaux antérieurs restent disponibles.

- [Rapport V8](docs/HALO_COMBATS_PERSONNAGES_V8.md) et [sources V8](docs/SOURCES_PERSONNAGES_V8.md).
- [Catalogue et laboratoire V{lab_version}](prototype/halo_combats_lab_v{lab_version}.html) et [guide V{lab_version}](prototype/README_V{lab_version}.md).
- [Journal V8](work/wave8/generation_results.json), [QA des nouveaux PNG](work/wave8/qa_wave8.json), [vérification](work/wave8/verification.json).
- [Inventaire visuel courant V8](data/characters_visual_inventory_v8.csv).
- [État V7](README_V7.md), [personnages V6](docs/HALO_COMBATS_PERSONNAGES_V6.md), [bible V1](docs/HALO_COMBATS_BIBLE_V1.md).

Les modes histoire complet, tournoi, finishers animés, movesets individuels et animations restent les travaux décrits dans la bible. Les 24 identités de base partagent toujours la mécanique partielle du laboratoire.
"""
    if not fresh:readme=readme.replace('- [Inventaire visuel courant V8](data/characters_visual_inventory_v8.csv).\n','')
    report=f"""# Halo Combats — rapport V8 : nouveaux candidats et suivi des manquants

## 1. Résultat

{intro}

{table}

## 2. Candidats produits

{chr(10).join(new_table) if fresh else 'Aucun PNG produit.'}

Les PNG sont copiés sans modification de leurs octets. Une image est comptée comme candidate, pas comme animation ou silhouette certifiée 1:1.

{chr(10).join(sections)}

## 3. Cibles et résultats réels

{chr(10).join(target_table)}

Une demande différée n’est pas comptée comme appel ni refus. Aucun prompt n’a été réécrit pour contourner les refus du service. La reprise du Grunt Heavy après l’erreur de transport utilise les mêmes entrées. Le premier appel avait bien invoqué image_gen avant son échec interne de lecture de référence ; il est compté comme appel technique réel, sans HTTP ni PNG.

## 4. Journal des appels

{chr(10).join(attempts)}

Les heures sont explicitement en UTC. Les réponses brutes et références sont conservées dans les producteurs gelés. Le journal distingue réussite, modération, quota, erreur technique et report sans appel.

## 5. Intégration et conservation

{integration}

Les 34 extensions restent consultatives. Les 24 combattants de base, les 20 rencontres boss, les 24 décors et les systèmes de combat proposés restent les mêmes. Le Scarab reste la seule rencontre boss partielle ; les deux masters de décor restent des fonds en un plan.

La baseline est V7 `{baseline['baseline_commit']}`, arbre `{baseline['baseline_tree']}`, vérifiée sur 271 fichiers. Les 90 anciennes fiches d’art et PNG restent identiques. Seuls les champs d’art des entrées nouvellement illustrées évoluent : listes des images, candidat préféré et statut d’art. Les propositions de gameplay, sources et identités ne sont pas réécrites. Le Warden conserve son réemploi du PNG boss V5, sans duplication.

Les **{baseline['historical_failures']} échecs historiques** sont conservés ; **{c['generation_failures']} erreurs V8** sont ajoutées, soit **{len(manifest['failed_requests'])}** au total. Les 7 erreurs de quota V7 ne sont pas reclassées et l’échec technique V8 n’est pas compté comme refus de modération.

Un inventaire visuel V8 séparé présente l’état courant, afin de préserver les CSV historiques. Les 17 chemins propres à la publication restent exclus de l’import source : 15 fichiers historiques sont préservés et les deux index globaux sont recalculés.

## 6. Vérification et limites

{test_text}

La vérification reconstruit les appels et la QA depuis les producteurs gelés, contrôle leurs SHA, les PNG et les préférences, puis protège tous les anciens fichiers hors registres courants autorisés. Les mesures alpha et de bord sont effectuées en lecture seule ; elles ne remplacent pas la comparaison visuelle aux références.

Les réserves de chaque candidat sont conservées, même lorsque le corps entier et le canal alpha sont présents. Le rendu navigateur interactif reste non observé après le refus de permission documenté en V7 ; aucun nouvel essai ou succès visuel n’est annoncé.

## 7. Travaux encore ouverts

**Premières images :** {missing_text}

**Correction :** Dinh. **Garde :** Major. Les animations, directions complémentaires, réglages compétitifs, movesets propres, narration jouable, tournoi, finishers et autres rencontres boss restent à produire.

Les prompts et références sont conservés pour les prochaines reprises demandées. Cette livraison ne programme aucun nouvel appel automatique.

## 8. Liens

- [Journal fusionné](../work/wave8/generation_results.json), [QA fusionnée](../work/wave8/qa_wave8.json), [reçus de gel](../work/wave8/producer_freeze_receipts.json).
- [Vérification](../work/wave8/verification.json), [manifeste](../data/asset_manifest.json), [compteurs](../data/delivery_counts.json).
- [Sources V8](SOURCES_PERSONNAGES_V8.md), [laboratoire V{lab_version}](../prototype/halo_combats_lab_v{lab_version}.html).
"""
    sources=['# Halo Combats — sources et provenance V8','','La V8 réemploie les références documentées et inspectées des vagues précédentes. Les images de référence ne sont pas publiées comme assets générés. Les nouveaux candidats restent distincts de leurs sources.','','## Journaux gelés','','| Fichier | SHA-256 | Appels |','|---|---|---:|']
    for row in journal['source_journals']:sources.append(f"| [{md(row['path'])}](../{row['path']}) | `{row['sha256']}` | {row['actual_tool_calls']} |")
    sources.extend(['',f"Journal fusionné : `{sha(WORK/'generation_results.json')}`.",f"QA fusionnée : `{sha(WORK/'qa_wave8.json')}`.",'','## Références par cible',''])
    for target in baseline['target_ids']:
        links=[]
        for row in journal['results']+journal['deferred_requests']:
            if row['entity_id']==target:links.extend(url for url in urls(row) if url not in links)
        sources.extend([f"### {names[target]}",''])
        sources.extend([f'- {url}' for url in links] or ['- Voir la référence antérieure, son chemin et son SHA dans le journal producteur.'])
        sources.append('')
    sources.extend(['## Limites','','Les noms de fichiers et prompts expriment la cible demandée, pas une preuve d’orientation observée. Les notes de QA et mesures alpha décrivent la sortie réellement inspectée. Les détails masqués dans les références ne sont pas certifiés. Aucun PNG n’est annoncé comme animation ou asset 1:1 validé.',''])
    return {PROJECT/'README.md':readme,PROJECT/'README_V8.md':readme,PROJECT/'docs/HALO_COMBATS_PERSONNAGES_V8.md':report,PROJECT/'docs/SOURCES_PERSONNAGES_V8.md':'\n'.join(sources)}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    outputs=render();changes=[str(p.relative_to(PROJECT)) for p,v in outputs.items() if not p.exists() or p.read_text(encoding='utf-8')!=v]
    if args.apply:
        for path,value in outputs.items():path.write_text(value,encoding='utf-8')
    print(json.dumps({'action':'applied' if args.apply else 'read_only','changed_paths':changes},ensure_ascii=False))

if __name__=='__main__':main()
