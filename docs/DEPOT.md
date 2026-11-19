# Dépôt Halo Combats

Dépôt existant : https://github.com/darknigthmare/halo-combats-

Le dépôt contenait initialement un README portant le titre `halo-combats-`. Cette importation conserve son historique Git et ajoute les livrables V1/V2. Les scripts de reconstruction V1 sont historiques ; ne pas relancer `scripts/prepare_delivery.py` sur un état V2/V3/V4, car il réinitialise les données à partir du premier lot. Les chemins `source_path` du journal sont des traces de génération ; les images publiées se lisent via les chemins relatifs `path` du manifeste.

Les archives dans `releases/` sont des instantanés datés. Les données à la racine du dépôt constituent le suivi courant. Aucune des poses candidates ne vaut certification de fidélité 1:1 ou personnage jouable complet.

## Mise à jour des personnages V3

La même branche et la PR nº1 conservent la reprise des 15 personnages manquants : 3 nouveaux PNG (Noble Six, Rookie et Alice), 12 refus consignés, soit 12 combattants illustrés sur 24. Les états V1/V2 restent des instantanés historiques ; cet état V3 est conservé dans son suivi daté.

Le contrôle de logique autonome se lance avec `node prototype/qa/logic.cjs`. Le contrôle navigateur `prototype/qa/verify.cjs` utilise des chemins relatifs au dépôt et demande une installation de Playwright ; `HALO_CHROMIUM_EXECUTABLE` permet de préciser un binaire Chromium. Sa syntaxe a été vérifiée, sans revendiquer une validation navigateur réussie.

## Checkpoint des personnages V4 — 21 essais

Le checkpoint V4 ajoute 9 PNG pour 8 personnages : le Major, Kat, Jorge, Jun, Carter, Johnson, Tartarus et Douglas. Les deux poses de Kat restent présentes ; la version v02 est préférée et les défauts de la v01 sont consignés. La couverture atteint 20 combattants illustrés sur 24, avec 21 poses de combattants, un boss et deux décors, soit 24 PNG candidats. Emile, Escharum, Jega et Chak ’Lok restent sans candidat dans ce checkpoint.

Le journal V4 comprend 21 essais : 9 réussites et 12 refus. Cet état est conservé dans le commit `bbbbbf5fd3aa5c9c59020a2564675a747fea2c9b` ; les historiques V1/V2/V3 sont conservés. Les références téléchargées ne sont pas des images générées et restent exclues du dépôt. Les observations de QA précisent notamment les limites des références de Johnson et Douglas, ainsi que les réserves de cadrage et de franges de Jun et Jorge.

Les empreintes des 15 PNG précédents sont inchangées. Les neuf nouveaux fichiers ont été copiés à l’identique depuis le snapshot contrôlé. Cette publication conserve les corrections de portabilité et ne modifie pas le prototype ; elle n’ajoute aucun résultat de test du gameplay. Les poses demeurent non certifiées, non animées et non intégrées.

## Livraison des personnages V4 — 29 essais

Le snapshot final ajoute six PNG au checkpoint précédent : les premières poses d’Emile, Chak ’Lok, Escharum et Jega, puis les retouches de Carter et d’Escharum. La vague V4 comprend 15 PNG pour 12 nouveaux personnages. Les versions v02 de Kat, Carter et Escharum sont préférées ; les originaux v01 restent conservés avec leurs défauts documentés.

Les 24 combattants possèdent désormais au moins une image candidate, soit 27 poses de combattants. Avec le boss et les deux décors, le dépôt contient 30 PNG candidats. Le journal V4 comporte 29 essais : 15 réussites et 14 refus ; les 61 échecs historiques sont conservés. Aucun personnage du roster principal ne reste sans candidat.

Le README et les données courantes correspondent à cette livraison V4. Les 24 PNG du checkpoint précédent sont inchangés et les six nouveaux fichiers sont byte-identiques au snapshot final contrôlé. Les images de référence téléchargées restent exclues des candidats et du dépôt. La couverture du roster ne vaut pas certification de fidélité : les poses restent non certifiées, non animées et non intégrées au moteur.
