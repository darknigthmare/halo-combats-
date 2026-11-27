# Halo Combats — intégration du guide général et des deux extensions V10

État documentaire du **27 novembre 2026 (Europe/Paris)**. Projet de Darknigthmare. Cette annexe complète la [bible active V10](HALO_COMBATS_BIBLE_V10.md). Les fondations de la [bible V1](HALO_COMBATS_BIBLE_V1.md) et ses chiffres historiques restent conservés.

Les **trois originaux sont intégrés sans modification**, et leurs **68 sections** sont raccordées aux données, au prototype et au plan de production Halo. La grille contient **311 exigences regroupées et vérifiables**. Cette couverture mesure l’intégration documentaire : elle ne signifie ni 68 fonctions livrées, ni une certification visuelle 1:1.

Données structurées : [combat_guide_coverage_v10.json](../data/combat_guide_coverage_v10.json). Chaque exigence possède un ID, une source, une décision, une priorité, une adaptation Halo, des fichiers témoins et des états séparés de conception, prototype et assets.

Inventaire courant : [catalogue V10](../data/universe_catalog_v10.json) et [fiches projectiles / VFX V10](../data/projectiles_v10.json). Les chiffres V9 ci-dessous décrivent uniquement le point de départ historique ; les fiches de projectile distinguent leurs références d’incarnation des règles proposées pour Halo Combats.

## 1. Originaux retrouvés et traçabilité

| Source | Date inscrite | Sections | Taille | Copie intégrale | Original Drive |
|---|---|---|---:|---|---|
| Guide général | 2026-11-25 | 00–29 | 55,172 octets | [Combat_Games_Guide_General_v1.0.txt](guides_combat/Combat_Games_Guide_General_v1.0.txt) | [Source](https://drive.google.com/file/d/14o_RrgXucs8Km-x1LQJtMK7rol6mENKy/view?usp=drivesdk) |
| Extension 01 — équipes et bonus | 2026-11-26 | 30–49 | 60,589 octets | [Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt) | [Source](https://drive.google.com/file/d/1rYxKLIbz67L1sstmJWsga76uK7cX2mXF/view?usp=drivesdk) |
| Extension 02 — accès et déblocages | 2026-11-27 | 50–67 | 47,334 octets | [Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt) | [Source](https://drive.google.com/file/d/1qr8hgvvjFqdWzcGaf1DPeKromk75bBn0/view?usp=drivesdk) |

L’Extension 02 est datée du 27 novembre dans le document ; son horodatage Drive du 26 novembre à 23:18 UTC correspond déjà au 27 novembre en France. Le fichier [source_metadata.json](guides_combat/source_metadata.json) conserve les dates, tailles et empreintes SHA-256. Aucun lien de téléchargement temporaire, jeton ou secret n’y figure.

- **Combat_Games_Guide_General_v1.0.txt** — SHA-256 `4844584616072ac0d52d37c2fab4365e1ec489240f17a721ee216e223b0355b7`.
- **Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt** — SHA-256 `330fb7485a7a52b2a20f855646c940aaac0fcd9510032bc84b2e17c518edd25f`.
- **Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt** — SHA-256 `08b57ea542e83c487fef3276997a612d4657f2ee9ed4f8e46b0bf65a2778038b`.

## 2. Ce qui existait avant cette intégration

Point de départ Git : `4303981d1dd7322e4f12e47112c0566cf5bc31ea`. La recherche des noms des trois guides et de leurs extensions dans `docs/`, `data/` et les README ne retournait aucune occurrence. La bible V1 couvrait déjà une partie des thèmes, mais les trois originaux et leurs nouvelles grilles n’étaient pas intégrés dans ces emplacements.

| Périmètre historique | Constat vérifié | Limite |
|---|---|---|
| Bible / données V1 | 24 identités, 24 arènes, 20 boss ; 264 normaux, 96 spéciaux, 24 supers, 48 finishers et 24 routes conçus | Fiches et paramètres de conception, pas leur intégration complète |
| Laboratoire V8 | Entraînement, duel IA, parcours Scarab partiel ; 24 identités sélectionnables | Simulation partagée, poses fixes, pas 24 kits individuels |
| Catalogue V9 | 232 fiches : 128 personnages, 24 costumes, 46 stages, 34 boss ; 104 PNG distincts | 77 fiches illustrées, 155 sans image au point V9 ; inventaire de l’univers non exhaustif |
| Images et animation V9 | PNG candidats et masters de décor | Zéro nouveau clip, zéro couche de parallaxe indépendante, fidélité 1:1 non certifiée |
| Preuves historiques | Rapports logique V8 et catalogue V9 conservés | Ils ne testent pas V10 et ne constituent pas une revue des pixels navigateur |

Sources du constat : [bible](HALO_COMBATS_BIBLE_V1.md), [guide du labo V8](../prototype/README_V8.md), [catalogue V9](../data/universe_catalog_v9.json), [manifeste V9](../data/asset_manifest_v9.json), [rapport V8](../prototype/qa_v8/results.json), [rapport V9](../prototype/qa_v9/results.json). Les nouveaux lots visuels V10 sont suivis séparément par leur manifeste ; ces nombres restent ceux du point de départ V9.

**Réception du catalogue V10 :** le [rapport navigateur](../prototype/qa_v10/catalog_browser_results.json) contient 12 contrôles réussis, sans erreur de script, sur bureau et mobile. Les compteurs, filtres, états des images, fiche CU32, fermeture clavier et absence de miroir sur Pavium sont vérifiés dans leurs scénarios nommés. Ces preuves sont rattachées à six exigences ; elles ne certifient ni tous les détails artistiques, ni le moteur de combat.

## 3. Contrat de fidélité et de narration

Halo Combats est une adaptation de fan créée pour ce projet. Les règles, noms de techniques inventés, jauges, fenêtres, duels, interfaces de collection et chorégraphies ne sont pas du lore officiel. L’objectif 1:1 porte sur l’identité, l’incarnation, l’apparence, les armes et les capacités ; il ne correspond pas à un format carré d’image.

Chaque fiche garde un statut : **canon attesté**, **adaptation jouable**, **original compatible**, **alternatif/crossover** ou **à confirmer**. Les sources visuelles exactes sont comparées au PNG. Les formes non montrées par une référence ne deviennent pas vérifiées par extrapolation. Aucun retournement horizontal automatique ne valide les prothèses, gravures, armes ou équipements asymétriques.

### Relations attestées et simulations

| Association | Ce qui est attesté | Règle Halo Combats |
|---|---|---|
| Jerome / Alice, versions HW2 | Membres de Red Team [H1] | Relation compatible ; chaque assist ou super reste une chorégraphie originale. Le duo sur Blood Gulch CE est une simulation libre. |
| Buck / Dare, versions ODST | Présence dans Alpha-Nine [H4] | Garder la période et l’équipement ODST. Un futur profil Spartan de Buck n’est pas injecté dans ce récit. |
| Fred / Kelly / Linda, versions H5 | Membres de Blue Team [H1] | Choisir deux membres pour le profil hybride ; une participation historique du Major demande son incarnation adéquate. |
| Major Infinite / Arbiter H3 | Alliance des personnages pendant Halo 3, pas de ces incarnations mélangées [H3] | Rencontre libre étiquetée simulation inter-époques ; aucune reconstitution historique annoncée. |
| Kai Silver / personnage du canon principal | Silver est une continuité indépendante [H2] | Croisement hypothétique du projet, explicitement séparé du récit principal. |

Une relation connue ne garantit ni présence dans un chapitre, ni arme commune, ni capacité de soutien universelle. La campagne vérifie disponibilité, état, connaissances et costume. Le partenaire KO ne revient pas pour un finisher. Cortana ou l’Arme ne reçoivent pas un corps combattant inventé sans un concept alternatif explicite.

### Archives de combat et grammaire des verrous

Le cadre original déjà présent dans la bible devient le lieu de consultation et de progression proposé. Les dossiers masqués, cadres de scan, autorisations et casiers sont une métaphore d’interface du projet. Cette présentation n’affirme pas qu’une institution Halo possède toutes les archives des autres factions ou d’autres continuités.

Le secret complet utilise un emplacement neutre. L’indice révélé peut utiliser une silhouette noire ; le contenu identifié conserve son nom et sa condition. Les couleurs sont doublées par icône et texte. Le mode statique garde la même information et ne dépend d’aucun abonnement.

## 4. Contrat du laboratoire extensions V10

**Logique partiellement vérifiée : 30 tests Node réussis, 0 échec.** La commande `node --test prototype/qa_v10/extensions.test.cjs` a été relancée indépendamment. Le [reçu](../work/wave10/guide_runtime_verification.json) conserve la sortie et les empreintes du code testé. Le point d’entrée est `prototype/halo_extensions_v10.html`.

**Navigateur : 26 contrôles nommés réussis, aucune erreur de script rapportée.** Le [rapport du laboratoire](../prototype/qa_v10/extensions_browser_results.json) a été relu et rattaché à la matrice. Il couvre des parcours sur bureau et écran mobile, la sélection, les actions équipe, le bonus de précision, la persistance et l’ouverture locale. Cette réception ne vaut pas validation de tous les périphériques, de tous les assets, des clips ou du moteur complet de collisions.

Périmètre visé : états déterministes d’un duo, assist/tag/taunt/super et conclusion, progression locale, présentation des slots, bonus de précision et de coordination. Le laboratoire ne prétend pas implémenter le moteur complet de collisions, les movesets du roster, des clips de combat, le réseau, des paiements ou un accès Patreon réel.

| Réglage de labo proposé | Valeur | Interprétation |
|---|---|---|
| Simulation / équipe | 60 Hz ; deux membres ; défaite après deux KO | Paramètres de simulation originale |
| Vie / jauge équipe | 1 000 PV par membre ; aucun bouclier simulé ; jauge 100 | Jauge initiale 100, distincte des trois barres individuelles V1 |
| Gain de jauge | 10 par normal ; plafond 25 par combo ; pas de gain passif | Fin du combo après 90 frames sans touche |
| Normal | 40 frames ; contact à 10 ; 80 dégâts | Événement logique de test, pas un mouvement animé final |
| Assistance | 25 jauge ; 18 arrivée + 6 active + 24 sortie ; 120 dégâts | Cooldown de 300 frames après sortie ; partenaire occupé pendant intervention |
| Relais | 15 jauge ; transfert à 18 ; contrôle à 36 | Cooldown du sortant 120 frames démarrant à f18 ; relais après KO gratuit |
| Taunt | 60 frames : 18 / 24 / 18 | Vulnérable ; cancel volontaire à partir de 42 ; aucun gain |
| Super duo | 75 jauge ; ouverture 18 | Touche : 150 frames/360 dégâts appliqués après scène confirmée ; garde : 60/20 ; raté : 72/0 |
| Scène de super | Cooldowns gelés ; aucun remboursement après engagement | Interruption et partenaire occupé restent explicites |
| Finisher équipe | Fenêtre 180 frames ; présentation 120 ; gratuit | Deux membres vivants et disponibles ; remplacement par victoire normale inchangée |

Ces valeurs sont implémentées dans le modèle de laboratoire et partiellement exercées par les tests. Elles restent des hypothèses d’équilibrage originales, sans origine canonique. L’équipe par défaut est Jerome/Alice HW2 ; le décor Blood Gulch CE impose la mention de simulation inter-époques. Aucun bouclier n’est simulé dans ce laboratoire. Le jeu complet doit ensuite intégrer les ressources et propriétés propres à chaque incarnation.

### Règles des droits et des récompenses

Quatre dimensions restent indépendantes : découverte, sources de droit, disponibilité des fichiers et compatibilité de partie. Une récompense peut être acquise avant son personnage ou avant l’installation de son image. Elle reste enregistrée ; l’interface expose la dépendance utile.

Une règle ET exige ses branches ; une règle OU admet chacune de ses alternatives. Les sources permanentes et temporaires sont conservées séparément. Expirer une source temporaire ne retire jamais une acquisition permanente valide. Une panne de vérification donne un état inconnu, sans inventer fin d’abonnement ou nouveau droit.

Les acquisitions sont idempotentes : un même événement, double clic ou rechargement ne crée pas une seconde récompense et ne facture pas deux fois une clé. Le résultat est enregistré avant la scène de révélation. Une partie autorisée garde sa configuration jusqu’au résultat ; une expiration s’applique avant la suivante avec remplacement annoncé et préférences préservées.

L’architecture optionnelle de soutien prévoit récompense permanente, catalogue temporaire et lots par période. **Aucun fournisseur, campagne, niveau payant, prix, jeton ou paiement réel n’est raccordé dans ce lot.** Les futurs cosmétiques ne changent ni statistiques, ni collisions, ni timings, ni lisibilité utile. Les sources de la section 60 seront revérifiées si cette intégration est engagée.

## 5. Premières fiches de production représentatives

Ces fiches précisent des décisions de production et des critères ; leur présence n’atteste pas la fabrication de leurs animations. Les identifiants ci-dessous désignent des fiches de conception. Les IDs de contenu runtime définitifs restent ceux de son catalogue versionné.

| Fiche Extension 01 | Application Halo | État et critère principal |
|---|---|---|
| A — HC_TAUNT_JEROME_HW2_01 | Contrôle tactique de posture/équipement, geste original compatible, sans réplique canon inventée | 60 frames prévues, vulnérabilité et cancel vérifiés ; entrée/maintien/sortie à dessiner |
| B — HC_SELECT_JEROME_HW2_01 | Aperçu de l’incarnation HW2, confirmation, attente, retrait et sortie courte | Nettoyage des objets de l’aperçu et choix immédiat ; clip de désélection à produire |
| C — HC_TEAM_RED_HW2_01 | Jerome actif / Alice réserve, rôles interchangeables, hybride deux membres | Vie individuelle, disponibilité exclusive, jauge commune et deux KO ; logique partiellement testée |
| D — HC_ASSIST_RED_HW2_01 | Intervention de couverture avec équipement du profil réellement retenu | Arrivée/action/sortie/cooldown, contact et vulnérabilité ; arme exacte à verrouiller avant dessin |
| E — HC_DUO_RED_HW2_01 | Coordination originale entre équipiers ; variantes de cible humain/alien/machine | Ouverture confirmée, blocage/raté courts, pas de membre KO ; storyboard et clips absents |
| F — HC_CLASH_ENERGY_01 | Confrontation de lames éligibles, règle originale avec profil sans QTE | Différée : définir contact, tiers, égalité, absence et reprise avant prototype |
| G — HC_ENTITY_EQUIPMENT_01 | Objet déployé de l’incarnation concernée, propriétaire stable | À décliner sur équipement attesté ; gestion KO/réserve/transition et limite avant activation |
| H — HC_BONUS_PRECISION_01 | Cibles d’exercice ; score et réussite d’entraînement | Logique de bonus testée ; décor de production et variante par kit à produire |
| I — HC_ARCHIVES_HUB_01 | Accueil relié à armurerie, dossiers, cartographie et trophées | Conception : chemins explicites, accès ciblés et aucune clé derrière sa propre récompense |
| J — HC_REWARD_COORDINATION_01 | Succès de coordination vers récompense du catalogue | ID stable, condition mesurable, attribution unique et reprise ; référence à la règle runtime finale |

| Fiche Extension 02 | Application Halo | État et critère principal |
|---|---|---|
| A — HC_SLOT_DOSSIER_01 | Slot dossier de combattant, secret/indice/identifié, action utile | Le masque ne signale jamais un PNG inachevé ; dépendance technique distincte |
| B — HC_UNLOCK_TRAINING_01 | Voie de défi OU autre source admissible, sauvegarde de profil | AND/OR, compteurs, claim unique, coût et reprise testés avant livraison |
| C — HC_SUPPORTER_MODEL_01 | Modèle optionnel permanent/temporaire/lot, avantage cosmétique | Spécification seulement ; aucun tiers réel, fournisseur ou paiement opérationnel |
| D — HC_LOCK_VISUAL_01 | Dossier masqué cyan/acier, contour de silhouette, emblème neutre secret | Métaphore UI originale ; texte/focus/contraste/lecteur d’écran et mouvement réduit |
| E — HC_STAGE_ACCESS_01 | Sélection d’arène distincte de participation ; confort inclus | En multijoueur futur, assets des destinations accessibles avant départ ou remplacement commun |
| F — HC_ENTITLEMENT_MATRIX_01 | Permanent + temporaire expiré, fichiers manquants, costume sans parent | Résultat correct après sauvegarde et reprise ; source restante maintient le droit effectif |

### Exploration et stages bonus : raccord narratif proposé

Le graphe d’exploration est une création du projet : accueil → armurerie, dossiers d’opérations, cartographie et trophées ; chaque destination revient à l’accueil. Un accès avancé se gagne depuis une activité déjà disponible. Les contenus importants ont une voie ciblée, sans récompense indispensable prisonnière de sa propre condition. L’exploration reste à implémenter ; le sélecteur de progression n’est pas une visite jouable de ces salles.

La précision apprend portée et ressources ; la coordination apprend assist/relais. La casse d’épave, la défense d’extraction et les hordes restent des futures fiches contextualisées, avec limites d’apparition, ressources adaptées et état de sortie. Les bonus facultatifs laissent poursuivre l’histoire après échec selon leur fiche. Aucun ennemi dangereux n’est déclaré fragile par simple commodité : exercice/simulation ou adaptation annoncée.

## 6. Matrice complète des 68 sections

Chaque section ci-dessous contient son adaptation et les exigences regroupées. Les originaux cités demeurent la référence intégrale. **Documenté** signifie spécifié ; les états prototype et assets indiquent séparément ce qui reste à réaliser. Les preuves existantes décrivent leur propre version et ne certifient pas les exigences ajoutées.

<a id="section-00"></a>

### Section 00 — Utilisation du guide et priorités

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Document / référence · **Assets :** `not_applicable`.

Le guide devient une grille de suivi Halo Combats. La production actuelle reste centrée sur les sprites fixes manquants ; les animations sont spécifiées et restent dans leur phase dédiée.

- **HC-G-00-01** — Examiner bible, catalogues, PNG et prototypes avant chaque lot ; préserver les fichiers validés et leur provenance.
- **HC-G-00-02** — Attribuer à chaque rubrique une décision, une priorité, des dépendances et une preuve ; conserver les fonctions différées avec leur motif.
- **HC-G-00-03** — Distinguer spécification, pose fixe, clip animé, intégration au jeu et validation ; ne pas convertir une demande de sprites en production d’animations implicite.
- **HC-G-00-04** — Fixer un périmètre nommé par version ; traiter architecture réseau et exploration tôt si leur implémentation est engagée.

Source intégrale : [section 00 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json).

<a id="section-01"></a>

### Section 01 — Identité du projet et périmètre

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Prototype V8 partiel · **Assets :** `static_candidates_partial`.

Conserver le duel latéral 2D UHD, Boss Battle à grandes échelles et Archives de combat comme cadre original de simulation. Clavier et tactile existent en prototype ; manette, multijoueur et plateformes finales demandent une validation distincte.

- **HC-G-01-01** — Nommer continuité, période et incarnation pour chaque contenu ; définir ton, piliers et bornes de la version livrée.
- **HC-G-01-02** — Décrire format latéral, échelle, difficulté, langues, sous-titres et périphériques réellement supportés.
- **HC-G-01-03** — Séparer modes de fondation, cible narrative et extensions ; ne pas annoncer une plateforme vérifiée sans exécution réelle.
- **HC-G-01-04** — Garder les systèmes communs réutilisables tout en isolant données, capacités et références Halo.

Source intégrale : [section 01 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/fighters.json](../data/fighters.json).

<a id="section-02"></a>

### Section 02 — Fidélité au lore et sources

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Document / référence · **Assets :** `unverified_fidelity`.

Les cinq statuts de fidélité deviennent obligatoires. Le canon principal, Silver, variantes Fracture et simulations originales restent distincts. Une chorégraphie du projet ne devient jamais un événement canonique.

- **HC-G-02-01** — Conserver œuvre, version, scène/page et référence visuelle exploitable ; signaler les références manquantes ou contradictoires.
- **HC-G-02-02** — Vérifier silhouette, proportions, matériaux, couleurs, asymétries, armes, personnalité et limites de capacité.
- **HC-G-02-03** — Classifier canon attesté, adaptation jouable, original compatible, alternatif/crossover ou à confirmer ; interdire la fusion silencieuse d’époques.
- **HC-G-02-04** — Marquer chiffres, noms de coups inventés et cadrage latéral comme adaptations ; une image générée seule ne certifie pas le 1:1.

Source intégrale : [section 02 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [docs/source_registry.json](source_registry.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json).

<a id="section-03"></a>

### Section 03 — Roster, personnages, variantes et costumes

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Prototype V8 partiel · **Assets :** `static_candidates_partial`.

Le roster de base comporte 24 identités ; le catalogue V9 regroupe 232 fiches de plusieurs catégories. Le catalogue n’active pas automatiquement des kits jouables, et Cortana ou l’Arme restent interfaces/soutiens selon la bible.

- **HC-G-03-01** — Inventorier par œuvre et par rôle personnages, antagonistes, classes ennemies, soutiens, PNJ et créations admises.
- **HC-G-03-02** — Distinguer identité, variante de règles, transformation, costume et palette avec identifiants liés au parent.
- **HC-G-03-03** — Définir rythme, ressource, forces, faiblesses et contre-jeu sans uniformiser artificiellement capacités ou boucliers.
- **HC-G-03-04** — Lister portrait, HUD, versus, sprite entier, armes, effets et besoins narratifs ; vérifier compatibilité tenue/période/scénario.
- **HC-G-03-05** — Contrôler collisions et silhouettes des costumes ; une arme ou capacité nouvelle requiert un profil distinct si elle modifie le kit.

Source intégrale : [section 03 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [data/fighters.json](../data/fighters.json), [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/expansion_characters.json](../data/expansion_characters.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json).

<a id="section-04"></a>

### Section 04 — Fondations du système de combat

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Prototype V8 partiel · **Assets :** `not_applicable`.

Le laboratoire fournit déplacement, saut, dash, garde, attaques et simulation 60 Hz. Le contrat complet à six boutons et les règles de manche de la bible restent la cible ; les divergences V8 sont enregistrées ci-dessous.

- **HC-G-04-01** — Définir joueurs, manches, chrono, victoire, égalité, double KO, abandon, pause et perte de périphérique.
- **HC-G-04-02** — Spécifier déplacements, limites, changement de côté, niveaux de garde, projections, chutes et relèves.
- **HC-G-04-03** — Donner à chaque archétype des réponses à distance, aux sauts, aux projections et à la pression ; mesurer la portée et les contreparties.
- **HC-G-04-04** — Documenter orientation, buffer, tolérances, maintien et priorité des saisies ; distinguer pas de simulation et fréquence d’affichage.
- **HC-G-04-05** — Ne déclarer une mécanique universelle validée qu’après confrontation avec ses fenêtres, états et cas simultanés.

Source intégrale : [section 04 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [prototype/lab_v8/app.js](../prototype/lab_v8/app.js), [prototype/qa_v8/results.json](../prototype/qa_v8/results.json).

<a id="section-05"></a>

### Section 05 — Movesets, coups spéciaux et ressources

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Prototype V8 partiel · **Assets :** `animation_missing`.

Les fiches V1 fournissent 264 normaux, 96 spéciaux et 24 supers conçus. Le laboratoire utilise un gabarit commun et ne constitue pas l’intégration de ces kits individuels.

- **HC-G-05-01** — Décrire normaux, directionnels, projections, spéciaux, ultimes, équipement, déplacements et défenses propres au personnage.
- **HC-G-05-02** — Pour chaque coup, relier ID, source, commande, conditions, démarrage/actif/récupération, portée, collisions, dégâts et ressources.
- **HC-G-05-03** — Fixer résultats touche/garde/contre/raté, immobilisations, cancels, invulnérabilités, interactions et signaux.
- **HC-G-05-04** — Conserver limites de combo, rebonds, juggle et retour du défenseur ; ne pas réinitialiser ces limites lors d’un relais.
- **HC-G-05-05** — Définir capacité, gain, dépense, recharge, épuisement, visibilité et reset de chaque ressource ; les valeurs restent des réglages à tester.

Source intégrale : [section 05 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [data/fighters.json](../data/fighters.json), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/animation_plan.json](../data/animation_plan.json).

<a id="section-06"></a>

### Section 06 — Ultimes, finishers et conclusions de combat

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Non implémenté · **Assets :** `animation_missing`.

Conserver la famille de neutralisations, exécutions, destructions d’unité et sorties de simulation déjà définie. Les 48 finishers V1 sont des propositions, pas des clips livrés.

- **HC-G-06-01** — Séparer ultime en combat, finisher après condition, pose de victoire et outro narrative.
- **HC-G-06-02** — Respecter intention du personnage, ton Halo, version d’arme et anatomie de la cible.
- **HC-G-06-03** — Définir nom original ou attesté, conditions, commande, distance, modes, durée, caméra, effets, son et retour.
- **HC-G-06-04** — Fournir des remplacements pour géants, machines, Lekgolo et cibles incompatibles ; ne pas réutiliser une prise humaine sans adaptation.
- **HC-G-06-05** — Documenter finishers de stage et abrègement ; une conclusion de simulation ne réécrit pas la chronologie officielle.

Source intégrale : [section 06 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [data/fighters.json](../data/fighters.json), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md).

<a id="section-07"></a>

### Section 07 — Présentation et relations entre personnages

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Non implémenté · **Assets :** `animation_missing`.

Relier la matrice de relations aux incarnations exactes. Les dialogues seront originaux et adaptés aux connaissances du personnage ; l’apparition d’un allié ne prouve pas sa présence dans tous les chapitres.

- **HC-G-07-01** — Planifier entrée, garde, taunt, réactions, victoire, défaite et sortie avec langage corporel propre.
- **HC-G-07-02** — Classifier alliances, rivalités, mentorat, inconnus et rencontres hypothétiques ; citer la source d’une relation attestée.
- **HC-G-07-03** — Prioriser échanges narratifs majeurs et prévoir variantes génériques pour les autres cas sans annoncer une scène exclusive par paire.
- **HC-G-07-04** — Vérifier période, équipement et connaissances ; calculer volume de production des dialogues et présentations.

Source intégrale : [section 07 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/fighters.json](../data/fighters.json).

<a id="section-08"></a>

### Section 08 — Histoire individuelle de chaque personnage

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Non implémenté · **Assets :** `narrative_art_missing`.

Les 24 routes conçues restent des parcours de reconstitution ou de simulation explicitement nommés. Chaque héros garde un enjeu propre, un rival motivé et une conclusion correspondant à son introduction.

- **HC-G-08-01** — Écrire situation, déclencheur, apprentissage, rival, revers, confrontation décisive et outro pour chaque jouable retenu.
- **HC-G-08-02** — Pour chaque combat, fixer raison, lieu, version d’adversaire, dialogue, résultat et transition.
- **HC-G-08-03** — Étiqueter route compatible, parallèle, alternative ou hypothétique ; expliquer alliés adversaires et personnages de périodes différentes.
- **HC-G-08-04** — Planifier illustrations distinctes d’intro/rival/ending, difficulté, sauvegarde, reprise et galerie ; chiffrer séparément embranchements.

Source intégrale : [section 08 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [data/fighters.json](../data/fighters.json), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md).

<a id="section-09"></a>

### Section 09 — Campagne globale distincte

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Non implémenté · **Assets :** `narrative_art_missing`.

Les six actes existants servent de cadre au parcours Archives de combat. Leur ordre éditorial relie des dossiers et des simulations ; il n’affirme pas un événement historique unique réunissant toutes les époques.

- **HC-G-09-01** — Définir intrigue du parcours, enjeux, factions, protagonistes, progression, revers et résolution distincts des routes individuelles.
- **HC-G-09-02** — Chaque chapitre fixe personnage/version, objectif narratif et jouable, lieux, adversaires, scènes, assets, échec et progression.
- **HC-G-09-03** — Documenter alternance duel/exploration/horde/boss et compatibilité des ressources ; garder les bonus de campagne hors duel normalisé.
- **HC-G-09-04** — Prévoir sélection de chapitre, checkpoints, objectifs, reprise après interruption et conséquences des choix.

Source intégrale : [section 09 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md).

<a id="section-10"></a>

### Section 10 — Illustrations et cinématiques narratives

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Non implémenté · **Assets :** `narrative_art_missing`.

Produire d’abord des fiches de plans pour intros, rivalités et endings Halo. Les portraits et poses de catalogue ne seront pas comptés comme scènes narratives achevées.

- **HC-G-10-01** — Fixer rôle narratif, acteurs, versions, tenue, blessures, émotions, lieu, heure et état du monde.
- **HC-G-10-02** — Décrire plans, cadrage, action, regards, lumière, palette, décor et réserves de texte.
- **HC-G-10-03** — Séparer dialogues/sous-titres des images ; conserver musique, sons, silences et transition vers le combat dans la fiche.
- **HC-G-10-04** — Contrôler continuité entre plans, statut des éléments et calques réellement nécessaires ; distinguer illustration collective et sprite isolé.

Source intégrale : [section 10 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/animation_plan.json](../data/animation_plan.json).

<a id="section-11"></a>

### Section 11 — Boss, machines et boss rush

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Prototype V8 partiel · **Assets :** `static_candidates_partial`.

Le Scarab V8 vérifie une boucle jambes/abordage/noyau partielle. Les 20 rencontres V1 et 34 fiches boss V9 n’équivalent pas à 34 boss jouables ; les géants conservent une échelle de scène.

- **HC-G-11-01** — Classifier duel, élite, phases, créature, machine et rencontre à objectifs ; conserver version exacte de chaque véhicule.
- **HC-G-11-02** — Spécifier phases, signaux, points faibles, réponses, victoire, échec, reprise et récompense.
- **HC-G-11-03** — Valider accès au noyau et solutions pour courte portée, projectiles, petites tailles et grands gabarits ; aucune immunité sans contre-jeu.
- **HC-G-11-04** — Séparer équilibrage boss, campagne et éventuelle version jouable.
- **HC-G-11-05** — Écrire règles Boss Rush: liste, ordre, ressources persistantes, récupération, essais, score, sauvegarde et entraînement.

Source intégrale : [section 11 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [data/bosses.json](../data/bosses.json), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [prototype/lab_v8/app.js](../prototype/lab_v8/app.js).

<a id="section-12"></a>

### Section 12 — Modes de jeu

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Prototype V8 partiel · **Assets :** `not_applicable`.

Entraînement, duel IA et Scarab partiel existent. Histoire, campagne, tournoi, Boss Rush complet, multijoueur et coopération restent des modes à produire ; le laboratoire extensions n’en remplace pas les parcours.

- **HC-G-12-01** — Pour chaque mode, définir entrée, sélection, règles, joueurs, victoire, résultat, revanche/sortie et reprise.
- **HC-G-12-02** — Conserver les fondations versus/IA/training/tutoriel et les cibles histoire/campagne/boss/galerie avec leurs états réels.
- **HC-G-12-03** — Décider explicitement survie, chrono, tournoi, équipes, tag, assist, coop, online, classement et observation.
- **HC-G-12-04** — Ne pas compter un bouton, une fiche de catalogue ou un futur mode verrouillé comme mode fonctionnel.

Source intégrale : [section 12 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [prototype/README_V8.md](../prototype/README_V8.md).

<a id="section-13"></a>

### Section 13 — Arènes : lieux, composition et lisibilité

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Prototype V8 partiel · **Assets :** `flat_masters_partial`.

Le registre de base décrit 24 arènes et V9 en catalogue 46. Les masters plats servent de composition ; chaque découpage latéral garde l’incarnation et annonce son adaptation 2D.

- **HC-G-13-01** — Fixer source, période, fonction, dimensions jouables, sol, limites, lumière et ambiance.
- **HC-G-13-02** — Distinguer lieu attesté et création compatible ; conserver plans nécessaires, horizon, ancrages et échelle.
- **HC-G-13-03** — Garantir pieds ancrés, contraste et avant-plan non occultant ; vérifier les grands combattants.
- **HC-G-13-04** — Qualifier jour/nuit, météo et destruction comme variations visuelles ou règles de jeu ; chiffrer sons, musique et états de campagne.

Source intégrale : [section 13 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [data/stages.json](../data/stages.json), [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/asset_manifest_v9.json](../data/asset_manifest_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json).

<a id="section-14"></a>

### Section 14 — Arènes vivantes, statiques et événements

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Prototype V8 partiel · **Assets :** `independent_layers_missing`.

Les profils spectacle, compétition et confort séparent présentation, interactions, dangers et transitions. Réduire l’animation de fond ne retire aucun projectile dangereux ni signal utile.

- **HC-G-14-01** — Gérer indépendamment décor vivant/statique/réduit, objets interactifs, dangers et transitions.
- **HC-G-14-02** — Définir événements par déclencheur, fréquence, durée, acteurs, effets et état final ; conserver des boucles désynchronisées.
- **HC-G-14-03** — Préserver géométrie et informations critiques lors d’un changement de confort ; fournir signaux statiques pour dangers conservés.
- **HC-G-14-04** — Partager les règles de gameplay entre joueurs ; seules les options de présentation compatibles restent locales.

Source intégrale : [section 14 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [data/stages.json](../data/stages.json), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md).

<a id="section-15"></a>

### Section 15 — Arènes connectées, transitions et interactions

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Non implémenté · **Assets :** `connected_stage_art_missing`.

Les transitions de secteur sont conçues comme connexions localisées dans un même ensemble Halo cohérent. Une porte ou projection ne téléporte pas silencieusement entre Blood Gulch, New Mombasa et Zeta Halo.

- **HC-G-15-01** — Chaque liaison identifie origine, destination existante, point de passage, condition, direction, ressource et défense possible.
- **HC-G-15-02** — Définir dégâts, combo, chrono, caméra, durée, positions et contrôle d’arrivée ; borner répétition et traiter KO/double déclenchement.
- **HC-G-15-03** — Charger la destination avant départ ; vérifier absence d’impasse, logique spatiale et reprise.
- **HC-G-15-04** — Pour chaque objet interactif, préciser capacité, portée, commande, coût, vulnérabilité, effet, charges, destruction et reset.
- **HC-G-15-05** — Vérifier les règles compétition/confort et les alternatives pour un personnage sans capacité d’interaction spécifique.

Source intégrale : [section 15 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [data/stages.json](../data/stages.json), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md).

<a id="section-16"></a>

### Section 16 — Ennemis, soutiens, véhicules et projectiles

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Prototype V8 partiel · **Assets :** `static_candidates_partial`.

Ennemis, projectiles, véhicules et soutiens reçoivent des catégories séparées. Une arme Infinite ne devient pas l’équipement d’un ODST 2552 ; le projet conservera les références d’émission et de trajet.

- **HC-G-16-01** — Inventorier ennemis, élites, faune, machines, véhicules, soutiens et PNJ avec rôles et modes.
- **HC-G-16-02** — Décrire silhouette, comportement, annonces, réactions, apparition et fonctions de chaque ennemi de campagne.
- **HC-G-16-03** — Pour projectile: source, propriétaire, arme, forme/couleur/taille, émission, trajectoire, portée, durée, impacts et collisions.
- **HC-G-16-04** — Définir garde, accrochage, réflexion/destruction/traversée, interaction décor/entités et contre-jeu.
- **HC-G-16-05** — Séparer sprite, traînée, départ, impact, dissipation et son ; classifier props visuels, destructibles, interactifs ou de mission.

Source intégrale : [section 16 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [data/bosses.json](../data/bosses.json), [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/fighters.json](../data/fighters.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json), [data/projectiles_v10.json](../data/projectiles_v10.json).

<a id="section-17"></a>

### Section 17 — Direction artistique et production des assets

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Catalogue V10 partiellement testé dans le navigateur · **Assets :** `static_candidates_partial`.

Poursuivre les sprites UHD autonomes: un seul personnage, projectile ou prop par source, corps complet et transparence réelle. Les asymétries de Kat, Jega, Rtas ou Atriox exigent un contrôle des deux côtés.

- **HC-G-17-01** — Conserver style, matériaux, proportions, lumière, perspective et lisibilité après réduction à la taille du jeu.
- **HC-G-17-02** — Vérifier sujet unique, cadrage entier, alpha réel, marges, échelle, orientation, ligne de sol et ancrages.
- **HC-G-17-03** — Ne pas valider automatiquement un miroir horizontal ; conserver chaque correction de prothèse, arme, inscription et pièce asymétrique.
  Preuve catalogue partielle : Catalogue navigateur: PNG Pavium affiché sans transformation miroir. Cela ne valide pas toutes les asymétries ni la conformité de toutes les images.
- **HC-G-17-04** — Relier nom stable, catalogue, provenance, conditions d’usage connues et contrôle visuel ; garder sources individuelles distinctes d’un atlas.
- **HC-G-17-05** — Inventorier variantes, portraits, armes, effets et couches de stage ; compter une pose seulement comme pose.

Source intégrale : [section 17 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [data/asset_manifest_v9.json](../data/asset_manifest_v9.json), [data/animation_plan.json](../data/animation_plan.json), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [prototype/qa_v10/catalog_browser_results.json](../prototype/qa_v10/catalog_browser_results.json).

<a id="section-18"></a>

### Section 18 — Animations, vfx, son et caméra

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Prototype V8 partiel · **Assets :** `animation_and_audio_missing`.

Planifier animations, VFX, SFX et caméra sur les états du combat, tout en conservant la phase actuelle de sprites fixes. Le mouvement d’un PNG par le moteur ne devient pas un clip de marche.

- **HC-G-18-01** — Lister attente, déplacements, coups, gardes, impacts, chutes, relèves, projections, interactions, victoire et finisher.
- **HC-G-18-02** — Définir entrées/sorties, points d’émission, contacts, boîtes et synchronisation temporelle.
- **HC-G-18-03** — Séparer effets de départ/trajet/impact/garde/bouclier et sons attaque/voix/UI/ambiance sans saturation.
- **HC-G-18-04** — Tester cadrage duel/boss, formats d’écran, changements de côté, retour de cinématique et réduction des secousses.
- **HC-G-18-05** — Documenter hitstop et ralentis sans changer implicitement la cadence de simulation.

Source intégrale : [section 18 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [data/animation_plan.json](../data/animation_plan.json), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [prototype/lab_v8/app.js](../prototype/lab_v8/app.js).

<a id="section-19"></a>

### Section 19 — Interface et expérience utilisateur

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Catalogue V10 partiellement testé dans le navigateur · **Assets :** `ui_partial`.

Conserver le catalogue V9 et le laboratoire V8, puis ajouter un point d’entrée explicite pour les extensions V10. Les informations d’incarnation, limites de prototype et absence d’asset restent lisibles.

- **HC-G-19-01** — Couvrir démarrage, mode, difficulté, sélection, versus, chargement, HUD, pause, résultat, revanche et sortie.
- **HC-G-19-02** — Inclure chapitres, galerie, codex, progression et messages de service seulement pour fonctions réellement présentes.
- **HC-G-19-03** — Assurer clavier/manette annoncés, remappage, focus, erreurs utiles et confirmation uniquement en cas de perte réelle.
  Preuve catalogue partielle : Catalogue navigateur: fermeture du dialogue au clavier et fiche projectile mobile contrôlées. Manette, remappage et toutes les séquences de jeu restent à valider.
- **HC-G-19-04** — Distinguer contenu accessible, verrouillé par règle, absent et incompatible ; garder présentations abrégées et revanche rapide.
  Preuve catalogue partielle : Catalogue navigateur: images manquantes et Cartographe à corriger restent identifiés; aucun de ses PNG n’est présenté comme contenu terminé. Les droits de jeu sont testés séparément dans le laboratoire.

Source intégrale : [section 19 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [prototype/lab_v8/app.js](../prototype/lab_v8/app.js), [prototype/universe_v9/app.js](../prototype/universe_v9/app.js), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [prototype/qa_v10/catalog_browser_results.json](../prototype/qa_v10/catalog_browser_results.json).

<a id="section-20"></a>

### Section 20 — Tutoriels, entraînement et apprentissage

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Prototype V8 partiel · **Assets :** `tutorial_assets_missing`.

Le training V8 sert de base. Le futur parcours d’exercice expose séparément apprentissage des commandes, équipement Halo, assist, tag, ressources et réponses aux boss.

- **HC-G-20-01** — Enseigner déplacement, distance, défense, projection, punition, ressources et combos par exercices et causes d’erreur.
- **HC-G-20-02** — Fournir pour chaque kit un plan de jeu, commandes, coups utiles, combos accessibles et faiblesses.
- **HC-G-20-03** — Configurer vie, ressources, positions, comportement du mannequin, partenaires et remise à zéro.
- **HC-G-20-04** — Prévoir enregistrement/lecture, boîtes, temps d’action, input display, coin, changements de côté, projectiles et boss.
- **HC-G-20-05** — Signaler incompatibilité d’un exercice ou d’une séquence lorsque sa version de règles change.

Source intégrale : [section 20 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [prototype/lab_v8/app.js](../prototype/lab_v8/app.js), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md).

<a id="section-21"></a>

### Section 21 — Ia et difficulté

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Prototype V8 partiel · **Assets :** `not_applicable`.

L’IA V8 est commune et limitée. La cible est une IA par archétype capable d’utiliser équipement, réserve et objectifs sans connaître une entrée joueur avant son engagement.

- **HC-G-21-01** — Relier style IA au combattant: pression, patience, mobilité, défense, ressource ou pièges.
- **HC-G-21-02** — Régler réactions, erreurs, précision et décisions ; documenter exceptions de boss et éviter avantage caché.
- **HC-G-21-03** — Apprendre à utiliser et contrer projectiles, projections, entités, interactions, transitions et objectifs.
- **HC-G-21-04** — Conserver diagnostic de défaite, aide facultative et progression après essais ; tester difficultés séparément.

Source intégrale : [section 21 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [prototype/lab_v8/app.js](../prototype/lab_v8/app.js), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md).

<a id="section-22"></a>

### Section 22 — Équilibrage et accessibilité

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Catalogue V10 partiellement testé dans le navigateur · **Assets :** `accessibility_partial`.

La validation doit comparer tailles, allonges et ressources réelles des familles Halo. Le confort visuel conserve les informations ; un raccourci d’accessibilité ne change pas les règles PvP.

- **HC-G-22-01** — Mesurer matchups, ouvertures, défenses, sorties de pression et contreparties entre archétypes.
- **HC-G-22-02** — Chercher infinies, verrouillages de garde, projections répétées et boucles de transition/assist/entité.
- **HC-G-22-03** — Séparer progression de campagne et paramètres compétitifs ; versionner chaque changement de réglage.
- **HC-G-22-04** — Fournir remappage, contrastes, textes, sous-titres, volumes séparés, distinction des joueurs et réduction flashes/secousses.
  Preuve catalogue partielle : Catalogue navigateur: affichage à 390 px sans débordement et fiche mobile fonctionnelle. Cette preuve ne valide pas l’ensemble de l’accessibilité ou des matchups.
- **HC-G-22-05** — Tester informations accessibles sans couleur ou son seul et règles communes des aides affectant le jeu.

Source intégrale : [section 22 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [prototype/lab_v8/app.js](../prototype/lab_v8/app.js), [prototype/qa_v10/catalog_browser_results.json](../prototype/qa_v10/catalog_browser_results.json).

<a id="section-23"></a>

### Section 23 — Multijoueur, réseau et replays

**Décision :** differee · **Priorité :** P0 · **Prototype :** Non implémenté · **Assets :** `not_applicable`.

Rollback, salons, réseau, observation et replays restent des cibles. La détermination logique du laboratoire V10 n’est pas un transport réseau, un serveur ou une validation de netcode.

- **HC-G-23-01** — Définir profils locaux, attribution des côtés, reconnexion des périphériques, pause et revanche.
- **HC-G-23-02** — Si online: sérialiser combat, graines, entités, ressources et transitions dès l’architecture ; séparer simulation et effets.
- **HC-G-23-03** — Spécifier salons, version des clients, qualité connexion, déconnexions et résultat ; décider classement et crossplay distinctement.
- **HC-G-23-04** — Enregistrer règles, identifiants, entrées et contrôles d’état pour replay, puis gérer versions incompatibles.
- **HC-G-23-05** — Tester latence, pertes et correction sans double dommage, voix, entité ni récompense avant toute annonce online.

Source intégrale : [section 23 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [prototype/README_V8.md](../prototype/README_V8.md).

<a id="section-24"></a>

### Section 24 — Progression, sauvegardes et rejouabilité

**Décision :** retenue · **Priorité :** P0 · **Prototype :** V10 partiel, logique et navigateur testés · **Assets :** `progression_art_missing`.

Le nouveau modèle d’accès local se rattache aux IDs existants. Le progrès d’un joueur et l’avancement de la production restent deux mesures distinctes.

- **HC-G-24-01** — Définir récompenses de maîtrise, histoires, personnages, costumes, stages, scènes, fiches et modes.
- **HC-G-24-02** — Rendre conditions et voies alternatives lisibles ; ne pas faire passer un contenu manquant pour une récompense verrouillée.
- **HC-G-24-03** — Conserver routes, chapitres, acquisitions, paramètres, préférences et profils après fermeture et migration.
  Preuve logique partielle : Lecture/écriture logique d’un profil local, IDs inconnus et formats futurs/corrompus refusés. Migration complète, profils multiples et reprise navigateur restent à vérifier.
  Preuve navigateur partielle : Navigateur: progrès et sélection conservés après rechargement, annulation de reset sans perte, seule la clé de ce laboratoire effacée au reset confirmé, sauvegarde corrompue conservée. Pas de migration complète ou compte distant testé.
- **HC-G-24-04** — Séparer bonus de campagne et duel normalisé ; définir hors ligne, reprise, doublons et règles de version.
  Preuve logique partielle : Lecture/écriture logique d’un profil local, IDs inconnus et formats futurs/corrompus refusés. Migration complète, profils multiples et reprise navigateur restent à vérifier.
  Preuve navigateur partielle : Navigateur: progrès et sélection conservés après rechargement, annulation de reset sans perte, seule la clé de ce laboratoire effacée au reset confirmé, sauvegarde corrompue conservée. Pas de migration complète ou compte distant testé.

Source intégrale : [section 24 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json), [prototype/qa_v10/extensions_browser_results.json](../prototype/qa_v10/extensions_browser_results.json).

<a id="section-25"></a>

### Section 25 — Organisation, inventaires et statistiques

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Catalogue V10 partiellement testé dans le navigateur · **Assets :** `not_applicable`.

Utiliser des identifiants stables, une matrice d’exigences et des preuves datées. Les nombres V1, V8 et V9 décrivent des périmètres différents et restent libellés par version.

- **HC-G-25-01** — Relier personnages, coups, costumes, stages, connexions, objets, projectiles, boss, scènes, audio et tests.
  Preuve catalogue partielle : Catalogue navigateur: filtres distincts de 19 projectiles et de 5 effets, recherche d’incarnation Halo 4, image M9 chargée et profil CU32 affiché. Les liens de production de tous les autres systèmes restent à étendre.
- **HC-G-25-02** — Suivre séparément lore, conception, art, intégration, validation et publication.
- **HC-G-25-03** — Calculer par catégorie et étape sur un dénominateur nommé ; absence de total = inventaire connu, dénominateur nul = non applicable.
  Preuve catalogue partielle : Catalogue navigateur: compteurs 256 fiches / 111 PNG / 172 sans visuel et 15 projectiles sans image contrôlés. Les unités et dénominateurs restent séparés, sans pourcentage global du jeu.
- **HC-G-25-04** — Pour complétude de bout en bout, exiger toutes les étapes sur les mêmes éléments ; ne pas moyenner images et fiches.
- **HC-G-25-05** — Distinguer local, commit, PR, fusion et livraison jouable, avec liens et limites vérifiables.

Source intégrale : [section 25 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/asset_manifest_v9.json](../data/asset_manifest_v9.json), [data/delivery_counts.json](../data/delivery_counts.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json), [prototype/qa_v10/catalog_browser_results.json](../prototype/qa_v10/catalog_browser_results.json).

<a id="section-26"></a>

### Section 26 — Critères de validation et ordre de production

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Document / référence · **Assets :** `not_applicable`.

Une rubrique documentée ne vaut pas fonctionnalité finie. Les tests historiques V8/V9 restent des preuves de leurs versions, jamais des tests V10 par héritage.

- **HC-G-26-01** — Définir fini pour fiche, sprite, combattant, arène, boss, route, campagne et mode.
- **HC-G-26-02** — Contrôler côtés, tailles, costumes, saisies, KO, temps, murs, transitions, sauvegarde et performances.
- **HC-G-26-03** — Valider d’abord une tranche complète représentative, puis étendre le catalogue et les scénarios.
- **HC-G-26-04** — Associer chaque résultat à la version et au niveau de preuve: logique, fichiers, pixels navigateur ou appareil.

Source intégrale : [section 26 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [prototype/qa_v8/results.json](../prototype/qa_v8/results.json), [prototype/qa_v9/results.json](../prototype/qa_v9/results.json).

<a id="section-27"></a>

### Section 27 — Fiches types à remplir

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Document / référence · **Assets :** `not_applicable`.

Conserver les dix fiches types du guide ; réutiliser les registres existants et enrichir les champs manquants sans dupliquer les identités.

- **HC-G-27-01** — Renseigner projet et personnage avec périmètre, sources, règles, récit, art, adaptations et incertitudes.
- **HC-G-27-02** — Renseigner action/projectile et finisher avec données temporelles, collisions, résultats et cibles.
- **HC-G-27-03** — Renseigner route, chapitre/scène, arène et liaison/interaction avec progression et continuité.
- **HC-G-27-04** — Renseigner boss et asset/suivi avec fichiers, dépendances, critères, preuves, publication et prochain écart.

Source intégrale : [section 27 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [data/fighters.json](../data/fighters.json), [data/stages.json](../data/stages.json), [data/bosses.json](../data/bosses.json), [data/animation_plan.json](../data/animation_plan.json), [data/projectiles_v10.json](../data/projectiles_v10.json).

<a id="section-28"></a>

### Section 28 — Instruction prête à transmettre à un projet

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Document / référence · **Assets :** `not_applicable`.

La présente annexe applique l’instruction commune à Halo Combats, en conservant le moteur, l’historique et l’autorisation de publication du projet.

- **HC-G-28-01** — Comparer existant et guide, puis rendre visibles présent/partiel/manquant/incertain/différé/non applicable.
- **HC-G-28-02** — Compléter bible et inventaires par lots cohérents, avec sources, adaptations, critères et un sujet par image autonome.
- **HC-G-28-03** — Respecter la phase sprites fixes et déclarer l’intégration réelle séparément.
- **HC-G-28-04** — Terminer chaque lot par périmètre, nombres, preuves, restants et blocages ; aucune complétude sans éléments vérifiables.

Source intégrale : [section 28 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/asset_manifest_v9.json](../data/asset_manifest_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json).

<a id="section-29"></a>

### Section 29 — Références vérifiées et vocabulaire

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Document / référence · **Assets :** `not_applicable`.

Les références Street Fighter, Mortal Kombat, Guilty Gear et Injustice expliquent des inspirations de système. Elles n’autorisent aucune capacité fictive à devenir du canon Halo.

- **HC-G-29-01** — Conserver les sources du guide dans l’original avec dates et titres précis.
- **HC-G-29-02** — Associer chaque référence à sa portée réelle et vérifier les détails instables au moment de leur implémentation.
- **HC-G-29-03** — Définir le vocabulaire de combat et distinguer inspiration d’un épisode, règle originale et canon de la franchise cible.

Source intégrale : [section 29 du guide](guides_combat/Combat_Games_Guide_General_v1.0.txt).
Fichiers témoins de l’existant : [docs/source_registry.json](source_registry.json), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md).

<a id="section-30"></a>

### Section 30 — Portée et rattachement au guide général

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 à vérifier · **Assets :** `animation_missing`.

Intégrer l’Extension 01 comme règles et fiches Halo reliées au roster, aux scènes et aux accès. Le laboratoire V10 constitue un sous-périmètre de vérification logique, pas l’intégration finale.

- **HC-E1-30-01** — Définir modes, périmètre, priorité et dépendances pour chaque fonction ; expliquer tout report ou adaptation.
- **HC-E1-30-02** — Conserver les cinq statuts de fidélité et l’incarnation de chaque participant.
- **HC-E1-30-03** — Distinguer assist, tag, super, finisher, fin dramatique, entité, clash, bonus et exploration.
- **HC-E1-30-04** — Documenter animations et poses maintenant sans compter des séquences non produites ; l’entité native ne consomme pas automatiquement un slot équipe.

Source intégrale : [section 30 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json).

<a id="section-31"></a>

### Section 31 — Taunts : provocations et réactions de personnalité

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 logique partielle testée · **Assets :** `animation_missing`.

Les taunts gardent la retenue tactique, la menace ou le défi propres au personnage. Le premier taunt de laboratoire est une règle vulnérable sans gain de ressource, accompagnée d’une pose statique.

- **HC-E1-31-01** — Identifier geste, contexte, costume, rival/allié et statut du nom ; prioriser un taunt complet par kit.
- **HC-E1-31-02** — Spécifier commande, conditions, entrée, boucle, sortie, durée, expression, accessoires, voix/VFX/SFX et reprise de contrôle.
- **HC-E1-31-03** — Définir vulnérabilité et interruption sur coup ou cancel volontaire sans effacer gratuitement sa contrepartie.
  Preuve logique partielle : Taunt vulnérable: coup interrompt, aucun gain, cancel prématuré refusé. Aucun clip ni voix produit.
- **HC-E1-31-04** — Séparer taunt de présentation et taunt à effet de jeu ; limiter répétitions et voix sans voler une commande.

Source intégrale : [section 31 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/animation_plan.json](../data/animation_plan.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-32"></a>

### Section 32 — Animations de sélection, confirmation et désélection

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 partiel, logique et navigateur testés · **Assets :** `selection_animation_missing`.

Le sélecteur distingue survol, présélection, confirmation, attente, costume, désélection et départ. Les sources statiques restent consultables ; une désélection dédiée sera produite par incarnation.

- **HC-E1-32-01** — Rendre les choix immédiats sans attendre la fin du visuel et prévoir sortie complète/abrégée.
  Preuve logique partielle : Événements logiques distincts désélection/confirmation/attente, choix actif/réserve et exclusion des doublons. Animation, nettoyages VFX/audio et navigation navigateur non prouvés ici.
  Preuve navigateur partielle : Navigateur: événements sélection/désélection émis après choix réel. Cela ne constitue pas un clip artistique de sélection.
- **HC-E1-32-02** — Nettoyer voix, particules, compagnon, ombres et éclairage appartenant à l’ancien aperçu lors de navigation rapide.
- **HC-E1-32-03** — Ne pas remplacer automatiquement la désélection par un clip inversé ; conserver accessoires et asymétries.
- **HC-E1-32-04** — Identifier actif/réserve/soutien, compatibilité de duo et retrait d’un membre.
  Preuve logique partielle : Événements logiques distincts désélection/confirmation/attente, choix actif/réserve et exclusion des doublons. Animation, nettoyages VFX/audio et navigation navigateur non prouvés ici.
- **HC-E1-32-05** — Tester deux curseurs, miroirs, costumes, choix simultanés/aléatoires et mode de mouvement réduit.

Source intégrale : [section 32 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [prototype/lab_v8/app.js](../prototype/lab_v8/app.js), [prototype/universe_v9/app.js](../prototype/universe_v9/app.js), [data/animation_plan.json](../data/animation_plan.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json), [prototype/qa_v10/extensions_browser_results.json](../prototype/qa_v10/extensions_browser_results.json).

<a id="section-33"></a>

### Section 33 — Profils d'équipe et catégories de partenaires

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 partiel, logique et navigateur testés · **Assets :** `team_art_missing`.

Retenir un profil hybride de deux membres dans le laboratoire : un actif et une réserve, vies individuelles, défaite à deux KO, arrivée gratuite du survivant. Tous les combats libres restent des simulations du projet.

- **HC-E1-33-01** — Annoncer assistance, tag ou hybride avant le match avec nombre, rôles, doublons, ordre et condition de défaite.
  Preuve logique partielle : Duo à PV individuels, défaite après deux KO et engagement exclusif du partenaire testés. Ressources propres à tous les kits et profils autres que hybride2 non intégrés.
- **HC-E1-33-02** — Conserver vie et ressources propres ; une seule intervention de roster par équipe à la fois.
  Preuve logique partielle : Duo à PV individuels, défaite après deux KO et engagement exclusif du partenaire testés. Ressources propres à tous les kits et profils autres que hybride2 non intégrés.
- **HC-E1-33-03** — Bloquer double engagement d’un partenaire déjà en assist, sortie, tag ou super.
  Preuve logique partielle : Duo à PV individuels, défaite après deux KO et engagement exclusif du partenaire testés. Ressources propres à tous les kits et profils autres que hybride2 non intégrés.
  Preuve navigateur partielle : Navigateur: bouton tag indisponible pendant assist; jauge diminuée exactement de 25 lors de l’assist. Les autres refus restent couverts seulement par les scénarios Node nommés.
- **HC-E1-33-04** — Gérer séparément entités natives, budgets d’équipe et ressources ; aucune invocation assimilée implicitement à un troisième combattant.

Source intégrale : [section 33 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [data/fighters.json](../data/fighters.json), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json), [prototype/qa_v10/extensions_browser_results.json](../prototype/qa_v10/extensions_browser_results.json).

<a id="section-34"></a>

### Section 34 — Commandes, jauges et disponibilité

**Décision :** retenue · **Priorité :** P0 · **Prototype :** V10 partiel, logique et navigateur testés · **Assets :** `ui_partial`.

Le labo utilise des actions distinctes et une jauge équipe de 100, séparée de l’énergie individuelle à trois segments de la bible. Les nombres exacts V10 sont des réglages de simulation, pas des valeurs Halo.

- **HC-E1-34-01** — Distinguer TAUNT, ASSISTANCE, RELAIS, SUPER_DUO, FINISHER_EQUIPE et ORDRE_ENTITE avec commandes remappables.
- **HC-E1-34-02** — Définir seuil et priorité si appui court/long partagé ; fournir raccourcis non ambigus.
- **HC-E1-34-03** — Documenter capacité, initial, gain, coût, recharge, plafonds et conservation des jauges.
  Preuve logique partielle : Coûts/refus sans débit, plafond de gain par combo, exclusion assist/tag et gel pause/scène testés. Remappage et hitstop complet restent hors preuve.
- **HC-E1-34-04** — Séparer quantité, cooldown, charge et état du partenaire ; afficher refus sans dépense avant engagement.
  Preuve logique partielle : Coûts/refus sans débit, plafond de gain par combo, exclusion assist/tag et gel pause/scène testés. Remappage et hitstop complet restent hors preuve.
  Preuve navigateur partielle : Navigateur: bouton tag indisponible pendant assist; jauge diminuée exactement de 25 lors de l’assist. Les autres refus restent couverts seulement par les scénarios Node nommés.
- **HC-E1-34-05** — Réserver dépense atomiquement, définir remboursements/interruption et horloge pendant pause/hitstop/scène/réserve.
  Preuve logique partielle : Coûts/refus sans débit, plafond de gain par combo, exclusion assist/tag et gel pause/scène testés. Remappage et hitstop complet restent hors preuve.

Source intégrale : [section 34 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/fighters.json](../data/fighters.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json), [prototype/qa_v10/extensions_browser_results.json](../prototype/qa_v10/extensions_browser_results.json).

<a id="section-35"></a>

### Section 35 — Assistances ponctuelles

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 logique partielle testée · **Assets :** `assist_animation_missing`.

Une assistance est une intervention brève d’un membre admissible du roster. Les tirs et frappes de l’animation future doivent provenir de son kit et de l’équipement de la version choisie.

- **HC-E1-35-01** — Définir disponible, appel, arrivée, action, sortie, cooldown et branches touché/interrompu/KO.
  Preuve logique partielle : Cycle assist 18+6+24, impact logique, PV de réserve, interruption et récupération de 300 frames testés. Pas de collision spatiale, mur, projection ou animation assist.
- **HC-E1-35-02** — Fixer commande, coût, états d’appel, point d’arrivée, orientation, cible, délai, annonces et sortie.
  Preuve logique partielle : Cycle assist 18+6+24, impact logique, PV de réserve, interruption et récupération de 300 frames testés. Pas de collision spatiale, mur, projection ou animation assist.
- **HC-E1-35-03** — Définir vulnérabilité, dégâts de réserve, conséquences du KO actif/soutien et début du cooldown.
  Preuve logique partielle : Cycle assist 18+6+24, impact logique, PV de réserve, interruption et récupération de 300 frames testés. Pas de collision spatiale, mur, projection ou animation assist.
- **HC-E1-35-04** — Traiter murs, projections, transitions et géants ; un secours défensif a sa règle distincte.
- **HC-E1-35-05** — Éviter double gain de jauge si deux membres sont touchés ; prévoir exercice d’appel et punition.

Source intégrale : [section 35 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [data/fighters.json](../data/fighters.json), [data/animation_plan.json](../data/animation_plan.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-36"></a>

### Section 36 — Tag : changement réel de combattant

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 partiel, logique et navigateur testés · **Assets :** `tag_animation_missing`.

Le tag V10 doit transférer réellement la référence active et les commandes, sans recharger munitions ou équipements. Le relais après KO reste gratuit si un membre vivant est disponible.

- **HC-E1-36-01** — Séparer relais volontaire, de combo, secours, après KO et scénarisé avec restrictions explicites.
  Preuve logique partielle : Tag: transfert f18, reprise f36, coût15, KO gratuit, maintien des PV et du budget combo testés. Munitions, transformations, géométrie et projectiles persistants restent à intégrer.
- **HC-E1-36-02** — Fixer départ, entrée, orientation, positions, collision, vulnérabilité et frame de transfert puis de reprise.
  Preuve logique partielle : Tag: transfert f18, reprise f36, coût15, KO gratuit, maintien des PV et du budget combo testés. Munitions, transformations, géométrie et projectiles persistants restent à intégrer.
  Preuve navigateur partielle : Navigateur: action de relais change le membre contrôlé. Les frames 18/36 sont contrôlées dans le modèle Node, pas par une analyse image de chaque frame.
- **HC-E1-36-03** — Conserver vie, munitions, transformations, effets et récupérations ; documenter toute régénération de réserve.
  Preuve logique partielle : Tag: transfert f18, reprise f36, coût15, KO gratuit, maintien des PV et du budget combo testés. Munitions, transformations, géométrie et projectiles persistants restent à intégrer.
- **HC-E1-36-04** — Conserver historique et budgets de combo pendant changement d’attaquant.
  Preuve logique partielle : Tag: transfert f18, reprise f36, coût15, KO gratuit, maintien des PV et du budget combo testés. Munitions, transformations, géométrie et projectiles persistants restent à intégrer.
- **HC-E1-36-05** — Garder propriétaire et comportement de cible de chaque projectile ; aucune réattribution silencieuse au nouvel actif.

Source intégrale : [section 36 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [data/fighters.json](../data/fighters.json), [data/animation_plan.json](../data/animation_plan.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json), [prototype/qa_v10/extensions_browser_results.json](../prototype/qa_v10/extensions_browser_results.json).

<a id="section-37"></a>

### Section 37 — Techniques combinées et supers d'équipe

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 logique partielle testée · **Assets :** `duo_animation_missing`.

Les supers d’équipe sont des chorégraphies originales Halo Combats. Red Team fournit un premier duo cohérent par relation ; la super reste originale même si les participants sont alliés attestés.

- **HC-E1-37-01** — Fixer participants, versions, disponibilité, ressources, portée, commande et cible compatible.
  Preuve logique partielle : Super: ouverture touche/garde/raté, refus double engagement, interruption sans remboursement, scène sur touche seulement et cooldowns gelés testés. Portée, chorégraphie et morphologies finales absentes.
- **HC-E1-37-02** — Déclencher la scène longue seulement après ouverture confirmée ; définir garde, raté et interruption.
  Preuve logique partielle : Super: ouverture touche/garde/raté, refus double engagement, interruption sans remboursement, scène sur touche seulement et cooldowns gelés testés. Portée, chorégraphie et morphologies finales absentes.
- **HC-E1-37-03** — Mobiliser les deux membres sans assist/tag parallèle et fixer celui qui reste actif à la sortie.
  Preuve logique partielle : Super: ouverture touche/garde/raté, refus double engagement, interruption sans remboursement, scène sur touche seulement et cooldowns gelés testés. Portée, chorégraphie et morphologies finales absentes.
- **HC-E1-37-04** — Prévoir contribution réelle de chaque membre, caméra, sons, VFX, morphologies et positions finales.
- **HC-E1-37-05** — Prioriser paires attestées puis relais générique annoncé ; borner dégâts, gains et cooldowns pendant scène.
  Preuve logique partielle : Super: ouverture touche/garde/raté, refus double engagement, interruption sans remboursement, scène sur touche seulement et cooldowns gelés testés. Portée, chorégraphie et morphologies finales absentes.

Source intégrale : [section 37 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [data/fighters.json](../data/fighters.json), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-38"></a>

### Section 38 — Finishers d'équipe et fins dramatiques conditionnelles

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 logique partielle testée · **Assets :** `finisher_animation_missing`.

La conclusion privilégie une fin dramatique admissible, puis finisher d’équipe, individuel et victoire normale. Le laboratoire peut vérifier cette priorité sans produire la cinématique finale.

- **HC-E1-38-01** — Définir fenêtre, commande, participants vivants/disponibles, coût, cible, lieu et résultat.
  Preuve logique partielle : Finisher: fenêtre après victoire, partenaire vivant, compatibilité duo/ère/stage/adversaire et fallback sans changer résultat testés; skip super produit le même état. Scène artistique, galerie et toutes morphologies non livrées.
- **HC-E1-38-02** — Vérifier versions, chapitre, état du stage, dernière action et morphologie avant une scène spécifique.
  Preuve logique partielle : Finisher: fenêtre après victoire, partenaire vivant, compatibilité duo/ère/stage/adversaire et fallback sans changer résultat testés; skip super produit le même état. Scène artistique, galerie et toutes morphologies non livrées.
- **HC-E1-38-03** — Ne pas ressusciter un partenaire KO ; prévoir remplacement compatible si conditions manquent.
  Preuve logique partielle : Finisher: fenêtre après victoire, partenaire vivant, compatibilité duo/ère/stage/adversaire et fallback sans changer résultat testés; skip super produit le même état. Scène artistique, galerie et toutes morphologies non livrées.
- **HC-E1-38-04** — Ne pas modifier une victoire déjà acquise par une présentation ; distinguer fin alternative et chronologie principale.
  Preuve logique partielle : Finisher: fenêtre après victoire, partenaire vivant, compatibilité duo/ère/stage/adversaire et fallback sans changer résultat testés; skip super produit le même état. Scène artistique, galerie et toutes morphologies non livrées.
- **HC-E1-38-05** — Prévoir indices, codex, galerie, abrègement et même état final après passage de scène.
  Preuve logique partielle : Finisher: fenêtre après victoire, partenaire vivant, compatibilité duo/ère/stage/adversaire et fallback sans changer résultat testés; skip super produit le même état. Scène artistique, galerie et toutes morphologies non livrées.

Source intégrale : [section 38 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/fighters.json](../data/fighters.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-39"></a>

### Section 39 — Clashes et confrontations avec qte

**Décision :** differee · **Priorité :** P2 · **Prototype :** Non implémenté · **Assets :** `clash_animation_missing`.

Un clash de lames ou d’énergies est une mécanique proposée, pas une propriété universelle du lore. Retenir une variante sans QTE pour compétition ; QTE narratif facultatif à concevoir après les fondations.

- **HC-E1-39-01** — Distinguer échange, clash mécanique et clash cinématique ; seuls groupes d’attaques éligibles déclenchent le système.
- **HC-E1-39-02** — Définir simultanéité par ticks, phases, contact, orientation, portée, ressources et limite de fréquence.
- **HC-E1-39-03** — Fixer priorités avec projectile tiers, piège et assist ; aucune priorité implicite au joueur de gauche.
- **HC-E1-39-04** — Spécifier commande, fenêtre, succès, échec, double succès, égalité, absence, durée max et déconnexion.
- **HC-E1-39-05** — Gérer chrono, entités et reprise ; fournir commandes remappées, maintien alternatif et résolution sans QTE commune au mode.

Source intégrale : [section 39 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md).

<a id="section-40"></a>

### Section 40 — Movesets à entités indépendantes et objets placés

**Décision :** retenue · **Priorité :** P2 · **Prototype :** Non implémenté · **Assets :** `entity_art_missing`.

Étendre les kits aux équipements réellement associés à leur incarnation : objets placés ou installation, leurre quand attesté, IA comme soutien technique. Aucun personnage n’obtient tous les pouvoirs du système.

- **HC-E1-40-01** — Classifier compagnon à ordre, autonome, double, illusion, objet, piège, installation, zone ou projectile piloté.
- **HC-E1-40-02** — Identifier propriétaire et routage de commande, action en absence et simultanéité autorisée avec son corps.
- **HC-E1-40-03** — Décrire placement, armement, durée, coût, limite, visibilité, activation et contre-jeu.
- **HC-E1-40-04** — Gérer envoyé/placé/armé/actif/retour/récupéré/interrompu/détruit et règle de redéploiement à la limite.
- **HC-E1-40-05** — Vérifier capacité/version dans Halo ; les références Zato ou Bridget décrivent une architecture, pas des techniques transférables.

Source intégrale : [section 40 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [data/fighters.json](../data/fighters.json), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/projectiles_v10.json](../data/projectiles_v10.json).

<a id="section-41"></a>

### Section 41 — Projectiles persistants et règles communes aux entités

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Prototype V8 partiel · **Assets :** `projectile_art_missing`.

La grenade persistante sert de cas initial ; propriétaire, cible et impacts restent stables pendant assist, tag, KO ou transition. Les futurs effets de plasma/Needler conservent arme et incarnation.

- **HC-E1-41-01** — Conserver propriétaire, création/coût, position, orientation, trajectoire, durée, cibles, impacts et fin de vie.
- **HC-E1-41-02** — Définir destruction, traversée, réflexion et changement explicite de propriétaire avec attribution dégâts/jauge.
- **HC-E1-41-03** — Régler entité lors de propriétaire touché/projeté/réserve/transformé/KO, transition, nouvelle manche ou cinématique.
- **HC-E1-41-04** — Limiter présence par personnage et équipe ; une option graphique ne retire pas un objet dangereux.
- **HC-E1-41-05** — Partager historique combo, rebonds et gains entre actif, assist et entités ; restaurer sans doublon après correction.

Source intégrale : [section 41 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [data/fighters.json](../data/fighters.json), [prototype/lab_v8/app.js](../prototype/lab_v8/app.js), [data/projectiles_v10.json](../data/projectiles_v10.json).

<a id="section-42"></a>

### Section 42 — Stages bonus et épreuves intégrées aux histoires

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 partiel, logique et navigateur testés · **Assets :** `bonus_art_missing`.

Retenir précision et coordination pour une première épreuve de labo. Les futures casses d’épave, hordes et extractions se situent en exercices ou scènes justifiées ; un Hunter n’est pas réduit à une cible fragile sans adaptation annoncée.

- **HC-E1-42-01** — Relier chaque bonus à une route ou un chapitre, avec rôle narratif/pédagogique et caractère facultatif ou obligatoire.
- **HC-E1-42-02** — Définir capacités admises, objectif, temps, réussite/échec, score, rang, récompense et état transmis.
  Preuve logique partielle : Bonus logique de précision: cibles uniques, temps, réussite/échec, résultat final idempotent et nouvelle tentative sans perte testés. Les dix familles, routes, rangs et assets ne sont pas tous implémentés.
  Preuve navigateur partielle : Navigateur: exercice de précision terminé par activation des boutons réels; le résultat enregistré survit au rechargement. Aucune horde ni campagne complète testée.
- **HC-E1-42-03** — Prévoir familles destruction, horde, précision, défense, mobilité, extraction, interaction, entité, coordination et culture si pertinentes.
  Preuve logique partielle : Bonus logique de précision: cibles uniques, temps, réussite/échec, résultat final idempotent et nouvelle tentative sans perte testés. Les dix familles, routes, rangs et assets ne sont pas tous implémentés.
- **HC-E1-42-04** — Pour horde, contrôler apparition, densité, collisions, ressources limitées, nettoyage et performances.
- **HC-E1-42-05** — Conserver reprise, difficulté, aides et attribution unique ; échec facultatif ne bloque pas arbitrairement l’histoire.
  Preuve logique partielle : Bonus logique de précision: cibles uniques, temps, réussite/échec, résultat final idempotent et nouvelle tentative sans perte testés. Les dix familles, routes, rangs et assets ne sont pas tous implémentés.

Source intégrale : [section 42 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/stages.json](../data/stages.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json), [prototype/qa_v10/extensions_browser_results.json](../prototype/qa_v10/extensions_browser_results.json).

<a id="section-43"></a>

### Section 43 — Espace d'exploration et de déblocage inspiré de la krypt

**Décision :** retenue · **Priorité :** P2 · **Prototype :** V10 logique partielle testée · **Assets :** `hub_art_missing`.

Étendre Archives de combat en espace de consultation et de collection original au projet : accueil, armurerie, dossiers d’opérations, cartographie et salle des trophées. Le mot Krypt désigne l’inspiration fonctionnelle, pas un lieu Halo.

- **HC-E1-43-01** — Définir nom, rôle, avatar, format de navigation et carte de zones réellement reliées.
- **HC-E1-43-02** — Relier indices, accès, objets, épreuves et récompenses aux histoires, bonus et boss.
- **HC-E1-43-03** — Privilégier acquisitions ciblées, gérer doublons et alternative aux récompenses essentielles si hasard retenu.
- **HC-E1-43-04** — Vérifier portes, mécanismes, connaissances, absence de cycle clé/récompense et reprise.
  Preuve logique partielle : Trois prérequis abstraits d’archives sans cycle ni attribution répétée testés. Ce graphe de données ne constitue pas un hub jouable.
- **HC-E1-43-05** — Séparer collection, entraînement, versus et compétition ; aucun bonus de statistiques caché.

Source intégrale : [section 43 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/stages.json](../data/stages.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-44"></a>

### Section 44 — Cohérence narrative, relations et compatibilités

**Décision :** retenue · **Priorité :** P0 · **Prototype :** V10 logique partielle testée · **Assets :** `team_art_missing`.

Les paires ont deux statuts indépendants: relation attestée et scène produite. Jerome/Alice HW2 constitue une relation attestée ; une confrontation à Blood Gulch CE reste une simulation inter-époques, et Chief Infinite/Arbiter H3 n’est pas une scène historique.

- **HC-E1-44-01** — Définir période, versions, relation, motivation, connaissance mutuelle, techniques et confiance pour chaque duo.
- **HC-E1-44-02** — Autoriser en campagne seulement partenaires présents à ce stade ; justifier soutien distant par moyens attestés.
- **HC-E1-44-03** — Étiqueter libre versus, alternatif et crossover ; séparer Silver du canon principal.
  Preuve logique partielle : Filtre de continuité principal/Silver/Fractures et version d’œuvre testé. Aucune rencontre historique ni relation supplémentaire n’est créée par ce filtre.
- **HC-E1-44-04** — Prioriser associations utiles et chiffrer paires ordonnées/non ordonnées avec variantes.
- **HC-E1-44-05** — Relier bonus et récompenses au rythme narratif ; ne pas imposer une scène exclusive à chaque combinaison.

Source intégrale : [section 44 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/fighters.json](../data/fighters.json), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-45"></a>

### Section 45 — Assets, animations, sons et mise en scène

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Document / référence · **Assets :** `animation_missing`.

Étendre le plan d’assets avec taunt, sélection/désélection, assist, tag, duo, entités, bonus et exploration. Aucun compteur de clips ne monte tant que des frames et transitions réelles ne sont pas produites.

- **HC-E1-45-01** — Pour personnage: entrer/tenir/sortir taunt, sélection, confirmation, attente, désélection, assist et tag.
- **HC-E1-45-02** — Pour équipe et entité: poses, dialogues, super, finisher, victoire, apparition/ordre/rappel/destruction et effets.
- **HC-E1-45-03** — Pour bonus et hub: décor, objectifs, états, ennemis, score, carte, portes, indices et récompenses.
- **HC-E1-45-04** — Conserver ancrages, contacts, asymétries, cadrage, durée, VFX/SFX et variantes nécessaires.
- **HC-E1-45-05** — Garder un sujet par source autonome ; séparer storyboard collectif, pose clé et clip intégré au combat.

Source intégrale : [section 45 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [data/animation_plan.json](../data/animation_plan.json), [data/asset_manifest_v9.json](../data/asset_manifest_v9.json).

<a id="section-46"></a>

### Section 46 — Interface, apprentissage, accessibilité et réseau

**Décision :** retenue · **Priorité :** P0 · **Prototype :** V10 logique partielle testée · **Assets :** `ui_partial`.

Le HUD extensions montre actif/réserve, jauge d’équipe, cooldown et refus. Le labo expose ses états sans annoncer un système réseau ou une capture animée qui n’existe pas.

- **HC-E1-46-01** — Hiérarchiser composition, vie de réserve, jauge, récupérations, ressources de kit et raisons d’indisponibilité.
- **HC-E1-46-02** — Prévoir exercices assist/tag/super/clash/entité et configuration de toutes leurs conditions.
- **HC-E1-46-03** — Assurer commandes remappées, sous-titres, mouvement réduit, caméra contrôlable et aides PvP compatibles.
- **HC-E1-46-04** — Pour réseau futur, synchroniser décisions sur simulation, pas sur durée locale de rendu.
- **HC-E1-46-05** — Après correction ou scène abrégée, préserver état final sans voix, jauge, entité ou récompense doublée.
  Preuve logique partielle : Abrègement du super et attente complète produisent le même état logique. Aucun rollback réseau, restitution audio ou VFX testé.

Source intégrale : [section 46 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [prototype/lab_v8/app.js](../prototype/lab_v8/app.js), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-47"></a>

### Section 47 — Validation, statistiques et ordre d'intégration

**Décision :** retenue · **Priorité :** P0 · **Prototype :** V10 logique partielle testée · **Assets :** `not_applicable`.

La validation V10 sera rattachée à ses nouveaux fichiers et non aux rapports V8. Les 18 cas de la source deviennent des scénarios de couverture ; les cas hors prototype restent à tester.

- **HC-E1-47-01** — Compter séparément taunts, sélection, assist/tag, duo, finisher, clash, entité, bonus et zones.
- **HC-E1-47-02** — Tester navigation rapide, taunt interrompu, assist/tag simultanés, double dépense, KO et super bloquée/ratée.
  Preuve logique partielle : Sous-ensemble de 30 scénarios Node identifié et exécuté: conflits, KO, branches super, bonus et sauvegarde. Les 18 cas complets du guide ne sont pas tous couverts.
- **HC-E1-47-03** — Tester scène incompatible, tiers pendant clash, QTE sans réponse, entité après KO et transition de stage.
- **HC-E1-47-04** — Tester réflexion, boucles infinies, densité horde, résultat bonus, sauvegarde et scène abrégée.
  Preuve logique partielle : Sous-ensemble de 30 scénarios Node identifié et exécuté: conflits, KO, branches super, bonus et sauvegarde. Les 18 cas complets du guide ne sont pas tous couverts.
- **HC-E1-47-05** — Conserver preuve par scénario, version et niveau de test ; différencier relais générique et chorégraphie exclusive.
  Preuve logique partielle : Sous-ensemble de 30 scénarios Node identifié et exécuté: conflits, KO, branches super, bonus et sauvegarde. Les 18 cas complets du guide ne sont pas tous couverts.

Source intégrale : [section 47 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [prototype/qa_v8/results.json](../prototype/qa_v8/results.json), [prototype/qa_v9/results.json](../prototype/qa_v9/results.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-48"></a>

### Section 48 — Dix fiches de production complémentaires

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Document / référence · **Assets :** `not_applicable`.

Les dix fiches Extension 01 sont conservées et leurs premières adaptations représentatives sont consignées dans cette annexe. Les fiches restant à décliner par personnage sont explicitement des travaux futurs.

- **HC-E1-48-01** — Renseigner taunt et sélection/désélection avec états, timing, nettoyage, confort et critères.
- **HC-E1-48-02** — Renseigner profil équipe, assist/tag, super/finisher/dramatique avec ressources, participants et compatibilités.
- **HC-E1-48-03** — Renseigner clash/QTE et entité/objet/projectile avec événements simultanés, propriétaires et restitution.
- **HC-E1-48-04** — Renseigner bonus, lieu exploratoire et règle/récompense avec progression, doublons, sauvegarde et preuves.

Source intégrale : [section 48 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/fighters.json](../data/fighters.json), [data/projectiles_v10.json](../data/projectiles_v10.json).

<a id="section-49"></a>

### Section 49 — Instruction d'intégration et références

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Document / référence · **Assets :** `not_applicable`.

L’Extension 01 complète le guide général dans la bible Halo. Les sources d’inspiration restent attachées à leurs épisodes et aucune de leurs règles n’est attribuée automatiquement à Halo.

- **HC-E1-49-01** — Relier chaque rubrique aux identifiants du roster, aux scènes, stages, progressions et inventaires.
- **HC-E1-49-02** — Conserver les sources et leur portée, notamment distinction MK assist, Tekken tag, DBFZ fin dramatique et Naruto clash.
- **HC-E1-49-03** — Respecter phase fixe, sujet unique et bilans documenté/produit/intégré/testé ; garder les limites visibles.

Source intégrale : [section 49 du guide](guides_combat/Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [docs/source_registry.json](source_registry.json).

<a id="section-50"></a>

### Section 50 — Portée, principes et raccordement aux guides

**Décision :** retenue · **Priorité :** P0 · **Prototype :** V10 à vérifier · **Assets :** `lock_ui_partial`.

L’Extension 02 s’applique aux combattants, partenaires, costumes, stages et modes retenus. Le verrou indique une règle d’accès ; l’absence de fichier reste une panne ou une production manquante.

- **HC-E2-50-01** — Décider périmètre, adaptation et priorité de chaque catégorie ; justifier les fonctions non retenues.
- **HC-E2-50-02** — Conserver statut de fidélité, incarnation et provenance des récompenses, y compris celles dédiées aux soutiens.
- **HC-E2-50-03** — Relier sélection, équipe, bonus et exploration au même catalogue.
- **HC-E2-50-04** — Distinguer prévu/conçu/produit/intégré/testé/livré ; ne pas cacher un système inachevé derrière un cadenas.

Source intégrale : [section 50 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json).

<a id="section-51"></a>

### Section 51 — États de découverte, de droit et de disponibilité

**Décision :** retenue · **Priorité :** P0 · **Prototype :** V10 partiel, logique et navigateur testés · **Assets :** `lock_ui_partial`.

Le modèle utilise quatre axes: découverte, droit, présence/compatibilité des fichiers et admissibilité dans le mode. Le labo doit pouvoir montrer une acquisition dont le PNG manque sans faux verrou d’abonnement.

- **HC-E2-51-01** — Découverte: secret, indice ou identifié ; un secret complet ne révèle pas la silhouette.
  Preuve logique partielle : États logiques séparés découverte/droits/assets/contexte: secret neutre, attente, permanent, temporaire expiré, dépendance et incompatibilité testés. Fichiers installables et tous messages navigateur restent hors preuve.
  Preuve navigateur partielle : Navigateur: texte accessible du dossier secret reste neutre, carte et détail n’exposent pas d’image. Les voix, bios et autres canaux anti-spoiler restent à étendre.
- **HC-E2-51-02** — Droit: absent, prêt à réclamer, permanent, temporaire, vérification en attente ou terminé, avec source connue.
  Preuve logique partielle : États logiques séparés découverte/droits/assets/contexte: secret neutre, attente, permanent, temporaire expiré, dépendance et incompatibilité testés. Fichiers installables et tous messages navigateur restent hors preuve.
- **HC-E2-51-03** — Technique: installé compatible, installation/mise à jour requise ou erreur ; indépendant du droit.
  Preuve logique partielle : États logiques séparés découverte/droits/assets/contexte: secret neutre, attente, permanent, temporaire expiré, dépendance et incompatibilité testés. Fichiers installables et tous messages navigateur restent hors preuve.
  Preuve navigateur partielle : Navigateur: droit gagné sans visuel produit reste non sélectionnable. Un vrai échec de chargement PNG affiche un état technique distinct, bloque le lancement et conserve le droit acquis. Le gestionnaire d’installation d’un jeu complet n’est pas livré.
- **HC-E2-51-04** — Mode/composition: autorisé ou incompatible, avec raisons et prochaine action utile.
  Preuve logique partielle : États logiques séparés découverte/droits/assets/contexte: secret neutre, attente, permanent, temporaire expiré, dépendance et incompatibilité testés. Fichiers installables et tous messages navigateur restent hors preuve.
- **HC-E2-51-05** — Afficher obstacles cumulés, dépendance de costume et libellés sans annoncer un droit permanent s’il peut expirer.
  Preuve logique partielle : États logiques séparés découverte/droits/assets/contexte: secret neutre, attente, permanent, temporaire expiré, dépendance et incompatibilité testés. Fichiers installables et tous messages navigateur restent hors preuve.

Source intégrale : [section 51 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json), [prototype/qa_v10/extensions_browser_results.json](../prototype/qa_v10/extensions_browser_results.json).

<a id="section-52"></a>

### Section 52 — Langage visuel adapté au lore

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 logique partielle testée · **Assets :** `lock_ui_partial`.

La charte choisit dossiers masqués, cadres cyan/acier et autorisation de simulation. Cette métaphore d’interface est originale, pas une nouvelle institution canonique contrôlant les accès des factions.

- **HC-E2-52-01** — Associer aperçu, icône, texte, chemin de progression et focus lisible.
- **HC-E2-52-02** — Silhouette noire avec contour/fond contrasté pour indice ; emblème neutre pour secret intégral.
  Preuve logique partielle : État secret renvoie nom neutre et aucun asset; indice demande silhouette. Aspect, contraste et focus doivent être revus dans le navigateur.
- **HC-E2-52-03** — Définir repos, focus, refus, récompense prête, ouverture et désélection, avec variante sans mouvement.
- **HC-E2-52-04** — Éviter flash et son seuls ; ne pas vendre l’option statique ni imposer une cinématique à chaque retour.
- **HC-E2-52-05** — Vérifier écriture, matériaux et symboles ; qualifier les éléments décoratifs originaux sans les présenter comme artefacts officiels.

Source intégrale : [section 52 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-53"></a>

### Section 53 — Emplacements de personnages et partenaires

**Décision :** retenue · **Priorité :** P0 · **Prototype :** V10 partiel, logique et navigateur testés · **Assets :** `lock_ui_partial`.

Les slots verrouillés restent consultables et ouvrent une fiche utile. Le random n’inclut que les candidats utilisables ; compagnon natif indispensable et partenaire du roster ne partagent pas le même droit.

- **HC-E2-53-01** — Afficher identité permise, portrait/masque, condition courte/détaillée, progression et action utile.
- **HC-E2-53-02** — Garder focus sur verrou mais refuser ajout à équipe ; expliquer sans boucle de messages.
  Preuve logique partielle : Un slot verrouillé reste inspectable et son choix est refusé; sélection dépend des droits, fichiers et contexte. Le focus visuel, tous prêts narratifs et le partage natif des kits ne sont pas validés.
  Preuve navigateur partielle : Navigateur: le dossier Arbiter verrouillé ne peut pas être ajouté à la sélection. Pas de validation de tous les appareils ou de toutes les variantes de focus.
- **HC-E2-53-03** — Après acquisition, révéler et activer si fichiers/conditions prêts ; sinon indiquer installation ou dépendance.
  Preuve logique partielle : Un slot verrouillé reste inspectable et son choix est refusé; sélection dépend des droits, fichiers et contexte. Le focus visuel, tous prêts narratifs et le partage natif des kits ne sont pas validés.
  Preuve navigateur partielle : Navigateur: droit gagné sans visuel produit reste non sélectionnable. Un vrai échec de chargement PNG affiche un état technique distinct, bloque le lancement et conserve le droit acquis. Le gestionnaire d’installation d’un jeu complet n’est pas livré.
- **HC-E2-53-04** — Définir partage des droits entre personnage, version, assist, forme et kit natif ; ne pas retirer un composant indispensable.
- **HC-E2-53-05** — Séparer droit individuel, compatibilité de duo, scène secrète et prêt narratif de chapitre.
  Preuve logique partielle : Un slot verrouillé reste inspectable et son choix est refusé; sélection dépend des droits, fichiers et contexte. Le focus visuel, tous prêts narratifs et le partage natif des kits ne sont pas validés.

Source intégrale : [section 53 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/fighters.json](../data/fighters.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json), [prototype/qa_v10/extensions_browser_results.json](../prototype/qa_v10/extensions_browser_results.json).

<a id="section-54"></a>

### Section 54 — Costumes, palettes et accessoires

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 logique partielle testée · **Assets :** `costume_art_partial`.

Les costumes conservent leur œuvre et leur période. La version ODST de Buck et la version Spartan Halo 5 ne deviennent pas interchangeables dans une scène 2552 ; les variations de kit demandent des profils distincts.

- **HC-E2-54-01** — Fixer politique d’aperçu complet/partiel/secret, provenance et mode d’obtention pour chaque costume.
- **HC-E2-54-02** — Distinguer aperçu et droit d’équipement ; retourner proprement à l’apparence autorisée.
- **HC-E2-54-03** — Conserver une récompense obtenue avant son personnage avec dépendance explicite et anti-spoiler cohérent.
  Preuve logique partielle : Costume acquis avant parent conservé comme droit permanent, avec dépendance explicite et choix refusé tant que parent indisponible.
- **HC-E2-54-04** — Gérer palettes/accessoires, ensembles partiels et doublons sans perte ni renouvellement artificiel.
- **HC-E2-54-05** — Garantir mêmes collisions/timings/ressources pour skin cosmétique ; variante de gameplay explicite si capacité change.

Source intégrale : [section 54 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/asset_manifest_v9.json](../data/asset_manifest_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-55"></a>

### Section 55 — Stages, variantes et destinations

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 à vérifier · **Assets :** `stage_art_partial`.

Séparer droit du lieu, ambiance, période, interactions et destination reliée. La miniature d’une version détruite peut être masquée jusqu’à découverte ; l’option statique fait partie du même accès de confort.

- **HC-E2-55-01** — Définir aperçu, verrou, condition et identité anti-spoiler pour stage et variante.
- **HC-E2-55-02** — Conserver accès aux présentations vivante/statique avec géométrie et signaux identiques lorsque purement visuelles.
- **HC-E2-55-03** — Pour futur stage soutien: documenter provenance, qui choisit, qui participe, entraînement et admission compétitive.
- **HC-E2-55-04** — Précharger assets et destinations de transition pour tous les participants ou choisir un remplacement commun avant match.
- **HC-E2-55-05** — Aucun habillage payant ne change avantage de camouflage, collisions ou symétrie des interactions.

Source intégrale : [section 55 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/stages.json](../data/stages.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json).

<a id="section-56"></a>

### Section 56 — Modes de jeu et parcours verrouillés

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 logique partielle testée · **Assets :** `mode_art_missing`.

Boss Rush et défis avancés peuvent devenir récompenses de progression lorsqu’ils sont fonctionnels. Un Boss Rush seulement planifié reste identifié comme non implémenté, même si sa condition est conçue.

- **HC-E2-56-01** — Définir modes/rosters concernés, conditions, description, progression et lien vers activité utile.
- **HC-E2-56-02** — Préserver réglages, accessibilité et apprentissage nécessaire aux mécaniques déjà jouables.
- **HC-E2-56-03** — Détecter cycles directs et indirects entre mode, personnage, stage et ressource.
  Preuve logique partielle : Préconditions abstraites des archives contrôlées sans cycle. Audit complet modes/personnages/stages et leurs ressources à étendre.
- **HC-E2-56-04** — Séparer maintenance/absence de fichiers d’un verrou de progression.
- **HC-E2-56-05** — Si mode soutien retenu plus tard, décrire accès, échéance, progression conservée et récompenses avant activation.

Source intégrale : [section 56 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-57"></a>

### Section 57 — Conditions de déblocage et progression

**Décision :** retenue · **Priorité :** P0 · **Prototype :** V10 logique partielle testée · **Assets :** `not_applicable`.

Les règles d’accès emploient IDs stables et expressions ET/OU explicites. Une voie gagnée en jeu reste valide après expiration d’une autre source temporaire.

- **HC-E2-57-01** — Identifier règle, contenus accordés, événements admissibles, compteur, objectif et périmètre profil/compte/sauvegarde/période.
  Preuve logique partielle : Conditions mesurables, branches ET/OU et sources indépendantes testées, dont acquisition permanente pendant fenêtre temporaire. Autorité de compte et événements distants absents.
- **HC-E2-57-02** — Afficher alternatives ET/OU fidèles sans transformer une voie gratuite OU soutien en obligation cumulée.
  Preuve logique partielle : Conditions mesurables, branches ET/OU et sources indépendantes testées, dont acquisition permanente pendant fenêtre temporaire. Autorité de compte et événements distants absents.
- **HC-E2-57-03** — Conserver les sources d’accès indépendantes et calculer droit effectif à partir de leurs validités.
  Preuve logique partielle : Conditions mesurables, branches ET/OU et sources indépendantes testées, dont acquisition permanente pendant fenêtre temporaire. Autorité de compte et événements distants absents.
- **HC-E2-57-04** — Définir difficulté, reprise, reset, abandon, dates et alternatives aux événements terminés.
- **HC-E2-57-05** — Détecter dépendances impossibles ; rétroactivité seulement à partir d’événements réellement enregistrés.

Source intégrale : [section 57 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-58"></a>

### Section 58 — Exploration, récompenses et scène de révélation

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 partiel, logique et navigateur testés · **Assets :** `reveal_art_missing`.

Le casier ou dossier des Archives référence le même ID que le menu, sans créer un second costume. Sauvegarder l’attribution avant la présentation afin de résister à une fermeture de l’écran.

- **HC-E2-58-01** — Décrire lieu, clé, condition, coût, contenu, découverte et état après ouverture.
- **HC-E2-58-02** — Choisir attribution automatique, réclamation ou découverte ; afficher prêt uniquement si une réclamation existe.
  Preuve logique partielle : Réclamation disponible calculée et attribution idempotente locale testées. Aucun achat, devise réelle ou double facturation fournisseur testé.
  Preuve navigateur partielle : Navigateur: Arbiter réclamé après condition devient sélectionnable; bouton de réclamation et droit effectif sont raccordés. Aucun achat ni fournisseur externe testé.
- **HC-E2-58-03** — Permettre de passer la scène sans perdre récompense ; atomiser coût et acquisition.
- **HC-E2-58-04** — Empêcher double facturation/double lot et annoncer politique si récompense déjà acquise autrement.
  Preuve logique partielle : Réclamation disponible calculée et attribution idempotente locale testées. Aucun achat, devise réelle ou double facturation fournisseur testé.
- **HC-E2-58-05** — Si galerie soutien, distinguer source externe et métaphore fictionnelle ; aucun personnage Halo ne souscrit narrativement à Patreon.

Source intégrale : [section 58 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json), [prototype/qa_v10/extensions_browser_results.json](../prototype/qa_v10/extensions_browser_results.json).

<a id="section-59"></a>

### Section 59 — Contenus dédiés aux abonnés et modèles d'acquisition

**Décision :** differee · **Priorité :** P2 · **Prototype :** Non implémenté · **Assets :** `supporter_art_missing`.

Documenter une architecture optionnelle de récompenses cosmétiques de soutien. Aucune offre, campagne, prix, niveau, produit ou monétisation opérationnelle n’est créé dans cette passe.

- **HC-E2-59-01** — Définir par avantage un modèle permanent, catalogue temporaire ou livraison par période et sa version.
- **HC-E2-59-02** — Fixer événement d’admissibilité, durée, lots inclus, essais/cadeaux/gratuit et dépendances.
- **HC-E2-59-03** — Annoncer exclusivité, éventuelles autres voies, plateformes et validité réelle avant engagement.
- **HC-E2-59-04** — Conserver les avantages par IDs stables même si nom/prix de l’offre change ; préserver acquisitions promises.
- **HC-E2-59-05** — Vérifier autorisations des assets avant une éventuelle offre ; un vêtement créé reste original compatible, pas canon par paiement.

Source intégrale : [section 59 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json).

<a id="section-60"></a>

### Section 60 — Liaison avec patreon ou un service équivalent

**Décision :** differee · **Priorité :** P2 · **Prototype :** Non implémenté · **Assets :** `not_applicable`.

Le connecteur Patreon ou équivalent reste hors implémentation V10. Le prototype ne lit aucun compte réel, jeton ni paiement ; ses scénarios temporaires sont uniquement des données de test.

- **HC-E2-60-01** — Créer uniquement après décision un parcours volontaire OAuth officiel, jamais une demande de mot de passe dans le jeu.
- **HC-E2-60-02** — Vérifier droits côté service de confiance, garder secrets hors client et limiter les données aux avantages nécessaires.
- **HC-E2-60-03** — Mapper fournisseur/campagne/compte/niveaux à avantages ; compte lié ne suffit pas à prouver un achat.
- **HC-E2-60-04** — Valider origine des événements, doublons, ordre et réconciliation ; prévoir resynchronisation et service inaccessible.
- **HC-E2-60-05** — Distinguer changement de compte, déliaison, annulation et suppression ; revérifier documentation fournisseur à l’implémentation.

Source intégrale : [section 60 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Aucune preuve d’implémentation dans le point de départ inspecté ; la spécification reste dans cette annexe et son original.

<a id="section-61"></a>

### Section 61 — Expiration, changements d'accès et fonctionnement hors ligne

**Décision :** retenue · **Priorité :** P0 · **Prototype :** V10 logique partielle testée · **Assets :** `not_applicable`.

Le calcul local de droits doit distinguer expiration confirmée, état inconnu et acquisition permanente. En production, une partie déjà autorisée garde sa configuration jusqu’au résultat.

- **HC-E2-61-01** — Ne retirer que la source temporaire expirée ou révoquée ; conserver une source permanente ou alternative encore valide.
  Preuve logique partielle : Expiration/révocation d’une source temporaire laisse une source permanente active; vérification en attente reste inconnue et ancien événement est ignoré. Modèle de données local uniquement.
- **HC-E2-61-02** — Annulation, baisse de niveau, remboursement et traitement en attente suivent date et preuve effectives.
- **HC-E2-61-03** — Panne de service = vérification indisponible, pas abonnement terminé ; aucune invention d’un droit nouveau.
  Preuve logique partielle : Expiration/révocation d’une source temporaire laisse une source permanente active; vérification en attente reste inconnue et ancien événement est ignoré. Modèle de données local uniquement.
- **HC-E2-61-04** — Définir justificatif hors ligne, durée/tolérance et reconnexion sans effacer sauvegarde.
- **HC-E2-61-05** — Appliquer changement après match ; préserver préférences, progression et historique et annoncer remplacement d’un costume/partenaire.

Source intégrale : [section 61 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-62"></a>

### Section 62 — Sélection locale, multijoueur, entraînement et replays

**Décision :** retenue · **Priorité :** P1 · **Prototype :** V10 logique partielle testée · **Assets :** `not_applicable`.

Séparer consulter, équiper, participer et entraîner. Le modèle est vérifié localement ; aucune politique multijoueur, replay ou invitation n’est déclarée opérationnelle sans moteur correspondant.

- **HC-E2-62-01** — Définir politique par profil principal, second joueur, invité et compte connecté.
- **HC-E2-62-02** — Distinguer possession du fichier, droit de sélection, participation à un stage et accès d’entraînement.
  Preuve logique partielle : Droit et asset restent séparés; composition invalide refusée et tirage aléatoire exclut contenu inaccessible/doublons. Profils invités, online, transitions et replays non testés.
- **HC-E2-62-03** — Valider avant match droits, installation, versions, composition et destination ; fournir remplacement annoncé.
  Preuve logique partielle : Droit et asset restent séparés; composition invalide refusée et tirage aléatoire exclut contenu inaccessible/doublons. Profils invités, online, transitions et replays non testés.
- **HC-E2-62-04** — Conserver équipes sauvegardées, exclure random invalide et ne remplacer que le contenu inaccessible.
  Preuve logique partielle : Droit et asset restent séparés; composition invalide refusée et tirage aléatoire exclut contenu inaccessible/doublons. Profils invités, online, transitions et replays non testés.
- **HC-E2-62-05** — Documenter replays et assets non possédés/anciens sans dépendre du seul abonnement actuel ; signaler incompatibilité réelle.

Source intégrale : [section 62 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-63"></a>

### Section 63 — Interface, textes, accessibilité et protection des surprises

**Décision :** retenue · **Priorité :** P0 · **Prototype :** V10 partiel, logique et navigateur testés · **Assets :** `lock_ui_partial`.

Un dossier secret ne révèle nom, image, silhouette ni texte accessible avant la condition prévue. Les messages séparent récompense, installation, incompatibilité et vérification ; l’interface n’invente pas de fin d’abonnement.

- **HC-E2-63-01** — Afficher identité permise, aperçu, état, voie, progression, dépendances, validité connue et prochaine action.
- **HC-E2-63-02** — Présenter toutes les alternatives ; aucune redirection de soutien imposée pour une voie gratuite existante.
- **HC-E2-63-03** — Tester icône/forme/texte, contraste, focus clavier/manette, lecteur d’écran et réduction des mouvements.
- **HC-E2-63-04** — Appliquer anti-spoiler aux noms, silhouettes, voix, bios, notifications, descriptions et tooltips.
  Preuve logique partielle : Secret: nom, image et titre d’œuvre neutralisés dans la réponse du modèle. Tous tooltips, voix, bios, notifications et lecteur d’écran restent à contrôler.
  Preuve navigateur partielle : Navigateur: texte accessible du dossier secret reste neutre, carte et détail n’exposent pas d’image. Les voix, bios et autres canaux anti-spoiler restent à étendre.
- **HC-E2-63-05** — Annoncer portée anti-spoiler en versus ; voir un adversaire peut révéler son apparence sans accorder sa possession.

Source intégrale : [section 63 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [prototype/universe_v9/app.js](../prototype/universe_v9/app.js), [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json), [prototype/qa_v10/extensions_browser_results.json](../prototype/qa_v10/extensions_browser_results.json).

<a id="section-64"></a>

### Section 64 — Production, sauvegarde et critères de validation

**Décision :** retenue · **Priorité :** P0 · **Prototype :** V10 partiel, logique et navigateur testés · **Assets :** `lock_ui_partial`.

Versionner catalogue et sources d’acquisition. Le laboratoire local sert à tester les transitions et l’idempotence ; les 22 cas de la source restent la matrice complète de réception.

- **HC-E2-64-01** — Conserver IDs, versions, lore, dépendances, découverte, règles et noms localisés séparément.
  Preuve logique partielle : IDs uniques, grants versionnés, doublons/ordre, format local et données inconnues testés. 30 tests partiels ne remplacent pas les 22 cas exhaustifs de la source ni une autorité serveur.
- **HC-E2-64-02** — Par source: origine, permanence, événement, validité, dernière vérification et motif de retrait.
  Preuve logique partielle : IDs uniques, grants versionnés, doublons/ordre, format local et données inconnues testés. 30 tests partiels ne remplacent pas les 22 cas exhaustifs de la source ni une autorité serveur.
- **HC-E2-64-03** — Attribuer une seule fois malgré double clic, reprise ou événement répété ; conserver migration, restauration et autorité du mode.
  Preuve logique partielle : IDs uniques, grants versionnés, doublons/ordre, format local et données inconnues testés. 30 tests partiels ne remplacent pas les 22 cas exhaustifs de la source ni une autorité serveur.
  Preuve navigateur partielle : Navigateur: progrès et sélection conservés après rechargement, annulation de reset sans perte, seule la clé de ce laboratoire effacée au reset confirmé, sauvegarde corrompue conservée. Pas de migration complète ou compte distant testé.
- **HC-E2-64-04** — Produire silhouettes, révélés, cadres, icônes, focus/refus/déblocage, sons et variantes accessibles séparément des combattants.
- **HC-E2-64-05** — Vérifier les 22 cas de la source sur texte, action, droit, sauvegarde et poursuite de jeu ; compter production et acquisitions séparément.
  Preuve logique partielle : IDs uniques, grants versionnés, doublons/ordre, format local et données inconnues testés. 30 tests partiels ne remplacent pas les 22 cas exhaustifs de la source ni une autorité serveur.

Source intégrale : [section 64 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/asset_manifest_v9.json](../data/asset_manifest_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json), [prototype/qa_v10/extensions_browser_results.json](../prototype/qa_v10/extensions_browser_results.json).

<a id="section-65"></a>

### Section 65 — Six fiches de production à remplir

**Décision :** retenue · **Priorité :** P1 · **Prototype :** Document / référence · **Assets :** `not_applicable`.

Les six fiches d’accès sont conservées intégralement et déclinées en fiches représentatives dans cette annexe ; les modèles soutien restent de conception tant qu’aucun fournisseur n’est raccordé.

- **HC-E2-65-01** — Renseigner contenu/slot et règle de déblocage avec secret, ET/OU, événements, coût, autorité et critères.
- **HC-E2-65-02** — Renseigner avantage de soutien avec modèle, preuve, permanence, exceptions, alternatives et politique de fin.
- **HC-E2-65-03** — Renseigner charte visuelle avec métaphore, grammaire, accessibilité et risque spoiler.
- **HC-E2-65-04** — Renseigner scénario stage et matrice de droits selon profils, sources, installation, contexte et sauvegarde.

Source intégrale : [section 65 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json).

<a id="section-66"></a>

### Section 66 — Instruction prête à transmettre à un projet

**Décision :** retenue · **Priorité :** P0 · **Prototype :** V10 logique partielle testée · **Assets :** `not_applicable`.

Cette annexe relie les deux extensions au guide et à la bible, tout en laissant visibles décisions différées et fonctions non encore produites.

- **HC-E2-66-01** — Intégrer slots cohérents, véritable secret, conditions, dépendances, attribution, textes et règles par contexte.
  Preuve logique partielle : Raccord partiel des états de slot et des droits permanents au laboratoire; preuves Node rattachées aux exigences. Pas de jeu complet, clips, service d’abonnement ou validation visuelle déduite.
- **HC-E2-66-02** — Relier histoires, campagne, bonus, défis et exploration sans cycle ni double récompense.
- **HC-E2-66-03** — Préserver propriétés des cosmétiques, confort des stages et droits permanents ; décrire options soutien sans prétendre à un service actif.
  Preuve logique partielle : Raccord partiel des états de slot et des droits permanents au laboratoire; preuves Node rattachées aux exigences. Pas de jeu complet, clips, service d’abonnement ou validation visuelle déduite.
- **HC-E2-66-04** — Vérifier cas de réception et maintenir documenté/produit/intégré/testé distincts.
  Preuve logique partielle : Raccord partiel des états de slot et des droits permanents au laboratoire; preuves Node rattachées aux exigences. Pas de jeu complet, clips, service d’abonnement ou validation visuelle déduite.

Source intégrale : [section 66 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Fichiers témoins de l’existant : [docs/HALO_COMBATS_BIBLE_V1.md](HALO_COMBATS_BIBLE_V1.md), [data/universe_catalog_v9.json](../data/universe_catalog_v9.json), [data/universe_catalog_v10.json](../data/universe_catalog_v10.json), [prototype/extensions_v10/rules.js](../prototype/extensions_v10/rules.js), [prototype/qa_v10/extensions.test.cjs](../prototype/qa_v10/extensions.test.cjs), [work/wave10/guide_runtime_verification.json](../work/wave10/guide_runtime_verification.json).

<a id="section-67"></a>

### Section 67 — Références vérifiées et vocabulaire

**Décision :** retenue · **Priorité :** P0 · **Prototype :** Document / référence · **Assets :** `not_applicable`.

Les références Patreon et le vocabulaire sont conservés dans l’original. Ils seront revérifiés lors d’une éventuelle implémentation ; le présent lot ne fait aucun appel au fournisseur.

- **HC-E2-67-01** — Conserver liens et date de revue des sources factuelles sans présenter recommandations de design comme règles imposées par Patreon.
- **HC-E2-67-02** — Définir slot, silhouette, droit, acquisition, admissibilité, catalogue, OAuth, événement et resynchronisation.
- **HC-E2-67-03** — Ne pas promettre intégration, offre, droits d’utilisation ou échéance non vérifiés.

Source intégrale : [section 67 du guide](guides_combat/Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt).
Aucune preuve d’implémentation dans le point de départ inspecté ; la spécification reste dans cette annexe et son original.

## 7. Écarts constatés entre conception et prototypes

| ID | Sujet | Bible / cible | Prototype / constat | Traitement |
|---|---|---|---|---|
| HC-DRIFT-01 | Buffer de saisie | 6 frames, bible V1 | 8 frames, laboratoire V8 | Écart de prototype conservé ; décider et tester avant unification. |
| HC-DRIFT-02 | Recharge grenade | 600 frames actives depuis consommation | compteur >420 avec stock inférieur à deux | Paramètre et origine du compteur à harmoniser dans le moteur complet. |
| HC-DRIFT-03 | Recharge bouclier | 2 points/frame après 240 frames | 1,15 point/frame après hitAt + 240 | Deux réglages distincts ; aucun résultat équilibrage final annoncé. |
| HC-DRIFT-04 | Manches | Deux manches gagnantes standard | Une manche de 99 secondes | Le labo n’est pas un mode tournoi ou versus complet. |
| HC-DRIFT-05 | Bouclier des identités humaines | Aucun bouclier MJOLNIR fictif pour ODST sans équipement attesté | Gabarit V8 1000 PV/200 bouclier pour toute identité sélectionnée | Qualifier le gabarit de test ; décliner ressources par incarnation avant validation lore. |
| HC-DRIFT-06 | Inventaires de périmètres | 24 combattants, 24 arènes, 20 boss V1 | 232 fiches V9: 128 personnages, 24 costumes, 46 stages, 34 boss | Conserver les versions et unités ; ne pas annoncer 128 personnages jouables. |
| HC-DRIFT-07 | Énergie individuelle et jauge équipe | Énergie de kit: trois segments de 100, bible V1 | Jauge équipe V10 prévue: 100 unités distinctes | Deux ressources nommées et séparées ; aucune conversion implicite entre elles. |
| HC-DRIFT-08 | Fichiers art et fonctionnalité | Sprite conforme puis clips, collisions et tests par kit | PNG candidats statiques, aucun nouveau clip V9 ni parallaxe indépendante | Fidélité visuelle 1:1 et jouabilité finale non certifiées par présence au catalogue. |

Ces écarts sont conservés sans changer le laboratoire V8 dans cette tâche documentaire. Ils doivent être résolus lors de l’intégration des kits et règles finales. Les dénominateurs de V1 et V9 restent tous deux valides pour leurs périmètres ; leur mélange serait trompeur.

## 8. Réception, restants et prochaines preuves

- **Vérifié dans cette tâche :** tailles et SHA-256 des trois copies, présence des 68 sections, IDs d’exigences uniques et existence des chemins témoins.
- **Conception intégrée :** adaptations Halo et décisions par rubrique, règles de continuité, modèles d’équipe, grammaire des verrous et cadre des droits.
- **V10 vérifié en logique :** 30 tests Node réussis. Les exigences concernées portent la portée exacte de la preuve ; elle ne vaut pas réception de toute la section.
- **V10 vérifié dans le navigateur :** 26 contrôles nommés, avec captures et limites dans le rapport de réception. Les parcours non couverts restent ouverts.
- **Non livré par cette tâche :** sprites supplémentaires, clips taunt/sélection/tag/duo, scènes complètes, audio, parallaxe découpée, hub jouable, clash/QTE, réseau, replays et service d’abonnement.
- **Fidélité à valider asset par asset :** incarnation, arme, proportions, anatomie, matière, asymétrie, cadre, transparence et comparaison visuelle conservée.

Les 18 cas de validation de l’Extension 01 et les 22 de l’Extension 02 restent intégraux dans leurs sources. Les tests d’un laboratoire doivent indiquer quels cas ils exercent réellement ; les autres gardent un état non testé ou non applicable justifié. Un slot correct ne termine pas le personnage qu’il représente.

## 9. Sources Halo primaires utilisées pour cette adaptation

- **[H1] [Anniversary Angle: March of the Dream Teams](https://www.halowaypoint.com/news/anniversary-angle-march-of-the-dream-teams)**, consulté le 2026-11-27. Portée : Composition de Blue Team et Red Team; aucun super duo de Halo Combats attesté par cette page.
- **[H2] [Silver Debrief: A New Beginning](https://www.halowaypoint.com/news/silver-debrief-a-new-beginning)**, consulté le 2026-11-27. Portée : La série TV utilise une chronologie indépendante; ne pas fusionner événements Silver et canon principal.
- **[H3] [A Halo 5 Primer: The Story So Far](https://news.xbox.com/en-us/2015/10/26/halo-5-primer-the-story-so-far/?ver=3.7.1)**, consulté le 2026-11-27. Portée : Alliance du Major et de l’Arbiter pendant Halo 3; ne justifie pas une version Infinite dans un épisode Halo 3.
- **[H4] [Feet First into Fall](https://www.halowaypoint.com/news/feet-first-into-fall)**, consulté le 2026-11-27. Portée : Alpha-Nine dans Halo 3: ODST; appui pour relations de même période, pas pour scènes inventées.

Ces références établissent les relations et continuités mentionnées. Elles ne valident ni les paramètres du laboratoire ni ses techniques inventées. Les autres fiches conservent les registres de sources existants et leurs réserves de contrôle.
