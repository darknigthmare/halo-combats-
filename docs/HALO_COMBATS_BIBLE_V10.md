# Halo Combats — Bible de production V10

État du **27 novembre 2026 (Europe/Paris)**. Projet de Darknigthmare. Cette version est le point d’entrée actif de la bible : elle rassemble les fondations déjà conçues, les trois guides complets, leurs adaptations Halo, les nouveaux visuels et les preuves de fonctionnement du lot V10.

**Objectif : fidélité à l’incarnation 1:1 et cohérence avec le lore. État de validation : aucun PNG certifié 1:1 à ce jour.** La présence d’une fiche, d’un fichier ou d’un test de logique ne suffit pas à valider un personnage terminé.

## 1. Documents constitutifs

| Document | Rôle dans la bible |
|---|---|
| [Bible V1](HALO_COMBATS_BIBLE_V1.md) | Fondations du combat, roster initial, arènes, boss, modes, histoires et ressources déjà conçues. |
| [Intégration des guides V10](HALO_COMBATS_GUIDE_INTEGRATION_V10.md) | Adaptation des 68 sections et suivi de 311 exigences ; décisions, dépendances, limites et sources. |
| [Guide général intégral](guides_combat/Combat_Games_Guide_General_v1.0.txt) | Sections 00–29 : architecture globale du jeu et critères de production. |
| [Extension 01 intégrale](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt) | Sections 30–49 : taunts, sélection, équipes, tag, supers, conclusions, bonus, entités et exploration. |
| [Extension 02 intégrale](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt) | Sections 50–67 : emplacements verrouillés, découverte, accès, récompenses et droits optionnels. |
| [Catalogue V10](HALO_COMBATS_CATALOGUE_V10.md) | État des incarnations, des 111 PNG et des manquants. |
| [Projectiles et VFX V10](HALO_COMBATS_PROJECTILES_V10.md) | 24 fiches de production, règles d’entités et sources propres au profil Infinite retenu. |
| [Classeur de production V10](HALO_COMBATS_PRODUCTION_V10.xlsx) | Synthèse, catalogue et exigences avec compteurs recalculables. |

Les originaux des guides sont conservés sans réécriture et vérifiés par SHA-256. Leur [provenance](guides_combat/source_metadata.json) et leur date propre restent accessibles. Le document général est daté du 25 novembre, l’Extension 01 du 26 novembre et l’Extension 02 du 27 novembre 2026.

Les paramètres V1 restent des fondations de conception. Les paramètres du laboratoire V10 concernent sa démonstration locale et sont nommés comme tels. La jauge d’équipe V10 ne remplace pas implicitement les trois segments d’énergie individuelle de la bible V1. Les [écarts recensés](HALO_COMBATS_GUIDE_INTEGRATION_V10.md#7-écarts-constatés-entre-conception-et-prototypes) restent à arbitrer avant l’unification du moteur.

## 2. Identité et périmètre

Halo Combats est un projet de fan de jeu de combat latéral. Il conserve une lecture nette des combattants et des grandes machines, des incarnations identifiables, et des fiches reliées à leurs œuvres. Les Archives de combat forment un cadre original de consultation et de simulation. Ce cadre ne rend pas historiques les rencontres impossibles entre périodes ou continuités.

Le catalogue couvre actuellement 128 personnages, 24 costumes, 46 stages, 34 boss, 19 projectiles et 5 effets. Les 112 œuvres ou composants recensés constituent un registre partiel : leur présence ne signifie pas que tous leurs contenus ont été inventoriés. Le statut de publication des œuvres hérité de V9 n’a pas été réaudité globalement dans ce lot.

La production de ce lot porte sur les **poses fixes**, deux **masters de décor**, la documentation, le catalogue et une **démonstration de règles**. Les clips de combat et de présentation restent des tâches explicites. Un bouton « super duo » dans la démonstration exécute des états et des événements ; il ne constitue pas une cinématique finale.

## 3. Contrat de fidélité et de lore

Chaque contenu doit conserver un identifiant stable, une œuvre, une incarnation, une période pertinente et une continuité. Les sources déterminent ce qui est attesté. Les gestes, règles de combat, valeurs, chorégraphies et interfaces originales portent leur statut d’adaptation.

### Contrôle visuel

Pour chaque PNG, vérifier silhouette, proportions, armure, matières, couleurs, arme, équipement, asymétries, mains, pieds et cadrage. Une vue de face seule ne vérifie pas le dos. Le miroir automatique est exclu pour préserver prothèses, gauntlets, plaques et gravures. Les projectiles sont des objets individuels ; les effets, traînées et corps d’armes ne sont pas confondus.

Une image porte un de ces états :

| État | Signification |
|---|---|
| Manquant | Aucun PNG lié ; la fiche peut déjà exister. |
| Candidat | Fichier présent, comparé, avec validation fine encore ouverte. |
| À corriger | Écart visible consigné ; le fichier reste consultable pour révision. |
| Certifié 1:1 | Réservé à une validation comparative complète ; aucun asset ne possède cet état en V10. |

La V10 conserve les 104 PNG V9 à l’identique et ajoute sept PNG sans retouche. Les images de référence externes restent identifiées par URL et empreinte ; elles ne sont pas comptabilisées comme créations du projet.

### Contrôle narratif

Le canon principal, Silver et les univers Fracture restent séparés. Une relation attestée permet de concevoir une collaboration ; elle ne prouve pas une scène précise. Un duo mélangeant les versions de plusieurs époques doit afficher son cadre de simulation. Les finishers ne ressuscitent pas un partenaire KO.

Les personnages conservent les équipements de leur incarnation. Une version ODST ne reçoit pas un bouclier MJOLNIR fictif. Une IA sans corps physique ne devient pas automatiquement un combattant humanoïde. Une modification de patch n’est pas confondue avec une autre œuvre.

Deux corrections concrètes sont appliquées : le Chevalier standard est rattaché à **Halo 4**, et les fiches Infinite utilisent un **profil sandbox CU32 daté du 30 avril 2024**, dont les changements connus corrigent l’ancien inventaire officiel. Ce profil ne prétend pas certifier l’équilibrage courant de tous les modes.

## 4. Extension 01 : règles d’équipe et présentations

Le [laboratoire des extensions](../prototype/halo_extensions_v10.html) expose une équipe de deux membres, leurs PV individuels, l’actif et la réserve. Sa jauge commune vaut 100 au maximum. Les valeurs sont des réglages de démonstration à équilibrer.

| Système | Comportement démontré | Production restante |
|---|---|---|
| Assistance | Arrivée, contact, sortie et récupération ; coût engagé ; partenaire occupé et vulnérable. | Animation et équipement exacts de chaque assistance. |
| Tag | Transfert du contrôle et conservation des PV ; coût volontaire, relais KO gratuit ; disponibilité exclusive. | Entrées/sorties dessinées, collisions et variantes de kits. |
| Taunt | États de début, maintien et fin ; vulnérabilité, interruption et cancel ; aucun gain gratuit. | Gestes, expressions et audio propres à chaque incarnation. |
| Super duo | Touche, garde et raté distincts ; coût engagé ; résultat identique si la présentation est passée. | Storyboard, clips, caméra et variantes de cibles. |
| Finisher | Fenêtre après victoire, vérification du duo et du contexte, repli vers victoire normale. | Chorégraphies spécifiques et conclusions narratives. |
| Sélection | Aperçu, confirmation et retrait enregistrés comme événements. | Clips de sélection/désélection ; les PNG restent fixes. |
| Bonus | Épreuve de précision et objectifs de coordination ; réussite et récompense persistées. | Décors dédiés, autres activités, niveaux et raccords aux histoires. |

Les collisions de combat du jeu complet, les affrontements à QTE, les objets posés, l’exploration des Archives, les replays et le réseau ne sont pas livrés par ce laboratoire. Ils demeurent dans les exigences de l’Extension 01 avec leurs dépendances.

## 5. Extension 02 : découverte, droits et fichiers

Le modèle conserve quatre dimensions séparées :

1. **Découverte** : secret, indice ou contenu identifié.
2. **Droits** : acquisition permanente, droit temporaire ou état de vérification inconnu.
3. **Fichiers disponibles** : présence effective du contenu requis.
4. **Compatibilité de partie** : continuité, mode, équipe et prérequis.

L’aperçu d’un contenu verrouillé ne le sélectionne pas et n’accorde aucun droit. Un contenu acquis mais sans image reste acquis ; son problème est la production manquante. Un costume peut être gagné avant son personnage et conserve cette acquisition.

Les conditions ET/OU, l’attribution unique, le coût unique et les sources multiples sont gérés dans le modèle local. L’expiration d’une source temporaire ne retire pas un droit permanent. Une erreur de vérification ne devient pas une preuve d’expiration. Les préférences de sélection et les événements gagnés sont sauvegardés sous un espace de stockage propre à cette version.

Les emplacements secrets masquent aussi leur identité ; les indices peuvent proposer une silhouette. Le texte et l’icône accompagnent la couleur. Le contenu connu affiche une condition utile et une explication distincte lorsqu’un fichier manque.

Les droits de soutien sont des **cas de simulation locale**, utiles pour vérifier permanent, temporaire, expiration et dépendances. Aucun abonnement réel, paiement, fournisseur, jeton ni compte externe n’est connecté. Les futurs avantages cosmétiques ne doivent pas modifier dégâts, collisions, timings ou lisibilité utile.

## 6. Projectiles, effets et changement de combattant

Les [24 fiches structurées](../data/projectiles_v10.json) distinguent l’identité sourcée de l’adaptation 2D. Chaque entité prévoit propriétaire initial, équipe, événement d’émission unique, cible éventuelle, durée, collision et politique de fin.

Un projectile déjà émis conserve son attribution après un tag. Un faisceau continu cesse lorsque son porteur ne peut plus le maintenir. Pause et présentation de super gèlent les durées ; passer une présentation ne réémet pas les dégâts. La fin de round nettoie les entités et compteurs. Les cibles d’accumulation du Needler excluent véhicules et structures.

Ces règles sont spécifiées pour l’intégration future. Les quatre PNG de projectiles disponibles ne prouvent ni collision jouable, ni impact animé, ni système de projectiles persistant implémenté.

## 7. État du lot V10

| Mesure | V9 | V10 |
|---|---:|---:|
| Fiches | 232 | 256 |
| PNG distincts | 104 | 111 |
| Fiches illustrées | 77 | 84 |
| Fiches historiques sans visuel | 155 | 152 |
| Nouveaux dossiers projectile/VFX sans visuel | — | 20 |
| Total des fiches sans visuel | 155 | 172 |
| Nouveaux clips d’animation | 0 | 0 |
| Calques de parallaxe indépendants | 0 | 0 |
| PNG certifiés 1:1 | 0 | 0 |

L’augmentation du total des manquants vient de l’ouverture de 24 dossiers projectile/VFX, dont quatre ont reçu un PNG. Trois anciens manquants sont illustrés : Pavium et les deux décors. Le catalogue expose ces cohortes séparément pour ne pas confondre extension du périmètre et régression.

Sept images ont été produites sur treize appels réels. Cinq appels ont été refusés à la sortie du service de génération ; un appel a rencontré une erreur technique. Le seul nouvel essai après erreur technique concernait Kelly ; il a ensuite été refusé. Aucun refus n’a été converti en faux fichier ou contourné par un autre moteur.

## 8. Validation et ordre de production

Les contrôles automatisés du lot vérifient les empreintes des PNG, l’intégrité des trois guides, les identités conservées, les compteurs, les catégories supplémentaires, l’égalité du catalogue hors ligne et du JSON, et les mécanismes de la démonstration. Les reçus sont regroupés dans [qa_v10](../prototype/qa_v10/) ; ils précisent la portée et les limites.

Ordre de travail maintenu :

1. Corriger les écarts des candidats, en commençant par les géométries déjà signalées.
2. Compléter les dossiers visuels et les poses fixes manquantes par incarnation.
3. Décliner les kits et les règles d’entités dans le moteur avec collisions vérifiables.
4. Produire les animations explicitement planifiées, leurs sons et leurs fenêtres.
5. Construire les modes et parcours complets avec leurs raccords narratifs.
6. Valider le réseau et les droits réels uniquement lorsque ces intégrations sont effectivement réalisées.

Le [plan de tâches](../data/production_tasks_v10.json) détaille les jalons visuel, fidélité et intégration spécifique par entrée. Ce suivi évite de réduire la production du jeu à un pourcentage de fichiers présents.
