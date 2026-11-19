# Dépôt Halo Combats

Dépôt existant : https://github.com/darknigthmare/halo-combats-

Le dépôt contenait initialement un README portant le titre `halo-combats-`. Cette importation conserve son historique Git et ajoute les livrables V1/V2. Les scripts de reconstruction V1 sont historiques ; ne pas relancer `scripts/prepare_delivery.py` sur un état V2/V3, car il réinitialise les données à partir du premier lot. Les chemins `source_path` du journal sont des traces de génération ; les images publiées se lisent via les chemins relatifs `path` du manifeste.

Les archives dans `releases/` sont des instantanés datés. Les données à la racine du dépôt constituent le suivi courant. Aucune des poses candidates ne vaut certification de fidélité 1:1 ou personnage jouable complet.

## Mise à jour des personnages V3

La même branche et la PR nº1 conservent la reprise des 15 personnages manquants : 3 nouveaux PNG (Noble Six, Rookie et Alice), 12 refus consignés, soit 12 combattants illustrés sur 24. Les états V1/V2 restent des instantanés historiques ; le README et les données à la racine portent l’état V3 courant.

Le contrôle de logique autonome se lance avec `node prototype/qa/logic.cjs`. Le contrôle navigateur `prototype/qa/verify.cjs` utilise des chemins relatifs au dépôt et demande une installation de Playwright ; `HALO_CHROMIUM_EXECUTABLE` permet de préciser un binaire Chromium. Sa syntaxe a été vérifiée, sans revendiquer une validation navigateur réussie.
