#!/usr/bin/env python3
"""Combine visual reviews, verify image hashes, and measure PNGs without editing pixels.

Default is read-only. --apply writes qa_wave6.json. --require-complete verifies
that every successful record in the frozen merged journal has a bound review.
Individual agent journals and review files are never modified.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
WORK = PROJECT / "work/wave6"
INPUTS = ["qa_unsc.json", "qa_aliens.json", "qa_root.json", "qa_central_reviews.json"]
spec = importlib.util.spec_from_file_location("halo_wave6", WORK / "consolidate_wave6.py")
v6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v6)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    grouped, inputs = {}, []
    for filename in INPUTS:
        path = WORK / filename
        if not path.exists():
            continue
        data = v6.read_json(path)
        rows = v6.v4.load_visual_qa(path)
        inputs.append({"path": path.relative_to(PROJECT).as_posix(), "sha256": v6.digest(path), "reviews": len(rows)})
        for row in rows:
            assert row.get("entity_id") and row.get("reviewed_utc") and row.get("sha256"), "Incomplete QA identity: " + filename
            source = Path(row["source_path"])
            assert source.is_file() and v6.digest(source) == row["sha256"], "Reviewed bytes changed: " + str(source)
            assert row.get("verdict") in {"candidate_with_reservations", "candidate_requires_correction"}, "Unexpected review verdict"
            assert isinstance(row.get("notes"), list) and row["notes"], "Review notes absent"
            assert all(isinstance(n, str) for n in row["notes"]), "Review notes must be text"
            references = row.get("reference_reviewed", [])
            references = [references] if isinstance(references, dict) else references
            for reference in references:
                assert v6.digest(Path(reference["path"])) == reference["sha256"], "Reference changed after independent review"
            review = copy.deepcopy(row)
            review["review_source"] = path.relative_to(PROJECT).as_posix()
            grouped.setdefault((row["entity_id"], row["sha256"]), []).append(review)
    combined = []
    for (owner, sha), reviews in sorted(grouped.items()):
        source = Path(reviews[0]["source_path"])
        metrics = v6.v4.inspect_png(source)
        notes = list(dict.fromkeys(n for r in reviews for n in r["notes"]))
        followup = list(dict.fromkeys(n for r in reviews for n in r.get("required_followup", [])))
        correction = any(r["verdict"] == "candidate_requires_correction" for r in reviews)
        qa = metrics["technical_qa"]
        alpha_note = (f"Mesure indépendante sans retouche : {metrics['width']} × {metrics['height']} px, {metrics['mode']}, "
                      f"alpha {metrics['alpha_range'][0]}–{metrics['alpha_range'][1]}, {qa['transparent_pixels']} pixels entièrement transparents. "
                      f"Contacts du cadre au seuil alpha > {qa['foreground_alpha_threshold']} : {qa['edge_contact_pixels_above_threshold']}. "
                      f"Marges au même seuil : {qa['canvas_margins_px_above_threshold']}.")
        notes.append(alpha_note)
        if qa["warnings"]:
            followup.extend(str(w) for w in qa["warnings"])
        selected = [r["preferred_for_scope"] for r in reviews if "preferred_for_scope" in r]
        row = {"entity_id": owner, "source_path": str(source), "sha256": sha,
               "reviewed_utc": max(r["reviewed_utc"] for r in reviews),
               "verdict": "candidate_requires_correction" if correction else "candidate_with_reservations",
               "notes": notes, "required_followup": list(dict.fromkeys(followup)),
               "image_metrics": metrics, "contributing_reviews": reviews,
               "central_independent_visual_review": any(r["review_source"].endswith("qa_central_reviews.json") for r in reviews)}
        observed = [r["observed_facing"] for r in reviews if r.get("observed_facing")]
        row["observed_facing"] = observed[-1] if observed else "not_recorded"
        if selected:
            row["preferred_for_scope"] = bool(selected[-1]) and not correction
        combined.append(row)
    missing = []
    journal = WORK / "generation_results.json"
    if journal.is_file():
        for record in v6.v4.records_from(v6.read_json(journal)):
            if v6.v4.is_failure(record):
                continue
            source = v6.v4.resolve_source(record, journal)
            if source is None or not source.is_file():
                missing.append({"entity_id": v6.v4.entity_id(record), "status": record.get("status", "source_missing")})
                continue
            key = (v6.v4.entity_id(record), v6.digest(source))
            if key not in grouped:
                missing.append({"entity_id": key[0], "sha256": key[1]})
    elif args.require_complete:
        raise ValueError("Merged generation journal missing")
    if args.require_complete:
        assert not missing, "Successful records without SHA-bound visual review: " + json.dumps(missing)
    result = {"generation_wave": 6, "review_policy": "Independent visual reviews and read-only PNG measurements; no 1:1 certification, animation or engine integration.",
              "updated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "input_reviews": inputs, "reviews": combined}
    if args.apply:
        assert all(v6.digest(PROJECT / r["path"]) == r["sha256"] for r in inputs), "QA inputs changed during merge"
        v6.write_atomic(WORK / "qa_wave6.json", v6.json_text(result))
    print(v6.json_text({"applied": args.apply, "review_count": len(combined), "central_independent_reviews": sum(r["central_independent_visual_review"] for r in combined), "missing_reviews": missing}))


if __name__ == "__main__":
    main()
