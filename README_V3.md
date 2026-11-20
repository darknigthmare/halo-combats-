# Halo Combats — livraison visuelle V3

Mode annexe de combat 2D et Boss Battle pour Darknigthmare. Mise à jour : 2026-11-19T17:40:53+00:00.

## État des personnages

**12 combattants illustrés sur 24 ; 12 restent sans image candidate.** La vague 3 apporte **3 nouveaux PNG**, pour 3 personnages.

Le journal V3 comprend 15 tentatives pour 15 personnages distincts : 3 réussites et 12 échecs. Parmi ces derniers, 12 sont des refus automatiques dont le motif précis n'a pas été fourni. Les succès après refus sont comptés comme présents. Les compteurs et journaux V1/V2 restent conservés.

| Catégorie | Fichiers disponibles | Portée |
|---|---:|---|
| Poses de combattants | 12 | 12 combattants sur 24 |
| Profils de boss | 1 | Candidats visuels de boss |
| Masters de décors | 2 | Couches parallaxe séparées à produire |
| Tous candidats visuels | 15 | Somme des catégories précédentes |
| Visuels certifiés | 0 | Aucune certification déduite d'une génération |
| Clips d'animation livrés | 0 | Les poses statiques ne sont pas des animations |

Personnages disposant d'une image : **Thel 'Vadam l’Arbiter, Noble Six, Edward Buck ODST, Le Rookie, Rtas 'Vadum, Atriox, Decimus, Alice 130, Jerome 092, Elite Zealot, Cethegus chef Brute, Mgalekgolo Hunter**.

Personnages nouvellement illustrés dans la vague 3 : **Alice 130, Noble Six, Le Rookie**.

Personnages encore sans image : **John 117 le Major, Avery Johnson, Emile A239, Jorge 052, Jun A266, Kat B320, Carter A259, Tartarus, Escharum, Jega 'Rdomnai, Chak 'Lok, Douglas 042**.

## Ouvrir les livrables

- [Suivi des personnages V3](docs/HALO_COMBATS_PERSONNAGES_V3.md) : couverture complète et observations.
- [Inventaire courant](data/characters_visual_inventory.csv) : les 24 combattants, fichiers, dimensions, alpha et statuts.
- [Nouveaux PNG V3](assets/characters_wave3/) : copies byte-identiques des sorties obtenues.
- [PNG V2](assets/characters_wave2/) et [candidats V1](assets/candidates/) : fichiers antérieurs conservés.
- [Manifeste courant](data/asset_manifest.json) et [compteurs](data/delivery_counts.json).
- [Bible DOCX V1](docs/HALO_COMBATS_BIBLE_V1.docx) et [bible Markdown V1](docs/HALO_COMBATS_BIBLE_V1.md).
- [Classeur de production V1](docs/HALO_COMBATS_PRODUCTION_V1.xlsx) : état daté ; les registres JSON/CSV portent le suivi visuel courant.
- [Prototype autonome](prototype/halo_combats_prototype.html) et [instructions du prototype](prototype/README.md).

## Fidélité, animations et intégration

Les images sont des poses candidates. Chaque fichier demande encore une comparaison aux modèles de l'épisode, un contrôle de la vue latérale et du détourage, ainsi que les animations. Les variantes neutres sans arme sont des références de personnage ; elles ne constituent pas toutes des gardes de combat prêtes à intégrer.

La bible définit 24 combattants, 264 normales, 96 spéciaux, 24 supers, 48 propositions de combos, 48 finishers, 24 routes narratives, 20 rencontres de boss et 24 arènes. Les valeurs d'équilibrage et routes sont des propositions de cette adaptation 2D.

Le plan de 1056 clips d'animation et de 144 couches parallaxe reste un plan de fabrication. Les images fixes ne sont pas comptées comme des clips.

Le prototype conserve ses silhouettes techniques temporaires et ses modes Entraînement, Duel IA et Boss Scarab. Le roster complet, les nouveaux PNG, la campagne, les tournois, les fatalités et le réseau ne sont pas intégrés au moteur par cette livraison visuelle. Les vérifications de logique V1 restent dans [prototype/qa/](prototype/qa/) ; aucun nouveau résultat de gameplay n'est revendiqué.

## Traçabilité

Le [journal V3](work/wave3/generation_results.json), les [observations QA V3](work/wave3/qa_wave3.json) et la [consolidation V3](work/wave3/consolidation_summary.json) séparent les tentatives des images réellement disponibles. Les historiques V1/V2 et leurs observations restent présents.

Les sources figurent dans [fighter_sources.json](data/fighter_sources.json), [world_sources.json](data/world_sources.json), [source_registry.json](docs/source_registry.json), ainsi que dans les prompts et le manifeste. Les références, le cut content et les propositions d'adaptation doivent rester distincts pendant la validation.

Les scripts sources de la V1 reconstruisent un état daté. Ne pas les rejouer sur les registres courants sans préserver les consolidations V2/V3.
