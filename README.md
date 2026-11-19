# Halo Combats — livraison visuelle V2

Mode annexe de combat 2D et Boss Battle pour Darknigthmare. Mise à jour : 2026-11-19T17:06:50+00:00.

## Résultat réel de la vague de personnages

Le roster défini contient **24 combattants**. **9 disposent d'au moins une pose candidate** ; **15 restent sans pose candidate**. Cette vague a produit **8 nouveaux PNG de personnages**.

Le dossier contient **12 candidats visuels au total**, en réunissant les 4 fichiers antérieurs et les nouveaux fichiers. Ce total comprend des personnages, un boss et des décors ; il n'est pas le nombre de combattants générés.

| Catégorie | Fichiers candidats livrés | Portée |
|---|---:|---|
| Poses de combattants | 9 | 9 combattants couverts sur 24 |
| Boss | 1 | Profil candidat du Scarab Halo 3 |
| Décors | 2 | Masters Valhalla et New Mombasa, sans couches parallaxe séparées |
| Tous candidats | 12 | Somme des trois catégories précédentes |
| Visuels certifiés | 0 | Aucune certification 1:1 déduite d'une génération |
| Clips d'animation livrés | 0 | Les poses candidates ne sont pas des animations |

Personnages disposant d'une pose candidate : **Thel 'Vadam l’Arbiter, Edward Buck ODST, Rtas 'Vadum, Atriox, Decimus, Jerome 092, Elite Zealot, Cethegus chef Brute, Mgalekgolo Hunter**.

Personnages nouvellement illustrés dans la vague 2 : **Atriox, Edward Buck ODST, Cethegus chef Brute, Decimus, Mgalekgolo Hunter, Jerome 092, Rtas 'Vadum, Elite Zealot**.

Parmi les nouveaux fichiers, **3 sont des références neutres sans arme** et 5 proviennent des demandes initiales de pose. Une référence calme sans arme ne constitue pas une garde de combat armée ni un ensemble d'animations. La variante de chaque fichier figure dans le manifeste et le CSV.

Le journal de cette vague contient **41 tentatives pour 23 personnages distincts** : 8 tentatives réussies et 33 échecs. Un personnage peut avoir plusieurs tentatives. Parmi les échecs, 33 ont été refusés par le contrôle automatique de génération ; leur motif précis n'a pas été fourni. Un échec antérieur ne laisse pas un personnage classé absent lorsqu'une tentative ultérieure a produit une image. Aucun fichier correspondant à une tentative échouée n'est compté comme livré ; les détails techniques sont conservés dans le manifeste et le journal.

## Ouvrir les livrables

- `docs/HALO_COMBATS_PERSONNAGES_V2.md` : couverture complète du roster, personnages encore manquants et réserves de contrôle.
- `data/characters_visual_inventory.csv` : inventaire des 24 combattants, chemins des images, dimensions, alpha, empreintes et statuts.
- `assets/characters_wave2/` : nouveaux PNG, copiés à l'identique sous des noms versionnés.
- `assets/candidates/` : quatre PNG candidats antérieurs, conservés.
- `data/asset_manifest.json` : manifeste courant de tous les candidats, avec prompts, références, mesures techniques et observations.
- `data/delivery_counts.json` : compteurs séparant le roster défini, les PNG livrés, leur catégorie et la couverture visuelle.
- `docs/HALO_COMBATS_BIBLE_V1.docx` et `.md` : bible de conception, version 1.
- `docs/HALO_COMBATS_PRODUCTION_V1.xlsx` : classeur de production, version 1 ; les registres JSON et CSV V2 portent l'état visuel courant.
- `prototype/halo_combats_prototype.html` : prototype autonome sans serveur ni connexion.

## Ce qui est défini et ce qui reste à produire

La bible décrit 24 combattants, 264 normales, 96 spéciaux, 24 supers, 48 propositions de combos, 24 routes avec introduction, rival et ending, 48 finishers, 20 rencontres de boss et 24 arènes à six couches. Les valeurs d'équilibrage et les routes narratives sont des propositions de cette adaptation 2D.

Le plan de 44 clips par combattant, soit 1 056 clips, demeure un plan de fabrication. Les 144 couches parallaxe prévues sont à produire. Les deux images d'arènes restent des masters de décor.

Les PNG de personnages sont des **poses candidates**. Ils nécessitent une comparaison aux modèles de l'épisode choisi, un contrôle du profil de combat et du détourage, les animations et l'intégration. Les mesures alpha et les empreintes ne valident ni l'anatomie ni la fidélité canonique. Les observations de `work/wave2/qa_wave2.json` sont rattachées aux empreintes des images effectivement examinées.

## Jouer au prototype

Choisir Entraînement, Duel IA ou Boss Scarab. Déplacement avec les flèches ou Q D, saut avec Espace, dash avec Maj, léger J, lourd K, tir L, grenade U, impulsion I, garde O et pause P. Contre le Scarab, casser les deux jambes vulnérables, rejoindre la balise centrale et utiliser E pour monter, puis attaquer le noyau sur le pont. Les boutons tactiles sont présents.

Le prototype utilise des silhouettes techniques temporaires. Il contient un personnage contrôlable, un adversaire IA et un boss. Le roster complet et les nouveaux PNG ne sont pas intégrés au moteur. La campagne, les tournois, les fatalités et le réseau demeurent des spécifications de la bible.

Les contrôles V1 de logique sont conservés dans `prototype/qa/`. Aucun nouveau test de gameplay n'est revendiqué par cette livraison visuelle.

## Références et traçabilité

`data/fighter_sources.json`, `data/world_sources.json` et `docs/source_registry.json` conservent les références et leur portée. Les références ajoutées pour cette vague figurent dans le manifeste et les fichiers de travail. Les versions d'armure, les épisodes, les concepts abandonnés et les propositions originales doivent rester distincts pendant la validation.

`work/wave2/generation_results.json` conserve les tentatives, `work/wave2/qa_wave2.json` les observations, et `work/wave2/consolidation_summary.json` la synthèse de consolidation. Les erreurs de génération restent visibles et ne sont pas transformées en livraisons.
