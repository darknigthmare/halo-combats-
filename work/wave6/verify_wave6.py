#!/usr/bin/env python3
"""Verify V6 conservation, art coverage and exact copies; optionally freeze imports.

The default is read-only. --write saves evidence. --snapshot-to freezes an
allowlist after every verification passes. Downloaded references are excluded.
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
WORK = PROJECT / "work/wave6"
spec = importlib.util.spec_from_file_location("halo_v6_consolidator", WORK / "consolidate_wave6.py")
v6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v6)
CENTRAL_OUTPUTS = [
    "README.md", "README_V6.md", "data/asset_manifest.json", "data/fighters.json",
    "data/delivery_counts.json", "data/characters_visual_inventory.csv",
    "data/expansion_characters.json", "data/expansion_characters_visual_inventory.csv",
    "docs/HALO_COMBATS_PERSONNAGES_V6.md", "docs/SOURCES_PERSONNAGES_V6.md",
]


def read(rel):
    return v6.read_json(PROJECT / rel)


def import_files(manifest):
    names = set(CENTRAL_OUTPUTS)
    names.update(a["path"] for a in manifest["active_candidates"] if a.get("generation_wave") == 6)
    for path in WORK.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.name.endswith((".pyc", ".tmp")):
            continue
        assert path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}, "Downloaded or generated images must not be hidden in work inputs"
        names.add(path.relative_to(PROJECT).as_posix())
    return sorted(names)


def hashes(names):
    return {p: v6.digest(PROJECT / p) for p in names}


def csv_rows(rel):
    with (PROJECT / rel).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--snapshot-to", type=Path)
    args = parser.parse_args()
    manifest = read("data/asset_manifest.json")
    roster = read("data/fighters.json")
    counts = read("data/delivery_counts.json")
    catalog = read("data/expansion_characters.json")
    baseline = read("work/wave6/baseline_v5.json")
    repo_base = read("work/wave6/baseline_repository_files.json")
    summary = read("work/wave6/consolidation_summary.json")
    records = v6.v4.records_from(read("work/wave6/generation_results.json"))
    qa = read("work/wave6/qa_wave6.json")
    reviews = qa["reviews"]
    v6.verify_baseline(manifest, baseline, counts, roster)
    assert len(roster["fighters"]) == 24
    source_entries, source_catalogs = v6.load_catalog(strict=True)
    assert source_catalogs == catalog["source_catalogs"] == summary["catalog_inputs"], "Catalog inputs changed"
    entries = catalog["entries"]
    entry_ids = {e["id"] for e in entries}
    assert len(entries) == len(entry_ids) == 34
    assert entry_ids == {e["id"] for e in source_entries}
    assert not entry_ids.intersection(f["id"] for f in roster["fighters"])
    for source in source_entries:
        entry = next(e for e in entries if e["id"] == source["id"])
        for key, value in source.items():
            assert entry[key] == value, "Catalog metadata lost: " + source["id"] + "/" + key
    for source in qa["input_reviews"]:
        assert v6.digest(PROJECT / source["path"]) == source["sha256"], "Contributing review changed"
    active = manifest["active_candidates"]
    by_id = {a["id"]: a for a in active}
    assert len(by_id) == len(active)
    assert len({a["sha256"] for a in active}) == len(active), "Identical bytes counted twice"
    wave = [a for a in active if a.get("generation_wave") == 6]
    copies = []
    for asset in active:
        assert v6.digest(PROJECT / asset["path"]) == asset["sha256"], "PNG bytes changed: " + asset["id"]
        if asset.get("generation_wave") != 6:
            continue
        source = Path(asset["source_path"])
        assert v6.digest(source) == asset["sha256"], "Original output differs: " + asset["id"]
        review = next((r for r in reviews if r["entity_id"] == asset["entity_id"] and r["sha256"] == asset["sha256"]), None)
        assert review and review.get("reviewed_utc"), "SHA-bound review missing"
        metrics = v6.v4.inspect_png(PROJECT / asset["path"])
        assert metrics == review["image_metrics"] == {k: asset[k] for k in metrics}, "Image measurements changed"
        assert asset["visual_review"] == review
        assert all(asset[k] == expected for k, expected in [("fidelity_status", "not_certified"), ("animation_status", "not_animated"), ("integration_status", "not_integrated")])
        assert asset["mode"] == "RGBA" and asset["alpha_range"][0] == 0 and asset["technical_qa"]["transparent_pixels"] > 0
        # A flawed output may be retained as evidence, with an explicit verdict.
        if any(asset["technical_qa"]["edge_contact_pixels_above_threshold"].values()):
            assert review["verdict"] == "candidate_requires_correction", "Frame contact must be acknowledged as requiring correction"
            assert not review.get("preferred_for_scope"), "Clipped output cannot be preferred"
        record = records[asset["journal_record"]]
        assert asset["observed_facing"] == review["observed_facing"] and asset["target_facing"] == record.get("target_facing", "right")
        for key in ("equipment_state", "facing", "variant", "journal_origin", "reference_input", "prompt", "attempt_kind", "entity_type", "pose_scope"):
            if key in record:
                assert asset.get(key) == record[key], "Generation metadata lost: " + key
        if asset["type"] == "expansion_character_pose":
            assert asset["entity_id"] in entry_ids and asset["roster_scope"] == "expansion" and asset["pose_scope"] == "initial_character_pose"
        else:
            assert asset["type"] == "fighter_pose" and asset["entity_id"] == "chief_infinite" and asset["roster_scope"] == "base" and asset["pose_scope"] == "guard_static"
        copies.append({"asset_id": asset["id"], "entity_id": asset["entity_id"], "path": asset["path"], "source_path": str(source), "sha256": asset["sha256"], "copy_exact": True, "visual_qa_sha_bound": True, "central_independent_visual_review": review["central_independent_visual_review"]})
    extension = [a for a in wave if a["type"] == "expansion_character_pose"]
    guards = [a for a in wave if a["type"] == "fighter_pose"]
    covered, reused = [], []
    for entry in entries:
        eid = entry["id"]
        assets = [a for a in active if a["type"] == "expansion_character_pose" and a["entity_id"] == eid]
        assert entry["new_visual_assets"] == [a["id"] for a in assets]
        assert entry["gameplay_design_status"] == "proposed_not_implemented"
        assert entry["fidelity_status"] == "not_certified" and entry["animation_status"] == "not_animated" and entry["integration_status"] == "not_integrated"
        if entry.get("reused_visual_asset"):
            assert eid == "warden_eternal_h5" and entry["generation_required"] is False and not assets
            old = by_id[entry["reused_visual_asset"]]
            assert old["id"] == "boss_warden_h5_profile_v01" and old["entity_id"] == "boss_warden_h5" and old["generation_wave"] == 5
            assert entry["visual_reuse"]["sha256"] == old["sha256"] and entry["visual_reuse"]["new_generation"] is False
            assert entry["visual_reuse"]["observed_facing"] == "left" and entry["visual_reuse"]["horizontal_mirror_performed"] is False
            assert entry["visual_assets"] == [old["id"]]
            reused.append(eid)
        else:
            assert entry["visual_assets"] == entry["new_visual_assets"]
        if entry["visual_assets"]:
            covered.append(eid)
        if entry.get("preferred_visual_asset"):
            assert entry["preferred_visual_asset"] in entry["visual_assets"]
            assert by_id[entry["preferred_visual_asset"]].get("visual_review_status") != "reviewed_candidate_requires_correction"
    assert reused == ["warden_eternal_h5"]
    assert counts["wave6_generation_attempts"] == len(records)
    assert counts["wave6_generation_failures"] == sum(v6.v4.is_failure(r) for r in records)
    assert counts["wave6_generated_pngs"] == len(wave)
    assert counts["wave6_generated_expansion_pngs"] == len(extension)
    assert counts["wave6_generated_guard_pngs"] == len(guards)
    assert counts["active_visual_candidates"] == baseline["candidate_count"] + len(wave) == len(active)
    assert counts["active_expansion_character_pose_candidates"] == len(extension)
    assert counts["expansion_catalog_entries"] == 34 and counts["expansion_catalog_entries_with_visual"] == len(covered)
    assert counts["expansion_catalog_entries_without_visual"] == 34 - len(covered)
    assert counts["expansion_catalog_entries_with_reused_visual"] == len(reused)
    assert counts["expansion_catalog_entries_with_preferred_visual"] == sum(bool(e.get("preferred_visual_asset")) for e in entries)
    assert counts["expansion_catalog_entries_requiring_correction_only"] == sum(e["art_status"] == "candidate_requires_correction" for e in entries)
    assert counts["expansion_catalog_entries_with_new_visual"] == len({a["entity_id"] for a in extension})
    assert counts["character_catalog_total_entries_including_base"] == 58
    assert counts["character_catalog_entities_with_visual_including_base"] == 24 + len(covered)
    for key, value in v6.design_counts(entries).items():
        assert counts[key] == value, "Proposed design count differs: " + key
    assert counts["historical_generation_failures_all_waves"] == len(manifest["failed_requests"])
    assert counts["animation_clips"] == 0 and counts["certified_visuals"] == 0
    assert summary["record_sha256"] == [v6.canonical_sha(r) for r in records]
    assert summary["journal_sha256"] == v6.digest(WORK / "generation_results.json")
    assert set(summary["expansion_entries_without_visual"]) == entry_ids - set(covered)
    base_rows = csv_rows("data/characters_visual_inventory.csv")
    expansion_rows = csv_rows("data/expansion_characters_visual_inventory.csv")
    assert len(base_rows) == len({r["entity_id"] for r in base_rows}) == 24
    assert len(expansion_rows) == 34 and {r["entity_id"] for r in expansion_rows} == entry_ids
    for row in expansion_rows:
        entry = next(e for e in entries if e["id"] == row["entity_id"])
        assert int(row["new_candidate_count"]) == len(entry["new_visual_assets"])
        assert row["reused_asset_id"] == entry.get("reused_visual_asset", "")
        assert row["all_candidate_paths"] == " ; ".join(by_id[aid]["path"] for aid in entry["visual_assets"])
        if entry["visual_assets"] and not entry.get("preferred_visual_asset"):
            assert row["observed_facing"] == "no_preferred_candidate" and row["visual_review_status"] == "reviewed_candidates_require_correction_no_preferred"
            assert "Aucun candidat préféré" in row["visual_qa"] and "Image non générée" not in row["visual_qa"]
        if row["preferred_asset_id"]:
            asset = by_id[row["preferred_asset_id"]]
            assert row["sha256"] == asset["sha256"] and row["relative_path"] == asset["path"]
            assert row["observed_facing"] == ("left" if entry.get("reused_visual_asset") else asset["observed_facing"])
        orientations = json.loads(row["candidate_orientations"])
        assert [o["asset_id"] for o in orientations] == entry["visual_assets"]
        for orientation in orientations:
            assert orientation["observed_facing"] == ("left" if entry.get("reused_visual_asset") else by_id[orientation["asset_id"]]["observed_facing"])
    chief_row = next(r for r in base_rows if r["entity_id"] == "chief_infinite")
    assert int(chief_row["historical_failure_count"]) == sum(v6.v4.entity_id(f) == "chief_infinite" for f in manifest["failed_requests"])
    excluded = set(repo_base["source_differences_at_capture"])
    immutable = []
    for row in repo_base["files"]:
        if row["path"] in excluded or row["path"] in CENTRAL_OUTPUTS:
            continue
        assert v6.digest(PROJECT / row["path"]) == row["sha256"], "Prior source file changed: " + row["path"]
        immutable.append(row["path"])
    names = import_files(manifest)
    assert not set(names).intersection(excluded), "Publication-specific baseline file would be overwritten"
    before = hashes(names)
    repeated = subprocess.run([sys.executable, str(WORK / "consolidate_wave6.py")], cwd=PROJECT, check=True, capture_output=True, text=True)
    repeat = json.loads(repeated.stdout)
    assert repeat["applied"] is False and repeat["new_assets_this_run"] == 0
    assert hashes(names) == before, "Read-only repeated consolidation modified files"
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    evidence = {"generation_wave": 6, "checked_utc": stamp, "readable_checked_at": v6.v5.display_date(stamp),
                "baseline_commit": baseline["baseline_commit"], "baseline_candidates_preserved": baseline["candidate_count"],
                "baseline_candidate_metadata_exact": True, "baseline_image_bytes_exact": True,
                "base_roster_24_and_neutral_preferences_exact": True, "boss_registry_exact": True,
                "historical_counter_preservation": True, "historical_failures_preserved": baseline["historical_failures"],
                "prior_unmodified_files_verified": immutable, "publication_specific_source_files_excluded": sorted(excluded),
                "new_images": copies, "counts": counts, "catalog_entries": len(entries), "reused_prior_assets_not_regenerated": reused,
                "repeat_read_only_pass": repeat, "repeat_did_not_modify_outputs": True,
                "expansion_entries_without_visual": summary["expansion_entries_without_visual"],
                "guard_fighters_without_candidate": summary["guard_fighters_without_candidate"],
                "scope": "Static candidate art catalog only. No 1:1 certification, animation or automatic gameplay integration. PNG bytes copied unchanged."}
    if args.write or args.snapshot_to:
        v6.write_atomic(WORK / "verification.json", v6.json_text(evidence))
    if args.snapshot_to:
        destination = args.snapshot_to.resolve()
        assert not destination.exists(), "Snapshot destination must be new"
        names = import_files(manifest)
        source_hashes = hashes(names)
        rows = []
        for rel in names:
            src, dst = PROJECT / rel, destination / "files" / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            assert v6.digest(dst) == source_hashes[rel], "Snapshot copy differs"
            rows.append({"path": rel, "sha256": source_hashes[rel], "bytes": dst.stat().st_size})
        assert source_hashes == hashes(names), "Source changed during snapshot"
        inv = {"created_utc": stamp, "baseline_commit": baseline["baseline_commit"], "snapshot_scope": "Explicit V6 imports only; preserve all other checkout files", "file_count": len(rows), "counts": counts, "files": rows}
        v6.write_atomic(destination / "FILES_SHA256.json", v6.json_text(inv))
        v6.write_atomic(destination / "SHA256SUMS.txt", "".join(f"{r['sha256']}  {r['path']}\n" for r in rows))
        print(v6.json_text({"snapshot": str(destination), "files": len(rows), "inventory_sha256": v6.digest(destination / "FILES_SHA256.json")}))
    print(v6.json_text({"verification": "passed", "new_pngs": len(wave), "extension_pngs": len(extension), "guard_pngs": len(guards), "total_candidates": len(active), "catalog_entries_with_visual": len(covered), "reused_prior_assets": len(reused), "prior_candidates_exact": baseline["candidate_count"], "read_only_repeat": repeat}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
