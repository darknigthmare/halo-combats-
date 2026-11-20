# Etat de production du premier lot

Version du 19 novembre 2026.

La bible et les registres décrivent le contenu prévu. Le prototype permet de tester une partie des mécaniques. Les quatre images du premier lot sont des candidats visuels, sans validation 1 à 1 ni animation finalisée.

## Candidats livrés

| Elément | Fichier | Contrôle restant |
| --- | --- | --- |
| arbiter_h3 | arbiter_halo3_neutral_right_v2.png | Pose neutre candidate. Fond alpha présent mais halo périphérique à contrôler. Orientation trois quarts trop marquée pour frame latérale finale. Armure et mandibules à comparer au modèle Halo 3. |
| boss_scarab_h3 | scarab_halo3_left_v2.png | Quatre pattes après correction. Alpha présent. Profil légèrement trois quarts, géométrie et proportions des modules à comparer au modèle Halo 3. Non segmenté, non animé. |
| st_valhalla_h3 | valhalla_halo3_master_v2.png | Anneau incorrect retiré, taille du beacon réduite. Concept maître latéral. Géométrie du beacon et topographie encore à comparer aux captures. Zéro calque indépendant livré. |
| st_mombasa_odst | mombasa_odst_night_master_v2.png | Ascenseur intact incorrect retiré pour le contexte de nuit retenu. Concept maître latéral. Identification des façades du secteur et comparaison ODST encore requises. Zéro calque indépendant livré. |

## Génération refusée

Master Chief Infinite a fait l’objet de deux demandes, dont une pose neutre sans arme. Les deux ont été refusées par le système automatique d’images. Aucun fichier de Chief n’est compté ni remplacé par un dessin technique dans le lot de sprites.

## Animation à produire

Le plan propose 44 clips par combattant, soit 1056 clips. Son budget indicatif atteint 27264 dessins pour les deux orientations, avant costumes, réactions de finishers, cinématiques de route et VFX. Il s’agit d’un budget de production, pas d’un nombre de fichiers réalisés. Zéro clip finalisé est livré.

## Décors à produire

Les 24 arènes sont détaillées en 144 couches prévues. Valhalla et Mombasa disposent d’un concept maître. Aucune de ces deux images plates ne constitue un ensemble de six couches séparées. La parallaxe du prototype repose encore sur ses dessins techniques.

## Prototype et validation

Le prototype autonome comprend entraînement, duel IA et Scarab à trois phases. Les 17 tests de logique Node passent. Le lancement de Chromium a été bloqué par l’environnement avant ouverture de page, donc le rendu navigateur et l’ergonomie tactile restent à vérifier. Le rapport et les scénarios sont conservés dans prototype/qa.

## Ordre recommandé pour la suite

1. Compléter les références comparatives des quatre candidats et corriger leurs écarts visuels.
2. Obtenir les poses latérales de combat du Chief et de l’Arbiter, puis leurs premiers clips de déplacement et d’attaque.
3. Produire six couches de Valhalla et les modules séparés du Scarab.
4. Intégrer un duel avec sprites, une route narrative et un tournoi local.
5. Etendre le roster en conservant les contrôles de fidélité, de données et de jouabilité.