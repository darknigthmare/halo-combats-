#!/usr/bin/env python3
"""Consolidate Halo Combats wave 2 character candidates without editing images.

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
DEFAULT_JOURNAL = PROJECT / "work/wave2/generation_results.json"
DEFAULT_QA = PROJECT / "work/wave2/qa_wave2.json"
DESTINATION = PROJECT / "assets/characters_wave2"
REPORT = PROJECT / "docs/HALO_COMBATS_PERSONNAGES_V2.md"
INVENTORY = PROJECT / "data/characters_visual_inventory.csv"
SUMMARY = PROJECT / "work/wave2/consolidation_summary.json"
COUNTS = PROJECT / "data/delivery_counts.json"
README_V2 = PROJECT / "README_V2.md"
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
    temporary = path.with_name(path.name + ".wave2.tmp")
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
    raise ValueError("qa_wave2.json doit être une liste ou un objet {reviews:[...]}.")


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


def french_report(fighters: list[dict], active: list[dict], before_missing: list[str], added: list[dict], failures: list[dict], duplicates: list[dict], stamp: str) -> tuple[str, str, dict]:
    candidates = [c for c in active if c.get("type") == "fighter_pose"]
    by_fighter = {f["id"]: [c for c in candidates if c.get("entity_id") == f["id"]] for f in fighters}
    remaining = [f["id"] for f in fighters if not by_fighter[f["id"]]]
    new_entities = sorted({a["entity_id"] for a in added})
    wave2_assets = [a for a in candidates if a.get("generation_wave") == 2]
    summary = {
        "updated_utc": stamp,
        "roster_count": len(fighters),
        "roster_unique_ids": len({f["id"] for f in fighters}),
        "missing_before_this_run": before_missing,
        "new_candidate_assets_this_run": len(added),
        "new_candidate_entities_this_run": new_entities,
        "fighter_entities_with_candidates": len(fighters) - len(remaining),
        "fighter_candidate_asset_count": len(candidates),
        "wave2_candidate_asset_count": len(wave2_assets),
        "wave2_candidate_entities": sorted({a["entity_id"] for a in wave2_assets}),
        "fighter_entities_without_candidates": remaining,
        "certified_fighter_assets": sum(c.get("fidelity_status") == "certified" for c in candidates),
        "animated_fighter_assets": sum(c.get("animation_status") == "animated" for c in candidates),
        "integrated_fighter_assets": sum(c.get("integration_status") == "integrated" for c in candidates),
        "failed_attempts_in_journal": failures,
        "duplicate_records_skipped": duplicates,
    }
    lines = [
        "# Halo Combats — inventaire des personnages, vague 2",
        "",
        f"Mise à jour : {stamp}.",
        "",
        "## Résultat de l'inventaire",
        "",
        f"Le roster contient **{len(fighters)} combattants distincts**. **{len(fighters) - len(remaining)} personnages disposent d'au moins une pose candidate**, pour {len(candidates)} fichiers candidats référencés. **{len(remaining)} personnages restent sans pose candidate.**",
        "",
        f"Cette consolidation ajoute {len(added)} fichiers candidats pour {len(new_entities)} personnages. Le journal comporte {len(failures)} tentative(s) en échec et {len(duplicates)} entrée(s) identique(s) ignorée(s). Les échecs précédents restent conservés dans le manifeste comme historique.",
        "",
        f"La vague 2 compte au total {len(wave2_assets)} poses candidates pour {len({a['entity_id'] for a in wave2_assets})} personnages.",
        "",
        "Les PNG sont copiés sans modification. La présence d'une pose ne signifie pas qu'un personnage est entièrement produit : les animations, les sprites d'attaque, les collisions, l'intégration et la validation comparative de fidélité restent à réaliser selon les statuts du manifeste.",
        "",
        f"**Fichiers combattants certifiés : {summary['certified_fighter_assets']}. Animés : {summary['animated_fighter_assets']}. Intégrés : {summary['integrated_fighter_assets']}.** Aucune certification de fidélité 1:1 n'est déduite de la seule génération.",
        "",
        "## Personnages encore sans image candidate",
        "",
    ]
    if remaining:
        for f in fighters:
            if f["id"] in remaining:
                lines.append(f"- **{f['name']}** — `{f['id']}`.")
    else:
        lines.append("Aucun personnage du roster de 24 combattants n'est sans pose candidate.")
    lines += ["", "## Couverture du roster", "", "| Personnage | ID | Poses candidates | Variante la plus récente | Contrôle visuel |", "|---|---|---:|---|---|"]
    csv_stream = io.StringIO(newline="")
    fields = ["entity_id", "name", "source_title", "candidate_count", "latest_asset_id", "attempt_kind", "pose_scope", "relative_path", "sha256", "width", "height", "mode", "alpha_min", "alpha_max", "edge_contacts", "art_status", "fidelity_status", "animation_status", "integration_status", "visual_review_status", "visual_qa"]
    writer = csv.DictWriter(csv_stream, fieldnames=fields)
    writer.writeheader()
    for f in fighters:
        assets = by_fighter[f["id"]]
        latest = assets[-1] if assets else {}
        failure = next((entry for entry in reversed(failures) if entry["entity_id"] == f["id"]), None)
        qa_text = latest.get("qa", failure_summary(failure) if failure else "Sans candidat généré.")
        if isinstance(qa_text, list):
            qa_text = " ; ".join(qa_text)
        variant = "Référence neutre sans arme" if latest.get("attempt_kind") == "neutral_unarmed" else ("Pose candidate" if assets else "Aucune image")
        review_state = "Inspection V2 avec réserves" if latest.get("visual_review") else ("QA antérieure à poursuivre" if assets else "Génération non obtenue")
        lines.append(f"| {f['name']} | `{f['id']}` | {len(assets)} | {variant} | {review_state} |")
        alpha = latest.get("alpha_range") or ["", ""]
        edge = latest.get("technical_qa", {}).get("edge_contact_pixels_above_threshold", {})
        writer.writerow({
            "entity_id": f["id"], "name": f["name"], "source_title": f.get("source_title", ""),
            "candidate_count": len(assets), "latest_asset_id": latest.get("id", ""),
            "attempt_kind": latest.get("attempt_kind", "pre_wave2" if assets else ""), "pose_scope": latest.get("pose_scope", "candidate_pose" if assets else ""),
            "relative_path": latest.get("path", ""), "sha256": latest.get("sha256", ""),
            "width": latest.get("width", ""), "height": latest.get("height", ""), "mode": latest.get("mode", ""),
            "alpha_min": alpha[0], "alpha_max": alpha[1],
            "edge_contacts": "; ".join(f"{k}:{v}" for k, v in edge.items() if v),
            "art_status": latest.get("status", "missing"), "fidelity_status": latest.get("fidelity_status", "not_certified"),
            "animation_status": latest.get("animation_status", "not_animated"), "integration_status": latest.get("integration_status", "not_integrated"),
            "visual_review_status": latest.get("visual_review_status", "not_reviewed_in_wave2"), "visual_qa": qa_text,
        })
    lines += ["", "## Observations sur les personnages illustrés", ""]
    for f in fighters:
        if not by_fighter[f["id"]]:
            continue
        latest = by_fighter[f["id"]][-1]
        lines += [f"### {f['name']}", "", f"Fichier : `{latest['path']}`. Dimensions : {latest.get('width', '?')} × {latest.get('height', '?')} px ; mode {latest.get('mode', '?')}. Statut : candidat, fidélité non certifiée.", ""]
        notes = latest.get("visual_review", {}).get("notes") or [latest.get("qa", "Contrôle visuel à effectuer.")]
        if isinstance(notes, str):
            notes = [notes]
        lines += ["- " + str(note) for note in notes]
        lines.append("")
    lines += ["## Lecture des contrôles techniques", "", "Les dimensions, le mode couleur, le canal alpha, la présence de pixels au bord et les sommes SHA-256 sont mesurés en lecture seule. Le seuil alpha de 16 repère un contact éventuel avec le cadre ; ce signal doit être examiné visuellement, car il ne prouve à lui seul ni une découpe ni un défaut anatomique. Les contacts de faible alpha 1 à 16 sont enregistrés séparément, même lorsque la silhouette ne touche pas le cadre.", "", "Les observations visuelles rattachées à une empreinte SHA-256 décrivent le fichier réellement examiné. Les fichiers sans observation restent à examiner. Chaque personnage demande ensuite une comparaison avec des références de son épisode, une vérification du profil de combat, un détourage de production et un jeu d'animations complet.", ""]
    if failures:
        lines += ["## Tentatives en échec dans le journal de cette vague", ""]
        for failure in failures:
            recovered = " Une autre tentative a toutefois produit une pose candidate disponible dans cet inventaire." if by_fighter.get(failure["entity_id"]) else " Le personnage reste sans pose candidate."
            lines.append(f"- `{failure['entity_id']}` — {failure_summary(failure)}{recovered}")
        lines.append("")
    return "\n".join(lines), "\ufeff" + csv_stream.getvalue(), summary


def delivery_counts(previous: dict, fighters: list[dict], active: list[dict], summary: dict, records: list[dict]) -> dict:
    counts = dict(previous)
    counts.update({
        "fighters": len(fighters),
        "active_visual_candidates": len(active),
        "active_fighter_pose_candidates": sum(a.get("type") == "fighter_pose" for a in active),
        "fighter_entities_with_visual_candidate": summary["fighter_entities_with_candidates"],
        "fighter_entities_without_visual_candidate": len(summary["fighter_entities_without_candidates"]),
        "active_boss_visual_candidates": sum(a.get("type") == "boss_profile" for a in active),
        "active_stage_visual_candidates": sum(a.get("type") == "stage_master" for a in active),
        "visual_candidates_pre_wave2": sum(a.get("generation_wave") != 2 for a in active),
        "wave2_generated_character_pngs": summary["wave2_candidate_asset_count"],
        "wave2_neutral_unarmed_pngs": sum(a.get("generation_wave") == 2 and a.get("attempt_kind") == "neutral_unarmed" for a in active),
        "wave2_initial_pose_pngs": sum(a.get("generation_wave") == 2 and a.get("attempt_kind", "original") != "neutral_unarmed" for a in active),
        "wave2_generation_attempts": len(records),
        "wave2_unique_fighters_requested": len({r.get("entity_id") or r.get("fighter_id") or r.get("id") for r in records}),
        "wave2_successful_generation_attempts": summary["successful_generation_attempts"],
        "wave2_unique_fighters_with_new_candidates": len(summary["wave2_candidate_entities"]),
        "wave2_generation_failures": len(summary["failed_attempts_in_journal"]),
        "wave2_automatic_generation_rejections": sum("moderation_blocked" in str(f.get("error", "")) for f in summary["failed_attempts_in_journal"]),
        "certified_visuals": sum(a.get("fidelity_status") == "certified" for a in active),
        "animation_clips": sum(a.get("animation_status") == "animated" for a in active),
        "updated_utc": summary["updated_utc"],
    })
    category_total = counts["active_fighter_pose_candidates"] + counts["active_boss_visual_candidates"] + counts["active_stage_visual_candidates"]
    if category_total != counts["active_visual_candidates"]:
        raise ValueError("Une catégorie de candidat n'est pas comptabilisée dans delivery_counts.")
    if counts["fighter_entities_with_visual_candidate"] + counts["fighter_entities_without_visual_candidate"] != counts["fighters"]:
        raise ValueError("Les compteurs de couverture du roster ne correspondent pas au nombre de combattants.")
    if counts["wave2_successful_generation_attempts"] + counts["wave2_generation_failures"] != counts["wave2_generation_attempts"]:
        raise ValueError("Les compteurs de tentatives réussies et échouées ne couvrent pas le journal.")
    return counts


def readme_v2(fighters: list[dict], active: list[dict], counts: dict, summary: dict) -> str:
    names = {f["id"]: f["name"] for f in fighters}
    covered = [names[entity] for entity in names if any(a.get("entity_id") == entity and a.get("type") == "fighter_pose" for a in active)]
    new_names = [names[entity] for entity in summary["wave2_candidate_entities"]]
    return f"""# Halo Combats — livraison visuelle V2

Mode annexe de combat 2D et Boss Battle pour Darknigthmare. Mise à jour : {summary['updated_utc']}.

## Résultat réel de la vague de personnages

Le roster défini contient **{counts['fighters']} combattants**. **{counts['fighter_entities_with_visual_candidate']} disposent d'au moins une pose candidate** ; **{counts['fighter_entities_without_visual_candidate']} restent sans pose candidate**. Cette vague a produit **{counts['wave2_generated_character_pngs']} nouveaux PNG de personnages**.

Le dossier contient **{counts['active_visual_candidates']} candidats visuels au total**, en réunissant les {counts['visual_candidates_pre_wave2']} fichiers antérieurs et les nouveaux fichiers. Ce total comprend des personnages, un boss et des décors ; il n'est pas le nombre de combattants générés.

| Catégorie | Fichiers candidats livrés | Portée |
|---|---:|---|
| Poses de combattants | {counts['active_fighter_pose_candidates']} | {counts['fighter_entities_with_visual_candidate']} combattants couverts sur {counts['fighters']} |
| Boss | {counts['active_boss_visual_candidates']} | Profil candidat du Scarab Halo 3 |
| Décors | {counts['active_stage_visual_candidates']} | Masters Valhalla et New Mombasa, sans couches parallaxe séparées |
| Tous candidats | {counts['active_visual_candidates']} | Somme des trois catégories précédentes |
| Visuels certifiés | {counts['certified_visuals']} | Aucune certification 1:1 déduite d'une génération |
| Clips d'animation livrés | {counts['animation_clips']} | Les poses candidates ne sont pas des animations |

Personnages disposant d'une pose candidate : **{', '.join(covered) if covered else 'aucun'}**.

Personnages nouvellement illustrés dans la vague 2 : **{', '.join(new_names) if new_names else 'aucun'}**.

Parmi les nouveaux fichiers, **{counts['wave2_neutral_unarmed_pngs']} sont des références neutres sans arme** et {counts['wave2_initial_pose_pngs']} proviennent des demandes initiales de pose. Une référence calme sans arme ne constitue pas une garde de combat armée ni un ensemble d'animations. La variante de chaque fichier figure dans le manifeste et le CSV.

Le journal de cette vague contient **{counts['wave2_generation_attempts']} tentatives pour {counts['wave2_unique_fighters_requested']} personnages distincts** : {counts['wave2_successful_generation_attempts']} tentatives réussies et {counts['wave2_generation_failures']} échecs. Un personnage peut avoir plusieurs tentatives. Parmi les échecs, {counts['wave2_automatic_generation_rejections']} ont été refusés par le contrôle automatique de génération ; leur motif précis n'a pas été fourni. Un échec antérieur ne laisse pas un personnage classé absent lorsqu'une tentative ultérieure a produit une image. Aucun fichier correspondant à une tentative échouée n'est compté comme livré ; les détails techniques sont conservés dans le manifeste et le journal.

## Ouvrir les livrables

- `docs/HALO_COMBATS_PERSONNAGES_V2.md` : couverture complète du roster, personnages encore manquants et réserves de contrôle.
- `data/characters_visual_inventory.csv` : inventaire des 24 combattants, chemins des images, dimensions, alpha, empreintes et statuts.
- `assets/characters_wave2/` : nouveaux PNG, copiés à l'identique sous des noms versionnés.
- `assets/candidates/` : quatre PNG candidats antérieurs, conservés.
- `data/asset_manifest.json` : manifeste courant de tous les candidats, avec prompts, références, mesures techniques et observations.
- `data/delivery_counts.json` : compteurs séparant le roster défini, les PNG livrés, leur catégorie et la couverture visuelle.
- `docs/HALO_COMBATS_BIBLE_V1.docx` et `.md` : bible de conception, version 1.
- `docs/HALO_COMBATS_PRODUCTION_V1.xlsx` : classeur de production, version 1 ; les registres JSON et CSV V2 portent l'état visuel courant.
- `prototype/halo_combats_prototype.html` : prototype autonome sans serveur ni connexion.

## Ce qui est défini et ce qui reste à produire

La bible décrit 24 combattants, 264 normales, 96 spéciaux, 24 supers, 48 propositions de combos, 24 routes avec introduction, rival et ending, 48 finishers, 20 rencontres de boss et 24 arènes à six couches. Les valeurs d'équilibrage et les routes narratives sont des propositions de cette adaptation 2D.

Le plan de 44 clips par combattant, soit 1 056 clips, demeure un plan de fabrication. Les 144 couches parallaxe prévues sont à produire. Les deux images d'arènes restent des masters de décor.

Les PNG de personnages sont des **poses candidates**. Ils nécessitent une comparaison aux modèles de l'épisode choisi, un contrôle du profil de combat et du détourage, les animations et l'intégration. Les mesures alpha et les empreintes ne valident ni l'anatomie ni la fidélité canonique. Les observations de `work/wave2/qa_wave2.json` sont rattachées aux empreintes des images effectivement examinées.

## Jouer au prototype

Choisir Entraînement, Duel IA ou Boss Scarab. Déplacement avec les flèches ou Q D, saut avec Espace, dash avec Maj, léger J, lourd K, tir L, grenade U, impulsion I, garde O et pause P. Contre le Scarab, casser les deux jambes vulnérables, rejoindre la balise centrale et utiliser E pour monter, puis attaquer le noyau sur le pont. Les boutons tactiles sont présents.

Le prototype utilise des silhouettes techniques temporaires. Il contient un personnage contrôlable, un adversaire IA et un boss. Le roster complet et les nouveaux PNG ne sont pas intégrés au moteur. La campagne, les tournois, les fatalités et le réseau demeurent des spécifications de la bible.

Les contrôles V1 de logique sont conservés dans `prototype/qa/`. Aucun nouveau test de gameplay n'est revendiqué par cette livraison visuelle.

## Références et traçabilité

`data/fighter_sources.json`, `data/world_sources.json` et `docs/source_registry.json` conservent les références et leur portée. Les références ajoutées pour cette vague figurent dans le manifeste et les fichiers de travail. Les versions d'armure, les épisodes, les concepts abandonnés et les propositions originales doivent rester distincts pendant la validation.

`work/wave2/generation_results.json` conserve les tentatives, `work/wave2/qa_wave2.json` les observations, et `work/wave2/consolidation_summary.json` la synthèse de consolidation. Les erreurs de génération restent visibles et ne sont pas transformées en livraisons.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--journal", type=Path, default=DEFAULT_JOURNAL)
    parser.add_argument("--visual-qa", type=Path, default=DEFAULT_QA)
    parser.add_argument("--apply", action="store_true", help="Copy candidates and update files; use only after the generation batch is complete.")
    args = parser.parse_args()
    journal = args.journal.resolve()
    roster_path, manifest_path = PROJECT / "data/fighters.json", PROJECT / "data/asset_manifest.json"
    roster = json.loads(roster_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    fighters, active = roster["fighters"], manifest["active_candidates"]
    ids = [f["id"] for f in fighters]
    if len(ids) != len(set(ids)):
        raise ValueError("Le roster contient des IDs dupliqués.")
    asset_ids = [a["id"] for a in active]
    if len(asset_ids) != len(set(asset_ids)):
        raise ValueError("Le manifeste contient des IDs de fichier dupliqués.")
    records = records_from(json.loads(journal.read_text(encoding="utf-8")))
    reviews = load_visual_qa(args.visual_qa)
    before_missing = [f["id"] for f in fighters if not any(c.get("entity_id") == f["id"] and c.get("type") == "fighter_pose" for c in active)]
    reserved, seen, content_owners = {}, {}, {}
    plans, failures, duplicates, added = [], [], [], []
    successful_attempts = 0
    for candidate in active:
        if candidate.get("sha256") and candidate.get("type") == "fighter_pose":
            content_owners.setdefault(candidate["sha256"], candidate["entity_id"])
    for index, record in enumerate(records):
        entity_id = record.get("entity_id") or record.get("fighter_id") or record.get("id")
        if entity_id not in ids:
            raise ValueError(f"Entrée {index}: combattant inconnu {entity_id!r}.")
        source = resolve_source(record, journal)
        if source is None:
            if record.get("error") or str(record.get("status", "")).lower() in {"failed", "error", "rejected", "blocked", "failure"}:
                failures.append({"entity_id": entity_id, "status": record.get("status", "failed"), "error": record.get("error", ""), "generation_wave": 2, "journal_record": index, "attempt_kind": record.get("attempt_kind", "original")})
                continue
            raise ValueError(f"Entrée {index} ({entity_id}): chemin PNG absent sans échec déclaré.")
        if not source.is_file():
            raise ValueError(f"Entrée {index} ({entity_id}): PNG absent : {source}")
        successful_attempts += 1
        sha256 = digest(source)
        if sha256 in content_owners and content_owners[sha256] != entity_id:
            raise ValueError(f"Un même PNG est affecté à deux combattants : {content_owners[sha256]} et {entity_id}.")
        content_owners[sha256] = entity_id
        identity = (entity_id, sha256)
        if identity in seen:
            duplicates.append({"entity_id": entity_id, "sha256": sha256, "journal_record": index, "same_as_record": seen[identity]})
            continue
        seen[identity] = index
        metrics = inspect_png(source)
        destination, asset_id, reused = choose_destination(entity_id, sha256, active, reserved)
        review = visual_review(entity_id, sha256, reviews)
        notes = review.get("notes", []) if review else []
        if isinstance(notes, str):
            notes = [notes]
        qa = " ".join(notes) if notes else "Pose candidate générée. Contrôle de l'anatomie, des armes, du profil et de la fidélité à la version de référence encore requis."
        candidate = {
            "id": asset_id, "entity_id": entity_id, "type": "fighter_pose",
            "prompt": record.get("prompt", ""), "output": destination.name,
            "qa": qa,
            "required_followup": ["Comparaison aux références de l'épisode", "Validation du profil latéral et de l'anatomie", "Vérification du détourage et des armes", "Animations et sprites de combat", "Collisions et intégration au moteur"],
            "status": "candidate", "fidelity_status": "not_certified", "animation_status": "not_animated", "integration_status": "not_integrated",
            "generation_wave": 2,
            "attempt_kind": record.get("attempt_kind", "original"),
            "pose_scope": "neutral_unarmed_reference" if record.get("attempt_kind") == "neutral_unarmed" else "initial_character_pose",
            "path": destination.relative_to(PROJECT).as_posix(), "sha256": sha256,
            "source_path": str(source), "source_journal": journal.relative_to(PROJECT).as_posix() if journal.is_relative_to(PROJECT) else str(journal),
            "journal_record": index,
            "visual_review_status": "reviewed_candidate_with_reservations" if review else "pending_visual_review",
            **metrics,
        }
        if review:
            candidate["visual_review"] = review
            if review.get("required_followup"):
                candidate["required_followup"] = list(dict.fromkeys(review["required_followup"] + candidate["required_followup"]))
        for key in ("reference_urls", "reference_images", "reference_title", "visual_lock", "critical_checks", "generation_attempt", "attempt_kind", "orientation"):
            if key in record:
                candidate[key] = record[key]
        existing_index = next((i for i, a in enumerate(active) if a["id"] == asset_id), None)
        if existing_index is not None:
            old = active[existing_index]
            # Preserve existing QA and provenance unless this exact PNG was reviewed.
            merged = {**old, **candidate}
            if not record.get("prompt") and old.get("prompt"):
                merged["prompt"] = old["prompt"]
            if not review:
                for key in ("qa", "visual_review", "visual_review_status", "required_followup"):
                    if key in old:
                        merged[key] = old[key]
            active[existing_index] = merged
        else:
            active.append(candidate)
            added.append(candidate)
        plans.append({"entity_id": entity_id, "source": str(source), "destination": str(destination), "asset_id": asset_id, "sha256": sha256, "reused": reused})
    for fighter in fighters:
        matches = [a for a in active if a.get("entity_id") == fighter["id"] and a.get("type") == "fighter_pose"]
        if matches:
            fighter.setdefault("status", {})["sprite"] = "candidate_generated"
            fighter["art_status"] = "candidate"
            fighter["visual_assets"] = list(dict.fromkeys(a["id"] for a in matches))
            fighter["fidelity_status"] = "not_certified"
            fighter.pop("visual_generation_failure", None)
        else:
            failed = next((entry for entry in reversed(failures) if entry["entity_id"] == fighter["id"]), None)
            if failed:
                fighter.setdefault("status", {})["sprite"] = "not_generated_generation_rejected" if "moderation_blocked" in str(failed.get("error", "")) else "not_generated_generation_failed"
                fighter["art_status"] = "generation_failed"
                fighter["visual_generation_failure"] = failure_summary(failed)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    manifest["updated_utc"] = stamp
    manifest["generated_unique_entities"] = len({a["entity_id"] for a in active})
    manifest["generated_fighter_entities"] = len({a["entity_id"] for a in active if a.get("type") == "fighter_pose"})
    manifest["certified_assets"] = sum(a.get("fidelity_status") == "certified" for a in active)
    manifest["animated_assets"] = sum(a.get("animation_status") == "animated" for a in active)
    manifest.setdefault("failed_requests", [])
    for failure in failures:
        if failure not in manifest["failed_requests"]:
            manifest["failed_requests"].append(failure)
    report, inventory, summary = french_report(fighters, active, before_missing, added, failures, duplicates, stamp)
    summary["generation_attempt_count"] = len(records)
    summary["unique_fighters_requested"] = sorted({r.get("entity_id") or r.get("fighter_id") or r.get("id") for r in records})
    summary["successful_generation_attempts"] = successful_attempts
    summary["failed_fighters_still_without_candidate"] = sorted({failure["entity_id"] for failure in failures} & set(summary["fighter_entities_without_candidates"]))
    report = report.replace(
        "## Personnages encore sans image candidate",
        f"Le journal comporte **{len(records)} tentatives pour {len(summary['unique_fighters_requested'])} personnages distincts** : {successful_attempts} tentatives réussies et {len(failures)} échecs. Un même personnage peut avoir plusieurs tentatives ; seul l'inventaire des fichiers réellement produits détermine sa couverture visuelle.\n\n## Personnages encore sans image candidate",
    )
    previous_counts = json.loads(COUNTS.read_text(encoding="utf-8")) if COUNTS.exists() else {}
    counts = delivery_counts(previous_counts, fighters, active, summary, records)
    readme = readme_v2(fighters, active, counts, summary)
    summary["planned_files"] = plans
    summary["applied"] = args.apply
    print(json.dumps({k: summary[k] for k in ("roster_count", "missing_before_this_run", "new_candidate_assets_this_run", "fighter_entities_with_candidates", "fighter_entities_without_candidates", "applied")}, ensure_ascii=False, indent=2))
    if not args.apply:
        print("Lecture seule : aucune copie ni mise à jour effectuée. Ajouter --apply après la fin du lot.")
        return 0
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for plan in plans:
        source, destination = Path(plan["source"]), Path(plan["destination"])
        if source == destination:
            continue
        if destination.exists():
            if digest(destination) != plan["sha256"]:
                raise ValueError(f"Le fichier de destination a changé depuis la planification : {destination}")
            continue
        with source.open("rb") as src, destination.open("xb") as dst:
            shutil.copyfileobj(src, dst, length=1024 * 1024)
            dst.flush()
            os.fsync(dst.fileno())
        if digest(destination) != plan["sha256"]:
            raise ValueError(f"La copie n'a pas la même empreinte SHA-256 : {destination}")
    atomic_write(manifest_path, json_text(manifest))
    atomic_write(roster_path, json_text(roster))
    atomic_write(REPORT, report)
    atomic_write(INVENTORY, inventory)
    atomic_write(SUMMARY, json_text(summary))
    atomic_write(COUNTS, json_text(counts))
    readme_archive = PROJECT / "work/wave2/README_V1_before_wave2.md"
    if (PROJECT / "README.md").is_file() and not readme_archive.exists():
        with (PROJECT / "README.md").open("rb") as src, readme_archive.open("xb") as dst:
            shutil.copyfileobj(src, dst)
    atomic_write(README_V2, readme)
    atomic_write(PROJECT / "README.md", readme)
    print(f"Mis à jour : {manifest_path.relative_to(PROJECT)}, {roster_path.relative_to(PROJECT)}, {REPORT.relative_to(PROJECT)}, {INVENTORY.relative_to(PROJECT)}, {COUNTS.relative_to(PROJECT)}, README.md et README_V2.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
