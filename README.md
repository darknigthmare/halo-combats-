# Halo Combats — V7 : laboratoire visuel et suivi de génération

La V7 ajoute un **laboratoire jouable utilisant les PNG existants** et un catalogue consultable des personnages, boss et décors. Les **90 fichiers d’image restent identiques** ; l’affichage conserve chaque pose native, sans miroir horizontal. Les 24 profils de base partagent les mécaniques partielles du laboratoire ; leurs movesets complets restent à implémenter.

La reprise des personnages manquants a rencontré la limite globale du service d’image : **7 appels ont reçu une erreur de quota, puis 12 demandes ont été différées sans appel**. **Aucun nouveau personnage illustré ni PNG n’a été généré dans cette vague.** Les 111 refus de génération antérieurs restent conservés séparément des 7 erreurs de quota V7.

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

## Ouvrir le laboratoire

Ouvrir [halo_combats_lab_v7.html](prototype/halo_combats_lab_v7.html) depuis une copie complète du dépôt. Le catalogue embarqué permet l’ouverture locale ; conserver les dossiers `assets`, `data` et `prototype` ensemble. Les commandes et scénarios sont détaillés dans le [guide du laboratoire](prototype/README_V7.md).

Le laboratoire propose les 24 profils de base, affiche les poses neutres et les 23 gardes disponibles, et présente séparément les 34 extensions. Les 20 boss peuvent être consultés ; le **Scarab** seul conserve la mécanique partielle déjà présente dans le précédent prototype. Les deux masters de décor sont utilisés comme images plates ; les 22 autres décors indiquent leur image manquante. Aucun calque indépendant de parallaxe ni nouvelle animation de personnage n’est livré.

## Vérification et portée réelle

Le rapport de test consigne **34 vérifications réussies et 0 échec** pour les contrôles effectivement exécutés. La validation dans un navigateur est bloquée avant le chargement de la page. Motif consigné : Last observed launch in this session: Chromium aborted before opening a page because socket() is not permitted. Node logic tests do not launch a browser.. Aucune validation visuelle interactive n’est revendiquée.

L’intégration déclarée dans le manifeste correspond précisément aux usages du [binding V7](data/prototype_asset_bindings_v7.json) : **50 PNG** possèdent un usage d’affichage statique dans le laboratoire et **40** un usage de catalogue seul. Les 90 restent consultables au catalogue, variantes comprises. Cette intégration conserve les réserves de QA, les orientations, les préférences et les états `not_certified` / `not_animated`.

Les **17 extensions sans image** restent : Kelly-087, Linda-058, Jameson Locke, Holly Tanaka, Veronica Dare, Kojo « Romeo » Agu, Michael « Mickey » Crespo, Commandante Laurette Agryna, N’tho ’Sraom, Usze ’Taham, Let ’Volir, Skirmisher Champion — classe Reach, Grunt Heavy — classe spécialisée Reach, Pavium, Bassus, Ur-Didact, Chevalier prométhéen — standard. La garde du Major manque toujours. L’image existante de Dinh reste à corriger et sans candidat préféré ; elle est consultable avec son avertissement.

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
