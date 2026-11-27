# Validation V10

Le lot passe 46 tests Node et 38 contrôles navigateur. Les reçus précisent les cas couverts ; aucune certification de jeu complet ou d’art 1:1 n’en découle.

- `results.json` et `node-results.tap` : 46 tests passés, 0 échec.
- `browser_results.json` : agrégation des 12 contrôles du catalogue et 26 du laboratoire.
- `catalog_browser_results.json` et `extensions_browser_results.json` : résultats détaillés.
- `catalog_*.png` et `extensions_*.png` : captures relues.
- `../../work/wave10/v10_independent_audit.json` : 29 contrôles des données et assets.

## Exécution

```sh
node --test prototype/qa_v9/catalog.test.cjs prototype/qa_v10/catalog.test.cjs prototype/qa_v10/extensions.test.cjs
node prototype/qa_v10/catalog.browser.cjs
node prototype/qa_v10/extensions.browser.cjs
```

Les scripts navigateur demandent Playwright et un Chromium disponible. Ils créent leur propre serveur HTTP local dans le même processus. Le script catalogue accepte `HALO_QA_CHROMIUM` ; consulter le script extensions pour sa recherche d’exécutable. Aucun identifiant de compte n’est utilisé.

La capture escouade desktop a été reprise après décodage complet des images et deux frames de peinture, car la première capture pouvait montrer des emplacements encore vides malgré les fichiers déjà chargés. Cette reprise ne modifie aucune source ni le reçu des 26 contrôles du laboratoire.

Seul Chromium est testé. Aucun test de manette réelle, de réseau, de collisions finales ou d’abonnement externe n’est revendiqué.
