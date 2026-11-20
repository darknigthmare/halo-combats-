# Halo Combats — laboratoire V8

La V8 rend consultables les **quatre nouveaux PNG de personnages** dans le laboratoire : Jameson Locke, Mickey, Skirmisher Champion et Bassus. Le catalogue contient désormais **94 PNG**, **21 extensions avec au moins un visuel** et **13 extensions encore sans image**.

Cette entrée conserve la simulation V7. Les **24 identités de base** restent les seules sélectionnables en combat et partagent les mêmes mécaniques. Les quatre nouveaux personnages appartiennent au catalogue des extensions ; aucun nouveau moveset ni rencontre de boss n’est activé.

## Ouvrir cette version

Depuis une copie complète du dépôt, ouvrir [halo_combats_lab_v8.html](halo_combats_lab_v8.html).

Conserver `assets/`, `data/` et `prototype/` ensemble, notamment les deux dossiers `prototype/lab_v7/` et `prototype/lab_v8/`. L’interface V8 réutilise la feuille de style V7 et charge ses propres scripts :

1. `lab_v8/catalog.js`, qui expose les données V8 embarquées ;
2. `lab_v8/app.js`, qui utilise ces données pour la simulation et le catalogue.

L’ouverture locale `file://` n’a pas besoin de `fetch`. Si `catalog.js` manque, le message indique explicitement le dossier `lab_v8`. Pour utiliser un serveur statique facultatif, depuis la racine du dépôt :

```bash
python -m http.server 8000 --directory .
```

Ouvrir ensuite `http://localhost:8000/prototype/halo_combats_lab_v8.html`. Si le bootstrap embarqué manque dans ce parcours HTTP, le laboratoire demande exclusivement `data/prototype_asset_bindings_v8.json` ; il ne revient pas aux données V7.

## Retrouver les nouveaux personnages

Ouvrir **Catalogue visuel**, choisir la catégorie **34 extensions**, puis rechercher un nom ci-dessous.

| Personnage | Incarnation utilisée | Image ajoutée |
|---|---|---|
| Jameson Locke | Halo 5: Guardians, armure HUNTER GEN2 | `locke_h5_initial_right_v01.png` |
| Michael « Mickey » Crespo | Halo 3: ODST, équipement de 2009 | `mickey_odst_initial_right_v01.png` |
| Skirmisher Champion | Halo: Reach, classe T’vaoan Champion | `skirmisher_champion_reach_initial_right_v01.png` |
| Bassus | Halo Infinite, armure or/rouge et marteau gravitationnel | `bassus_infinite_initial_right_v01.png` |

Chaque entrée conserve sa référence de jeu, sa variante, ses sources et ses réserves de vérification. Les PNG sont affichés entiers, avec leur orientation native. **Bassus est surtout frontal, tête vers la droite** ; son image n’est pas présentée comme un profil latéral validé. Les autres nouveaux candidats gardent également leurs réserves de pose, de cadrage et de détail.

Les images restent des **candidats statiques, sans certification de fidélité 1:1**. Aucun PNG n’a été inversé, découpé ou retouché lors de cette intégration. La garde du Major reste sans image dédiée ; Dinh conserve son avertissement de correction et n’a pas de visuel préféré.

## Périmètre conservé

| Élément | État dans la V8 |
|---|---|
| Personnages recensés | 58 : 24 identités de base et 34 extensions |
| Sélection de combat | 24 identités de base, règles communes |
| Poses de base | 24 poses neutres préférées et 23 gardes statiques |
| Modes mécaniques | Entraînement, duel IA, rencontre partielle du Scarab |
| Scarab | Jambes, abordage, noyau ; mécanique V7 conservée |
| Boss consultables | 20 ; les autres rencontres ne sont pas activées |
| Décors recensés | 24, dont deux masters PNG plats |
| Extensions illustrées | 21, dont Dinh avec une image à corriger |
| Extensions sans image | 13 |
| PNG uniques | 94, variantes comprises |
| Nouvelles animations ou nouveaux movesets | Aucun |

Les commandes restent celles du [guide V7](README_V7.md) : flèches ou Q/D pour déplacer, Espace pour sauter, Maj pour dash, J/K pour frapper, L pour tirer, U pour une grenade, I pour l’impulsion, O pour garder, E pour monter sur le Scarab et P pour la pause. Les boutons tactiles sont conservés.

Le moteur déplace des poses fixes. La caméra, les collisions, les dégâts, les entrées, l’IA et les phases du Scarab ne changent pas en V8. Les modes histoire complets, tournoi, finishers animés et movesets individuels restent des travaux de conception et d’implémentation distincts.

## Vérifications exécutées

Depuis la racine du dépôt :

```bash
node prototype/qa_v8/logic.cjs
```

Le rapport [results.json](qa_v8/results.json) contient **38 contrôles réussis, zéro échec**, avec les empreintes des fichiers testés. La suite reprend les contrôles de la simulation et vérifie spécifiquement :

- la parité du JSON V8 et du catalogue embarqué ;
- les 94 PNG et leurs SHA-256, les 21 extensions illustrées et les 13 manquantes ;
- les quatre nouvelles variantes, leur incarnation et leur disponibilité en consultation uniquement ;
- le parcours HTTP sans bootstrap, qui doit charger le JSON V8 ;
- le message local sans bootstrap, qui doit citer `lab_v8` ;
- l’absence de changement mécanique entre les scripts V7 et V8 ;
- les sélections, la pause, les commandes, les erreurs d’image, le cadrage et le parcours Scarab existant.

Ces tests utilisent un DOM, un canvas et un chargement d’image simulés dans Node. Ils lisent les en-têtes et empreintes des vrais PNG, mais **ne vérifient pas le rendu des pixels dans un navigateur**.

## Navigateur : aucune exécution en V8

**Aucun navigateur n’a été lancé pour cette version.** Le rapport V8 porte donc `browser_validation.status: not_run` et `attempts_v8: 0`.

Le fichier [browser_block.json de V7](qa_v7/browser_block.json) reste un constat historique distinct : Chromium avait échoué avant ouverture de page sur une permission de socket. Ce constat n’est pas présenté comme une nouvelle tentative V8. Aucune capture ou validation visuelle desktop/mobile V8 n’est annoncée.

Un scénario adapté à la page V8 est fourni pour un environnement disposant de Playwright et autorisant Chromium :

```bash
node prototype/qa_v8/verify_browser.cjs
```

Ce script n’a pas été exécuté pendant cette livraison. Ses variables facultatives restent `HALO_PLAYWRIGHT_MODULE`, `HALO_CHROMIUM_PATH`, `HALO_TEST_URL` et `HALO_QA_SCREENSHOT_DIR`. Les captures éventuellement produites lors d’une future exécution devront encore être examinées visuellement.

## Fichiers V8

- [halo_combats_lab_v8.html](halo_combats_lab_v8.html) : entrée de cette version.
- [app.js](lab_v8/app.js) : même simulation que V7, avec libellés et chemin de secours V8.
- [catalog.js](lab_v8/catalog.js) et [prototype_asset_bindings_v8.json](../data/prototype_asset_bindings_v8.json) : données V8 synchronisées.
- [logic.cjs](qa_v8/logic.cjs), [results.json](qa_v8/results.json) et [verify_browser.cjs](qa_v8/verify_browser.cjs) : contrôles et scénario navigateur non exécuté.

La V7 reste disponible dans ses fichiers d’origine. Ses scripts, sa feuille de style, ses données embarquées et ses rapports n’ont pas été modifiés.
