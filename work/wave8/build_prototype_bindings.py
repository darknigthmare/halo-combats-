#!/usr/bin/env python3
"""Build portable V8 static-asset bindings without changing source data or PNGs.

Run with a Python environment providing Pillow. --check verifies the committed
JSON instead of writing it. All pixel operations are read-only measurements.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "data/prototype_asset_bindings_v8.json"
BOOTSTRAP = ROOT / "prototype/lab_v8/catalog.js"
REPORT = ROOT / "work/wave8/prototype_bindings_validation.json"
PRIOR_BINDING = ROOT / "data/prototype_asset_bindings_v7.json"
INPUTS = {
    "fighters": ("data/fighters.json", "fighters"),
    "expansions": ("data/expansion_characters.json", "entries"),
    "bosses": ("data/bosses.json", "entities"),
    "stages": ("data/stages.json", "stages"),
    "assets": ("data/asset_manifest.json", "active_candidates"),
}
USAGE_ORDER = ("catalog", "combat_neutral", "combat_guard", "boss", "stage")
STATUS_VALUES = {"candidate", "needs_correction", "missing"}


def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unique(items):
    return list(dict.fromkeys(x for x in items if x))


def portable_text(value):
    """Do not publish temporary local reference paths through runtime metadata."""
    if not isinstance(value, str):
        return value
    return re.sub(r"/workspace/[^\s\"'<>]+", "[référence locale non publiée]", value)


def checked_repo_path(value, suffix=None):
    if not isinstance(value, str) or not value:
        raise ValueError(f"Invalid empty repository path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value or urlparse(value).scheme:
        raise ValueError(f"Non-portable repository path: {value!r}")
    absolute = (ROOT / value).resolve()
    if not absolute.is_relative_to(ROOT) or not absolute.is_file():
        raise ValueError(f"Missing repository file: {value!r}")
    if suffix and absolute.suffix.lower() != suffix:
        raise ValueError(f"Wrong file type: {value!r}")
    return value


def source_links(*values):
    """Collect documentary URLs; none of these are image-rendering paths."""
    found = []
    seen = set()

    def walk(value, key=""):
        if isinstance(value, dict):
            for k, v in value.items():
                if k in {"local_ref", "source_path", "inspection_local_ref", "path", "paths"}:
                    continue
                walk(v, k)
        elif isinstance(value, list):
            for item in value:
                walk(item, key)
        elif isinstance(value, str) and value.startswith(("https://", "http://")):
            if value not in seen:
                seen.add(value)
                found.append({
                    "url": value,
                    "kind": key or "documentary_reference",
                    "use": "documentary_link_only",
                })

    for value in values:
        walk(value)
    return found


def observed_direction(asset):
    """Use recorded observations, never the intended prompt or filename."""
    if asset["id"] == "scarab_h3_profile_v2":
        # Individual view_image inspection of this exact original PNG was reported
        # by wave7_unsc while implementing the V7 lab; this is not a filename guess.
        return (
            "left", "left_three_quarter", "v7_individual_original_png_inspection",
            "Inspection individuelle V7 : véhicule entier, émetteur/tête orienté vers la gauche et quatre pieds visibles. Aucun retournement du PNG."
        )
    review = asset.get("visual_review") or {}
    raw = asset.get("observed_facing") or review.get("observed_facing")
    if raw:
        lower = raw.lower()
        native = ("front" if "front" in lower else
                  "left" if "left" in lower else
                  "right" if "right" in lower else "unknown")
        return native, raw, "manifest.observed_facing", None

    notes = review.get("notes", [])
    # These literal statements concern the generated output in existing QA.
    # Check frontal observations before left-facing requests mentioned negatively.
    front_phrases = (
        "la sortie est presque frontale",
        "pose surtout frontale",
        "la silhouette reste très frontale",
        "module partiel frontal",
        "module partiel uniquement : noyau frontal",
    )
    for note in notes:
        if any(phrase in note.lower() for phrase in front_phrases):
            return "front", "mostly_front", "manifest.visual_review.notes", note

    right_phrases = (
        "orientée vers la droite", "orienté vers la droite",
        "tourné vers la droite", "tournée vers la droite",
        "regarde vers la droite", "vers la droite en trois",
        "trois-quarts vers la droite", "profil vers la droite",
        "garde statique lisible vers la droite", "garde statique vers la droite",
        "garde statique de boxe lisible vers la droite",
        "garde statique lourde vers la droite", "garde statique massive vers la droite",
        "garde armée statique vers la droite", "garde armée vers la droite",
        "garde à mains vides vers la droite", "garde à mains ouvertes vers la droite",
        "garde défensive vers la droite", "garde de corps à corps vers la droite",
        "la pose est calme, vers la droite", "debout vers la droite",
        "pose neutre entière vers la droite", "pose neutre vers la droite",
        "la direction vers la droite", "principalement latérale vers la droite",
    )
    left_phrases = (
        "entier tourné vers la gauche", "entier, orienté vers la gauche",
        "orientée vers la gauche", "orienté vers la gauche",
        "la pose tourne vers la gauche", "son avant est à gauche",
        "la proue pointe vers la gauche", "orienté en diagonale vers la gauche",
        "le pilote regarde vers la gauche", "entier orienté vers la gauche",
    )
    for native, phrases in (("right", right_phrases), ("left", left_phrases)):
        for note in notes:
            # A source description or a failed requested direction is not observation.
            lower = note.lower()
            if ("ne satisfait pas la demande" in lower
                    or "dans la référence orientée" in lower
                    or "référence source orientée" in lower):
                continue
            if any(phrase in lower for phrase in phrases):
                return native, f"{native}_as_recorded_in_review", "manifest.visual_review.notes", note
    # The three partial modules explicitly have a documented frontal presentation.
    if asset.get("facing") == "reference_supported_front":
        return "front", "reference_supported_front", "manifest.facing", None
    return "unknown", "not_recorded_unambiguously", "not_inferred_from_filename_or_prompt", None


def measure_png(path, manifest):
    sha = digest(path)
    if sha != manifest["sha256"]:
        raise ValueError(f"SHA mismatch: {manifest['id']}")
    with Image.open(path) as image:
        image.load()
        width, height = image.size
        if (width, height) != (manifest["width"], manifest["height"]):
            raise ValueError(f"Dimension mismatch: {manifest['id']}")
        has_alpha = "A" in image.getbands()
        alpha_range = None
        bbox = nonzero_bbox = None
        if has_alpha:
            alpha = image.getchannel("A")
            alpha_range = list(alpha.getextrema())
            nonzero_bbox = alpha.getbbox()
            # A thresholded in-memory measurement mask is never saved or composited.
            bbox = alpha.point(lambda value: 255 if value > 16 else 0).getbbox()
        if alpha_range != manifest.get("alpha_range"):
            raise ValueError(f"Alpha-range mismatch: {manifest['id']}")
        return {
            "sha256": sha,
            "dimensions": {"width": width, "height": height},
            "width": width,
            "height": height,
            "mode": image.mode,
            "alpha_bbox": list(bbox) if bbox else None,
            "alpha": {
                "present": has_alpha,
                "range": alpha_range,
                "bbox_nonzero": list(nonzero_bbox) if nonzero_bbox else None,
                "bbox_above_threshold": list(bbox) if bbox else None,
                "foreground_threshold": 16 if has_alpha else None,
                "measurement": "read_only_original_png",
            },
        }


def make_asset(asset, all_entities):
    path = checked_repo_path(asset["path"], ".png")
    review = asset.get("visual_review") or {}
    status = ("needs_correction"
              if "requires_correction" in str(review.get("verdict", ""))
              or "requires_correction" in str(asset.get("visual_review_status", ""))
              else "candidate")
    native, observed, evidence, quote = observed_direction(asset)
    pose = asset.get("pose_scope") or {
        "fighter_pose": "neutral_static",
        "boss_profile": "boss_profile",
        "stage_master": "stage_master",
    }.get(asset["type"], "static_candidate")
    entity_sources = [
        entity for entity in all_entities
        if entity["id"] == asset["entity_id"] or asset["id"] in entity.get("visual_assets", [])
    ]
    refs = [
        {
            key: entity[key] for key in ("source_url", "source_title", "sources")
            if key in entity
        } for entity in entity_sources
    ]
    links = source_links(
        {"reference_urls": asset.get("reference_urls", [])},
        asset.get("reference_input", {}),
        asset.get("additional_reference_inputs", []),
        refs,
    )
    source_journal = asset.get("source_journal")
    if source_journal:
        checked_repo_path(source_journal, ".json")
    return {
        "id": asset["id"],
        "asset_id": asset["id"],
        "entity_id": asset["entity_id"],
        "entity_ids": [],
        "path": path,
        "type": asset["type"],
        "status": status,
        **measure_png(ROOT / path, asset),
        "pose": pose,
        "variant": str(asset.get("variant") or asset["id"]),
        "native_facing": native,
        "observed_facing": observed,
        "facing_evidence": evidence,
        "facing_evidence_note": portable_text(quote),
        "mirror_allowed": False,
        "preferred": False,
        "preferred_for": [],
        "source": f"Image candidate Halo Combats ; {source_journal or 'lot initial V1/V2'}",
        "sources": links,
        "provenance": {
            "manifest": "data/asset_manifest.json",
            "source_journal": source_journal,
            "generation_wave": asset.get("generation_wave", 1),
            "reference_kind": (
                asset.get("reference_input", {}).get("kind")
                if isinstance(asset.get("reference_input"), dict) else None
            ),
        },
        "qa": {
            "summary": portable_text(asset.get("qa", "")),
            "review_status": asset.get("visual_review_status", "initial_candidate_notes"),
            "verdict": review.get("verdict", "candidate_not_certified"),
            "notes": [portable_text(note) for note in review.get("notes", [])],
            "technical_warnings": [
                portable_text(note) for note in asset.get("technical_qa", {}).get("warnings", [])
            ],
        },
        "limitations": unique(
            portable_text(note) for note in
            asset.get("required_followup", []) + review.get("required_followup", [])
        ),
        "fidelity_status": "not_certified",
        "animation_status": "not_animated",
        "representation_scope": asset.get("representation_scope", "static_candidate_only"),
        "complete_silhouette": asset.get("complete_silhouette"),
        "depicted_region": asset.get("depicted_region"),
    }


def make_document():
    lists = {}
    for name, (path, key) in INPUTS.items():
        lists[name] = json.loads((ROOT / path).read_text())[key]
    expected = {"fighters": 24, "expansions": 34, "bosses": 20, "stages": 24, "assets": 94}
    for name, count in expected.items():
        if len(lists[name]) != count:
            raise ValueError(f"Unexpected {name} count: {len(lists[name])}, expected {count}")
        ids = [entry["id"] for entry in lists[name]]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate IDs in {name}")

    source_assets = {asset["id"]: asset for asset in lists["assets"]}
    entities = lists["fighters"] + lists["expansions"] + lists["bosses"] + lists["stages"]
    index = {asset["id"]: make_asset(asset, entities) for asset in lists["assets"]}
    if len({asset["path"] for asset in index.values()}) != 94:
        raise ValueError("The asset index contains duplicate physical paths")
    usages = defaultdict(set)

    def attach(asset_id, entity_id, usage="catalog", preferred=False):
        if asset_id not in index:
            raise ValueError(f"Unknown asset {asset_id} referenced by {entity_id}")
        asset = index[asset_id]
        if entity_id not in asset["entity_ids"]:
            asset["entity_ids"].append(entity_id)
        usages[asset_id].add(usage)
        if preferred:
            if asset["status"] != "candidate":
                raise ValueError(f"Correction-required asset selected as preferred: {asset_id}")
            asset["preferred"] = True
            record = {"entity_id": entity_id, "usage": usage}
            if record not in asset["preferred_for"]:
                asset["preferred_for"].append(record)

    def ref(asset_id, label=None):
        if not asset_id:
            return {
                "id": None, "asset_id": None, "label": label or "Image manquante",
                "path": None, "status": "missing", "native_facing": "unknown",
                "source": None, "preferred": False, "mirror_allowed": False,
            }
        asset = index[asset_id]
        return {
            "id": asset_id,
            "asset_id": asset_id,
            "label": label or f"{asset['pose']} · {asset['variant']}",
            "path": asset["path"],
            "status": asset["status"],
            "native_facing": asset["native_facing"],
            "observed_facing": asset["observed_facing"],
            "pose": asset["pose"],
            "variant": asset["variant"],
            "source": asset["source"],
            "sources": asset["sources"],
            "sha256": asset["sha256"],
            "dimensions": asset["dimensions"],
            "alpha_bbox": asset["alpha_bbox"],
            "mirror_allowed": False,
            "preferred": asset["preferred"],
        }

    def asset_ids(entity):
        ids = unique(
            entity.get("visual_assets", [])
            + [a["id"] for a in lists["assets"] if a["entity_id"] == entity["id"]]
        )
        for asset_id in ids:
            attach(asset_id, entity["id"])
        return ids

    def select(ids, explicit=None):
        def eligible(asset_id):
            review = source_assets[asset_id].get("visual_review") or {}
            return index[asset_id]["status"] == "candidate" and review.get("preferred_for_scope") is not False
        if explicit:
            if explicit not in ids or not eligible(explicit):
                raise ValueError(f"Invalid explicit preferred asset: {explicit}")
            return explicit
        good = [asset_id for asset_id in ids if eligible(asset_id)]
        if len(good) > 1:
            raise ValueError(f"Several candidates require an explicit preferred flag: {good}")
        return good[0] if good else None

    def status_for(ids):
        if any(index[asset_id]["status"] == "candidate" for asset_id in ids):
            return "candidate"
        return "needs_correction" if ids else "missing"

    base = []
    for entity in lists["fighters"]:
        ids = asset_ids(entity)
        guards = [asset_id for asset_id in ids if index[asset_id]["pose"] == "guard_static"]
        neutral_ids = [asset_id for asset_id in ids if asset_id not in guards]
        neutral = select(neutral_ids, entity.get("preferred_visual_asset"))
        guard = select(guards, entity.get("preferred_guard_asset"))
        if neutral:
            attach(neutral, entity["id"], "combat_neutral", True)
        if guard:
            attach(guard, entity["id"], "combat_guard", True)
        base.append({
            "id": entity["id"], "name": entity["name"], "source_game": entity["era"],
            "status": status_for(ids), "playable": True, "roster_scope": "base",
            "mechanics_scope": "shared_partial_prototype",
            "moveset_id": entity["id"],
            "full_moveset_implemented": False,
            "native_facing": index[neutral]["native_facing"] if neutral else "unknown",
            "preferred_asset": neutral, "preferred_guard_asset": guard,
            "assets": {"neutral": ref(neutral, "Pose neutre"), "guard": ref(guard, "Garde statique")},
            "variants": [ref(asset_id) for asset_id in ids],
            "source": entity["era"],
            "sources": source_links({"source_url": entity.get("source_url")}),
            "mirror_allowed": False,
        })

    expansions = []
    for entity in lists["expansions"]:
        ids = asset_ids(entity)
        preferred = select(ids, entity.get("preferred_visual_asset"))
        if entity["id"] == "dinh_infinite":
            if preferred is not None or status_for(ids) != "needs_correction":
                raise ValueError("Dinh must remain available for review without a preferred asset")
        if preferred:
            attach(preferred, entity["id"], "catalog", True)
        expansions.append({
            "id": entity["id"], "name": entity["name"],
            "source_game": entity["game_version"], "category": entity["category"],
            "status": status_for(ids), "playable": False, "roster_scope": "expansion",
            "mechanics_scope": "catalog_only", "moveset_id": None,
            "full_moveset_implemented": False,
            "preferred_asset": preferred,
            "variants": [ref(asset_id) for asset_id in ids],
            "source": entity["game_version"],
            "sources": source_links(entity.get("sources", [])),
            "mirror_allowed": False,
            "image_missing": not ids,
        })

    bosses = []
    for entity in lists["bosses"]:
        ids = asset_ids(entity)
        preferred = select(ids, entity.get("preferred_visual_asset"))
        mechanic = entity["id"] == "boss_scarab_h3"
        if preferred:
            attach(preferred, entity["id"], "boss" if mechanic else "catalog", True)
        bosses.append({
            "id": entity["id"], "name": entity["name"], "source_game": entity["origin"],
            "status": status_for(ids), "playable": False,
            "mechanic_playable": mechanic,
            "mechanics_scope": "existing_partial_scarab_encounter" if mechanic else "catalog_only",
            "preferred_asset": preferred,
            "variants": [ref(asset_id) for asset_id in ids],
            "source": entity["origin"],
            "sources": source_links({"source_url": entity.get("source_url")}),
            "mirror_allowed": False,
        })

    stages = []
    for entity in lists["stages"]:
        ids = asset_ids(entity)
        preferred = select(ids, entity.get("preferred_visual_asset"))
        if preferred:
            attach(preferred, entity["id"], "stage", True)
        binding = ref(preferred)
        stages.append({
            "id": entity["id"], "name": entity["name"], "source_game": entity["origin"],
            "status": status_for(ids), "asset_id": preferred, "preferred_asset": preferred,
            "path": binding["path"], "variants": [ref(asset_id) for asset_id in ids],
            "source": entity["origin"],
            "sources": source_links({"source_url": entity.get("source_url")}),
            "render_scope": "single_flat_master" if preferred else "no_generated_image",
            "independent_parallax_layers": 0, "planned_parallax_layers": len(entity.get("layers", [])),
            "mirror_allowed": False,
        })

    if set(usages) != set(index):
        raise ValueError(f"Orphan assets: {sorted(set(index) - set(usages))}")
    # Preferred state is finalized only after every entity and cross-roster reuse.
    for group in (base, expansions, bosses, stages):
        for entity in group:
            for variant in entity.get("variants", []):
                variant["preferred"] = index[variant["asset_id"]]["preferred"]

    usage_rows = [{
        "asset_id": asset_id, "path": index[asset_id]["path"],
        "usages": [name for name in USAGE_ORDER if name in usages[asset_id]],
        "entity_ids": index[asset_id]["entity_ids"],
        "usage_scope": "static_prototype_only",
    } for asset_id in index]
    counts = {
        "base_fighters": len(base), "playable_base_fighters": sum(x["playable"] for x in base),
        "expansion_characters": len(expansions), "playable_expansion_characters": 0,
        "character_catalog_entries": len(base) + len(expansions),
        "bosses": len(bosses), "boss_mechanics_available": sum(x["mechanic_playable"] for x in bosses),
        "stages": len(stages), "stage_masters": sum(bool(x["path"]) for x in stages),
        "missing_stage_images": sum(not x["path"] for x in stages),
        "unique_png_assets": len(index),
        "candidate_png_assets": sum(x["status"] == "candidate" for x in index.values()),
        "png_assets_needing_correction": sum(x["status"] == "needs_correction" for x in index.values()),
        "base_neutral_bindings": sum(bool(x["assets"]["neutral"]["path"]) for x in base),
        "base_guard_bindings": sum(bool(x["assets"]["guard"]["path"]) for x in base),
        "missing_base_guard_images": sum(not x["assets"]["guard"]["path"] for x in base),
        "illustrated_expansion_entries": sum(bool(x["variants"]) for x in expansions),
        "missing_expansion_images": sum(not x["variants"] for x in expansions),
        "unique_expansion_origin_pngs": sum(a["type"] == "expansion_character_pose" for a in index.values()),
        "animated_assets": 0, "certified_1_to_1_assets": 0, "independent_parallax_layers": 0,
    }
    document = {
        "schema_version": 1, "project": "Halo Combats", "wave": 8,
        "scope": "Laboratoire statique de mécanique commune et catalogue des candidats existants.",
        "source_files": [path for path, _ in INPUTS.values()],
        "path_base": "repository_root",
        "bitmap_source_rule": "Only repository-relative paths in assets_index may be rendered.",
        "render_policy": {
            "preserve_native_pose": True, "mirroring_allowed": False,
            "animation_available": False, "one_to_one_fidelity_certified": False,
            "missing_assets": "explicit_missing_state_without_external_artwork",
            "source_urls": "documentary_links_only_never_bitmap_src",
        },
        "limitations": [
            "Les PNG sont des poses statiques candidates ; leur consultation ne vaut pas animation ni fidélité certifiée.",
            "Les 24 profils de base partagent le laboratoire mécanique partiel ; leurs movesets complets ne sont pas tous implémentés.",
            "Les 34 extensions sont consultables dans le catalogue uniquement et restent exclues du choix de combattant.",
            "Seul le Scarab possède la mécanique de boss partielle existante ; les 19 autres entrées restent consultatives.",
            "Deux masters de décor plats sont disponibles ; aucun calque de parallaxe indépendant n’est livré.",
            "Les orientations non documentées restent inconnues ; les noms de fichiers et prompts ne prouvent pas l’orientation observée.",
            "Les sources externes servent à la provenance et ne remplacent aucune image manquante.",
        ],
        "counts": counts, "base_fighters": base, "expansion_characters": expansions,
        "bosses": bosses, "stages": stages, "assets_index": index, "asset_usages": usage_rows,
    }
    validate(document)
    return document


def validate(document):
    index = document["assets_index"]
    c = document["counts"]
    assert c["base_fighters"] == 24 and c["expansion_characters"] == 34
    assert c["character_catalog_entries"] == 58 and c["bosses"] == 20
    assert c["stages"] == 24 and c["stage_masters"] == 2
    assert c["unique_png_assets"] == 94 and c["base_guard_bindings"] == 23
    assert c["missing_expansion_images"] == 13 and c["illustrated_expansion_entries"] == 21
    assert c["png_assets_needing_correction"] == 6
    prior = json.loads(PRIOR_BINDING.read_text())
    assert len(prior["assets_index"]) == 90
    for asset_id, previous in prior["assets_index"].items():
        assert index[asset_id] == previous, f"Historical binding changed: {asset_id}"
    for group in ("base_fighters", "bosses", "stages"):
        assert document[group] == prior[group], f"Historical {group} binding changed"
    new_ids = set(index) - set(prior["assets_index"])
    assert len(new_ids) == 4
    usages = {row["asset_id"]: row for row in document["asset_usages"]}
    for asset_id in new_ids:
        assert index[asset_id]["provenance"]["generation_wave"] == 8
        assert index[asset_id]["type"] == "expansion_character_pose"
        assert usages[asset_id]["usages"] == ["catalog"]
    assert not any(x["playable"] or x["moveset_id"] for x in document["expansion_characters"])
    assert {x["id"] for x in document["bosses"] if x["mechanic_playable"]} == {"boss_scarab_h3"}
    assert set(index["boss_warden_h5_profile_v01"]["entity_ids"]) == {"warden_eternal_h5", "boss_warden_h5"}
    dinh = next(x for x in document["expansion_characters"] if x["id"] == "dinh_infinite")
    assert dinh["status"] == "needs_correction" and dinh["preferred_asset"] is None
    assert index["dinh_infinite_initial_right_v01"]["preferred"] is False
    chief = next(x for x in document["base_fighters"] if x["id"] == "chief_infinite")
    assert chief["assets"]["guard"]["status"] == "missing"
    assert chief["assets"]["guard"]["path"] is None
    for asset in index.values():
        assert asset["status"] in STATUS_VALUES
        assert asset["native_facing"] in {"left", "right", "front", "unknown"}
        assert asset["mirror_allowed"] is False
        assert asset["entity_ids"]
        checked_repo_path(asset["path"], ".png")
    for row in document["asset_usages"]:
        assert row["asset_id"] in index and row["path"] == index[row["asset_id"]]["path"]
        assert row["usages"] and set(row["usages"]).issubset(USAGE_ORDER)
        assert "catalog" in row["usages"]
        if index[row["asset_id"]]["status"] == "needs_correction":
            assert row["usages"] == ["catalog"]
    text = encode(document)
    assert "/workspace/" not in text and "data:image" not in text
    assert not any("http" in a["path"] for a in index.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify current binding without writing files")
    args = parser.parse_args()
    document = make_document()
    contents = encode(document)
    bootstrap_contents = (
        "// Generated by work/wave8/build_prototype_bindings.py; same data as the JSON.\n"
        "window.HALO_COMBATS_DATA = " + contents.rstrip() + ";\n"
    )
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text() != contents:
            raise SystemExit("FAIL: binding is missing or differs from deterministic source rebuild")
        if not BOOTSTRAP.is_file() or BOOTSTRAP.read_text() != bootstrap_contents:
            raise SystemExit("FAIL: classic-script bootstrap differs from the JSON payload")
    else:
        OUTPUT.write_text(contents)
        BOOTSTRAP.parent.mkdir(parents=True, exist_ok=True)
        BOOTSTRAP.write_text(bootstrap_contents)
    usage_counts = Counter(usage for row in document["asset_usages"] for usage in row["usages"])
    report = {
        "schema_version": 1, "wave": 8, "result": "pass",
        "binding_path": OUTPUT.relative_to(ROOT).as_posix(),
        "binding_sha256": hashlib.sha256(contents.encode()).hexdigest(),
        "bootstrap_path": BOOTSTRAP.relative_to(ROOT).as_posix(),
        "bootstrap_sha256": hashlib.sha256(bootstrap_contents.encode()).hexdigest(),
        "json_bootstrap_parity": True,
        "counts": document["counts"], "asset_usage_counts": dict(usage_counts),
        "checked_asset_ids": list(document["assets_index"]),
        "prior_binding_path": PRIOR_BINDING.relative_to(ROOT).as_posix(),
        "prior_binding_sha256": digest(PRIOR_BINDING),
        "historical_asset_bindings_unchanged": 90,
        "new_catalog_only_pngs": 4,
        "checks": [
            "94 unique repo-local PNG paths exist and match manifest SHA-256, dimensions and alpha ranges.",
            "Read-only alpha bounding boxes measured; no PNG written, mirrored, resized or encoded as base64.",
            "All catalogue IDs resolve and all 94 assets have a catalogue usage, including prior variants.",
            "24 base fighters selectable; 34 expansion entries remain catalogue-only.",
            "Four V8 PNGs add catalogue images only; 21 extension entries are illustrated and 13 remain missing.",
            "All 90 previous asset bindings and base/boss/stage bindings match V7 exactly.",
            "A visual review with preferred_for_scope=false cannot be promoted to a preferred image.",
            "Preferred neutral and guard assets are explicit; Chief guard remains missing.",
            "Six correction-required PNGs have catalogue usage only; Dinh has no preferred asset.",
            "Warden is one indexed PNG reused by two catalogue entities.",
            "Only Scarab has the existing boss mechanic; 19 other boss entries remain catalogue-only.",
            "24 stages reference exactly two flat master PNGs; 22 explicitly lack an image.",
            "No workspace path, external bitmap source or data-image payload occurs in rendering bindings.",
            "Native orientation uses recorded QA observations; filename and prompt are not treated as observed evidence.",
            "The classic-script bootstrap assigns the same JSON payload to window.HALO_COMBATS_DATA without requiring fetch.",
        ],
        "limits": [
            "This validates data bindings and file integrity, not browser rendering or completed gameplay.",
            "No new canonical comparison is claimed; fidelity QA is inherited from the manifest. Scarab facing was independently observed in V7.",
            "No animation, independent parallax layers or 1:1 fidelity is certified.",
        ],
    }
    if not args.check:
        REPORT.write_text(encode(report))
    print(encode({"result": "pass", "binding": str(OUTPUT.relative_to(ROOT)),
                  "counts": document["counts"], "usages": dict(usage_counts)}).strip())


if __name__ == "__main__":
    main()
