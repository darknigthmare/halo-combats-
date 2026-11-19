from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / "HALO_COMBATS_PERSONNAGES_V2.parts.json").read_text())
chunks = []
for entry in manifest["parts"]:
    data = (root / entry["name"]).read_bytes()
    if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
        raise SystemExit("Partie absente, tronquée ou altérée : " + entry["name"])
    chunks.append(data)
archive = b"".join(chunks)
if len(archive) != manifest["bytes"] or hashlib.sha256(archive).hexdigest() != manifest["sha256"]:
    raise SystemExit("L'archive reconstituée ne correspond pas au fichier original.")
target = root / manifest["archive"]
if target.exists() and target.read_bytes() != archive:
    raise SystemExit("Un autre fichier existe déjà à cet emplacement ; aucun écrasement.")
if not target.exists():
    target.write_bytes(archive)
print(f"Archive vérifiée : {target.name}, {len(archive)} octets, SHA-256 {manifest['sha256']}")
