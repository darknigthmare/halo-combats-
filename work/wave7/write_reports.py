#!/usr/bin/env python3
"""Write the V7 delivery notes from frozen journals, bindings and actual QA."""
from pathlib import Path
import hashlib
import json

PROJECT = Path(__file__).resolve().parents[2]
WORK = PROJECT / 'work/wave7'

def read(rel): return json.loads((PROJECT / rel).read_text(encoding='utf-8'))
def sha(rel): return hashlib.sha256((PROJECT / rel).read_bytes()).hexdigest()
def md(value): return str(value).replace('|', '\\|').replace('\n', ' ')
def links(value):
    result = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key not in {'prompt', 'error'}: result.extend(links(child))
    elif isinstance(value, list):
        for child in value: result.extend(links(child))
    elif isinstance(value, str) and value.startswith(('https://', 'http://')):
        result.append(value)
    return list(dict.fromkeys(result))

def main():
    journal = read('work/wave7/generation_results.json')
    counts = read('data/delivery_counts.json')
    bindings = read('data/prototype_asset_bindings_v7.json')
    qa = read('prototype/qa_v7/results.json')
    catalog = read('data/expansion_characters.json')
    fighters = read('data/fighters.json')['fighters']
    entries = {entry['id']: entry for entry in catalog['entries']}
    names = {e['id']: e['name'] for e in catalog['entries']}
    names.update({f['id']: f['name'] for f in fighters})
    assert journal['counts']['actual_tool_calls'] == 7 and journal['counts']['deferred_without_call'] == 12
    assert counts['wave7_generated_pngs'] == 0 and counts['active_visual_candidates'] == 90
    assert qa['failed'] == 0 and qa['passed'] > 0
    browser = qa['browser_validation']
    browser_note = ('Le navigateur a été exécuté avec succès, selon le rapport lié ci-dessous.' if browser['status'] == 'passed'
                    else 'La validation dans un navigateur est bloquée avant le chargement de la page. Motif consigné : ' + md(browser['reason']) + '. Aucune validation visuelle interactive n’est revendiquée.')
    missing = [entry['name'] for entry in catalog['entries'] if not entry['visual_assets']]
    common_counts = '''| Mesure | V7 / état cumulé |
|---|---:|
| Cibles de génération prévues en V7 | 19 |
| Appels de génération réellement effectués | 7 |
| Erreurs de quota `HTTP 429 usage_limit_reached` | 7 |
| Nouveaux refus de modération | 0 |
| Demandes différées sans appel | 12 |
| Nouveaux PNG | **0** |
| PNG candidats existants conservés | **90** |
| Combattants de base sélectionnables dans le laboratoire | 24 |
| Entrées d’extension consultables, non sélectionnables en combat | 34 |
| Extensions illustrées / encore sans image | 17 / 17 |
| Gardes statiques du roster de base | 23 / 24 |
| Boss documentés / avec mécanique partielle dans le laboratoire | 20 / 1 |
| Décors documentés / masters plats disponibles | 24 / 2 |
| Nouveaux clips d’animation / visuels certifiés 1:1 | 0 / 0 |'''
    readme = f'''# Halo Combats — V7 : laboratoire visuel et suivi de génération

La V7 ajoute un **laboratoire jouable utilisant les PNG existants** et un catalogue consultable des personnages, boss et décors. Les **90 fichiers d’image restent identiques** ; l’affichage conserve chaque pose native, sans miroir horizontal. Les 24 profils de base partagent les mécaniques partielles du laboratoire ; leurs movesets complets restent à implémenter.

La reprise des personnages manquants a rencontré la limite globale du service d’image : **7 appels ont reçu une erreur de quota, puis 12 demandes ont été différées sans appel**. **Aucun nouveau personnage illustré ni PNG n’a été généré dans cette vague.** Les 111 refus de génération antérieurs restent conservés séparément des 7 erreurs de quota V7.

{common_counts}

## Ouvrir le laboratoire

Ouvrir [halo_combats_lab_v7.html](prototype/halo_combats_lab_v7.html) depuis une copie complète du dépôt. Le catalogue embarqué permet l’ouverture locale ; conserver les dossiers `assets`, `data` et `prototype` ensemble. Les commandes et scénarios sont détaillés dans le [guide du laboratoire](prototype/README_V7.md).

Le laboratoire propose les 24 profils de base, affiche les poses neutres et les 23 gardes disponibles, et présente séparément les 34 extensions. Les 20 boss peuvent être consultés ; le **Scarab** seul conserve la mécanique partielle déjà présente dans le précédent prototype. Les deux masters de décor sont utilisés comme images plates ; les 22 autres décors indiquent leur image manquante. Aucun calque indépendant de parallaxe ni nouvelle animation de personnage n’est livré.

## Vérification et portée réelle

Le rapport de test consigne **{qa['passed']} vérifications réussies et {qa['failed']} échec** pour les contrôles effectivement exécutés. {browser_note}

L’intégration déclarée dans le manifeste correspond précisément aux usages du [binding V7](data/prototype_asset_bindings_v7.json) : **50 PNG** possèdent un usage d’affichage statique dans le laboratoire et **40** un usage de catalogue seul. Les 90 restent consultables au catalogue, variantes comprises. Cette intégration conserve les réserves de QA, les orientations, les préférences et les états `not_certified` / `not_animated`.

Les **17 extensions sans image** restent : {', '.join(missing)}. La garde du Major manque toujours. L’image existante de Dinh reste à corriger et sans candidat préféré ; elle est consultable avec son avertissement.

Les **33 propositions de combat d’extension de V6**, leurs 132 pistes de spéciaux, 33 supers, 33 finishers et 33 parcours courts sont conservées comme propositions antérieures. Elles ne sont pas recomptées comme nouveautés V7 ni activées en combat. Les modes histoire complet, tournoi, finishers animés, movesets individuels complets et autres rencontres boss restent à réaliser.

## Livrables et historique

- [Laboratoire V7](prototype/halo_combats_lab_v7.html), [guide](prototype/README_V7.md) et [tests reproductibles](prototype/qa_v7/).
- [Rapport de livraison V7](docs/HALO_COMBATS_PERSONNAGES_V7.md) et [sources V7](docs/SOURCES_PERSONNAGES_V7.md).
- [Journal V7 : appels et reports](work/wave7/generation_results.json), [vérification de conservation](work/wave7/verification.json).
- [Manifeste des 90 images](data/asset_manifest.json), [compteurs](data/delivery_counts.json), [binding du laboratoire](data/prototype_asset_bindings_v7.json).
- [Catalogue des 34 extensions](data/expansion_characters.json), [inventaire visuel V6 conservé](data/expansion_characters_visual_inventory.csv) et [propositions détaillées V6](docs/HALO_COMBATS_PERSONNAGES_V6.md).
- [Livraison V6 conservée](README_V6.md), [V5 : gardes et Boss Battle](README_V5.md), [V4](README_V4.md), [V3](README_V3.md), [V2](README_V2.md).
- [Bible V1](docs/HALO_COMBATS_BIBLE_V1.md), [bible DOCX](docs/HALO_COMBATS_BIBLE_V1.docx) et [prototype précédent conservé](prototype/halo_combats_prototype.html).

La V7 reste une adaptation expérimentale. Les images candidates ne sont pas certifiées fidèles 1:1 ; les documents distinguent les spécifications proposées, l’art statique et le comportement réellement codé.
'''
    called = {row['entity_id']: row for row in journal['results']}
    deferred = {row['entity_id']: row for row in journal['deferred_requests']}
    target_rows = []
    baseline = read('work/wave7/baseline_v6.json')
    for eid in baseline['target_ids']:
        purpose = 'Première image d’extension' if eid in baseline['missing_extension_ids'] else ('Correction de l’image existante' if eid == 'dinh_infinite' else 'Garde statique manquante')
        outcome = 'Appel réel — quota HTTP 429, aucune image' if eid in called else 'Différée — aucun appel effectué'
        art = 'Image toujours absente' if eid in baseline['missing_extension_ids'] else ('Candidat V6 à corriger, sans préféré' if eid == 'dinh_infinite' else 'Pose neutre conservée ; garde absente')
        target_rows.append('| ' + ' | '.join(md(value) for value in (names[eid], eid, purpose, outcome, art)) + ' |')
    call_rows = []
    for row in journal['results']:
        call_rows.append('| ' + ' | '.join(md(v) for v in (names[row['entity_id']], row['started_utc'], row['completed_utc'], '429', 'usage_limit_reached', row['source_journal'])) + ' |')
    report = f'''# Halo Combats — rapport V7 : art conservé, génération interrompue et laboratoire

## 1. Résultat de cette livraison

La V7 fait passer les images existantes dans un laboratoire visuel autonome, avec sélection des 24 profils de base et consultation séparée des extensions, boss et décors. Elle n’ajoute **aucun PNG**. Les sept appels réellement partis vers le service de génération ont tous échoué sur la limite globale d’usage ; les douze autres demandes n’ont pas été envoyées.

{common_counts}

Le registre cumule désormais **118 échecs de génération réels** : les **111 refus antérieurs**, conservés byte pour byte dans leur préfixe logique, et **7 erreurs de quota**. Le nombre de refus automatiques de modération reste 111. Une demande différée ne compte ni comme appel, ni comme rejet, ni comme image produite.

## 2. Les 19 cibles et leur état réel

| Personnage | Identifiant stable | Objet prévu | Résultat V7 | État de l’art après V7 |
|---|---|---|---|---|
{chr(10).join(target_rows)}

Les dix-sept extensions manquantes restent donc manquantes. L’image de Dinh possède toujours sa réserve sur le côté anatomique des poches bleues ; aucun remplacement n’existe. Le Major conserve son image neutre et n’a toujours pas de garde statique. Aucun visuel de référence téléchargé n’a été substitué à une image manquante.

## 3. Preuve des appels effectués

| Cible | Début UTC | Fin UTC | HTTP | Classe d’erreur | Journal producteur |
|---|---|---|---:|---|---|
{chr(10).join(call_rows)}

Les réponses brutes, prompts, références et liens de provenance sont conservés dans les journaux producteurs. La fusion indique leur SHA-256 et sépare `results` de `deferred_requests`. Les enregistrements de quota sont ajoutés au journal historique avec `failure_category: service_quota` ; aucun report n’y est ajouté. Aucun fallback de génération ni reprise automatique n’est programmé par cette livraison.

## 4. Ce que le laboratoire utilise

| Usage déclaré dans le binding | PNG distincts pour cet usage | Portée |
|---|---:|---|
| `catalog` | 90 | Toutes les variantes existantes peuvent être consultées avec leur QA |
| `combat_neutral` | 24 | Une pose neutre préférée par profil de base |
| `combat_guard` | 23 | Gardes statiques existantes ; aucun substitut pour le Major |
| `boss` | 1 | Image du Scarab pour la mécanique partielle existante |
| `stage` | 2 | Deux masters affichés en un seul plan chacun |

Ces usages se recoupent : les 50 PNG utilisés par le laboratoire sont aussi au catalogue. **50 + 40 = 90 fichiers uniques** ; le tableau d’usages ne représente pas cinq lots additionnables.

Les poses gardent leur orientation native. Le Warden V5 reste une seule image, liée à son entrée boss et à son entrée d’extension, sans nouvelle génération ni copie comptée deux fois. Les variantes à corriger restent accessibles avec leur réserve ; elles ne deviennent pas des préférés. Les 34 extensions sont consultatives et ne sont pas activées dans la sélection de combat.

Les 24 profils de base partagent le noyau mécanique partiel du laboratoire. Leurs fiches de données demeurent des spécifications proposées ; cette livraison ne prétend pas implémenter leurs 264 normales, 96 spéciaux, 24 supers, 48 combos, 48 finishers et 24 routes narratives. Les 19 autres boss restent consultatifs, même lorsqu’un profil PNG existe.

## 5. Conservation stricte des versions antérieures

La baseline publiée est le commit `{baseline['baseline_commit']}`. Son arbre comporte 236 fichiers. Les 17 chemins propres à la publication restent exclus de l’import source V7 : 15 fichiers historiques, dont les archives et adaptations de portabilité, sont conservés à l’identique ; les deux index globaux `PUBLICATION_INVENTORY.json` et `SHA256SUMS.txt` sont recalculés pour l’arbre livré.

Les **90 SHA-256 des PNG** restent inchangés. Pour leurs 90 fiches actives, seuls `integration_status` et `prototype_usage_v7` sont autorisés à évoluer. Le second champ recopie exactement l’entrée correspondante de `asset_usages` ; le premier vaut `prototype_static_display` pour les 50 usages du laboratoire et `prototype_catalog_display` pour les 40 usages de catalogue seul. Le vérificateur reconstruit les usages attendus depuis les préférés figés des inventaires et registres ; cette exception n’autorise aucune autre modification de métadonnées.

Les identifiants, propriétaire d’origine, type, chemin, SHA, pose, orientation, équipements, prompts, références, détails de QA, réserves, fidélité, animation et préférences restent identiques. Les 24 fiches de base, 34 entrées d’extension et 20 rencontres boss sont conservées. Les compteurs V1 à V6 et les anciens journaux ne sont pas réécrits. Les 33 propositions d’extension publiées en V6 restent des propositions V6.

Les inventaires CSV restent les instantanés V6 de leurs préférences et compteurs. L’état courant des appels V7 est porté par le journal fusionné, le manifeste et `delivery_counts.json` ; l’usage courant des images est porté par le binding V7. Le statut de gameplay des entrées d’extension reste non implémenté même lorsque leur image est consultable au catalogue.

## 6. Vérification exécutée et limite de preuve

Le rapport [results.json](../prototype/qa_v7/results.json) consigne **{qa['passed']} contrôles réussis**, **{qa['failed']} échec** et les SHA-256 exacts des fichiers testés. Les scripts de contrôle restent dans [prototype/qa_v7](../prototype/qa_v7/).

{browser_note}

La vérification de livraison contrôle aussi les 90 fichiers d’art et leurs métadonnées, l’immutabilité des registres historiques, les 7 erreurs réelles, les 12 reports, la correspondance entre le binding et les usages déclarés, les fichiers historiques exclus de l’import et l’idempotence de la consolidation. Elle fige ensuite les seuls fichiers V7 prévus dans un snapshot haché avant publication.

## 7. Travaux encore ouverts

| Domaine | Reste concret |
|---|---|
| Génération de personnages | Produire les 17 premières images d’extension manquantes après rétablissement du service |
| Corrections | Dinh ; réserves existantes d’anatomie, d’orientation, de cadre et de transparence |
| Gardes de base | Garde du Major |
| Animations | Aucun clip livré ; créer et valider les animations, les directions et les transitions |
| Combat | Implémenter et équilibrer les movesets individuels au-delà du noyau partiel partagé |
| Narration et tournoi | Mode histoire complet, intros/rivaux/endings mis en scène, tableau de tournoi et progression |
| Finishers | Mise en scène, conditions, interactions et animations prévues dans la bible |
| Boss Battle | Développer les rencontres au-delà de la mécanique partielle du Scarab ; compléter les trois silhouettes partielles |
| Décors | Produire 22 masters manquants et les calques indépendants de parallaxe |
| Validation visuelle | Exécuter le laboratoire dans un navigateur disponible et examiner les silhouettes en situation |

## 8. Fichiers de référence

- [Journal fusionné V7](../work/wave7/generation_results.json) et [reçus de gel](../work/wave7/producer_freeze_receipts.json).
- [Vérification de livraison](../work/wave7/verification.json), [compteurs](../data/delivery_counts.json) et [manifeste](../data/asset_manifest.json).
- [Binding statique](../data/prototype_asset_bindings_v7.json), [laboratoire](../prototype/halo_combats_lab_v7.html), [guide](../prototype/README_V7.md).
- [Sources et limites V7](SOURCES_PERSONNAGES_V7.md), [rapport V6 conservé](HALO_COMBATS_PERSONNAGES_V6.md), [bible V1](HALO_COMBATS_BIBLE_V1.md).
'''
    producer_rows = ['| ' + row['path'] + ' | `' + row['sha256'] + '` | ' + str(row['actual_tool_calls']) + ' | ' + str(row['deferred_without_call']) + ' |' for row in journal['source_journals']]
    reference_rows = []
    for eid in baseline['target_ids']:
        row = called.get(eid, deferred.get(eid))
        urls = links(row)
        if not urls:
            urls = links(entries.get(eid, next((f for f in fighters if f['id'] == eid), {})))
        rendered = '<br>'.join('[' + str(i + 1) + '](' + url + ')' for i, url in enumerate(urls)) or 'Voir le journal V6 indiqué et les références locales consignées'
        reference_rows.append('| ' + md(names[eid]) + ' | ' + ('Appel réel, quota' if eid in called else 'Différée sans appel') + ' | ' + rendered + ' |')
    sources = f'''# Halo Combats — sources et portée documentaire V7

## État de la production

La V7 ne crée aucun nouveau PNG. Elle conserve les références et prompts de la reprise prévue, enregistre les sept appels ayant reçu une erreur de quota et les douze cibles différées sans appel. Les fichiers de référence téléchargés restent hors du dépôt ; leurs chemins et empreintes sont documentés lorsqu’ils existent déjà dans les journaux.

Les références Halo servent à comparer les incarnations, équipements et asymétries. Leur disponibilité ne certifie ni les images générées antérieurement ni les poses adaptées au jeu de combat. Le laboratoire utilise exclusivement les 90 PNG candidats du dépôt. Les URL de sources sont des liens documentaires ; elles ne sont jamais utilisées comme substituts visuels d’un personnage manquant.

## Journaux producteurs figés

| Journal | SHA-256 à la fusion | Appels réels | Reports sans appel |
|---|---|---:|---:|
{chr(10).join(producer_rows)}

Journal consolidé : `work/wave7/generation_results.json`, SHA-256 `{sha('work/wave7/generation_results.json')}`. Les réponses exactes restent dans les sources ; la normalisation ajoute la classification de quota sans changer la nature de l’événement. Les QA producteurs n’inventent aucune revue de nouveau PNG : il n’en existe pas dans cette vague.

## Références des cibles prévues

Les liens ci-dessous proviennent des journaux et du catalogue figé V6. Les pages Halopedia peuvent archiver un rendu promotionnel officiel ou pointer vers une source primaire ; elles conservent leur rôle documentaire d’origine. Les journaux précisent la provenance et le SHA de l’image effectivement fournie quand un appel a eu lieu. Les limites déjà relevées sur les vues occultées, asymétries et rendus conceptuels restent valables.

| Cible | Action V7 | Références consignées |
|---|---|---|
{chr(10).join(reference_rows)}

## Sources de l’intégration au laboratoire

Le binding `data/prototype_asset_bindings_v7.json` est construit depuis les registres `fighters`, `expansion_characters`, `bosses`, `stages`, l’inventaire de préférés et le manifeste d’images du projet. Il référence les 90 fichiers internes par identifiant, chemin, SHA-256, dimensions, mesures d’alpha et réserves de QA. Les dimensions et l’alpha sont mesurés en lecture seule ; aucun pixel n’est traité.

Les observations de QA V1 à V6, les incarnations, les propositions de gameplay et leurs sources restent dans [SOURCES_PERSONNAGES_V6.md](SOURCES_PERSONNAGES_V6.md), [HALO_COMBATS_PERSONNAGES_V6.md](HALO_COMBATS_PERSONNAGES_V6.md) et la [bible V1](HALO_COMBATS_BIBLE_V1.md). Cette reprise ne les publie pas à nouveau comme recherche ou conception nouvelle.

## Validation et réserves

{browser_note}

Les résultats exécutés et SHA des fichiers testés sont dans [results.json](../prototype/qa_v7/results.json). La [vérification V7](../work/wave7/verification.json) relie ces preuves au snapshot publié. Les mentions de prototype statique décrivent l’usage codé ; elles ne signifient ni animation livrée, ni comportement propre complet pour chaque personnage, ni fidélité visuelle 1:1.
'''
    outputs = {'README.md': readme, 'README_V7.md': readme,
               'docs/HALO_COMBATS_PERSONNAGES_V7.md': report,
               'docs/SOURCES_PERSONNAGES_V7.md': sources}
    for path, text in outputs.items():
        (PROJECT / path).write_text(text, encoding='utf-8')
    print(json.dumps({'written': list(outputs), 'new_pngs': 0, 'actual_calls': 7,
                      'deferred': 12, 'prototype_qa_status': qa['status']}, ensure_ascii=False))

if __name__ == '__main__': main()
