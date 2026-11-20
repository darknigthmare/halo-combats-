# Reconstituer le ZIP V2

Le ZIP de personnages V2 est conservé ici en deux parties binaires : le fichier original dépassait la limite de taille du transfert GitHub disponible. Tous ses fichiers individuels sont également présents dans ce dépôt.

Télécharger les deux fichiers `.part01` / `.part02`, le manifeste `.parts.json` et `reassemble_archive.py` dans le même dossier, puis exécuter :

```bash
python3 reassemble_archive.py
```

Le script vérifie la taille et le SHA-256 de chaque partie puis reconstitue `HALO_COMBATS_PERSONNAGES_V2.zip` octet pour octet. Empreinte originale : `02a18b8f05fc962740a48a34c2af53305bff2efeb90d8d032b6c22c14d0e4ab0`. La reconstitution refuse d’écraser un fichier existant différent.
