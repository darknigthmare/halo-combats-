# Halo Combats — livraison visuelle V4

Mode annexe de combat 2D et Boss Battle pour Darknigthmare. Mise à jour : 2026-11-19T20:25:42+00:00.

## État des personnages

**20 combattants illustrés sur 24 ; 4 restent sans image candidate.** La vague 4 apporte **9 nouveaux PNG**, pour 8 personnages.

Le journal V4 comprend 21 tentatives pour 12 personnages distincts : 9 réussites et 12 échecs. Parmi ces derniers, 12 sont des refus automatiques dont le motif précis n'a pas été fourni. Les succès après refus sont comptés comme présents. Les compteurs et journaux V1/V2/V3 restent conservés.

| Catégorie | Fichiers disponibles | Portée |
|---|---:|---|
| Poses de combattants | 21 | 20 combattants sur 24 |
| Profils de boss | 1 | Candidats visuels de boss |
| Masters de décors | 2 | Couches parallaxe séparées à produire |
| Tous candidats visuels | 24 | Somme des catégories précédentes |
| Visuels certifiés | 0 | Aucune certification déduite d'une génération |
| Clips d'animation livrés | 0 | Les poses statiques ne sont pas des animations |

Personnages disposant d'une image : **John 117 le Major, Thel 'Vadam l’Arbiter, Avery Johnson, Noble Six, Jorge 052, Jun A266, Kat B320, Carter A259, Edward Buck ODST, Le Rookie, Rtas 'Vadum, Tartarus, Atriox, Decimus, Alice 130, Douglas 042, Jerome 092, Elite Zealot, Cethegus chef Brute, Mgalekgolo Hunter**.

Personnages nouvellement illustrés dans la vague 4 : **Carter A259, John 117 le Major, Douglas 042, Avery Johnson, Jorge 052, Jun A266, Kat B320, Tartarus**.

Personnages encore sans image : **Emile A239, Escharum, Jega 'Rdomnai, Chak 'Lok**.

## Ouvrir les livrables

- [Suivi des personnages V4](docs/HALO_COMBATS_PERSONNAGES_V4.md) : couverture complète et observations.
- [Inventaire courant](data/characters_visual_inventory.csv) : les 24 combattants, fichiers, dimensions, alpha et statuts.
- [Nouveaux PNG V4](assets/characters_wave4/) : copies byte-identiques des sorties obtenues.
- [PNG V3](assets/characters_wave3/), [PNG V2](assets/characters_wave2/) et [candidats V1](assets/candidates/) : fichiers antérieurs conservés.
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

Le [journal V4](work/wave4/generation_results.json), les [observations QA V4](work/wave4/qa_wave4.json) et la [consolidation V4](work/wave4/consolidation_summary.json) séparent les tentatives des images réellement disponibles. Les historiques V1/V2/V3 et leurs observations restent présents.

Les sources figurent dans [fighter_sources.json](data/fighter_sources.json), [world_sources.json](data/world_sources.json), [source_registry.json](docs/source_registry.json), ainsi que dans les prompts et le manifeste. Les références, le cut content et les propositions d'adaptation doivent rester distincts pendant la validation.

Les scripts sources de la V1 reconstruisent un état daté. Ne pas les rejouer sur les registres courants sans préserver les consolidations V2/V3/V4.
