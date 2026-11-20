# Halo Combats — livraison V5 : gardes et Boss Battle

Mode annexe de combat 2D pour Darknigthmare. Mise à jour : 19 novembre 2026 à 23:18 (heure de Paris, UTC+01:00).

## État livré

**24/24 combattants possèdent un visuel de référence ; 23/24 possèdent aussi une garde statique candidate.** Les visuels disponibles couvrent **20/20 rencontres Boss Battle**.

Pour les rencontres Boss Battle, **17/20 disposent d'au moins une silhouette complète candidate** ; **3 rencontres n'ont qu'une présence ou un élément partiel**. Les portées exactes figurent dans l'inventaire et le rapport V5.

La V5 ajoute **43 PNG** : 23 gardes et 20 profils de boss/événements. Les versions précédentes restent disponibles.

Garde encore manquante : **John 117 le Major**, après 3 échecs de génération conservés. Sa pose de référence antérieure reste disponible. La V5 totalise 54 tentatives, dont 11 échecs ; l'historique cumulé conserve 72 échecs. Le Locust V02 à quatre pattes est préféré ; le V01 reste archivé dans les candidats avec son défaut anatomique signalé.

| Catégorie | Fichiers disponibles | Portée |
|---|---:|---|
| Poses de combattants | 50 | Références antérieures et gardes statiques |
| Gardes statiques comprises ci-dessus | 23 | 23/24 combattants |
| Profils et présences Boss Battle | 21 | 20/20 rencontres ; portée complète ou partielle précisée |
| Masters de décors | 2 | Couches parallaxe indépendantes à produire |
| Tous candidats visuels | 73 | Total de fichiers distincts |
| Clips d'animation livrés | 0 | Les poses fixes ne sont pas des clips |

Les visuels restent candidats, non certifiés 1:1. Une garde ne constitue pas une boucle animée ; un profil de boss ne constitue pas une rencontre jouable. Cette livraison ne modifie pas le prototype.

## Ouvrir les livrables

- [Gardes V5](assets/characters_wave5/) et [profils Boss Battle V5](assets/bosses_wave5/).
- [Suivi détaillé V5](docs/HALO_COMBATS_GARDES_BOSS_V5.md), [inventaire des personnages](data/characters_visual_inventory.csv) et [inventaire Boss Battle](data/bosses_visual_inventory.csv).
- [Références Boss Battle](docs/SOURCES_BOSS_V5.md) et [preuves de vérification V5](work/wave5/verification.json).
- [Manifeste courant](data/asset_manifest.json), [compteurs](data/delivery_counts.json), [journal V5](work/wave5/generation_results.json) et [QA V5](work/wave5/qa_wave5.json).
- [Livraison V4](README_V4.md), [V3](README_V3.md) et [V2](README_V2.md) : états historiques conservés.
- [Bible DOCX V1](docs/HALO_COMBATS_BIBLE_V1.docx), [bible Markdown V1](docs/HALO_COMBATS_BIBLE_V1.md) et [classeur V1](docs/HALO_COMBATS_PRODUCTION_V1.xlsx) : spécifications et état daté ; les registres JSON/CSV portent le suivi visuel courant.
- [Prototype indépendant](prototype/halo_combats_prototype.html) : entraînement, duel IA et mécanique partielle Scarab avec visuels temporaires.

Les animations, armes/effets manquants, collisions, comportement des boss et intégration complète restent à produire. Les rencontres événementielles conservent leur rôle narratif spécifié ; une image de Guardian n'implique pas sa destruction.
