# Halo Combats — rapport V8 : nouveaux candidats et suivi des manquants

## 1. Résultat

La reprise V8 a produit **4 nouveau(x) PNG candidat(s)** : **Jameson Locke, Michael « Mickey » Crespo, Skirmisher Champion — classe Reach, Bassus**. **20 appels réels** ont été effectués sur **19 cibles distinctes**. Les autres résultats comprennent **15 refus `moderation_blocked`**, **0 erreur(s) de quota** et **1 erreur(s) technique(s)**. Les réponses du service restent conservées exactement.

| Mesure | V8 / état courant |
|---|---:|
| Cibles prévues / distinctes appelées | 19 / 19 |
| Appels réellement effectués | 20 |
| Nouveaux PNG | **4** |
| Nouvelles identités d’extension illustrées | 4 |
| Refus `moderation_blocked` | 15 |
| Erreurs de quota / autres erreurs techniques | 0 / 1 |
| Demandes différées sans appel | 0 |
| PNG cumulés / anciens PNG conservés | 94 / 90 |
| Extensions avec image / encore sans image | 21 / 13 |
| Gardes de base disponibles | 23 / 24 |
| Nouveaux clips d’animation / certification 1:1 | 0 / 0 |

## 2. Candidats produits

| Personnage | Candidat | Orientation observée | Statut |
|---|---|---|---|
| Jameson Locke | [locke_h5_initial_right_v01](../assets/characters_wave8/locke_h5_initial_right_v01.png) | right_three_quarter | Candidat avec réserves |
| Michael « Mickey » Crespo | [mickey_odst_initial_right_v01](../assets/characters_wave8/mickey_odst_initial_right_v01.png) | right_three_quarter | Candidat avec réserves |
| Skirmisher Champion — classe Reach | [skirmisher_champion_reach_initial_right_v01](../assets/characters_wave8/skirmisher_champion_reach_initial_right_v01.png) | right_three_quarter | Candidat avec réserves |
| Bassus | [bassus_infinite_initial_right_v01](../assets/characters_wave8/bassus_infinite_initial_right_v01.png) | mostly_front_head_right | Candidat avec réserves |

Les PNG sont copiés sans modification de leurs octets. Une image est comptée comme candidate, pas comme animation ou silhouette certifiée 1:1.

### Jameson Locke

- Fichier : [assets/characters_wave8/locke_h5_initial_right_v01.png](../assets/characters_wave8/locke_h5_initial_right_v01.png).
- SHA-256 : `ec65dd5fd06a829473d3f5ed2a3edbcc361c9b67ca0cd07ad84f691e7934b916`.
- Format : 1327 × 1185 px, RGBA, alpha [0, 255].
- Orientation observée : right_three_quarter.
- Sélection : préféré pour sa portée statique.
- Fidélité non certifiée ; aucune animation.

**Observations de QA :**

- Aperçu renvoyé par imagegen inspecté individuellement : un Locke complet, casque fermé HUNTER à visière cyan, armure gris acier, deux bottes et fusil vert entièrement visibles.
- Deux mains tiennent un seul fusil ; silhouette, pose et tête orientées vers la droite, mais torse encore en trois-quarts, pas un profil strict.
- La référence officielle est frontale/trois-quarts ; volumes de côté, petits marquages et géométrie détaillée du fusil restent à comparer au modèle.
- La marge au-dessus du casque est de18px et sous les bottes de36px sur1185px ; les6% demandés ne sont pas atteints.
- Quelques franges colorées fines se voient sur les contours dans l’aperçu ; détourage de production à examiner.
- Inspection individuelle root du PNG livré et du rendu officiel Halo 5 : corps, deux pieds, casque et fusil entiers ; pose vers la droite en trois-quarts.
- Armure HUNTER gris sombre, visière cyan et fusil vert cohérents globalement avec la référence ; microgéométrie et détails occultés non certifiés.
- L’image est normalement lisible dans view_image côté root. Le rendu presque noir observé par le producteur n’est pas reproduit ici ; aucun pixel n’a été modifié.
- Mesure indépendante en lecture seule : 1327 × 1185 px, RGBA, alpha [0, 255], 1209141 pixels entièrement transparents. Marges au seuil alpha >16 : {'left': 212, 'top': 18, 'right': 275, 'bottom': 36}. Contacts du cadre : {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}.

**Suite requise :**

- Comparer la géométrie latérale de l’armure et du fusil à des vues canoniques supplémentaires.
- Produire un cadrage avec marges verticales plus homogènes et un profil plus strict avant animation.
- Marges verticales serrées, inférieures à6% demandés.
- Vue trois-quarts, pas un profil latéral strict.
- Validation de production du contour alpha et des détails fins encore nécessaire.
- Quelques pixels de faible alpha (1 à 16) atteignent le bord ; contrôler le bruit de détourage en composition.
- Marges inférieures à 2 % du canevas ou à 8 px : top.
- Validation de fidélité aux références du jeu
- Animations et déclinaisons
- Collisions et intégration au moteur

### Michael « Mickey » Crespo

- Fichier : [assets/characters_wave8/mickey_odst_initial_right_v01.png](../assets/characters_wave8/mickey_odst_initial_right_v01.png).
- SHA-256 : `8ded78a52c5db662362c34b1cf9bce1baeeb68c584746fdd7d0a6c0d21a4ed93`.
- Format : 1095 × 1437 px, RGBA, alpha [0, 255].
- Orientation observée : right_three_quarter.
- Sélection : préféré pour sa portée statique.
- Fidélité non certifiée ; aucune animation.

**Observations de QA :**

- Aperçu imagegen et PNG local via view_image inspectés individuellement : Mickey ODST2009 entier, casque, deux bottes et SPNKr complet visibles.
- Lampe à la tempe anatomique droite, bande crème de casque, bandes rouges d’épaule, sac rectangulaire et cylindres sur tibia droit concordent avec la référence.
- Deux mains visibles sur le lanceur et proportions humaines ; pose dirigée vers la droite mais torse encore en trois-quarts.
- Les microtextes du SPNKr sont partiellement déformés ; géométrie fine du double tube et surfaces occultées non certifiables depuis cette seule référence.
- Marges alpha54px en haut et48px en bas sur1437px, inférieures aux6% demandés ; fines franges colorées de détourage visibles par endroits.
- Inspection root individuelle du PNG et du rendu Bungie : personnage, deux pieds et SPNKr entiers ; orientation droite trois-quarts.
- Lampe de casque et cylindres du tibia du côté anatomique droit, sac et marques rouges globalement cohérents avec la référence.
- Image normalement lisible dans view_image côté root ; aucun pixel modifié.
- Mesure indépendante en lecture seule : 1095 × 1437 px, RGBA, alpha [0, 255], 1055635 pixels entièrement transparents. Marges au seuil alpha >16 : {'left': 149, 'top': 54, 'right': 114, 'bottom': 48}. Contacts du cadre : {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}.

**Suite requise :**

- Comparer les détails et marquages du SPNKr à des vues officielles supplémentaires.
- Prévoir profil strict, marges verticales homogènes et contrôle des contours alpha avant animation.
- Vue trois-quarts peu latérale.
- Petits marquages du SPNKr approximatifs et détails occultés à valider.
- Marges verticales54/48px inférieures aux6% demandés.
- Quelques pixels de faible alpha (1 à 16) atteignent le bord ; contrôler le bruit de détourage en composition.
- Validation de fidélité aux références du jeu
- Animations et déclinaisons
- Collisions et intégration au moteur

### Skirmisher Champion — classe Reach

- Fichier : [assets/characters_wave8/skirmisher_champion_reach_initial_right_v01.png](../assets/characters_wave8/skirmisher_champion_reach_initial_right_v01.png).
- SHA-256 : `31d782be78204694b4f1b66cc3459f18607925049e421efc2c23b145f75ab88d`.
- Format : 1165 × 1350 px, RGBA, alpha [0, 255].
- Orientation observée : right_three_quarter.
- Sélection : préféré pour sa portée statique.
- Fidélité non certifiée ; aucune animation.

**Observations de QA :**

- Un seul Skirmisher entier : haut de crête, plumage, deux bras, deux jambes et trois griffes visibles par pied ; pose tournée vers la droite en trois-quarts.
- Comparaison à la capture Reach : armure Champion or/ocre, haute crête, collerette sombre, grands épauliers et pistolet plasma compact conservés ; absence de bouclier rond et de boucliers de Murmillo.
- La tête et les talons restent dans le cadre, mais les marges mesurées ne sont que de 12 px en haut et 14 px en bas ; la marge confortable demandée n’est pas atteinte.
- La référence ne mesure que341×757px et coupe le haut de la crête : sommet, microgéométrie du pistolet, doigts et détails de plumes demeurent extrapolés. Quelques franges colorées du contour restent à vérifier sur les décors.
- Inspection individuelle root du PNG livré et de la petite référence canonique : silhouette entière, crête et pieds visibles, orientation droite trois-quarts.
- Armure or/ocre, plumage sombre, grande crête, protections de bras et pistolet correspondent globalement au Champion Reach.
- Image normalement lisible dans view_image côté root ; aucun pixel n’a été modifié.
- Mesure indépendante en lecture seule : 1165 × 1350 px, RGBA, alpha [0, 255], 1123077 pixels entièrement transparents. Marges au seuil alpha >16 : {'left': 107, 'top': 12, 'right': 151, 'bottom': 14}. Contacts du cadre : {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}.

**Suite requise :**

- Comparer casque/crête, arme et organisation des doigts à des vues Reach supplémentaires avant toute certification1:1.
- Produire une variante avec marges haut/bas plus homogènes et vue plus latérale si nécessaire ; ne pas modifier automatiquement les pixels ou retourner la silhouette.
- Valider les contours alpha en situation et créer les animations/directions séparément.
- Marges haut et bas très serrées.
- Référence de faible définition : microdétails et parties occultées extrapolés, pas de certification1:1.
- Vue trois-quarts, pas un profil latéral strict.
- Quelques pixels de faible alpha (1 à 16) atteignent le bord ; contrôler le bruit de détourage en composition.
- Marges inférieures à 2 % du canevas ou à 8 px : top, bottom.
- Validation de fidélité aux références du jeu
- Animations et déclinaisons
- Collisions et intégration au moteur

### Bassus

- Fichier : [assets/characters_wave8/bassus_infinite_initial_right_v01.png](../assets/characters_wave8/bassus_infinite_initial_right_v01.png).
- SHA-256 : `4657d0914ff9a93eb88b75fb684efc8921c3f3a325025cda65e9372f19f888dd`.
- Format : 1536 × 1024 px, RGBA, alpha [0, 254].
- Orientation observée : mostly_front_head_right.
- Sélection : préféré pour sa portée statique.
- Fidélité non certifiée ; aucune animation.

**Observations de QA :**

- Un seul Bassus entier, casque en éventail et pieds visibles ; un seul marteau complet tenu à deux mains. La tête vise la droite mais le torse reste proche de face, sans profil latéral strict.
- Comparaison aux références Infinite : casque or/rouge à crête centrale, barbe grise à attaches rouges, armure dorée et cramoisie, épauliers, brassards et grandes jambes cohérents globalement.
- La tête du marteau, ses modules lumineux et plusieurs microdétails sont reconstruits à partir de vues partielles ; ils ne sont pas certifiés identiques au modèle Infinite.
- Les marges alpha >16 ne sont que de 4 px en haut et 12 px en bas, sans contact direct avec les bords à ce seuil ; le cadrage reste trop serré pour une marge de production homogène.
- Le halo brun du preview correspond à des couleurs RGB cachées sous alpha 0 dans les points inspectés ; aucun fond opaque n’a été établi. La silhouette est conservée sans retouche.
- Inspection root individuelle du PNG et des deux références Bassus : corps, pieds, casque et marteau entiers ; tête vers la droite, torse proche frontal.
- Casque éventail rouge/or, barbe blanche, armure et parties visibles du marteau cohérents globalement ; géométrie fine du marteau et parties occultées non certifiées.
- Le PNG est normalement lisible côté root. Des échantillons du halo brun apparent ont alpha0 : aucune présence de fond opaque établie par ces mesures.
- Mesure indépendante en lecture seule : 1536 × 1024 px, RGBA, alpha [0, 254], 1046291 pixels entièrement transparents. Marges au seuil alpha >16 : {'left': 179, 'top': 4, 'right': 143, 'bottom': 12}. Contacts du cadre : {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}.

**Suite requise :**

- Reprendre le cadrage avec marges homogènes et une pose plus latérale lors d’une future variante, sans miroir horizontal.
- Comparer la géométrie de la tête du marteau, les prises des mains et les panneaux d’armure aux vues Infinite supplémentaires avant toute validation 1:1.
- Vérifier contours alpha en composition et produire les animations/directions séparément.
- Marges verticales4/12px très faibles.
- Torse proche frontal ; ce n’est pas une vue de profil strict.
- Le marteau complet est en partie reconstruit depuis références partiellement occultées ; microgéométrie à valider.
- Quelques pixels de faible alpha (1 à 16) atteignent le bord ; contrôler le bruit de détourage en composition.
- Marges inférieures à 2 % du canevas ou à 8 px : top, bottom.
- Validation de fidélité aux références du jeu
- Animations et déclinaisons
- Collisions et intégration au moteur


## 3. Cibles et résultats réels

| Cible | Objet | Appels | PNG | Résultats |
|---|---|---:|---:|---|
| Kelly-087 | Première image d’extension | 1 | 0 | moderation_blocked |
| Linda-058 | Première image d’extension | 1 | 0 | moderation_blocked |
| Jameson Locke | Première image d’extension | 1 | 1 | generated_candidate |
| Holly Tanaka | Première image d’extension | 1 | 0 | moderation_blocked |
| Veronica Dare | Première image d’extension | 1 | 0 | moderation_blocked |
| Kojo « Romeo » Agu | Première image d’extension | 1 | 0 | moderation_blocked |
| Michael « Mickey » Crespo | Première image d’extension | 1 | 1 | generated_candidate |
| Commandante Laurette Agryna | Première image d’extension | 1 | 0 | moderation_blocked |
| N’tho ’Sraom | Première image d’extension | 1 | 0 | moderation_blocked |
| Usze ’Taham | Première image d’extension | 1 | 0 | moderation_blocked |
| Let ’Volir | Première image d’extension | 1 | 0 | moderation_blocked |
| Skirmisher Champion — classe Reach | Première image d’extension | 1 | 1 | generated_candidate |
| Grunt Heavy — classe spécialisée Reach | Première image d’extension | 2 | 0 | reference_transport_closed, moderation_blocked |
| Pavium | Première image d’extension | 1 | 0 | moderation_blocked |
| Bassus | Première image d’extension | 1 | 1 | generated_candidate |
| Ur-Didact | Première image d’extension | 1 | 0 | moderation_blocked |
| Chevalier prométhéen — standard | Première image d’extension | 1 | 0 | moderation_blocked |
| Hieu Dinh | Correction des poches | 1 | 0 | moderation_blocked |
| John 117 le Major | Garde statique | 1 | 0 | moderation_blocked |

Une demande différée n’est pas comptée comme appel ni refus. Aucun prompt n’a été réécrit pour contourner les refus du service. La reprise du Grunt Heavy après l’erreur de transport utilise les mêmes entrées. Le premier appel avait bien invoqué image_gen avant son échec interne de lecture de référence ; il est compté comme appel technique réel, sans HTTP ni PNG.

## 4. Journal des appels

| Cible | Début UTC | Fin UTC | HTTP | Résultat |
|---|---|---|---:|---|
| Kelly-087 | 2026-11-20T08:14:08.633546+00:00 | 2026-11-20T08:16:10.831957+00:00 | 400 | moderation_blocked |
| Ur-Didact | 2026-11-20T08:17:04.263Z | 2026-11-20T08:18:55.087Z | 400 | moderation_blocked |
| Chevalier prométhéen — standard | 2026-11-20T08:17:04.264Z | 2026-11-20T08:18:07.953Z | 400 | moderation_blocked |
| John 117 le Major | 2026-11-20T08:21:02.076Z | 2026-11-20T08:22:38.947Z | 400 | moderation_blocked |
| Hieu Dinh | 2026-11-20T08:21:02.077Z | 2026-11-20T08:21:45.607Z | 400 | moderation_blocked |
| Linda-058 | 2026-11-20T08:16:41.191Z | 2026-11-20T08:18:20.228Z | 400 | moderation_blocked |
| Jameson Locke | 2026-11-20T08:16:41.192Z | 2026-11-20T08:17:34.549Z | — | generated_candidate |
| Holly Tanaka | 2026-11-20T08:20:42.660Z | 2026-11-20T08:22:05.360Z | 400 | moderation_blocked |
| Veronica Dare | 2026-11-20T08:20:42.660Z | 2026-11-20T08:21:29.034Z | 400 | moderation_blocked |
| Kojo « Romeo » Agu | 2026-11-20T08:22:50.635Z | 2026-11-20T08:26:22.610Z | 400 | moderation_blocked |
| Michael « Mickey » Crespo | 2026-11-20T08:22:50.636Z | 2026-11-20T08:24:34.469Z | — | generated_candidate |
| Commandante Laurette Agryna | 2026-11-20T08:28:28.331Z | 2026-11-20T08:29:18.364Z | 400 | moderation_blocked |
| N’tho ’Sraom | 2026-11-20T08:17:00.771Z | 2026-11-20T08:18:04.014Z | 400 | moderation_blocked |
| Usze ’Taham | 2026-11-20T08:17:00.771Z | 2026-11-20T08:18:58.382Z | 400 | moderation_blocked |
| Let ’Volir | 2026-11-20T08:19:22.470Z | 2026-11-20T08:20:24.314Z | 400 | moderation_blocked |
| Skirmisher Champion — classe Reach | 2026-11-20T08:19:22.470Z | 2026-11-20T08:21:15.636Z | — | generated_candidate |
| Grunt Heavy — classe spécialisée Reach | 2026-11-20T08:22:55.141Z | 2026-11-20T08:24:34.279Z | — | reference_transport_closed |
| Pavium | 2026-11-20T08:22:55.141Z | 2026-11-20T08:24:09.606Z | 400 | moderation_blocked |
| Bassus | 2026-11-20T08:25:54.081Z | 2026-11-20T08:26:45.373Z | — | generated_candidate |
| Grunt Heavy — classe spécialisée Reach | 2026-11-20T08:28:24.997Z | 2026-11-20T08:29:26.824Z | 400 | moderation_blocked |

Les heures sont explicitement en UTC. Les réponses brutes et références sont conservées dans les producteurs gelés. Le journal distingue réussite, modération, quota, erreur technique et report sans appel.

## 5. Intégration et conservation

Les nouveaux personnages d’extension sont consultables dans le **catalogue V8**, sans activation de leurs movesets en combat. L’entrée V8 réutilise les mécaniques et le style V7 ; son script est une copie minimale avec libellé et chemin de secours JSON V8. Le laboratoire, les bindings et les résultats V7 restent conservés. Le catalogue embarqué V8 et le JSON contiennent les mêmes données.

Les 34 extensions restent consultatives. Les 24 combattants de base, les 20 rencontres boss, les 24 décors et les systèmes de combat proposés restent les mêmes. Le Scarab reste la seule rencontre boss partielle ; les deux masters de décor restent des fonds en un plan.

La baseline est V7 `6c719b3041c04f75f7443135dd1b9f1d638bbe1d`, arbre `e1761c27d6e16eb78c34279be7aafec1d48efa27`, vérifiée sur 271 fichiers. Les 90 anciennes fiches d’art et PNG restent identiques. Seuls les champs d’art des entrées nouvellement illustrées évoluent : listes des images, candidat préféré et statut d’art. Les propositions de gameplay, sources et identités ne sont pas réécrites. Le Warden conserve son réemploi du PNG boss V5, sans duplication.

Les **118 échecs historiques** sont conservés ; **16 erreurs V8** sont ajoutées, soit **134** au total. Les 7 erreurs de quota V7 ne sont pas reclassées et l’échec technique V8 n’est pas compté comme refus de modération.

Un inventaire visuel V8 séparé présente l’état courant, afin de préserver les CSV historiques. Les 17 chemins propres à la publication restent exclus de l’import source : 15 fichiers historiques sont préservés et les deux index globaux sont recalculés.

## 6. Vérification et limites

Les contrôles ciblés du catalogue V8 consignent **38 réussites et 0 échec(s)** dans `prototype/qa_v8/results.json`. Ils vérifient les données et le chargement simulé ; ils ne constituent pas un examen des pixels dans un navigateur.

La vérification reconstruit les appels et la QA depuis les producteurs gelés, contrôle leurs SHA, les PNG et les préférences, puis protège tous les anciens fichiers hors registres courants autorisés. Les mesures alpha et de bord sont effectuées en lecture seule ; elles ne remplacent pas la comparaison visuelle aux références.

Les réserves de chaque candidat sont conservées, même lorsque le corps entier et le canal alpha sont présents. Le rendu navigateur interactif reste non observé après le refus de permission documenté en V7 ; aucun nouvel essai ou succès visuel n’est annoncé.

## 7. Travaux encore ouverts

**Premières images :** Kelly-087, Linda-058, Holly Tanaka, Veronica Dare, Kojo « Romeo » Agu, Commandante Laurette Agryna, N’tho ’Sraom, Usze ’Taham, Let ’Volir, Grunt Heavy — classe spécialisée Reach, Pavium, Ur-Didact, Chevalier prométhéen — standard.

**Correction :** Dinh. **Garde :** Major. Les animations, directions complémentaires, réglages compétitifs, movesets propres, narration jouable, tournoi, finishers et autres rencontres boss restent à produire.

Les prompts et références sont conservés pour les prochaines reprises demandées. Cette livraison ne programme aucun nouvel appel automatique.

## 8. Liens

- [Journal fusionné](../work/wave8/generation_results.json), [QA fusionnée](../work/wave8/qa_wave8.json), [reçus de gel](../work/wave8/producer_freeze_receipts.json).
- [Vérification](../work/wave8/verification.json), [manifeste](../data/asset_manifest.json), [compteurs](../data/delivery_counts.json).
- [Sources V8](SOURCES_PERSONNAGES_V8.md), [laboratoire V8](../prototype/halo_combats_lab_v8.html).
