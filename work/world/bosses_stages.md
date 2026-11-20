# Boss Battle et arènes de Halo Combats

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
