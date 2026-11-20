# Halo Combats — rapport V7 : art conservé, génération interrompue et laboratoire

## 1. Résultat de cette livraison

La V7 fait passer les images existantes dans un laboratoire visuel autonome, avec sélection des 24 profils de base et consultation séparée des extensions, boss et décors. Elle n’ajoute **aucun PNG**. Les sept appels réellement partis vers le service de génération ont tous échoué sur la limite globale d’usage ; les douze autres demandes n’ont pas été envoyées.

| Mesure | V7 / état cumulé |
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
| Nouveaux clips d’animation / visuels certifiés 1:1 | 0 / 0 |

Le registre cumule désormais **118 échecs de génération réels** : les **111 refus antérieurs**, conservés byte pour byte dans leur préfixe logique, et **7 erreurs de quota**. Le nombre de refus automatiques de modération reste 111. Une demande différée ne compte ni comme appel, ni comme rejet, ni comme image produite.

## 2. Les 19 cibles et leur état réel

| Personnage | Identifiant stable | Objet prévu | Résultat V7 | État de l’art après V7 |
|---|---|---|---|---|
| Kelly-087 | kelly_h5 | Première image d’extension | Appel réel — quota HTTP 429, aucune image | Image toujours absente |
| Linda-058 | linda_h5 | Première image d’extension | Appel réel — quota HTTP 429, aucune image | Image toujours absente |
| Jameson Locke | locke_h5 | Première image d’extension | Appel réel — quota HTTP 429, aucune image | Image toujours absente |
| Holly Tanaka | tanaka_h5 | Première image d’extension | Appel réel — quota HTTP 429, aucune image | Image toujours absente |
| Veronica Dare | dare_odst | Première image d’extension | Différée — aucun appel effectué | Image toujours absente |
| Kojo « Romeo » Agu | romeo_odst | Première image d’extension | Différée — aucun appel effectué | Image toujours absente |
| Michael « Mickey » Crespo | mickey_odst | Première image d’extension | Différée — aucun appel effectué | Image toujours absente |
| Commandante Laurette Agryna | agryna_infinite | Première image d’extension | Différée — aucun appel effectué | Image toujours absente |
| N’tho ’Sraom | ntho_h3 | Première image d’extension | Appel réel — quota HTTP 429, aucune image | Image toujours absente |
| Usze ’Taham | usze_h3 | Première image d’extension | Appel réel — quota HTTP 429, aucune image | Image toujours absente |
| Let ’Volir | let_volir_hw2 | Première image d’extension | Appel réel — quota HTTP 429, aucune image | Image toujours absente |
| Skirmisher Champion — classe Reach | skirmisher_champion_reach | Première image d’extension | Différée — aucun appel effectué | Image toujours absente |
| Grunt Heavy — classe spécialisée Reach | grunt_heavy_reach | Première image d’extension | Différée — aucun appel effectué | Image toujours absente |
| Pavium | pavium_hw2 | Première image d’extension | Différée — aucun appel effectué | Image toujours absente |
| Bassus | bassus_infinite | Première image d’extension | Différée — aucun appel effectué | Image toujours absente |
| Ur-Didact | didact_h4 | Première image d’extension | Différée — aucun appel effectué | Image toujours absente |
| Chevalier prométhéen — standard | knight_h4 | Première image d’extension | Différée — aucun appel effectué | Image toujours absente |
| Hieu Dinh | dinh_infinite | Correction de l’image existante | Différée — aucun appel effectué | Candidat V6 à corriger, sans préféré |
| John 117 le Major | chief_infinite | Garde statique manquante | Différée — aucun appel effectué | Pose neutre conservée ; garde absente |

Les dix-sept extensions manquantes restent donc manquantes. L’image de Dinh possède toujours sa réserve sur le côté anatomique des poches bleues ; aucun remplacement n’existe. Le Major conserve son image neutre et n’a toujours pas de garde statique. Aucun visuel de référence téléchargé n’a été substitué à une image manquante.

## 3. Preuve des appels effectués

| Cible | Début UTC | Fin UTC | HTTP | Classe d’erreur | Journal producteur |
|---|---|---|---:|---|---|
| Kelly-087 | 2026-11-20T06:37:22.023Z | 2026-11-20T06:37:29.980Z | 429 | usage_limit_reached | work/wave7/generation_results_unsc.json |
| Linda-058 | 2026-11-20T06:37:22.023Z | 2026-11-20T06:37:30.355Z | 429 | usage_limit_reached | work/wave7/generation_results_unsc.json |
| Jameson Locke | 2026-11-20T06:37:22.023Z | 2026-11-20T06:37:30.686Z | 429 | usage_limit_reached | work/wave7/generation_results_unsc.json |
| Holly Tanaka | 2026-11-20T06:37:22.023Z | 2026-11-20T06:37:29.537Z | 429 | usage_limit_reached | work/wave7/generation_results_unsc.json |
| N’tho ’Sraom | 2026-11-20T06:38:12.822Z | 2026-11-20T06:38:13.222Z | 429 | usage_limit_reached | work/wave7/generation_results_aliens.json |
| Usze ’Taham | 2026-11-20T06:38:12.823Z | 2026-11-20T06:38:13.559Z | 429 | usage_limit_reached | work/wave7/generation_results_aliens.json |
| Let ’Volir | 2026-11-20T06:38:12.823Z | 2026-11-20T06:38:13.828Z | 429 | usage_limit_reached | work/wave7/generation_results_aliens.json |

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

La baseline publiée est le commit `8c4dff83b48611a3439d67e1c15a3e0326b2a1ec`. Son arbre comporte 236 fichiers. Les 17 chemins propres à la publication restent exclus de l’import source V7 : 15 fichiers historiques, dont les archives et adaptations de portabilité, sont conservés à l’identique ; les deux index globaux `PUBLICATION_INVENTORY.json` et `SHA256SUMS.txt` sont recalculés pour l’arbre livré.

Les **90 SHA-256 des PNG** restent inchangés. Pour leurs 90 fiches actives, seuls `integration_status` et `prototype_usage_v7` sont autorisés à évoluer. Le second champ recopie exactement l’entrée correspondante de `asset_usages` ; le premier vaut `prototype_static_display` pour les 50 usages du laboratoire et `prototype_catalog_display` pour les 40 usages de catalogue seul. Le vérificateur reconstruit les usages attendus depuis les préférés figés des inventaires et registres ; cette exception n’autorise aucune autre modification de métadonnées.

Les identifiants, propriétaire d’origine, type, chemin, SHA, pose, orientation, équipements, prompts, références, détails de QA, réserves, fidélité, animation et préférences restent identiques. Les 24 fiches de base, 34 entrées d’extension et 20 rencontres boss sont conservées. Les compteurs V1 à V6 et les anciens journaux ne sont pas réécrits. Les 33 propositions d’extension publiées en V6 restent des propositions V6.

Les inventaires CSV restent les instantanés V6 de leurs préférences et compteurs. L’état courant des appels V7 est porté par le journal fusionné, le manifeste et `delivery_counts.json` ; l’usage courant des images est porté par le binding V7. Le statut de gameplay des entrées d’extension reste non implémenté même lorsque leur image est consultable au catalogue.

## 6. Vérification exécutée et limite de preuve

Le rapport [results.json](../prototype/qa_v7/results.json) consigne **34 contrôles réussis**, **0 échec** et les SHA-256 exacts des fichiers testés. Les scripts de contrôle restent dans [prototype/qa_v7](../prototype/qa_v7/).

La validation dans un navigateur est bloquée avant le chargement de la page. Motif consigné : Last observed launch in this session: Chromium aborted before opening a page because socket() is not permitted. Node logic tests do not launch a browser.. Aucune validation visuelle interactive n’est revendiquée.

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
