#!/usr/bin/env python3
"""Consolidate V5 static guard and Boss Battle profile candidates.

Default: a read-only plan. --apply requires a stable root-owned journal and a
SHA-bound visual review for every new PNG. Images are read for QA and copied
byte for byte; they are never transformed or resaved. V1–V4 candidate metadata,
image bytes, failure history and counters are immutable.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import importlib.util
import io
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT = Path(__file__).resolve().parents[2]
WORK = PROJECT / "work/wave5"
JOURNAL = WORK / "generation_results.json"
QA = WORK / "qa_wave5.json"
BASELINE = WORK / "baseline_v4.json"
SUMMARY = WORK / "consolidation_summary.json"
REPORT = PROJECT / "docs/HALO_COMBATS_GARDES_BOSS_V5.md"
CHARACTER_CSV = PROJECT / "data/characters_visual_inventory.csv"
BOSS_CSV = PROJECT / "data/bosses_visual_inventory.csv"
MANIFEST = PROJECT / "data/asset_manifest.json"
FIGHTERS = PROJECT / "data/fighters.json"
BOSSES = PROJECT / "data/bosses.json"
COUNTS = PROJECT / "data/delivery_counts.json"

_spec = importlib.util.spec_from_file_location("halo_wave4_read_helpers", PROJECT / "work/wave4/consolidate_wave4.py")
v4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v4)
digest = v4.digest
json_text = v4.json_text
is_failure = v4.is_failure
entity_id = v4.entity_id
failure_summary = v4.failure_summary


def canonical_sha(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def write_atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".wave5.tmp")
    with tmp.open("w", encoding="utf-8", newline="") as stream:
        stream.write(text)
        stream.flush()
        os.fsync(stream.fileno())
    tmp.replace(path)


def display_date(stamp):
    value = datetime.fromisoformat(stamp).astimezone(ZoneInfo("Europe/Paris"))
    months = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre")
    offset = value.strftime("%z")
    return f"{value.day} {months[value.month-1]} {value.year} à {value:%H:%M} (heure de Paris, UTC{offset[:3]}:{offset[3:]})"


def safe_md(value):
    return str(value).replace("|", "/").replace("\r", " ").replace("\n", " ")


def boss_scope(asset):
    if not asset:
        return "Sans image"
    if asset.get("complete_silhouette", True):
        return "Silhouette complète candidate"
    region = asset.get("depicted_region") or asset.get("representation_scope") or "présence / élément partiel"
    return "Partiel : " + str(region)


def entity_kind(record, fighter_ids, boss_ids):
    owner = entity_id(record)
    kind = record.get("entity_type") or ("fighter" if owner in fighter_ids else "boss" if owner in boss_ids else "")
    if (kind == "fighter" and owner not in fighter_ids) or (kind == "boss" and owner not in boss_ids) or kind not in {"fighter", "boss"}:
        raise ValueError(f"Entité ou type hors registre : {owner} / {kind}")
    expected = "guard_static" if kind == "fighter" else "boss_profile"
    if record.get("pose_scope", expected) != expected:
        raise ValueError(f"Portée V5 inattendue : {owner} / {record.get('pose_scope')}")
    return kind, expected


def verify_baseline(manifest, baseline, counts):
    current = {a["id"]: a for a in manifest["active_candidates"]}
    if len(current) != len(manifest["active_candidates"]):
        raise ValueError("IDs de candidats dupliqués dans le manifeste.")
    for old in baseline["candidates"]:
        a = current.get(old["id"])
        if a is None or canonical_sha(a) != old["metadata_sha256"]:
            raise ValueError(f"Métadonnées V1–V4 modifiées : {old['id']}")
        if digest(PROJECT / a["path"]) != old["sha256"]:
            raise ValueError(f"PNG V1–V4 modifié : {old['path']}")
    n = baseline["historical_failures"]
    if canonical_sha(manifest["failed_requests"][:n]) != baseline["prior_failed_requests_sha256"]:
        raise ValueError("L'historique des échecs V1–V4 a changé.")
    for key, value in baseline["prior_counts"].items():
        if key.startswith(("wave2_", "wave3_", "wave4_")) and counts.get(key) != value:
            raise ValueError(f"Compteur historique modifié : {key}")


def destination_for(owner, kind, sha, active, reserved):
    scope = "guard_static" if kind == "fighter" else "boss_profile"
    for a in active:
        if entity_id(a) == owner and a.get("sha256") == sha and a.get("pose_scope") == scope:
            return PROJECT / a["path"], a["id"]
    folder = PROJECT / ("assets/characters_wave5" if kind == "fighter" else "assets/bosses_wave5")
    stem = f"{owner}_guard_right" if kind == "fighter" else f"{owner}_profile"
    for version in range(1, 10000):
        asset_id = f"{stem}_v{version:02d}"
        path = folder / f"{asset_id}.png"
        if asset_id in reserved:
            if reserved[asset_id] == sha:
                return path, asset_id
            continue
        old = next((a for a in active if a["id"] == asset_id), None)
        if old and old.get("sha256") != sha:
            continue
        if path.exists() and (not path.is_file() or digest(path) != sha):
            continue
        reserved[asset_id] = sha
        return path, asset_id
    raise ValueError(f"Versions épuisées pour {owner}.")


def preferred(assets, previous_id=None):
    marked = [a for a in assets if a.get("visual_review", {}).get("preferred_for_scope")]
    if len(marked) > 1:
        raise ValueError("Plusieurs variantes préférées pour la même entité et portée.")
    if marked:
        return marked[0]
    previous = next((a for a in assets if a["id"] == previous_id), None)
    if previous:
        return previous
    usable = [a for a in assets if a.get("visual_review_status") != "reviewed_candidate_requires_correction"]
    return (usable or assets)[-1] if assets else None


def make_csv(rows, fields):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return "\ufeff" + out.getvalue()


def make_outputs(fighters, bosses, active, records, failures, summary, counts, old_csv_rows):
    fassets = {f["id"]: [a for a in active if a["type"] == "fighter_pose" and entity_id(a) == f["id"]] for f in fighters}
    bassets = {b["id"]: [a for a in active if a["type"] == "boss_profile" and entity_id(a) == b["id"]] for b in bosses}
    old_rows = {r["entity_id"]: r for r in old_csv_rows}
    csv_rows = []
    for f in fighters:
        owner = f["id"]
        all_poses = fassets[owner]
        guards = [a for a in all_poses if a.get("pose_scope") == "guard_static"]
        refs = [a for a in all_poses if a.get("pose_scope") != "guard_static"]
        guard = preferred(guards, f.get("preferred_guard_asset"))
        ref = next((a for a in refs if a["id"] == f.get("preferred_visual_asset")), refs[-1] if refs else {})
        row = dict(old_rows.get(owner, {}))
        row.update({
            "entity_id": owner, "name": f["name"], "source_title": f.get("source_title", ""),
            "candidate_count": len(all_poses), "latest_asset_id": all_poses[-1]["id"] if all_poses else "",
            "preferred_asset_id": ref.get("id", ""), "relative_path": ref.get("path", ""),
            "reference_pose_candidate_count": len(refs), "guard_candidate_count": len(guards),
            "preferred_guard_asset_id": guard["id"] if guard else "",
            "guard_relative_path": guard["path"] if guard else "",
            "guard_sha256": guard["sha256"] if guard else "",
            "guard_equipment_state": guard.get("equipment_state", "") if guard else "",
            "guard_facing": guard.get("facing", guard.get("orientation", "right")) if guard else "",
            "guard_visual_review_status": guard.get("visual_review_status", "") if guard else "no_guard_image",
            "guard_visual_qa": guard.get("qa", "") if guard else "Aucune garde statique produite.",
            "wave5_attempt_count": sum(entity_id(r) == owner for r in records),
            "historical_failure_count": sum(entity_id(x) == owner for x in failures),
            "currently_present_despite_historical_failure": bool(all_poses and any(entity_id(x) == owner for x in failures)),
        })
        csv_rows.append(row)
    fields = list(old_csv_rows[0]) if old_csv_rows else ["entity_id", "name"]
    for row in csv_rows:
        fields.extend(k for k in row if k not in fields)
    fighter_csv = make_csv(csv_rows, fields)
    boss_rows = []
    for b in bosses:
        profile = preferred(bassets[b["id"]], b.get("preferred_visual_asset"))
        boss_rows.append({
            "entity_id": b["id"], "name": b["name"], "origin": b.get("origin", ""),
            "mode": b.get("mode", ""), "scale_category": b.get("scale_category", ""),
            "candidate_count": len(bassets[b["id"]]), "preferred_asset_id": profile["id"] if profile else "",
            "relative_path": profile["path"] if profile else "", "sha256": profile["sha256"] if profile else "",
            "width": profile.get("width", "") if profile else "", "height": profile.get("height", "") if profile else "",
            "art_status": "candidate" if profile else "not_generated", "fidelity_status": "not_certified",
            "animation_status": "not_animated", "integration_status": "not_integrated",
            "visual_review_status": profile.get("visual_review_status", "prior_qa_to_continue") if profile else "no_image",
            "visual_qa": profile.get("qa", "") if profile else "Profil manquant.",
            "wave5_attempt_count": sum(entity_id(r) == b["id"] for r in records),
            "representation_scope": profile.get("representation_scope", "complete_profile") if profile else "",
            "complete_silhouette": profile.get("complete_silhouette", True) if profile else False,
            "depicted_region": profile.get("depicted_region", "") if profile else "",
            "facing": profile.get("facing", profile.get("orientation", "")) if profile else "",
            "complete_profile_candidate_count": sum(a.get("complete_silhouette", True) for a in bassets[b["id"]]),
            "partial_visual_candidate_count": sum(not a.get("complete_silhouette", True) for a in bassets[b["id"]]),
        })
    boss_csv = make_csv(boss_rows, list(boss_rows[0]))
    local_date = display_date(summary["updated_utc"])
    missing_guards = [f["name"] for f in fighters if f["id"] in summary["guard_fighters_without_candidate"]]
    missing_guard_text = ", ".join(missing_guards) if missing_guards else "aucune"
    missing_guard_failures = sum(entity_id(r) in summary["guard_fighters_without_candidate"] and is_failure(r) for r in records)
    lines = ["# Halo Combats — gardes statiques et Boss Battle, vague 5", "", f"Mise à jour : {local_date}.", "",
        "## Résultats vérifiés", "",
        f"La V5 apporte **{counts['wave5_generated_pngs']} nouveaux PNG distincts** : {counts['wave5_generated_guard_pngs']} gardes statiques et {counts['wave5_generated_boss_pngs']} profils ou présences de rencontres Boss Battle.", "",
        f"**{counts['fighter_entities_with_guard_candidate']}/{len(fighters)} combattants possèdent une garde statique candidate** ; les {counts['fighter_entities_with_visual_candidate']}/{len(fighters)} combattants conservent leurs poses de référence antérieures. **{counts['boss_entities_with_visual_candidate']}/{len(bosses)} rencontres Boss Battle disposent d'un visuel candidat.**", "",
        f"Parmi les rencontres Boss Battle illustrées, **{counts['boss_entities_with_complete_profile_candidate']} disposent d'une silhouette complète candidate** ; {counts['boss_entities_with_partial_visual_only']} disposent uniquement d'une présence ou d'un élément partiel. Un asset partiel ne compte pas comme corps complet du boss.", "",
        f"Le journal contient {len(records)} tentatives : {counts['wave5_successful_generation_attempts']} réussites et {counts['wave5_generation_failures']} échecs. Les {counts['historical_generation_failures_all_waves']} échecs historiques restent conservés ; une réussite ultérieure ne laisse pas l'entité classée manquante.", "",
        f"Garde encore manquante : **{safe_md(missing_guard_text)}**. {missing_guard_failures} échecs de génération sont conservés pour cette liste ; la pose de référence antérieure reste disponible. Le Locust V01 est conservé comme candidat à corriger ; le Locust V02 à quatre pattes est la variante préférée.", "",
        "Une garde est une image fixe de posture de combat, pas une boucle d'animation ni une animation de blocage. Les profils de boss ne remplacent pas les éléments articulés, phases, effets, collisions ou comportements. Aucun nouveau clip animé ou asset intégré au moteur n'est revendiqué. La fidélité 1:1 reste à valider.", "",
        "## Gardes des combattants", "", "| Personnage | Images de garde | Variante préférée | Contrôle visuel |", "|---|---:|---|---|"]
    for f in fighters:
        guards = [a for a in fassets[f["id"]] if a.get("pose_scope") == "guard_static"]
        a = preferred(guards, f.get("preferred_guard_asset"))
        lines.append(f"| {safe_md(f['name'])} | {len(guards)} | {a['path'] if a else 'Manquante'} | {a.get('visual_review_status', 'à contrôler') if a else 'Sans image'} |")
    lines += ["", "## Profils et présences de rencontres Boss Battle", "", "Les entrées de type événement, dont le Guardian et la présence du Gravemind, conservent leur rôle défini dans la bible. La disponibilité d'une image ne crée pas un combat canonique ni une nouvelle condition de destruction. Une présence ou un tentacule isolé est explicitement distingué d'une silhouette complète.", "", "| Rencontre | Jeu | Images | Variante préférée | Portée |", "|---|---|---:|---|---|"]
    for b in bosses:
        a = preferred(bassets[b["id"]], b.get("preferred_visual_asset"))
        lines.append(f"| {safe_md(b['name'])} | {safe_md(b.get('origin', ''))} | {len(bassets[b['id']])} | {a['path'] if a else 'Manquant'} | {safe_md(boss_scope(a))} |")
    lines += ["", "## Observations des nouveaux fichiers", ""]
    for a in active:
        if a.get("generation_wave") != 5:
            continue
        lines += [f"### {a['id']}", "", f"Fichier : {a['path']} — {a['width']} × {a['height']} px, {a['mode']}. Empreinte SHA-256 : {a['sha256']}.", ""]
        for note in a.get("visual_review", {}).get("notes", [a.get("qa", "Inspection en attente.")]):
            lines.append("- " + str(note))
        lines.append("")
    lines += ["## Références, conservation et limites", "",
        "Les gardes reprennent les candidats de référence déjà disponibles. Une image générée antérieure n'est pas une validation indépendante de la géométrie du jeu original. Les sources complémentaires utilisées pour les boss restent documentées dans leurs métadonnées et dans les briefs ; les téléchargements de référence ne sont pas comptés comme nouvelles générations.", "",
        "Les PNG ont été copiés octet pour octet. Les 30 candidats antérieurs et leurs métadonnées sont conservés, avec les préférences neutres de Kat, Carter et Escharum. Les préférences de garde sont séparées des préférences neutres. Le canal alpha, les marges et les contacts au cadre sont mesurés en lecture seule ; les notes visuelles sont liées au SHA du fichier inspecté.", "",
        "Le CSV des personnages conserve les colonnes de référence historiques. candidate_count compte toutes les poses, latest_asset_id désigne le fichier le plus récent, preferred_asset_id et relative_path restent la référence neutre/précédente. Les colonnes guard_* identifient la garde séparément. Les réserves signalées doivent être résolues avant production finale des animations.", ""]
    if summary["failed_attempts_in_journal"]:
        lines += ["## Échecs V5 conservés", ""]
        for f in summary["failed_attempts_in_journal"]:
            lines.append(f"- Entrée {f['journal_record'] + 1}, {f['entity_id']} : {failure_summary(f)}")
        lines.append("")
    report = "\n".join(lines).rstrip() + "\n"
    readme = f"""# Halo Combats — livraison V5 : gardes et Boss Battle

Mode annexe de combat 2D pour Darknigthmare. Mise à jour : {local_date}.

## État livré

**{counts['fighter_entities_with_visual_candidate']}/{len(fighters)} combattants possèdent un visuel de référence ; {counts['fighter_entities_with_guard_candidate']}/{len(fighters)} possèdent aussi une garde statique candidate.** Les visuels disponibles couvrent **{counts['boss_entities_with_visual_candidate']}/{len(bosses)} rencontres Boss Battle**.

Pour les rencontres Boss Battle, **{counts['boss_entities_with_complete_profile_candidate']}/{len(bosses)} disposent d'au moins une silhouette complète candidate** ; **{counts['boss_entities_with_partial_visual_only']} rencontres n'ont qu'une présence ou un élément partiel**. Les portées exactes figurent dans l'inventaire et le rapport V5.

La V5 ajoute **{counts['wave5_generated_pngs']} PNG** : {counts['wave5_generated_guard_pngs']} gardes et {counts['wave5_generated_boss_pngs']} profils de boss/événements. Les versions précédentes restent disponibles.

Garde encore manquante : **{missing_guard_text}**, après {missing_guard_failures} échecs de génération conservés. Sa pose de référence antérieure reste disponible. La V5 totalise {counts['wave5_generation_attempts']} tentatives, dont {counts['wave5_generation_failures']} échecs ; l'historique cumulé conserve {counts['historical_generation_failures_all_waves']} échecs. Le Locust V02 à quatre pattes est préféré ; le V01 reste archivé dans les candidats avec son défaut anatomique signalé.

| Catégorie | Fichiers disponibles | Portée |
|---|---:|---|
| Poses de combattants | {counts['active_fighter_pose_candidates']} | Références antérieures et gardes statiques |
| Gardes statiques comprises ci-dessus | {counts['active_guard_pose_candidates']} | {counts['fighter_entities_with_guard_candidate']}/{len(fighters)} combattants |
| Profils et présences Boss Battle | {counts['active_boss_visual_candidates']} | {counts['boss_entities_with_visual_candidate']}/{len(bosses)} rencontres ; portée complète ou partielle précisée |
| Masters de décors | {counts['active_stage_visual_candidates']} | Couches parallaxe indépendantes à produire |
| Tous candidats visuels | {counts['active_visual_candidates']} | Total de fichiers distincts |
| Clips d'animation livrés | {counts.get('animation_clips', 0)} | Les poses fixes ne sont pas des clips |

Les visuels restent candidats, non certifiés 1:1. Une garde ne constitue pas une boucle animée ; un profil de boss ne constitue pas une rencontre jouable. Cette livraison ne modifie pas le prototype.

## Ouvrir les livrables

- [Gardes V5](assets/characters_wave5/) et [profils Boss Battle V5](assets/bosses_wave5/).
- [Suivi détaillé V5](docs/HALO_COMBATS_GARDES_BOSS_V5.md), [inventaire des personnages](data/characters_visual_inventory.csv) et [inventaire Boss Battle](data/bosses_visual_inventory.csv).
- [Références Boss Battle](docs/SOURCES_BOSS_V5.md) et [preuves de vérification V5](work/wave5/verification.json).
- [Manifeste courant](data/asset_manifest.json), [compteurs](data/delivery_counts.json), [journal V5](work/wave5/generation_results.json) et [QA V5](work/wave5/qa_wave5.json).
- [Livraison V4](README_V4.md), [V3](README_V3.md) et [V2](README_V2.md) : états historiques conservés.
- [Bible DOCX V1](docs/HALO_COMBATS_BIBLE_V1.docx), [bible Markdown V1](docs/HALO_COMBATS_BIBLE_V1.md) et [classeur V1](docs/HALO_COMBATS_PRODUCTION_V1.xlsx) : spécifications et état daté ; les registres JSON/CSV portent le suivi visuel courant.
- [Prototype indépendant](prototype/halo_combats_prototype.html) : entraînement, duel IA et mécanique partielle Scarab avec visuels temporaires.

Les animations, armes/effets manquants, collisions, comportement des boss et intégration complète restent à produire. Les rencontres événementielles conservent leur rôle narratif spécifié ; une image de Guardian n'implique pas sa destruction.
"""
    return report, fighter_csv, boss_csv, readme


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--journal", type=Path, default=JOURNAL)
    parser.add_argument("--qa", type=Path, default=QA)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    journal = args.journal.resolve()
    records = v4.records_from(json.loads(journal.read_text(encoding="utf-8")))
    reviews = v4.load_visual_qa(args.qa)
    baseline = json.loads(BASELINE.read_text())
    manifest = json.loads(MANIFEST.read_text()); roster = json.loads(FIGHTERS.read_text()); world = json.loads(BOSSES.read_text())
    old_counts = json.loads(COUNTS.read_text())
    with CHARACTER_CSV.open(encoding="utf-8-sig", newline="") as stream:
        old_csv_rows = list(csv.DictReader(stream))
    verify_baseline(manifest, baseline, old_counts)
    guarded_paths = [journal, args.qa, BASELINE, MANIFEST, FIGHTERS, BOSSES, COUNTS, CHARACTER_CSV]
    file_guards = {p: digest(p) for p in guarded_paths}
    fighters, bosses = roster["fighters"], world["entities"]
    fighter_ids = {x["id"] for x in fighters}; boss_ids = {x["id"] for x in bosses}
    active = manifest["active_candidates"]
    prior_active = copy.deepcopy(active)
    v4.verify_existing_assets(active, fighter_ids)
    record_hashes = [canonical_sha(r) for r in records]
    if SUMMARY.exists():
        previous = json.loads(SUMMARY.read_text())
        old_hashes = previous.get("record_sha256", [])
        if record_hashes[:len(old_hashes)] != old_hashes:
            raise ValueError("Une entrée du journal déjà consolidée a été modifiée ou retirée.")
    reserved, seen, added, plans, failures, duplicates, reused_prior = {}, {}, [], [], [], [], []
    content_owners = {a["sha256"]: entity_id(a) for a in active}
    journal_rel = journal.relative_to(PROJECT).as_posix()
    for index, record in enumerate(records):
        owner = entity_id(record); kind, scope = entity_kind(record, fighter_ids, boss_ids)
        if is_failure(record):
            failure = {"entity_id": owner, "entity_type": kind, "pose_scope": scope, "status": record.get("status", "generation_failed"), "error": record.get("error", ""), "prompt": record.get("prompt", ""), "generation_wave": 5, "source_journal": journal_rel, "journal_record": index, "attempt_kind": record.get("attempt_kind", scope)}
            for key in ("generation_method", "reference_input", "correction_of_source_path", "retry_of_attempt", "retry_reason", "retry_index", "variant", "journal_origin", "equipment_state", "facing", "representation_scope", "complete_silhouette", "depicted_region"):
                if key in record: failure[key] = record[key]
            failures.append(failure); continue
        source = v4.resolve_source(record, journal)
        if source is None or not source.is_file():
            raise ValueError(f"PNG absent pour l'entrée {index + 1} : {owner}")
        sha = digest(source)
        if sha in content_owners and content_owners[sha] != owner:
            raise ValueError(f"Les mêmes octets sont affectés à deux entités : {owner} et {content_owners[sha]}")
        content_owners[sha] = owner
        if (owner, sha) in seen:
            duplicates.append({"entity_id": owner, "sha256": sha, "journal_record": index, "same_as_record": seen[(owner, sha)]}); continue
        seen[(owner, sha)] = index
        old = next((a for a in active if a.get("sha256") == sha and a.get("generation_wave") != 5), None)
        if old:
            reused_prior.append({"entity_id": owner, "asset_id": old["id"], "sha256": sha, "journal_record": index}); continue
        review = next((r for r in reversed(reviews) if r.get("entity_id") == owner and r.get("sha256") == sha), None)
        if args.apply and (not review or not review.get("reviewed_utc")):
            raise ValueError(f"Revue visuelle liée au SHA manquante : {owner}, {sha}")
        metrics = review.get("image_metrics") if review else None
        if not metrics: metrics = v4.inspect_png(source)
        destination, asset_id = destination_for(owner, kind, sha, active, reserved)
        notes = review.get("notes", []) if review else ["Inspection visuelle en attente."]
        if isinstance(notes, str): notes = [notes]
        candidate = {
            "id": asset_id, "entity_id": owner, "entity_type": kind, "type": "fighter_pose" if kind == "fighter" else "boss_profile",
            "prompt": record.get("prompt", ""), "output": destination.name, "path": destination.relative_to(PROJECT).as_posix(),
            "qa": " ".join(notes), "status": "candidate", "fidelity_status": "not_certified", "animation_status": "not_animated", "integration_status": "not_integrated",
            "generation_wave": 5, "pose_scope": scope, "attempt_kind": record.get("attempt_kind", scope), "sha256": sha,
            "source_path": str(source), "source_journal": journal_rel, "journal_record": index,
            "visual_review_status": "reviewed_candidate_requires_correction" if review and review.get("verdict") == "candidate_requires_correction" else "reviewed_candidate_with_reservations" if review else "pending_visual_review",
            "required_followup": list(dict.fromkeys((review.get("required_followup", []) if review else []) + ["Validation de fidélité aux références du jeu", "Animations et déclinaisons", "Collisions et intégration au moteur"])), **metrics,
        }
        if review: candidate["visual_review"] = review
        if kind == "boss":
            candidate.update({"representation_scope": "complete_profile", "complete_silhouette": True})
        for key in ("reference_urls", "reference_images", "reference_title", "visual_lock", "critical_checks", "orientation", "facing", "equipment_state", "generation_method", "reference_input", "referenced_image_paths", "correction_of_source_path", "correction_of_sha256", "input_asset_id", "input_asset_path", "encounter_usage", "retry_of_attempt", "retry_reason", "retry_index", "variant", "journal_origin", "representation_scope", "complete_silhouette", "depicted_region", "reference_evidence_limits"):
            if key in record: candidate[key] = record[key]
        if kind == "boss" and review and "complete_silhouette" in review:
            candidate["complete_silhouette"] = review["complete_silhouette"]
        existing_index = next((i for i, a in enumerate(active) if a["id"] == asset_id), None)
        if existing_index is None:
            active.append(candidate); added.append(candidate)
        else:
            if active[existing_index].get("generation_wave") != 5: raise ValueError("Tentative de réécriture d'un candidat antérieur.")
            active[existing_index] = {**active[existing_index], **candidate}
        plans.append({"entity_id": owner, "entity_type": kind, "asset_id": asset_id, "source": str(source), "destination": str(destination), "sha256": sha})
    for failure in failures:
        old = next((f for f in manifest["failed_requests"] if f.get("generation_wave") == 5 and f.get("source_journal") == journal_rel and f.get("journal_record") == failure["journal_record"]), None)
        if old is not None and old != failure: raise ValueError("Échec précédemment consolidé modifié.")
        if old is None: manifest["failed_requests"].append(failure)
    for f in fighters:
        poses = [a for a in active if a["type"] == "fighter_pose" and entity_id(a) == f["id"]]
        guards = [a for a in poses if a.get("pose_scope") == "guard_static"]
        f["visual_assets"] = [a["id"] for a in poses]
        f["guard_visual_assets"] = [a["id"] for a in guards]
        guard = preferred(guards, f.get("preferred_guard_asset"))
        f["guard_art_status"] = "static_candidate_generated" if guard else "not_generated"
        if guard: f["preferred_guard_asset"] = guard["id"]
    for b in bosses:
        profiles = [a for a in active if a["type"] == "boss_profile" and entity_id(a) == b["id"]]
        if profiles:
            b["visual_assets"] = [a["id"] for a in profiles]
            b["preferred_visual_asset"] = preferred(profiles, b.get("preferred_visual_asset"))["id"]
            b["art_status"] = "candidate"; b["fidelity_status"] = "not_certified"
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    wave = [a for a in active if a.get("generation_wave") == 5]
    guards = [a for a in active if a.get("pose_scope") == "guard_static"]
    fcovered = {entity_id(a) for a in active if a["type"] == "fighter_pose"}
    bcovered = {entity_id(a) for a in active if a["type"] == "boss_profile"}
    bcomplete = {entity_id(a) for a in active if a["type"] == "boss_profile" and a.get("complete_silhouette", True)}
    bpartial = {entity_id(a) for a in active if a["type"] == "boss_profile" and not a.get("complete_silhouette", True)}
    gcovered = {entity_id(a) for a in guards}
    counts = dict(old_counts)
    counts.update({
        "active_visual_candidates": len(active), "active_fighter_pose_candidates": sum(a["type"] == "fighter_pose" for a in active),
        "active_boss_visual_candidates": sum(a["type"] == "boss_profile" for a in active), "active_stage_visual_candidates": sum(a["type"] == "stage_master" for a in active),
        "active_guard_pose_candidates": len(guards), "fighter_entities_with_guard_candidate": len(gcovered), "fighter_entities_without_guard_candidate": len(fighter_ids - gcovered),
        "fighter_entities_with_visual_candidate": len(fcovered), "fighter_entities_without_visual_candidate": len(fighter_ids - fcovered),
        "boss_entities_with_visual_candidate": len(bcovered), "boss_entities_without_visual_candidate": len(boss_ids - bcovered),
        "boss_entities_with_complete_profile_candidate": len(bcomplete), "boss_entities_without_complete_profile_candidate": len(boss_ids - bcomplete),
        "boss_entities_with_partial_visual_only": len(bpartial - bcomplete),
        "visual_candidates_pre_wave5": baseline["candidate_count"], "wave5_generated_pngs": len(wave),
        "wave5_generated_guard_pngs": sum(a["type"] == "fighter_pose" for a in wave), "wave5_generated_boss_pngs": sum(a["type"] == "boss_profile" for a in wave),
        "wave5_generated_complete_boss_pngs": sum(a["type"] == "boss_profile" and a.get("complete_silhouette", True) for a in wave),
        "wave5_generated_partial_boss_pngs": sum(a["type"] == "boss_profile" and not a.get("complete_silhouette", True) for a in wave),
        "wave5_generation_attempts": len(records), "wave5_successful_generation_attempts": sum(not is_failure(r) for r in records), "wave5_generation_failures": len(failures),
        "wave5_automatic_generation_rejections": sum("moderation_blocked" in str(f.get("error", "")) for f in failures),
        "wave5_unique_fighters_with_guard_candidates": len({entity_id(a) for a in wave if a["type"] == "fighter_pose"}),
        "wave5_unique_boss_entities_with_candidates": len({entity_id(a) for a in wave if a["type"] == "boss_profile"}),
        "historical_generation_failures_all_waves": len(manifest["failed_requests"]), "updated_utc": stamp,
    })
    if sum(counts[k] for k in ["active_fighter_pose_candidates", "active_boss_visual_candidates", "active_stage_visual_candidates"]) != len(active): raise ValueError("Somme des catégories incohérente.")
    manifest.update({"updated_utc": stamp, "generated_unique_entities": len({entity_id(a) for a in active}), "generated_fighter_entities": len(fcovered), "generated_boss_entities": len(bcovered), "generated_guard_entities": len(gcovered)})
    summary = {"generation_wave": 5, "updated_utc": stamp, "journal_sha256": file_guards[journal], "record_sha256": record_hashes, "counts": counts, "new_candidate_assets_this_run": len(added), "new_candidate_ids_this_run": [a["id"] for a in added], "failed_attempts_in_journal": failures, "duplicate_records_skipped": duplicates, "reused_prior_candidate_records": reused_prior, "planned_files": plans, "guard_fighters_without_candidate": sorted(fighter_ids - gcovered), "boss_entities_without_candidate": sorted(boss_ids - bcovered), "applied": args.apply}
    summary["boss_entities_without_complete_profile_candidate"] = sorted(boss_ids - bcomplete)
    summary["boss_entities_with_partial_visual_only"] = sorted(bpartial - bcomplete)
    report, fighter_csv, boss_csv, readme = make_outputs(fighters, bosses, active, records, manifest["failed_requests"], summary, counts, old_csv_rows)
    verify_baseline(manifest, baseline, counts)
    for old in prior_active:
        if old.get("generation_wave") != 5 and next(a for a in active if a["id"] == old["id"]) != old: raise ValueError("Métadonnées antérieures modifiées.")
    for path, sha in file_guards.items():
        if digest(path) != sha: raise ValueError(f"Fichier modifié pendant la préparation : {path}")
    print(json_text({"applied": args.apply, "attempts": len(records), "new_assets_this_run": len(added), "wave5_pngs": len(wave), "guard_fighters": len(gcovered), "boss_entities": len(bcovered), "total_candidates": len(active), "failures_all_waves": len(manifest["failed_requests"])}))
    if not args.apply:
        print("Lecture seule : aucune copie ni modification."); return 0
    for plan in plans:
        source, dest = Path(plan["source"]), Path(plan["destination"])
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            if digest(dest) != plan["sha256"]: raise ValueError(f"Collision de copie : {dest}")
            continue
        with source.open("rb") as src, dest.open("xb") as dst:
            shutil.copyfileobj(src, dst, 1024*1024); dst.flush(); os.fsync(dst.fileno())
        if digest(dest) != plan["sha256"]: raise ValueError(f"Copie différente : {dest}")
    backup = WORK / "README_V4_before_wave5.md"
    if not backup.exists(): shutil.copyfile(PROJECT / "README.md", backup)
    outputs = [(MANIFEST, json_text(manifest)), (FIGHTERS, json_text(roster)), (BOSSES, json_text(world)), (COUNTS, json_text(counts)), (CHARACTER_CSV, fighter_csv), (BOSS_CSV, boss_csv), (REPORT, report), (PROJECT / "README_V5.md", readme), (PROJECT / "README.md", readme), (SUMMARY, json_text(summary))]
    for path, content in outputs: write_atomic(path, content)
    print("Consolidation V5 appliquée, PNG copiés à l'identique, historique et préférences neutres conservés.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
