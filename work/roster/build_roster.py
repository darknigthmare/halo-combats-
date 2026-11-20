from pathlib import Path
import json
import re

ROOT=Path(__file__).parent
SOURCES={
 'infinite_armor':{'title':'Customization Overview Season 5','url':'https://www.halowaypoint.com/news/customization-overview-season-5','ref':'turn460148904search0','supports':'Armure GEN3 Mark VI du Major dans Halo Infinite; différences avec les kits multijoueur.'},
 'equipment':{'title':'Equipment in Halo Infinite','url':'https://support.halowaypoint.com/hc/en-us/articles/26608497528596-Equipment-in-Halo-Infinite','ref':'turn460148904search2','supports':'Fonctions du Grappleshot et du Drop Wall; distinction campagne et multijoueur.'},
 'noble':{'title':'Spotlight May 19 2022','url':'https://www.halowaypoint.com/news/spotlight-may-19-2022','ref':'turn291509373search14','supports':'Noms et indicatifs des membres de Noble Team. Les illustrations communautaires ne remplacent pas des captures du jeu pour valider les armures.'},
 'reach':{'title':'Halo Reach Available Now With Halo The Master Chief Collection','url':'https://news.xbox.com/en-us/2019/12/03/halo-reach-available-now-with-halo-the-master-chief-collection-3/','ref':'turn664862621search27','supports':'Noble Team et cadre de Halo Reach.'},
 'women':{'title':'Women’s History Month 2024','url':'https://www.halowaypoint.com/news/womens-history-month-2024','ref':'turn671005482view1','supports':'Identité et spécialités de Kat et Alice; les règles de combat proposées restent originales.'},
 'rookie':{'title':'Official Cosplay Guide The Rookie','url':'https://www.halowaypoint.com/news/official-cosplay-guide-the-rookie','ref':'turn671005482view2','supports':'Références officielles détaillées de l’armure du Rookie de Halo 3 ODST.'},
 'odst_weapons':{'title':'Canon Fodder Feet First Into Fall','url':'https://www.halowaypoint.com/en-us/news/canon-fodder-feet-first-into-fall','ref':'turn460148904search9','supports':'Identité visuelle Rookie et armes M7S, M6C SOCOM, MA5C et M90A; Devoted Sentries de Reach.'},
 'teams':{'title':'Anniversary Angle March of the Dream Teams','url':'https://www.halowaypoint.com/news/anniversary-angle-march-of-the-dream-teams','ref':'turn671005482view0','supports':'Red Team composée de Jerome, Alice, Douglas; Alpha Nine issue des ODST.'},
 'rtas':{'title':'Customization Overview Great Journey','url':'https://www.halowaypoint.com/news/customization-overview-great-journey','ref':'turn671005482view3','supports':'Identité, histoire et rôle de Rtas Vadum; comparaison Mark VI Halo 2.'},
 'h3':{'title':'Sweet Sixteenth','url':'https://www.halowaypoint.com/news/sweet-sixteenth','ref':'turn664862621search13','supports':'Major, Arbiter Thel Vadam et Avery Johnson dans Halo 3.'},
 'tartarus':{'title':'Canon Fodder All About Anvil','url':'https://www.halowaypoint.com/news/canon-fodder-all-about-anvil','ref':'turn460148904search5','supports':'Fist of Rukt de Tartarus et introduction du marteau gravitationnel.'},
 'atriox':{'title':'Canon Fodder Encyclopedic Enlightenment','url':'https://www.halowaypoint.com/news/canon-fodder-encyclopedic-enlightenment','ref':'turn291509373search0','supports':'Atriox, Red Team et Chainbreaker; comparaison des apparitions Wars 2 et Infinite.'},
 'decimus':{'title':'Halo Wars 2 Releases Original Art Collection','url':'https://news.xbox.com/en-us/2017/02/02/halo-wars-2-releases-original-art-collection-featuring-gabz-craig-drake-kevin-tong/','ref':'turn291509373search18','supports':'Illustration officielle de Decimus et appartenance aux Parias.'},
 'banished':{'title':'Canon Fodder Of Protocols and Prisons','url':'https://www.halowaypoint.com/news/canon-fodder-of-protocols-and-prisons','ref':'turn291509373search16','supports':'Chak Lok, Escharum, Tour et House of Reckoning.'},
 'escharum_axe':{'title':'Canon Fodder O Come All Ye Fiction','url':'https://www.halowaypoint.com/news/canon-fodder-o-come-all-ye-fiction','ref':'turn909270892view0','supports':'Diminisher of Hope est la hache gravitationnelle personnelle d’Escharum.'},
 'jega':{'title':'Halo Edge of Dawn Out Now','url':'https://www.halowaypoint.com/news/halo-edge-of-dawn-out-now','ref':'turn671005482view4','supports':'Jega Rdomnai demeure présent après la campagne Infinite; son sort ne doit pas être inventé.'},
 'chieftain':{'title':'Canon Fodder High Value Histories','url':'https://www.halowaypoint.com/news/canon-fodder-high-value-histories','ref':'turn664862621search24','supports':'Cethegus est le chef Brute du duel dans la mission The Ark de Halo 3.'},
 'hunter':{'title':'The New Halo Encyclopedia is Out Today','url':'https://www.halowaypoint.com/news/the-new-halo-encyclopedia-is-out-today','ref':'turn664862621search5','supports':'Nomenclature Mgalekgolo et classification Lekgolo; validation visuelle Halo 3 encore requise.'},
 'zealot':{'title':'Halo Reach Achievements List','url':'https://support.halowaypoint.com/hc/en-us/articles/360037081152-Halo-Reach-Achievements-List','ref':'turn664862621search2','supports':'Présence d’un Elite Zealot dans Tip of the Spear; modèle à relever dans Reach.'}
}

F=[]
def special(name,cmd,startup,active,recovery,block,damage,effect,counter,cost='aucun'):
    return dict(name=name,input=cmd,startup_frames=startup,active_frames=active,recovery_frames=recovery,on_block=block,damage=damage,effect=effect,counterplay=counter,cost=cost)

def add(id,name,era,source,archetype,hp,shield,weight,resource,visual,normals,specials,super_,combos,strength,weakness,intro,rival,ending,finishers,costumes,weapon,grenades=2):
    profiles={
      'léger':[(5,2,10,-1,35),(8,3,15,-4,55),(13,4,21,-7,85),(15,3,26,-12,80),(9,4,24,-11,75),(7,1,25,0,110)],
      'moyen':[(6,2,11,-2,40),(9,3,16,-5,60),(14,4,23,-9,90),(17,4,28,-14,85),(10,5,25,-12,80),(7,1,27,0,120)],
      'lourd':[(8,3,14,-3,45),(12,4,20,-7,75),(19,5,29,-13,110),(21,5,32,-18,100),(13,6,30,-16,95),(9,1,31,0,135)],
      'colosse':[(10,3,17,-5,50),(14,5,23,-9,85),(23,6,34,-17,125),(25,5,36,-22,110),(16,7,35,-20,105),(11,1,35,0,150)]}
    tags=['5L','2M','5H','3H','2H','6L+M']
    properties=['haut; annulable M ou H','bas; annulable en spécial sur contact','médian; annulable en spécial sur touche','lanceur; une relance aérienne maximum','anti-air; invulnérabilité aux seuls coups aériens de f4 à la première active','projection au sol; déchoppable sur 7 frames; récupération indiquée si ratée']
    n=[]
    for i,(title,stats) in enumerate(zip(normals,profiles[weight])):
      n.append(dict(name=title,input=tags[i],startup_frames=stats[0],active_frames=stats[1],recovery_frames=stats[2],on_block=None if i==5 else stats[3],damage=stats[4],properties=properties[i]))
    src=SOURCES[source]
    F.append(dict(id=id,name=name,era=era,source_title=src['title'],source_url=src['url'],source_id=source,archetype=archetype,health=hp,shield=shield,weight=weight,unique_resource=resource,visual_lock=visual,normals=n,specials=specials,super=super_,combos=combos,strength=strength,weakness=weakness,intro=intro,rival=rival,ending=ending,finishers=finishers,costumes=costumes,weapon=weapon,grenade_capacity=grenades,status={'design':'proposed','visual_reference':'requires_frame_by_frame_validation','sprite':'not_generated_here','animation':'not_generated','gameplay':'not_implemented'},narrative_status='adaptation originale non canonique'))

add('chief_infinite','John 117 le Major','Halo Infinite','infinite_armor','Polyvalent à contrôle de distance',1000,200,'moyen',
 'Charge équipement 0–100; régénération hors utilisation; grappin coûte 35, mur 60. Le délai interdit de les enchaîner sans décision.',
 'GEN3 Mark VI vert olive, 117 sur le plastron, visière dorée, proportions Infinite; ne pas remplacer par Mark VII multijoueur.',
 ['Direct blindé','Balayage de botte','Crosse MA40','Coude montant','Uppercut blindé','Désarmement de proximité'],[
 special('Rafale MA40','236R',12,6,20,-8,75,'Trois balles; avance courte au premier tir, trois unités du chargeur.','Passer au-dessus ou faire dépenser le chargeur.','3 munitions'),
 special('Traction au Grappleshot','214A',18,6,24,-14,55,'Accroche au sol ou sur adversaire; rapproche le Major, sans téléportation ni traversée de garde.','Frapper le câble au départ ou garder puis punir.','35 charge'),
 special('Frappe ascendante','623H',11,5,31,-21,100,'Anti-air franc; aucun blindage contre une attaque basse au sol.','Rester au sol et punir la retombée.'),
 special('Drop Wall','22A',27,1,25,None,0,'Générateur détruisible, 180 durabilité; le mur laisse passer les corps et cesse après 180 frames.','Approcher à pied ou détruire le générateur.','60 charge')],
 dict(name='Brèche de Zeta',input='236236H',cost_bars=2,startup_frames=12,on_block=-25,damage=320,effect='Saisie au grappin sur touche confirmée, crosse, projection et rafale finale; aucune saisie sur garde.'),
 ['5L > 2M > 5H xx 236R : confirmation simple, séparation finale.','3H > saut j.M > j.H > 214A xx 236236H : extension au mur, une traction par combo.'],
 'Réponses aux trois distances; défend une recharge sans supprimer les approches adverses.','Recharge et gadgets partagent les fenêtres de vulnérabilité; pression courte sans ressource.',
 'Le Major accroche une arme au sol, la vérifie puis se place entre son adversaire et une balise de secours.',
 dict(id='atriox_hw2',reason='Confrontation symbolique des chefs de guerre; cette rencontre mélange volontairement les versions Infinite et Wars 2.'),
 'Après la dernière simulation, il récupère la balise perdue et repart chercher les survivants. Aucun anneau n’est activé et aucun événement futur officiel n’est annoncé.',
 ['Exécution Grappleshot puis frappe blindée, cadrage bref.','Surcharge d’une bobine à fusion déposée derrière l’adversaire.'],
 ['Base Infinite GEN3','Mark V CE comme variante historique avec profil visuel propre','Mark VI Halo 3 comme variante historique; pas de mélange des pièces'], 'MA40 et Sidekick')

add('arbiter_h3',"Thel 'Vadam l’Arbiter",'Halo 3','h3','Duelliste à épée et lecture défensive',1000,200,'moyen',
 'Discipline 0–3; une parade réussie produit une charge; une feinte en consomme une. Aucune invisibilité gratuite héritée de Halo 2.',
 'Harnois Arbiter argenté de Halo 3; mandibles, casque et pieds digitigrades exacts; épée à deux lames.',
 ['Pommeau','Balayage digitigrade','Taille oblique','Lame ascendante','Revers au ciel','Projection au harnois'],[
 special('Fente énergétique','236H',17,5,28,-16,120,'Fente à portée moyenne; arrête la course au contact et ne piste pas un saut.','Garder debout ou esquiver avant le départ.'),
 special('Rafale plasma','236R',16,7,24,-11,65,'Deux projectiles lents; pression bouclier accrue, pas de visée automatique.','Sauter la seconde salve et punir la récupération.','20 chaleur'),
 special('Parade de duelliste','214A',5,12,25,None,70,'Contre les coups médians et hauts; ouvre une riposte unique, perd contre projection et bas.','Retarder le coup ou balayer.'),
 special('Feinte du Kaidon','22A',13,1,17,None,0,'Retrait puis retour au neutre; annulation uniquement depuis une normale gardée.','Suivre la retraite sans frapper trop tôt.','1 Discipline')],
 dict(name='Sentence de l’Arbiter',input='236236H',cost_bars=2,startup_frames=13,on_block=-24,damage=325,effect='Fente puis trois impacts énergétiques sur confirmation; animation réduite contre les grandes silhouettes.'),
 ['2M > 5H xx 236H : punition à portée moyenne.','214A réussi > 5M > 3H > j.H xx 236236H : riposte avec jauge.'],
 'Allonge régulière et punition des attaques prévisibles.','Projectile lent; parade vulnérable aux projections et aux variations de rythme.',
 'L’Arbiter déploie son épée, observe le terrain puis baisse légèrement sa lame avant le signal.',
 dict(id='tartarus_h2',reason='Rivalité de Halo 2 revisitée en simulation avec son apparence Halo 3; aucune réécriture de la chronologie.'),
 'Il range l’épée devant une porte désormais ouverte. Les guerriers qui le suivent sont invités à choisir eux-mêmes leur route.',
 ['Fente d’épée puis retrait de lame hors gros plan.','Désarmement suivi d’une grenade plasma sur l’arme abandonnée.'],
 ['Base Halo 3','Harnois Halo 2 Classic','Harnois Halo 2 Anniversary; modèles séparés'], 'Épée énergétique et fusil plasma')

add('johnson_h3','Avery Johnson','Halo 3','h3','Vétéran de soutien à punition',1100,0,'moyen',
 'Discipline d’escouade 0–2; recharger proprement et punir une attaque ratée renforcent une rafale, sans invoquer de soldat.',
 'Tenue de marine et casquette de Halo 3, visage adulte caractéristique; jamais une armure de Spartan.',
 ['Direct du vétéran','Coup de genou bas','Crosse longue','Épaule montante','Coup de canon montant','Prise au col'],[
 special('Rafale BR55','236R',13,6,23,-10,80,'Salve horizontale; la dernière balle repousse, utile pour sécuriser une recharge.','Avancer entre les salves.','3 munitions'),
 special('Tir de barrage','214R',21,12,29,-15,95,'Rafale oblique qui ferme un saut précis; angle fixé au déclenchement.','Attendre le tir puis avancer au sol.','6 munitions'),
 special('Ralliement','22A',28,1,24,None,0,'Convertit une charge de discipline en 90 récupération de santé récupérable; une fois par round.','Mettre la pression pour empêcher l’animation.','1 Discipline'),
 special('Contre au fusil','623H',12,5,29,-19,105,'Crosse puis tir court sur confirmation; ne donne pas d’invulnérabilité complète.','Faire rater la crosse à distance.')],
 dict(name='Tenez la ligne',input='236236R',cost_bars=2,startup_frames=15,on_block=-28,damage=310,effect='Barrage de fusil suivi d’un tir de laser préparé; interruption possible avant le premier impact.'),
 ['5L > 2M > 5H xx 236R : repousser puis recharger.','623H anti-air > pas avant > 5H xx 236236R : punition de saut.'],
 'Pression lisible et forte punition des imprudences.','Pas de bouclier régénérant ni de mobilité de Spartan; ralliement rare.',
 'Johnson inspecte son fusil et désigne une position à tenir; ses répliques sont écrites pour ce mode.',
 dict(id='cethegus_h3',reason='Duel entre discipline d’infanterie et défi brutal, sans inventer une rencontre historique personnelle.'),
 'Le compte rendu affiche tous les alliés revenus. Johnson éteint le tableau des scores avant de rejoindre l’escouade.',
 ['Coup de crosse suivi d’un tir final cadré à distance.','Plaquage et grenade glissée dans l’équipement adverse.'],
 ['Base Halo 3','Tenue Halo 2 sous validation des différences de visage et équipement'], 'BR55 et laser de super')

add('noble_six','Noble Six','Halo Reach','reach','Assaut mobile et adaptation contrôlée',1000,200,'moyen',
 'Carburant jetpack 100; 30 par impulsion. Une configuration d’équipement est fixée avant le combat, sans combinaison jetpack et Armor Lock.',
 'Armure Mark V B de référence promotionnelle Reach; identité personnalisable du joueur respectée, aucun visage officiel inventé.',
 ['Frappe de gant','Glissade basse','Crosse MA37','Genou propulsé','Revers aérien','Clé de bras'],[
 special('Entrée MA37','236R',14,6,22,-9,75,'Courte avance et rafale; conserve l’orientation au départ.','Garder puis reprendre l’initiative.','3 munitions'),
 special('Impulsion jetpack','214A',10,1,20,None,0,'Déplacement oblique court; trajectoire visible, pas de garde pendant la montée.','Intercepter l’angle de sortie.','30 carburant'),
 special('Tir aérien','236R en air',17,5,24,-13,85,'Salve diagonale; une seule par saut, atterrissage vulnérable.','Marcher sous le tir et punir.','3 munitions'),
 special('Interception Six','623H',10,5,29,-19,95,'Coude anti-air et retombée rapide.','Feinter le saut puis punir au sol.')],
 dict(name='Dernière extraction',input='236236H',cost_bars=2,startup_frames=12,on_block=-27,damage=315,effect='Percée au fusil suivie d’une projection et d’un tir à courte portée; pas de frappe orbitale imaginaire.'),
 ['5L > 2M > 3H > j.M > j.H : route sans carburant.','5H xx 214A > j.H > 236R en air xx 236236H : route avancée à confirmer.'],
 'Angles d’approche variés et contrôle aérien limité.','Dépend du carburant; sorties du jetpack lisibles et vulnérables.',
 'Six ferme une balise de navigation, regarde une navette s’éloigner puis adopte une garde silencieuse.',
 dict(id='zealot_reach',reason='Adversaire de Reach adapté en duel; aucune identité arbitraire assignée au Zealot générique.'),
 'La simulation s’arrête à l’instant où le dernier transport quitte l’atmosphère. Le rapport de Noble reste une archive, sans scène prétendant sauver Six dans le canon.',
 ['Désarmement puis courte exécution au couteau, hors détail graphique.','Jetpack pour prendre l’angle et tir final de précision.'],
 ['Référence Reach grise','Gabarits et équipements personnalisés étiquetés joueur, silhouette de collision constante'], 'MA37 et magnum')

add('emile_reach','Emile A239','Halo Reach','noble','Pression rapprochée et piège au recul',1000,200,'moyen',
 'Six cartouches de fusil; rechargement cartouche par cartouche interruptible. Le couteau ne consomme aucune cartouche.',
 'Casque EVA avec crâne gravé, grand couteau kukri et épaulière caractéristiques; gravure asymétrique à redessiner côté gauche.',
 ['Coup de pommeau','Balayage au couteau','Crosse de shotgun','Kukri montant','Crosse verticale','Crochetage d’épaule'],[
 special('Décharge M45','236R',15,3,29,-18,135,'Maximum proche; dégâts réduits à 45 au-delà de deux largeurs.','Rester hors portée puis punir.','1 cartouche'),
 special('Entaille de poursuite','214H',18,4,25,-12,110,'Avance courte; attrape les retraits au sol mais perd face à une frappe rapide.','Interrompre avant l’avancée.'),
 special('Crosse de rejet','623H',11,5,29,-20,95,'Anti-air compact; laisse l’adversaire à portée de fusil.','Faire rater avec saut retardé.'),
 special('Rechargement couvert','22R',22,1,18,None,0,'Une cartouche ajoutée après 22 frames; maintien pour continuer sans invulnérabilité.','Approcher pendant l’animation.')],
 dict(name='Personne ne passe',input='236236H',cost_bars=2,startup_frames=10,on_block=-26,damage=335,effect='Crosse, projection puis décharge finale; première frappe de courte portée.'),
 ['2M > 5H xx 236R : confirmation au contact.','3H > j.H > 214H xx 236236H : mur requis pour la dernière liaison.'],
 'Très dangereux à courte portée; sanctionne les reculs systématiques.','Faible portée et rechargement exposé; aucune solution gratuite au zonage.',
 'Emile essuie une marque sur la gravure de son casque puis replace son couteau dans sa main.',
 dict(id='zealot_reach',reason='Écho au conflit de Reach; sa route offre un duel original sans modifier l’issue officielle de son histoire.'),
 'Les armes se taisent quand la porte blindée se ferme. Un casque marqué reste éclairé dans les archives de Noble.',
 ['Couteau et décharge de shotgun, montage rapide.','Désarmement brutal puis impact de la crosse sur l’adversaire au sol.'],
 ['Base Reach','Variante usée de fin de campagne; mêmes pièces d’armure'], 'M45 et kukri')

add('jorge_reach','Jorge 052','Halo Reach','noble','Lourd protecteur et suppression',1050,200,'lourd',
 'Chaleur de mitrailleuse 0–100; à 100, ventilation forcée 90 frames. Le joueur peut ventiler plus tôt.',
 'Silhouette massive, armure verte et rouge Reach, visière dorée et mitrailleuse dédiée; taille réelle préservée.',
 ['Direct massif','Botte basse','Crosse de mitrailleuse','Épaule montante','Balayage du canon','Projection protectrice'],[
 special('Suppression lourde','236R',22,18,34,-18,125,'Six impacts faibles; angle horizontal, déplacement interdit pendant le tir.','Sauter tôt ou attendre la chauffe.','35 chaleur'),
 special('Ancrage','214A',16,22,28,None,0,'Absorbe un coup de projectile en payant ses dégâts; aucune résistance aux projections.','Approcher et projeter.'),
 special('Canon de barrage','623R',20,12,32,-19,110,'Tir oblique anti-air, direction verrouillée.','Avancer sous la ligne de tir.','25 chaleur'),
 special('Ventilation active','22R',24,1,24,None,0,'Réduit la chaleur de 45 seulement si toute l’action aboutit.','Punir la récupération au sol.')],
 dict(name='Rempart de Noble',input='236236R',cost_bars=2,startup_frames=19,on_block=-31,damage=330,effect='Barrage à portée moyenne puis percussion au canon; animation déclenchée seulement au premier impact.'),
 ['5L > 2M > 5H xx 236R : pression lourde courte.','2H anti-air > 623R xx 236236R : coûte de la chaleur et de la jauge.'],
 'Verrouille une ligne et punit les sauts prévisibles.','Lent, gros volume exposé; surchauffe et prises le mettent en difficulté.',
 'Jorge aide un civil à quitter le champ de simulation puis abaisse sa mitrailleuse vers la menace.',
 dict(id='hunter_h3',reason='Contraste de masse et de protection; duel interépoques clairement étiqueté archive croisée.'),
 'L’objectif évacué compte davantage que le score. Jorge laisse la mitrailleuse refroidir pendant que les derniers signaux alliés deviennent verts.',
 ['Percussion puis rafale à courte portée.','Projection contre un obstacle et destruction de l’arme adverse.'],
 ['Base Reach','Casque retiré pour intro et victoire uniquement'], 'Mitrailleuse de Jorge')

add('jun_reach','Jun A266','Halo Reach','noble','Tireur à angles et préparation',950,200,'léger',
 'Quatre cartouches de précision; stabilité monte en restant immobile 18 frames et disparaît lors d’un saut.',
 'Armure de reconnaissance Reach, foulard et accessoires d’épaule; silhouette plus légère que Jorge.',
 ['Jab au gant','Coup de pied bas','Crosse du sniper','Genou montant','Canon anti-air','Clé d’évacuation'],[
 special('Tir stabilisé','236R',24,1,36,-24,145,'Tir horizontal télégraphié; 100 dégâts sans stabilité, pas de headshot automatique.','Sauter sur le signal sonore.','1 cartouche'),
 special('Angle haut','623R',22,1,34,-22,125,'Vise une diagonale fixe; manque les adversaires au sol proches.','Passer sous le canon.','1 cartouche'),
 special('Repli de reconnaissance','214A',12,1,24,None,0,'Recul rapide sans invulnérabilité complète; n’efface pas un projectile.','Poursuivre la sortie.'),
 special('Pose de visée','22A',18,1,18,None,0,'Obtient stabilité, affiche reflet et son de lunette; aucune détection à travers une garde.','Forcer Jun à bouger.')],
 dict(name='Ligne dégagée',input='236236R',cost_bars=2,startup_frames=20,on_block=-30,damage=310,effect='Premier tir visible puis repositionnement et second tir; le premier reste gardable.'),
 ['2M > 5H xx 236R : confirmation au milieu de l’écran.','2H > 623R xx 236236R : conversion anti-air précise.'],
 'Dégâts élevés sur lecture et excellent contrôle des trajectoires.','Pression proche faible; chargeur court; tous les tirs doivent annoncer leur départ.',
 'Jun vérifie la lunette, cherche une sortie puis choisit sa ligne de tir.',
 dict(id='jega_infinite',reason='Reconnaissance contre camouflage; affrontement hypothétique entre spécialistes de la chasse.'),
 'Il consigne la faille observée et transmet l’exercice à une nouvelle promotion. Le passage de relais est une conclusion originale de cette simulation.',
 ['Désarmement et tir de précision depuis une position sûre.','Interception au couteau suivie d’un tir bref.'],
 ['Base Reach','Variante casque retiré réservée aux scènes'], 'SRS99 de Reach')

add('kat_reach','Kat B320','Halo Reach','women','Technicienne de terrain et placement',1000,200,'léger',
 'Deux charges IEM de lance-grenades; capteur posé un à la fois. Les effets électroniques sont des adaptations de gameplay, pas un pouvoir de piratage à distance.',
 'Armure bleue Reach, bras prothétique droit et casque Air Assault; ne jamais inverser le bras par miroir automatique.',
 ['Direct prothétique','Frappe de botte','Crosse tactique','Coude montant','Revers haut','Verrou de poignet'],[
 special('Tir de couverture','236R',12,4,22,-9,70,'Rafale courte qui protège la pose du capteur si confirmée.','Garder puis avancer.','2 munitions'),
 special('IEM au rebond','214G',26,6,31,-18,85,'Grenade de lanceur rebondissante; perte de bouclier renforcée, délai avant explosion.','Changer de côté ou détruire le projectile selon l’arme.','1 charge IEM'),
 special('Capteur de proximité','22A',25,1,24,None,0,'Balise de sol détruisible; révèle un camouflage dans une zone réduite, sans dégâts.','Détruire la balise ou rester hors zone.'),
 special('Interception mécanique','623H',10,4,28,-19,90,'Frappe ascendante courte; aucun bonus physique illimité du bras prothétique.','Attaquer avec une longue portée au sol.')],
 dict(name='Solution de brèche',input='236236G',cost_bars=2,startup_frames=19,on_block=-27,damage=315,effect='Charge IEM puis tir dans l’ouverture; le suivi n’a lieu que sur touche, aucune paralysie infinie.'),
 ['5L > 2M > 5H xx 236R : confirmer avant de poser.','214G explosion > 3H > j.H xx 236236G : route sur placement préparé.'],
 'Prépare le terrain et retire les avantages d’un camouflage.','Pose lente, balise fragile, faibles dégâts sans préparation.',
 'Kat referme un panneau de commande, vérifie son bras puis marque une zone sur le sol.',
 dict(id='chak_lok',reason='Détection et libération contre dissimulation et contrôle d’une prison, duel thématique original.'),
 'Le système de portes passe en accès libre. Kat copie le journal des prisonniers et ferme la simulation avant d’en lire les noms.',
 ['IEM, désarmement et tir de neutralisation final.','Charge de démolition placée sur l’équipement adverse puis retrait.'],
 ['Base Reach','Visière relevée uniquement pour scènes compatibles'], 'Magnum et lance-grenades Reach')

add('carter_reach','Carter A259','Halo Reach','noble','Chef de ligne et contre-offensive',1000,200,'moyen',
 'Ordre 0–2 gagné par garde parfaite; dépensé pour une avancée couverte. Il commande ses déplacements, sans soldats invoqués.',
 'Armure bleue Commando Reach, antennes et épaulières asymétriques; gabarit distinct de Kat.',
 ['Direct Commando','Balayage de garde','Crosse DMR','Épaule de percée','Revers du canon','Prise de commandement'],[
 special('DMR de couverture','236R',17,1,23,-10,90,'Tir unique rapide à portée moyenne, récupération fixe.','Approcher après le tir.','1 munition'),
 special('Avancée couverte','214A',15,14,25,None,0,'Avance sous résistance à un projectile; perd contre les projections et les coups bas.','Balayer ou prendre.','1 Ordre'),
 special('Contre de ligne','623H',11,5,30,-20,100,'Anti-air qui ramène au centre sans changer les côtés gratuitement.','Feinter une approche aérienne.'),
 special('Repositionnement','22A',12,1,22,None,0,'Petit pas contrôlé; s’annule après une garde parfaite, sinon reste punissable.','Varier le rythme de pression.')],
 dict(name='Noble avance',input='236236H',cost_bars=2,startup_frames=14,on_block=-26,damage=320,effect='Percée au corps puis série courte au DMR; aucune intervention hors écran.'),
 ['2M > 5H xx 236R : maintenir l’adversaire devant soi.','Garde parfaite > 214A > 5L > 3H > j.H : dépense un Ordre.'],
 'Stabilise le combat et convertit une bonne défense en avancée.','Peu de dégâts explosifs et dépend des lectures de garde.',
 'Carter vérifie six indicateurs sur sa manche puis rejoint le centre de l’arène.',
 dict(id='atriox_hw2',reason='Opposition de commandement; simulation interépoques sans rencontre canonique supposée.'),
 'Le bilan de l’exercice montre une extraction complète. Carter accepte le résultat, puis demande une nouvelle simulation avec moins de pertes possibles.',
 ['Projection puis double tir contrôlé.','Démolition d’un couvert fragilisé sur l’adversaire vaincu.'],
 ['Base Reach','Usure de fin de campagne sans modifier les pièces'], 'DMR')

add('buck_odst','Edward Buck ODST','Halo 3 ODST','teams','Assaut humain et rechargement discipliné',1100,0,'moyen',
 'Chargeur de fusil 24; rechargement de 48 frames. Une fenêtre d’action claire récompense le moment choisi, sans bonus aléatoire.',
 'Tenue ODST Halo 3 ODST; casque, couteau et marquages Buck propres; pas d’armure Helljumper Spartan IV dans le même profil.',
 ['Direct ODST','Tacle court','Crosse MA5C','Genou montant','Canon de rejet','Plaquage d’escouade'],[
 special('Percée MA5C','236R',14,8,24,-11,90,'Rafale en marchant; trois impacts, arrêt net sur garde.','Bloquer puis répondre au corps.','6 munitions'),
 special('Automag de recul','214R',15,2,25,-12,75,'Tir unique avec petit retrait; n’évite pas une prise proche.','Anticiper le recul.','1 munition secondaire'),
 special('Interception de ruelle','623H',12,5,29,-20,95,'Genou anti-air sans aura de bouclier.','Attaquer au sol en dehors de la portée.'),
 special('Recharge tactique','22R',48,1,10,None,0,'Restaure le chargeur; annulable avant f30, sans obtenir les munitions.','Mettre sous pression avant f48.')],
 dict(name='Zone d’extraction',input='236236R',cost_bars=2,startup_frames=16,on_block=-28,damage=315,effect='Rafale, plaquage et tir final; pas de Pelican qui arrive instantanément.'),
 ['5L > 2M > 5H xx 236R : route sûre sur confirmation.','2H > 214R xx 236236R : conversion à distance courte.'],
 'Bonne pression en mouvement et réponses simples.','Pas de bouclier, pas de saut surhumain; doit gagner sa recharge.',
 'Buck vérifie les canaux de son équipe, range sa balise puis pointe son fusil.',
 dict(id='cethegus_h3',reason='Infanterie de Mombasa contre commandement Brute; rivalité originale, pas une rencontre revendiquée.'),
 'Il recompte les balises de son escouade avant de quitter les rues. Le score individuel disparaît derrière le message d’extraction.',
 ['Clé au bras puis automag à courte portée.','Plaquage derrière un couvert et rafale hors gros plan.'],
 ['Base ODST','Casque retiré pour scènes','Buck Spartan IV réservé à un futur profil de règles distinct'], 'MA5C et M6C SOCOM')

add('rookie_odst','Le Rookie','Halo 3 ODST','rookie','Reconnaissance silencieuse et punition',1050,0,'léger',
 'VISR activable sans invisibilité; révèle une silhouette camouflée à courte portée mais augmente un signal visible côté adversaire.',
 'Utiliser les vues du guide cosplay officiel; armure, pochettes, casque et sac du Rookie, aucun visage inventé.',
 ['Pommeau silencieux','Balayage bas','Crosse M7S','Genou de dégagement','Canon remontant','Prise de dos'],[
 special('Rafale M7S','236R',12,6,22,-9,70,'Tir de suppression bref; suppressor visible, aucun projectile silencieux sans signal de gameplay.','Avancer après la rafale.','4 munitions'),
 special('Automag posé','214R',18,1,25,-12,90,'Tir unique plus lent, gagne en portée mais pas en priorité.','Changer d’angle au signal.','1 munition'),
 special('VISR','22A',18,1,19,None,0,'Filtre de détection local pendant 180 frames; silhouettes restent lisibles pour les deux joueurs.','Sortir du rayon ou profiter de l’activation.'),
 special('Retrait de ruelle','214A',11,1,23,None,0,'Recul bas limité; les attaques basses et projections l’attrapent.','Poursuivre au sol.')],
 dict(name='Point de rendez-vous',input='236236R',cost_bars=2,startup_frames=18,on_block=-27,damage=300,effect='Automag puis rafale M7S et déplacement vers un couvert; aucune pause invisible.'),
 ['2M > 5H xx 236R : confirmation de proximité.','5H xx 214R xx 236236R : punition d’une grosse récupération.'],
 'Dissipe les ruses visuelles et punit les gestes trop engagés.','Fragile, mobilité humaine et dégâts de pression limités.',
 'Le Rookie suit une indication lumineuse, relève son arme et ne prononce aucune réplique.',
 dict(id='chak_lok',reason='Exploration et recherche de prisonniers contre interrogateur camouflé, scénario de simulation.'),
 'Il dépose l’indice retrouvé sur une table. Un canal allié s’allume; le Rookie tourne la tête puis quitte l’image.',
 ['Désarmement discret et tir final de l’automag.','Grenade sous un bouclier retourné, puis retrait derrière un couvert.'],
 ['Base ODST','Tenue mouillée et usée de Mombasa sans ajout de plaques'], 'M7S et M6C SOCOM')

add('rtas_h3',"Rtas 'Vadum",'Halo 3','rtas','Commandant Sangheili à pression méthodique',1000,200,'moyen',
 'Cadence 0–3; alterner lame et plasma sans répéter produit une charge de recul contrôlé, aucun bombardement orbital en duel.',
 'Armure blanche Halo 3, mâchoire mutilée à respecter, proportions Sangheili; ne pas utiliser l’armure Spartan inspirée de lui.',
 ['Pommeau de commandant','Revers bas','Taille longue','Lame verticale','Rejet du harnois','Projection de pont'],[
 special('Lame de pont','236H',16,5,27,-15,115,'Taille horizontale longue; pointe seule donne le meilleur recul.','Avancer sous le départ ou garder à bonne distance.'),
 special('Double plasma','236R',18,8,25,-12,80,'Deux tirs espacés pour empêcher l’avancée monotone.','Sauter entre les deux.','25 chaleur'),
 special('Repli ordonné','214A',14,1,20,None,0,'Recule à distance fixe après un coup confirmé.','Poursuivre la sortie.','1 Cadence'),
 special('Revers de passerelle','623H',12,5,31,-21,105,'Anti-air large mais lente récupération.','Rester au sol et punir.')],
 dict(name='Pont sécurisé',input='236236H',cost_bars=2,startup_frames=14,on_block=-27,damage=325,effect='Plasma de rupture puis assaut à l’épée; aucun vaisseau miniature.'),
 ['2M > 5H xx 236H : pression de pointe.','236R touche > 5H xx 214A > 236236H : exige la bonne distance et une charge.'],
 'Gère les distances et alterne les tempos.','Repli payant; angles verticaux prévisibles.',
 'Rtas ferme un canal du Shadow of Intent et mesure le silence avant d’activer son épée.',
 dict(id='jega_infinite',reason='Deux doctrines Sangheili, fidélité à une cause contre chasse clandestine; affrontement original.'),
 'Le commandant choisit une route d’évacuation avant une cible à poursuivre. Le navire reste à sa vraie échelle dans le panorama final.',
 ['Riposte à l’épée et désarmement.','Projection contre une console suivie d’un tir plasma.'],
 ['Base Halo 3','Modèle Halo 2 Anniversary comme costume historique distinct'], 'Épée et fusil plasma')

add('tartarus_h2','Tartarus','Halo 2','tartarus','Grappler lourd à marteau',1100,180,'lourd',
 'Charge de Fist of Rukt 0–100; impulsion coûte 40. Protection de duel limitée à un coup, jamais le bouclier invincible du boss original.',
 'Fourrure blanche, armure Halo 2 et Fist of Rukt exact; Classic et Anniversary ne partagent pas le même rendu.',
 ['Poing de chef','Botte écrasante','Manche du marteau','Crochet du Rukt','Marteau ascendant','Étreinte Brute'],[
 special('Fist of Rukt','236H',24,6,35,-22,155,'Grand impact au sol; échoue contre saut correctement anticipé.','Sauter au départ et punir derrière.'),
 special('Traction gravitationnelle','214A',28,7,32,-20,90,'Attire à courte distance en cas de touche; la garde empêche la traction.','Garder et punir.','40 charge'),
 special('Revers du patriarche','623H',16,6,36,-25,125,'Anti-air lourd, aucune invulnérabilité contre les attaques au sol.','Feinter le saut.'),
 special('Défi du chef','22A',25,18,32,None,0,'Absorbe un projectile, subit ses dégâts réduits, puis perd la protection.','Utiliser plusieurs petits impacts ou une projection.','30 charge')],
 dict(name='Jugement du Rukt',input='236236H',cost_bars=2,startup_frames=20,on_block=-32,damage=350,effect='Saisie de très courte portée puis impact au sol; la première saisie se saute.'),
 ['5L > 2M > 5H xx 236H : lourd, confirme avant engagement.','2H > 623H xx 236236H : uniquement près du mur.'],
 'Menace de projection et dégâts de lecture.','Très lent et exposé après un échec; défense limitée en tournoi.',
 'Tartarus frappe une fois le sol du manche puis inspecte l’arène comme un tribunal.',
 dict(id='arbiter_h3',reason='Rivalité historique de Halo 2, rejouée avec des archives d’apparences séparées.'),
 'Dans cette issue alternative, son marteau reste seul devant les portes du sanctuaire. La victoire ne confirme pas ses croyances ni ne remplace l’histoire de Halo 2.',
 ['Projection au marteau puis impact terminal.','Traction courte et écrasement de l’équipement au sol.'],
 ['Halo 2 Classic','Halo 2 Anniversary; fidélité évaluée séparément'], 'Fist of Rukt',grenades=0)

add('atriox_hw2','Atriox','Halo Wars 2','atriox','Brawler de contrôle et prises',1100,150,'lourd',
 'Ascendant 0–3 gagné en punissant; améliore la portée d’une saisie sans devenir une attraction imblocable.',
 'Version Wars 2, armure asymétrique et gantelet, Chainbreaker à trois têtes énergétiques; pas de fusion avec Infinite.',
 ['Poing ganté','Botte lourde','Revers de Chainbreaker','Gantelet montant','Manche vertical','Prise du gantelet'],[
 special('Arc de Chainbreaker','236H',22,6,33,-20,145,'Balayage large qui ferme le recul au sol.','Sauter tôt ou interrompre au départ.'),
 special('Crochet de guerre','214H',19,4,29,-17,120,'Ramène l’ennemi seulement sur touche; garde conserve sa position.','Garder puis punir.'),
 special('Gantelet ascendant','623H',14,6,33,-23,115,'Anti-air proche avec un seul coup d’armure f8–13, dégâts subis conservés.','Attaquer bas ou par deux impacts.'),
 special('Saisie de domination','214A',14,2,35,None,160,'Prise commandée au sol; saut et recul gagnent, échec très vulnérable.','Sauter ou reculer à la lecture.','1 Ascendant pour portée accrue facultative')],
 dict(name='Briseur de ligne',input='236236H',cost_bars=2,startup_frames=18,on_block=-30,damage=350,effect='Impact du gantelet puis Chainbreaker; la garde du premier coup bloque toute la séquence.'),
 ['2M > 5H xx 236H : punir une approche lente.','5H xx 214H > 5L xx 236236H : liaison proche après attraction sur touche.'],
 'Impose la peur de la prise et retient la distance.','Démarrages lents; se fait punir lorsqu’il cherche la prise sans préparation.',
 'Atriox relève Chainbreaker d’un tas de débris, regarde l’arme adverse puis avance sans se presser.',
 dict(id='jerome_hw2',reason='Red Team et Atriox appartiennent au conflit de Wars 2; la revanche jouable reste une adaptation.'),
 'Les unités regroupées attendent son ordre. Il choisit les ressources d’une base abandonnée, laissant la victoire individuelle hors du rapport.',
 ['Gantelet, désarmement et coup de Chainbreaker.','Projection de l’adversaire contre son propre équipement détruit.'],
 ['Base Wars 2','Infinite en variante complète avec références propres et règles identiques seulement en exhibition'], 'Chainbreaker',grenades=0)

add('decimus_hw2','Decimus','Halo Wars 2','decimus','Colosse mécanisé à engagements lents',1150,120,'colosse',
 'Réacteur 100; salve 35, charge 25; refroidissement volontaire expose les articulations. Son exosquelette conserve son volume.',
 'Exosquelette de combat Wars 2, silhouette et armes à relever sur le modèle du jeu; caméra élargie, jamais miniature de Brute.',
 ['Piston court','Pied hydraulique','Bras mécanique','Levage de vérin','Arc de tourelle','Prise mécanisée'],[
 special('Salve d’exosquelette','236R',27,10,37,-24,145,'Rafale lourde horizontale; projectile annoncé et départ fixe.','Sauter pendant l’armement.','35 réacteur'),
 special('Charge de démolition','214H',28,10,39,-26,150,'Avancée lente résistante à un impact; ne traverse pas l’adversaire.','Projeter ou frapper bas deux fois.','25 réacteur'),
 special('Rejet supérieur','623H',19,7,40,-28,130,'Grande couverture anti-air avec récupération très longue.','Feinter le saut puis entrer au sol.'),
 special('Décompression','22A',35,1,25,None,0,'Récupère 40 réacteur, armure suspendue pendant l’action.','Punir les évents exposés.')],
 dict(name='Démantèlement',input='236236R',cost_bars=2,startup_frames=25,on_block=-35,damage=350,effect='Impact mécanique puis salve; pas de canon orbital en mode tournoi.'),
 ['5L > 2M > 5H xx 236R : route lourde.','2H > 623H xx 236236R : conversion proche du mur uniquement.'],
 'Très grande portée et capacité à tenir un passage.','Grosse cible, faible vitesse; presque tous les échecs donnent une punition.',
 'Des fixations mécaniques se verrouillent; Decimus vérifie le réacteur avant d’orienter son armement.',
 dict(id='douglas_hw2',reason='Confrontation avec Red Team sur l’Arche; duel réduit à une rencontre originale de ce mode.'),
 'Un rapport de récupération défile sur le blindage. La simulation se termine sur ses ateliers, sans annuler sa mort officielle dans le récit de Wars 2.',
 ['Écrasement mécanique de la position adverse, cadrage éloigné.','Saisie puis tir de l’armement de l’exosquelette.'],
 ['Exosquelette Wars 2','Version hors exosquelette réservée aux scènes et à un profil futur distinct'], 'Armement de l’exosquelette',grenades=0)

add('escharum_infinite','Escharum','Halo Infinite','escharum_axe','Patriarche à alternance feu et hache',1100,150,'lourd',
 'Ferveur 0–100 par pression gardée; activation temporaire améliore l’avance, sans recharge de vie ni invulnérabilité. Les 150 points de bouclier sont une règle de simulation 2D, distincte de la protection de la campagne reliée à Esparza.',
 'Armure et vieillissement Infinite; Diminisher of Hope, hache gravitationnelle à lame hardlight, et Scrap Cannon séparés en poses de changement d’arme.',
 ['Gantelet court','Botte du patriarche','Manche lourd','Hache montante','Revers de garde','Prise du défi'],[
 special('Rafale Scrap Cannon','236R',24,12,34,-22,130,'Tir qui repousse; vitesse au sol nulle durant la rafale.','Sauter tôt puis punir.','30 chaleur'),
 special('Marche du défi','214A',18,18,27,None,0,'Avance résistante à un impact, pas à une prise.','Projeter ou multiplier les coups.','40 Ferveur'),
 special('Diminisher of Hope','236H',25,6,35,-23,155,'Impact proche et onde courte au sol; un seul hit par cible.','Sauter l’onde ou punir de loin.'),
 special('Revers du vétéran','623H',15,6,34,-24,115,'Anti-air large; avance minimale.','Feinter une descente.')],
 dict(name='Dernier défi',input='236236H',cost_bars=2,startup_frames=22,on_block=-32,damage=345,effect='Assaut de hache gravitationnelle suivi d’une onde; aucune source extérieure de bouclier en tournoi.'),
 ['2M > 5H xx 236H : punition de proximité.','236R touche > 214A > 5H xx 236236H : nécessite Ferveur et bonne portée.'],
 'Pression de proximité et menace constante de hache.','Alternance d’armes lente; pas d’aide des machines de son combat de boss.',
 'Escharum referme un enregistrement, pose le canon et prend sa hache.',
 dict(id='chief_infinite',reason='Duel central de la campagne Infinite; version tournoi sans otage servant de batterie de bouclier.'),
 'L’enregistrement du duel rejoint les archives des Parias. Cette conclusion alternative ne réécrit pas son décès dans la campagne officielle.',
 ['Hache et projection contre un pilier de l’arène.','Renversement suivi d’une salve courte de Scrap Cannon.'],
 ['Base Infinite','Armure de défi endommagée, mêmes composants'], 'Diminisher of Hope et Scrap Cannon',grenades=0)

add('jega_infinite',"Jega 'Rdomnai",'Halo Infinite','jega','Assassin de feintes et camouflage',950,180,'léger',
 'Camouflage 100; 40 par activation, maximum 90 frames. Contour, poussière et son restent perceptibles; attaque révèle immédiatement.',
 'Sangheili cybernétique Infinite, membres prothétiques et lames rouges; préserver toutes les asymétries, aucune copie miroir.',
 ['Poing cybernétique','Entaille basse','Lame rouge','Crochet montant','Revers de lame','Prise du chasseur'],[
 special('Fente écarlate','236H',15,5,27,-16,115,'Approche rapide droite; ne suit pas un saut.','Garder puis punir.'),
 special('Voile du chasseur','214A',22,1,25,None,0,'Camouflage partiel avec signaux lisibles; ne retire ni hurtbox ni verrouillage du joueur adverse.','Capteur, frappe large ou écoute.','40 camouflage'),
 special('Crochet cybernétique','623H',10,5,30,-21,95,'Anti-air rapide mais portée courte.','Attaquer au sol de loin.'),
 special('Pas de prédation','22A',16,1,24,None,0,'Dash court qui s’arrête avant l’adversaire; aucun côté changé automatiquement.','Occuper sa destination.')],
 dict(name='Chasse close',input='236236H',cost_bars=2,startup_frames=12,on_block=-28,damage=325,effect='Lame initiale gardable puis succession de frappes; éclairage maintient la lisibilité.'),
 ['5L > 2M > 5H xx 236H : confirmation rapide.','214A > approche visible > 3H > j.H xx 236236H : camouflage ne garantit pas l’ouverture.'],
 'Feintes de timing, menace rapide et camouflage tactique.','Faible endurance et récupération des lames punissable; capteurs utiles contre lui.',
 'Une déformation d’air devient silhouette; Jega active une lame puis l’autre en entrant dans la lumière.',
 dict(id='rtas_h3',reason='Conflit de doctrine inventé; Jega demeure un personnage vivant après Infinite selon Edge of Dawn.'),
 'Son signal disparaît après la fin de l’exercice. L’archive n’affirme ni sa mort ni un événement futur au-delà des sources officielles.',
 ['Double lame et extinction du camouflage au dernier impact.','Prise cybernétique suivie d’une lame courte, cadrage contrôlé.'],
 ['Base Infinite','Dommages et poussière cohérents, sans inventer de variante canonique'], 'Lames énergétiques rouges',grenades=0)

add('chak_lok',"Chak 'Lok",'Halo Infinite','banished','Contrôleur camouflé à portée d’épée',1000,180,'moyen',
 'Dissimulation 100; 45 par camouflage 80 frames, 20 par faux départ sonore. Aucun doublon solide invoqué.',
 'Harnois doré Infinite de Chak Lok, silhouette Sangheili; à distinguer d’un Zealot Reach rouge.',
 ['Pommeau doré','Balayage de tour','Taille de garde','Lame de levage','Revers d’épée','Prise d’interrogateur'],[
 special('Estoc de la Tour','236H',18,5,28,-17,120,'Longue pointe droite, peu de couverture verticale.','Sauter l’estoc au signal.'),
 special('Dissimulation','214A',24,1,25,None,0,'Camouflage partiel; la poussière et le bourdonnement indiquent la position.','Utiliser le capteur ou une attaque de zone.','45 Dissimulation'),
 special('Contre de coursive','623H',13,6,32,-22,105,'Revers anti-air plus large que celui de Jega, plus lent.','Attaquer au sol avant le revers.'),
 special('Faux départ','22A',18,1,20,None,0,'Son de lame et petit mouvement sans hitbox; pas de silhouette autonome qui attaque.','Ne pas réagir au son seul.','20 Dissimulation')],
 dict(name='Porte condamnée',input='236236H',cost_bars=2,startup_frames=16,on_block=-29,damage=325,effect='Estoc, projection puis frappe; aucune séquence de torture jouable.'),
 ['2M > 5H xx 236H : tenir la portée de lame.','Faux départ > punition 5H xx 236236H : combo commence après la faute adverse.'],
 'Très bon contrôle d’un espace étroit.','Camouflage neutralisé par capteur et départs assez lents.',
 'Une porte de la Tour se verrouille; Chak Lok apparaît à son côté et incline sa lame.',
 dict(id='kat_reach',reason='Capteur de terrain contre dissimulation; rivalité créée pour l’adaptation.'),
 'Les portes de la simulation se referment sur une salle vide. Sa victoire hypothétique reste isolée du résultat de la campagne Infinite.',
 ['Frappe d’épée après désarmement.','Projection contre une porte et impact énergétique bref.'],
 ['Base Infinite','Camouflage comme état VFX distinct, pas un costume'], 'Épée énergétique',grenades=0)

add('alice_hw2','Alice 130','Halo Wars 2','women','Suppression mobile et libération de terrain',1050,200,'lourd',
 'Bande de 30 unités; rafale en consomme 6; récupération manuelle 62 frames. Sa mobilité en tir reste inférieure à une marche libre.',
 'Mark IV Wars 2 et marquages Alice à relever précisément; mitrailleuse lourde, jamais simple recoloration de Jerome.',
 ['Gantelet direct','Frappe basse','Crosse lourde','Épaule de libération','Canon montant','Projection Red Team'],[
 special('Barrage de libération','236R',21,14,30,-17,120,'Rafale en avançant d’un pas; s’arrête sur garde.','Sauter ou attendre la fin.','6 unités'),
 special('Percée latérale','214H',20,6,29,-17,120,'Charge d’épaule courte, sans résistance innée.','Interrompre avec un coup rapide.'),
 special('Arc de couverture','623R',19,10,32,-20,110,'Tir oblique fixé; manque une approche basse.','Avancer sous le tir.','5 unités'),
 special('Changement de bande','22R',62,1,12,None,0,'Recharge complète, interrompue si touchée avant la fin.','Punir avant le verrouillage final.')],
 dict(name='Extraction musclée',input='236236R',cost_bars=2,startup_frames=18,on_block=-30,damage=335,effect='Assaut au canon et rafale croisée de sa propre arme; aucune escouade invoquée.'),
 ['5L > 2M > 5H xx 236R : finir avec recul.','214H touche > 5L > 3H > j.H xx 236236R : près du mur.'],
 'Pression plus mobile que Jorge et grande portée.','Recharge longue; silhouette lourde, couverture basse faible.',
 'Alice détache une sangle d’évacuation puis verrouille sa mitrailleuse.',
 dict(id='atriox_hw2',reason='Réponse aux pertes de Red Team dans Wars 2; revanche hypothétique.'),
 'Le dernier prisonnier franchit le sas; Alice reprend sa position jusqu’à la fermeture complète.',
 ['Crosse et rafale de mitrailleuse.','Projection à travers un couvert léger puis tir final.'],
 ['Base Wars 2','Dommages de campagne sans modifier la morphologie'], 'Mitrailleuse lourde')

add('douglas_hw2','Douglas 042','Halo Wars 2','teams','Artillerie à trajectoires et salves',1000,200,'moyen',
 'Deux roquettes; rechargement 72 frames. Explosions gardables et dégâts personnels réduits si déclenchées trop près.',
 'Mark IV Wars 2, marquages et lance-roquettes propres; blessure et équipement d’un épisode non mélangés aux scènes précédentes.',
 ['Poing Red Team','Botte basse','Crosse de lanceur','Genou de levage','Tube montant','Clé d’assaut'],[
 special('Roquette directe','236R',26,1,38,-25,160,'Projectile lent annoncé; explosion unique, aucune poursuite automatique.','Sauter tôt ou neutraliser avec projectile puissant.','1 roquette'),
 special('Tir en cloche','214R',30,1,37,-24,145,'Arc fixe vers une zone donnée; laisse un angle d’approche proche.','Entrer sous l’arc.','1 roquette'),
 special('Rejet au lanceur','623H',12,5,30,-21,100,'Crosse anti-air pour défendre la portée minimale.','Feinter le saut et projeter.'),
 special('Recharge double','22R',72,1,10,None,0,'Deux roquettes restaurées à la fin seulement.','Maintenir une menace pendant le rechargement.')],
 dict(name='Couloir de feu',input='236236R',cost_bars=2,startup_frames=24,on_block=-34,damage=340,effect='Première roquette gardable puis détonation dirigée; pas de dégâts illimités dans le coin.'),
 ['2M > 5H xx 236R : exige une distance de sécurité.','214R touche > 3H > j.H xx 236236R : préparation de trajectoire.'],
 'Explosions qui limitent les déplacements et forte punition.','Très dépendant de ses deux tirs, danger au contact, recharge la plus longue.',
 'Douglas introduit deux roquettes et vérifie une dernière fois sa visée.',
 dict(id='decimus_hw2',reason='Opposition aux forces mécanisées de Decimus sur l’Arche, scénarisée en duel original.'),
 'Il coupe le dernier vecteur de renfort dans l’exercice puis rejoint Red Team. Les roquettes restantes sont comptées avant le départ.',
 ['Projection puis roquette dans un équipement abandonné derrière la cible.','Crosse, recul et impact explosif cadré large.'],
 ['Base Wars 2','État blessé réservé aux cinématiques de la période correspondante'], 'Lance-roquettes')

add('jerome_hw2','Jerome 092','Halo Wars 2','teams','Leader de percée et laser chargé',1000,200,'moyen',
 'Charge laser 0–100 en maintien; mouvement ralenti; relâcher avant le seuil produit seulement une feinte sans tir.',
 'Mark IV Wars 2, marquages 092; profil campagne au laser. Commander Jerome avec Hydra et Mantis reste une variante de règles future.',
 ['Direct de commandement','Balayage blindé','Crosse de laser','Épaule Red Team','Revers du canon','Désarmement Red Team'],[
 special('Laser Spartan','236R maintenu',40,3,36,-24,155,'Rayon horizontal précédé d’un point de visée; interruption avant f40 annule le tir.','Approcher pendant la charge ou sauter au signal.','100 charge'),
 special('Percée Red Team','214H',18,6,28,-16,110,'Assaut d’épaule qui rapproche et stoppe sur garde.','Garder puis punir.'),
 special('Slam d’interception','623H',14,6,33,-23,115,'Petit saut et impact proche; version duel bornée, sans atterrissage automatique sur l’ennemi.','S’éloigner de la zone annoncée.'),
 special('Feinte de charge','22A',15,1,18,None,0,'Visée visible sans rayon; conserve 20 charge au plus pour le prochain essai.','Ne pas sauter au premier voyant.')],
 dict(name='Brèche du Spirit',input='236236R',cost_bars=2,startup_frames=18,on_block=-30,damage=330,effect='Percussion puis laser à courte portée; uniquement après touche initiale.'),
 ['5L > 2M > 5H xx 214H : gagner du terrain.','5H xx laser chargé > 236236R : liaison à régler dans le prototype, coût élevé.'],
 'Choix de charge et puissant contrôle linéaire.','Laser très annoncé, pas de salve rapide pour couvrir toutes les approches.',
 'Jerome relève les données de mission puis fait pivoter son laser vers l’arène.',
 dict(id='atriox_hw2',reason='Chef de Red Team face au meneur des Parias; revanche inventée, pas nouvel événement canonique.'),
 'Le rapport repart vers le Spirit of Fire. Red Team quitte l’écran ensemble, la mission restant plus grande que le duel.',
 ['Plaquage puis laser final.','Désarmement, coup blindé et destruction de la position adverse.'],
 ['Base Wars 2','Commander Jerome réservé à profil Hydra et Mantis séparé'], 'Laser Spartan et arme secondaire')

add('zealot_reach','Elite Zealot','Halo Reach','zealot','Assaut aérien et lames longues',1000,200,'moyen',
 'Ferveur 0–2 gagnée après avance réussie; une extension aérienne coûte une charge. Rang générique, aucun nom inventé présenté comme officiel.',
 'Armure Zealot Reach rouge sombre, casque et jambes digitigrades; ne pas utiliser l’Elite doré Halo CE.',
 ['Pommeau Zealot','Patte de balayage','Taille rituelle','Lame de levage','Crochet anti-air','Projection de ferveur'],[
 special('Assaut de ferveur','236H',18,5,29,-18,120,'Bond vers l’avant suivi d’une taille; destination fixée.','Anti-air sur l’ascension.'),
 special('Rafale plasma','236R',17,7,25,-12,75,'Deux projectiles pour accompagner l’approche.','Sauter entre les tirs.','20 chaleur'),
 special('Lame du ciel','623H',12,6,32,-22,110,'Anti-air qui ne protège pas les pieds.','Attaquer bas avant le départ.'),
 special('Extension de chasse','214A en air',16,1,24,None,0,'Petit déplacement aérien, une fois par saut et par charge.','Couvrir la destination.','1 Ferveur')],
 dict(name='Vœu de conquête',input='236236H',cost_bars=2,startup_frames=17,on_block=-29,damage=325,effect='Bond gardable puis assaut de lame; pas de tracking intégral.'),
 ['2M > 5H xx 236H : pression moyenne.','3H > j.M > 214A en air > j.H xx 236236H : une charge.'],
 'Bonne portée et menace aérienne distincte de l’Arbiter.','Arrivées prévisibles et ressources limitées pour varier les trajectoires.',
 'Le Zealot contrôle un sceau de mission, déploie sa lame et avance sans hésitation.',
 dict(id='noble_six',reason='Adversaire représentatif de Reach; la narration parle d’un Zealot sans fusionner plusieurs individus du jeu.'),
 'Un symbole de mission s’allume, puis l’archive se ferme. La campagne de Reach conserve son déroulement officiel.',
 ['Saisie du harnois puis frappe d’épée.','Bond et percussion énergétique sur la position vaincue.'],
 ['Base Zealot Reach','Field Marshal réservé à variante précisément documentée, pas simple recoloration'], 'Épée et plasma')

add('cethegus_h3','Cethegus chef Brute','Halo 3','chieftain','Duelliste lourd de l’Arche',1100,150,'lourd',
 'Défi 0–2 gagné en avançant ou gardant; permet un pas blindé. L’invincibilité de certains équipements de Halo 3 est exclue du duel classé.',
 'Chef Brute du duel The Ark, armure et casque Halo 3 à relever; aucun assemblage avec l’armure Escharum.',
 ['Poing de l’Arche','Botte du défi','Manche transversal','Crochet au marteau','Arc supérieur','Prise du chef'],[
 special('Marteau de l’Arche','236H',25,6,35,-23,155,'Impact lourd avec petit souffle au sol, un seul contact par cible.','Sauter ou punir à distance.'),
 special('Pas du défi','214A',18,15,28,None,0,'Avance résistante à un coup; garde possible seulement après la récupération.','Projeter ou faire deux impacts.','1 Défi'),
 special('Arc de rejet','623H',15,6,35,-24,120,'Anti-air de grande portée et longue récupération.','Feinter le saut puis punir.'),
 special('Rupture de garde','214H',29,5,33,-21,135,'Attaque médiane lente qui réduit la garde, toujours gardable.','Interrompre dès le signal.')],
 dict(name='Duel de l’Arche',input='236236H',cost_bars=2,startup_frames=23,on_block=-34,damage=350,effect='Marteau initial gardable puis projection; aucun attroupement qui attaque le joueur.'),
 ['2M > 5H xx 236H : dégâts sur bonne lecture.','214H touche > 5L xx 236236H : lien seulement sur contre-touche.'],
 'Très forte pression mentale autour du marteau.','Départs les plus visibles, pas de projectile régulier.',
 'Le chef Brute repousse les spectateurs de l’arène puis lève le marteau en défi.',
 dict(id='johnson_h3',reason='Duel thématique original; dans Halo 3 le duel de l’Arche l’oppose au Major, distinction conservée dans le codex.'),
 'Les spectateurs cessent leurs cris lorsque l’arène se vide. Le résultat reste une variante de tournoi, pas un événement ajouté à la bataille de l’Arche.',
 ['Projection et impact gravitationnel final.','Désarmement au manche puis écrasement de l’arme adverse.'],
 ['Base Halo 3 Cethegus','Autres chefs Brutes comme apparences documentées sans nouveau nom personnel'], 'Marteau gravitationnel')

add('hunter_h3','Mgalekgolo Hunter','Halo 3','hunter','Colosse à bouclier physique et canon',1200,0,'colosse',
 'Plaque physique intacte et stabilité de garde 220; à zéro, la garde s’ouvre pendant 240 frames puis peut être relevée. La plaque ne repousse pas et ne se régénère pas matériellement. Elle ne couvre ni le dos ni les projections. Canon chauffe à 100.',
 'Hunter bleu Halo 3, colonie orange, dos vulnérable, bouclier massif et canon; taille conservée par cadrage élargi.',
 ['Bord de bouclier','Pied massif','Balayage de plaque','Levage du bouclier','Canon de rejet','Prise de colosse'],[
 special('Canon à combustible','236R',32,8,39,-27,155,'Rayon ou salve selon référence Halo 3 retenue; une seule variante visuelle verrouillée avant production.','Passer derrière au départ.','40 chaleur'),
 special('Charge de bouclier','214H',28,10,40,-28,150,'Avancée frontale; peut arrêter deux projectiles en consommant la stabilité de garde, sans destruction de la plaque.','Sauter derrière ou projeter.'),
 special('Revers de carapace','623H',20,7,42,-29,140,'Très large anti-air qui expose ensuite le dos.','Feinter puis punir le dos.'),
 special('Repli de colonie','22A',36,1,28,None,0,'Réduit la chaleur de 45; arrête de couvrir le corps pendant la ventilation.','Approcher pendant l’ouverture.')],
 dict(name='Colère de la colonie',input='236236H',cost_bars=2,startup_frames=26,on_block=-36,damage=355,effect='Percussion au bouclier puis canon; pas de deuxième Hunter invoqué en duel compétitif.'),
 ['5L > 2M > 5H xx 236R : route lente, vérification de portée obligatoire.','2H > 623H xx 236236H : près du mur seulement.'],
 'Portée et protection frontale imposantes.','Très grande cible, dos exposé, faible mobilité; se faire contourner est décisif.',
 'Le Hunter répond à un grondement hors champ puis déploie son bouclier; le partenaire reste hors de l’aire de duel.',
 dict(id='jorge_reach',reason='Opposition thématique des deux protecteurs lourds; les époques sont volontairement croisées.'),
 'La colonie rejoint son partenaire lorsque la zone cesse de trembler. Cette scène originale ne donne aucun nom canonique au Hunter générique.',
 ['Percussion de bouclier puis canon à distance courte.','Charge qui projette l’adversaire dans un couvert détruit.'],
 ['Base Halo 3','Autres modèles Halo comme variantes futures avec silhouettes et canons propres'], 'Bouclier et canon',grenades=0)

EXTRA_NORMAL_NAMES={
 'chief_infinite':['Crochet blindé','Botte accroupie','Jab aérien','Genou Spartan','Crosse plongeante'],
 'arbiter_h3':['Revers de lame','Pommeau bas','Pommeau aérien','Taille suspendue','Lame descendante'],
 'johnson_h3':['Crochet du vétéran','Coup de pied accroupi','Jab en saut','Genou du vétéran','Crosse descendante'],
 'noble_six':['Crochet de Six','Botte accroupie','Direct en saut','Genou Noble','Crosse plongeante'],
 'emile_reach':['Crochet au kukri','Entaille accroupie','Pommeau en saut','Genou d’assaut','Kukri descendant'],
 'jorge_reach':['Poing de protection','Botte de soutien','Poing en saut','Genou lourd','Canon plongeant'],
 'jun_reach':['Crochet de reconnaissance','Coup bas bref','Direct en saut','Genou de reconnaissance','Crosse de sniper plongeante'],
 'kat_reach':['Crochet prothétique','Botte d’interruption','Poing en saut','Genou tactique','Crosse tactique descendante'],
 'carter_reach':['Crochet Commando','Botte de garde','Direct en saut','Genou de percée','Crosse DMR descendante'],
 'buck_odst':['Crochet ODST','Botte accroupie','Direct en saut','Genou de ruelle','Crosse MA5C descendante'],
 'rookie_odst':['Crochet silencieux','Pommeau accroupi','Direct en saut','Genou de reconnaissance','Crosse M7S descendante'],
 'rtas_h3':['Revers de commandant','Pommeau accroupi','Poing en saut','Taille de passerelle','Épée descendante'],
 'tartarus_h2':['Crochet du patriarche','Poing bas','Poing suspendu','Genou du chef','Rukt plongeant'],
 'atriox_hw2':['Crochet du gantelet','Botte d’arrêt','Gantelet en saut','Genou de guerre','Chainbreaker descendant'],
 'decimus_hw2':['Revers de vérin','Pied hydraulique bref','Piston en bond','Genou mécanique','Bras d’exosquelette plongeant'],
 'escharum_infinite':['Crochet du patriarche','Botte d’arrêt','Gantelet en saut','Genou du défi','Hache gravitationnelle descendante'],
 'jega_infinite':['Revers cybernétique','Lame basse brève','Poing cybernétique en saut','Lame suspendue','Double lame descendante'],
 'chak_lok':['Revers doré','Pommeau bas','Poing en saut','Taille de coursive','Estoc descendant'],
 'alice_hw2':['Crochet de libération','Botte d’arrêt','Gantelet en saut','Genou d’extraction','Mitrailleuse descendante'],
 'douglas_hw2':['Crochet Red Team','Botte accroupie','Direct en saut','Genou de couverture','Tube de lanceur descendant'],
 'jerome_hw2':['Crochet de percée','Botte d’interruption','Direct en saut','Genou Red Team','Crosse de laser descendante'],
 'zealot_reach':['Revers rituel','Pommeau bas','Poing en saut','Taille de ferveur','Lame de conquête descendante'],
 'cethegus_h3':['Crochet du chef','Poing accroupi','Gantelet en bond','Genou du défi','Marteau de l’Arche descendant'],
 'hunter_h3':['Revers de plaque','Pied d’arrêt','Bord de plaque en bond','Choc de carapace aérien','Plaque plongeante']
}
EXTRA_STATS={
 'léger':[(8,3,14,-3,55),(5,2,11,-2,30),(5,3,12,None,35),(8,4,16,None,60),(12,5,21,None,85)],
 'moyen':[(9,3,16,-4,60),(6,2,12,-3,35),(6,3,13,None,40),(9,4,17,None,65),(14,5,23,None,90)],
 'lourd':[(12,4,20,-6,75),(8,3,15,-4,40),(8,4,16,None,45),(12,5,21,None,80),(18,6,28,None,110)],
 'colosse':[(14,5,23,-8,85),(10,3,18,-6,45),(10,4,20,None,50),(15,5,25,None,90),(22,7,33,None,125)]
}
for fighter in F:
 for normal in fighter['normals']:
  normal['allowed_state']='ground'
  normal['hit_level']='throw' if normal['input']=='6L+M' else ('low' if normal['input']=='2M' else ('high' if normal['input']=='5L' else 'mid'))
 for ix,(name,stats) in enumerate(zip(EXTRA_NORMAL_NAMES[fighter['id']],EXTRA_STATS[fighter['weight']])):
  command=['5M','2L','j.L','j.M','j.H'][ix]
  air=ix>=2
  fighter['normals'].append(dict(name=name,input=command,startup_frames=stats[0],active_frames=stats[1],recovery_frames=stats[2],on_block=stats[3],damage=stats[4],allowed_state='air' if air else 'ground',hit_level='overhead' if air else ('low' if command=='2L' else 'mid'),landing_recovery_frames={'léger':6,'moyen':7,'lourd':8,'colosse':10}[fighter['weight']] if air else 0,properties=('overhead; garde debout; avantage réel selon hauteur de contact; récupération d’atterrissage obligatoire avant spécial terrestre' if air else 'annulable en normale supérieure ou spécial sur contact; aucune invulnérabilité')))
 for sp in fighter['specials']:
  sp['allowed_state']='air' if 'en air' in sp['input'] else 'ground'
 fighter['super']['allowed_state']='ground'
 fighter['combos']=[c.replace('j.H xx 236','j.H > atterrissage > 236').replace('j.H > 214','j.H > atterrissage > 214').replace('236R en air xx 236236H','236R en air > atterrissage > 236236H') for c in fighter['combos']]

EXPANSIONS=[
 ('UNSC et Spartans','Fred 104, Kelly 087, Linda 058, Locke, Vale, Tanaka, Dare, Dutch, Romeo, Mickey, Sgt Forge, Agryna, Dinh, Eklund','Rôles et armures distincts; ne pas réduire Blue Team à des couleurs.'),
 ('Covenants et alliés','Ripa Moramee, Sesa Refumee, Ntho Sraom, Usze Taham, Let Volir, Jackal, Skirmisher, Grunt spécialisé','Les anonymes sont des classes, les personnages nommés conservent une biographie sourcée.'),
 ('Parias','Pavium, Voridus, Colony, Yapyap, Hyperius, Tovarus, Bassus','Colony et Yapyap nécessitent de décider une unité jouable et de traiter séparément les pouvoirs RTS.'),
 ('Forerunners et Flood','Didacte, Warden Eternal, Harbinger, chevalier prométhéen, forme de combat Flood','Les entités géantes ou volantes passent d’abord en boss; les formes Flood ne fusionnent pas artificiellement les espèces hôtes.'),
 ('Autres continuités','Halo Legends, romans, comics, Silver Timeline et contenus coupés documentés','Étiquettes distinctes, zéro apparence supposée officielle sans référence. Silver Timeline n’écrase pas la continuité des jeux.')
]

COMMON='''# Roster et parcours de Halo Combats

## Cadre de conception

Cette annexe définit vingt quatre combattants de départ et leurs parcours d’arcade. Les identités et les apparences proviennent de Halo; les commandes, les chiffres, les enchaînements, les scènes et les rivalités interépoques sont des propositions originales pour Halo Combats. Aucun de ces parcours n’est une nouvelle histoire officielle. Une archive d’entraînement permet de réunir des périodes différentes sans ressusciter des personnages dans la chronologie.

La fidélité un pour un constitue un objectif de production vérifiable. Elle exige les vues de face, de dos et des deux profils d’une version déterminée du jeu, une comparaison des pièces et une validation des proportions. Une description textuelle ou une première image générée ne suffit pas à la certifier. Les fichiers de cette annexe ne contiennent aucun sprite ni animation achevés. Le statut de chaque fiche reste une conception à implémenter.

## Grammaire des commandes

La simulation tourne à 60 Hz. L, M et H sont les attaques légère, moyenne et lourde; R utilise l’arme; G utilise la grenade ou la munition secondaire autorisée; A commande l’aptitude. Les directions suivent le pavé numérique face à droite: 5 neutre, 2 bas, 6 avant, 4 arrière, 3 diagonale basse avant. Les quarts de cercle 236 et 214 et le dragon 623 sont toujours relatifs à l’orientation. Le menu propose les mêmes actions avec raccourcis accessibles et historique des entrées.

Trois barres d’énergie constituent le maximum commun. Les supers ci-dessous coûtent deux barres. Les grenades portées sont limitées à deux; un personnage sans grenade n’en reçoit pas une arbitrairement. Les deux charges IEM de Kat occupent son stock de grenades. R+G recharge l’arme ou ventile lorsque le personnage le permet; une fiche peut également proposer 22R pour la même action. La différence ne crée aucune annulation supplémentaire.

Les chiffres indiquent démarrage, durée active, récupération, avantage sur garde et dégâts bruts avant réduction de combo. Une valeur négative de garde signifie que l’attaquant agit plus tard. La valeur «sans contact» concerne les poses et déplacements qui ne frappent pas. Les projectiles affichent leur durée d’émission; leur temps de trajet peut modifier l’avantage réel. Les projections listent la récupération si elles ratent et ne se bloquent pas. Elles se déchoppent sur sept frames, sauf prises commandées qui se battent par mouvement ou saut.

Le tableau de chaque personnage donne trois normales, un lanceur, un anti-air et une projection. Les autres normales de proximité, saut, accroupi et course restent une tâche de production; elles ne sont pas comptées comme terminées. Les commandes 5M, j.M et j.H apparaissant dans les exemples sont des besoins explicites d’extension du moveset. Le prototype devra valider chaque liaison et ajouter ces données avant publication jouable. «xx» signifie une annulation autorisée; «>» une liaison ou un enchaînement. Un combo indiqué est une intention de conception, pas une route déjà testée.

Les dégâts de combo suivent 100, 90, 80, 70 puis 60 pour cent pour les premières frappes, avec plancher 35 pour cent sur les suivantes et minimum 40 pour cent sur un super. Un seul rebond mural, une seule relance et une seule traction sont autorisés par combo. Toute répétition d’une même attaque spéciale après sa première extension augmente le recul et force la sortie. Les grandes silhouettes n’obtiennent pas des boucles infinies parce que leurs hitboxes restent plus longtemps dans un tir.

## Endurance et équité

Le repère Spartan est 1000 points de santé et 200 de bouclier. Les chiffres des fiches sont des valeurs compétitives, pas des mesures du lore. Les personnages humains sans Mjolnir reçoivent davantage de santé mais aucun bouclier fictif. L’armure d’un Hunter agit comme une protection physique frontale avec angles et stabilité de garde. Le délai de régénération du bouclier, ses interruptions et les dégâts plasma doivent être communs à toutes les fiches et documentés dans le système central.

Les poids léger, moyen, lourd et colosse servent à régler inertie et récupération. Ils ne changent pas les règles universelles de projection et n’immunisent pas automatiquement contre les combos. Decimus et Hunter conservent leur gabarit: zoom, largeur d’arène et cadrage assurent la visibilité. Si une scène ne peut maintenir cette échelle, elle devient une scène de boss au lieu de réduire le personnage.

## Structure des routes narratives

Chaque parcours dure huit rencontres: deux apprentissages contre archétypes différents, une rencontre de faction, une épreuve de mouvement, un combat intermédiaire, le rival, un boss de grande taille, puis le duel final. Les deux dernières places peuvent s’inverser pour garder une fin lisible. Les boss sont choisis dans le registre des combats géants selon l’époque de la route. Les rencontres entre époques affichent explicitement «simulation croisée» à la sélection et dans le journal.

L’introduction dure huit à douze secondes; les échanges avec le rival dix à quinze secondes; l’ending trente à quarante cinq secondes. Tout peut être passé après une première entrée, revu dans une galerie, et sous-titré avec noms de locuteurs. Le Rookie conserve une mise en scène silencieuse. Les répliques éventuelles sont originales; aucune citation de jeu n’est fabriquée.

Chaque fiche prévoit deux exécutions. Elles interviennent seulement après le résultat définitif du match et restent désactivables ou remplaçables par une mise hors combat courte. La campagne ne transforme pas automatiquement une exécution de tournoi en mort canonique. L’option tournoi passe la scène après trois secondes et ne récompense pas la violence par un avantage de gameplay. L’adaptation conserve l’impact des armes Halo, les boucliers, les dégâts d’armure et les explosions sans ajouter une grammaire de démembrement étrangère à chaque référence.

## Sélection initiale

Les vingt quatre choix constituent un premier périmètre de production et non l’ensemble de l’univers Halo. Les costumes, armures de plusieurs jeux et états endommagés restent des variantes. Un changement de nature comme Buck ODST devenu Spartan IV requiert un profil de règles propre, pas une peau conservant artificiellement les statistiques humaines. L’interface affiche le jeu de référence, l’équipement et les restrictions du profil avant de lancer un combat.
'''

def render():
 out=['''# Roster et parcours de Halo Combats

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
''']
 detailed={'chief_infinite','arbiter_h3','johnson_h3','noble_six','emile_reach','jorge_reach','kat_reach','atriox_hw2','escharum_infinite','jega_infinite','jerome_hw2','hunter_h3'}
 out.append('| ID | Combattant | Référence | Rôle | Santé | Bouclier |\n|---|---|---|---|---:|---:|')
 for f in F: out.append(f"| {f['id']} | {f['name']} | {f['era']} | {f['archetype']} | {f['health']} | {f['shield']} |")
 for i,f in enumerate(F,1):
  out.append(f"\n## {i} {f['name']}\n")
  out.append(f"**Référence et silhouette.** {f['era']}. {f['visual_lock'] if f['id'] in detailed else ''} [Source {f['source_id']}]({f['source_url']}).")
  if f['id'] in detailed:
   out.append(f"**Profil.** {f['archetype']}; {f['health']} santé et {f['shield']} bouclier; poids {f['weight']}. {f['unique_resource']}")
   out.append('\n| Commande | Coup | Démarrage actif récupération | Garde | Dégâts |\n|---|---|---|---:|---:|')
   for n in f['normals'][:6]:
    out.append(f"| {n['input']} | {n['name']} | {n['startup_frames']}/{n['active_frames']}/{n['recovery_frames']} | {n['on_block'] if n['on_block'] is not None else 'prise'} | {n['damage']} |")
   out.append('\n**Spéciaux.**')
   for s in f['specials']:
    frames=f"{s['startup_frames']}/{s['active_frames']}/{s['recovery_frames']}"
    block=f"{s['on_block']:+}" if isinstance(s['on_block'],int) else 'sans contact'
    out.append(f"\n- **{s['name']} — {s['input']}**. {frames} frames; garde {block}; {s['damage']} dégâts; coût {s['cost']}. {s['effect']} Réponse adverse: {s['counterplay']}")
   s=f['super'];out.append(f"\n**Super.** {s['name']}, {s['input']}, {s['cost_bars']} barres, départ {s['startup_frames']} frames, garde {s['on_block']}, {s['damage']} dégâts. {s['effect']}")
   out.append('\n**Combos proposés.** '+ ' / '.join(c.split(' : ')[0] for c in f['combos'])+'.')
  else:
   out.append('**Quatre spéciaux.** '+'; '.join(f"{s['name']} ({s['input']}, {s['startup_frames']}f, {s['damage']} dégâts)" for s in f['specials'])+'.')
   s=f['super'];out.append(f"**Super.** {s['name']} ({s['input']}, deux barres, {s['damage']} dégâts). Les onze normales, les contre-jeux, les durées complètes et les deux combos figurent dans roster.json.")
  out.append(f"\n**Forces et réponse adverse.** {f['strength']} {f['weakness']}")
  rival=next(x for x in F if x['id']==f['rival']['id'])['name']
  out.append(f"\n**Parcours original non canonique.** Intro: {f['intro']} Rival: {rival}. {f['rival']['reason']} Ending: {f['ending']}")
  out.append('\n**Deux exécutions.** '+' / '.join(f['finishers']))
  if f['id'] in detailed: out.append('\n**Variantes à produire.** '+'; '.join(f['costumes'])+'.')
 out.append('\n## Extensions de roster\n')
 for cat,names,rule in EXPANSIONS:out.append(f'**{cat}.** {names}. {rule}\n')
 out.append('''## Contrôles de fidélité et points à résoudre

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
''')
 for k,s in SOURCES.items():out.append(f"- **{k}** — [{s['title']}]({s['url']}).")
 return re.sub(r'(?<=\|)\n\n(?=\|)', '\n', '\n\n'.join(out))+'\n'

assert len(F)==24
assert len({x['id'] for x in F})==24
assert all(len(x['specials'])==4 and len(x['normals'])==11 and len(x['combos'])==2 and len(x['finishers'])==2 for x in F)
assert all(x['rival']['id'] in {y['id'] for y in F} for x in F)
payload={'schema_version':'1.0','project':'Halo Combats','language':'fr','date':'2026-11-19','scope':'24 combattants proposés; règles originales, canon visuel à valider','simulation_hz':60,'max_energy_bars':3,'max_grenades':2,'fighters':F,'expansions':[{'category':a,'candidates':b,'rule':c} for a,b,c in EXPANSIONS],'sources':SOURCES}
(ROOT/'roster.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'roster_chapter.md').write_text(render(),encoding='utf-8')
(ROOT/'source_registry.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'fighters':len(F),'normals':sum(len(x['normals']) for x in F),'specials':sum(len(x['specials']) for x in F),'supers':len(F),'combos':sum(len(x['combos']) for x in F),'story_routes':len(F),'finishers':sum(len(x['finishers']) for x in F),'words_markdown':len(render().split()),'files':['roster.json','roster_chapter.md','source_registry.json']},ensure_ascii=False))
