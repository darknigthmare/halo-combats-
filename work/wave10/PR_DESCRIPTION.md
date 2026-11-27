## Pourquoi

Les trois guides de construction du jeu de combat et leurs deux extensions étaient absents du dépôt V9. Le suivi mêlait aussi contenu documenté, PNG disponibles et fonctionnalités réellement exécutables. Cette V10 intègre les originaux, relie chaque exigence à Halo et poursuit la production sans déclarer terminés les éléments encore en conception.

## Changements

- Bible V10 active, trois originaux conservés octet pour octet, provenance SHA-256, adaptation des 68 sections et matrice de 311 exigences.
- Laboratoire local des extensions : duo actif/réserve, assist/tag/taunt/super/finisher, coûts et interruptions, bonus de précision, déblocages ET/OU, droits permanents/temporaires simulés, distinction entre aperçu/droit/fichier/compatibilité et sauvegarde versionnée.
- Sept PNG supplémentaires : Pavium HW2, Sword Base Reach, Cartographe CE, M9, grenade à pointes, grenade plasma et aiguille Needler Infinite. Les 104 PNG historiques restent inchangés.
- Catalogue de 256 fiches / 111 PNG avec catégories projectiles et VFX, images entières, sources, réserves et statuts. Ajout de 24 dossiers de production, sans prétendre livrer leurs collisions.
- Classeur à trois onglets, compteurs recalculables, exigences et preuves partielles.
- Correction du Chevalier standard vers Halo 4 ; profil Infinite CU32 daté, correction EMP, fusée Spike, cibles Needler et distinction Ravageur/Rebound.

## État de production

| Mesure | V9 | V10 |
|---|---:|---:|
| Fiches | 232 | 256 |
| PNG distincts | 104 | 111 |
| Fiches illustrées | 77 | 84 |
| Anciens dossiers sans visuel | 155 | 152 |
| Nouveaux dossiers sans visuel | — | 20 |
| Total sans visuel | 155 | 172 |

Le périmètre s’agrandit : les 24 nouveaux dossiers incluent 4 PNG. Six nouvelles images restent candidates et le Cartographe est à corriger. Aucune certification 1:1, animation ni couche de parallaxe indépendante n’est annoncée.

## Vérification

- **46/46 tests Node** : 30 extensions, 8 catalogue V10 et 8 régression V9.
- **38/38 contrôles Chromium** : 12 catalogue et 26 laboratoire, formats bureau/mobile, 0 erreur JavaScript ; accès direct aux fichiers vérifié pour le laboratoire.
- Parcours de coordination et précision 12/12, acquisition/sélection, sauvegarde/rechargement, reset isolé, données corrompues conservées et PNG réellement absent correctement bloqué.
- **29/29 points d’audit indépendant**, dont empreintes des 104 PNG, identités héritées, sources et compteurs.
- XLSX rendu et contrôlé ; formules recalculées, modification temporaire d’entrée restaurée, aucune erreur de formule.
- Reçus et captures sous `prototype/qa_v10/`, audit et revues sous `work/wave10/`. Inventaire et SHA256 de publication mis à jour.

## Portée

Les 68 sections sont intégrées documentairement.71exigences possèdent une preuve V10 partielle ; aucune réception globale des extensions n’est prétendue. Les images restent fixes et les valeurs du laboratoire sont des adaptations originales. Le prototype n’implémente pas un moteur complet de collisions, les kits individuels, les clips, le réseau ni un abonnement réel.

Treize appels de génération ont produit sept PNG ; cinq refus de sortie et une erreur technique sont consignés. Aucun fichier fictif ni contournement de refus.

## Points d’entrée

- `docs/HALO_COMBATS_BIBLE_V10.md`
- `prototype/halo_universe_v10.html`
- `prototype/halo_extensions_v10.html`
- `docs/HALO_COMBATS_PRODUCTION_V10.xlsx`
