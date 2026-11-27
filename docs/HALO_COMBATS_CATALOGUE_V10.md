# Halo Combats — catalogue et images V10

Le [catalogue consultable](../prototype/halo_universe_v10.html) rassemble **256 fiches**, **112 œuvres ou composants** et **111 PNG distincts**. Les données sont dans [universe_catalog_v10.json](../data/universe_catalog_v10.json) ; le [manifeste V10](../data/asset_manifest_v10.json) conserve les empreintes des fichiers.

## Nouveaux fichiers

| Contenu | Incarnation | État |
|---|---|---|
| Pavium | Halo Wars 2: Awakening the Nightmare, modèle cinématique | Candidat ; pose très frontale, détails et marges à vérifier. |
| Cour de Sword Base | Halo: Reach classique | Candidat ; volumes recomposés pour une scène latérale. |
| Plage du Cartographe silencieux | Halo CE classique | À corriger ; auvent trop arrondi, volumes et lumière différents. |
| Grenade M9 | Halo Infinite | Candidat statique. |
| Grenade à pointes | Halo Infinite | Candidat statique. |
| Grenade à plasma | Halo Infinite | Candidat statique. |
| Aiguille du Needler | Halo Infinite | Candidat statique. |

Les deux décors sont des masters aplatis. **Aucun calque de parallaxe indépendant et aucun clip animé n’est ajouté.** Le fichier de Sword Base a été restauré depuis les octets exacts du résultat du générateur après une écriture locale vide ; les pixels n’ont pas été retouchés.

## Comptes réconciliés

| Catégorie | Fiches V10 |
|---|---:|
| Personnages | 128 |
| Costumes | 24 |
| Stages | 46 |
| Boss | 34 |
| Projectiles | 19 |
| VFX | 5 |
| **Total** | **256** |

**84 fiches illustrées, 172 fiches sans visuel.** Parmi les 232 anciennes fiches, les manquants passent de 155 à 152. Les vingt nouveaux manquants appartiennent aux 24 nouveaux dossiers projectile/VFX. Les 104 PNG historiques sont inchangés et les sept créations V10 sont copiées sans retouche.

Le Chevalier prométhéen standard est corrigé de l’œuvre Halo 5 vers **Halo 4**, conformément au texte de son incarnation déjà présent. Le [rapport de cohérence](../work/wave10/version_consistency_audit.json) explique l’erreur de classement de la phrase «pas le modèle Halo 5». Les anciennes versions des catalogues restent conservées.

## Tentatives de génération

Treize appels réels ont donné sept PNG, cinq refus de sortie du service et une erreur technique. Les refus concernent Kelly H5, Romeo ODST, Agryna Infinite, Grunt Heavy Reach et 343 Guilty Spark H3. Kelly a d’abord rencontré une erreur de lecture technique puis un refus à son unique nouvel essai. Aucune image n’est annoncée pour ces résultats.

Les journaux conservent les demandes, références, chemins, résultats et identifiants d’erreur : [première série](../work/wave10/root_generation.json), [suite](../work/wave10/root_generation_followup.json), [Pavium et autres cibles](../work/wave10/alien_generation.json). Les sources exactes et les revues de pixels figurent dans [asset_reviews.json](../work/wave10/asset_reviews.json).

## Consultation

Le catalogue fonctionne avec son JSON embarqué hors ligne ou depuis un serveur HTTP local. Recherche et filtres se combinent par catégorie, œuvre, média, continuité, état d’art et manquants. La fiche montre l’incarnation, l’image entière, les réserves, les sources et l’état d’implémentation. Les projectiles et VFX ont leurs propres catégories.

L’[entrée des extensions V10](../prototype/halo_extensions_v10.html) et la [bible active](HALO_COMBATS_BIBLE_V10.md) sont reliées depuis le catalogue. La présence d’un PNG dans les archives ne rend pas cette identité jouable dans le laboratoire.

## Vérification

Les tests V10 contrôlent conservation des 104 PNG, liens des sept créations, identités, compteurs, sources et originalité des trois guides, parité JSON/embarqué et restrictions de profils. Ils complètent les tests de règles d’équipe/déblocage et la régression du catalogue V9.

Commande : `node --test prototype/qa_v9/catalog.test.cjs prototype/qa_v10/catalog.test.cjs prototype/qa_v10/extensions.test.cjs`.

Les reçus précis et les captures de validation réelle sont dans [prototype/qa_v10](../prototype/qa_v10/). Ils ne constituent pas une certification de fidélité visuelle 1:1.
