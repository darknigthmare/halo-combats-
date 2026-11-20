# Halo Combats

## Bible de conception du mode de combat 2D

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
