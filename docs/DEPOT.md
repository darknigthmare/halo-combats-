# Dépôt Halo Combats

Dépôt existant : https://github.com/darknigthmare/halo-combats-

Le dépôt contenait initialement un README portant le titre `halo-combats-`. Cette importation conserve son historique Git et ajoute les livrables V1/V2. Les scripts de reconstruction V1 sont historiques ; ne pas relancer `scripts/prepare_delivery.py` sur un état V2/V3/V4, car il réinitialise les données à partir du premier lot. Les chemins `source_path` du journal sont des traces de génération ; les images publiées se lisent via les chemins relatifs `path` du manifeste.

Les archives dans `releases/` sont des instantanés datés. Les données à la racine du dépôt constituent le suivi courant. Aucune des poses candidates ne vaut certification de fidélité 1:1 ou personnage jouable complet.

## Mise à jour des personnages V3

La même branche et la PR nº1 conservent la reprise des 15 personnages manquants : 3 nouveaux PNG (Noble Six, Rookie et Alice), 12 refus consignés, soit 12 combattants illustrés sur 24. Les états V1/V2 restent des instantanés historiques ; cet état V3 est conservé dans son suivi daté.

Le contrôle de logique autonome se lance avec `node prototype/qa/logic.cjs`. Le contrôle navigateur `prototype/qa/verify.cjs` utilise des chemins relatifs au dépôt et demande une installation de Playwright ; `HALO_CHROMIUM_EXECUTABLE` permet de préciser un binaire Chromium. Sa syntaxe a été vérifiée, sans revendiquer une validation navigateur réussie.

## Checkpoint des personnages V4 — 21 essais

Le checkpoint V4 ajoute 9 PNG pour 8 personnages : le Major, Kat, Jorge, Jun, Carter, Johnson, Tartarus et Douglas. Les deux poses de Kat restent présentes ; la version v02 est préférée et les défauts de la v01 sont consignés. La couverture atteint 20 combattants illustrés sur 24, avec 21 poses de combattants, un boss et deux décors, soit 24 PNG candidats. Emile, Escharum, Jega et Chak ’Lok restent sans candidat dans ce checkpoint.

Le journal V4 comprend 21 essais : 9 réussites et 12 refus. Le README et les registres courants correspondent à ce checkpoint figé ; les historiques V1/V2/V3 sont conservés. Les références téléchargées ne sont pas des images générées et restent exclues du dépôt. Les observations de QA précisent notamment les limites des références de Johnson et Douglas, ainsi que les réserves de cadrage et de franges de Jun et Jorge.

Les empreintes des 15 PNG précédents sont inchangées. Les neuf nouveaux fichiers ont été copiés à l’identique depuis le snapshot contrôlé. Cette publication conserve les corrections de portabilité et ne modifie pas le prototype ; elle n’ajoute aucun résultat de test du gameplay. Les poses demeurent non certifiées, non animées et non intégrées.
