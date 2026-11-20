# Halo Combats — V9 : catalogue de l’univers et 10 images supplémentaires

Le lot V9 reprend le travail resté local après la fusion de la PR #1 : **10 PNG supplémentaires**, **130 nouvelles fiches**, et un catalogue consultable regroupant **232 fiches**, **112 œuvres ou composants** et **104 PNG distincts**. Les 94 images V8 sont conservées octet pour octet.

## Ouvrir le catalogue

Ouvrir [Archives de l’univers V9](prototype/halo_universe_v9.html) dans un navigateur, directement depuis les fichiers ou avec un serveur HTTP local à la racine du dépôt. Recherche, filtres par œuvre/média/continuité, catégories, fiches détaillées et filtre des manquants sont disponibles. Le [laboratoire de combat V8](prototype/halo_combats_lab_v8.html) reste accessible depuis le catalogue.

| Livrable V9 | Contenu |
|---|---|
| Personnages | Linda-058, Veronica Dare, N’tho ’Sraom, Holly Tanaka, Usze ’Taham |
| Costumes | Edward Buck Spartan Halo 5 ; Thel ’Vadam Halo 5 |
| Décors | Blood Gulch Halo CE ; Lockout Halo 2 |
| Boss / véhicule | M510 Mammoth Halo 4, candidat à corriger |

Le catalogue comporte **128 personnages, 24 costumes, 46 stages et 34 boss**. **77 fiches ont au moins une image ; 155 restent sans visuel.** Les références des jeux, romans, BD, animations et prises de vues réelles sont reliées à leurs fiches. Le registre reste un inventaire en cours : une œuvre recensée n’est pas une œuvre intégralement couverte.

Les nouveaux PNG sont des poses fixes ou des masters de décor. Les réserves de silhouette, d’équipement, de cadrage et d’asymétrie restent visibles dans chaque fiche. Les décors n’ont pas encore de calques de parallaxe indépendants. **Aucune nouvelle animation, aucun moveset complet et aucune certification de fidélité 1:1 ne sont annoncés par cette livraison.**

## Données et suivi

- [Catalogue V9 documenté](docs/HALO_COMBATS_CATALOGUE_V9.md), [données JSON](data/universe_catalog_v9.json) et [manifeste des 104 PNG](data/asset_manifest_v9.json).
- Journaux de production : [personnages](work/wave9/character_generation.json), [décors et Mammoth](work/wave9/root_generation.json), [compléments](work/wave9/additional_generation.json).
- [Tests du catalogue](prototype/qa_v9/catalog.test.cjs) : `node --test prototype/qa_v9/catalog.test.cjs`.
- [État V8 conservé](README_V8.md), [bible initiale](docs/HALO_COMBATS_BIBLE_V1.md) et [bilan de construction V9](work/wave9/catalogue_build_report.json).

## Historique V8

Le texte ci-dessous conserve le bilan de la V8 ; ses nombres décrivent cette version historique.

### V8 : reprise des personnages manquants

La reprise V8 a produit **4 nouveau(x) PNG candidat(s)** : **Jameson Locke, Michael « Mickey » Crespo, Skirmisher Champion — classe Reach, Bassus**. **20 appels réels** ont été effectués sur **19 cibles distinctes**. Les autres résultats comprennent **15 refus `moderation_blocked`**, **0 erreur(s) de quota** et **1 erreur(s) technique(s)**. Les réponses du service restent conservées exactement.

| Mesure | V8 / état courant |
|---|---:|
| Cibles prévues / distinctes appelées | 19 / 19 |
| Appels réellement effectués | 20 |
| Nouveaux PNG | **4** |
| Nouvelles identités d’extension illustrées | 4 |
| Refus `moderation_blocked` | 15 |
| Erreurs de quota / autres erreurs techniques | 0 / 1 |
| Demandes différées sans appel | 0 |
| PNG cumulés / anciens PNG conservés | 94 / 90 |
| Extensions avec image / encore sans image | 21 / 13 |
| Gardes de base disponibles | 23 / 24 |
| Nouveaux clips d’animation / certification 1:1 | 0 / 0 |

## Images et catalogue

Les nouveaux personnages d’extension sont consultables dans le **catalogue V8**, sans activation de leurs movesets en combat. L’entrée V8 réutilise les mécaniques et le style V7 ; son script est une copie minimale avec libellé et chemin de secours JSON V8. Le laboratoire, les bindings et les résultats V7 restent conservés. Le catalogue embarqué V8 et le JSON contiennent les mêmes données.

Les images produites sont des poses statiques candidates. Les observations de transparence, d’orientation, de marges, de détails extrapolés et d’équipement restent attachées à chaque PNG. Aucune inversion horizontale, retouche ou certification 1:1 n’est appliquée automatiquement.

## Manquants

Les extensions encore sans image sont : Kelly-087, Linda-058, Holly Tanaka, Veronica Dare, Kojo « Romeo » Agu, Commandante Laurette Agryna, N’tho ’Sraom, Usze ’Taham, Let ’Volir, Grunt Heavy — classe spécialisée Reach, Pavium, Ur-Didact, Chevalier prométhéen — standard.

La garde du Major reste absente. Dinh conserve son candidat V6 à corriger, sans visuel préféré. Leurs demandes V8 n’ont pas produit de remplacement.

## Vérification

Les contrôles ciblés du catalogue V8 consignent **38 réussites et 0 échec(s)** dans `prototype/qa_v8/results.json`. Ils vérifient les données et le chargement simulé ; ils ne constituent pas un examen des pixels dans un navigateur.

La validation visuelle interactive reste non réalisée après le blocage navigateur documenté en V7. Les 90 anciens PNG et leurs 90 fiches d’art sont conservés strictement. Les versions et journaux antérieurs restent disponibles.

- [Rapport V8](docs/HALO_COMBATS_PERSONNAGES_V8.md) et [sources V8](docs/SOURCES_PERSONNAGES_V8.md).
- [Catalogue et laboratoire V8](prototype/halo_combats_lab_v8.html) et [guide V8](prototype/README_V8.md).
- [Journal V8](work/wave8/generation_results.json), [QA des nouveaux PNG](work/wave8/qa_wave8.json), [vérification](work/wave8/verification.json).
- [Inventaire visuel courant V8](data/characters_visual_inventory_v8.csv).
- [État V7](README_V7.md), [personnages V6](docs/HALO_COMBATS_PERSONNAGES_V6.md), [bible V1](docs/HALO_COMBATS_BIBLE_V1.md).

Les modes histoire complet, tournoi, finishers animés, movesets individuels et animations restent les travaux décrits dans la bible. Les 24 identités de base partagent toujours la mécanique partielle du laboratoire.
