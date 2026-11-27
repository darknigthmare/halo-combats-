# Halo Combats — V10 : bible, extensions et nouveaux visuels

La V10 reprend la V9 fusionnée et intègre les **trois guides complets** : guide général, Extension 01 (équipes, taunts, tag et bonus) et Extension 02 (emplacements verrouillés, déblocages et droits). La bible relie **68 sections et 311 exigences** à leur adaptation Halo et à leurs preuves de réalisation.

Le catalogue contient **256 fiches**, **111 PNG distincts** et **112 œuvres ou composants**. Sept PNG sont ajoutés, et les 104 historiques sont conservés octet pour octet. Le laboratoire local des extensions expose des règles exécutables avec des poses fixes.

## Ouvrir le projet

| Entrée | Contenu |
|---|---|
| [Bible active V10](docs/HALO_COMBATS_BIBLE_V10.md) | Fondations, trois guides, décisions, fidélité, extensions et état réel de production. |
| [Catalogue visuel V10](prototype/halo_universe_v10.html) | Recherche, catégories, œuvres, continuités, manquants et images entières. |
| [Laboratoire des extensions](prototype/halo_extensions_v10.html) | Composition, aperçu verrouillé, progression, assist/tag/taunt/super/finisher et bonus. |
| [Classeur de production](docs/HALO_COMBATS_PRODUCTION_V10.xlsx) | Synthèse recalculable, catalogue et exigences. |

Les deux pages HTML fonctionnent depuis le dépôt complet, directement ou via un serveur HTTP local :

```sh
python -m http.server 8080
```

Ouvrir ensuite `http://localhost:8080/prototype/halo_universe_v10.html`. Conserver les dossiers `assets`, `data` et `prototype` ensemble.

## Les trois guides sont intégrés

Les copies originales se trouvent dans [docs/guides_combat](docs/guides_combat/), avec leurs SHA-256 et leur provenance. Elles étaient absentes des documents et données du point de départ V9.

L’[annexe d’intégration](docs/HALO_COMBATS_GUIDE_INTEGRATION_V10.md) reprend toutes les sections et suit 311 exigences. L’intégration documentaire est complète ; l’implémentation des mécaniques reste partielle et son état est indiqué séparément. Les exemples généralistes sont adaptés aux incarnations Halo, aux relations attestées et aux limites de leurs équipements.

Le laboratoire met en œuvre un sous-ensemble représentatif : duo actif/réserve, coûts, récupération, interruptions, tag après KO, résultat de super, finisher conditionnel, bonus et droits locaux. Il ne livre ni réseau, ni paiement, ni service d’abonnement. Les clips de sélection, combat et cinéma restent à produire.

## Images de ce lot

| Nouvelle image | Incarnation | État |
|---|---|---|
| Pavium | Halo Wars 2: Awakening the Nightmare | Candidat |
| Cour de Sword Base | Halo: Reach | Candidat |
| Cartographe silencieux | Halo CE classique | À corriger |
| M9, grenade plasma, grenade à pointes, aiguille Needler | Halo Infinite | Quatre candidats statiques |

Chaque PNG garde ses références, ses réserves, sa transparence et son orientation. Le Cartographe présente une géométrie trop arrondie ; sa fiche l’indique. Les deux décors sont des masters aplatis.

**Aucune image n’est certifiée 1:1, aucun nouveau clip animé ni calque de parallaxe indépendant n’est annoncé.** Les mécaniques de test ne valident pas un moveset complet.

## Production réconciliée

| Mesure | V10 |
|---|---:|
| Personnages / costumes / stages / boss | 128 / 24 / 46 / 34 |
| Projectiles / VFX | 19 / 5 |
| Fiches illustrées / sans visuel | 84 / 172 |
| Anciens manquants V9 encore sans image | 152 sur 155 |
| Nouveaux dossiers projectile/VFX sans image | 20 sur 24 |
| PNG historiques préservés / nouveaux | 104 / 7 |

Les nouveaux dossiers rendent visible du travail supplémentaire ; ils expliquent la hausse du total des manquants. Ils spécifient le comportement futur des entités sans prétendre livrer leurs collisions.

Corrections : Chevalier standard rattaché à Halo 4 ; profil Infinite CU32 explicite ; continuités séparées. Les paramètres 2D et les chorégraphies sont présentés comme des adaptations du projet.

## Vérification et sources de production

```sh
node --test prototype/qa_v9/catalog.test.cjs prototype/qa_v10/catalog.test.cjs prototype/qa_v10/extensions.test.cjs
```

Cette commande vérifie **46 tests** : 30 pour les extensions, 8 pour les nouvelles données et 8 de régression du catalogue V9. Les **38 contrôles navigateur** (12 catalogue +26 laboratoire) ont réussi sur ordinateur et mobile, sans erreur JavaScript. Les reçus et captures sont conservés dans [qa_v10](prototype/qa_v10/). Un [audit indépendant](work/wave10/v10_independent_audit.json) vérifie 29 points de conservation, provenance, comptage et cohérence.

- [Catalogue documenté](docs/HALO_COMBATS_CATALOGUE_V10.md), [données](data/universe_catalog_v10.json) et [manifeste des PNG](data/asset_manifest_v10.json).
- [Projectiles et VFX](docs/HALO_COMBATS_PROJECTILES_V10.md), [spécifications](data/projectiles_v10.json) et [tâches de production](data/production_tasks_v10.json).
- [Matrice des guides](data/combat_guide_coverage_v10.json), [revues des images](work/wave10/asset_reviews.json) et [journal de génération](work/wave10/root_generation_followup.json).
- [Guide du laboratoire](prototype/extensions_v10/README.md).

Historique conservé : [V9](README_V9.md), [V8](README_V8.md), [bible V1](docs/HALO_COMBATS_BIBLE_V1.md), [laboratoire V8](prototype/halo_combats_lab_v8.html).

Projet de fan non officiel. La fidélité visuelle et la couverture de l’univers restent des objectifs de production vérifiables, pas des certifications déduites du nombre de fichiers.
