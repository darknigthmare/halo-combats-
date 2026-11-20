# Halo Combats — laboratoire V7

Le laboratoire V7 relie les images candidates existantes au prototype mécanique : **24 identités de base sélectionnables**, entraînement, duel contre l’IA, rencontre Scarab et catalogue documenté. Les 24 identités partagent les mêmes règles de simulation. Leurs movesets individuels ne sont pas implémentés.

Il s’agit d’une nouvelle page indépendante ; le prototype V1 et les journaux de génération V6 restent inchangés.

## Ouvrir le laboratoire

Conserver la structure complète du dépôt, notamment `assets/`, `data/` et `prototype/`.

Ouvrir directement `prototype/halo_combats_lab_v7.html` dans un navigateur récent. Le fichier charge les scripts classiques locaux `lab_v7/catalog.js` puis `lab_v7/app.js`. Le bootstrap contient les mêmes données que `data/prototype_asset_bindings_v7.json` ; aucun `fetch` n’est nécessaire pour ce parcours `file://`. Les PNG sont chargés depuis leurs chemins locaux, sans CDN ni données d’image encodées dans le code.

Un serveur statique est aussi possible. Depuis la racine du dépôt :

```bash
python -m http.server 8000 --directory .
```

Ouvrir ensuite :

```text
http://localhost:8000/prototype/halo_combats_lab_v7.html
```

Si le bootstrap est absent, le mode HTTP peut lire le JSON directement. Une ouverture `file://` sans `catalog.js` affiche une erreur explicite au lieu de prétendre charger le roster.

Le parcours d’ouverture est couvert par les tests de bootstrap et de chargement simulé. **Le rendu dans un navigateur n’a pas pu être observé dans l’environnement de livraison**, car Chromium a échoué avant l’ouverture de la page sur une permission de création de socket. La procédure navigateur reproductible figure plus bas.

## Contenu du laboratoire

| Fonction | État V7 |
| --- | --- |
| Sélection P1 / adversaire | 24 identités de base ; noms et jeux d’origine provenant du catalogue |
| Entraînement | Mannequin, énergie renouvelée, remise à zéro après KO |
| Duel IA | Une manche de 99 secondes, IA, résultat et redémarrage |
| Scarab | Trois phases mécaniques : jambes, abordage, noyau ; parcours possible au corps à corps |
| Images en combat | PNG neutres et poses statiques de garde disponibles, chargés à la demande |
| Garde du Major | Garde mécanique active ; pose neutre conservée et absence de pose dédiée signalée |
| Décor | Choix entre les deux masters existants ; une image de fond complète par scène |
| Catalogue personnages | 24 bases + 34 extensions = 58 entrées |
| Catalogue boss | 20 entrées ; seul le Scarab possède une rencontre mécanique dans ce laboratoire |
| Catalogue décors | 24 entrées ; deux possèdent un master PNG, 22 restent sans image |
| Recherche et filtres | Nom, jeu, identifiant, catégorie et état du visuel, y compris les variantes anciennes à corriger |
| Sources | Liens documentaires explicites ; aucun téléchargement automatique depuis ces liens |
| Extensions | Consultation uniquement ; aucune sélection en combat |

Les variantes conservent leurs états propres. Le filtre **À corriger** trouve les six entités possédant un PNG dans cet état et ouvre la variante concernée. **Hieu Dinh** est explicitement signalé comme candidat à corriger, sans visuel préféré et sans accès au combat. Les trois modules de boss partiels affichent leur zone représentée et l’absence de silhouette totale. Une image manquante donne un état vide ; aucune image d’un autre personnage ne lui est substituée.

## Commandes

| Action | Clavier |
| --- | --- |
| Déplacement | Flèches gauche / droite, Q D ou A D |
| Saut | Espace, flèche haut, Z ou W |
| Dash | Maj |
| Coup léger | J |
| Coup lourd | K |
| Tir | L |
| Grenade | U |
| Impulsion d’énergie | I |
| Garde maintenue | O |
| Monter sur le Scarab | E près de la balise, après destruction des jambes |
| Pause / reprise | P |

Des boutons tactiles couvrent les mêmes actions. La perte de focus, l’ouverture des commandes et l’entrée dans le catalogue mettent le combat en pause et relâchent les entrées maintenues. Le retour au laboratoire conserve la pause jusqu’à reprise explicite. Les champs de recherche, sélecteurs et dialogues ignorent les raccourcis de combat. Espace et Entrée gardent leur comportement natif sur les boutons et liens.

## Rendu des images et fidélité

Les PNG restent des **poses statiques d’étude**. Le moteur déplace ou fait sauter la pose entière ; les coups ajoutent des effets graphiques. Il ne joue ni animation de course, ni frames d’attaque, ni sprite sheet.

L’orientation native est conservée. **Aucune inversion horizontale** n’est appliquée aux images, afin de préserver les asymétries de l’équipement et des armures. Une flèche au sol indique la direction mécanique des attaques. Elle peut donc différer de l’orientation du visuel. Une orientation non documentée reste indiquée comme non déterminée.

Chaque `drawImage` utilise l’image source entière, sans découpe de région. Les boîtes alpha servent uniquement à calculer une échelle et à poser les pieds sur le sol ; elles ne modifient aucun pixel ni aucun fichier PNG. Le catalogue affiche également chaque source entière avec `object-fit: contain`.

La caméra rapproche le duel lorsque l’espace le permet. Elle adapte sa projection à l’enveloppe complète des PNG, aux sauts, aux grandes silhouettes aux limites du monde et au saut depuis le pont du Scarab. Ces ajustements ne changent ni les coordonnées mécaniques, ni la physique, ni les boîtes de collision. Les collisions restent celles du prototype partagé ; leur option d’affichage aide à constater cet écart avec les illustrations.

Le Scarab est une seule illustration entière et statique. Les deux cibles des jambes, le pont, la balise et le noyau sont des repères de simulation en surimpression. Le PNG ne simule ni effondrement des jambes ni ouverture réelle de panneaux. Les deux décors sont des masters complets affichés en un plan de fond ; aucun parallaxe à plusieurs calques n’est annoncé.

En cas de fichier indisponible, le combat affiche un **repère technique explicitement nommé**. Le catalogue affiche « Image indisponible » et conserve les métadonnées. Ces secours ne sont pas présentés comme des images fidèles du personnage.

Le cache conserve au plus **10 images chargées**, avec **deux requêtes simultanées**. Les images en cours d’utilisation et le détail du catalogue restent épinglés ; les demandes obsolètes qui n’ont pas démarré sont abandonnées lors d’un changement de sélection. Les erreurs ne sont pas retentées à chaque frame. Le nombre d’octets décodés exposé par le harness est une estimation, pas une mesure de la mémoire réelle du navigateur.

## Mécaniques conservées

Le cœur du prototype V1 reste à 60 Hz avec buffer d’action de huit frames : déplacement, saut, dash, coups léger/lourd, tir, grenade, impulsion, garde de face, dégâts, recul, hitstop, recharge du bouclier, IA, télégraphies du Scarab, progression des trois phases et redémarrage.

Les valeurs sont communes aux 24 choix : 1 000 PV, 200 de bouclier, deux grenades et trois segments d’énergie. Elles restent des valeurs de laboratoire. Les silhouettes et dimensions visuelles ne constituent pas des volumes de collision validés pour un jeu compétitif.

Les modes histoire, intro/rival/ending jouables, tournoi, fatalités, movesets distincts, commandes directionnelles avancées, multijoueur, rollback, audio, sauvegarde et animations finales ne sont pas implémentés dans cette page. Les documents de conception du projet restent la référence pour ces travaux.

## Vérifications livrées

Depuis la racine du dépôt :

```bash
node prototype/qa_v7/logic.cjs
```

Le rapport `prototype/qa_v7/results.json` contient **34 contrôles passés**, leurs noms et les SHA-256 exacts des fichiers testés. Les scénarios couvrent les règles de combat conservées, le parcours Scarab au corps à corps, les 24 sélections, les états du catalogue et de ses variantes, la pause, les raccourcis, les erreurs de chargement, le cache, le cadrage mathématique et les références des 90 PNG.

Ces tests utilisent un DOM, un canvas et un cycle de chargement d’image **simulés** dans Node. Les dimensions d’en-tête et empreintes des vrais fichiers PNG sont vérifiées. Le test confirme les arguments de dessin, l’absence de miroir/découpe et la logique des secours ; il ne certifie pas le rendu des pixels ou l’ergonomie sur un appareil réel.

### Navigateur : blocage documenté et scénario reproductible

Un lancement de Chromium a été tenté pendant l’implémentation. Il a avorté avant l’ouverture de la page :

```text
process_singleton_posix.cc:297
socket() failed: Operation not permitted (1)
```

La preuve séparée est `prototype/qa_v7/browser_block.json`. Aucun autre essai n’a été effectué après ce refus de permission. Aucun contrôle visuel desktop/mobile ni capture de navigateur n’est annoncé comme réalisé. Le script Node ne tente pas de lancer Chromium lorsqu’il relit ce constat.

Dans un environnement disposant de Playwright et d’un Chromium autorisé :

```bash
node prototype/qa_v7/verify_browser.cjs
```

Le script utilise l’ouverture locale par défaut. Les paramètres facultatifs sont :

| Variable | Utilité |
| --- | --- |
| `HALO_PLAYWRIGHT_MODULE` | Chemin du module Playwright si sa résolution standard ne le trouve pas |
| `HALO_CHROMIUM_PATH` | Chemin d’un exécutable Chromium ; `/usr/bin/chromium` est utilisé s’il existe |
| `HALO_TEST_URL` | URL HTTP à tester à la place de l’ouverture locale |
| `HALO_QA_SCREENSHOT_DIR` | Dossier de captures facultatif, de préférence hors du dépôt |

Le scénario vérifie le chargement réel des images, les sélections, les commandes, les trois phases du Scarab, les états du catalogue et l’absence de débordement horizontal à 1 440 et 390 pixels de largeur. Il écrit son propre `browser_results.json`. Si des captures sont demandées, elles restent à inspecter visuellement ; leur création seule n’est pas une validation de l’interface.

## Fichiers de cette version

- `prototype/halo_combats_lab_v7.html` : interface indépendante.
- `prototype/lab_v7/app.js` : moteur partagé, projection des PNG, cache, catalogue et interactions.
- `prototype/lab_v7/style.css` : mise en page responsive.
- `prototype/lab_v7/catalog.js` : bootstrap produit depuis les bindings JSON par le générateur de métadonnées.
- `data/prototype_asset_bindings_v7.json` : données et associations des assets ; source lisible du bootstrap.
- `prototype/qa_v7/logic.cjs` : contrôles reproductibles sans navigateur.
- `prototype/qa_v7/verify_browser.cjs` : scénarios navigateur à reprendre dans un environnement compatible.
- `prototype/qa_v7/results.json` et `browser_block.json` : résultats et limites de vérification.

Cette intégration réutilise les images existantes. Elle n’ajoute aucune image de personnage à la vague V7 et ne transforme aucun candidat en asset certifié 1:1.
