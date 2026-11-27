# Halo Combats — projectiles et VFX V10

Les [données V10](../data/projectiles_v10.json) ajoutent **19 projectiles et 5 effets** au catalogue. Quatre PNG statiques sont présents : M9, grenade à plasma, grenade à pointes et aiguille du Needler. Les vingt autres dossiers n’ont pas encore de visuel.

## Référence retenue et limite des sources

L’[inventaire officiel Halo Infinite](https://support.halowaypoint.com/hc/en-us/articles/6882880281364-Halo-Infinite-Weapon-Equipment-and-Vehicle-Inventory) fournit des identités et comportements généraux. Certaines formulations sont historiques. Les [notes Banished Honor](https://support.halowaypoint.com/hc/en-us/articles/25897330878868-Halo-Infinite-Banished-Honor-Update-Patch-Notes) et la [présentation CU32](https://www.halowaypoint.com/news/banished-honor-sandbox) corrigent notamment le pistolet plasma, la grenade à pointes et le Calcineur.

Le profil de comportement est explicitement **CU32, 30 avril 2024, multijoueur**. Il ne prétend pas reproduire tout l’équilibrage du jeu actuel ni imposer ces modifications à une campagne dont les règles diffèrent. Le modèle visuel reste celui d’Infinite, sans mélange avec les autres jeux.

La surcharge du pistolet plasma possède l’EMP rétabli par CU32. La fusée de la grenade à pointes démarre une fois l’objet immobilisé ; sa référence de 1,2 seconde donne 72 pas à 60 Hz. Le Calcineur ne reçoit pas l’ancien effet d’aspiration. Ces corrections sont conservées dans les données et contrôlées par un test ciblé.

## Familles de production

| Famille | Dossiers |
|---|---|
| Grenades | M9 ; plasma ; pointes ; dynamo ; éclat de grenade à pointes |
| Needler | Aiguille ; effet de supercombine |
| Plasma | Pistolet normal ; surcharge ; carabine à impulsion ; Ravageur normal ; charge ; nappe persistante ; fusil traqueur |
| Lumière solide | Orbe du Calcineur ; particule de Vague de chaleur ; faisceau de sentinelle |
| Projectiles physiques | Micromissile Hydra ; roquette SPNKr ; pointe de l’Empaleur ; pointe du Déchiqueteur |
| Électricité / gravité | Décharge du Disrupteur ; effet du fusil électrique ; onde du marteau |

Le nom d’un dossier désigne son incarnation et sa fonction. Il ne certifie pas la production de l’arme, du porteur ou de toutes les étapes d’un effet.

## Contrat commun d’entité

Les choix ci-dessous sont une adaptation originale pour Halo Combats. Ils doivent être implémentés puis testés ; aucun système de collision de projectile n’est annoncé comme livré par ce document.

- **Identité et attribution :** identifiant d’émission unique ; combattant source et équipe immuables ; dégâts et récompenses attribués à cette source après un tag.
- **Mouvement :** trajectoire déclarée par fiche, vitesse et dimensions à équilibrer séparément du PNG ; balayage entre deux positions pour les projectiles rapides.
- **Collision :** forme dédiée, obstacle admissible, budget de contacts et règle de consommation. Les transparences de l’image ne constituent pas une hitbox.
- **Persistance :** un projectile émis peut subsister après la sortie ou le KO du porteur. Le faisceau maintenu cesse avec lui. Aucune résurrection ni réattribution implicite.
- **Pause et scènes :** âge, déplacement, fusée et dégâts gelés ; reprendre ou passer une scène conserve le même état logique.
- **Fin de round :** nettoyage des projectiles, attaches, nappes, compteurs et événements différés.
- **Réseau futur :** événements et hasard déterministes prévus ; aucun rollback opérationnel livré.

Pour le Needler, l’attache et l’accumulation ne sont pas admises sur véhicules ou structures. Pour le Ravageur standard, la charge est balistique : le rebond particulier d’une variante n’est pas importé sans preuve. Une nappe suit le sol réel et reste distincte de son projectile d’origine.

## Fichiers et étapes d’art

Chaque fiche conserve source, silhouette attendue, état d’art, règles proposées et étapes à produire. Le vol statique déjà dessiné ne valide pas les impacts, la dissipation ou une animation.

| PNG V10 | État | Réserves |
|---|---|---|
| M9 Infinite | Candidat | Détails des panneaux et marges à valider. |
| Grenade à pointes Infinite | Candidat | Géométrie fine des pointes, matériaux et asymétries à comparer. |
| Grenade plasma Infinite | Candidat | Segmentation et détails lumineux à confirmer. |
| Aiguille Needler Infinite | Candidat | Facettes et traînée à confronter à davantage de captures. |

Les fichiers conservent leur alpha natif et leur orientation. Les [revues d’assets](../work/wave10/asset_reviews.json) consignent les empreintes, dimensions, transparences et réserves de chaque image.
