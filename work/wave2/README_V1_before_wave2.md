# Halo Combats

Mode annexe de combat 2D et Boss Battle. Version 1 du 19 novembre 2026, pour Darknigthmare.

## Ouvrir le dossier

- `docs/HALO_COMBATS_BIBLE_V1.docx` : bible de conception avec sommaire cliquable.
- `docs/HALO_COMBATS_BIBLE_V1.md` : version texte structurée de la bible.
- `docs/HALO_COMBATS_PRODUCTION_V1.xlsx` : suivi filtrable des combattants, spéciaux, histoires, boss, arènes et premiers assets.
- `prototype/halo_combats_prototype.html` : prototype autonome à ouvrir dans un navigateur, sans serveur ni connexion.
- `assets/candidates/` : quatre PNG candidats individuels du premier lot.
- `docs/ETAT_PRODUCTION_V1.md` : contrôles restants, générations refusées et prochaines étapes.
- `data/` : registres JSON de conception, sources, prompts, empreintes et plan d’animation.

## Contenu défini

La bible décrit 24 combattants, 264 normales, 96 spéciaux, 24 supers, 48 propositions de combos, 24 routes avec introduction, rival et ending, 48 finishers, 20 rencontres de boss et 24 arènes à six couches. Les valeurs d’équilibrage et les routes narratives sont des créations pour cette adaptation 2D.

Les quatre candidats visuels sont l’Arbiter de Halo 3, le Scarab de Halo 3, Valhalla et New Mombasa de nuit. Ils restent à comparer aux modèles et lieux de référence. Aucun clip finalisé ni asset certifié 1 à 1 n’est déclaré livré. Le Chief reste sans image après deux refus automatiques de génération.

Le plan d’animation propose 44 clips par combattant. Ses 1 056 lignes et son budget de dessins décrivent un travail à produire ; ce ne sont pas des fichiers déjà générés. Les deux décors sont des concepts maîtres. Les 144 couches parallaxe de production sont encore à fabriquer.

## Jouer au prototype

Choisir Entraînement, Duel IA ou Boss Scarab. Déplacement avec les flèches ou Q D, saut avec Espace, dash avec Maj, léger J, lourd K, tir L, grenade U, impulsion I, garde O et pause P. Contre le Scarab, casser les deux jambes vulnérables, rejoindre la balise centrale et utiliser E pour monter, puis attaquer le noyau sur le pont. Les boutons tactiles sont également présents.

Le prototype utilise des silhouettes techniques temporaires. Il ne contient qu’un personnage contrôlable, un adversaire IA et un boss. La campagne, les tournois, les fatalités, le réseau et le roster complet restent des spécifications de la bible.

Dix-sept tests de logique ont réussi, dont une victoire complète contre le Scarab au corps à corps. La vérification visuelle dans Chromium n’a pas pu être exécutée : l’environnement a bloqué le lancement du navigateur. Les scénarios de reprise et le résultat détaillé figurent dans `prototype/qa/`.

## Références et fidélité

Les registres `fighter_sources.json`, `world_sources.json` et `docs/source_registry.json` conservent les URLs et la portée des références. Une source sur une famille de véhicules n’est pas présentée comme une preuve du dessin exact de chaque variante. Les variantes d’armure, les versions d’épisodes, les contenus abandonnés et les propositions originales sont distingués.

Le manifeste des quatre PNG contient leur taille, mode couleur, alpha, empreinte SHA-256, prompt initial, correction et contrôle restant. Les anciennes variantes non retenues ne remplacent pas les candidats actifs du dossier.

## Données de suivi

Les statuts de conception, visuel, animation, intégration et fidélité sont indépendants. La synthèse du classeur se recalcule à partir de la feuille Assets. Le registre JSON de règles reste la référence détaillée des mouvements, et le classeur sert à la production.

`SHA256SUMS.txt` permet de vérifier les fichiers du paquet. Aucun contenu externe n’est nécessaire pour ouvrir le prototype.
