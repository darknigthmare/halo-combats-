# Halo Combats prototype mécanique

Version 0.1 du 19 novembre 2026. Ouvrir `halo_combats_prototype.html` dans un navigateur récent. Le fichier contient son interface, son moteur et ses dessins techniques ; il fonctionne sans serveur, sans connexion et sans dépendance externe.

## Ce qui fonctionne

- Entraînement contre mannequin avec énergie renouvelée et remise à zéro après KO.
- Duel contre une IA, une manche de 99 secondes, résultat et redémarrage.
- Boss Scarab en trois phases : casser deux jambes, monter à l’ascenseur central, détruire le noyau sur le pont. Le parcours a été vérifié au corps à corps, sans tir obligatoire.
- Déplacement latéral, saut, dash, garde de face, coup léger, coup lourd, tir, grenade temporisée, impulsion consommant de l’énergie.
- 1000 PV, 200 points de bouclier et recharge après quatre secondes sans impact ; deux grenades avec renouvellement temporisé ; trois segments d’énergie.
- Boucle de simulation à 60 Hz, file d’actions de huit frames, collisions, startup et recovery, recul, hitstop, télégraphies de zones dangereuses.
- Caméra à défilement, plusieurs plans de décor en parallaxe, barres de vie et de bouclier, retour d’impact, boîtes de collision optionnelles.
- Commandes clavier et boutons tactiles, pause, reprise, aide et arrêt automatique en cas de perte de focus.

## Commandes

| Action | Clavier |
| --- | --- |
| Gauche droite | Flèches ou Q D ou A D |
| Saut | Espace ou flèche haut ou Z ou W |
| Dash | Maj |
| Coup léger | J |
| Coup lourd | K |
| Tir | L |
| Grenade | U |
| Impulsion d’énergie | I |
| Garde maintenue | O |
| Monter sur le Scarab | E près de la balise, après destruction des jambes |
| Pause reprise | P |

Ces commandes simplifiées appartiennent au prototype ; elles ne remplacent pas la disposition complète à six boutons décrite dans la bible.

## Limites explicites

Les silhouettes et le décor sont des dessins techniques temporaires. Aucun sprite officiel, sprite de production, animation finalisée ou élément certifié fidèle 1:1 n’est intégré. Le Scarab est un schéma de scène, sans fidélité géométrique validée.

Ce prototype comprend un seul combattant contrôlable, une IA et une rencontre de boss. Il n’implémente pas la campagne, les routes de tous les personnages, le tournoi, les fatalités, les prises, les mouvements directionnels complexes, le multijoueur local ou en ligne, la coopération, le rollback, la sauvegarde, l’audio, les replays ou les contrôleurs de jeu. Ces éléments restent des spécifications de la bible.

Les valeurs sont des hypothèses de conception. Le duel est un test de mécanique, pas une simulation compétitive équilibrée. Le rendu tactile est prévu dans le HTML ; il doit encore être vérifié sur appareils réels.

## Vérification réalisée

17 contrôles de logique passent dans Node, avec DOM et canvas simulés. Ils couvrent l’initialisation, le déplacement clavier, les coups et les tirs, la garde, la recharge du bouclier, la grenade, le saut, le dash, la pause, l’IA, les trois phases du Scarab au corps à corps et le redémarrage. Le rapport détaillé est `qa/results.json`.

La tentative de validation Chromium headless a été bloquée au démarrage du navigateur par l’environnement d’exécution : création de socket refusée. Aucun rendu navigateur ou contrôle visuel n’est donc annoncé comme validé. Le scénario Playwright conservé dans `qa/verify.cjs` permet de reprendre cette vérification dans un environnement compatible.

Lancer les contrôles de logique avec `node qa/logic.cjs`. Les contrôles navigateur nécessitent Playwright et Chromium ; adapter les chemins de runtime dans `qa/verify.cjs` hors de l’environnement de création.

## Base d’intégration

Remplacer les fonctions de dessin des silhouettes et du décor par les sprites et calques approuvés sans modifier les règles de collision. Définir ensuite les personnages via les données de la bible, séparer simulation et rendu, et ajouter la sérialisation déterministe avant tout travail de rollback. Les données du prototype ne constituent pas un contrat réseau.
