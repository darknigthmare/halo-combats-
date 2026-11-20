#!/usr/bin/env python3
"""Refresh the publication index from the selected catalogue and Git-visible files."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {"PUBLICATION_INVENTORY.json", "SHA256SUMS.txt"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", type=int, required=True)
    args = parser.parse_args()
    catalogue_path = f"data/universe_catalog_v{args.version}.json"
    catalogue = json.loads((ROOT / catalogue_path).read_text(encoding="utf-8"))
    previous = json.loads((ROOT / "PUBLICATION_INVENTORY.json").read_text(encoding="utf-8"))
    paths = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT
    ).decode("utf-8").split("\0")
    files = []
    for relative in sorted(set(paths) - EXCLUDED - {""}):
        target = ROOT / relative
        if not target.is_file():
            continue
        payload = target.read_bytes()
        files.append({"path": relative, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
    browser_path = ROOT / f"prototype/qa_v{args.version}/browser_results.json"
    browser = json.loads(browser_path.read_text(encoding="utf-8")) if browser_path.exists() else {
        "status": "not_run", "reason": "No current-version browser result has been recorded."
    }
    inventory = {
        "version": args.version,
        "scope": f"Halo Combats V{args.version}: catalogue de production, PNG statiques et références; fidélité 1:1 non certifiée.",
        "catalogue": catalogue_path,
        "coverage": catalogue["counts"],
        "legacy_v8_coverage": previous.get("legacy_v8_coverage", previous.get("coverage", {})),
        "historical_source_checkpoint_inventory_sha256": previous.get("historical_source_checkpoint_inventory_sha256", previous.get("source_checkpoint_inventory_sha256")),
        "browser_validation": browser,
        "checksum_policy": "SHA-256 of Git-visible deliverable files, excluding this inventory and SHA256SUMS.txt to avoid recursion.",
        "files": files,
    }
    (ROOT / "PUBLICATION_INVENTORY.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "SHA256SUMS.txt").write_text("".join(f"{item['sha256']}  {item['path']}\n" for item in files), encoding="utf-8")
    print(json.dumps({"version": args.version, "indexed_files": len(files), "png_assets": catalogue["counts"]["unique_png_assets"]}))


if __name__ == "__main__":
    main()
