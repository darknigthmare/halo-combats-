#!/usr/bin/env python3
"""Consolidate Halo Combats wave 3 character candidates without editing images.

Default is a read-only planning pass. Run with --apply only once the generation
batch is complete. The image inspection uses Pillow for pixel measurements only;
source PNG bytes are copied verbatim, never resaved or transformed.

Accepted generation journal: a list, or {"results": [...]}. Each record should
contain entity_id, source_path, prompt and status. Failed attempts may instead
contain entity_id, error and status="failed". Alternative explicit source fields
source_file, local_path, image_path, output_path and path are also accepted.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


PROJECT = Path(__file__).resolve().parents[2]
DEFAULT_JOURNAL = PROJECT / "work/wave3/generation_results.json"
DEFAULT_QA = PROJECT / "work/wave3/qa_wave3.json"
DESTINATION = PROJECT / "assets/characters_wave3"
REPORT = PROJECT / "docs/HALO_COMBATS_PERSONNAGES_V3.md"
INVENTORY = PROJECT / "data/characters_visual_inventory.csv"
SUMMARY = PROJECT / "work/wave3/consolidation_summary.json"
COUNTS = PROJECT / "data/delivery_counts.json"
README_V3 = PROJECT / "README_V3.md"
SOURCE_FIELDS = (
    "source_path", "source_file", "local_path", "image_path", "output_path", "path"
)
ALPHA_THRESHOLD = 16


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".wave3.tmp")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def json_text(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def failure_summary(record: dict) -> str:
    error = str(record.get("error", ""))
    if "moderation_blocked" in error:
        return "Génération refusée par le contrôle automatique ; motif précis non fourni."
    if error:
        return "La génération a échoué ; détail technique conservé dans le manifeste."
    return "Échec de génération déclaré dans le journal."


def records_from(value) -> list[dict]:
    if isinstance(value, list):
        records = value
    elif isinstance(value, dict):
        records = next((value[k] for k in ("results", "generations", "entries") if k in value), None)
        if records is None:
            raise ValueError("Le journal doit contenir une liste results, generations ou entries.")
    else:
        raise ValueError("Format du journal non reconnu.")
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        raise ValueError("Chaque entrée du journal doit être un objet JSON.")
    return records


def resolve_source(record: dict, journal: Path) -> Path | None:
    raw = next((record[k] for k in SOURCE_FIELDS if isinstance(record.get(k), str) and record[k]), None)
    if raw is None:
        return None
    source = Path(raw)
    if source.is_absolute():
        return source.resolve()
    for base in (journal.parent, PROJECT, Path.cwd()):
        if (base / source).is_file():
            return (base / source).resolve()
    return (journal.parent / source).resolve()


def inspect_png(path: Path) -> dict:
    """Read pixels and report alpha/edge data; no image manipulation or saving."""
    with Image.open(path) as im:
        if im.format != "PNG":
            raise ValueError(f"Le fichier n'est pas un PNG : {path}")
        im.load()
        width, height = im.size
        has_alpha = "A" in im.getbands()
        alpha = im.getchannel("A") if has_alpha else None
        alpha_range = list(alpha.getextrema()) if alpha is not None else None
        histogram = alpha.histogram() if alpha is not None else None
        pixels = alpha.load() if alpha is not None else None
        nonzero_bbox = list(alpha.getbbox()) if alpha is not None and alpha.getbbox() else ([0, 0, width, height] if alpha is None else None)
        edge_nonzero = (
            {
                "left": sum(pixels[0, y] > 0 for y in range(height)),
                "right": sum(pixels[width - 1, y] > 0 for y in range(height)),
                "top": sum(pixels[x, 0] > 0 for x in range(width)),
                "bottom": sum(pixels[x, height - 1] > 0 for x in range(width)),
            }
            if pixels is not None else {"left": height, "right": height, "top": width, "bottom": width}
        )
        min_x, min_y, max_x, max_y = width, height, -1, -1
        edge_counts = {"left": 0, "right": 0, "top": 0, "bottom": 0}
        edge_near_opaque = {"left": 0, "right": 0, "top": 0, "bottom": 0}
        meaningful_pixels = 0
        if pixels is None:
            min_x, min_y, max_x, max_y = 0, 0, width - 1, height - 1
            meaningful_pixels = width * height
            edge_counts = {"left": height, "right": height, "top": width, "bottom": width}
            edge_near_opaque = dict(edge_counts)
        else:
            for y in range(height):
                for x in range(width):
                    a = pixels[x, y]
                    if a > ALPHA_THRESHOLD:
                        meaningful_pixels += 1
                        min_x, min_y = min(min_x, x), min(min_y, y)
                        max_x, max_y = max(max_x, x), max(max_y, y)
                        if x == 0:
                            edge_counts["left"] += 1
                        if x == width - 1:
                            edge_counts["right"] += 1
                        if y == 0:
                            edge_counts["top"] += 1
                        if y == height - 1:
                            edge_counts["bottom"] += 1
                    if a >= 250:
                        if x == 0:
                            edge_near_opaque["left"] += 1
                        if x == width - 1:
                            edge_near_opaque["right"] += 1
                        if y == 0:
                            edge_near_opaque["top"] += 1
                        if y == height - 1:
                            edge_near_opaque["bottom"] += 1
        bbox = [min_x, min_y, max_x + 1, max_y + 1] if max_x >= 0 else None
        margins = (
            {"left": min_x, "top": min_y, "right": width - max_x - 1, "bottom": height - max_y - 1}
            if bbox else None
        )
        warnings = []
        if not has_alpha:
            warnings.append("Aucun canal alpha : le fond n'est pas détouré dans ce fichier.")
        elif histogram[0] == 0:
            warnings.append("Canal alpha présent, mais aucun pixel entièrement transparent.")
        if not meaningful_pixels:
            warnings.append("Aucun contenu au-dessus du seuil alpha 16.")
        contacted = [edge for edge, count in edge_counts.items() if count]
        if contacted:
            warnings.append("Pixels alpha > 16 au bord : " + ", ".join(contacted) + ". Vérification visuelle nécessaire.")
        elif any(edge_nonzero.values()):
            warnings.append("Quelques pixels de faible alpha (1 à 16) atteignent le bord ; contrôler le bruit de détourage en composition.")
        if margins:
            tight = [edge for edge, gap in margins.items() if gap < max(8, round((width if edge in ("left", "right") else height) * 0.02))]
            if tight:
                warnings.append("Marges inférieures à 2 % du canevas ou à 8 px : " + ", ".join(tight) + ".")
        return {
            "width": width,
            "height": height,
            "mode": im.mode,
            "alpha_range": alpha_range,
            "technical_qa": {
                "inspection": "Pillow read-only; copied PNG bytes remain unchanged",
                "has_alpha": has_alpha,
                "transparent_pixels": histogram[0] if histogram else 0,
                "semitransparent_pixels": sum(histogram[1:255]) if histogram else 0,
                "opaque_pixels": histogram[255] if histogram else width * height,
                "near_opaque_pixels": sum(histogram[250:]) if histogram else width * height,
                "alpha_nonzero_bbox": nonzero_bbox,
                "edge_contact_pixels_alpha_nonzero": edge_nonzero,
                "foreground_alpha_threshold": ALPHA_THRESHOLD,
                "foreground_pixels_above_threshold": meaningful_pixels,
                "foreground_bbox_above_threshold": bbox,
                "canvas_margins_px_above_threshold": margins,
                "edge_contact_pixels_above_threshold": edge_counts,
                "edge_contact_pixels_alpha_at_least_250": edge_near_opaque,
                "warnings": warnings,
                "anatomy_and_canon": "requires_visual_reference_comparison",
            },
        }


def load_visual_qa(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, list):
        return value
    if isinstance(value, dict) and isinstance(value.get("reviews"), list):
        return value["reviews"]
    raise ValueError("qa_wave3.json doit être une liste ou un objet {reviews:[...]}.")


def visual_review(entity_id: str, sha256: str, reviews: list[dict]) -> dict | None:
    matches = [r for r in reviews if r.get("entity_id") == entity_id and r.get("sha256") == sha256]
    return matches[-1] if matches else None


def choose_destination(entity_id: str, sha256: str, active: list[dict], reserved: dict) -> tuple[Path, str, bool]:
    for candidate in active:
        if candidate.get("entity_id") == entity_id and candidate.get("sha256") == sha256:
            path = PROJECT / candidate["path"]
            if not path.is_file() or digest(path) != sha256:
                raise ValueError(f"Le candidat déjà référencé est absent ou a changé : {path}")
            return path, candidate["id"], True
    for number in range(1, 10000):
        asset_id = f"{entity_id}_neutral_right_v{number:02d}"
        path = DESTINATION / f"{asset_id}.png"
        if str(path) in reserved:
            if reserved[str(path)] == sha256:
                return path, asset_id, True
            continue
        matching_id = next((c for c in active if c["id"] == asset_id), None)
        if matching_id and matching_id.get("sha256") != sha256:
            continue
        if path.exists():
            if not path.is_file():
                raise ValueError(f"Collision avec un répertoire : {path}")
            if digest(path) != sha256:
                continue
            return path, asset_id, False
        reserved[str(path)] = sha256
        return path, asset_id, False
    raise ValueError(f"Impossible de choisir une version pour {entity_id}.")



def is_failure(record: dict) -> bool:
    status = str(record.get("status", "")).lower()
    return bool(record.get("error")) or any(
        token in status for token in ("fail", "error", "reject", "block")
    )


def entity_id(record: dict) -> str:
    return str(record.get("entity_id") or record.get("fighter_id") or record.get("id") or "")


def pose_scope(record: dict) -> str:
    if record.get("pose_scope"):
        return str(record["pose_scope"])
    if record.get("attempt_kind") == "neutral_unarmed":
        return "neutral_unarmed_reference"
    return "character_pose_candidate"


def verify_existing_assets(active: list[dict], known_ids: set[str]) -> None:
    """Reject missing or changed prior files before counting them as available."""
    asset_ids = [a["id"] for a in active]
    if len(asset_ids) != len(set(asset_ids)):
        raise ValueError("Le manifeste comporte des IDs de fichier dupliqués.")
    owners = {}
    for asset in active:
        path = (PROJECT / asset["path"]).resolve()
        if not path.is_relative_to(PROJECT) or not path.is_file():
            raise ValueError(f"Candidat antérieur absent ou hors projet : {path}")
        sha = digest(path)
        if asset.get("sha256") and asset["sha256"] != sha:
            raise ValueError(f"Le candidat antérieur a changé : {path}")
        if asset.get("type") == "fighter_pose":
            owner = entity_id(asset)
            if owner not in known_ids:
                raise ValueError(f"Candidat combattant hors roster : {owner}")
            if sha in owners and owners[sha] != owner:
                raise ValueError("Les mêmes octets sont attribués à deux combattants.")
            owners[sha] = owner


def make_summary(fighters: list[dict], active: list[dict], prior_active: list[dict],
                 records: list[dict], failures: list[dict], all_failures: list[dict],
                 plans: list[dict], added: list[dict], duplicates: list[dict],
                 reused_prior: list[dict], stamp: str, journal_sha: str,
                 apply: bool) -> dict:
    candidates = [a for a in active if a.get("type") == "fighter_pose"]
    prior_candidates = [a for a in prior_active if a.get("type") == "fighter_pose"]
    current_wave = [a for a in candidates if a.get("generation_wave") == 3]
    prior_wave = [a for a in candidates if a.get("generation_wave") != 3]
    covered = {entity_id(a) for a in candidates}
    covered_before = {entity_id(a) for a in prior_candidates}
    history_failed = {entity_id(f) for f in all_failures}
    remaining = [f["id"] for f in fighters if f["id"] not in covered]
    requested = {entity_id(r) for r in records}
    return {
        "updated_utc": stamp,
        "generation_wave": 3,
        "journal_sha256": journal_sha,
        "roster_count": len(fighters),
        "roster_unique_ids": len({f["id"] for f in fighters}),
        "missing_before_this_run": [f["id"] for f in fighters if f["id"] not in covered_before],
        "missing_before_wave3": [f["id"] for f in fighters if not any(entity_id(a) == f["id"] for a in prior_wave)],
        "new_candidate_assets_this_run": len(added),
        "new_candidate_entities_this_run": sorted({entity_id(a) for a in added}),
        "fighter_entities_with_candidates": len(covered),
        "fighter_candidate_asset_count": len(candidates),
        "fighter_entities_without_candidates": remaining,
        "wave3_candidate_asset_count": len(current_wave),
        "wave3_candidate_entities": sorted({entity_id(a) for a in current_wave}),
        "wave3_neutral_unarmed_asset_count": sum(a.get("attempt_kind") == "neutral_unarmed" for a in current_wave),
        "generation_attempt_count": len(records),
        "unique_fighters_requested": sorted(requested),
        "successful_generation_attempts": sum(not is_failure(r) for r in records),
        "failed_attempts_in_journal": failures,
        "automatic_rejections_in_journal": sum("moderation_blocked" in str(f.get("error", "")) for f in failures),
        "historical_failed_attempt_count": len(all_failures),
        "historical_failed_fighters": sorted(history_failed),
        "currently_present_despite_historical_failure": sorted(covered & history_failed),
        "failed_fighters_still_without_candidate": sorted(set(remaining) & history_failed),
        "missing_not_attempted_this_wave": [fid for fid in remaining if fid not in requested],
        "duplicate_records_skipped": duplicates,
        "reused_prior_candidate_records": reused_prior,
        "certified_fighter_assets": sum(a.get("fidelity_status") == "certified" for a in candidates),
        "animated_fighter_assets": sum(a.get("animation_status") == "animated" for a in candidates),
        "integrated_fighter_assets": sum(a.get("integration_status") == "integrated" for a in candidates),
        "planned_files": plans,
        "applied": apply,
    }


def delivery_counts(previous: dict, fighters: list[dict], active: list[dict], summary: dict) -> dict:
    counts = dict(previous)
    counts.update({
        "fighters": len(fighters),
        "active_visual_candidates": len(active),
        "active_fighter_pose_candidates": sum(a.get("type") == "fighter_pose" for a in active),
        "fighter_entities_with_visual_candidate": summary["fighter_entities_with_candidates"],
        "fighter_entities_without_visual_candidate": len(summary["fighter_entities_without_candidates"]),
        "active_boss_visual_candidates": sum(a.get("type") == "boss_profile" for a in active),
        "active_stage_visual_candidates": sum(a.get("type") == "stage_master" for a in active),
        "visual_candidates_pre_wave3": sum(a.get("generation_wave") != 3 for a in active),
        "wave3_generated_character_pngs": summary["wave3_candidate_asset_count"],
        "wave3_neutral_unarmed_pngs": summary["wave3_neutral_unarmed_asset_count"],
        "wave3_other_pose_pngs": summary["wave3_candidate_asset_count"] - summary["wave3_neutral_unarmed_asset_count"],
        "wave3_generation_attempts": summary["generation_attempt_count"],
        "wave3_unique_fighters_requested": len(summary["unique_fighters_requested"]),
        "wave3_successful_generation_attempts": summary["successful_generation_attempts"],
        "wave3_unique_fighters_with_new_candidates": len(summary["wave3_candidate_entities"]),
        "wave3_generation_failures": len(summary["failed_attempts_in_journal"]),
        "wave3_automatic_generation_rejections": summary["automatic_rejections_in_journal"],
        "historical_generation_failures_all_waves": summary["historical_failed_attempt_count"],
        "certified_visuals": sum(a.get("fidelity_status") == "certified" for a in active),
        "updated_utc": summary["updated_utc"],
    })
    # This operation creates static poses only; retain the separate animation count.
    counts.setdefault("animation_clips", 0)
    category_total = sum(counts[key] for key in (
        "active_fighter_pose_candidates", "active_boss_visual_candidates", "active_stage_visual_candidates"
    ))
    if category_total != counts["active_visual_candidates"]:
        raise ValueError("Catégorie visuelle non comptabilisée.")
    if counts["fighter_entities_with_visual_candidate"] + counts["fighter_entities_without_visual_candidate"] != len(fighters):
        raise ValueError("Compteurs de couverture incohérents.")
    if counts["wave3_successful_generation_attempts"] + counts["wave3_generation_failures"] != counts["wave3_generation_attempts"]:
        raise ValueError("Compteurs de tentatives incohérents.")
    return counts


def clean_md(value) -> str:
    return str(value).replace("|", "/").replace("\r", " ").replace("\n", " ")


def reports(fighters: list[dict], active: list[dict], records: list[dict],
            history: list[dict], summary: dict, counts: dict) -> tuple[str, str, str]:
    poses = [a for a in active if a.get("type") == "fighter_pose"]
    by_fighter = {f["id"]: [a for a in poses if entity_id(a) == f["id"]] for f in fighters}
    names = {f["id"]: f["name"] for f in fighters}
    missing = summary["fighter_entities_without_candidates"]
    current_failures = summary["failed_attempts_in_journal"]
    covered_names = [f["name"] for f in fighters if by_fighter[f["id"]]]
    new_names = [names[fid] for fid in summary["wave3_candidate_entities"]]
    lines = [
        "# Halo Combats — inventaire des personnages, vague 3", "",
        f"Mise à jour : {summary['updated_utc']}.", "",
        "## Résultat vérifié", "",
        f"Le roster contient **{len(fighters)} combattants distincts**. **{summary['fighter_entities_with_candidates']} disposent d'au moins une pose candidate**, pour {summary['fighter_candidate_asset_count']} fichiers. **{len(missing)} restent sans image candidate.**", "",
        f"La vague 3 a produit {summary['wave3_candidate_asset_count']} PNG distincts pour {len(summary['wave3_candidate_entities'])} personnages. Le journal contient {summary['generation_attempt_count']} tentatives pour {len(summary['unique_fighters_requested'])} personnages distincts : {summary['successful_generation_attempts']} réussites et {len(current_failures)} échecs, dont {summary['automatic_rejections_in_journal']} refus automatiques.", "",
        f"Les {summary['historical_failed_attempt_count']} échecs historiques de toutes les vagues restent enregistrés. Une réussite ultérieure rend le personnage présent ; les refus antérieurs ne le font pas compter comme manquant. Les {len(summary['reused_prior_candidate_records'])} réutilisations éventuelles d'un PNG antérieur et les {len(summary['duplicate_records_skipped'])} doublons internes ne sont pas comptés comme de nouvelles images.", "",
        "Les PNG sont copiés sans recadrage, recompression, redimensionnement ni autre modification. Une image de référence statique ne remplace pas les animations, le moveset ou l'intégration au moteur.", "",
        f"**Poses certifiées : {summary['certified_fighter_assets']} ; animées : {summary['animated_fighter_assets']} ; intégrées : {summary['integrated_fighter_assets']}.** La génération et les contrôles techniques ne certifient pas la fidélité 1:1.", "",
        "## Personnages encore sans image", "",
    ]
    lines.extend(f"- **{names[fid]}** — {fid}." for fid in missing)
    if not missing:
        lines.append("Tous les combattants du roster disposent d'au moins une image candidate.")
    lines += ["", "## Couverture du roster", "",
              "| Personnage | ID | Images | Variante récente | État actuel |",
              "|---|---|---:|---|---|"]
    table = io.StringIO(newline="")
    fields = [
        "entity_id", "name", "source_title", "candidate_count", "latest_asset_id",
        "generation_wave", "attempt_kind", "pose_scope", "relative_path", "sha256",
        "width", "height", "mode", "alpha_min", "alpha_max", "edge_contacts",
        "art_status", "fidelity_status", "animation_status", "integration_status",
        "visual_review_status", "visual_qa", "wave3_attempt_count",
        "historical_failure_count", "currently_present_despite_historical_failure",
    ]
    writer = csv.DictWriter(table, fieldnames=fields)
    writer.writeheader()
    for fighter in fighters:
        fid = fighter["id"]
        assets = by_fighter[fid]
        latest = assets[-1] if assets else {}
        historical = [f for f in history if entity_id(f) == fid]
        last_failure = historical[-1] if historical else None
        notes = latest.get("qa") or (failure_summary(last_failure) if last_failure else "Sans image candidate.")
        if isinstance(notes, list):
            notes = " ; ".join(str(n) for n in notes)
        variant = "Référence neutre sans arme" if latest.get("attempt_kind") == "neutral_unarmed" else ("Pose candidate" if assets else "Aucune image")
        if assets:
            state = "Présent malgré refus antérieur" if historical else "Présent ; validation requise"
        else:
            state = "Manquant ; échec de génération" if historical else "Manquant ; aucune image produite"
        lines.append(f"| {clean_md(fighter['name'])} | {fid} | {len(assets)} | {variant} | {state} |")
        alpha = latest.get("alpha_range") or ["", ""]
        edges = latest.get("technical_qa", {}).get("edge_contact_pixels_above_threshold", {})
        writer.writerow({
            "entity_id": fid, "name": fighter["name"], "source_title": fighter.get("source_title", ""),
            "candidate_count": len(assets), "latest_asset_id": latest.get("id", ""),
            "generation_wave": latest.get("generation_wave", 1 if assets else ""),
            "attempt_kind": latest.get("attempt_kind", "prior_wave" if assets else ""),
            "pose_scope": latest.get("pose_scope", "candidate_pose" if assets else ""),
            "relative_path": latest.get("path", ""), "sha256": latest.get("sha256", ""),
            "width": latest.get("width", ""), "height": latest.get("height", ""), "mode": latest.get("mode", ""),
            "alpha_min": alpha[0], "alpha_max": alpha[1],
            "edge_contacts": "; ".join(f"{k}:{v}" for k, v in edges.items() if v),
            "art_status": "candidate" if assets else ("generation_failed" if historical else "missing"),
            "fidelity_status": latest.get("fidelity_status", "not_certified"),
            "animation_status": latest.get("animation_status", "not_animated"),
            "integration_status": latest.get("integration_status", "not_integrated"),
            "visual_review_status": latest.get("visual_review_status", "prior_qa_to_continue" if assets else "no_image"),
            "visual_qa": notes,
            "wave3_attempt_count": sum(entity_id(r) == fid for r in records),
            "historical_failure_count": len(historical),
            "currently_present_despite_historical_failure": bool(assets and historical),
        })
    lines += ["", "## Observations sur les images disponibles", ""]
    for fighter in fighters:
        assets = by_fighter[fighter["id"]]
        if not assets:
            continue
        latest = assets[-1]
        lines += [f"### {fighter['name']}", "",
                  f"Fichier : {latest['path']}. Définition : {latest.get('width', '?')} × {latest.get('height', '?')} px ; mode {latest.get('mode', '?')}. Statut de fidélité : {latest.get('fidelity_status', 'not_certified')}.", ""]
        notes = latest.get("visual_review", {}).get("notes") or [latest.get("qa", "Inspection visuelle à effectuer.")]
        if isinstance(notes, str):
            notes = [notes]
        lines.extend("- " + str(note) for note in notes)
        lines.append("")
    lines += ["## Contrôles techniques et portée", "",
              "Les dimensions, le canal alpha, les pixels au bord et les SHA-256 sont mesurés en lecture seule. Le seuil alpha >16 permet de repérer un contact de silhouette avec le cadre ; les faibles résidus alpha 1–16 sont enregistrés séparément. Ces mesures ne remplacent pas l'inspection visuelle et ne prouvent pas, à elles seules, une coupe du corps ou un détourage parfait.", "",
              "Les notes visuelles sont liées à l'empreinte du PNG réellement examiné. Une fidélité 1:1 exige ensuite une comparaison aux modèles et références de l'épisode choisi. Les poses neutres sans arme ne sont pas des gardes de combat finales.", ""]
    if current_failures:
        lines += ["## Échecs de la vague 3", ""]
        for failure in current_failures:
            available = bool(by_fighter[entity_id(failure)])
            state = "Une image obtenue par une autre tentative est disponible." if available else "Le personnage reste sans image."
            lines.append(f"- Entrée {failure['journal_record'] + 1}, {entity_id(failure)} : {failure_summary(failure)} {state}")
        lines.append("")
    readme = f"""# Halo Combats — livraison visuelle V3

Mode annexe de combat 2D et Boss Battle pour Darknigthmare. Mise à jour : {summary['updated_utc']}.

## État des personnages

**{counts['fighter_entities_with_visual_candidate']} combattants illustrés sur {counts['fighters']} ; {counts['fighter_entities_without_visual_candidate']} restent sans image candidate.** La vague 3 apporte **{counts['wave3_generated_character_pngs']} nouveaux PNG**, pour {counts['wave3_unique_fighters_with_new_candidates']} personnages.

Le journal V3 comprend {counts['wave3_generation_attempts']} tentatives pour {counts['wave3_unique_fighters_requested']} personnages distincts : {counts['wave3_successful_generation_attempts']} réussites et {counts['wave3_generation_failures']} échecs. Parmi ces derniers, {counts['wave3_automatic_generation_rejections']} sont des refus automatiques dont le motif précis n'a pas été fourni. Les succès après refus sont comptés comme présents. Les compteurs et journaux V1/V2 restent conservés.

| Catégorie | Fichiers disponibles | Portée |
|---|---:|---|
| Poses de combattants | {counts['active_fighter_pose_candidates']} | {counts['fighter_entities_with_visual_candidate']} combattants sur {counts['fighters']} |
| Profils de boss | {counts['active_boss_visual_candidates']} | Candidats visuels de boss |
| Masters de décors | {counts['active_stage_visual_candidates']} | Couches parallaxe séparées à produire |
| Tous candidats visuels | {counts['active_visual_candidates']} | Somme des catégories précédentes |
| Visuels certifiés | {counts['certified_visuals']} | Aucune certification déduite d'une génération |
| Clips d'animation livrés | {counts['animation_clips']} | Les poses statiques ne sont pas des animations |

Personnages disposant d'une image : **{', '.join(covered_names) if covered_names else 'aucun'}**.

Personnages nouvellement illustrés dans la vague 3 : **{', '.join(new_names) if new_names else 'aucun'}**.

Personnages encore sans image : **{', '.join(names[fid] for fid in missing) if missing else 'aucun'}**.

## Ouvrir les livrables

- [Suivi des personnages V3](docs/HALO_COMBATS_PERSONNAGES_V3.md) : couverture complète et observations.
- [Inventaire courant](data/characters_visual_inventory.csv) : les 24 combattants, fichiers, dimensions, alpha et statuts.
{('- [Nouveaux PNG V3](assets/characters_wave3/) : copies byte-identiques des sorties obtenues.' if counts['wave3_generated_character_pngs'] else '- Aucun nouveau PNG obtenu dans cette vague ; les tentatives sont conservées dans le journal V3.')}
- [PNG V2](assets/characters_wave2/) et [candidats V1](assets/candidates/) : fichiers antérieurs conservés.
- [Manifeste courant](data/asset_manifest.json) et [compteurs](data/delivery_counts.json).
- [Bible DOCX V1](docs/HALO_COMBATS_BIBLE_V1.docx) et [bible Markdown V1](docs/HALO_COMBATS_BIBLE_V1.md).
- [Classeur de production V1](docs/HALO_COMBATS_PRODUCTION_V1.xlsx) : état daté ; les registres JSON/CSV portent le suivi visuel courant.
- [Prototype autonome](prototype/halo_combats_prototype.html) et [instructions du prototype](prototype/README.md).

## Fidélité, animations et intégration

Les images sont des poses candidates. Chaque fichier demande encore une comparaison aux modèles de l'épisode, un contrôle de la vue latérale et du détourage, ainsi que les animations. Les variantes neutres sans arme sont des références de personnage ; elles ne constituent pas toutes des gardes de combat prêtes à intégrer.

La bible définit {counts.get('fighters', 24)} combattants, {counts.get('normals', 264)} normales, {counts.get('specials', 96)} spéciaux, {counts.get('supers', 24)} supers, {counts.get('combos', 48)} propositions de combos, {counts.get('finishers', 48)} finishers, {counts.get('story_routes', 24)} routes narratives, {counts.get('boss_encounters', 20)} rencontres de boss et {counts.get('stages', 24)} arènes. Les valeurs d'équilibrage et routes sont des propositions de cette adaptation 2D.

Le plan de {counts.get('planned_animation_clips', 1056)} clips d'animation et de {counts.get('planned_parallax_layers', 144)} couches parallaxe reste un plan de fabrication. Les images fixes ne sont pas comptées comme des clips.

Le prototype conserve ses silhouettes techniques temporaires et ses modes Entraînement, Duel IA et Boss Scarab. Le roster complet, les nouveaux PNG, la campagne, les tournois, les fatalités et le réseau ne sont pas intégrés au moteur par cette livraison visuelle. Les vérifications de logique V1 restent dans [prototype/qa/](prototype/qa/) ; aucun nouveau résultat de gameplay n'est revendiqué.

## Traçabilité

Le [journal V3](work/wave3/generation_results.json), les [observations QA V3](work/wave3/qa_wave3.json) et la [consolidation V3](work/wave3/consolidation_summary.json) séparent les tentatives des images réellement disponibles. Les historiques V1/V2 et leurs observations restent présents.

Les sources figurent dans [fighter_sources.json](data/fighter_sources.json), [world_sources.json](data/world_sources.json), [source_registry.json](docs/source_registry.json), ainsi que dans les prompts et le manifeste. Les références, le cut content et les propositions d'adaptation doivent rester distincts pendant la validation.

Les scripts sources de la V1 reconstruisent un état daté. Ne pas les rejouer sur les registres courants sans préserver les consolidations V2/V3.
"""
    return "\n".join(lines), "\ufeff" + table.getvalue(), readme


def main() -> int:
    import copy
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--journal", type=Path, default=DEFAULT_JOURNAL)
    parser.add_argument("--visual-qa", type=Path, default=DEFAULT_QA)
    parser.add_argument("--apply", action="store_true",
                        help="Copier et mettre à jour uniquement après la fin du lot.")
    args = parser.parse_args()
    journal = args.journal.resolve()
    roster_path = PROJECT / "data/fighters.json"
    manifest_path = PROJECT / "data/asset_manifest.json"
    guarded = [roster_path, manifest_path, journal]
    if COUNTS.is_file():
        guarded.append(COUNTS)
    if args.visual_qa.is_file():
        guarded.append(args.visual_qa)
    guards = {path: digest(path) for path in guarded}
    roster = json.loads(roster_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    journal_value = json.loads(journal.read_text(encoding="utf-8"))
    if isinstance(journal_value, dict) and journal_value.get("wave", 3) != 3:
        raise ValueError("Ce script ne consolide que le journal de la vague 3.")
    fighters = roster["fighters"]
    active = manifest["active_candidates"]
    prior_active = copy.deepcopy(active)
    ids = [f["id"] for f in fighters]
    if len(ids) != len(set(ids)) or not all(ids):
        raise ValueError("IDs du roster absents ou dupliqués.")
    verify_existing_assets(active, set(ids))
    records = records_from(journal_value)
    reviews = load_visual_qa(args.visual_qa)
    journal_rel = journal.relative_to(PROJECT).as_posix() if journal.is_relative_to(PROJECT) else str(journal)
    reserved, seen, content_owners = {}, {}, {}
    plans, failures, duplicates, added, reused_prior = [], [], [], [], []
    for candidate in active:
        if candidate.get("type") == "fighter_pose" and candidate.get("sha256"):
            content_owners[candidate["sha256"]] = entity_id(candidate)
    for index, record in enumerate(records):
        owner = entity_id(record)
        if owner not in ids:
            raise ValueError(f"Entrée {index}: combattant inconnu {owner!r}.")
        if is_failure(record):
            failure = {
                "entity_id": owner, "status": record.get("status", "generation_failed"),
                "error": record.get("error", ""), "prompt": record.get("prompt", ""),
                "generation_wave": 3, "source_journal": journal_rel, "journal_record": index,
                "attempt_kind": record.get("attempt_kind", "reference_retry"),
            }
            failures.append(failure)
            continue
        source = resolve_source(record, journal)
        if source is None or not source.is_file():
            raise ValueError(f"Entrée {index} ({owner}) : PNG absent sans échec déclaré.")
        sha = digest(source)
        if sha in content_owners and content_owners[sha] != owner:
            raise ValueError(f"Un même PNG est affecté à {content_owners[sha]} et {owner}.")
        content_owners[sha] = owner
        identity = (owner, sha)
        if identity in seen:
            duplicates.append({"entity_id": owner, "sha256": sha, "journal_record": index,
                               "same_as_record": seen[identity]})
            continue
        seen[identity] = index
        prior_match = next((a for a in active if entity_id(a) == owner and a.get("sha256") == sha
                            and a.get("generation_wave") != 3), None)
        if prior_match:
            reused_prior.append({"entity_id": owner, "sha256": sha, "journal_record": index,
                                 "asset_id": prior_match["id"], "path": prior_match["path"]})
            continue
        metrics = inspect_png(source)
        destination, asset_id, reused = choose_destination(owner, sha, active, reserved)
        review = visual_review(owner, sha, reviews)
        notes = review.get("notes", []) if review else []
        if isinstance(notes, str):
            notes = [notes]
        candidate = {
            "id": asset_id, "entity_id": owner, "type": "fighter_pose",
            "prompt": record.get("prompt", ""), "output": destination.name,
            "qa": " ".join(str(n) for n in notes) if notes else
                  "Pose candidate générée ; inspection visuelle et comparaison aux références requises.",
            "required_followup": [
                "Comparaison aux références de l'épisode",
                "Validation de la vue latérale et des asymétries",
                "Contrôle du détourage et du cadrage",
                "Animations, collisions et intégration au moteur",
            ],
            "status": "candidate", "fidelity_status": "not_certified",
            "animation_status": "not_animated", "integration_status": "not_integrated",
            "generation_wave": 3, "attempt_kind": record.get("attempt_kind", "reference_retry"),
            "pose_scope": pose_scope(record), "path": destination.relative_to(PROJECT).as_posix(),
            "sha256": sha, "source_path": str(source), "source_journal": journal_rel,
            "journal_record": index,
            "visual_review_status": "reviewed_candidate_with_reservations" if review else "pending_visual_review",
            **metrics,
        }
        if review:
            candidate["visual_review"] = review
            if review.get("required_followup"):
                candidate["required_followup"] = list(dict.fromkeys(
                    list(review["required_followup"]) + candidate["required_followup"]
                ))
        for key in ("reference_urls", "reference_images", "reference_title", "visual_lock",
                    "critical_checks", "generation_attempt", "orientation"):
            if key in record:
                candidate[key] = record[key]
        existing_index = next((i for i, a in enumerate(active) if a["id"] == asset_id), None)
        if existing_index is not None:
            old = active[existing_index]
            if old.get("generation_wave") != 3:
                raise ValueError("Une consolidation V3 ne doit pas réécrire un candidat V1/V2.")
            merged = {**old, **candidate}
            if not record.get("prompt"):
                merged["prompt"] = old.get("prompt", "")
            if not review:
                for key in ("qa", "visual_review", "visual_review_status", "required_followup"):
                    if key in old:
                        merged[key] = old[key]
            active[existing_index] = merged
        else:
            active.append(candidate)
            added.append(candidate)
        plans.append({"entity_id": owner, "source": str(source), "destination": str(destination),
                      "asset_id": asset_id, "sha256": sha, "reused": reused})
    manifest.setdefault("failed_requests", [])
    for failure in failures:
        prior_failure = next((f for f in manifest["failed_requests"]
                              if f.get("generation_wave") == 3 and f.get("source_journal") == journal_rel
                              and f.get("journal_record") == failure["journal_record"]), None)
        if prior_failure and prior_failure != failure:
            raise ValueError("Une tentative déjà consolidée a été modifiée dans le journal.")
        if not prior_failure:
            manifest["failed_requests"].append(failure)
    for fighter in fighters:
        matches = [a for a in active if entity_id(a) == fighter["id"] and a.get("type") == "fighter_pose"]
        if matches:
            fighter.setdefault("status", {})["sprite"] = "candidate_generated"
            fighter["art_status"] = "candidate"
            fighter["visual_assets"] = list(dict.fromkeys(a["id"] for a in matches))
            fighter["fidelity_status"] = "certified" if any(a.get("fidelity_status") == "certified" for a in matches) else "not_certified"
            fighter.pop("visual_generation_failure", None)
        else:
            historical = [f for f in manifest["failed_requests"] if entity_id(f) == fighter["id"]]
            if historical:
                failure = historical[-1]
                fighter.setdefault("status", {})["sprite"] = (
                    "not_generated_generation_rejected" if "moderation_blocked" in str(failure.get("error", ""))
                    else "not_generated_generation_failed"
                )
                fighter["art_status"] = "generation_failed"
                fighter["visual_generation_failure"] = failure_summary(failure)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    manifest.update({
        "updated_utc": stamp,
        "generated_unique_entities": len({entity_id(a) for a in active}),
        "generated_fighter_entities": len({entity_id(a) for a in active if a.get("type") == "fighter_pose"}),
        "certified_assets": sum(a.get("fidelity_status") == "certified" for a in active),
        "animated_assets": sum(a.get("animation_status") == "animated" for a in active),
    })
    summary = make_summary(fighters, active, prior_active, records, failures,
                           manifest["failed_requests"], plans, added, duplicates, reused_prior,
                           stamp, guards[journal], args.apply)
    previous_counts = json.loads(COUNTS.read_text(encoding="utf-8")) if COUNTS.is_file() else {}
    counts = delivery_counts(previous_counts, fighters, active, summary)
    report, inventory, readme = reports(fighters, active, records, manifest["failed_requests"], summary, counts)
    for old in prior_active:
        if old.get("generation_wave") != 3:
            now = next(a for a in active if a["id"] == old["id"])
            if now != old:
                raise ValueError("Un candidat antérieur V1/V2 a été modifié.")
    # A changing journal or another writer must not be silently overwritten.
    for path, sha in guards.items():
        if not path.is_file() or digest(path) != sha:
            raise ValueError(f"Le fichier a changé pendant la préparation : {path}")
    print(json.dumps({k: summary[k] for k in (
        "generation_attempt_count", "wave3_candidate_asset_count", "roster_count",
        "fighter_entities_with_candidates", "fighter_entities_without_candidates", "applied"
    )}, ensure_ascii=False, indent=2))
    if not args.apply:
        print("Lecture seule : aucune copie ni mise à jour effectuée.")
        return 0
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for plan in plans:
        source, destination = Path(plan["source"]), Path(plan["destination"])
        if source == destination:
            continue
        if destination.exists():
            if not destination.is_file() or digest(destination) != plan["sha256"]:
                raise ValueError(f"Collision après planification : {destination}")
            continue
        with source.open("rb") as src, destination.open("xb") as dst:
            shutil.copyfileobj(src, dst, length=1024 * 1024)
            dst.flush()
            os.fsync(dst.fileno())
        if digest(destination) != plan["sha256"]:
            raise ValueError(f"La copie diffère de la source : {destination}")
    backup = PROJECT / "work/wave3/README_V2_before_wave3.md"
    backup.parent.mkdir(parents=True, exist_ok=True)
    if (PROJECT / "README.md").is_file() and not backup.exists():
        with (PROJECT / "README.md").open("rb") as src, backup.open("xb") as dst:
            shutil.copyfileobj(src, dst)
    for path, text in (
        (manifest_path, json_text(manifest)), (roster_path, json_text(roster)),
        (REPORT, report), (INVENTORY, inventory), (SUMMARY, json_text(summary)),
        (COUNTS, json_text(counts)), (README_V3, readme), (PROJECT / "README.md", readme),
    ):
        atomic_write(path, text)
    print("Consolidation V3 appliquée ; PNG copiés à l'identique, historique V1/V2 conservé.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

