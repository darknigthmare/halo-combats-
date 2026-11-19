# Références visuelles des boss — Vague V5

## Périmètre

Le registre contient 20 rencontres. Le Scarab Deutoros de Halo 3 possède déjà un candidat V2. Ce dossier prépare les 19 autres rencontres : **16 briefs permettent une génération candidate**, et **3 nécessitent encore une référence visuelle complète**. Une portée partielle est aussi documentée pour la biomasse murale de Cortana / High Charity ; elle ne remplace pas la référence complète manquante du Gravemind. Ces documents ne constituent pas des assets générés et ne changent pas le statut de validation du registre.

Les images de référence ont été téléchargées sans modification locale, puis examinées avec `view_image`. Les grands fichiers ont parfois été examinés via la miniature fournie par le site source ; l’original téléchargé est conservé avec son SHA-256. Aucune image source téléchargée n’est destinée à être ajoutée au dépôt. Le JSON contient les URL des pages et images, les dimensions, les empreintes, la provenance, les observations, les limites et les propositions de prompts.

- [Métadonnées et prompts des 19 rencontres](../work/wave5/boss_reference_briefs.json)
- Registre de référence : [data/bosses.json](../data/bosses.json)

`generated: false` qualifie chaque image de référence. `generation_ready: true` signifie seulement qu’un candidat peut être produit pour examen ; `certified_1_to_1` reste `false` partout.

## Tableau de préparation

| Rencontre | Version verrouillée | Références | Préparation |
|---|---|---:|---|
| Locust (`boss_locust_hw`) | Halo Wars — version Covenant originale | 3 | Candidate possible |
| Wraith paria (`boss_wraith_infinite`) | Halo Infinite — Wraith paria | 1 | Candidate possible |
| Banshee paria (`boss_banshee_infinite`) | Halo Infinite — Banshee paria | 3 | Candidate possible |
| Phantom paria (`boss_phantom_infinite`) | Halo Infinite — Phantom paria | 2 | Candidate possible |
| Phaeton (`boss_phaeton_h5`) | Halo 5: Guardians — Phaeton de base | 2 | Candidate possible |
| Harvester (`boss_harvester_h4`) | Halo 4 — Spartan Ops, capture MCC | 2 | Candidate possible |
| Lich (`boss_lich_h4`) | Halo 4 — Reclaimer | 1 | Candidate possible |
| Kraken (`boss_kraken_h5`) | Halo 5: Guardians — Enemy Lines | 4 | Candidate possible |
| Warden Eternal (`boss_warden_h5`) | Halo 5: Guardians | 1 | Candidate possible |
| Paire de Hunters du Cartographe (`boss_hunters_ce`) | Halo: Combat Evolved Classic — The Silent Cartographer | 2 | Candidate possible |
| Goliath (`boss_goliath_hw2`) | Halo Wars 2 — pack Colony | 2 | Candidate possible |
| Abomination du Flood (`boss_abomination_hw2`) | Halo Wars 2: Awakening the Nightmare | 1 | Candidate possible |
| Proto Gravemind (`boss_proto_gravemind_hw2`) | Halo Wars 2: Awakening the Nightmare — Manifestation | 1 | Référence complète requise |
| Juggernaut du Flood (`boss_juggernaut_ftr`) | Halo: Fireteam Raven | 1 | Candidate possible |
| Sentinelle Enforcer (`boss_enforcer_h2`) | Halo 2 Classic — Sacred Icon / Quarantine Zone | 1 | Candidate possible |
| Sentinelle Retriever (`boss_retriever_hw2`) | Halo Wars 2 | 1 | Candidate possible |
| Goblin piloté par un Grunt (`boss_goblin_h5`) | Halo 5: Guardians — Warzone Firefight | 2 | Candidate possible |
| Guardian de Halo 5 (`event_guardian_h5`) | Halo 5: Guardians — Guardian événementiel | 2 | Référence complète requise |
| Présence du Gravemind (`event_gravemind_h3`) | Halo 3 — présence du Gravemind, Cortana / High Charity | 3 | Module de biomasse possible ; silhouette complète non documentée |

## Verrous de silhouette et de version

Le Harvester H4 a six pattes, le Locust Halo Wars en a quatre, et le Kraken H5 utilise trois bras grappins. Ils demandent des silhouettes distinctes. Le Hunter du Cartographe est celui de Combat Evolved Classic ; un seul individu doit être produit par PNG, puis la rencontre peut utiliser deux instances. Le Goblin H5 conserve un canon à aiguilles et un poing sur deux bras différents, avec son pilote visible sous le dôme. Le Phaeton de base ne doit pas devenir un Helios.

Les rendus de l’Abomination HW2 et du Juggernaut Fireteam Raven ne sont pas interchangeables. L’Abomination est documentée par son apparence de jeu dans *Light the Fuse*, pour éviter la confusion avec le Gaunt de cinématique. Les véhicules parias d’Infinite restent liés à Infinite, même lorsqu’un véhicule de Halo Wars 2 partage un nom de famille.

## Trois besoins de référence encore ouverts

1. **Proto-Gravemind HW2 — Manifestation.** La capture prouve la masse émergée et ses tentacules, mais coupe plusieurs extrémités. Le livrable approprié est une structure enracinée et des modules de tentacules documentés ; aucun corps bipède ou souterrain ne doit être inventé.
2. **Guardian H5.** Les captures officielles et le fond d’écran coupent le bas ou les extrémités. Une vue authentique entière manque encore. Le fichier H5Guardian.png n’a pas été retenu en raison de son historique de rendus de fans contestés. L’entité reste un événement monumental de fuite et d’objectifs.
3. **Gravemind H3 — Cortana / High Charity.** Les tentacules trouvés sont ceux de la Citadelle dans *The Covenant*, tandis que l’autre image montre seulement un interlude en environnement Flood. Aucune n’autorise un corps complet ni un appendice complet situé dans la rencontre du registre. Une capture supplémentaire de *Cortana* documente des poches et membranes sur un mur de High Charity : un module de biomasse est possible avec `complete_silhouette: false`. Le besoin de corps ou d’appendice entier reste ouvert. La tête de Halo 2/H2A ne doit pas combler cette lacune.

## Sources et observations par rencontre

### Locust

Identifiant : `boss_locust_hw`. Version : **Halo Wars — version Covenant originale**.

Référence principale : [boss_locust_hw_reference.jpg](https://www.halopedia.org/File:HW_Locust_Render.jpg). Type : `official_game_website_render_rehosted`.

Origine ou page de provenance : https://web.archive.org/web/20110324040203/http://www.halowars.com/GameInfo/Factory.aspx

Rendu publié sur le site officiel Halo Wars, corroboré par une capture du jeu sur Chasms. Coque/canon violet allongé incliné vers l’avant, articulations mécaniques sombres, accents cyan, marcheur à quatre pattes.

**Limites.** Les références restent en trois quarts ; le nouveau détourage montre le flanc mais manque d’origine primaire détaillée. Le suffixe local side désigne une seconde vue frontale, pas un profil orthographique. Le modèle officiel et la capture en jeu corroborent le détourage ; conserver quatre pattes, jamais la variante paria HW2.

Références complémentaires :

- [boss_locust_hw_side_reference.png](https://www.halopedia.org/File:HW_Locust.png) — Capture en jeu de JackVibe, Chasms, publiée le 20 décembre 2023. Vue frontale en trois quarts du modèle du jeu. Limite : Le nom local side est historique ; il ne désigne pas une vue de profil.
- [boss_locust_hw_profile_reference.png](https://www.halopedia.org/File:HW-T30-Locust.png) — Rendu catégorisé Halo Wars sur Halopedia, recadré par Shazamikaze en 2014. Flanc oblique de la coque, canon et disposition des pattes. Limite : Origine primaire précise non renseignée ; à corroborer par le rendu officiel et le screenshot.

### Wraith paria

Identifiant : `boss_wraith_infinite`. Version : **Halo Infinite — Wraith paria**.

Référence principale : [boss_wraith_infinite_reference.jpg](https://www.halopedia.org/File:HINF_BanishedWraith_Render_1.jpg). Type : `developer_asset_render_rehosted`.

Origine ou page de provenance : https://www.artstation.com/artwork/LeZaGl

Rendu du modèle par Dan Sarkar, créateur de cet asset Infinite. Carrosserie rouge usée, plaques acier/noires, deux larges lobes latéraux, mortier dorsal et petite tourelle supérieure.

**Limites.** Présentation du modèle haute résolution ; comparer ensuite les détails au modèle en jeu. Angle trois quarts, pas une vue latérale ; conserver le Wraith Infinite plutôt que celui de HW2.

### Banshee paria

Identifiant : `boss_banshee_infinite`. Version : **Halo Infinite — Banshee paria**.

Référence principale : [boss_banshee_infinite_reference.png](https://www.halopedia.org/File:HINF_Banished_Banshee_Transparent.png). Type : `prerelease_reference_corroborated_by_released_campaign_screenshot`.

Vues de juin 2021 corroborées par une capture de la campagne publiée en janvier 2022, Annex Ridge. Même Banshee paria rouge/acier à coque compacte et ailes écartées ; les images montrent aussi la canopée ouverte.

**Limites.** Le Banshee d’Annex Ridge est partiellement masqué par des caisses ; la vue détourée apporte la silhouette. Pas de vue latérale orthographique complète de la campagne ; les détails du flanc opposé restent à vérifier. Le détourage de 2021 est fourni par un contributeur ; aucune modification locale des pixels.

Références complémentaires :

- [boss_banshee_infinite_game_reference.png](https://www.halopedia.org/File:HINF_BanishedBanshee.png) — Capture de TheArb1ter117, 14 juin 2021. Coque rouge et canopée ouverte. Limite : Source pré-sortie ; extrémités partiellement coupées.
- [boss_banshee_infinite_final_reference.png](https://www.halopedia.org/File:HINF-AnnexRidgeBanshee.png) — Capture de Sith Venator publiée le 16 janvier 2022. Le Banshee rouge final de la campagne corrobore les vues de 2021. Limite : Le véhicule est partiellement caché par les caisses ; référence de corroboration.

### Phantom paria

Identifiant : `boss_phantom_infinite`. Version : **Halo Infinite — Phantom paria**.

Référence principale : [boss_phantom_infinite_reference.png](https://www.halopedia.org/File:HINF_Phantom.png). Type : `game_screenshots_rehosted`.

Vue de dessous de la campagne présentée en 2021, complétée par une capture du modèle en Forge Firefight en 2023. Coque paria rouge/noire très anguleuse, pointe centrale de nez, nacelles latérales et canon ventral.

**Limites.** La vue de 2023 provient de Forge et non d’une mission de campagne ; elle renseigne le modèle du véhicule. Aucun profil orthographique ; petites pièces ventrales et flanc opposé restent à vérifier. Ne pas substituer le Phantom HW2 malgré le nom de famille partagé.

Références complémentaires :

- [boss_phantom_infinite_side_reference.png](https://www.halopedia.org/File:HINF_Phantom_1.png) — Capture de JackVibe, 25 décembre 2023. Vue entière du modèle paria rouge/noir/acier, en trois quarts. Limite : La scène vient de Forge ; ne pas la décrire comme une capture de mission de campagne.

### Phaeton

Identifiant : `boss_phaeton_h5`. Version : **Halo 5: Guardians — Phaeton de base**.

Référence principale : [boss_phaeton_h5_reference.png](https://www.halopedia.org/File:H5G-Phaeton.png). Type : `game_cutout_plus_developer_sculpt`.

Origine ou page de provenance : https://www.artstation.com/artwork/Xdwg0

Capture détourée H5, corroborée par le modèle haute résolution de Dan Sarkar. Corps gris clair effilé, deux ensembles circulaires latéraux, ouvertures mécaniques et lueurs orange.

**Limites.** La capture détourée ne renseigne pas sa provenance primaire ; le sculpt confirme la géométrie mais pas les textures. Le Phaeton Helios est une variante différente à exclure.

Références complémentaires :

- [boss_phaeton_h5_sculpt_reference.jpg](https://www.halopedia.org/File:H5G_-_Phaeton_hig-res_model.jpg) — Dan Sarkar, ArtStation Xdwg0. Dessus et trois quarts du modèle avec ses deux ensembles circulaires. Limite : Sans textures ; la capture du jeu doit donner les couleurs.

### Harvester

Identifiant : `boss_harvester_h4`. Version : **Halo 4 — Spartan Ops, capture MCC**.

Référence principale : [boss_harvester_h4_reference.jpg](https://www.halopedia.org/File:HTMCC_H4_Harvester_Screenshot_Side.jpg). Type : `game_screenshot_plus_developer_sculpt`.

Origine ou page de provenance : https://www.artstation.com/artwork/RnY4D

Vue en jeu de H4 Spartan Ops portée dans MCC ; géométrie corroborée par le sculpt de Kolby Jukes. Immense carapace organique métallique sombre, six longues pattes et assemblage de forage central.

**Limites.** Le screenshot coupe les extrémités ; le sculpt entier en quatre vues complète la structure. Le sculpt est gris et ne documente pas les textures ; reprendre les matériaux du jeu, sans recoloration arbitraire. L’éclairage verdâtre du niveau influence la couleur apparente.

Références complémentaires :

- [boss_harvester_h4_sculpt_reference.jpg](https://www.halopedia.org/File:Harvester_Sculpt.jpg) — Kolby Jukes, ArtStation RnY4D. Quatre vues du sculpt montrant la géométrie entière et les six pattes. Limite : Sculpt gris ; les textures finales ne sont pas documentées par cette image.

### Lich

Identifiant : `boss_lich_h4`. Version : **Halo 4 — Reclaimer**.

Référence principale : [boss_lich_h4_reference.png](https://www.halopedia.org/File:H4IG_-_Lich.png). Type : `official_interactive_guide_rehosted`.

Origine ou page de provenance : https://www.halopedia.org/Halo_4_Interactive_Guide

Capture du guide interactif promotionnel Halo 4, section véhicule Lich. Coque Covenant violette bombée, longues pointes/mandibules avant et ventre sombre mécanique.

**Limites.** Le fichier source est une capture du guide ; le vaisseau occupe seulement une partie des 1170×385 pixels. Source primaire historique Halo Waypoint dépubliée ; pas de référence latérale haute résolution. La variante paria de HW2 et le Lich de cinématique H2A ne sont pas les sources retenues.

### Kraken

Identifiant : `boss_kraken_h5`. Version : **Halo 5: Guardians — Enemy Lines**.

Référence principale : [boss_kraken_h5_reference.jpg](https://www.halopedia.org/File:H5G_PK_KrakenAssault_Screenshot.jpg). Type : `official_press_screenshots_plus_official_book_render_and_developer_concept`.

Origine ou page de provenance : https://web.archive.org/web/20151021011231/https://www.halowaypoint.com/en-us/games/halo-5-guardians

Captures officielles Enemy Lines corroborées par un rendu entier de Halo Encyclopedia 2022 et les vues concept de Shae Shatz pour H5. Tour de siège volante à TROIS bras grappins, grande coque sommitale, section centrale ouverte et détails cyan.

**Limites.** Le rendu entier provient de l’encyclopédie, pas d’une extraction directe du jeu ; les captures H5 servent à vérifier les matériaux et volumes. Les vues de Shae Shatz sont du concept art ; elles confirment la disposition générale, sans certifier chaque détail final. Le profil latéral exact et la séparation des trois bras devront être contrôlés après génération.

Références complémentaires :

- [boss_kraken_h5_full_reference.jpg](https://www.halopedia.org/File:H5G-KrakenonEnemyLines.jpg) — Kit de presse Halo Waypoint, capture Enemy Lines. Vue générale du Kraken avec matériaux et proportions du jeu. Limite : Sommet coupé et certains bras masqués.
- [boss_kraken_h5_book_reference.png](https://www.halopedia.org/File:Enc22_Kraken.png) — Halo Encyclopedia (édition 2022), rendu extrait et détouré par le réhébergeur. Silhouette entière de la tour avec les trois bras rapprochés. Limite : Référence de livre, pas capture de gameplay H5 ; silhouette frontale encore à tourner pour un profil.
- [boss_kraken_h5_ortho_reference.jpg](https://www.halopedia.org/File:H5G_Kraken_Ortho_Concept.jpg) — Shae Shatz, site portfolio archivé. Vues de face et trois quarts de la structure à trois bras. Limite : Concept art ; ne pas transférer ses détails non corroborés au modèle final.

### Warden Eternal

Identifiant : `boss_warden_h5`. Version : **Halo 5: Guardians**.

Référence principale : [boss_warden_h5_reference.png](https://www.halopedia.org/File:H5G_Warden_render.png). Type : `official_press_render_rehosted`.

Origine ou page de provenance : https://web.archive.org/web/20150629031730/https://www.halowaypoint.com/en-us/games/halo-5-guardians/xbox-one

Corps humanoïde Forerunner argenté et noir, segments d’armure flottants ou séparés, accents ambre, grande arme lumineuse orange. Silhouette entière visible : tête à large couronne, deux jambes à pieds segmentés, deux bras ; pose dynamique en trois quarts. Rendu du kit de presse H5 explicitement identifié par la page source.

**Limites.** Le rendu n’est pas un profil orthographique ; un profil strict nécessite une seconde vue. Effets de lumière étendus autour du corps ; ne pas transformer ces halos en appendices. La page signale une modification historique du cadrage ; téléchargement local conservé sans modification. Ne pas utiliser les couleurs ou accessoires du Mythic Warden.

### Paire de Hunters du Cartographe

Identifiant : `boss_hunters_ce`. Version : **Halo: Combat Evolved Classic — The Silent Cartographer**.

Référence principale : [boss_hunters_ce_reference.png](https://www.halopedia.org/File:HCE-IgidoOgado.png). Type : `exact_encounter_screenshot_plus_game_cutout`.

Capture du duo nommé Igido Nosa Hurru et Ogada Nosa Fasu au Cartographe, corroborée par un modèle Classic entier détouré. Armure bleue simple, chair Lekgolo orange visible, grands piquants dorsaux, bouclier sombre et canon violet/vert.

**Limites.** La capture entière isolée manque d’origine primaire détaillée ; correspondance visuelle vérifiée avec la scène documentée. Ne pas confondre Classic avec Anniversary ou Campaign Evolved. Un seul Hunter par image : la rencontre utilise deux instances ; le nombre de boss du registre reste un.

Références complémentaires :

- [boss_hunters_ce_full_reference.png](https://www.halopedia.org/File:HCE-MgalekgoloHunterAlt.png) — Capture détourée réhébergée, recadrage Shazamikaze en 2013. Un Hunter entier en garde, bouclier et canon asymétriques, pieds et épines contenus. Limite : Provenance primaire incomplète ; vérifiée contre le duo documenté du Cartographe.

### Goliath

Identifiant : `boss_goliath_hw2`. Version : **Halo Wars 2 — pack Colony**.

Référence principale : [boss_goliath_hw2_reference.jpg](https://www.halopedia.org/File:HW2_PK_Colony_Goliaths_1.jpg). Type : `official_press_screenshot_plus_official_blitz_art`.

Origine ou page de provenance : https://www.xbox.com/en-GB/games/store/colony-leader-pack/9NBLGGH4TQNR/0010

Capture officielle du pack Colony et illustration Blitz par Luke Kopycinski publiée sur Halo Waypoint. Énorme masse Lekgolo penchée vers l’avant, armure rouge/acier, grands pics dorsaux, lueurs vertes et lourds membres de mêlée.

**Limites.** Les unités de la capture sont petites ; l’illustration Blitz apporte des détails mais ne remplace pas le modèle 3D final. La source illustrée montre un Marine saisi : le futur asset doit contenir le Goliath seul. Ne pas reprendre le canon du Hunter Captain.

Références complémentaires :

- [boss_goliath_hw2_blitz_reference.jpg](https://www.halopedia.org/File:HW2_-_Goliath.jpg) — Luke Kopycinski ; portfolio et Halo Waypoint Leggo My Lekgolo. Détails illustrés du Goliath rouge/acier, masses Lekgolo et pics dorsaux. Limite : Illustration de carte Blitz, pas vue technique du modèle ; Marine de la scène à exclure.

### Abomination du Flood

Identifiant : `boss_abomination_hw2`. Version : **Halo Wars 2: Awakening the Nightmare**.

Référence principale : [boss_abomination_hw2_reference.png](https://www.halopedia.org/File:HW2_FloodAbomination_Profile.png). Type : `game_screenshot_rehosted`.

Origine ou page de provenance : https://www.halopedia.org/File:HW2_FloodAbomination_Profile.png

Capture du modèle de jeu dans Light the Fuse, attribuée à JackVibe sur Halopedia. Masse supérieure bombée couverte de poches jaunes, tissus fibreux sombres et rouges, bras allongés et jambes ployées. Profil presque latéral utile pour conserver la silhouette du modèle RTS.

**Limites.** Vue de dessus oblique RTS, arrière partiellement masqué. Flammes, ombre et débris du niveau ne font pas partie du boss. Ne pas confondre avec le Gaunt de cinématique ni avec le Juggernaut Fireteam Raven ; les rendus Flood Commander peuvent représenter une autre variante. L’articulation la plus lointaine est partiellement cachée : contrôle complémentaire avant validation 1:1.

### Proto Gravemind

Identifiant : `boss_proto_gravemind_hw2`. Version : **Halo Wars 2: Awakening the Nightmare — Manifestation**.

Référence principale : [boss_proto_gravemind_hw2_reference.png](https://www.halopedia.org/File:HW2_LargeProtoGravemind.png). Type : `game_screenshot_rehosted`.

Capture explicite de Manifestation : énorme masse Flood émergée du sol avec plaques charnues et core frontal. Des tentacules distincts émergent autour du corps ; absence de silhouette de bipède.

**Limites.** Plusieurs tentacules et le haut de la masse dépassent du cadre ; une base souterraine n’est pas observable. Ne pas fabriquer de jambes ou un corps libre portant la tête du Gravemind H2. Le livrable adapté sera la masse exposée et des modules de tentacules, après références complètes de chaque module.

### Juggernaut du Flood

Identifiant : `boss_juggernaut_ftr`. Version : **Halo: Fireteam Raven**.

Référence principale : [boss_juggernaut_ftr_reference.png](https://www.halopedia.org/File:HFR_Juggernaught_Render_2.png). Type : `official_press_render_rehosted`.

Origine ou page de provenance : https://www.halowaypoint.com/en-us/forums/92f069f023a1483db48c88ce05eb4ccf/topics/halo-fireteam-raven-community-content-care-pack/f38ead46-d2bd-4813-9ef3-7dd1f8c82ccf/posts

Rendu explicitement issu du kit officiel Fireteam Raven, nom original FireteamRaven_Render_FloodJuggernaut_Pose.png. Corps massif bulbeux chair brune pâle, deux grandes jambes digitigrades terminées par des pieds larges. Deux longs appendices fouets latéraux à extrémités sombres pointues ; tête intégrée à la masse et côtes fibreuses visibles.

**Limites.** Rendu frontal en trois quarts ; le flanc caché n’est pas documenté. Ne pas utiliser le prototype coupé de Halo 2 ni l’Abomination de Halo Wars 2. Conserver l’intégralité des fouets, sans agrandir artificiellement leurs pointes.

### Sentinelle Enforcer

Identifiant : `boss_enforcer_h2`. Version : **Halo 2 Classic — Sacred Icon / Quarantine Zone**.

Référence principale : [boss_enforcer_h2_reference.png](https://www.halopedia.org/File:H2_Sentinel_Enforcer_AngleView.png). Type : `game_screenshot_rehosted`.

Capture explicitement identifiée Halo 2, Sacred Icon ; silhouette anguleuse Classic. Drone flottant gris/brun, grande coque centrale, bras-pinces inférieurs et double protection énergétique frontale.

**Limites.** Les effets lumineux masquent partiellement la face et les émetteurs. Ne pas mélanger les panneaux de l’Enforcer H2 Anniversary ; un profil propre reste à contrôler.

### Sentinelle Retriever

Identifiant : `boss_retriever_hw2`. Version : **Halo Wars 2**.

Référence principale : [boss_retriever_hw2_reference.jpg](https://www.halopedia.org/File:HW2-Retriever.jpg). Type : `developer_asset_screenshot_rehosted`.

Origine ou page de provenance : https://www.artstation.com/artwork/96q8a

Modèle en jeu présenté par son créateur Gerard Muntés ; matériaux et shaders attribués à l’équipe environnement. Sentinelle volante : deux grandes surfaces latérales segmentées, corps central allongé et plusieurs appendices mécaniques inférieurs ; accents cyan.

**Limites.** Vue oblique de dessus, arrière caché ; aucune vue de profil orthographique. Ne pas utiliser les captures HW2 du design préliminaire signalé PRD.

### Goblin piloté par un Grunt

Identifiant : `boss_goblin_h5`. Version : **Halo 5: Guardians — Warzone Firefight**.

Référence principale : [boss_goblin_h5_reference.png](https://www.halopedia.org/File:H5G_-_Goblin_render.png). Type : `game_render_corroborated_by_official_xbox_screenshot`.

Origine ou page de provenance : https://news.xbox.com/en-us/2016/06/29/warzone-firefight-available-now-halo-5-guardians-download-halo-5-guardians-free-today/

Rendu catégorisé Halo 5: Guardians et Pnap-pattern Goblin par Halopedia. Mech bipède violet avec pilote Unggoy visible derrière un dôme frontal bleu ; canon à aiguilles sur un bras et gros poing sur l’autre. Deux jambes mécaniques courtes et larges ; épaulière volumineuse et plusieurs ouvertures dorsales. Une capture primaire Xbox Wire du 29 juin 2016 corrobore le design et l’asymétrie du mech.

**Limites.** Origine précise du rendu détouré non indiquée, mais silhouette et équipement corroborés par la capture officielle Xbox. Le cadre touche les pieds, donc vérifier le rendu final avec une marge complète. Vue en trois quarts ; ne pas certifier un profil 1:1 sur cette seule référence. Ne pas confondre le mech Goblin avec l’armure MJOLNIR Goblin ou la variante Temple.

Références complémentaires :

- [boss_goblin_h5_xbox_reference.jpg](https://news.xbox.com/en-us/2016/06/29/warzone-firefight-available-now-halo-5-guardians-download-halo-5-guardians-free-today/) — Microsoft / 343 Industries, Xbox Wire, 29 juin 2016. Capture officielle entière du mech et de ses deux bras asymétriques. Limite : Éclairage extérieur et sol masquant une partie des pieds.

### Guardian de Halo 5

Identifiant : `event_guardian_h5`. Version : **Halo 5: Guardians — Guardian événementiel**.

Référence principale : [event_guardian_h5_reference.jpg](https://www.halopedia.org/File:H5G-Battle_of_Sunaion-Guardian_rising.jpg). Type : `official_press_screenshot_plus_waypoint_wallpaper`.

Origine ou page de provenance : https://web.archive.org/web/20150907043849/https://www.halowaypoint.com/en-us/games/halo-5-guardians

Capture officielle Battle of Sunaion et fond d’écran attribué à Halo Waypoint. Structure Forerunner colossale au centre vertical, larges éléments latéraux séparés et sources cyan.

**Limites.** Les deux sources coupent le bas ou les extrémités ; elles ne prouvent pas une silhouette entière. Le fichier H5Guardian.png a un historique de rendus de fans contestés ; il n’est pas retenu comme référence fiable. Boss événement : échelle monumentale en arrière-plan et fuite/objectifs, sans inventer un duel à points de vie.

Références complémentaires :

- [event_guardian_h5_wallpaper_reference.jpg](https://www.halopedia.org/File:Halo_5_-_Guardian_wallpaper.jpg) — Attribué à Halo Waypoint par le réhébergeur ; URL primaire historique non détaillée. Large vue de face des structures latérales et du centre du Guardian. Limite : Bas et extrémités coupés ; ne suffit pas à une silhouette complète.

### Présence du Gravemind

Identifiant : `event_gravemind_h3`. Version : **Halo 3 — présence du Gravemind, Cortana / High Charity**.

Référence principale : [event_gravemind_h3_reference.jpg](https://www.halopedia.org/File:GravemindMainTentaclesHalo3.jpg). Type : `game_context_screenshots_rehosted`.

La capture de tentacules montre la Citadelle de The Covenant ; elle confirme le matériau H3, pas la scène Cortana. La vue d’interlude montre un environnement Flood de Halo 3 ; aucun corps complet du Gravemind n’y apparaît. Une capture de Cortana, attribuée à Dragonclaws et publiée le 15 octobre 2010, montre des poches organiques et membranes sur un mur de High Charity. Elle permet uniquement de préparer un module de biomasse murale.

**Limites.** La première image ne correspond pas au lieu du registre ; usage contexte seulement. Aucune référence suffisante à un corps entier ou à un tentacule complet de Cortana retrouvée dans ce lot. Ne pas importer la tête H2/H2A ni transformer l’événement en monstre bipède.

Références complémentaires :

- [event_gravemind_h3_interlude_reference.jpg](https://www.halopedia.org/File:Gravemind_Halo3.jpg) — Capture réhébergée sur Halopedia, détails de prise de vue non renseignés. Environnement infesté et effet d’interlude ; aucun corps du Gravemind visible. Limite : Seulement une référence de contexte ; ne permet pas de dessiner un tentacule complet.

- [event_gravemind_h3_cortana_biomass_reference.jpg](https://www.halopedia.org/File:Flood_wall.jpg) — Capture de Cortana / High Charity, Dragonclaws, 15 octobre 2010. Poches brunes et membranes fibreuses d’un mur infesté. Limite : aucun corps complet ni tentacule entier ; portée `environmental_biomass_module`, `complete_silhouette: false`, sans certification 1:1.

## Règle de génération

Le prompt de chaque entrée demande un seul sujet entier, sur fond transparent, orienté vers la gauche, avec marge pour les pieds, pics, ailes et armes. Une légère vue en trois quarts peut rester nécessaire lorsque les références ne documentent pas un profil strict. Les poses et le cadrage proposés sont des choix d’adaptation 2D ; les zones non observées restent à vérifier. Aucune certification 1:1, animation, collision ou intégration moteur ne découle de ces briefs.

La portée partielle du module de biomasse de Cortana constitue une exception explicite au cadrage d’un sujet complet : seule la surface organique observée peut être adaptée, sans inventer son prolongement ni la présenter comme le corps du Gravemind. Le JSON conserve `generation_ready: false` pour la silhouette complète et décrit séparément cette portée partielle.
