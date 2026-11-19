#!/usr/bin/env python3
"""Verify consolidated V5 and optionally freeze an explicit publication snapshot.

No pixels are changed. The default is read-only. --write saves evidence, and
--snapshot-to copies only the explicit V5 import set after every gate passes.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
WORK = PROJECT / "work/wave5"
_spec = importlib.util.spec_from_file_location("halo_v5_consolidator", WORK / "consolidate_wave5.py")
v5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v5)

CENTRAL_OUTPUTS = [
    "README.md", "README_V5.md", "data/asset_manifest.json", "data/fighters.json",
    "data/bosses.json", "data/delivery_counts.json", "data/characters_visual_inventory.csv",
    "data/bosses_visual_inventory.csv", "docs/HALO_COMBATS_GARDES_BOSS_V5.md",
    "docs/SOURCES_BOSS_V5.md",
]


def read_json(rel):
    return json.loads((PROJECT / rel).read_text(encoding="utf-8"))


def strip_visual_fields(value, key, fields):
    value = json.loads(json.dumps(value))
    value[key] = [{k: v for k, v in row.items() if k not in fields} for row in value[key]]
    return value


def import_files(manifest):
    result = set(CENTRAL_OUTPUTS)
    result.update(a["path"] for a in manifest["active_candidates"] if a.get("generation_wave") == 5)
    for path in WORK.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.name.endswith((".pyc", ".tmp")):
            continue
        result.add(path.relative_to(PROJECT).as_posix())
    return sorted(result)


def file_hashes(paths):
    return {p: v5.digest(PROJECT / p) for p in paths}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--snapshot-to", type=Path)
    args = parser.parse_args()
    manifest = read_json("data/asset_manifest.json")
    fighters = read_json("data/fighters.json")
    bosses = read_json("data/bosses.json")
    counts = read_json("data/delivery_counts.json")
    baseline = read_json("work/wave5/baseline_v4.json")
    repo_baseline = read_json("work/wave5/baseline_repository_files.json")
    summary = read_json("work/wave5/consolidation_summary.json")
    records = v5.v4.records_from(read_json("work/wave5/generation_results.json"))
    reviews = v5.v4.load_visual_qa(WORK / "qa_wave5.json")
    v5.verify_baseline(manifest, baseline, counts)
    protected = baseline["registry_structure"]
    assert v5.canonical_sha(strip_visual_fields(fighters, "fighters", set(protected["fighter_excluded_fields"]))) == protected["fighters_protected_sha256"], "Fighter design or neutral preference changed"
    assert v5.canonical_sha(strip_visual_fields(bosses, "entities", set(protected["boss_excluded_fields"]))) == protected["bosses_protected_sha256"], "Boss design changed"
    assert {f["id"]: f.get("preferred_visual_asset") for f in fighters["fighters"]} == protected["neutral_preferences"], "Neutral preferences changed"
    active = manifest["active_candidates"]
    wave = [a for a in active if a.get("generation_wave") == 5]
    assert len({a["id"] for a in active}) == len(active), "Duplicate candidate ID"
    assert len({a["sha256"] for a in active}) == len(active), "Duplicate image bytes counted twice"
    copies = []
    for asset in active:
        assert v5.digest(PROJECT / asset["path"]) == asset["sha256"], f"Asset changed: {asset['id']}"
        if asset.get("generation_wave") != 5:
            continue
        source = Path(asset["source_path"])
        assert v5.digest(source) == asset["sha256"], f"Source copy differs: {asset['id']}"
        review = next((r for r in reviews if r.get("entity_id") == asset["entity_id"] and r.get("sha256") == asset["sha256"]), None)
        assert review and review.get("reviewed_utc"), f"Visual QA absent: {asset['id']}"
        assert review["image_metrics"] == {k: asset[k] for k in ("width", "height", "mode", "alpha_range", "technical_qa")}, f"Metrics differ: {asset['id']}"
        assert asset["fidelity_status"] == "not_certified" and asset["animation_status"] == "not_animated" and asset["integration_status"] == "not_integrated"
        assert asset["mode"] == "RGBA" and asset["alpha_range"][0] == 0 and asset["technical_qa"]["transparent_pixels"] > 0
        assert not any(asset["technical_qa"]["edge_contact_pixels_above_threshold"].values()), f"Foreground touches frame: {asset['id']}"
        record = records[asset["journal_record"]]
        for key in ("equipment_state", "facing", "retry_index", "variant", "journal_origin", "representation_scope", "complete_silhouette", "depicted_region"):
            if key in record:
                assert asset.get(key) == record[key], f"Lost journal metadata {key}: {asset['id']}"
        copies.append({"asset_id": asset["id"], "entity_id": asset["entity_id"], "path": asset["path"], "source_path": str(source), "sha256": asset["sha256"], "copy_exact": True, "visual_qa_sha_bound": True})
    guards = [a for a in wave if a["pose_scope"] == "guard_static"]
    profiles = [a for a in wave if a["pose_scope"] == "boss_profile"]
    assert counts["active_visual_candidates"] == len(active)
    assert counts["wave5_generated_pngs"] == len(wave)
    assert counts["wave5_generated_guard_pngs"] == len(guards)
    assert counts["wave5_generated_boss_pngs"] == len(profiles)
    complete = {a["entity_id"] for a in active if a["type"] == "boss_profile" and a.get("complete_silhouette", True)}
    partial = {a["entity_id"] for a in active if a["type"] == "boss_profile" and not a.get("complete_silhouette", True)}
    assert counts["boss_entities_with_complete_profile_candidate"] == len(complete)
    assert counts["boss_entities_without_complete_profile_candidate"] == len(bosses["entities"]) - len(complete)
    assert counts["boss_entities_with_partial_visual_only"] == len(partial - complete)
    assert counts["wave5_generated_complete_boss_pngs"] == sum(a.get("complete_silhouette", True) for a in profiles)
    assert counts["wave5_generated_partial_boss_pngs"] == sum(not a.get("complete_silhouette", True) for a in profiles)
    assert set(summary["boss_entities_with_partial_visual_only"]) == partial - complete
    assert counts["wave5_generation_attempts"] == len(records)
    assert counts["wave5_generation_failures"] == sum(v5.is_failure(r) for r in records)
    assert counts["historical_generation_failures_all_waves"] == len(manifest["failed_requests"])
    assert counts["animation_clips"] == 0 and counts["certified_visuals"] == 0
    assert summary["record_sha256"] == [v5.canonical_sha(r) for r in records], "Journal changed after consolidation"
    candidate_ids = {a["id"] for a in active}
    for f in fighters["fighters"]:
        assert all(i in candidate_ids for i in f["visual_assets"])
        if f.get("preferred_guard_asset"):
            assert f["preferred_guard_asset"] in f["guard_visual_assets"]
    for rel, expected in [("data/characters_visual_inventory.csv", 24), ("data/bosses_visual_inventory.csv", 20)]:
        with (PROJECT / rel).open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        assert len(rows) == expected and len({r["entity_id"] for r in rows}) == expected
        if rel.endswith("characters_visual_inventory.csv"):
            by_id = {a["id"]: a for a in active}
            for row in rows:
                preferred_guard = row["preferred_guard_asset_id"]
                if preferred_guard:
                    guard = by_id[preferred_guard]
                    assert row["guard_equipment_state"] == guard.get("equipment_state", "")
                    assert guard["visual_review_status"] != "reviewed_candidate_requires_correction"
        else:
            for row in rows:
                assert (row["complete_silhouette"] == "True") == (row["entity_id"] in complete)
    excluded = set(repo_baseline["source_differences_at_capture"])
    immutable_checked = []
    for item in repo_baseline["files"]:
        rel = item["path"]
        if rel in excluded or rel in CENTRAL_OUTPUTS:
            continue
        assert v5.digest(PROJECT / rel) == item["sha256"], f"Prior file changed: {rel}"
        immutable_checked.append(rel)
    paths = import_files(manifest)
    assert not (set(paths) & excluded), "Import would overwrite prior publication-specific files"
    before = file_hashes(paths)
    result = subprocess.run([sys.executable, str(WORK / "consolidate_wave5.py")], cwd=PROJECT, check=True, text=True, capture_output=True)
    repeat = json.JSONDecoder().raw_decode(result.stdout.lstrip())[0]
    assert repeat["applied"] is False and repeat["new_assets_this_run"] == 0, "Consolidation is not idempotent"
    assert file_hashes(paths) == before, "Read-only repeat changed outputs"
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    evidence = {
        "generation_wave": 5, "checked_utc": stamp, "readable_checked_at": v5.display_date(stamp),
        "baseline_commit": baseline["baseline_commit"], "baseline_candidates_preserved": baseline["candidate_count"],
        "baseline_candidate_metadata_exact": True, "baseline_image_bytes_exact": True,
        "protected_fighter_and_boss_design_exact": True, "neutral_preferences_exact": True,
        "historical_counter_preservation": True, "historical_failures_preserved": baseline["historical_failures"],
        "prior_unmodified_files_verified": immutable_checked, "publication_specific_source_files_excluded": sorted(excluded),
        "new_images": copies, "counts": counts, "repeat_read_only_pass": repeat,
        "repeat_added_no_assets_or_failure_records": True, "repeat_did_not_modify_outputs": True,
        "guard_fighters_without_candidate": summary["guard_fighters_without_candidate"],
        "boss_entities_without_candidate": summary["boss_entities_without_candidate"],
        "boss_entities_without_complete_profile_candidate": summary["boss_entities_without_complete_profile_candidate"],
        "boss_entities_with_partial_visual_only": summary["boss_entities_with_partial_visual_only"],
        "scope": "Static candidate PNGs only; no animation, engine integration, or 1:1 certification. Technical QA is read-only. Existing generated candidates and downloaded game references are not new generations.",
    }
    if args.write or args.snapshot_to:
        v5.write_atomic(WORK / "verification.json", v5.json_text(evidence))
    if args.snapshot_to:
        destination = args.snapshot_to.resolve()
        if destination.exists():
            raise ValueError(f"Snapshot destination must be new: {destination}")
        paths = import_files(manifest)
        source_hashes = file_hashes(paths)
        rows = []
        for rel in paths:
            src, dst = PROJECT / rel, destination / "files" / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            assert v5.digest(dst) == source_hashes[rel], f"Snapshot copy differs: {rel}"
            rows.append({"path": rel, "sha256": source_hashes[rel], "bytes": dst.stat().st_size})
        assert source_hashes == file_hashes(paths), "Source changed during snapshot"
        inventory = {"created_utc": stamp, "baseline_commit": baseline["baseline_commit"], "snapshot_scope": "Explicit V5 imports only; preserve all other checkout files", "file_count": len(rows), "counts": counts, "files": rows}
        v5.write_atomic(destination / "FILES_SHA256.json", v5.json_text(inventory))
        v5.write_atomic(destination / "SHA256SUMS.txt", "".join(f"{r['sha256']}  {r['path']}\n" for r in rows))
        print(v5.json_text({"snapshot": str(destination), "files": len(rows), "inventory_sha256": v5.digest(destination / "FILES_SHA256.json")}))
    print(v5.json_text({"verification": "passed", "new_pngs": len(wave), "static_guard_pngs": len(guards), "boss_profile_pngs": len(profiles), "total_candidates": len(active), "prior_candidates_exact": baseline["candidate_count"], "read_only_repeat": repeat}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
