# Halo Combats

## Bible de conception du mode de combat 2D

Version 1 du 19 novembre 2026 — Projet de Darknigthmare

Cette bible réunit les règles du duel, les parcours narratifs, le roster initial, les rencontres de boss et les arènes. Elle définit 24 combattants, 264 normales, 96 spéciaux, 24 supers, 24 routes, 48 exécutions, 20 rencontres de boss et 24 arènes. Les visuels, animations et intégrations sont suivis séparément dans le registre de production.

Les identités et incarnations visuelles se réfèrent aux œuvres Halo citées. Les valeurs de combat, parcours d’arcade et transformations en affrontements 2D sont des propositions de conception originales. La validation graphique un pour un demande une comparaison avec la version de jeu indiquée sur chaque fiche.


# Partie 1 Règles et production

Version 1 du 19 novembre 2026. Projet de Darknigthmare.

Halo Combats est un mode annexe de combat en vue latérale. Il transforme les différences entre Spartans, ODST, Sangheili, Jiralhanae et Lekgolo en styles de jeu lisibles, tout en conservant les armures, les armes, les silhouettes et les lieux propres à chaque épisode. Son deuxième pilier est un mode Boss Battle où un combattant affronte des véhicules, des constructions et des organismes de grande taille au cours de rencontres à objectifs.

Cette bible définit un premier ensemble de 24 combattants, 24 arènes et 20 rencontres de boss. Elle réunit les règles de combat, les routes narratives, les commandes, les modes de jeu, les spécifications visuelles et les critères de production. Les chiffres de dégâts, les fenêtres en frames, les scénarios de tournoi et les chorégraphies de finishers sont des créations destinées à cette adaptation. Ils ne sont pas des valeurs extraites des jeux Halo.

### Identité et promesse de jeu

Le duel doit évoquer Halo dès les premières secondes : un bouclier cède, une grenade impose un déplacement, une arme impose sa portée, puis une action au contact décide de l'échange. Les personnages disposent d'une vraie grammaire de jeu de combat : garde haute et basse, projections, anti-airs, confirmations, annulations, contres et récupération. La profondeur vient de la rencontre de ces deux systèmes.

Le style visuel visé est un rendu 2D UHD détaillé, avec silhouettes entières et animation image par image. La caméra reste latérale pendant les échanges. Les intros et les finishers peuvent employer d'autres cadrages, puis revenir exactement à l'ancrage du combat. Un costume doit pouvoir être identifié sans lire son nom. Un déplacement doit rester compréhensible sans effet lumineux.

### Règle de fidélité

Chaque fiche possède une incarnation de référence : jeu, version visuelle, armure, équipement et contexte. Le Chief en Mark VI GEN3 appartient à la référence Halo Infinite ; son Mark V de Combat Evolved et son Mark VI des autres épisodes sont des ensembles séparés. Halo Waypoint distingue explicitement plusieurs de ces armures dans Master Class [S01]. Une armure alternative ne donne pas automatiquement accès à l'équipement d'une autre époque.

La fidélité doit être vérifiée sur cinq axes : silhouette, construction de l'armure, anatomie, matériaux et équipement. Le nom d'un personnage dans un prompt ne constitue pas une validation. Une illustration générée reste candidate jusqu'à comparaison avec les références. Les proportions d'affichage peuvent être adaptées dans une plage documentée pour le duel ; les véhicules géants gardent leur rôle de structures dans la scène Boss Battle.

Un même identifiant logique peut posséder plusieurs costumes. Une incarnation dont les capacités changent devient un profil de règles distinct, lié au personnage parent. Aucun nouveau personnage n'est compté uniquement parce que sa couleur change. Les concepts abandonnés et la continuité télévisée sont étiquetés séparément. Un concept officiel ne prouve pas à lui seul qu'un contenu a été prévu pour être jouable ; Halo Waypoint rappelle explicitement cette distinction [S02].

## Organisation du contenu

### Sélection des combattants

L'écran présente les factions puis les personnages. La fiche affiche l'incarnation, l'archétype, la portée privilégiée, la difficulté, la ressource personnelle et les commandes principales. Le portrait de sélection et le sprite de combat sont deux images différentes. Le choix du costume conserve la miniature de sa propre armure. Un personnage masqué ou casqué ne reçoit pas automatiquement une variante démasquée.

Le roster de base privilégie les différences d'action : polyvalence du Chief, allonge de l'Arbiter, contrôle de zone de Jorge, pièges de Kat, tir préparé de Jun, mobilité de Noble Six, pression lourde des Brutes et défense directionnelle du Hunter. Les fiches détaillées établissent le contre-jeu de chaque capacité. Les personnages humains sans bouclier ne reçoivent pas un bouclier Mjolnir fictif pour uniformiser l'interface.

### Extensions de catalogue

Les extensions prévues couvrent Blue Team, Fireteam Osiris, Alpha Nine, les protagonistes des Halo Wars, les chefs covenants et les Parias, les unités Flood et les constructions forerunners. Chaque ajout passe par le même contrôle d'incarnation. Les candidats comprennent Fred, Kelly, Linda, Locke, Tanaka, Vale, Dare, Dutch, Romeo, Mickey, Forge, Anders en rôle de soutien, Cutter comme commandement, Ripa 'Moramee, Sesa 'Refumee, les Prophètes en rencontres scénarisées, Shipmaster de Halo Wars 2, Colony, Yapyap, Pavium, Voridus, le Didacte et la Harbinger. Une candidature n'est pas une fiche complète ni une illustration produite.

Les unités génériques ont leur propre gamme de variantes : Marine, ODST, Spartan personnalisable, Elite Minor, Major, Ultra, Ranger, Spec Ops et Zealot, Jackal, Skirmisher, Grunt et Brute. Les petites espèces demandent des règles de hurtbox et de franchissement spécifiques avant admission au classé. Cortana, l'Arme, les Monitors et les personnages de commandement sont d'abord prévus comme narrateurs, objectifs, soutiens ou avatars de menu. Les transformer en combattants physiques exige un concept de jeu explicitement original.

Le corpus de référence distingue Combat Evolved et son édition Anniversary, Halo 2 et Anniversary, Halo 3, ODST, Reach, Halo 4, Halo 5, Infinite, Halo Wars, Halo Wars 2, Spartan Assault, Spartan Strike et Fireteam Raven. Les romans, comics, Legends, Forward Unto Dawn et Nightfall peuvent alimenter les extensions après établissement d'une référence visuelle. Les publications ultérieures sont ajoutées avec leur statut de disponibilité effectivement vérifié. La continuité Silver de la série télévisée reste une catégorie distincte.

## Système de combat

### Commandes communes

Le mode standard emploie six boutons et une direction relative à l'adversaire. L est le coup léger, M le moyen, H le lourd, R l'arme à distance, G la grenade et A l'aptitude. Arrière maintenu effectue la garde haute ; bas et arrière effectuent la garde basse. Haut saute, bas s'accroupit, deux pressions avant ou arrière déclenchent le dash correspondant. L et M ensemble projettent. M et H ensemble déclenchent le briseur défensif lorsque les conditions sont remplies.

La notation utilise le pavé numérique pour un personnage tourné vers la droite : 5 neutre, 2 bas, 6 avant, 4 arrière, 8 haut. 236 signifie quart de cercle avant, 214 quart de cercle arrière, 623 mouvement de type dragon. j.L désigne un léger en l'air. Les commandes se retournent lorsque le personnage change de côté. Une option affiche les flèches à la place des chiffres.

Le mode simplifié remplace les mouvements par A et une direction, tout en gardant les mêmes coûts, fenêtres et dégâts. Il n'ajoute ni priorité ni invulnérabilité. Les raccourcis de projection, dash et super peuvent être assignés. Le contrôle tactile utilise une zone directionnelle et six boutons dont la taille et la position sont modifiables. Les actions à maintien disposent d'une option bascule compatible avec les règles du match.

### Paramètres de base

La simulation fonctionne à 60 mises à jour par seconde. Une frame représente environ 16,67 millisecondes. L'affichage peut fonctionner à une autre fréquence, mais il n'altère ni la vitesse des attaques ni leur portée. Le duel standard se joue en deux manches gagnantes, avec 99 secondes par manche. Les paramètres de tournoi peuvent imposer trois manches gagnantes.

Le gabarit de référence d'un Spartan possède 1 000 points de santé et 200 points de bouclier. Ces valeurs sont des paramètres de conception. Les fiches peuvent les modifier dans des bornes expliquées. La garde est mécanique et ne correspond pas au bouclier : un personnage peut se défendre même si son bouclier a été épuisé. La barre d'énergie comporte trois segments de 100 unités. Le stock de grenades est plafonné à deux.

La fenêtre de mémorisation des commandes est de six frames. Les séquences directionnelles sont reconnues sur vingt frames, avec une tolérance de deux directions neutres. La dernière direction pertinente doit dater de six frames au plus au moment du bouton. Les priorités sont super, spécial, projection puis normal. Une direction simultanée opposée devient neutre. Une option d'aide visuelle indique pourquoi une commande n'a pas été reconnue.

### Déplacement et espace

Chaque personnage a des vitesses distinctes de marche avant, marche arrière et dash. Le dash avant possède une phase de départ punissable ; le dash arrière n'est pas invincible par défaut. Le saut est un engagement avec trajectoire lisible, sans correction aérienne libre. Certains personnages obtiennent une aptitude de mobilité spécifique qui consomme une ressource ou impose une récupération.

Les corps se bloquent au sol. Ils peuvent se croiser dans les airs lorsque leurs boîtes le permettent. Le coin n'autorise pas à traverser une cible immobilisée. Le jeu recalcule le côté de garde avant chaque nouvelle action, mais ne retourne pas artificiellement un projectile déjà lancé. Les zones de frappe sont indépendantes du dessin et consultables en entraînement.

Les tailles sont conservées autant que possible : un Hunter est clairement plus massif qu'un Spartan, lui-même plus massif qu'un ODST. La caméra ajuste son cadre avant le début de la manche en fonction des deux gabarits. Elle ne réduit pas soudainement le personnage pour masquer un problème d'espace. Les très grandes unités sont réservées au mode Boss Battle.

### Coups et défense

Le léger standard démarre entre cinq et sept frames, le moyen entre huit et douze, le lourd entre treize et vingt-deux. Les exceptions sont indiquées dans la fiche. Toute attaque décrit son anticipation, ses frames actives, sa récupération, sa hauteur, son déplacement, ses dégâts, son avantage en garde et sa fenêtre d'annulation. Les attaques puissantes ont une réponse possible : sauter, se baisser, interrompre, esquiver ou punir la récupération.

La garde haute bloque les coups moyens, hauts et overheads, y compris les attaques aériennes signalées comme overhead. La garde basse bloque les moyens, les hauts dont la hitbox atteint la cible accroupie et les bas ; elle échoue contre les overheads. Un coup haut peut passer au-dessus d'une cible accroupie sans la toucher. Un overhead doit avoir une anticipation visuelle distincte. Les projections ratent une cible hors portée, invulnérable à la projection ou déjà en état aérien. Le déchoppage accepte L et M dans une fenêtre de sept frames, sauf projections de commande explicitement signalées. Une projection de commande consomme une ressource ou impose une longue récupération en cas d'échec.

La garde parfaite intervient pendant les trois premières frames d'une garde correcte. Elle réduit le recul et donne une petite quantité d'énergie ; elle n'annule pas automatiquement toute pression. Le briseur défensif coûte deux segments d'énergie et repousse l'attaquant. Il est disponible pendant une garde ou certains états de hitstun, une seule fois par combo, puis devient indisponible pendant un délai documenté. Il ne peut pas interrompre une cinématique de fin de match.

### Bouclier et santé

Le bouclier absorbe d'abord les dégâts qui lui sont assignés. Une rupture produit un son et un contour reconnaissables. Le calcul distingue bouclier, santé, garde, armure temporaire et invulnérabilité ; ces états ne sont jamais représentés par la même couleur seule. La recharge commence après 240 frames sans dommage ni contact bloqué et rend deux points par frame. Une nouvelle pression remet le délai à zéro. Aucun soin de santé automatique n'est accordé au duel standard.

Le plasma peut avoir un coefficient de dégâts de bouclier supérieur à son coefficient de santé. Le projectile balistique peut présenter le comportement inverse. Ces coefficients sont des réglages de jeu, jamais une obligation d'utiliser des munitions réelles. Les armes spéciales possèdent des ressources finies par séquence, une chauffe ou une récupération. Le tir ne doit pas permettre de gagner simplement en maintenant R à distance maximale.

Pour limiter l'attente systématique, le règlement classé désactive la recharge durant les quinze dernières secondes. Le départage au temps compare le ratio de santé et de bouclier énergétique restants sur leur maximum cumulé. La plaque physique du Hunter est exclue de ce calcul. Pour un personnage sans bouclier, le ratio correspond simplement à sa santé restante sur sa santé maximale. Une égalité parfaite rejoue la manche. Le temps ne diminue pas pendant une pause autorisée hors réseau ou une présentation obligatoire.

### Armes et grenades

Une arme à distance fait partie du kit : elle ne transforme pas tout combattant en tireur identique. Le fusil automatique produit une rafale courte avec récupération, le sniper demande une préparation audible et le lance-roquettes consomme une munition lente à récupérer. La cadence, le recul et la portée se lisent dans l'animation. Une attaque à distance à bout portant peut perdre contre un normal rapide.

Les grenades ont un arc, un temps d'amorçage et un avertissement. Deux grenades au maximum sont détenues et deux au maximum peuvent appartenir à un même joueur dans la scène. Le réapprovisionnement standard exige 600 frames de temps actif depuis la consommation d'une charge, sans pause de chrono exploitable. Les variantes de campagne peuvent utiliser des ramassages. Une grenade plasma collée demeure visible et sonore ; ses interactions avec les projections et les transitions sont déterministes.

Les explosions ne se contentent pas d'une boîte rectangulaire invisible : le rayon réel et sa durée sont enregistrés, les obstacles éventuellement protecteurs sont explicitement marqués. Dans les arènes classées, le décor ne bloque pas les tirs. Les dégâts environnementaux sont désactivés. Les situations avec une grenade persistante après KO se terminent selon une règle commune : le résultat est arrêté lorsque tous les événements déjà déclenchés de la fenêtre de double KO ont été résolus.

### Combos et annulations

Les routes ordinaires permettent L vers M vers H, puis un spécial compatible, puis un super autorisé. Certaines branches sont interdites pour préserver les différences de roster. Un coup manqué ne s'annule pas sauf exception écrite. Le troisième usage du même starter dans un combo réduit fortement le hitstun. Un compteur de juggle et un budget de rebonds empêchent les boucles aériennes.

Les multiplicateurs proposés pour les dégâts successifs sont 100, 90, 80, 70, 60, 50, 40 puis 35 pour cent. Un minimum spécifique protège la valeur d'un super sans garantir un combo mortel. Le total théorique visé pour une confirmation simple est de 180 à 260 dégâts ; une route exigeante avec deux ressources vise 350 à 450. Les valeurs finales doivent être mesurées après intégration, et les routes des fiches restent des intentions à tester.

La chute autorise récupération au sol, relevée normale ou retardée selon l'état reçu. Les invulnérabilités de relevée ont une durée explicite et ne peuvent être prolongées par une entrée répétée. Le training affiche l'état, l'avantage, les ressources consommées et la raison d'une rupture de combo.

## Modes de jeu

### Histoire et parcours individuels

Le cadre original est une archive de simulations nommée Archives de combat. Ce dispositif permet de proposer des rencontres entre époques sans les présenter comme des événements historiques officiels. Le joueur choisit une route située, une reconstitution libre ou une simulation hypothétique. L'interface annonce ce statut avant l'introduction. Les simulations sont un choix de mise en scène du projet ; elles ne prétendent pas raconter un nouveau chapitre canonique.

Une route individuelle comprend une introduction en trois plans, deux duels d'apprentissage, un incident de terrain, deux confrontations de faction, une scène avec le rival, le duel de rivalité, une rencontre de boss et une conclusion en trois plans. Les introductions et les endings emploient des images distinctes. Les combats secondaires tournent dans un groupe cohérent au lieu de répéter toujours la même échelle. Un chapitre terminé peut être rejoué sans revoir toute la route.

Le rival exprime un conflit de méthode, une opposition historique ou un miroir de gameplay. Il n'est pas choisi uniquement parce qu'il appartient à une autre faction. Une route de Johnson peut mettre en scène son rôle de protecteur ; une route de l'Arbiter interroge les ordres et le choix d'une alliance ; une route de Kat met l'information et les accès au centre des objectifs. Chaque ending doit résoudre l'enjeu introduit. Une victoire de simulation ne ressuscite pas un personnage dans la continuité officielle.

La campagne de référence se structure en six actes : prise en main UNSC, différences entre Spartans et ODST, conflit covenant, rupture et alliances, menace Flood, puis conflit avec les Parias. Les actes débloquent des dossiers de lore, des palettes admissibles et des éléments de galerie. Ils ne débloquent pas de bonus de dégâts pour le classé.

### Arcade et versus

L'arcade propose une échelle courte de cinq combats ou une échelle longue de huit, avec un rival prédéfini et un boss optionnel. La difficulté modifie les décisions de l'IA et ses erreurs, sans lecture des entrées avant qu'une action soit engagée. Les rencontres et récompenses sont reproductibles à partir d'une graine enregistrée.

Le versus local permet humains, IA et miroir. Le mode équipe peut utiliser trois personnages en relais, sans assistances simultanées dans sa première version. Un mode tag avec entrée, sortie et combo d'équipe est une extension à équilibrer séparément. Les règles personnalisées affichent clairement leurs écarts : énergie infinie, gravité, hazards, stocks et multiplicateurs. Elles ne se mélangent pas aux statistiques classées.

### Tournois

Le tournoi local accepte 4, 8, 16 ou 32 participants, humains et IA, avec noms modifiables et têtes de série. Le format à élimination simple qualifie le gagnant de chaque match. Les places vacantes sont des exemptions explicites ; elles ne simulent pas un match ni ne produisent de statistiques de coups.

La double élimination utilise deux tableaux. La première défaite envoie dans le tableau inférieur, la seconde élimine. Une grande finale contre le vainqueur invaincu exige une remise à zéro si ce dernier perd le premier set. Le format toutes rondes utilise les victoires de sets, puis la confrontation directe, puis la différence de manches. Les égalités persistantes déclenchent un match de départage.

Un set se joue au meilleur de trois matchs, puis au meilleur de cinq pour les finales selon le règlement choisi. Le perdant peut changer de personnage ; le gagnant conserve le sien. Les arènes classées sont sélectionnées par alternance de bans dans un ensemble prévalidé. La sauvegarde intervient après chaque résultat confirmé. Un résultat peut être corrigé avant de lancer le match suivant, avec historique local de correction.

### Boss Battle

Le joueur conserve son personnage, ses commandes et ses ressources. La scène modifie la nature de l'objectif : esquiver un bombardement, ouvrir un blindage, prendre un ascenseur, atteindre une plateforme ou protéger une équipe d'extraction. Les personnages de mêlée disposent toujours d'un accès valable aux points faibles. Aucun boss ne doit exiger un projectile que certains personnages ne possèdent pas.

Les formats sont opération libre, Boss Rush, entraînement de phase et coopération à deux. La coopération vise initialement 1,7 fois la santé des points faibles, et non deux fois toutes les attaques. Les réanimations nécessitent une zone sûre et une canalisation interrompue par un dommage. La télégraphie indique la cible et la zone affectée sans cacher les pieds des combattants.

La difficulté peut raccourcir les temps morts, ajouter une combinaison d'attaques ou imposer un objectif secondaire. Elle conserve un délai de réaction raisonnable et ne retire pas la seule voie d'accès d'un archétype. Le scoring récompense objectifs, esquives et efficacité. Il pénalise les dégâts reçus sans transformer les longues animations de finishers en avantage de score.

### Entraînement et apprentissage

Le tutoriel enseigne déplacement, garde, projection, anti-air, confirmation, grenade, bouclier, punition et mécanique personnelle. Chaque exercice explique une erreur concrète et permet de reprendre immédiatement. Les missions de combo acceptent la notation classique ou simplifiée et montrent les étapes déjà reconnues.

Le laboratoire permet enregistrement et lecture d'actions du mannequin, garde automatique après le premier coup, relevée aléatoire, affichage des boîtes, avance image par image, ressources réglables et état du bouclier. Une capture de situation enregistre les positions, ressources, projectiles et graine. La mise à jour d'un personnage signale les anciens exercices devenus incompatibles.

### Réseau et replays

Le réseau visé est un duel avec rollback. La simulation doit être déterministe et stocker un état sérialisable incluant les entités, temporisations, projectiles et graines. Les effets visuels et audio ne modifient pas l'état de combat. Un effet déjà confirmé ne se rejoue pas plusieurs fois après correction. Les invitations, spectateurs, salons et matchmaking sont des fonctions de production à implémenter ; leur présence dans la bible ne les rend pas disponibles dans le prototype.

Un replay contient la version des règles, les identifiants de contenu, les entrées et des empreintes d'état périodiques. Il reste marqué incompatible si les données requises manquent. Une déconnexion ne transforme pas automatiquement une partie privée en résultat classé. La pause se négocie au niveau du match et ne dépend pas seulement de la visibilité de l'onglet.

## Fatalités et présentations

### Grammaire des finishers

Chaque combattant reçoit deux finishers : un geste bref lié à sa manière de combattre et une conclusion plus spectaculaire liée à son équipement ou à la scène. La bible utilise le mot fatalité pour la catégorie demandée, mais les animations peuvent se terminer par une neutralisation, une disparition de simulation ou une destruction d'unité. Le style reste celui de Halo, avec poids, énergie, blindages et réactions lisibles.

Un finisher est disponible après la victoire définitive, dans une fenêtre proposée de 180 frames. Une commande courte ou un bouton d'accessibilité déclenche la même séquence. Il n'affecte pas le résultat, le classement ni la récompense compétitive. Si le joueur n'agit pas, une victoire standard se joue. Le perdant peut demander une présentation abrégée selon les règles du salon.

Les cibles sont réparties en familles de squelette : humain casqué, humain non casqué, Sangheili, Jiralhanae, Lekgolo et construction. Une attaque conçue pour un cou humain n'est pas réutilisée sans adaptation sur les mandibles d'un Elite ou sur une colonie Lekgolo. Les finishers d'un véhicule se déroulent sur ses points faibles, avec évacuation de l'attaquant.

Les interactions attaquant et cible utilisent une timeline commune. Elle synchronise anticipation, contact, impact, réaction, caméra, particules et retour à l'écran de résultat. Chaque personnage conserve des frames individuelles. Le masquage d'une jonction se fait par cadrage ou effet cohérent, jamais par un changement brutal de taille.

### Intros et sorties

Les présentations comprennent entrée dans l'arène, garde initiale, provocation, victoire de manche, défaite de manche, victoire finale, défaite finale et sortie. Chaque pose fixe possède une entrée et une sortie si elle fait partie d'une animation. Une animation de respiration ne remplace pas les étapes d'une attaque.

Les dialogues de rivalité sont originaux. Ils expriment la situation sans reprendre de longs dialogues des jeux. Une alternative sans voix garde les sous-titres et le rythme des plans. Les voix de production demandent enregistrement ou interprétation autorisés ; aucun fichier audio n'est déclaré livré à partir d'une simple ligne de texte.

## Direction artistique et production

### Sprites individuels

Une image contient un seul personnage ou une seule unité. Le corps, l'arme, les doigts, les pieds et les appendices doivent être entièrement dans le cadre, avec une marge utile. Le fond des sprites est réellement transparent. Une silhouette sur damier peint ou un halo opaque n'est pas validée comme détourage.

Le master de personnage vise une hauteur de travail d'environ 1 536 pixels, à ajuster selon les détails. Le pivot est placé au sol entre les appuis, les points d'attache de l'arme sont enregistrés et la zone utile conserve la même échelle entre les poses. Les nombres inscrits et les pièces asymétriques interdisent de valider automatiquement un miroir horizontal. Les deux orientations ont leurs corrections propres.

La nomenclature sépare personnage, incarnation, action, orientation et frame. Exemple : chief_infinite_idle_right_0001.png. Une séquence JSON contient la durée de chaque frame, les événements et les coordonnées d'ancrage. Les boîtes de collision sont des données, pas des pixels de couleur cachés dans l'illustration.

### Budget initial d'animation

Le budget de référence comprend attente, marche avant, marche arrière, dash avant et arrière, accroupissement, saut et chute, gardes haute et basse, impacts haut et bas, chute, relevée, projection, normals au sol et aériens, quatre spéciaux, super, grenade, provocation, entrée, victoires, défaites et deux finishers. Le registre de production détaille chaque état au lieu de compter les seules poses de sélection.

L'animation peut afficher douze dessins par seconde tout en conservant une simulation à soixante frames. Les frames d'anticipation, contact et récupération sont distinctes et leurs durées sont des multiples entiers de la simulation. Les effets de bouclier, de plasma et de poussière sont séparés des corps pour éviter de régénérer toute la silhouette à chaque variation de lumière.

Une animation n'est acceptée qu'après contrôle du pivot, de l'échelle, de la continuité du volume, de la lisibilité du contact et de la synchronisation avec les données de mouvement. Une unique illustration déplacée par translation ne devient pas une animation de marche finalisée.

### Décors parallaxe

Une arène de production comporte six couches indépendantes : ciel, structures très éloignées, relief et bâtiments intermédiaires, fond proche, sol jouable et premier plan. Leurs facteurs indicatifs sont 0,04, 0,12, 0,28, 0,55, 1 et 1,15. Ces nombres expriment une vitesse relative à la caméra et se règlent avec le cadre. Une illustration plate constitue seulement un concept maître tant que les couches indépendantes n'existent pas.

La ligne de combat est horizontale et dégagée. Les éléments de premier plan ne masquent pas les pieds ni les projectiles en classé. Une transition entre secteurs conserve la logique du match et ne crée pas de dégâts ou d'annulation non annoncés. Les hazards de campagne sont télégraphiés et désactivables en versus. Les événements lointains enrichissent la scène sans modifier les boîtes.

### Audio et interface

L'audio distingue rupture de bouclier, recharge prête, garde parfaite, projectile, attaque imblocable et danger de boss. Les options permettent de limiter la dynamique, renforcer les signaux utiles et couper séparément voix, musique, ambiance et effets. L'identité sonore définitive demande un travail de création et d'intégration distinct.

Le HUD utilise des formes et des chiffres en complément de la couleur. Il indique santé, bouclier, énergie, grenades et ressource personnelle. Contre un géant, l'objectif actuel et son point faible ont priorité sur une grande barre décorative. Les options comprennent taille du texte, contrastes, daltonisme, réduction du mouvement, suppression du tremblement, clignotements réduits et sous-titres de télégraphie.

## Architecture et critères de livraison

### Données communes

Les registres séparent fighters, moves, stages, bosses, cinematics et assets. Chaque entrée possède un identifiant stable, une version, un statut, une provenance et ses dépendances. Le moteur charge les données de règles avant les illustrations et vérifie qu'aucun identifiant requis n'est absent. Les ressources manquantes affichent un état explicite dans l'atelier, sans être comptées comme produites.

Le statut de conception indique si une fiche existe. Le statut visuel indique absent, candidat ou validé. Le statut d'animation distingue aucune séquence, séquence partielle et ensemble accepté. Le statut d'intégration indique séparément la présence dans le moteur. Une seule colonne terminé serait trompeuse, car ces quatre étapes peuvent évoluer indépendamment.

### Priorités de réalisation

La première tranche jouable vise Chief contre Elite dans une arène simple, puis un Scarab avec jambes, accès, cœur et évacuation. Cette tranche doit vérifier le plaisir du déplacement, les fenêtres de punition et la lisibilité des échelles. La tranche suivante ajoute quatre archétypes, deux arènes de production, un tournoi local et une route narrative complète. Le reste du roster vient après validation des règles communes.

Les données de la bible peuvent être importées progressivement. Le prototype joint met à l'épreuve une partie des mécaniques avec des visuels temporaires. Il ne constitue ni l'intégration des 24 combattants, ni une version réseau, ni un jeu finalisé. La création des images commence en parallèle et leur journal de contrôle conserve les erreurs observées, les corrections et les manquants.

### Conditions d'acceptation

Un duel est accepté lorsque garde, projection, annulation, changement de côté, double KO, délai de recharge et pause donnent des résultats reproductibles. Un boss est accepté lorsqu'il reste gagnable par chaque archétype, que toutes les attaques possèdent un signal préalable, que les checkpoints restaurent les bons états et qu'aucun objectif n'exige une ressource définitivement épuisée.

Une arène est acceptée lorsque les six couches fonctionnent sans trous, que la ligne de combat reste lisible dans tous les cadrages et que le profil classé désactive tous les effets de gameplay. Un personnage est accepté lorsque ses versions sont identifiées, ses mouvements disposent de phases visuelles propres et ses asymétries restent correctes dans les deux orientations.

La fidélité 1:1 est un objectif de contrôle à chaque livraison. Elle n'est pas validée collectivement parce qu'un lot a été généré. Les captures de comparaison, les références de jeu et les corrections par asset constituent la preuve attendue.

## Références générales

[S01] Halo Waypoint, Master Class. Référence officielle des incarnations du Master Chief, notamment Mark V, Mark VI GEN2 et Mark VI GEN3. https://www.halowaypoint.com/en-us/news/master-class

[S02] Halo Waypoint, Canon Fodder Foundations. Distinction entre exploration artistique et contenu effectivement prévu ou coupé. https://www.halowaypoint.com/news/canon-fodder-foundations

Les références détaillées des combattants, unités et arènes figurent dans leurs registres et dans les chapitres suivants. Les règles de combat, scénarios, paramètres numériques et structures de modes décrits ici sont des propositions de conception originales pour Halo Combats.


# Partie 2 Combattants et parcours

## Cadre et commandes

Cette annexe propose vingt quatre combattants. Les personnages et apparences proviennent de Halo; les chiffres, commandes, enchaînements et scènes sont des créations de Halo Combats. Les rencontres interépoques portent la mention simulation croisée. La fidélité un pour un reste un objectif à vérifier par des vues du jeu: aucune fiche textuelle ne certifie un sprite terminé.

La simulation tourne à 60 Hz. L, M, H désignent les frappes légère, moyenne et lourde; R l’arme; G la grenade; A l’aptitude. Les directions suivent le pavé numérique face à droite: 5 neutre, 2 bas, 6 avant, 4 arrière. Les commandes 236, 214 et 623 sont relatives à l’orientation. R+G recharge ou ventile; 22R peut doubler cette commande sans avantage supplémentaire.

Le plafond commun est trois barres d’énergie et deux grenades. Un personnage sans grenade n’en reçoit pas arbitrairement. Les valeurs se lisent démarrage, durée active, récupération; la garde négative exprime un désavantage. Pour les projectiles, l’active décrit l’émission et le trajet modifie l’avantage réel. Les projections ont sept frames de déchoppe; leur récupération est celle d’un échec. Les prises commandées se battent par saut ou déplacement.

Chaque fiche définit onze normales: les six coups du tableau et cinq entrées complémentaires 5M, 2L, j.L, j.M et j.H, détaillées dans roster.json. Les trois attaques aériennes sont overhead et exigent une garde debout; une récupération d’atterrissage précède tout spécial terrestre. Les liaisons restent à tester: xx signifie annulation et > enchaînement ou liaison. Un rebond mural, une relance et une traction maximum sont permis par combo. La réduction de dégâts et les boucliers dépendent du système central.

Le repère Spartan est 1000 santé et 200 bouclier, valeur compétitive sans prétention physique. Les humains sans Mjolnir n’obtiennent pas de bouclier fictif. Le Hunter protège frontalement avec une plaque physique. Les colosses conservent leur gabarit grâce au cadrage et à la largeur de l’arène; ils ne sont pas miniaturisés.

## Routes et exécutions

Chaque parcours prévoit huit rencontres: deux apprentissages, une faction, une épreuve de mouvement, un intermédiaire, le rival, un boss géant et le duel final. Intro de huit à douze secondes, échange rival de dix à quinze secondes, ending de trente à quarante cinq secondes. Les scènes sont passables, sous-titrées et consultables dans la galerie. Le Rookie reste silencieux.

Les deux exécutions de chaque personnage arrivent après le résultat définitif. Elles sont désactivables, ne changent pas le canon et n’apportent aucun bonus de gameplay. L’impact des armes et boucliers respecte Halo. Les costumes ne gonflent pas le roster; Buck Spartan IV réclamerait un profil distinct de Buck ODST.

## Sélection initiale


| ID | Combattant | Référence | Rôle | Santé | Bcl. |
|---|---|---|---|---:|---:|
| chief_infinite | John 117 le Major | Halo Infinite | Polyvalent à contrôle de distance | 1000 | 200 |
| arbiter_h3 | Thel 'Vadam l’Arbiter | Halo 3 | Duelliste à épée et lecture défensive | 1000 | 200 |
| johnson_h3 | Avery Johnson | Halo 3 | Vétéran de soutien à punition | 1100 | 0 |
| noble_six | Noble Six | Halo Reach | Assaut mobile et adaptation contrôlée | 1000 | 200 |
| emile_reach | Emile A239 | Halo Reach | Pression rapprochée et piège au recul | 1000 | 200 |
| jorge_reach | Jorge 052 | Halo Reach | Lourd protecteur et suppression | 1050 | 200 |
| jun_reach | Jun A266 | Halo Reach | Tireur à angles et préparation | 950 | 200 |
| kat_reach | Kat B320 | Halo Reach | Technicienne de terrain et placement | 1000 | 200 |
| carter_reach | Carter A259 | Halo Reach | Chef de ligne et contre-offensive | 1000 | 200 |
| buck_odst | Edward Buck ODST | Halo 3 ODST | Assaut humain et rechargement discipliné | 1100 | 0 |
| rookie_odst | Le Rookie | Halo 3 ODST | Reconnaissance silencieuse et punition | 1050 | 0 |
| rtas_h3 | Rtas 'Vadum | Halo 3 | Commandant Sangheili à pression méthodique | 1000 | 200 |
| tartarus_h2 | Tartarus | Halo 2 | Grappler lourd à marteau | 1100 | 180 |
| atriox_hw2 | Atriox | Halo Wars 2 | Brawler de contrôle et prises | 1100 | 150 |
| decimus_hw2 | Decimus | Halo Wars 2 | Colosse mécanisé à engagements lents | 1150 | 120 |
| escharum_infinite | Escharum | Halo Infinite | Patriarche à alternance feu et hache | 1100 | 150 |
| jega_infinite | Jega 'Rdomnai | Halo Infinite | Assassin de feintes et camouflage | 950 | 180 |
| chak_lok | Chak 'Lok | Halo Infinite | Contrôleur camouflé à portée d’épée | 1000 | 180 |
| alice_hw2 | Alice 130 | Halo Wars 2 | Suppression mobile et libération de terrain | 1050 | 200 |
| douglas_hw2 | Douglas 042 | Halo Wars 2 | Artillerie à trajectoires et salves | 1000 | 200 |
| jerome_hw2 | Jerome 092 | Halo Wars 2 | Leader de percée et laser chargé | 1000 | 200 |
| zealot_reach | Elite Zealot | Halo Reach | Assaut aérien et lames longues | 1000 | 200 |
| cethegus_h3 | Cethegus chef Brute | Halo 3 | Duelliste lourd de l’Arche | 1100 | 150 |
| hunter_h3 | Mgalekgolo Hunter | Halo 3 | Colosse à bouclier physique et canon | 1200 | 0 |


## 1 John 117 le Major


**Référence et silhouette.** Halo Infinite. GEN3 Mark VI vert olive, 117 sur le plastron, visière dorée, proportions Infinite; ne pas remplacer par Mark VII multijoueur. [R01].

**Profil.** Polyvalent à contrôle de distance; 1000 santé et 200 bouclier; poids moyen. Charge équipement 0–100; régénération hors utilisation; grappin coûte 35, mur 60. Le délai interdit de les enchaîner sans décision.


| Entrée | Coup | Démarrage actif récupération | Garde | Dégâts |
|---|---|---|---:|---:|
| 5L | Direct blindé | 6/2/11 | -2 | 40 |
| 2M | Balayage de botte | 9/3/16 | -5 | 60 |
| 5H | Crosse MA40 | 14/4/23 | -9 | 90 |
| 3H | Coude montant | 17/4/28 | -14 | 85 |
| 2H | Uppercut blindé | 10/5/25 | -12 | 80 |
| 6L+M | Désarmement de proximité | 7/1/27 | prise | 120 |


**Spéciaux.**


- **Rafale MA40 — 236R**. 12/6/20 frames; garde -8; 75 dégâts; coût 3 munitions. Trois balles; avance courte au premier tir, trois unités du chargeur. Réponse adverse: Passer au-dessus ou faire dépenser le chargeur.


- **Traction au Grappleshot — 214A**. 18/6/24 frames; garde -14; 55 dégâts; coût 35 charge. Accroche au sol ou sur adversaire; rapproche le Major, sans téléportation ni traversée de garde. Réponse adverse: Frapper le câble au départ ou garder puis punir.


- **Frappe ascendante — 623H**. 11/5/31 frames; garde -21; 100 dégâts; coût aucun. Anti-air franc; aucun blindage contre une attaque basse au sol. Réponse adverse: Rester au sol et punir la retombée.


- **Drop Wall — 22A**. 27/1/25 frames; garde sans contact; 0 dégâts; coût 60 charge. Générateur détruisible, 180 durabilité; le mur laisse passer les corps et cesse après 180 frames. Réponse adverse: Approcher à pied ou détruire le générateur.


**Super.** Brèche de Zeta, 236236H, 2 barres, départ 12 frames, garde -25, 320 dégâts. Saisie au grappin sur touche confirmée, crosse, projection et rafale finale; aucune saisie sur garde.


**Combos proposés.** 5L > 2M > 5H xx 236R / 3H > saut j.M > j.H > atterrissage > 214A xx 236236H.


**Forces et réponse adverse.** Réponses aux trois distances; défend une recharge sans supprimer les approches adverses. Recharge et gadgets partagent les fenêtres de vulnérabilité; pression courte sans ressource.


**Parcours original non canonique.** Intro: Le Major accroche une arme au sol, la vérifie puis se place entre son adversaire et une balise de secours. Rival: Atriox. Confrontation symbolique des chefs de guerre; cette rencontre mélange volontairement les versions Infinite et Wars 2. Ending: Après la dernière simulation, il récupère la balise perdue et repart chercher les survivants. Aucun anneau n’est activé et aucun événement futur officiel n’est annoncé.


**Deux exécutions.** Exécution Grappleshot puis frappe blindée, cadrage bref. / Surcharge d’une bobine à fusion déposée derrière l’adversaire.


**Variantes à produire.** Base Infinite GEN3; Mark V CE comme variante historique avec profil visuel propre; Mark VI Halo 3 comme variante historique; pas de mélange des pièces.


## 2 Thel 'Vadam l’Arbiter


**Référence et silhouette.** Halo 3. Harnois Arbiter argenté de Halo 3; mandibles, casque et pieds digitigrades exacts; épée à deux lames. [R10].

**Profil.** Duelliste à épée et lecture défensive; 1000 santé et 200 bouclier; poids moyen. Discipline 0–3; une parade réussie produit une charge; une feinte en consomme une. Aucune invisibilité gratuite héritée de Halo 2.


| Entrée | Coup | Démarrage actif récupération | Garde | Dégâts |
|---|---|---|---:|---:|
| 5L | Pommeau | 6/2/11 | -2 | 40 |
| 2M | Balayage digitigrade | 9/3/16 | -5 | 60 |
| 5H | Taille oblique | 14/4/23 | -9 | 90 |
| 3H | Lame ascendante | 17/4/28 | -14 | 85 |
| 2H | Revers au ciel | 10/5/25 | -12 | 80 |
| 6L+M | Projection au harnois | 7/1/27 | prise | 120 |


**Spéciaux.**


- **Fente énergétique — 236H**. 17/5/28 frames; garde -16; 120 dégâts; coût aucun. Fente à portée moyenne; arrête la course au contact et ne piste pas un saut. Réponse adverse: Garder debout ou esquiver avant le départ.


- **Rafale plasma — 236R**. 16/7/24 frames; garde -11; 65 dégâts; coût 20 chaleur. Deux projectiles lents; pression bouclier accrue, pas de visée automatique. Réponse adverse: Sauter la seconde salve et punir la récupération.


- **Parade de duelliste — 214A**. 5/12/25 frames; garde sans contact; 70 dégâts; coût aucun. Contre les coups médians et hauts; ouvre une riposte unique, perd contre projection et bas. Réponse adverse: Retarder le coup ou balayer.


- **Feinte du Kaidon — 22A**. 13/1/17 frames; garde sans contact; 0 dégâts; coût 1 Discipline. Retrait puis retour au neutre; annulation uniquement depuis une normale gardée. Réponse adverse: Suivre la retraite sans frapper trop tôt.


**Super.** Sentence de l’Arbiter, 236236H, 2 barres, départ 13 frames, garde -24, 325 dégâts. Fente puis trois impacts énergétiques sur confirmation; animation réduite contre les grandes silhouettes.


**Combos proposés.** 2M > 5H xx 236H / 214A réussi > 5M > 3H > j.H > atterrissage > 236236H.


**Forces et réponse adverse.** Allonge régulière et punition des attaques prévisibles. Projectile lent; parade vulnérable aux projections et aux variations de rythme.


**Parcours original non canonique.** Intro: L’Arbiter déploie son épée, observe le terrain puis baisse légèrement sa lame avant le signal. Rival: Tartarus. Rivalité de Halo 2 revisitée en simulation avec son apparence Halo 3; aucune réécriture de la chronologie. Ending: Il range l’épée devant une porte désormais ouverte. Les guerriers qui le suivent sont invités à choisir eux-mêmes leur route.


**Deux exécutions.** Fente d’épée puis retrait de lame hors gros plan. / Désarmement suivi d’une grenade plasma sur l’arme abandonnée.


**Variantes à produire.** Base Halo 3; Harnois Halo 2 Classic; Harnois Halo 2 Anniversary; modèles séparés.


## 3 Avery Johnson


**Référence et silhouette.** Halo 3. Tenue de marine et casquette de Halo 3, visage adulte caractéristique; jamais une armure de Spartan. [R10].

**Profil.** Vétéran de soutien à punition; 1100 santé et 0 bouclier; poids moyen. Discipline d’escouade 0–2; recharger proprement et punir une attaque ratée renforcent une rafale, sans invoquer de soldat.


| Entrée | Coup | Démarrage actif récupération | Garde | Dégâts |
|---|---|---|---:|---:|
| 5L | Direct du vétéran | 6/2/11 | -2 | 40 |
| 2M | Coup de genou bas | 9/3/16 | -5 | 60 |
| 5H | Crosse longue | 14/4/23 | -9 | 90 |
| 3H | Épaule montante | 17/4/28 | -14 | 85 |
| 2H | Coup de canon montant | 10/5/25 | -12 | 80 |
| 6L+M | Prise au col | 7/1/27 | prise | 120 |


**Spéciaux.**


- **Rafale BR55 — 236R**. 13/6/23 frames; garde -10; 80 dégâts; coût 3 munitions. Salve horizontale; la dernière balle repousse, utile pour sécuriser une recharge. Réponse adverse: Avancer entre les salves.


- **Tir de barrage — 214R**. 21/12/29 frames; garde -15; 95 dégâts; coût 6 munitions. Rafale oblique qui ferme un saut précis; angle fixé au déclenchement. Réponse adverse: Attendre le tir puis avancer au sol.


- **Ralliement — 22A**. 28/1/24 frames; garde sans contact; 0 dégâts; coût 1 Discipline. Convertit une charge de discipline en 90 récupération de santé récupérable; une fois par round. Réponse adverse: Mettre la pression pour empêcher l’animation.


- **Contre au fusil — 623H**. 12/5/29 frames; garde -19; 105 dégâts; coût aucun. Crosse puis tir court sur confirmation; ne donne pas d’invulnérabilité complète. Réponse adverse: Faire rater la crosse à distance.


**Super.** Tenez la ligne, 236236R, 2 barres, départ 15 frames, garde -28, 310 dégâts. Barrage de fusil suivi d’un tir de laser préparé; interruption possible avant le premier impact.


**Combos proposés.** 5L > 2M > 5H xx 236R / 623H anti-air > pas avant > 5H xx 236236R.


**Forces et réponse adverse.** Pression lisible et forte punition des imprudences. Pas de bouclier régénérant ni de mobilité de Spartan; ralliement rare.


**Parcours original non canonique.** Intro: Johnson inspecte son fusil et désigne une position à tenir; ses répliques sont écrites pour ce mode. Rival: Cethegus chef Brute. Duel entre discipline d’infanterie et défi brutal, sans inventer une rencontre historique personnelle. Ending: Le compte rendu affiche tous les alliés revenus. Johnson éteint le tableau des scores avant de rejoindre l’escouade.


**Deux exécutions.** Coup de crosse suivi d’un tir final cadré à distance. / Plaquage et grenade glissée dans l’équipement adverse.


**Variantes à produire.** Base Halo 3; Tenue Halo 2 sous validation des différences de visage et équipement.


## 4 Noble Six


**Référence et silhouette.** Halo Reach. Armure Mark V B de référence promotionnelle Reach; identité personnalisable du joueur respectée, aucun visage officiel inventé. [R04].

**Profil.** Assaut mobile et adaptation contrôlée; 1000 santé et 200 bouclier; poids moyen. Carburant jetpack 100; 30 par impulsion. Une configuration d’équipement est fixée avant le combat, sans combinaison jetpack et Armor Lock.


| Entrée | Coup | Démarrage actif récupération | Garde | Dégâts |
|---|---|---|---:|---:|
| 5L | Frappe de gant | 6/2/11 | -2 | 40 |
| 2M | Glissade basse | 9/3/16 | -5 | 60 |
| 5H | Crosse MA37 | 14/4/23 | -9 | 90 |
| 3H | Genou propulsé | 17/4/28 | -14 | 85 |
| 2H | Revers aérien | 10/5/25 | -12 | 80 |
| 6L+M | Clé de bras | 7/1/27 | prise | 120 |


**Spéciaux.**


- **Entrée MA37 — 236R**. 14/6/22 frames; garde -9; 75 dégâts; coût 3 munitions. Courte avance et rafale; conserve l’orientation au départ. Réponse adverse: Garder puis reprendre l’initiative.


- **Impulsion jetpack — 214A**. 10/1/20 frames; garde sans contact; 0 dégâts; coût 30 carburant. Déplacement oblique court; trajectoire visible, pas de garde pendant la montée. Réponse adverse: Intercepter l’angle de sortie.


- **Tir aérien — 236R en air**. 17/5/24 frames; garde -13; 85 dégâts; coût 3 munitions. Salve diagonale; une seule par saut, atterrissage vulnérable. Réponse adverse: Marcher sous le tir et punir.


- **Interception Six — 623H**. 10/5/29 frames; garde -19; 95 dégâts; coût aucun. Coude anti-air et retombée rapide. Réponse adverse: Feinter le saut puis punir au sol.


**Super.** Dernière extraction, 236236H, 2 barres, départ 12 frames, garde -27, 315 dégâts. Percée au fusil suivie d’une projection et d’un tir à courte portée; pas de frappe orbitale imaginaire.


**Combos proposés.** 5L > 2M > 3H > j.M > j.H / 5H xx 214A > j.H > 236R en air > atterrissage > 236236H.


**Forces et réponse adverse.** Angles d’approche variés et contrôle aérien limité. Dépend du carburant; sorties du jetpack lisibles et vulnérables.


**Parcours original non canonique.** Intro: Six ferme une balise de navigation, regarde une navette s’éloigner puis adopte une garde silencieuse. Rival: Elite Zealot. Adversaire de Reach adapté en duel; aucune identité arbitraire assignée au Zealot générique. Ending: La simulation s’arrête à l’instant où le dernier transport quitte l’atmosphère. Le rapport de Noble reste une archive, sans scène prétendant sauver Six dans le canon.


**Deux exécutions.** Désarmement puis courte exécution au couteau, hors détail graphique. / Jetpack pour prendre l’angle et tir final de précision.


**Variantes à produire.** Référence Reach grise; Gabarits et équipements personnalisés étiquetés joueur, silhouette de collision constante.


## 5 Emile A239


**Référence et silhouette.** Halo Reach. Casque EVA avec crâne gravé, grand couteau kukri et épaulière caractéristiques; gravure asymétrique à redessiner côté gauche. [R03].

**Profil.** Pression rapprochée et piège au recul; 1000 santé et 200 bouclier; poids moyen. Six cartouches de fusil; rechargement cartouche par cartouche interruptible. Le couteau ne consomme aucune cartouche.


| Entrée | Coup | Démarrage actif récupération | Garde | Dégâts |
|---|---|---|---:|---:|
| 5L | Coup de pommeau | 6/2/11 | -2 | 40 |
| 2M | Balayage au couteau | 9/3/16 | -5 | 60 |
| 5H | Crosse de shotgun | 14/4/23 | -9 | 90 |
| 3H | Kukri montant | 17/4/28 | -14 | 85 |
| 2H | Crosse verticale | 10/5/25 | -12 | 80 |
| 6L+M | Crochetage d’épaule | 7/1/27 | prise | 120 |


**Spéciaux.**


- **Décharge M45 — 236R**. 15/3/29 frames; garde -18; 135 dégâts; coût 1 cartouche. Maximum proche; dégâts réduits à 45 au-delà de deux largeurs. Réponse adverse: Rester hors portée puis punir.


- **Entaille de poursuite — 214H**. 18/4/25 frames; garde -12; 110 dégâts; coût aucun. Avance courte; attrape les retraits au sol mais perd face à une frappe rapide. Réponse adverse: Interrompre avant l’avancée.


- **Crosse de rejet — 623H**. 11/5/29 frames; garde -20; 95 dégâts; coût aucun. Anti-air compact; laisse l’adversaire à portée de fusil. Réponse adverse: Faire rater avec saut retardé.


- **Rechargement couvert — 22R**. 22/1/18 frames; garde sans contact; 0 dégâts; coût aucun. Une cartouche ajoutée après 22 frames; maintien pour continuer sans invulnérabilité. Réponse adverse: Approcher pendant l’animation.


**Super.** Personne ne passe, 236236H, 2 barres, départ 10 frames, garde -26, 335 dégâts. Crosse, projection puis décharge finale; première frappe de courte portée.


**Combos proposés.** 2M > 5H xx 236R / 3H > j.H > atterrissage > 214H xx 236236H.


**Forces et réponse adverse.** Très dangereux à courte portée; sanctionne les reculs systématiques. Faible portée et rechargement exposé; aucune solution gratuite au zonage.


**Parcours original non canonique.** Intro: Emile essuie une marque sur la gravure de son casque puis replace son couteau dans sa main. Rival: Elite Zealot. Écho au conflit de Reach; sa route offre un duel original sans modifier l’issue officielle de son histoire. Ending: Les armes se taisent quand la porte blindée se ferme. Un casque marqué reste éclairé dans les archives de Noble.


**Deux exécutions.** Couteau et décharge de shotgun, montage rapide. / Désarmement brutal puis impact de la crosse sur l’adversaire au sol.


**Variantes à produire.** Base Reach; Variante usée de fin de campagne; mêmes pièces d’armure.


## 6 Jorge 052


**Référence et silhouette.** Halo Reach. Silhouette massive, armure verte et rouge Reach, visière dorée et mitrailleuse dédiée; taille réelle préservée. [R03].

**Profil.** Lourd protecteur et suppression; 1050 santé et 200 bouclier; poids lourd. Chaleur de mitrailleuse 0–100; à 100, ventilation forcée 90 frames. Le joueur peut ventiler plus tôt.


| Entrée | Coup | Démarrage actif récupération | Garde | Dégâts |
|---|---|---|---:|---:|
| 5L | Direct massif | 8/3/14 | -3 | 45 |
| 2M | Botte basse | 12/4/20 | -7 | 75 |
| 5H | Crosse de mitrailleuse | 19/5/29 | -13 | 110 |
| 3H | Épaule montante | 21/5/32 | -18 | 100 |
| 2H | Balayage du canon | 13/6/30 | -16 | 95 |
| 6L+M | Projection protectrice | 9/1/31 | prise | 135 |


**Spéciaux.**


- **Suppression lourde — 236R**. 22/18/34 frames; garde -18; 125 dégâts; coût 35 chaleur. Six impacts faibles; angle horizontal, déplacement interdit pendant le tir. Réponse adverse: Sauter tôt ou attendre la chauffe.


- **Ancrage — 214A**. 16/22/28 frames; garde sans contact; 0 dégâts; coût aucun. Absorbe un coup de projectile en payant ses dégâts; aucune résistance aux projections. Réponse adverse: Approcher et projeter.


- **Canon de barrage — 623R**. 20/12/32 frames; garde -19; 110 dégâts; coût 25 chaleur. Tir oblique anti-air, direction verrouillée. Réponse adverse: Avancer sous la ligne de tir.


- **Ventilation active — 22R**. 24/1/24 frames; garde sans contact; 0 dégâts; coût aucun. Réduit la chaleur de 45 seulement si toute l’action aboutit. Réponse adverse: Punir la récupération au sol.


**Super.** Rempart de Noble, 236236R, 2 barres, départ 19 frames, garde -31, 330 dégâts. Barrage à portée moyenne puis percussion au canon; animation déclenchée seulement au premier impact.


**Combos proposés.** 5L > 2M > 5H xx 236R / 2H anti-air > 623R xx 236236R.


**Forces et réponse adverse.** Verrouille une ligne et punit les sauts prévisibles. Lent, gros volume exposé; surchauffe et prises le mettent en difficulté.


**Parcours original non canonique.** Intro: Jorge aide un civil à quitter le champ de simulation puis abaisse sa mitrailleuse vers la menace. Rival: Mgalekgolo Hunter. Contraste de masse et de protection; duel interépoques clairement étiqueté archive croisée. Ending: L’objectif évacué compte davantage que le score. Jorge laisse la mitrailleuse refroidir pendant que les derniers signaux alliés deviennent verts.


**Deux exécutions.** Percussion puis rafale à courte portée. / Projection contre un obstacle et destruction de l’arme adverse.


**Variantes à produire.** Base Reach; Casque retiré pour intro et victoire uniquement.


## 7 Jun A266


**Référence et silhouette.** Halo Reach.  [R03].

**Quatre spéciaux.** Tir stabilisé (236R, 24f, 145 dégâts); Angle haut (623R, 22f, 125 dégâts); Repli de reconnaissance (214A, 12f, 0 dégâts); Pose de visée (22A, 18f, 0 dégâts).

**Super.** Ligne dégagée (236236R, deux barres, 310 dégâts). Les onze normales, les contre-jeux, les durées complètes et les deux combos figurent dans roster.json.


**Forces et réponse adverse.** Dégâts élevés sur lecture et excellent contrôle des trajectoires. Pression proche faible; chargeur court; tous les tirs doivent annoncer leur départ.


**Parcours original non canonique.** Intro: Jun vérifie la lunette, cherche une sortie puis choisit sa ligne de tir. Rival: Jega 'Rdomnai. Reconnaissance contre camouflage; affrontement hypothétique entre spécialistes de la chasse. Ending: Il consigne la faille observée et transmet l’exercice à une nouvelle promotion. Le passage de relais est une conclusion originale de cette simulation.


**Deux exécutions.** Désarmement et tir de précision depuis une position sûre. / Interception au couteau suivie d’un tir bref.


## 8 Kat B320


**Référence et silhouette.** Halo Reach. Armure bleue Reach, bras prothétique droit et casque Air Assault; ne jamais inverser le bras par miroir automatique. [R05].

**Profil.** Technicienne de terrain et placement; 1000 santé et 200 bouclier; poids léger. Deux charges IEM de lance-grenades; capteur posé un à la fois. Les effets électroniques sont des adaptations de gameplay, pas un pouvoir de piratage à distance.


| Entrée | Coup | Démarrage actif récupération | Garde | Dégâts |
|---|---|---|---:|---:|
| 5L | Direct prothétique | 5/2/10 | -1 | 35 |
| 2M | Frappe de botte | 8/3/15 | -4 | 55 |
| 5H | Crosse tactique | 13/4/21 | -7 | 85 |
| 3H | Coude montant | 15/3/26 | -12 | 80 |
| 2H | Revers haut | 9/4/24 | -11 | 75 |
| 6L+M | Verrou de poignet | 7/1/25 | prise | 110 |


**Spéciaux.**


- **Tir de couverture — 236R**. 12/4/22 frames; garde -9; 70 dégâts; coût 2 munitions. Rafale courte qui protège la pose du capteur si confirmée. Réponse adverse: Garder puis avancer.


- **IEM au rebond — 214G**. 26/6/31 frames; garde -18; 85 dégâts; coût 1 charge IEM. Grenade de lanceur rebondissante; perte de bouclier renforcée, délai avant explosion. Réponse adverse: Changer de côté ou détruire le projectile selon l’arme.


- **Capteur de proximité — 22A**. 25/1/24 frames; garde sans contact; 0 dégâts; coût aucun. Balise de sol détruisible; révèle un camouflage dans une zone réduite, sans dégâts. Réponse adverse: Détruire la balise ou rester hors zone.


- **Interception mécanique — 623H**. 10/4/28 frames; garde -19; 90 dégâts; coût aucun. Frappe ascendante courte; aucun bonus physique illimité du bras prothétique. Réponse adverse: Attaquer avec une longue portée au sol.


**Super.** Solution de brèche, 236236G, 2 barres, départ 19 frames, garde -27, 315 dégâts. Charge IEM puis tir dans l’ouverture; le suivi n’a lieu que sur touche, aucune paralysie infinie.


**Combos proposés.** 5L > 2M > 5H xx 236R / 214G explosion > 3H > j.H > atterrissage > 236236G.


**Forces et réponse adverse.** Prépare le terrain et retire les avantages d’un camouflage. Pose lente, balise fragile, faibles dégâts sans préparation.


**Parcours original non canonique.** Intro: Kat referme un panneau de commande, vérifie son bras puis marque une zone sur le sol. Rival: Chak 'Lok. Détection et libération contre dissimulation et contrôle d’une prison, duel thématique original. Ending: Le système de portes passe en accès libre. Kat copie le journal des prisonniers et ferme la simulation avant d’en lire les noms.


**Deux exécutions.** IEM, désarmement et tir de neutralisation final. / Charge de démolition placée sur l’équipement adverse puis retrait.


**Variantes à produire.** Base Reach; Visière relevée uniquement pour scènes compatibles.


## 9 Carter A259


**Référence et silhouette.** Halo Reach.  [R03].

**Quatre spéciaux.** DMR de couverture (236R, 17f, 90 dégâts); Avancée couverte (214A, 15f, 0 dégâts); Contre de ligne (623H, 11f, 100 dégâts); Repositionnement (22A, 12f, 0 dégâts).

**Super.** Noble avance (236236H, deux barres, 320 dégâts). Les onze normales, les contre-jeux, les durées complètes et les deux combos figurent dans roster.json.


**Forces et réponse adverse.** Stabilise le combat et convertit une bonne défense en avancée. Peu de dégâts explosifs et dépend des lectures de garde.


**Parcours original non canonique.** Intro: Carter vérifie six indicateurs sur sa manche puis rejoint le centre de l’arène. Rival: Atriox. Opposition de commandement; simulation interépoques sans rencontre canonique supposée. Ending: Le bilan de l’exercice montre une extraction complète. Carter accepte le résultat, puis demande une nouvelle simulation avec moins de pertes possibles.


**Deux exécutions.** Projection puis double tir contrôlé. / Démolition d’un couvert fragilisé sur l’adversaire vaincu.


## 10 Edward Buck ODST


**Référence et silhouette.** Halo 3 ODST.  [R08].

**Quatre spéciaux.** Percée MA5C (236R, 14f, 90 dégâts); Automag de recul (214R, 15f, 75 dégâts); Interception de ruelle (623H, 12f, 95 dégâts); Recharge tactique (22R, 48f, 0 dégâts).

**Super.** Zone d’extraction (236236R, deux barres, 315 dégâts). Les onze normales, les contre-jeux, les durées complètes et les deux combos figurent dans roster.json.


**Forces et réponse adverse.** Bonne pression en mouvement et réponses simples. Pas de bouclier, pas de saut surhumain; doit gagner sa recharge.


**Parcours original non canonique.** Intro: Buck vérifie les canaux de son équipe, range sa balise puis pointe son fusil. Rival: Cethegus chef Brute. Infanterie de Mombasa contre commandement Brute; rivalité originale, pas une rencontre revendiquée. Ending: Il recompte les balises de son escouade avant de quitter les rues. Le score individuel disparaît derrière le message d’extraction.


**Deux exécutions.** Clé au bras puis automag à courte portée. / Plaquage derrière un couvert et rafale hors gros plan.


## 11 Le Rookie


**Référence et silhouette.** Halo 3 ODST.  [R06].

**Quatre spéciaux.** Rafale M7S (236R, 12f, 70 dégâts); Automag posé (214R, 18f, 90 dégâts); VISR (22A, 18f, 0 dégâts); Retrait de ruelle (214A, 11f, 0 dégâts).

**Super.** Point de rendez-vous (236236R, deux barres, 300 dégâts). Les onze normales, les contre-jeux, les durées complètes et les deux combos figurent dans roster.json.


**Forces et réponse adverse.** Dissipe les ruses visuelles et punit les gestes trop engagés. Fragile, mobilité humaine et dégâts de pression limités.


**Parcours original non canonique.** Intro: Le Rookie suit une indication lumineuse, relève son arme et ne prononce aucune réplique. Rival: Chak 'Lok. Exploration et recherche de prisonniers contre interrogateur camouflé, scénario de simulation. Ending: Il dépose l’indice retrouvé sur une table. Un canal allié s’allume; le Rookie tourne la tête puis quitte l’image.


**Deux exécutions.** Désarmement discret et tir final de l’automag. / Grenade sous un bouclier retourné, puis retrait derrière un couvert.


## 12 Rtas 'Vadum


**Référence et silhouette.** Halo 3.  [R09].

**Quatre spéciaux.** Lame de pont (236H, 16f, 115 dégâts); Double plasma (236R, 18f, 80 dégâts); Repli ordonné (214A, 14f, 0 dégâts); Revers de passerelle (623H, 12f, 105 dégâts).

**Super.** Pont sécurisé (236236H, deux barres, 325 dégâts). Les onze normales, les contre-jeux, les durées complètes et les deux combos figurent dans roster.json.


**Forces et réponse adverse.** Gère les distances et alterne les tempos. Repli payant; angles verticaux prévisibles.


**Parcours original non canonique.** Intro: Rtas ferme un canal du Shadow of Intent et mesure le silence avant d’activer son épée. Rival: Jega 'Rdomnai. Deux doctrines Sangheili, fidélité à une cause contre chasse clandestine; affrontement original. Ending: Le commandant choisit une route d’évacuation avant une cible à poursuivre. Le navire reste à sa vraie échelle dans le panorama final.


**Deux exécutions.** Riposte à l’épée et désarmement. / Projection contre une console suivie d’un tir plasma.


## 13 Tartarus


**Référence et silhouette.** Halo 2.  [R11].

**Quatre spéciaux.** Fist of Rukt (236H, 24f, 155 dégâts); Traction gravitationnelle (214A, 28f, 90 dégâts); Revers du patriarche (623H, 16f, 125 dégâts); Défi du chef (22A, 25f, 0 dégâts).

**Super.** Jugement du Rukt (236236H, deux barres, 350 dégâts). Les onze normales, les contre-jeux, les durées complètes et les deux combos figurent dans roster.json.


**Forces et réponse adverse.** Menace de projection et dégâts de lecture. Très lent et exposé après un échec; défense limitée en tournoi.


**Parcours original non canonique.** Intro: Tartarus frappe une fois le sol du manche puis inspecte l’arène comme un tribunal. Rival: Thel 'Vadam l’Arbiter. Rivalité historique de Halo 2, rejouée avec des archives d’apparences séparées. Ending: Dans cette issue alternative, son marteau reste seul devant les portes du sanctuaire. La victoire ne confirme pas ses croyances ni ne remplace l’histoire de Halo 2.


**Deux exécutions.** Projection au marteau puis impact terminal. / Traction courte et écrasement de l’équipement au sol.


## 14 Atriox


**Référence et silhouette.** Halo Wars 2. Version Wars 2, armure asymétrique et gantelet, Chainbreaker à trois têtes énergétiques; pas de fusion avec Infinite. [R12].

**Profil.** Brawler de contrôle et prises; 1100 santé et 150 bouclier; poids lourd. Ascendant 0–3 gagné en punissant; améliore la portée d’une saisie sans devenir une attraction imblocable.


| Entrée | Coup | Démarrage actif récupération | Garde | Dégâts |
|---|---|---|---:|---:|
| 5L | Poing ganté | 8/3/14 | -3 | 45 |
| 2M | Botte lourde | 12/4/20 | -7 | 75 |
| 5H | Revers de Chainbreaker | 19/5/29 | -13 | 110 |
| 3H | Gantelet montant | 21/5/32 | -18 | 100 |
| 2H | Manche vertical | 13/6/30 | -16 | 95 |
| 6L+M | Prise du gantelet | 9/1/31 | prise | 135 |


**Spéciaux.**


- **Arc de Chainbreaker — 236H**. 22/6/33 frames; garde -20; 145 dégâts; coût aucun. Balayage large qui ferme le recul au sol. Réponse adverse: Sauter tôt ou interrompre au départ.


- **Crochet de guerre — 214H**. 19/4/29 frames; garde -17; 120 dégâts; coût aucun. Ramène l’ennemi seulement sur touche; garde conserve sa position. Réponse adverse: Garder puis punir.


- **Gantelet ascendant — 623H**. 14/6/33 frames; garde -23; 115 dégâts; coût aucun. Anti-air proche avec un seul coup d’armure f8–13, dégâts subis conservés. Réponse adverse: Attaquer bas ou par deux impacts.


- **Saisie de domination — 214A**. 14/2/35 frames; garde sans contact; 160 dégâts; coût 1 Ascendant pour portée accrue facultative. Prise commandée au sol; saut et recul gagnent, échec très vulnérable. Réponse adverse: Sauter ou reculer à la lecture.


**Super.** Briseur de ligne, 236236H, 2 barres, départ 18 frames, garde -30, 350 dégâts. Impact du gantelet puis Chainbreaker; la garde du premier coup bloque toute la séquence.


**Combos proposés.** 2M > 5H xx 236H / 5H xx 214H > 5L xx 236236H.


**Forces et réponse adverse.** Impose la peur de la prise et retient la distance. Démarrages lents; se fait punir lorsqu’il cherche la prise sans préparation.


**Parcours original non canonique.** Intro: Atriox relève Chainbreaker d’un tas de débris, regarde l’arme adverse puis avance sans se presser. Rival: Jerome 092. Red Team et Atriox appartiennent au conflit de Wars 2; la revanche jouable reste une adaptation. Ending: Les unités regroupées attendent son ordre. Il choisit les ressources d’une base abandonnée, laissant la victoire individuelle hors du rapport.


**Deux exécutions.** Gantelet, désarmement et coup de Chainbreaker. / Projection de l’adversaire contre son propre équipement détruit.


**Variantes à produire.** Base Wars 2; Infinite en variante complète avec références propres et règles identiques seulement en exhibition.


## 15 Decimus


**Référence et silhouette.** Halo Wars 2.  [R13].

**Quatre spéciaux.** Salve d’exosquelette (236R, 27f, 145 dégâts); Charge de démolition (214H, 28f, 150 dégâts); Rejet supérieur (623H, 19f, 130 dégâts); Décompression (22A, 35f, 0 dégâts).

**Super.** Démantèlement (236236R, deux barres, 350 dégâts). Les onze normales, les contre-jeux, les durées complètes et les deux combos figurent dans roster.json.


**Forces et réponse adverse.** Très grande portée et capacité à tenir un passage. Grosse cible, faible vitesse; presque tous les échecs donnent une punition.


**Parcours original non canonique.** Intro: Des fixations mécaniques se verrouillent; Decimus vérifie le réacteur avant d’orienter son armement. Rival: Douglas 042. Confrontation avec Red Team sur l’Arche; duel réduit à une rencontre originale de ce mode. Ending: Un rapport de récupération défile sur le blindage. La simulation se termine sur ses ateliers, sans annuler sa mort officielle dans le récit de Wars 2.


**Deux exécutions.** Écrasement mécanique de la position adverse, cadrage éloigné. / Saisie puis tir de l’armement de l’exosquelette.


## 16 Escharum


**Référence et silhouette.** Halo Infinite. Armure et vieillissement Infinite; Diminisher of Hope, hache gravitationnelle à lame hardlight, et Scrap Cannon séparés en poses de changement d’arme. [R15].

**Profil.** Patriarche à alternance feu et hache; 1100 santé et 150 bouclier; poids lourd. Ferveur 0–100 par pression gardée; activation temporaire améliore l’avance, sans recharge de vie ni invulnérabilité. Les 150 points de bouclier sont une règle de simulation 2D, distincte de la protection de la campagne reliée à Esparza.


| Entrée | Coup | Démarrage actif récupération | Garde | Dégâts |
|---|---|---|---:|---:|
| 5L | Gantelet court | 8/3/14 | -3 | 45 |
| 2M | Botte du patriarche | 12/4/20 | -7 | 75 |
| 5H | Manche lourd | 19/5/29 | -13 | 110 |
| 3H | Hache montante | 21/5/32 | -18 | 100 |
| 2H | Revers de garde | 13/6/30 | -16 | 95 |
| 6L+M | Prise du défi | 9/1/31 | prise | 135 |


**Spéciaux.**


- **Rafale Scrap Cannon — 236R**. 24/12/34 frames; garde -22; 130 dégâts; coût 30 chaleur. Tir qui repousse; vitesse au sol nulle durant la rafale. Réponse adverse: Sauter tôt puis punir.


- **Marche du défi — 214A**. 18/18/27 frames; garde sans contact; 0 dégâts; coût 40 Ferveur. Avance résistante à un impact, pas à une prise. Réponse adverse: Projeter ou multiplier les coups.


- **Diminisher of Hope — 236H**. 25/6/35 frames; garde -23; 155 dégâts; coût aucun. Impact proche et onde courte au sol; un seul hit par cible. Réponse adverse: Sauter l’onde ou punir de loin.


- **Revers du vétéran — 623H**. 15/6/34 frames; garde -24; 115 dégâts; coût aucun. Anti-air large; avance minimale. Réponse adverse: Feinter une descente.


**Super.** Dernier défi, 236236H, 2 barres, départ 22 frames, garde -32, 345 dégâts. Assaut de hache gravitationnelle suivi d’une onde; aucune source extérieure de bouclier en tournoi.


**Combos proposés.** 2M > 5H xx 236H / 236R touche > 214A > 5H xx 236236H.


**Forces et réponse adverse.** Pression de proximité et menace constante de hache. Alternance d’armes lente; pas d’aide des machines de son combat de boss.


**Parcours original non canonique.** Intro: Escharum referme un enregistrement, pose le canon et prend sa hache. Rival: John 117 le Major. Duel central de la campagne Infinite; version tournoi sans otage servant de batterie de bouclier. Ending: L’enregistrement du duel rejoint les archives des Parias. Cette conclusion alternative ne réécrit pas son décès dans la campagne officielle.


**Deux exécutions.** Hache et projection contre un pilier de l’arène. / Renversement suivi d’une salve courte de Scrap Cannon.


**Variantes à produire.** Base Infinite; Armure de défi endommagée, mêmes composants.


## 17 Jega 'Rdomnai


**Référence et silhouette.** Halo Infinite. Sangheili cybernétique Infinite, membres prothétiques et lames rouges; préserver toutes les asymétries, aucune copie miroir. [R16].

**Profil.** Assassin de feintes et camouflage; 950 santé et 180 bouclier; poids léger. Camouflage 100; 40 par activation, maximum 90 frames. Contour, poussière et son restent perceptibles; attaque révèle immédiatement.


| Entrée | Coup | Démarrage actif récupération | Garde | Dégâts |
|---|---|---|---:|---:|
| 5L | Poing cybernétique | 5/2/10 | -1 | 35 |
| 2M | Entaille basse | 8/3/15 | -4 | 55 |
| 5H | Lame rouge | 13/4/21 | -7 | 85 |
| 3H | Crochet montant | 15/3/26 | -12 | 80 |
| 2H | Revers de lame | 9/4/24 | -11 | 75 |
| 6L+M | Prise du chasseur | 7/1/25 | prise | 110 |


**Spéciaux.**


- **Fente écarlate — 236H**. 15/5/27 frames; garde -16; 115 dégâts; coût aucun. Approche rapide droite; ne suit pas un saut. Réponse adverse: Garder puis punir.


- **Voile du chasseur — 214A**. 22/1/25 frames; garde sans contact; 0 dégâts; coût 40 camouflage. Camouflage partiel avec signaux lisibles; ne retire ni hurtbox ni verrouillage du joueur adverse. Réponse adverse: Capteur, frappe large ou écoute.


- **Crochet cybernétique — 623H**. 10/5/30 frames; garde -21; 95 dégâts; coût aucun. Anti-air rapide mais portée courte. Réponse adverse: Attaquer au sol de loin.


- **Pas de prédation — 22A**. 16/1/24 frames; garde sans contact; 0 dégâts; coût aucun. Dash court qui s’arrête avant l’adversaire; aucun côté changé automatiquement. Réponse adverse: Occuper sa destination.


**Super.** Chasse close, 236236H, 2 barres, départ 12 frames, garde -28, 325 dégâts. Lame initiale gardable puis succession de frappes; éclairage maintient la lisibilité.


**Combos proposés.** 5L > 2M > 5H xx 236H / 214A > approche visible > 3H > j.H > atterrissage > 236236H.


**Forces et réponse adverse.** Feintes de timing, menace rapide et camouflage tactique. Faible endurance et récupération des lames punissable; capteurs utiles contre lui.


**Parcours original non canonique.** Intro: Une déformation d’air devient silhouette; Jega active une lame puis l’autre en entrant dans la lumière. Rival: Rtas 'Vadum. Conflit de doctrine inventé; Jega demeure un personnage vivant après Infinite selon Edge of Dawn. Ending: Son signal disparaît après la fin de l’exercice. L’archive n’affirme ni sa mort ni un événement futur au-delà des sources officielles.


**Deux exécutions.** Double lame et extinction du camouflage au dernier impact. / Prise cybernétique suivie d’une lame courte, cadrage contrôlé.


**Variantes à produire.** Base Infinite; Dommages et poussière cohérents, sans inventer de variante canonique.


## 18 Chak 'Lok


**Référence et silhouette.** Halo Infinite.  [R14].

**Quatre spéciaux.** Estoc de la Tour (236H, 18f, 120 dégâts); Dissimulation (214A, 24f, 0 dégâts); Contre de coursive (623H, 13f, 105 dégâts); Faux départ (22A, 18f, 0 dégâts).

**Super.** Porte condamnée (236236H, deux barres, 325 dégâts). Les onze normales, les contre-jeux, les durées complètes et les deux combos figurent dans roster.json.


**Forces et réponse adverse.** Très bon contrôle d’un espace étroit. Camouflage neutralisé par capteur et départs assez lents.


**Parcours original non canonique.** Intro: Une porte de la Tour se verrouille; Chak Lok apparaît à son côté et incline sa lame. Rival: Kat B320. Capteur de terrain contre dissimulation; rivalité créée pour l’adaptation. Ending: Les portes de la simulation se referment sur une salle vide. Sa victoire hypothétique reste isolée du résultat de la campagne Infinite.


**Deux exécutions.** Frappe d’épée après désarmement. / Projection contre une porte et impact énergétique bref.


## 19 Alice 130


**Référence et silhouette.** Halo Wars 2.  [R05].

**Quatre spéciaux.** Barrage de libération (236R, 21f, 120 dégâts); Percée latérale (214H, 20f, 120 dégâts); Arc de couverture (623R, 19f, 110 dégâts); Changement de bande (22R, 62f, 0 dégâts).

**Super.** Extraction musclée (236236R, deux barres, 335 dégâts). Les onze normales, les contre-jeux, les durées complètes et les deux combos figurent dans roster.json.


**Forces et réponse adverse.** Pression plus mobile que Jorge et grande portée. Recharge longue; silhouette lourde, couverture basse faible.


**Parcours original non canonique.** Intro: Alice détache une sangle d’évacuation puis verrouille sa mitrailleuse. Rival: Atriox. Réponse aux pertes de Red Team dans Wars 2; revanche hypothétique. Ending: Le dernier prisonnier franchit le sas; Alice reprend sa position jusqu’à la fermeture complète.


**Deux exécutions.** Crosse et rafale de mitrailleuse. / Projection à travers un couvert léger puis tir final.


## 20 Douglas 042


**Référence et silhouette.** Halo Wars 2.  [R08].

**Quatre spéciaux.** Roquette directe (236R, 26f, 160 dégâts); Tir en cloche (214R, 30f, 145 dégâts); Rejet au lanceur (623H, 12f, 100 dégâts); Recharge double (22R, 72f, 0 dégâts).

**Super.** Couloir de feu (236236R, deux barres, 340 dégâts). Les onze normales, les contre-jeux, les durées complètes et les deux combos figurent dans roster.json.


**Forces et réponse adverse.** Explosions qui limitent les déplacements et forte punition. Très dépendant de ses deux tirs, danger au contact, recharge la plus longue.


**Parcours original non canonique.** Intro: Douglas introduit deux roquettes et vérifie une dernière fois sa visée. Rival: Decimus. Opposition aux forces mécanisées de Decimus sur l’Arche, scénarisée en duel original. Ending: Il coupe le dernier vecteur de renfort dans l’exercice puis rejoint Red Team. Les roquettes restantes sont comptées avant le départ.


**Deux exécutions.** Projection puis roquette dans un équipement abandonné derrière la cible. / Crosse, recul et impact explosif cadré large.


## 21 Jerome 092


**Référence et silhouette.** Halo Wars 2. Mark IV Wars 2, marquages 092; profil campagne au laser. Commander Jerome avec Hydra et Mantis reste une variante de règles future. [R08].

**Profil.** Leader de percée et laser chargé; 1000 santé et 200 bouclier; poids moyen. Charge laser 0–100 en maintien; mouvement ralenti; relâcher avant le seuil produit seulement une feinte sans tir.


| Entrée | Coup | Démarrage actif récupération | Garde | Dégâts |
|---|---|---|---:|---:|
| 5L | Direct de commandement | 6/2/11 | -2 | 40 |
| 2M | Balayage blindé | 9/3/16 | -5 | 60 |
| 5H | Crosse de laser | 14/4/23 | -9 | 90 |
| 3H | Épaule Red Team | 17/4/28 | -14 | 85 |
| 2H | Revers du canon | 10/5/25 | -12 | 80 |
| 6L+M | Désarmement Red Team | 7/1/27 | prise | 120 |


**Spéciaux.**


- **Laser Spartan — 236R maintenu**. 40/3/36 frames; garde -24; 155 dégâts; coût 100 charge. Rayon horizontal précédé d’un point de visée; interruption avant f40 annule le tir. Réponse adverse: Approcher pendant la charge ou sauter au signal.


- **Percée Red Team — 214H**. 18/6/28 frames; garde -16; 110 dégâts; coût aucun. Assaut d’épaule qui rapproche et stoppe sur garde. Réponse adverse: Garder puis punir.


- **Slam d’interception — 623H**. 14/6/33 frames; garde -23; 115 dégâts; coût aucun. Petit saut et impact proche; version duel bornée, sans atterrissage automatique sur l’ennemi. Réponse adverse: S’éloigner de la zone annoncée.


- **Feinte de charge — 22A**. 15/1/18 frames; garde sans contact; 0 dégâts; coût aucun. Visée visible sans rayon; conserve 20 charge au plus pour le prochain essai. Réponse adverse: Ne pas sauter au premier voyant.


**Super.** Brèche du Spirit, 236236R, 2 barres, départ 18 frames, garde -30, 330 dégâts. Percussion puis laser à courte portée; uniquement après touche initiale.


**Combos proposés.** 5L > 2M > 5H xx 214H / 5H xx laser chargé > 236236R.


**Forces et réponse adverse.** Choix de charge et puissant contrôle linéaire. Laser très annoncé, pas de salve rapide pour couvrir toutes les approches.


**Parcours original non canonique.** Intro: Jerome relève les données de mission puis fait pivoter son laser vers l’arène. Rival: Atriox. Chef de Red Team face au meneur des Parias; revanche inventée, pas nouvel événement canonique. Ending: Le rapport repart vers le Spirit of Fire. Red Team quitte l’écran ensemble, la mission restant plus grande que le duel.


**Deux exécutions.** Plaquage puis laser final. / Désarmement, coup blindé et destruction de la position adverse.


**Variantes à produire.** Base Wars 2; Commander Jerome réservé à profil Hydra et Mantis séparé.


## 22 Elite Zealot


**Référence et silhouette.** Halo Reach.  [R19].

**Quatre spéciaux.** Assaut de ferveur (236H, 18f, 120 dégâts); Rafale plasma (236R, 17f, 75 dégâts); Lame du ciel (623H, 12f, 110 dégâts); Extension de chasse (214A en air, 16f, 0 dégâts).

**Super.** Vœu de conquête (236236H, deux barres, 325 dégâts). Les onze normales, les contre-jeux, les durées complètes et les deux combos figurent dans roster.json.


**Forces et réponse adverse.** Bonne portée et menace aérienne distincte de l’Arbiter. Arrivées prévisibles et ressources limitées pour varier les trajectoires.


**Parcours original non canonique.** Intro: Le Zealot contrôle un sceau de mission, déploie sa lame et avance sans hésitation. Rival: Noble Six. Adversaire représentatif de Reach; la narration parle d’un Zealot sans fusionner plusieurs individus du jeu. Ending: Un symbole de mission s’allume, puis l’archive se ferme. La campagne de Reach conserve son déroulement officiel.


**Deux exécutions.** Saisie du harnois puis frappe d’épée. / Bond et percussion énergétique sur la position vaincue.


## 23 Cethegus chef Brute


**Référence et silhouette.** Halo 3.  [R17].

**Quatre spéciaux.** Marteau de l’Arche (236H, 25f, 155 dégâts); Pas du défi (214A, 18f, 0 dégâts); Arc de rejet (623H, 15f, 120 dégâts); Rupture de garde (214H, 29f, 135 dégâts).

**Super.** Duel de l’Arche (236236H, deux barres, 350 dégâts). Les onze normales, les contre-jeux, les durées complètes et les deux combos figurent dans roster.json.


**Forces et réponse adverse.** Très forte pression mentale autour du marteau. Départs les plus visibles, pas de projectile régulier.


**Parcours original non canonique.** Intro: Le chef Brute repousse les spectateurs de l’arène puis lève le marteau en défi. Rival: Avery Johnson. Duel thématique original; dans Halo 3 le duel de l’Arche l’oppose au Major, distinction conservée dans le codex. Ending: Les spectateurs cessent leurs cris lorsque l’arène se vide. Le résultat reste une variante de tournoi, pas un événement ajouté à la bataille de l’Arche.


**Deux exécutions.** Projection et impact gravitationnel final. / Désarmement au manche puis écrasement de l’arme adverse.


## 24 Mgalekgolo Hunter


**Référence et silhouette.** Halo 3. Hunter bleu Halo 3, colonie orange, dos vulnérable, bouclier massif et canon; taille conservée par cadrage élargi. [R18].

**Profil.** Colosse à bouclier physique et canon; 1200 santé et 0 bouclier; poids colosse. Plaque physique intacte et stabilité de garde 220; à zéro, la garde s’ouvre pendant 240 frames puis peut être relevée. La plaque ne repousse pas et ne se régénère pas matériellement. Elle ne couvre ni le dos ni les projections. Canon chauffe à 100.


| Entrée | Coup | Démarrage actif récupération | Garde | Dégâts |
|---|---|---|---:|---:|
| 5L | Bord de bouclier | 10/3/17 | -5 | 50 |
| 2M | Pied massif | 14/5/23 | -9 | 85 |
| 5H | Balayage de plaque | 23/6/34 | -17 | 125 |
| 3H | Levage du bouclier | 25/5/36 | -22 | 110 |
| 2H | Canon de rejet | 16/7/35 | -20 | 105 |
| 6L+M | Prise de colosse | 11/1/35 | prise | 150 |


**Spéciaux.**


- **Canon à combustible — 236R**. 32/8/39 frames; garde -27; 155 dégâts; coût 40 chaleur. Rayon ou salve selon référence Halo 3 retenue; une seule variante visuelle verrouillée avant production. Réponse adverse: Passer derrière au départ.


- **Charge de bouclier — 214H**. 28/10/40 frames; garde -28; 150 dégâts; coût aucun. Avancée frontale; peut arrêter deux projectiles en consommant la stabilité de garde, sans destruction de la plaque. Réponse adverse: Sauter derrière ou projeter.


- **Revers de carapace — 623H**. 20/7/42 frames; garde -29; 140 dégâts; coût aucun. Très large anti-air qui expose ensuite le dos. Réponse adverse: Feinter puis punir le dos.


- **Repli de colonie — 22A**. 36/1/28 frames; garde sans contact; 0 dégâts; coût aucun. Réduit la chaleur de 45; arrête de couvrir le corps pendant la ventilation. Réponse adverse: Approcher pendant l’ouverture.


**Super.** Colère de la colonie, 236236H, 2 barres, départ 26 frames, garde -36, 355 dégâts. Percussion au bouclier puis canon; pas de deuxième Hunter invoqué en duel compétitif.


**Combos proposés.** 5L > 2M > 5H xx 236R / 2H > 623H xx 236236H.


**Forces et réponse adverse.** Portée et protection frontale imposantes. Très grande cible, dos exposé, faible mobilité; se faire contourner est décisif.


**Parcours original non canonique.** Intro: Le Hunter répond à un grondement hors champ puis déploie son bouclier; le partenaire reste hors de l’aire de duel. Rival: Jorge 052. Opposition thématique des deux protecteurs lourds; les époques sont volontairement croisées. Ending: La colonie rejoint son partenaire lorsque la zone cesse de trembler. Cette scène originale ne donne aucun nom canonique au Hunter générique.


**Deux exécutions.** Percussion de bouclier puis canon à distance courte. / Charge qui projette l’adversaire dans un couvert détruit.


**Variantes à produire.** Base Halo 3; Autres modèles Halo comme variantes futures avec silhouettes et canons propres.


## Extensions de roster


**UNSC et Spartans.** Fred 104, Kelly 087, Linda 058, Locke, Vale, Tanaka, Dare, Dutch, Romeo, Mickey, Sgt Forge, Agryna, Dinh, Eklund. Rôles et armures distincts; ne pas réduire Blue Team à des couleurs.


**Covenants et alliés.** Ripa Moramee, Sesa Refumee, Ntho Sraom, Usze Taham, Let Volir, Jackal, Skirmisher, Grunt spécialisé. Les anonymes sont des classes, les personnages nommés conservent une biographie sourcée.


**Parias.** Pavium, Voridus, Colony, Yapyap, Hyperius, Tovarus, Bassus. Colony et Yapyap nécessitent de décider une unité jouable et de traiter séparément les pouvoirs RTS.


**Forerunners et Flood.** Didacte, Warden Eternal, Harbinger, chevalier prométhéen, forme de combat Flood. Les entités géantes ou volantes passent d’abord en boss; les formes Flood ne fusionnent pas artificiellement les espèces hôtes.


**Autres continuités.** Halo Legends, romans, comics, Silver Timeline et contenus coupés documentés. Étiquettes distinctes, zéro apparence supposée officielle sans référence. Silver Timeline n’écrase pas la continuité des jeux.


## Contrôles de fidélité et points à résoudre

Le gantelet d’Atriox, le bras droit de Kat, les prothèses de Jega, la mâchoire de Rtas et la gravure d’Emile nécessitent deux directions dessinées et vérifiées. Retourner le sprite horizontalement donnerait des erreurs d’anatomie ou de costume. Les armes longues sont aussi contrôlées des deux côtés, avec éjection, chargeur et dispositifs asymétriques.

L’Arbiter Halo 3 ne reçoit pas automatiquement l’aptitude de camouflage de son gameplay Halo 2. Le Grappleshot, le mur et les autres équipements d’Infinite restent liés à un profil Infinite. Les capacités de soutien RTS de Halo Wars 2 ne se matérialisent pas comme des armées illimitées dans un duel. La version campagne de Jerome au laser et Commander Jerome au Hydra et au Mantis nécessitent des fiches distinctes si le second profil est ajouté.

La documentation officielle actuelle confirme que Jega apparaît après la campagne Infinite dans Edge of Dawn. Une victoire d’arcade ne doit donc pas établir sa mort. De même, les routes de Noble, Johnson, Tartarus, Decimus et Escharum sont des exercices alternatifs, pas des corrections de leurs destins officiels. La version du Hunter, de son canon et du harnois de Decimus doit encore être verrouillée par captures du jeu avant la première validation graphique.

Le roster initial ne propose ni Cortana ni la nouvelle IA du Major comme combattante physique. Elles peuvent être narratrices et interfaces. Un corps ou une arme inventés demanderaient une étiquette de création originale. La Silver Timeline conserve ses propres apparences et événements. Les prototypes, concepts et contenus coupés éventuels portent leur statut de provenance, sans être présentés comme réalisés dans les jeux commercialisés.

## Registre de production

Le registre comprend 24 identités, 264 entrées normales incluant lanceur, anti-air, projection et trois attaques aériennes, 96 spéciaux, 24 supers, 48 propositions de combos, 24 introductions, 24 rivalités, 24 endings et 48 exécutions. Les commandes de base des combos sont définies; leurs liaisons ne sont pas revendiquées testées. Les animations, collisions, liaisons, bruitages, scènes, portraits et images individuelles restent à implémenter et à valider.

Chaque combattant réclame au minimum une référence principale, deux profils, un portrait, une pose neutre dans chaque direction, huit états de déplacement, six réactions de contact, garde haute et basse, relevées, projections, attaques et toutes les transitions. Une pose ne compte pas comme une animation. Les quatre états introduction, provocation, victoire et défaite comportent entrée, maintien et sortie. Les VFX de bouclier et de camouflage sont des couches indépendantes; la peau de base demeure identifiable sans eux.

Les tests de gameplay utiles portent sur les erreurs réelles: liaisons annoncées réalisables, infinités exclues, côté gauche fidèle, projectiles bloqués, grenades plafonnées, recharge interrompue, clones absents, colosses cadrés, supers punissables et exécutions désactivables. Une simple présence de fichiers ne valide aucune de ces propriétés.

## Sources officielles consultées

Les sources suivantes servent à identifier les personnages, les périodes, certains équipements et les références visuelles. Elles ne valident pas les chiffres de combat ou les scénarios originaux. Les jeux nommés restent les références de production visuelle; leurs captures comparatives doivent être annexées avant de certifier une fidélité complète.


- **R01** — [Customization Overview Season 5](https://www.halowaypoint.com/news/customization-overview-season-5).

- **R02** — [Equipment in Halo Infinite](https://support.halowaypoint.com/hc/en-us/articles/26608497528596-Equipment-in-Halo-Infinite).

- **R03** — [Spotlight May 19 2022](https://www.halowaypoint.com/news/spotlight-may-19-2022).

- **R04** — [Halo Reach Available Now With Halo The Master Chief Collection](https://news.xbox.com/en-us/2019/12/03/halo-reach-available-now-with-halo-the-master-chief-collection-3/).

- **R05** — [Women’s History Month 2024](https://www.halowaypoint.com/news/womens-history-month-2024).

- **R06** — [Official Cosplay Guide The Rookie](https://www.halowaypoint.com/news/official-cosplay-guide-the-rookie).

- **R07** — [Canon Fodder Feet First Into Fall](https://www.halowaypoint.com/en-us/news/canon-fodder-feet-first-into-fall).

- **R08** — [Anniversary Angle March of the Dream Teams](https://www.halowaypoint.com/news/anniversary-angle-march-of-the-dream-teams).

- **R09** — [Customization Overview Great Journey](https://www.halowaypoint.com/news/customization-overview-great-journey).

- **R10** — [Sweet Sixteenth](https://www.halowaypoint.com/news/sweet-sixteenth).

- **R11** — [Canon Fodder All About Anvil](https://www.halowaypoint.com/news/canon-fodder-all-about-anvil).

- **R12** — [Canon Fodder Encyclopedic Enlightenment](https://www.halowaypoint.com/news/canon-fodder-encyclopedic-enlightenment).

- **R13** — [Halo Wars 2 Releases Original Art Collection](https://news.xbox.com/en-us/2017/02/02/halo-wars-2-releases-original-art-collection-featuring-gabz-craig-drake-kevin-tong/).

- **R14** — [Canon Fodder Of Protocols and Prisons](https://www.halowaypoint.com/news/canon-fodder-of-protocols-and-prisons).

- **R15** — [Canon Fodder O Come All Ye Fiction](https://www.halowaypoint.com/news/canon-fodder-o-come-all-ye-fiction).

- **R16** — [Halo Edge of Dawn Out Now](https://www.halowaypoint.com/news/halo-edge-of-dawn-out-now).

- **R17** — [Canon Fodder High Value Histories](https://www.halowaypoint.com/news/canon-fodder-high-value-histories).

- **R18** — [The New Halo Encyclopedia is Out Today](https://www.halowaypoint.com/news/the-new-halo-encyclopedia-is-out-today).

- **R19** — [Halo Reach Achievements List](https://support.halowaypoint.com/hc/en-us/articles/360037081152-Halo-Reach-Achievements-List).


# Partie 3 Boss Battle et arènes

## Intention de jeu et état de production

Boss Battle transpose les grandes menaces de Halo dans un combat **latéral** où le personnage conserve ses commandes, ses déplacements et ses attaques. Le plaisir vient de la lecture des intentions, du placement, des ouvertures et de l’abattage ou du sabotage d’un adversaire qui domine le terrain. La caméra ne transforme pas la rencontre en tir à la troisième personne. Les machines gigantesques deviennent des structures que l’on traverse, tandis que les créatures de taille intermédiaire peuvent réellement partager le plan de combat.

Le présent chapitre spécifie **20 rencontres et 24 arènes**, soit **144 couches de décor à produire** avant variantes et animations. Il ne déclare aucun de ces assets terminé. Les modèles, animations, sons, collisions et scripts restent au statut prévu. Les noms et origines renvoient à Halo ; toutes les phases, durées, dégâts, dispositifs de contre-jeu et règles coopératives ci-dessous constituent une conception originale pour Halo Combats.

La fidélité demandée impose une référence de version pour chaque élément. Le Scarab de Halo 3 ne reçoit pas la silhouette de Halo 2 ; le Phantom paria d’Infinite ne réutilise pas les textures covenantes de Reach. Les caractéristiques visuelles seront confrontées à des captures du jeu retenu avant validation. Une source confirmant l’existence d’une unité ne suffit pas à certifier un sprite comme reproduction 1 à 1.

## Les trois échelles de rencontre

Les **duels lourds** accueillent Hunters, Goliath, Goblin et Warden Eternal. Le personnage et son adversaire peuvent tenir dans le même cadrage, avec une différence de taille visible. Les coups ne projettent pas arbitrairement le boss dans les airs. La pression remplit une jauge de déséquilibre ; le renversement ouvre une fenêtre adaptée au moveset choisi. Les prises classiques deviennent des actions courtes sur un bras, une articulation ou un point d’appui, avec la même commande et la même dépense de ressource.

Les **assauts de véhicules** concernent notamment Wraith, Banshee, Phantom et Phaeton. L’unité possède des modules lisibles : blindage, armes, accès et système central. Une zone intacte produit un retour d’impact distinct et aucun faux dommage sur le noyau. Un véhicule aérien dispose toujours d’une séquence atteignable depuis une plateforme, une panne forcée ou une interaction. Les combattants de mêlée ne sont jamais obligés de posséder une arme à feu pour terminer la rencontre.

Les **sièges de structures** regroupent Scarab, Lich, Kraken, Harvester et Proto Gravemind. L’écran montre une partie du corps ou de la machine à une taille crédible. Les plans éloignés suggèrent le reste. Les sections jouables s’enchaînent horizontalement ou par ascenseurs, tout en conservant un plan de collision latéral. Une vue générale sert d’introduction et de repère ; elle ne réduit pas le combattant à quelques pixels pendant une attaque exigeant de la précision.

Guardian et Gravemind forment deux cas particuliers. La condition de victoire est une extraction, un confinement ou la réalisation d’un objectif. Aucun n’est transformé en adversaire humanoïde doté d’une petite barre de vie. Le Guardian de Halo 5, la carte Guardian de Halo 3 et le Guardian supprimé de Halo 3 sont trois références distinctes. L’article officiel Digsite décrit précisément le dernier comme un ancien concept de Sentinelle, séparé du contenu sorti. [W09]

## Règles communes des affrontements

La simulation cible 60 mises à jour par seconde. Une indication de 60 frames représente donc une seconde de jeu simulée. Une chute du nombre d’images affichées ne raccourcit pas les avertissements. Les télégraphies comprennent une préparation corporelle ou mécanique, un son directionnel et un marquage discret de la zone concernée. La couleur seule ne porte jamais l’information. Les signaux rouges peuvent être remplacés par une forme pleine ; les signaux évitables par saut disposent d’une silhouette au sol.

Le réglage de départ considère un Spartan à 1 000 points de vie et 200 points de bouclier. Les autres combattants gardent les valeurs définies par leur fiche. Pour les boss à réserve de vie, la coopération à deux propose un coefficient initial de 1,7, à ajuster par essais. Ce coefficient ne s’applique ni au nombre d’actions obligatoires ni au temps de réaction. Une porte ne nécessite pas davantage d’activations simplement parce qu’un second joueur est présent. Les dégâts reçus restent identiques entre solo et coopération à difficulté égale.

Une attaque faible du boss doit pouvoir être bloquée sans transformer la garde en solution universelle. Les charges lourdes demandent une esquive ou un placement derrière un obstacle. Les avertissements identifient explicitement les attaques impossibles à parer. Les prises de personnage ne saisissent jamais un Scarab entier : la commande lance une action contextuelle uniquement lorsque la cible ou le dispositif adéquat est à portée. Le jeu affiche « articulation », « trappe » ou « relais » au lieu de promettre une projection irréalisable.

Chaque ouverture possède un plafond de dégâts par cycle. Un combo puissant peut écourter une phase, mais ne saute pas le déplacement qui enseigne la rencontre suivante. Le plafond doit rester visible dans le retour d’impact : une cible devenue invulnérable se referme et ne continue pas d’accepter des coups sans réponse. Les transitions ont une durée maximale prévue et ne réinitialisent pas les consommables à chaque animation. Une super cinématique ne déplace ni les autres joueurs ni les modules du boss.

Les routes de mêlée sont testées avec les tirs et grenades désactivés. Elles peuvent employer une grue, une passerelle, un levier, une charge posée ou un relais du décor. Ces moyens sont offerts par la rencontre, ne dépendent pas d’un objet déverrouillé ailleurs et ne consomment pas une ressource irréversible. Un grappler peut prendre plus de temps à se rapprocher, mais son ouverture récompense ce risque. Un tireur bénéficie de son allonge sans pouvoir neutraliser le boss depuis une position définitivement sûre.

Le mode Histoire sauvegarde après une phase réussie. Le checkpoint contient l’état de tous les modules, des portes, des objets, des réserves et du générateur aléatoire. La reprise réinitialise cet ensemble ; elle ne permet pas de cumuler des dommages à travers les défaites. Boss Rush reprend au début de la rencontre, avec les ressources prévues pour le run. Les morts causées par une chute de décor annoncent le danger avant de retirer la collision.

En coopération, un joueur KO peut être relevé pendant une fenêtre de huit secondes, puis revient au prochain point sûr si son partenaire termine la phase. La réanimation demande deux secondes près du corps et s’interrompt sous les dégâts. Les rôles sont temporaires : n’importe quel combattant peut maintenir un relais ou ouvrir un accès. Les attaques du boss sont émises par une autorité de simulation avec un identifiant d’événement ; les deux clients ne choisissent jamais séparément les cibles ni les plateformes qui s’effondrent. Une divergence détectée au changement de phase entraîne resynchronisation depuis le dernier état validé avant de reprendre le chrono.

## Catalogue des vingt rencontres

| Rencontre | Référence de version | Forme jouable et condition de victoire |
|---|---|---|
| Scarab Deutoros | Halo 3 | Immobiliser puis aborder et détruire le noyau |
| Locust | Halo Wars | Surcharger le projecteur et exploiter son arrêt |
| Wraith paria | Halo Infinite | Éviter le mortier puis neutraliser le char par abordage |
| Banshee paria | Halo Infinite | Survivre aux passes et créer une fenêtre de neutralisation |
| Phantom paria | Halo Infinite | Contrer les débarquements puis atteindre la soute |
| Phaeton | Halo 5 Guardians | Lire les déplacements et exposer le système central |
| Harvester | Halo 4 Spartan Ops | Infiltrer le site et arrêter le forage |
| Lich | Halo 4 | Aborder le bâtiment, saboter puis évacuer |
| Kraken | Halo 5 Guardians | Traverser les ponts et détruire le générateur |
| Warden Eternal | Halo 5 Guardians | Briser une garde et punir le noyau dorsal |
| Paire de Hunters | Halo Combat Evolved classique | Séparer le duo et atteindre les zones découvertes |
| Goliath | Halo Wars 2 pack Colony | Provoquer les coups massifs puis déséquilibrer |
| Abomination du Flood | Halo Wars 2 Awakening the Nightmare | Couper les renforts et isoler la créature |
| Proto Gravemind | Halo Wars 2 Awakening the Nightmare | Ouvrir les défenses et terminer le confinement |
| Juggernaut du Flood | Halo Fireteam Raven | Piéger les appendices et survivre aux charges |
| Sentinelle Enforcer | Halo 2 classique | Contourner les boucliers et désactiver les bras |
| Sentinelle Retriever | Halo Wars 2 | Utiliser les dispositifs du site contre la machine |
| Goblin | Halo 5 Warzone Firefight | Forcer une chute et atteindre le cockpit |
| Guardian | Halo 5 Guardians | Évacuer à travers ses impulsions sans tenter un duel |
| Présence du Gravemind | Halo 3 | Atteindre la sortie de la zone contaminée |

La présence des Goliaths dans le pack Colony est confirmée par la présentation officielle Xbox. [W06] Le Juggernaut mérite une distinction supplémentaire : supprimé pendant le développement de Halo 2, il apparaît effectivement dans Fireteam Raven. Le catalogue principal retient cette version sortie ; une éventuelle reconstruction de Halo 2 porte un marquage « archives de développement » et conserve son propre modèle. [W08]

## Scarab de Halo 3

**Identité.** La fiche visuelle verrouille le Deutoros, son châssis à quatre pattes, sa tête et le noyau accessible sur la partie arrière. L’article officiel consacré aux Scarabs différencie les versions Halo 2 et Halo 3 et mentionne le noyau occupé par les Lekgolo. [W01] Le déroulement ci-dessous est une adaptation originale et non la retranscription de valeurs du FPS.

**Phase une, approche.** Le joueur progresse sous le flanc du Scarab sur une voie de sol large. Deux pattes peuvent couper momentanément la trajectoire, mais jamais fermer simultanément les seules issues. L’appui commence par 66 frames de levée et une ombre croissante ; la collision offensive dure 12 frames, puis la patte reste stabilisée 90 frames. Frappes et prises contextuelles sur le vérin exposé remplissent une jauge locale. Deux ouvertures réussies suffisent au réglage initial pour faire plier la patte et mettre une rampe à portée. Le bouclier ne protège pas d’un écrasement annoncé comme imparable.

**Phase deux, abordage.** Une plateforme de service rejoint le pont affaissé. Le déplacement reste latéral et aucune compétence de grappling propre à un Spartan n’est obligatoire. Le boss balaie le fond de la scène ; seules les intersections signalées avec la voie jouable possèdent une collision. Le balayage comporte 96 frames de charge, 90 frames de passage et 120 frames de refroidissement. Le personnage peut éliminer une défense locale ou ouvrir un accès pendant ce repos. Les renforts sont limités à deux ennemis actifs en solo et trois en coopération.

**Phase trois, noyau et sortie.** Le blindage intérieur s’ouvre pendant trois secondes après activation de deux verrous mécaniques. Les dégâts de mêlée, les tirs et les projections contextuelles participent à la même réserve locale. À la destruction du noyau, un trajet d’extraction s’allume sur le pont, avec vingt secondes initiales et des points d’appui fixes. Le final montre l’explosion à distance lorsque le personnage est hors du volume dangereux. Il ne joue pas une fatalité humanoïde sur la machine.

**Corps et limites.** Les pattes forment quatre corps distincts, la coque un obstacle de scène et le noyau une cible locale. Les parties lointaines ne bloquent pas les joueurs. Les mouvements de la plateforme emploient la même transformation déterministe que leurs ancres ; aucune texture ne glisse indépendamment de sa collision. Le joueur conserve au moins 220 pixels de hauteur au cadrage de référence 1080p pendant la phase d’esquive, valeur de lisibilité proposée à valider.

**Solo et coopération.** En solo, un verrou reste ouvert après action et permet d’aller chercher l’autre. À deux, l’un peut distraire les défenses pendant que l’autre ouvre le passage ; aucun maintien simultané de deux boutons n’est exigé. Les checkpoints suivent l’agenouillement et l’ouverture de l’accès au noyau. En cas d’échec pendant l’extraction, la reprise commence devant le noyau encore intact, jamais dans une explosion déjà déclenchée. Les essais doivent vérifier les deux sens d’abordage, le personnage le plus lent et une victoire sans projectile.

## Wraith paria de Halo Infinite

**Identité.** La silhouette et les armes restent celles du Wraith paria d’Infinite, identifié comme véhicule de siège dans l’inventaire officiel. [W02] La rencontre oppose une masse mobile à un combattant piéton. Le char prend une largeur substantielle de l’écran ; sa silhouette ne devient pas celle d’un adversaire debout et son mortier ne se transforme pas en rayon continu.

**Phase une, comprendre la parabole.** Le Wraith garde le côté droit du terrain tandis que ses tirs dessinent des trajectoires différentes. Le canon prévient pendant 54 frames, puis le projectile possède un temps de vol visible. L’impact est annoncé par une ellipse au sol qui se stabilise au moment du départ du tir. Le projectile ne corrige plus sa destination après ce verrouillage. Les 75 frames de récupération permettent de progresser. Deux obstacles bas offrent des refuges contre les tirs de soutien, mais aucun n’annule toutes les trajectoires de mortier.

**Phase deux, empêcher la charge.** À mi-parcours, le char change d’angle et tente une percée. Une poussée de moteurs et un mouvement de coque annoncent la charge pendant 72 frames. Le trajet reste fixé avant ses 42 frames offensives. Le joueur peut franchir une marche de sécurité ou attirer le Wraith sur une butée. L’arrêt met à nu les zones de service pendant 96 frames. Les butées se réarment automatiquement après refroidissement ; manquer l’occasion ne rend pas la rencontre impossible.

**Phase trois, neutralisation.** Après deux arrêts réussis, la trappe d’abordage devient accessible. Le joueur ouvre la fixation par coups lourds ou commande d’interaction, puis réalise une action de sabotage de trois secondes interrompable par les derniers défenseurs. Il doit quitter la coque avant l’explosion locale. Cette action est présentée comme une victoire de rencontre ; elle n’ajoute pas un armement permanent au moveset. Le pilote n’est pas exposé dans une animation graphique obligatoire.

**Hitboxes et contre-jeu.** La coque comporte une zone de déplacement solide et une hitbox de contact seulement pendant la charge. Une simple proximité à l’arrêt ne tue pas. Le canon et les propulseurs sont des cibles locales avec des états visuels distincts. Le jeu empêche que le véhicule recule hors caméra en tirant sur un personnage coincé à la limite. Un grappler bénéficie d’une interaction plus rapide sur la fixation ; un tireur réduit plus tôt la résistance d’un module, sans pouvoir sauter tout le mécanisme d’abordage.

**Coopération et reprise.** Le mortier choisit une cible avec un délai de deux secondes minimum entre changements. L’indicateur de visée s’applique au sol, reste compréhensible pour les deux joueurs et ne poursuit pas soudain le partenaire en réanimation. Un joueur peut provoquer la charge et l’autre utiliser la trappe, mais les actions restent faisables seul. Le checkpoint se situe avant la phase de charge. La difficulté Légendaire combine davantage de schémas ; elle ne rend pas la trajectoire invisible et ne réduit pas le délai sous un seuil lisible.

## Paire de Hunters du Cartographe

**Identité.** Cette rencontre utilise les Hunters de Halo Combat Evolved classique. La paire du Cartographe est reconnue officiellement sous les noms Igido Nosa Hurru et Ogada Nosa Fasu. [W03] La fiche de sprites conserve les proportions, les volumes et la palette du jeu choisi ; un futur costume Anniversary doit être validé séparément. Les comportements alternés définis ici sont des règles de l’adaptation.

**Phase une, lire la relation.** Un Hunter presse au corps à corps tandis que l’autre prépare un tir depuis l’arrière. Le coup de bouclier comporte 48 frames de préparation, 10 frames actives et 72 frames de retour. Le joueur apprend à sortir de son axe et à atteindre la zone dorsale. Le tireur prépare son attaque pendant 72 frames ; la collision dure 6 frames, puis il récupère 96 frames. Un pilier permet de briser la ligne de feu. Les deux attaques ne doivent pas se synchroniser de manière à condamner les deux côtés du personnage.

**Phase deux, encerclement.** À 60 % de la réserve totale initiale, les Hunters tentent une permutation. Le passage est prévenu par un mouvement de déplacement et un échange sonore ; aucune téléportation n’inverse le sens de garde. Le joueur peut empêcher la permutation en infligeant assez de pression à un adversaire engagé, ou la laisser se produire pour attirer le nouveau tireur près du pilier. La distance entre les Hunters ouvre régulièrement un couloir d’évitement. Les attaques des deux ne se neutralisent pas automatiquement ; le décor reste l’outil de séparation principal.

**Phase trois, dernier défenseur.** Le survivant dispose d’une courte séquence plus agressive et d’une récupération plus longue après ses coups lourds. Le joueur conserve un moyen fiable d’obtenir le dos : esquive de l’attaque engagée, puis course courte dans la fenêtre. Aucun headshot obligatoire n’est demandé. Le boss ne devient pas invincible parce que le personnage a épuisé son arme. Un contre réussi peut déboucher sur une prise de bouclier contextuelle qui ouvre le flanc sans prétendre projeter tout le Hunter comme un humain.

**Volumes et position.** Chaque Hunter garde sa réserve, sa jauge de déséquilibre et son état d’animation. Le bouclier sert de surface de blocage directionnelle. La fenêtre dorsale suit un ancrage du tronc et disparaît quand la posture la recouvre. Le point faible ne clignote pas à travers le corps, pour éviter que des coups portés de face soient comptés comme dorsaux. Une attaque qui traverse visuellement le bouclier mais échoue doit produire un son de métal et un recul cohérents.

**Coopération.** Le jeu autorise la séparation naturelle du duo sans attribuer définitivement un Hunter à chaque joueur. Un arbitre de menaces empêche deux attaques imparables sur le même joueur dans un intervalle insuffisant. La caméra garde une arène unique ; elle ne s’étire pas à l’infini si les partenaires se placent aux extrémités. Le checkpoint Histoire est avant le duo entier, car reprendre contre le seul survivant effacerait l’apprentissage central. Les essais incluent deux personnages sans tirs et un abandon de partenaire en milieu de combat.

## Kraken de Halo 5 Guardians

**Identité.** Le Kraken appartient aux machines de siège de Halo 5. La source officielle confirme sa présence dans Osiris, tandis qu’une rétrospective de campagne cite son abordage et la bataille de Sunaion. [W03, W12] Le modèle exact d’Enemy Lines sert de référence visuelle. Le Kraken n’est pas traité comme un Scarab agrandi : sa structure jouable, ses ponts et son accès intérieur composent une autre rencontre.

**Phase une, atteindre le pont.** Une introduction montre le véhicule entier derrière les reliefs. La vue de jeu revient aussitôt au personnage sur une passerelle. Des éléments de terrain et des plateformes de transport offrent une route d’abordage sans pilotage imposé. Le boss prépare un balayage pendant 108 frames, tire durant 90 frames et expose un accès pendant 120 frames. Une pause plus longue suit deux attaques pour laisser rejoindre le prochain abri. Aucune collision provenant d’un tir hors écran n’est activée sans signal au bord de l’image.

**Phase deux, descendre au générateur.** Le personnage avance sur des tronçons latéraux reliés par des ascenseurs. Les mouvements verticaux sont des transitions brèves à commande conservée ; la caméra reste orthogonale à chaque tranche. Deux défenses doivent être neutralisées pour déverrouiller l’accès inférieur. Le parcours n’exige pas de double saut spécifique. Un combattant très lourd franchit les mêmes distances grâce aux plateformes. Les joueurs ne peuvent pas laisser l’un des deux enfermé dans une tranche précédente : les portes attendent le retour ou téléportent le retardataire seulement hors danger, avec indication préalable.

**Phase trois, générateur et évacuation.** Le générateur possède trois segments de protection. L’ouverture de chacun donne une fenêtre offensive, suivie d’un recul bref du champ de sécurité. Les grands dégâts accélèrent cette étape mais ne détruisent pas les trois segments d’un seul impact. Après sabotage, les sorties sont signalées et les effondrements démarrent avec 180 frames de préavis. La destruction retire d’abord les collisions des éléments déjà évacués. La zone où le joueur est engagé ne disparaît pas pendant une super qu’il a déclenchée avant le signal.

**Structure.** Le corps du Kraken est un ensemble de pièces de scène, chacune avec ancre, état et séquence de dommage. La cible globale de l’interface indique les objectifs restants plutôt qu’une quantité de vie absurde. Les vaisseaux et les canons du fond participent à l’échelle diégétique mais n’ajoutent pas des tirs imprévisibles. La visibilité des plateformes prime sur les fumées et débris décoratifs.

**Solo, coopération et reprise.** Le checkpoint suit l’abordage, puis l’accès au générateur. En coopération, un joueur peut contrôler les renforts pendant que l’autre ouvre les protections. Le changement de tranche n’est validé qu’une fois les deux états de joueur confirmés. En cas de déconnexion, l’ouverture ne reste pas dépendante d’un maintien disparu. La reprise après échec d’extraction revient avant le sabotage final avec une réserve prédéfinie. Les essais comprennent une liaison simulée avec latence, perte d’un message d’ascenseur et revanche immédiate après la destruction.

## Abomination de Awakening the Nightmare

**Identité.** L’Abomination est référencée dans Halo Wars 2 Awakening the Nightmare ; les captures de son modèle de jeu et de sa fiche Phoenix Logs doivent compléter la validation visuelle. La présentation officielle de l’extension confirme son cadre paria et le retour du Flood, mais elle ne suffit pas à valider chaque détail de la créature. [W11] Le modèle de jeu choisi ne doit pas être remplacé par une autre forme Flood proche aperçue dans une cinématique.

**Phase une, colonie mobile.** L’Abomination domine le premier tiers du terrain. Elle n’est pas soulevée par les launchers du joueur. Son balayage d’appendice se prépare durant 72 frames, possède 18 frames actives puis 108 frames de récupération. Le joueur peut sauter la section basse ou se retirer, puis atteindre la masse abaissée. Des petits ennemis sont introduits par un point unique, visible et temporairement destructible. Ils servent à enseigner l’effet du commandement local, pas à masquer la télégraphie du boss.

**Phase deux, infestation.** À 65 % de vie, deux nids latéraux commencent à produire des renforts. Le joueur peut fermer les deux vannes de confinement pour réduire la pression. Les vannes reviennent à disposition après un échec et ne demandent pas de munitions. Un appel de la créature annonce la vague au moins deux secondes avant la première apparition. Le nombre total de petits ennemis demeure limité. La contamination du sol laisse toujours une bande sèche assez large pour la projection ou le dash le plus lent du roster.

**Phase trois, isolation.** L’Abomination tente un écrasement avec 96 frames de préparation, 18 actives et 132 de récupération. Attirer son appendice sur une fermeture de porte l’immobilise pendant quatre secondes. Le personnage peut alors employer ses coups, sa super ou une prise contextuelle sur la zone exposée. L’efficacité d’une prise se traduit par de la pression et des dégâts, sans transformer le boss en marionnette suspendue. À la victoire, la créature s’effondre dans son propre volume ; elle ne vient pas recouvrir l’interface ni bloquer l’issue du joueur.

**Volumes et lisibilité.** Le corps possède une collision de déplacement simple, les appendices plusieurs volumes offensifs temporaires et la masse exposée une cible claire. Les particules de spores sont derrière la voie jouable pendant les préparations. Les membres peuvent se recouvrir visuellement, mais un même coup du joueur ne déclenche jamais plusieurs fois les dégâts sur la même entité. Les organismes supplémentaires ne poussent pas le personnage dans une attaque déjà inévitable.

**Coopération et reprise.** Deux joueurs peuvent répartir nids et boss, puis se réunir pendant l’immobilisation. La vie augmente selon le coefficient commun ; les vannes restent au nombre de deux. Le checkpoint Histoire suit la fermeture initiale des accès. Il restaure les spores, nids et limites de renforts pour éviter des états où une porte fermée laisserait apparaître des ennemis à l’intérieur. Les essais incluent un personnage de faible mobilité, une victoire sans tirs et une lisibilité correcte avec les effets de gore réduits.

## Proto Gravemind de Awakening the Nightmare

**Identité.** La référence de production est la rencontre Manifestation de Halo Wars 2 Awakening the Nightmare. Il faut préparer des vues d’ensemble, des détails de biomasse et des repères du terrain à partir du jeu avant validation graphique. La proposition conserve le principe d’un organisme démesuré qui requiert l’exploitation du champ de bataille. Elle n’attribue pas au personnage la capacité de détruire cette masse à mains nues.

**Phase une, ouvrir le réseau.** Le Proto Gravemind occupe l’arrière-plan et déborde hors cadre. La voie latérale longe des installations partiellement envahies. Le joueur ouvre un relais en éliminant les organismes qui obstruent son mécanisme, puis rétablit une source d’énergie. Une poussée de biomasse se prépare pendant 120 frames, agit pendant 42 frames et laisse une récupération de 180 frames. Les appendices qui traversent la lane possèdent des collisions locales ; le volume immense de fond n’en possède aucune.

**Phase deux, rompre les verrous.** Trois organes protégés deviennent des objectifs successifs. Chaque ouverture demande un dispositif du site, puis une courte phase de combat local. Le joueur déplace une cellule, libère une commande ou maintient un faisceau de défense en position. Le grappler peut utiliser toutes ces actions avec son bouton d’interaction. Une attaque lourde détruit un verrou physique accessible ; elle ne soustrait pas arbitrairement des milliards de points de vie au corps global. Les impacts de soutien touchent le monstre dans le fond, avec un retour visuel synchronisé à l’objectif validé.

**Phase trois, confinement final.** Le dernier relais lance une séquence de soutien. Le personnage protège la commande contre deux vagues courtes, puis rejoint une position sûre. Le compte à rebours indique une action concrète, avec progression visible du dispositif. Il n’exige pas de courir à l’aveugle vers un point hors écran. Si la commande tombe temporairement en panne, un levier de secours réactive le cycle ; la défaite n’est prononcée que si le personnage meurt ou si l’objectif affiché est réellement perdu.

**Interface et échelle.** Trois icônes d’organes et une jauge de confinement remplacent la barre de vie habituelle. Le panoramique de fond répond aux phases, mais l’échelle du personnage reste constante sur chaque tronçon. Les tentacules éloignés suivent un calendrier visuel différent des attaques réelles ; le code ne confond pas décor et menace. La caméra peut montrer la dimension totale pendant les transitions sûres, puis revient au cadrage de lecture avant toute reprise des contrôles.

**Coopération et reprise.** Les deux joueurs peuvent partager la protection d’un relais et l’ouverture d’un organe, puis échanger leurs rôles. En solo, les tâches simultanées deviennent une séquence, sans compagnon requis. Les checkpoints suivent chaque verrou réussi ; ils mémorisent également les objets disponibles pour éviter une cellule déjà consommée avec un relais redevenu fermé. Si un client se désynchronise, l’organisme de fond ne détermine jamais l’état de victoire : seul le registre des trois objectifs validés fait foi. Le test de validation impose un run complet sans projectile de personnage et une reprise après chaque étape.

## Règles de composition des arènes

Chaque arène comporte six couches : ciel, lointain, fond, plan intermédiaire, plan jouable et premier plan. Leurs coefficients horizontaux proposés sont respectivement **0,04 ; 0,12 ; 0,28 ; 0,55 ; 1,00 ; 1,15**. Ce sont des paramètres de composition à régler, pas des mesures reprises des jeux Halo. Le plan de collision se trouve uniquement dans la cinquième couche. Les silhouettes et les volumes qui dépassent des couches décoratives ne créent aucune collision cachée.

Le canevas de travail mesure 3 840 × 2 160 pixels. La ligne des pieds se situe à 1 680 pixels ; le moteur conserve ce repère par ancrage plutôt que par recadrages manuels. Les positions de départ sont proposées à 35 % et 65 % de la largeur, avec limites à 8 % et 92 %. Le fond prévoit du débordement horizontal pour les mouvements de caméra. Le premier plan ne traverse ni les pieds ni les attaques basses ; il s’efface lorsqu’une séquence cinématique l’exige.

La version classée d’une arène conserve une surface stable et des limites identiques pour les deux joueurs. Les transitions changent la lumière, la météo, la population du fond ou l’état visuel d’un bâtiment. Elles n’ajoutent ni tir réel ni perte de plateforme. Les dangers sont des variantes facultatives pour parties personnalisées, Histoire et défis. Chaque danger possède un signal d’au moins 90 frames au réglage initial, une fréquence minimale et un contrôle empêchant qu’il se combine à une transition illisible.

Les collisions ne sont jamais déduites automatiquement d’une image générée. Un masque jouable séparé décrit le sol et les limites. Les sprites des personnages sont contrôlés sur chaque stage avec fond clair, sombre, feu et fumée. Le filtre de visibilité peut réduire les contrastes du décor, la pluie et les particules sans modifier les timings. La palette du personnage conserve ses couleurs de faction, tandis qu’un contour discret optionnel évite qu’une armure verte disparaisse dans une forêt.

## Catalogue des vingt quatre arènes

**1. Hangar du Pillar of Autumn — Halo Combat Evolved classique.** La baie extérieure révèle l’orbite, puis les silhouettes de vaisseaux et la coque ; passerelles et monte-charges encadrent le plan métallique. Les alarmes et les départs de personnel animent le fond. Le danger facultatif est une décompression localisée. Les cadres du premier plan ne couvrent pas les déplacements accroupis.

**2. Blood Gulch — Halo Combat Evolved classique.** Ciel d’anneau, falaises, canyon, bases rouge et bleue, terre de la vallée et rochers proches composent les six plans. Un convoi lointain donne de la vie. Une variante personnalisée permet un passage de véhicule annoncé. La base reste le modèle bas de CE, pour éviter de transformer le lieu en Valhalla.

**3. Plage du Cartographe silencieux — Halo Combat Evolved classique.** L’arc de Halo et la côte encadrent la falaise, la porte forerunner, la plage et les végétaux latéraux. Un Pelican peut traverser le fond. Le ressac constitue une option de danger limitée aux bordures. La coupe latérale de la plage est une adaptation jouable ; elle ne prétend pas reproduire tout le niveau FPS.

**4. Vallée de la salle de contrôle — Halo Combat Evolved classique.** Pics, crêtes, pont, neige tassée et congères établissent la profondeur sous un ciel pâle. Une chute de neige facultative est signalée sur une corniche. En classé, seules la brume et les patrouilles éloignées évoluent. Les angles de l’architecture et la palette correspondent au rendu classique choisi.

**5. Station Le Caire — Halo 2 classique.** La Terre et les plateformes orbitales restent derrière la baie. La superstructure mène aux parois, puis à la coursive et aux rails proches. La bataille spatiale produit de la lumière sans déplacer les hitboxes. Une version Histoire peut déclencher des secousses annoncées, avec option de réduction visuelle du tremblement.

**6. Pont de New Mombasa — Halo 2 classique.** Skyline, tours, chaussées voisines et route du duel organisent un combat urbain dégagé. Le Scarab visible en arrière-plan est le Protos de Halo 2. Les débris de chaussée appartiennent à la variante avec dangers. Les barrières du premier plan sont découpées pour laisser lire les pieds et les glissades.

**7. Ruines de Delta Halo — Halo 2 classique.** Anneau, montagnes, monuments, colonnes, dalles et frondes créent une profondeur calme. Le passage d’une gondole reste décoratif en classé. La lumière évolue au fil des rounds, sans rendre une garde invisible. La végétation et les ruines ne se confondent pas avec le Cartographe de CE.

**8. Grand hall de Grande Bonté — Halo 2 classique.** La voûte de la cité, les flèches, les volumes covenants, les arcades, le sol cérémoniel et les ornements forment une arène intacte. Les portes énergétiques deviennent un danger facultatif. Aucun organe Flood ne figure dans cette version : l’infection possède sa propre arène.

**9. Lockout — Halo 2 classique.** Le ciel neigeux et l’abîme s’étagent derrière les roches, les tours et la plateforme. Le givre reste un premier plan périphérique. Le parcours vertical original est transformé en surface latérale explicitement assumée. Une variante hors classé emploie un jet glacé ; le duel compétitif conserve un sol plat.

**10. Valhalla — Halo 3.** Le ciel de l’Arche ne présente aucun arc de Halo. Montagnes, chute, rivière et tours identifient le lieu. Le sol de berge est nivelé pour les règles du duel. Les man-cannons peuvent animer les côtés ; leur effet physique n’existe que dans les variantes prévues. Herbes et rochers proches n’empiètent pas sur la zone utile.

**11. Cartographe de l’Arche — Halo 3.** Le ciel de l’Arche, le désert et les escarpements donnent de l’ampleur à la façade forerunner. Le joueur se bat sur une terrasse minérale, pas sur une miniature du bâtiment. Les machines lointaines évoluent hors collision. Aucun anneau de CE n’est ajouté pour remplir le ciel.

**12. Citadelle de l’Alliance — Halo 3.** Ciel, montagnes enneigées et tours de barrière encadrent la citadelle. Le plan de combat occupe une terrasse stable. Les rayons du fond changent d’intensité entre les rounds ; une onde de pylône peut exister dans la version aventure. Les structures proches préservent la visibilité des armes longues.

**13. Grande Bonté infectée — Halo 3.** La voûte, les réservoirs et les parois sont contaminés, tandis qu’une passerelle sèche garantit la lecture. Les filaments proches restent périphériques. Les pulsations ne modifient pas les distances. Les poches contaminées sont réservées aux dangers facultatifs. L’arène doit être reconstruite, pas obtenue par une simple recoloration du hall de Halo 2.

**14. Guardian la forêt — Halo 3.** Canopée, arbres massifs, structures suspendues et plateforme centrale évoquent la carte multijoueur. Le feuillage du premier plan s’écarte du centre. Un ascenseur secondaire anime le décor. Le nom de la carte ne justifie pas l’ajout d’un Guardian géant de Halo 5.

**15. Rues de Mombasa — Halo 3 ODST.** Skyline nocturne, écrans, façades, chaussée humide et obstacles proches donnent une scène urbaine lisible. Pluie et affichages du Surintendant rythment le fond. Le contraste des armures doit être vérifié. Une variante peut intégrer un projecteur signalé sans empêcher la lecture des silhouettes.

**16. Toit du NMPD — Halo 3 ODST.** Les gratte-ciels et les toits bas encadrent un héliport, une toiture stable et des antennes périphériques. Les Phantoms restent au fond en compétition. Leurs salves deviennent un danger seulement dans la version prévue. La surface ne rétrécit pas au fil des rounds classés.

**17. Toit de Nouvelle Alexandrie — Halo Reach.** Les tours abîmées et les lueurs du siège dominent une façade béton. La plateforme garde des repères clairs pour les esquives. Des débris annoncés peuvent servir aux défis. La palette, les équipements et les volumes relèvent de Reach, sans motifs d’armure ou végétation empruntés à Infinite.

**18. Cour de Sword Base — Halo Reach.** Montagnes, falaises, façade, cour et palissades composent une base militaire. Une porte de sécurité peut fermer une portion de décor, sans changer les limites classées. Les véhicules au fond ne traversent pas la lane. La signalétique est produite séparément pour garantir des inscriptions nettes.

**19. Boneyard — Halo Reach.** Le chantier et la coque de frégate restent gigantesques derrière le duel. Grues et câbles encadrent le sol d’atelier. La variante avec dangers signale les chutes de matériel. L’échelle navale se lit grâce aux éléments de service ; le vaisseau n’est pas réduit pour entrer entièrement à l’écran.

**20. Antichambre de Requiem — Halo 4.** Ciel artificiel, montagnes et architecture suspendue précèdent une plateforme d’alliage. Les plaques proches servent à la profondeur. Les mouvements lointains sont décoratifs en classé. Les portails offensifs appartiennent aux variantes prévues. La géométrie Halo 4 ne remplace pas celle des sites Halo 3.

**21. Passerelle de Sunaion — Halo 5 Guardians.** Le ciel de Sanghelios et l’océan supportent les flèches et plateformes de la ville. Le duel prend place sur une large passerelle. Le Guardian demeure monumental et éloigné. Ses effets physiques apparaissent uniquement dans l’événement d’évacuation ou les variantes spécifiées.

**22. Avant poste de l’Arche — Halo Wars 2.** Reliefs, végétation et fortifications donnent une scène de guerre où les matériaux UNSC, parias et forerunners restent distincts. L’artillerie se manifeste au loin en classé. Une option aventure transforme un impact balisé en danger. Les barrières proches ne cachent pas les adversaires de petite taille.

**23. Plateau fracturé de Zeta Halo — Halo Infinite.** La courbure brisée, les fragments suspendus et les colonnes hexagonales définissent le panorama. Pins et équipements entourent une terrasse rocheuse stable. Nuages et fragments évoluent derrière le combat. La rupture d’une bordure n’existe que hors classé. Un anneau intact ne doit pas remplacer la cassure caractéristique.

**24. Maison du Jugement — Halo Infinite.** La voûte, la charpente paria et les projecteurs cadrent un champ de bataille d’entraînement. Les barrières sont pensées pour la lecture des distances. Les signaux de surveillance changent entre les rounds. Le lieu sert aussi de cadre naturel aux défis ; l’article officiel rappelle sa fonction d’arène imposée aux prisonniers de l’UNSC. [W04]

## Production des ressources et critères de réception

Le lot initial de chaque boss comprend une silhouette de référence, une pose neutre, les préparations, impacts et récupérations de ses attaques, les états de dégâts, les points faibles et les effets séparés. La machine entière et chaque module articulé ont leurs fichiers distincts. Une image de référence du Scarab ne vaut pas un boss animé ; une animation du noyau ne valide pas les pattes. Le manifeste suit ces états séparément pour montrer exactement ce qui manque.

Pour chaque stage, les six couches sont produites séparément avec le même horizon, les mêmes marges et la même ligne de sol. Un fond aplati peut servir de concept de composition, mais ne reçoit pas le statut « parallaxe livrée ». La jonction des bords, les transparences et les zones découvertes par le déplacement de caméra sont contrôlées avant export. La version sans dangers partage les images compatibles, mais conserve sa propre configuration de collision et de chronologie.

Une rencontre est recevable lorsque son objectif est compris sans lecture préalable, qu’un personnage de mêlée peut la terminer, que chaque attaque a un contre identifiable, que le dernier checkpoint redémarre sans état incohérent et que l’échelle reste convaincante. Les tests ne cherchent pas seulement une victoire avec Chief : ils utilisent le plus lent, le plus petit et un profil de projection. Une phase qui impose une compétence particulière doit fournir un moyen de décor équivalent.

La priorité de fabrication recommandée est Scarab, Wraith et Hunters pour valider les trois formes de lecture, puis Abomination pour la pression des renforts, Kraken pour les scènes reliées et Proto Gravemind pour les objectifs monumentaux. Les autres rencontres réemploient les outils ainsi validés sans copier leurs attaques. La production visuelle commence par une référence individuelle de chaque silhouette ; les animations viennent après validation des proportions et de la version.

## Références et limites de vérification

Les identifiants W01 à W12 correspondent aux titres et liens complets de `sources.json`. Les sources web vérifiées confirment les identités et les distinctions mentionnées dans les passages cités. Les plans de niveaux, palettes exactes et angles latéraux exigent encore les captures de référence prévues. Une mention d’unité dans un article ne vaut pas contrôle du modèle complet.

Les fiches Locust, Retriever, Goblin et Présence du Gravemind conservent des références primaires de jeu à compléter visuellement. Les formes Abomination et Proto Gravemind doivent être comparées au jeu et aux Phoenix Logs, et non validées à partir de la seule page commerciale de l’extension. Cette distinction figure dans les JSON afin que les futurs lots ne transforment pas automatiquement « référencé » en « produit » ou « conforme 1 à 1 ».

- **W01** — Halo Waypoint, [Canon Fodder If They Want Lore We Will Give Em Lore](https://www.halowaypoint.com/news/canon-fodder-give-em-lore).
- **W02** — Halo Support, [Halo Infinite Weapon Equipment and Vehicle Inventory](https://support.halowaypoint.com/hc/en-us/articles/6882880281364-Halo-Infinite-Weapon-Equipment-and-Vehicle-Inventory).
- **W03** — Halo Waypoint, [Canon Fodder High Value Histories](https://www.halowaypoint.com/news/canon-fodder-high-value-histories).
- **W04** — Halo Waypoint, [Canon Fodder Fiction Festivities](https://www.halowaypoint.com/news/canon-fodder-fiction-festivities).
- **W05** — Xbox Wire, [First Look at Warzone Firefight in Halo 5 Guardians](https://news.xbox.com/en-us/2016/03/20/first-look-at-warzone-firefight-in-halo-5-guardians/).
- **W06** — Xbox Store, [Pack de chef Colony](https://www.xbox.com/fr-fr/games/store/pack-de-chef-colony/bw74dckrsq4r).
- **W07** — Halo Waypoint, [The Nightmare Has Awoken](https://www.halowaypoint.com/en-us/news/the-nightmare-has-awoken).
- **W08** — Halo Waypoint, [That Is So Raven](https://www.halowaypoint.com/news/thats-so-raven).
- **W09** — Halo Waypoint, [Digsite Discoveries](https://www.halowaypoint.com/news/digsite-discoveries).
- **W10** — Halo Waypoint, [Digsite Deep Dive](https://www.halowaypoint.com/news/digsite-deep-dive).
- **W11** — Xbox Store, [Halo Wars 2 Awakening the Nightmare](https://www.xbox.com/en-US/games/store/halo-wars-2-awakening-the-nightmare/9NBLGGH4TQDD).
- **W12** — Halo Waypoint, [Anniversary Angle Memorable Campaign Moments](https://www.halowaypoint.com/news/anniversary-angle-memorable-campaign-moments).
