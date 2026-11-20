# Halo Combats — inventaire des personnages, vague 2

Mise à jour : 2026-11-19T17:06:50+00:00.

## Résultat de l'inventaire

Le roster contient **24 combattants distincts**. **9 personnages disposent d'au moins une pose candidate**, pour 9 fichiers candidats référencés. **15 personnages restent sans pose candidate.**

Cette consolidation ajoute 8 fichiers candidats pour 8 personnages. Le journal comporte 33 tentative(s) en échec et 0 entrée(s) identique(s) ignorée(s). Les échecs précédents restent conservés dans le manifeste comme historique.

La vague 2 compte au total 8 poses candidates pour 8 personnages.

Les PNG sont copiés sans modification. La présence d'une pose ne signifie pas qu'un personnage est entièrement produit : les animations, les sprites d'attaque, les collisions, l'intégration et la validation comparative de fidélité restent à réaliser selon les statuts du manifeste.

**Fichiers combattants certifiés : 0. Animés : 0. Intégrés : 0.** Aucune certification de fidélité 1:1 n'est déduite de la seule génération.

Le journal comporte **41 tentatives pour 23 personnages distincts** : 8 tentatives réussies et 33 échecs. Un même personnage peut avoir plusieurs tentatives ; seul l'inventaire des fichiers réellement produits détermine sa couverture visuelle.

## Personnages encore sans image candidate

- **John 117 le Major** — `chief_infinite`.
- **Avery Johnson** — `johnson_h3`.
- **Noble Six** — `noble_six`.
- **Emile A239** — `emile_reach`.
- **Jorge 052** — `jorge_reach`.
- **Jun A266** — `jun_reach`.
- **Kat B320** — `kat_reach`.
- **Carter A259** — `carter_reach`.
- **Le Rookie** — `rookie_odst`.
- **Tartarus** — `tartarus_h2`.
- **Escharum** — `escharum_infinite`.
- **Jega 'Rdomnai** — `jega_infinite`.
- **Chak 'Lok** — `chak_lok`.
- **Alice 130** — `alice_hw2`.
- **Douglas 042** — `douglas_hw2`.

## Couverture du roster

| Personnage | ID | Poses candidates | Variante la plus récente | Contrôle visuel |
|---|---|---:|---|---|
| John 117 le Major | `chief_infinite` | 0 | Aucune image | Génération non obtenue |
| Thel 'Vadam l’Arbiter | `arbiter_h3` | 1 | Pose candidate | QA antérieure à poursuivre |
| Avery Johnson | `johnson_h3` | 0 | Aucune image | Génération non obtenue |
| Noble Six | `noble_six` | 0 | Aucune image | Génération non obtenue |
| Emile A239 | `emile_reach` | 0 | Aucune image | Génération non obtenue |
| Jorge 052 | `jorge_reach` | 0 | Aucune image | Génération non obtenue |
| Jun A266 | `jun_reach` | 0 | Aucune image | Génération non obtenue |
| Kat B320 | `kat_reach` | 0 | Aucune image | Génération non obtenue |
| Carter A259 | `carter_reach` | 0 | Aucune image | Génération non obtenue |
| Edward Buck ODST | `buck_odst` | 1 | Référence neutre sans arme | Inspection V2 avec réserves |
| Le Rookie | `rookie_odst` | 0 | Aucune image | Génération non obtenue |
| Rtas 'Vadum | `rtas_h3` | 1 | Référence neutre sans arme | Inspection V2 avec réserves |
| Tartarus | `tartarus_h2` | 0 | Aucune image | Génération non obtenue |
| Atriox | `atriox_hw2` | 1 | Pose candidate | Inspection V2 avec réserves |
| Decimus | `decimus_hw2` | 1 | Pose candidate | Inspection V2 avec réserves |
| Escharum | `escharum_infinite` | 0 | Aucune image | Génération non obtenue |
| Jega 'Rdomnai | `jega_infinite` | 0 | Aucune image | Génération non obtenue |
| Chak 'Lok | `chak_lok` | 0 | Aucune image | Génération non obtenue |
| Alice 130 | `alice_hw2` | 0 | Aucune image | Génération non obtenue |
| Douglas 042 | `douglas_hw2` | 0 | Aucune image | Génération non obtenue |
| Jerome 092 | `jerome_hw2` | 1 | Pose candidate | Inspection V2 avec réserves |
| Elite Zealot | `zealot_reach` | 1 | Référence neutre sans arme | Inspection V2 avec réserves |
| Cethegus chef Brute | `cethegus_h3` | 1 | Pose candidate | Inspection V2 avec réserves |
| Mgalekgolo Hunter | `hunter_h3` | 1 | Pose candidate | Inspection V2 avec réserves |

## Observations sur les personnages illustrés

### Thel 'Vadam l’Arbiter

Fichier : `assets/candidates/arbiter_halo3_neutral_right_v2.png`. Dimensions : 1024 × 1536 px ; mode RGBA. Statut : candidat, fidélité non certifiée.

- Pose neutre candidate. Fond alpha présent mais halo périphérique à contrôler. Orientation trois quarts trop marquée pour frame latérale finale. Armure et mandibules à comparer au modèle Halo 3.

### Edward Buck ODST

Fichier : `assets/characters_wave2/buck_odst_neutral_right_v01.png`. Dimensions : 1024 × 1536 px ; mode RGBA. Statut : candidat, fidélité non certifiée.

- Un ODST au gabarit humain, casque fermé à visière bleu-argent, armure gris anthracite et poches textiles, debout avec les deux mains vides. Tête, mains et bottes complètes dans le cadre. La pose calme sans arme sert de référence de personnage, pas de garde de combat.
- La vue est principalement latérale vers la droite avec une légère rotation du buste. Le module radio sur le côté anatomiquement droit du casque paraît respecté. Le couteau de torse mentionné parmi les verrous de Buck n’est pas clairement identifiable sur ce plastron : l’équipement distinctif complet reste à vérifier.
- Marges verticales modestes de 30 px en haut et de 27 px en bas au seuil alpha >16 ; marges latérales larges de 291 et 320 px. Aucun contact direct alpha >16 avec le cadre ; seuls 7 pixels de faible alpha atteignent le bord gauche.
- PNG RGBA 1024 × 1536, alpha 0 à 254, avec 1162970 pixels entièrement transparents. Le halo gris de l’aperçu contient des points alpha 0 ; il ne prouve pas un fond opaque. Les 15512 pixels alpha 1 à 16 et les contours restent à vérifier en composition.
- Les formes exactes du casque, du CNM, du plastron et des petits marquages doivent être comparées au Buck de Halo 3 ODST 2009 pour le distinguer d’un ODST générique.

### Rtas 'Vadum

Fichier : `assets/characters_wave2/rtas_h3_neutral_right_v01.png`. Dimensions : 1145 × 1374 px ; mode RGBA. Statut : candidat, fidélité non certifiée.

- Rtas est présenté debout, calme, les deux mains vides et relâchées, avec armure blanche, sous-couche sombre et jambes digitigrades. Les mains, les pieds et le casque sont dans le cadre. Cette variante est une référence neutre sans arme, pas une garde de combat ni une animation.
- La direction vers la droite et l’orientation plus latérale sont lisibles, avec une rotation encore visible du buste. Le côté et la perspective du visage ne permettent pas de confirmer clairement l’absence des deux mandibules gauches ; ce trait distinctif de Half-Jaw reste à vérifier sur une vue adaptée.
- Marge haute de 9 px au seuil alpha > 16 : casque trop proche du cadre. Marges gauche/droite 279/349 px et marge basse 31 px. Aucun contact alpha >16 ; 148 pixels de faible alpha atteignent le bord supérieur.
- PNG RGBA 1145 × 1374, alpha 0 à 255, avec 1166249 pixels entièrement transparents. L’aperçu présente des résidus blancs/gris au-dessus du casque et sur certains contours ; les points échantillonnés ont alpha 0 à 4. Ils ne constituent pas un fond blanc opaque, mais le détourage de production reste à nettoyer/valider.
- Le modèle d’armure Assault Halo 3, le casque et le visage doivent être comparés aux références de Rtas ; aucune fidélité 1:1 n’est certifiée.

### Atriox

Fichier : `assets/characters_wave2/atriox_hw2_neutral_right_v01.png`. Dimensions : 1536 × 1024 px ; mode RGBA. Statut : candidat, fidélité non certifiée.

- Personnage, deux pieds et tête complète de Chainbreaker visibles. Trois pointes distinctes et énergie rouge visibles ; armure claire asymétrique, tresses et gantelet volumineux cohérents avec le brief, sans certification comparative au modèle officiel.
- Pose nettement de trois quarts : la poitrine reste très exposée face à la caméra. Le gantelet anatomiquement droit paraît à gauche de l’image ; il saisit la hampe au lieu d’être avancé seul en garde. L’arme est presque horizontale.
- Cadrage serré : la boîte alpha > 16 ne laisse que 6 px en haut, 6 px en bas et 17 px à droite. Aucune silhouette ne touche cependant directement le bord à ce seuil.
- Un halo gris/noir est visible dans l’aperçu RGB. Les points de fond échantillonnés dans ce halo ont pourtant alpha 0 ; il serait inexact de qualifier tout ce halo de fond opaque. Le fichier possède 855654 pixels alpha 0 et 41981 pixels alpha 1 à 16. La propreté du contour en composition réelle reste à contrôler.

### Decimus

Fichier : `assets/characters_wave2/decimus_hw2_neutral_right_v01.png`. Dimensions : 1536 × 1024 px ; mode RGBA. Statut : candidat, fidélité non certifiée.

- Exosquelette très volumineux rouge et métal sombre, visage dégagé et cheveux blancs visibles. Deux mains mécaniques tiennent une seule arme gravitationnelle complète à énergie rouge ; les pieds et le sommet de l’exosquelette restent dans le cadre. Aucun bras-canon distinct n’est ajouté de façon évidente.
- Vue nettement de trois quarts, poitrine très visible, avec arme tenue presque horizontalement. Les détails de visage, d’armature, de vérins, de plaques et de tête d’arme demandent une comparaison au modèle de gameplay final Halo Wars 2.
- Marges serrées au seuil alpha > 16 : 5 px en haut, 9 px en bas et 14 px à droite de l’arme. Aucun contact direct alpha >16, mais de faibles valeurs alpha 1 à 16 atteignent les bords gauche, haut et bas.
- PNG RGBA 1536 × 1024, alpha 0 à 254, avec 745563 pixels entièrement transparents. Des points gris/rouges du halo visible dans l’aperçu ont alpha 0 ; ce halo RGB ne prouve pas un fond opaque. Les 35114 pixels alpha 1 à 16 et les contours sont à contrôler en composition.
- Le rendu reste une pose candidate : les dimensions du personnage, les raccords mécaniques et l’identité précise de l’arme ne sont pas certifiés 1:1.

### Jerome 092

Fichier : `assets/characters_wave2/jerome_hw2_neutral_right_v01.png`. Dimensions : 1199 × 1312 px ; mode RGBA. Statut : candidat, fidélité non certifiée.

- Armure vert olive, visière dorée, bande rouge sur le plastron, inscription 092 et losange rouge visibles. Une seule arme lourde tenue à deux mains ; corps, pieds et extrémité du canon dans le cadre. Aucun membre supplémentaire évident dans cette vue.
- Vue de trois quarts prononcée, avec un plastron presque frontal : elle reste à remplacer ou valider pour le profil latéral du jeu de combat. La pose statique ne représente pas un moveset animé.
- Casque très proche du bord supérieur : marge de 7 px au seuil alpha > 16. Les pieds laissent 14 px en bas. Aucun pixel de contenu alpha > 16 ne touche directement un bord ; une coupe effective du casque ne peut donc pas être affirmée sur ce seul contrôle.
- PNG RGBA 1199 × 1312, alpha 0 à 255, avec 1023210 pixels entièrement transparents. Les éventuelles franges visibles dans l’aperçu doivent être vérifiées en composition ; le contour n’est pas certifié propre.
- La géométrie exacte du casque Mark IV, des plaques, des marquages et du Spartan Laser demande une comparaison aux références Halo Wars 2.

### Elite Zealot

Fichier : `assets/characters_wave2/zealot_reach_neutral_right_v01.png`. Dimensions : 1199 × 1312 px ; mode RGBA. Statut : candidat, fidélité non certifiée.

- Sangheili debout avec armure bordeaux/rouge sombre, épaules et casque pointus, jambes digitigrades et mains vides. Le casque, les deux mains et les deux pieds sont dans le cadre. Aucun équipement ou membre supplémentaire évident.
- Pose calme de référence, orientée vers la droite et encore de trois quarts. Elle ne constitue pas une garde de combat armée ni une animation. L’orientation et la superposition du visage ne permettent pas de valider séparément les quatre mandibules.
- Marges serrées de 8 px en haut du casque et de 14 px sous les pieds au seuil alpha >16, avec 288/350 px sur les côtés. Aucun contact de contenu alpha >16 avec le cadre ; 8 pixels de faible alpha touchent le bord gauche et 9 le bord supérieur.
- PNG RGBA 1199 × 1312, alpha 0 à 255, avec 1142819 pixels entièrement transparents et 23889 pixels alpha 1 à 16. Le détourage de production reste à contrôler en composition.
- Les formes exactes du casque et des épaules doivent être comparées au Zealot de Reach afin de distinguer cette variante des autres grades Sangheili, notamment Field Marshal ; la couleur seule ne certifie pas le modèle.

### Cethegus chef Brute

Fichier : `assets/characters_wave2/cethegus_h3_neutral_right_v01.png`. Dimensions : 1536 × 1024 px ; mode RGBA. Statut : candidat, fidélité non certifiée.

- Chef Brute en armure sombre et rouge, haute crête de casque et marteau gravitationnel complet visibles. Deux mains saisissent une seule hampe ; les deux pieds et la crête sont dans le cadre. Aucun membre supplémentaire évident dans cette vue.
- La pose montre une large face avant du plastron et reste nettement de trois quarts. La tête est orientée vers la droite, mais le corps ne constitue pas encore une pose latérale stricte.
- Marges de 5 px en haut de la crête et de 7 px sous les pieds, au seuil alpha > 16 ; marge de 45 px à droite du marteau. Aucun contact direct avec le bord à ce seuil, mais cadrage trop serré verticalement.
- PNG RGBA 1536 × 1024, alpha 0 à 254, avec 959422 pixels entièrement transparents. Plusieurs points du halo gris/noir visible dans l’aperçu ont alpha 0. Les 25251 pixels alpha 1 à 16 et le contour demandent un contrôle en composition réelle.
- Les détails de casque, de plaques rouges, de visage et de marteau doivent être comparés aux captures du duel de The Ark. La ressemblance à un chef Brute ne certifie pas à elle seule la fidélité exacte à Cethegus.

### Mgalekgolo Hunter

Fichier : `assets/characters_wave2/hunter_h3_neutral_right_v01.png`. Dimensions : 1536 × 1024 px ; mode RGBA. Statut : candidat, fidélité non certifiée.

- Armure bleue, colonie de vers orange, pointes dorsales courbes, canon à lueur verte et bouclier physique visibles. Les deux pieds, les pointes et le bouclier sont dans le cadre. Le canon au bras anatomiquement droit et le bouclier au gauche paraissent respectés dans cette vue de trois quarts.
- La silhouette reste très frontale et de trois quarts, plutôt que latérale. Les grandes zones de vers exposées aux épaules, au cou, au bras du bouclier et aux jambes demandent une comparaison à la géométrie Halo 3 ; leur conformité exacte ne peut pas être affirmée.
- Marges serrées : 4 px au-dessus des pointes, 12 px sous les pieds et 27 px à gauche, au seuil alpha > 16. Aucune partie ne touche directement le bord à ce seuil.
- PNG RGBA 1536 × 1024, alpha 0 à 254, avec 833560 pixels entièrement transparents. Le halo gris/bleu visible dans l’aperçu inclut des zones échantillonnées alpha 0 : il ne prouve pas un fond opaque. Les 36085 pixels alpha 1 à 16 et le contour doivent être vérifiés en composition réelle.
- Formes du canon, du bouclier, des plaques et des pointes dorsales à comparer au modèle Halo 3 avant toute certification.

## Lecture des contrôles techniques

Les dimensions, le mode couleur, le canal alpha, la présence de pixels au bord et les sommes SHA-256 sont mesurés en lecture seule. Le seuil alpha de 16 repère un contact éventuel avec le cadre ; ce signal doit être examiné visuellement, car il ne prouve à lui seul ni une découpe ni un défaut anatomique. Les contacts de faible alpha 1 à 16 sont enregistrés séparément, même lorsque la silhouette ne touche pas le cadre.

Les observations visuelles rattachées à une empreinte SHA-256 décrivent le fichier réellement examiné. Les fichiers sans observation restent à examiner. Chaque personnage demande ensuite une comparaison avec des références de son épisode, une vérification du profil de combat, un détourage de production et un jeu d'animations complet.

## Tentatives en échec dans le journal de cette vague

- `rtas_h3` — Génération refusée par le contrôle automatique ; motif précis non fourni. Une autre tentative a toutefois produit une pose candidate disponible dans cet inventaire.
- `tartarus_h2` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `noble_six` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `emile_reach` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `jorge_reach` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `kat_reach` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `chief_infinite` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `johnson_h3` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `jun_reach` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `carter_reach` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `buck_odst` — Génération refusée par le contrôle automatique ; motif précis non fourni. Une autre tentative a toutefois produit une pose candidate disponible dans cet inventaire.
- `rookie_odst` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `alice_hw2` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `douglas_hw2` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `escharum_infinite` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `jega_infinite` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `chak_lok` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `zealot_reach` — Génération refusée par le contrôle automatique ; motif précis non fourni. Une autre tentative a toutefois produit une pose candidate disponible dans cet inventaire.
- `chief_infinite` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `kat_reach` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `noble_six` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `emile_reach` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `jorge_reach` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `johnson_h3` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `jun_reach` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `carter_reach` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `rookie_odst` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `alice_hw2` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `douglas_hw2` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `tartarus_h2` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `escharum_infinite` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `jega_infinite` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
- `chak_lok` — Génération refusée par le contrôle automatique ; motif précis non fourni. Le personnage reste sans pose candidate.
