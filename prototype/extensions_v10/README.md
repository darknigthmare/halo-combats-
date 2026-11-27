# Halo Combats — laboratoire des extensions V10

Ouvrir [`../halo_extensions_v10.html`](../halo_extensions_v10.html), directement depuis le dépôt ou depuis un serveur HTTP local. La page réutilise les images existantes de la V9 et fonctionne sans dépendance réseau.

Ce laboratoire rend consultables et exécutables des règles représentatives des extensions du guide : composition, déblocage, assistance, relais, super duo, taunt, finisher et épreuve de précision. Il n’implémente pas un jeu de combat complet. Les images sont des poses fixes candidates, sans nouveau clip, sans animation d’attaque, sans inversion horizontale et sans validation de fidélité graphique 1:1.

## Périmètre concret

- **22 dossiers représentatifs de la V9** : 11 personnages, 3 apparences, 4 stages, 4 modes. L’inventaire global continue dans le [catalogue V10](../halo_universe_v10.html).
- **Trois dimensions d’accès et une vérification de compatibilité** : découverte, source du droit, disponibilité des fichiers ou du mode, puis admissibilité dans la composition choisie.
- **Sélection réelle au sein du laboratoire** : actif, réserve, apparence, stage et mode. Un aperçu ne sélectionne ni ne débloque. Les doublons d’équipe sont refusés.
- **Simulation déterministe à 60 Hz** : commandes acceptées ou refusées, coûts, états d’action, santé, récupération, contrôle après relais et résultat final.
- **Deux objectifs d’apprentissage** : parcours de coordination (assistance, relais, super) et mini-épreuve de précision à 12 cibles.
- **Parcours de découverte en trois dossiers** : briefing, arsenal, archives. Les dépendances sont ordonnées et les récompenses sont réclamées explicitement.
- **Progression locale sauvegardée** sous la seule clé `halo-combats.extensions-v10.profile`, version de schéma 1.

Les fichiers `content.js` et `rules.js` peuvent être lus par Node et par le navigateur. `app.js` relie ces données aux commandes de la page. `style.css` définit l’interface responsive, les états de focus et la présentation à mouvement réduit.

## Sens de « simulation »

La page est un banc de règles. Les boutons « confirmer la touche », « rencontrer la garde » et « manquer la cible » imposent le résultat de la prochaine ouverture pour tester ses branches. Ils ne constituent pas un moteur de détection de collision. Les boutons d’impact sont des injections d’essai explicitement séparées des commandes normales.

Les PV de 1 000 par membre et les dégâts ci-dessous sont des valeurs originales d’adaptation. **Aucun système de bouclier énergétique n’est simulé**, pour aucun personnage. En particulier, sélectionner Buck ou Dare ne leur invente pas un bouclier. Les munitions, grenades, boîtes de collision, déplacements, garde réelle, commandes directionnelles, kit individuel, buffer d’entrée, rondes et netcode du jeu complet restent hors de ce module. Il ne remplace pas le laboratoire V8 et ne recopie pas ses écarts de valeurs avec la bible V1.

Les images ne jouent pas artificiellement une attaque grâce à une translation ou à un miroir CSS. Le HUD et le journal affichent les transitions calculées. Les événements `preselect`, `deselect`, `select_confirm` et `selection_idle` sont émis et consultables dans l’état du laboratoire ; les clips correspondant à ces événements restent à produire. La liste d’événements de menu est limitée aux 30 derniers et n’est pas une sauvegarde d’animations.

## Composition et continuités

Le profil est un **hybride à deux** : un actif et une réserve contrôlable ou mobilisable en soutien. Les deux membres possèdent leur propre santé. L’équipe perd lorsque les deux sont KO. Un partenaire KO ne participe pas à une super ou à un finisher et n’est pas ressuscité par une présentation.

Jerome et Alice de Halo Wars 2 sont proposés par défaut. Blood Gulch CE sert de fond d’exercice : cette juxtaposition est une simulation inter-époques, pas un événement de la chronologie. Le choix « Incarnations Halo 3 uniquement » impose la version de chaque dossier. Les ensembles Silver Timeline et Fractures sont séparés ; un dossier acquis dans un autre ensemble reste consultable, mais ne devient pas admissible dans l’équipe courante.

Le costume de l’Arbiter Halo 5 est adapté comme apparence de simulation avec des règles inchangées. Il est exclu du profil strict Halo 3. Buck Spartan Halo 5 n’est pas présenté comme un simple skin de Buck ODST dans cette sélection, puisque l’incarnation implique davantage qu’un changement de couleur. Les relations, costumes et scènes décrits par le catalogue gardent leur provenance.

## Règles d’équipe originales

| Action | Conditions et coût | Résolution |
|---|---|---|
| Attaque test | Actif libre ; coût 0 | 40 frames ; impact à f10 ; 80 PV sur touche ; +10 jauge, plafonné par combo |
| Assistance | Actif libre, partenaire vivant et disponible ; 25 jauge | Arrivée 18 f, action 6 f, sortie 24 f ; 120 PV ; récupération 300 f à la sortie |
| Relais volontaire | Actif libre, partenaire vivant, disponible et hors récupération ; 15 jauge | Transfert du contrôle à f18 ; retour au contrôle à f36 ; récupération du sortant 120 f à partir du transfert |
| Relais après KO | Un survivant existe | Gratuit, même si la jauge est vide ou le survivant en récupération ; un appel en cours est retiré proprement |
| Taunt | Actif libre ; coût et gain 0 | 60 f : entrée 18, pose 24, sortie 18 ; vulnérable ; sortie volontaire à partir de f42 ; un impact interrompt vers la réaction |
| Super duo en touche | Deux membres disponibles ; 75 jauge | Ouverture 18 f, scène 132 f ; 360 PV à la fin ; aucun gain de jauge |
| Super duo gardée | Même coût | 20 PV de dégâts résiduels, durée totale 60 f ; pas de longue scène |
| Super duo ratée | Même coût | Aucun dégât, durée totale 72 f ; pas de longue scène |
| Finisher d’équipe | Victoire déjà acquise, fenêtre 180 f, deux membres vivants et partenaire libre | Gratuit ; présentation de 120 f ; résultat et PV préservés |

La jauge est plafonnée à 100 et commence à 100. Elle n’a **aucune recharge passive**. Le budget de gain est de 25 par combo ; il est réinitialisé après 90 frames sans touche. Le relais conserve ce budget, la vie et les récupérations de chaque membre. Un appel refusé ne consomme rien. Deux commandes au même instant sont traitées séquentiellement dans la simulation ; la première réservation du partenaire ou de la jauge empêche une seconde dépense concurrente.

La récupération progresse sur l’horloge de jeu. La pause et le hitstop la gèlent. Les scènes de super confirmées et les présentations de finisher la gèlent aussi ; attendre une cinématique ne recharge donc pas gratuitement les partenaires. Le bouton « Abréger la scène » exécute les mêmes étapes déterministes et produit le même état final. Une super interrompue pendant l’ouverture ne rembourse pas son coût.

Un impact sur le soutien touche ses propres PV, retire son intervention et engage sa récupération. Un membre hors terrain ne reçoit pas un impact injecté réservé au soutien présent. Une attaque ou assistance déjà engagée conserve son identifiant de propriétaire après un changement d’actif.

La fin particulière « Coordination sangheili » exige N’tho Halo 3, Usze Halo 3, Valhalla Halo 3 et une cible Brute Halo 3. Il s’agit d’une **chorégraphie originale à produire**, pas de la reconstruction attestée d’une scène du jeu. Les autres configurations utilisent une conclusion de simulation générique. Si le partenaire est indisponible, l’expiration de la fenêtre conduit à la victoire standard sans modifier le résultat.

## Dossiers, conditions et droits

`contentState` renvoie séparément :

1. `discovery` : secret, indice/silhouette ou identifié ;
2. `access` : aucune source, permanent, temporaire, vérification en attente, expiré ou retiré ;
3. `technical` : aperçu disponible, visuel à produire, mode à produire ou erreur de chargement du fichier ;
4. `compatible` et les dépendances, avec tous les obstacles détaillés.

Un secret n’émet aucun portrait ni nom dans les éléments affichés ou leurs textes accessibles. Son code catalogue reste lisible dans les sources JavaScript : la protection évite les spoilers de l’interface, elle ne chiffre pas le catalogue. Le réglage permettant d’afficher les identités ne donne aucun droit de sélection.

Une source permanente valide prévaut sur l’expiration ou la révocation d’une autre source. Une vérification en attente n’est pas annoncée comme une expiration. Les mises à jour de source utilisent une révision monotone ; les doublons et les événements plus anciens sont ignorés. Ces règles sont couvertes par les tests unitaires ; **aucun service externe, paiement, compte d’abonné ni webhook n’est connecté à cette page**.

Les récompenses gagnées localement ont une source stable `reward/<id>`. Les réclamer deux fois ne crée pas de doublon. Un costume acquis avant son personnage reste acquis. Un personnage dont le visuel V9 est absent, ou un mode dont le contenu n’est pas produit, reste techniquement indisponible même après acquisition : le cadenas de progression ne masque pas ce manque.

Un PNG référencé qui échoue réellement au chargement reçoit l’état distinct « Fichier indisponible ». Les compositions qui l’utilisent ne peuvent pas lancer l’essai, mais leurs sources de droit sont conservées. Le rétablissement du fichier puis le rechargement de la page réévaluent sa disponibilité.

Le choix de mouvement réduit, la présentation statique et l’épreuve de précision restent disponibles sans condition payante. Les « récompenses » n’accordent que des choix dans ce laboratoire, pas des droits de compte ou une acquisition dans le jeu complet.

## Bonus et reprise

L’épreuve de précision utilise 12 marqueurs d’exercice d’interface, sans remplacer un ennemi Halo par un faux sprite. Une cible apparaît toutes les 120 frames, reste 240 frames, et le délai total est de 1 800 frames. L’objectif est 8 touches. Le temps étendu multiplie ces durées par trois et conserve les mêmes récompenses locales. Une cible touchée ne peut pas être comptée deux fois.

Le résultat n’est enregistré qu’après la fin de l’épreuve. Le meilleur score est conservé après un échec. L’identifiant de la partie empêche une double application du résultat et les acquisitions restent idempotentes. Les marqueurs sont activables par souris, tactile et clavier. Le temps s’arrête lorsque l’onglet est masqué ou qu’une autre section du laboratoire est affichée.

Les hordes avec ennemis et collisions, bonus de destruction, exploration physique, clashes/QTE, entités natives, pièges, projectiles persistants, deux curseurs locaux, manette, remappage complet, réseau et replays demeurent des exigences documentées à intégrer ultérieurement. Ce bonus de précision ne compte pas comme la livraison de tous ces systèmes.

## Sauvegarde

La sauvegarde contient les sources de droit, découvertes, meilleurs résultats, trois objectifs d’équipe, archives consultées, composition et préférences. La simulation en cours n’est pas sauvegardée : un nouvel essai réinitialise ses PV et jauges, tandis que la progression du laboratoire est conservée.

Un format futur ou un JSON corrompu n’est **jamais écrasé automatiquement**. L’interface conserve les octets existants et utilise une session temporaire. La réinitialisation demande une confirmation dans la page, puis retire uniquement la clé de ce laboratoire. Elle n’efface pas les sauvegardes des autres prototypes. Si le navigateur refuse le stockage, le message indique l’absence de sauvegarde et les essais restent possibles.

Cette version définit son propre schéma 1, sans prétendre migrer une sauvegarde de jeu ou une progression V8 existante. Les valeurs chargées sont validées, les identifiants inconnus sont refusés, et les champs non reconnus ne sont pas propagés dans le profil utilisé.

## Vérification

```sh
node --check prototype/extensions_v10/rules.js
node --check prototype/extensions_v10/content.js
node --check prototype/extensions_v10/app.js
node --test prototype/qa_v10/extensions.test.cjs
```

Les 30 tests ciblent les invariants concrets : sélection verrouillée, secret accessible, branches ET/OU, acquisition répétée, dépendance de costume, plusieurs sources de droit, expiration, événement plus ancien, assets absents, continuité, doublons, parcours d’archives, double réservation, absence de jauge, interruption, relais gratuit après KO, conservation du combo et des PV, pause, taunt, trois issues de super, abrègement, résultat de finisher, bonus et sauvegarde.

**Résultat du 27 novembre 2026 : 30 tests Node réussis, 0 échec.** Ces tests de logique ne certifient ni les images ni les animations.

La vérification navigateur est distincte : **26 assertions réussies, 0 erreur JavaScript**, sur Chromium 158.0.8127.0 piloté par Playwright, aux formats 1 365 × 1 000 et 390 × 844. Le parcours clique les commandes de coordination, réclame puis sélectionne un personnage, termine les 12 cibles par leurs vrais boutons, recharge la progression, vérifie la sauvegarde corrompue et la réinitialisation limitée à ce laboratoire, et injecte un PNG manquant pour vérifier le refus explicite. Il contrôle aussi l’absence de débordement horizontal, les cibles tactiles et l’ouverture locale `file:`.

Le [reçu navigateur](../qa_v10/extensions_browser_results.json) conserve les assertions, le périmètre, les limites et les SHA-256 des sept fichiers exécutés ou associés à la vérification. Les six captures `extensions_*.png` sont conservées dans `prototype/qa_v10/` ; leur mise en page a été relue. Le [harness réexécutable](../qa_v10/extensions.browser.cjs) crée son propre serveur HTTP temporaire et nécessite Playwright dans l’environnement de QA :

```sh
node prototype/qa_v10/extensions.browser.cjs
# Si Chromium n’est pas installé dans le cache Playwright :
HALO_CHROMIUM_PATH=/chemin/vers/chromium node prototype/qa_v10/extensions.browser.cjs
```

Ces 26 assertions sont un contrôle de ce parcours représentatif. Elles ne remplacent pas les cas d’acceptation complets des guides, une recette manette, réseau ou multijoueur, ni une réception artistique 1:1.
