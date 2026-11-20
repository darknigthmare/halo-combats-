#!/usr/bin/env python3
"""Consolidate V6 expansion-character art without changing the base gameplay roster.

Default is read-only. --apply requires all 34 catalog entries and SHA-bound QA.
Downloaded references are never published as generated assets. PNG bytes are
copied unchanged. A Warden catalog alias reuses its V5 boss asset explicitly.
"""
from __future__ import annotations

import argparse
import copy
import csv
import importlib.util
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
WORK = PROJECT / "work/wave6"
JOURNAL = WORK / "generation_results.json"
QA = WORK / "qa_wave6.json"
BASELINE = WORK / "baseline_v5.json"
SUMMARY = WORK / "consolidation_summary.json"
CATALOG = PROJECT / "data/expansion_characters.json"
CATALOG_INPUTS = {"unsc_catalog.json": 14, "alien_catalog.json": 15, "root_catalog.json": 5}
REPORT = PROJECT / "docs/HALO_COMBATS_PERSONNAGES_V6.md"
SOURCES = PROJECT / "docs/SOURCES_PERSONNAGES_V6.md"
MANIFEST = PROJECT / "data/asset_manifest.json"
FIGHTERS = PROJECT / "data/fighters.json"
COUNTS = PROJECT / "data/delivery_counts.json"
BASE_CSV = PROJECT / "data/characters_visual_inventory.csv"
EXTENSION_CSV = PROJECT / "data/expansion_characters_visual_inventory.csv"

_spec = importlib.util.spec_from_file_location("halo_wave5_helpers", PROJECT / "work/wave5/consolidate_wave5.py")
v5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v5)
v4 = v5.v4
digest, canonical_sha, json_text = v5.digest, v5.canonical_sha, v5.json_text
write_atomic, safe_md = v5.write_atomic, v5.safe_md


def preferred(assets, previous_id=None):
    # Retain flawed outputs in the catalog, but never select them automatically.
    usable = [a for a in assets if a.get("visual_review_status") != "reviewed_candidate_requires_correction"]
    return v5.preferred(usable, previous_id)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def entries_from(value):
    if isinstance(value, list):
        return value
    for key in ("entries", "characters", "records"):
        if isinstance(value, dict) and isinstance(value.get(key), list):
            return value[key]
    raise ValueError("A catalog must contain entries/characters/records or a list.")


def protected_roster(roster, fields):
    result = copy.deepcopy(roster)
    for fighter in result["fighters"]:
        if fighter["id"] == "chief_infinite":
            for key in fields:
                fighter.pop(key, None)
    return result


def verify_baseline(manifest, baseline, counts, roster):
    active = {a["id"]: a for a in manifest["active_candidates"]}
    assert len(active) == len(manifest["active_candidates"]), "Duplicate candidate ID"
    for old in baseline["candidates"]:
        asset = active.get(old["id"])
        assert asset and canonical_sha(asset) == old["metadata_sha256"], "Prior metadata changed: " + old["id"]
        assert digest(PROJECT / old["path"]) == old["sha256"], "Prior PNG changed: " + old["path"]
    assert canonical_sha(manifest["failed_requests"][:baseline["historical_failures"]]) == baseline["prior_failed_requests_sha256"], "Prior failures changed"
    for key, value in baseline["prior_counts"].items():
        if key.startswith(("wave2_", "wave3_", "wave4_", "wave5_")) or key in {"fighters", "normals", "specials", "supers", "combos", "finishers", "story_routes", "boss_encounters", "stages", "planned_parallax_layers", "planned_animation_clips", "drawing_budget_both_directions", "animation_clips", "certified_visuals"}:
            assert counts.get(key) == value, "Protected counter changed: " + key
    p = baseline["registry_structure"]
    assert canonical_sha(protected_roster(roster, p["chief_allowed_fields"])) == p["fighters_protected_sha256"], "Base fighter design or other art metadata changed"
    assert canonical_sha(read_json(PROJECT / "data/bosses.json")) == p["bosses_protected_sha256"], "Boss registry changed"
    assert {f["id"]: f.get("preferred_visual_asset") for f in roster["fighters"]} == p["neutral_preferences"], "Neutral preferences changed"


def load_catalog(strict=False):
    entries, inputs = [], []
    for filename, expected in CATALOG_INPUTS.items():
        path = WORK / filename
        if not path.is_file():
            if strict:
                raise ValueError("Catalog input absent: " + filename)
            continue
        rows = entries_from(read_json(path))
        if strict and len(rows) != expected:
            raise ValueError(f"{filename}: expected {expected} entries, got {len(rows)}")
        inputs.append({"path": path.relative_to(PROJECT).as_posix(), "sha256": digest(path), "entries": len(rows)})
        for row in rows:
            entry = copy.deepcopy(row)
            entry["id"] = str(entry.get("id") or entry.get("entity_id") or "")
            if not entry["id"] or not entry.get("name"):
                raise ValueError("Catalog entry needs id and name")
            if not entry.get("game_version"):
                raise ValueError("Exact game_version absent: " + entry["id"])
            entry["catalog_source"] = path.relative_to(PROJECT).as_posix()
            entries.append(entry)
    ids = [e["id"] for e in entries]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate expansion catalog ID")
    if strict and len(entries) != 34:
        raise ValueError("Expected 34 catalog entries including reused Warden")
    if strict:
        assert "colony_single_body_hw2" in ids and "colony_hunter_captain_hw2" not in ids, "Colony must not be replaced by its distinct Hunter Captain unit"
    return entries, inputs


def destination_for(owner, scope, sha, active, reserved):
    prior = next((a for a in active if a.get("entity_id") == owner and a.get("sha256") == sha and a.get("pose_scope") == scope), None)
    if prior:
        return PROJECT / prior["path"], prior["id"]
    stem = owner + ("_guard_right" if scope == "guard_static" else "_initial_right")
    folder = PROJECT / "assets/characters_wave6"
    for version in range(1, 10000):
        name = f"{stem}_v{version:02d}"
        path = folder / (name + ".png")
        old = next((a for a in active if a["id"] == name), None)
        if old and old["sha256"] != sha:
            continue
        if name in reserved and reserved[name] != sha:
            continue
        if path.exists() and (not path.is_file() or digest(path) != sha):
            continue
        reserved[name] = sha
        return path, name
    raise ValueError("No available version: " + owner)


def compact(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, separators=(",", ":"))


DESIGN_LABELS = {
    "status": "Statut", "scope": "Portée", "name": "Nom", "description": "Description",
    "specials_proposed": "Spéciaux proposés", "boss_readability": "Lisibilité et règles de combat",
    "story_proposal": "Introduction, rival et fin proposés", "existing_boss_link": "Lien avec le boss existant",
    "reuse_scope": "Portée du réemploi", "function_proposed": "Fonction proposée",
    "counterplay_proposed": "Contre-jeu", "counterplay": "Contre-jeu",
    "weakness_and_counterplay_proposed": "Faiblesses et contre-jeu", "weaknesses": "Faiblesses",
    "intro_proposed": "Introduction proposée", "rival_proposed": "Rival proposé", "ending_proposed": "Fin proposée",
    "frame_data_status": "Données de combat à définir", "super_proposed": "Super proposée",
    "finisher_proposed": "Finisher proposé", "sequence": "Déroulement", "trigger": "Déclenchement",
    "target_adaptation": "Adaptation aux cibles", "presentation": "Présentation",
    "implementation_status": "État de production", "premise": "Situation", "continuity": "Continuité",
    "intro": "Introduction", "rival": "Rival", "ending": "Fin", "story": "Parcours proposé",
}


def design_prose(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join("**" + DESIGN_LABELS.get(k, k.replace("_", " ")) + " :** " + design_prose(v) for k, v in value.items())
    if isinstance(value, list):
        return " ; ".join(design_prose(v) for v in value)
    return str(value)


def design_counts(entries):
    briefs = [e.get("combat_brief", {}) for e in entries]
    return {
        "expansion_entries_with_combat_brief": sum(bool(b) for b in briefs),
        "expansion_entries_with_new_combat_proposals": sum(bool(b.get("specials_proposed")) for b in briefs),
        "expansion_proposed_specials": sum(len(b.get("specials_proposed", [])) for b in briefs),
        "expansion_proposed_supers": sum(bool(b.get("super_proposed")) for b in briefs),
        "expansion_proposed_finishers": sum(bool(b.get("finisher_proposed")) for b in briefs),
        "expansion_short_story_proposals": sum(any(b.get(k) for k in ("story_proposal", "intro_proposed", "story", "story_route_proposed")) for b in briefs),
    }


def source_links(entry):
    found = []
    def visit(value):
        if isinstance(value, str) and value.startswith(("https://", "http://")):
            found.append(value)
        elif isinstance(value, dict):
            for key, item in value.items():
                if key not in {"prompt", "source_path", "local_file", "inspection_path"}:
                    visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)
    visit(entry)
    return list(dict.fromkeys(found))


def make_outputs(entries, active, records, summary, counts, old_base_rows, roster, failures):
    by_id = {a["id"]: a for a in active}
    extension_rows = []
    for entry in entries:
        asset = by_id.get(entry.get("preferred_visual_asset"))
        entry_assets = [by_id[aid] for aid in entry["visual_assets"]]
        fallback_qa = ("Aucun candidat préféré ; les variantes existantes requièrent une correction. " + " ".join(a["id"] + " : " + a.get("qa", "") for a in entry_assets)) if entry_assets else "Image non générée."
        extension_rows.append({
            "entity_id": entry["id"], "name": entry["name"], "category": compact(entry.get("category", "")), "game_version": entry["game_version"],
            "selected_representation": compact(entry.get("selected_representation", "")), "proposed_role": compact(entry.get("proposed_role", "")),
            "art_status": entry["art_status"], "new_candidate_count": len(entry["new_visual_assets"]), "reused_asset_id": entry.get("reused_visual_asset", ""),
            "preferred_asset_id": asset["id"] if asset else "", "relative_path": asset["path"] if asset else "", "sha256": asset["sha256"] if asset else "",
            "all_candidate_paths": " ; ".join(a["path"] for a in entry_assets), "all_candidate_sha256": " ; ".join(a["sha256"] for a in entry_assets),
            "equipment_state": entry.get("equipment_state", asset.get("equipment_state", "") if asset else ""),
            "target_facing": "not_applicable_prior_reuse" if entry.get("reused_visual_asset") else asset.get("target_facing", "right") if asset else "right",
            "observed_facing": "left" if entry.get("reused_visual_asset") else asset.get("observed_facing", "not_recorded") if asset else "no_preferred_candidate" if entry_assets else "no_image",
            "candidate_orientations": compact([{"asset_id": aid, "target_facing": "not_applicable_prior_reuse" if entry.get("reused_visual_asset") else by_id[aid].get("target_facing", "right"), "observed_facing": "left" if entry.get("reused_visual_asset") else by_id[aid].get("observed_facing", "not_recorded")} for aid in entry["visual_assets"]]),
            "visual_review_status": asset.get("visual_review_status", "") if asset else "reviewed_candidates_require_correction_no_preferred" if entry_assets else "no_image",
            "fidelity_status": "not_certified", "animation_status": "not_animated", "integration_status": "not_integrated", "gameplay_design_status": "proposed_not_implemented",
            "wave6_attempt_count": sum(v4.entity_id(r) == entry["id"] for r in records), "wave6_failure_count": sum(v4.entity_id(r) == entry["id"] and v4.is_failure(r) for r in records),
            "sources": " ; ".join(source_links(entry)), "visual_qa": asset.get("qa", "") if asset else fallback_qa,
        })
    extension_csv = v5.make_csv(extension_rows, list(extension_rows[0]) if extension_rows else ["entity_id", "name"])
    base_rows = copy.deepcopy(old_base_rows)
    chief = next(f for f in roster["fighters"] if f["id"] == "chief_infinite")
    guards = [a for a in active if a.get("entity_id") == "chief_infinite" and a.get("pose_scope") == "guard_static"]
    guard = preferred(guards, chief.get("preferred_guard_asset"))
    for row in base_rows:
        if row["entity_id"] != "chief_infinite":
            continue
        poses = [a for a in active if a.get("entity_id") == "chief_infinite" and a["type"] == "fighter_pose"]
        row.update({"candidate_count": len(poses), "latest_asset_id": poses[-1]["id"], "guard_candidate_count": len(guards), "preferred_guard_asset_id": guard["id"] if guard else "", "guard_relative_path": guard["path"] if guard else "", "guard_sha256": guard["sha256"] if guard else "", "guard_equipment_state": guard.get("equipment_state", "") if guard else "", "guard_facing": guard.get("facing", "right") if guard else "", "guard_visual_review_status": guard.get("visual_review_status", "") if guard else "no_guard_image", "guard_visual_qa": guard.get("qa", "") if guard else "Garde statique toujours manquante.", "wave6_attempt_count": sum(v4.entity_id(r) == "chief_infinite" for r in records)})
        row["historical_failure_count"] = sum(v4.entity_id(r) == "chief_infinite" for r in failures)
    fields = list(old_base_rows[0])
    fields += [k for row in base_rows for k in row if k not in fields]
    fields = list(dict.fromkeys(fields))
    base_csv = v5.make_csv(base_rows, fields)
    date = v5.display_date(summary["updated_utc"])
    corrections = counts["expansion_catalog_entries_requiring_correction_only"]
    correction_phrase = "1 entrée n’a que des sorties à corriger" if corrections == 1 else f"{corrections} entrées n’ont que des sorties à corriger"
    missing = [e["name"] for e in entries if not e["visual_assets"]]
    missing_text = ", ".join(missing) or "Aucune dans les 34 entrées nommées de cette extension."
    chief_text = ("La garde du Major dispose maintenant d'un candidat V6." if guard else
                  "Une variante de garde du Major existe mais requiert encore une correction." if guards else
                  "La garde du Major reste manquante ; tous les refus sont conservés.")
    readme = f"""# Halo Combats — livraison V6 : personnages des extensions

Mise à jour : {date}.

La V6 ajoute **{counts['wave6_generated_pngs']} PNG distincts** : **{counts['wave6_generated_expansion_pngs']} visuels de personnages/classes d'extension** et **{counts['wave6_generated_guard_pngs']} garde du roster de base**.

Le catalogue d'extensions comporte **34 entrées**. **{counts['expansion_catalog_entries_with_visual']}/34 disposent d'un visuel candidat**, dont **{counts['expansion_catalog_entries_with_reused_visual']} réutilisation explicite du Warden Eternal V5**. Cette réutilisation ne compte pas comme nouvelle génération. Parmi les entrées illustrées, **{counts['expansion_catalog_entries_with_preferred_visual']} possèdent un candidat préféré**, et **{correction_phrase}**. Les **24 fiches de combattants de base** conservent leurs spécifications ; les extensions sont documentées séparément et ne sont pas automatiquement intégrées au prototype.

{chief_text} Le roster de base possède **{counts['fighter_entities_with_guard_candidate']}/24 gardes statiques**.

L’annexe de bible développe **{counts['expansion_entries_with_new_combat_proposals']} propositions de combat d’extension** : **{counts['expansion_proposed_specials']} pistes de spéciaux**, **{counts['expansion_proposed_supers']} supers**, **{counts['expansion_proposed_finishers']} finishers** et **{counts['expansion_short_story_proposals']} parcours courts proposés**. Ces adaptations sont originales, non canoniques et non implémentées ; elles ne constituent pas des movesets complets ni équilibrés.

| Mesure | État |
|---|---:|
| Tentatives de génération V6 | {counts['wave6_generation_attempts']} |
| PNG générés V6 | {counts['wave6_generated_pngs']} |
| Échecs V6 conservés | {counts['wave6_generation_failures']} |
| Images candidates cumulées, variantes comprises | {counts['active_visual_candidates']} |
| Entrées base + extensions documentées | {counts['character_catalog_total_entries_including_base']} |
| Entrées base + extensions avec visuel | {counts['character_catalog_entities_with_visual_including_base']} |
| Fiches de gameplay du roster de base | 24 |
| Clips d'animation livrés | {counts['animation_clips']} |

**Entrées d'extension encore sans image :** {missing_text}

Les images sont fixes, non certifiées 1:1 et non intégrées au moteur. Les réserves d'anatomie, de cadrage, de transparence et de références sont conservées pour chaque version. Les classes anonymes, le représentant de Colony et les personnages à priorité Boss Battle sont explicités dans le catalogue. Le backlog « autres continuités » reste à énumérer ; une couverture des 34 entrées ne représente pas tous les personnages de Halo.

## Livrables

- [Visuels des personnages V6](assets/characters_wave6/).
- [Catalogue des extensions](data/expansion_characters.json) et [inventaire visuel CSV](data/expansion_characters_visual_inventory.csv).
- [Rapport V6](docs/HALO_COMBATS_PERSONNAGES_V6.md) et [sources V6](docs/SOURCES_PERSONNAGES_V6.md).
- [Journal V6](work/wave6/generation_results.json), [QA V6](work/wave6/qa_wave6.json) et [vérification](work/wave6/verification.json).
- [Compteurs courants](data/delivery_counts.json) et [manifeste des images](data/asset_manifest.json).
- [V5 : gardes et Boss Battle](README_V5.md), [V4](README_V4.md), [V3](README_V3.md), [V2](README_V2.md).
- [Bible V1](docs/HALO_COMBATS_BIBLE_V1.md), [bible DOCX](docs/HALO_COMBATS_BIBLE_V1.docx) et [prototype indépendant](prototype/halo_combats_prototype.html).

Les rencontres Boss Battle restent au nombre de 20 dans leur registre, dont 17 avec silhouette entière candidate et 3 uniquement partielles. Leurs animations, phases et intégration restent à produire.
"""
    lines = ["# Halo Combats — personnages des extensions, vague 6", "", f"Mise à jour : {date}.", "", "## Résultats", "", f"{counts['wave6_generation_attempts']} tentatives, {counts['wave6_generated_pngs']} nouveaux PNG distincts, {counts['wave6_generation_failures']} échecs conservés. Le corpus compte {counts['active_visual_candidates']} images candidates.", "", f"{counts['expansion_catalog_entries_with_visual']}/34 entrées d'extension ont un visuel, dont le Warden réutilisé depuis la V5. {chief_text}", "", "Les 24 fiches de gameplay existantes ne sont pas remplacées par ce catalogue d'art. Les rôles et modalités de représentation constituent des propositions d'adaptation ; seuls les faits explicitement sourcés sont présentés comme références des jeux.", "", "## Catalogue", "", "| Entrée | Incarnation | Portée / rôle proposé | État visuel | Visuel disponible |", "|---|---|---|---|---|"]
    for e in entries:
        a = by_id.get(e.get("preferred_visual_asset"))
        role = e.get("proposed_role", e.get("selected_representation", ""))
        role_text = role.get("description", compact(role)) if isinstance(role, dict) else compact(role)
        preferred_text = f"[{a['id']}](../{a['path']})" if a else "Image existante à corriger : " + ", ".join(f"[{aid}](../{by_id[aid]['path']})" for aid in e["visual_assets"]) if e["visual_assets"] else "Manquant"
        lines.append(f"| {safe_md(e['name'])} | {safe_md(e['game_version'])} | {safe_md(role_text)} | {e['art_status']} | {preferred_text} |")
    lines += ["", "## Annexe de bible — propositions d’adaptation", "", "Les propositions suivantes sont propres à Halo Combats. Elles ne décrivent pas un scénario canonique et ne constituent ni un moveset implémenté ni une validation de l’équilibrage. Elles prolongent la bible sans modifier les 24 fiches de gameplay existantes.", ""]
    for e in entries:
        if not e.get("combat_brief"):
            continue
        role = e.get("proposed_role", "")
        lines += ["### " + e["name"], "", "Incarnation de référence : " + e["game_version"] + ".", "", "Rôle proposé : " + (role.get("description", compact(role)) if isinstance(role, dict) else str(role)), ""]
        for key, value in e["combat_brief"].items():
            lines += ["**" + DESIGN_LABELS.get(key, key.replace("_", " ")) + "**", ""]
            if isinstance(value, list):
                lines += ["- " + design_prose(item) for item in value]
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    lines += ["**" + DESIGN_LABELS.get(subkey, subkey.replace("_", " ")) + " :** " + design_prose(subvalue), ""]
            else:
                lines.append(design_prose(value))
            lines.append("")
    lines += ["", "## Manquants et limites de portée", "", missing_text, "", "Warden Eternal : l'entrée réutilise le PNG de boss déjà publié ; aucun second corps n'est produit ni compté. Colony : le représentant unitaire est identifié dans sa fiche et ne transforme pas la paire canonique en un individu unique. Didacte, Harbinger et Warden gardent la priorité Boss Battle prévue par la bible ; l'Harbinger est Xalanyn, malgré le classement administratif commun Forerunners/Flood du backlog.", "", "Les autres continuités (Legends, romans, comics, Silver Timeline et contenus coupés documentés) restent un backlog non exhaustivement recensé. Les modèles complets, animations et variantes supplémentaires ne sont pas déduits d'une image fixe.", "", "## Revue des nouveaux PNG", ""]
    for a in active:
        if a.get("generation_wave") != 6:
            continue
        lines += ["### " + a["id"], "", f"Fichier : {a['path']} — {a['width']} × {a['height']} px, {a['mode']}. SHA-256 : {a['sha256']}.", ""]
        lines += ["- " + str(note) for note in a.get("visual_review", {}).get("notes", ["Inspection visuelle en attente."])]
        lines.append("")
    lines += ["## Conservation et vérification", "", "Les 73 anciens PNG et leurs métadonnées sont préservés, ainsi que les 72 échecs antérieurs. Les nouvelles images sont copiées octet pour octet ; aucune transformation de pixels n'est faite par le consolidateur. Chaque revue est liée à l'empreinte du PNG inspecté. Les champs d'équipement, incarnation, limites de source et réserves sont conservés.", "", "## Échecs V6", ""]
    for f in summary["failed_attempts_in_journal"]:
        lines.append(f"- Entrée {f['journal_record'] + 1}, {f['entity_id']} : {v4.failure_summary(f)}")
    if not summary["failed_attempts_in_journal"]:
        lines.append("Aucun échec enregistré.")
    sources = ["# Halo Combats — sources des personnages V6", "", "Les fichiers source téléchargés sont des références, pas des images générées. Leurs URL, empreintes, dimensions et limites détaillées sont conservées dans les catalogues de travail et les métadonnées des générations. La fidélité 1:1 n'est pas certifiée par la seule présence d'une source.", ""]
    if (WORK / "yapyap_reference_followup.json").is_file():
        sources += ["Complément pour Yapyap : [inspection supplémentaire du portfolio primaire de Jeremy Cook](../work/wave6/yapyap_reference_followup.json). Le portrait reste recadré et le key art montre une petite figure assise ; la réserve sur les pieds et le bas des jambes extrapolés n’est pas levée.", ""]
    for e in entries:
        sources += ["## " + e["name"], "", "Incarnation : " + e["game_version"] + ".", "", "Représentation : " + compact(e.get("selected_representation", "À préciser dans la fiche.")), ""]
        sources += ["- " + u for u in source_links(e)] or ["- Sources et limites présentes dans le catalogue de travail lié."]
        sources += ["", "Catalogue détaillé : " + e["catalog_source"], ""]
    return readme, "\n".join(lines).rstrip() + "\n", "\n".join(sources).rstrip() + "\n", base_csv, extension_csv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    records = v4.records_from(read_json(JOURNAL))
    entries, catalog_inputs = load_catalog(args.apply)
    reviews = v4.load_visual_qa(QA)
    baseline = read_json(BASELINE)
    manifest, roster, counts = read_json(MANIFEST), read_json(FIGHTERS), read_json(COUNTS)
    verify_baseline(manifest, baseline, counts, roster)
    with BASE_CSV.open(encoding="utf-8-sig", newline="") as stream:
        old_base_rows = list(csv.DictReader(stream))
    guarded_paths = [JOURNAL, QA, BASELINE, MANIFEST, FIGHTERS, COUNTS, BASE_CSV] + [PROJECT / x["path"] for x in catalog_inputs]
    file_guards = {p: digest(p) for p in guarded_paths if p.exists()}
    active, prior = manifest["active_candidates"], copy.deepcopy(manifest["active_candidates"])
    ids = {e["id"] for e in entries}
    assert not ids.intersection(f["id"] for f in roster["fighters"]), "Catalog duplicates base roster IDs"
    hashes = [canonical_sha(r) for r in records]
    if SUMMARY.exists():
        old_hashes = read_json(SUMMARY)["record_sha256"]
        assert hashes[:len(old_hashes)] == old_hashes, "Already consolidated journal changed"
    reserved, seen, plans, failures, duplicates, added = {}, {}, [], [], [], []
    owners = {a["sha256"]: v4.entity_id(a) for a in active}
    journal_rel = JOURNAL.relative_to(PROJECT).as_posix()
    for index, record in enumerate(records):
        owner = v4.entity_id(record)
        kind = record.get("entity_type")
        expected_scope = "guard_static" if owner == "chief_infinite" else "initial_character_pose"
        if (owner != "chief_infinite" and owner not in ids) or kind not in {"fighter", "expansion_character"} or (kind == "fighter") != (owner == "chief_infinite"):
            raise ValueError("Unexpected entity/type: " + owner + "/" + str(kind))
        if record.get("pose_scope") != expected_scope:
            raise ValueError("Unexpected pose scope: " + owner)
        if v4.is_failure(record):
            failure = copy.deepcopy(record)
            failure.update({"entity_id": owner, "generation_wave": 6, "source_journal": journal_rel, "journal_record": index})
            failures.append(failure)
            continue
        source = v4.resolve_source(record, JOURNAL)
        if source is None or not source.is_file():
            raise ValueError("Generated PNG missing: " + owner)
        sha = digest(source)
        if sha in owners and owners[sha] != owner:
            raise ValueError("Image bytes assigned to different entities: " + owner)
        owners[sha] = owner
        if (owner, sha) in seen:
            duplicates.append({"entity_id": owner, "sha256": sha, "journal_record": index, "same_as_record": seen[(owner, sha)]})
            continue
        seen[(owner, sha)] = index
        assert not any(a.get("generation_wave") != 6 and a["sha256"] == sha for a in active), "Historical asset incorrectly logged as new generation"
        review = next((r for r in reversed(reviews) if r.get("entity_id") == owner and r.get("sha256") == sha), None)
        if args.apply and (not review or not review.get("reviewed_utc")):
            raise ValueError("SHA-bound QA missing: " + owner)
        metrics = review.get("image_metrics") if review else None
        metrics = metrics or v4.inspect_png(source)
        notes = review.get("notes", []) if review else ["Inspection visuelle en attente."]
        assert isinstance(notes, list) and all(isinstance(note, str) for note in notes), "QA notes must be a list of strings"
        destination, asset_id = destination_for(owner, expected_scope, sha, active, reserved)
        candidate = copy.deepcopy(record)
        candidate.pop("status", None)
        candidate.pop("error", None)
        candidate.pop("output_hint", None)
        candidate.update({"id": asset_id, "entity_id": owner, "type": "fighter_pose" if kind == "fighter" else "expansion_character_pose", "roster_scope": "base" if kind == "fighter" else "expansion", "output": destination.name, "path": destination.relative_to(PROJECT).as_posix(), "source_path": str(source), "sha256": sha, "generation_wave": 6, "source_journal": journal_rel, "journal_record": index, "status": "candidate", "fidelity_status": "not_certified", "animation_status": "not_animated", "integration_status": "not_integrated", "qa": " ".join(notes), "visual_review_status": "reviewed_candidate_requires_correction" if review and review.get("verdict") == "candidate_requires_correction" else "reviewed_candidate_with_reservations" if review else "pending_visual_review", "required_followup": list(dict.fromkeys((review.get("required_followup", []) if review else []) + ["Validation de fidélité aux références du jeu", "Animations et déclinaisons", "Collisions et intégration au moteur"])), **metrics})
        if review:
            candidate["visual_review"] = review
        candidate["target_facing"] = record.get("target_facing", "right")
        candidate["observed_facing"] = review.get("observed_facing", "not_recorded") if review else "not_recorded"
        old_index = next((i for i, a in enumerate(active) if a["id"] == asset_id), None)
        if old_index is None:
            active.append(candidate)
            added.append(asset_id)
        else:
            assert active[old_index].get("generation_wave") == 6
            active[old_index] = candidate
        plans.append({"asset_id": asset_id, "entity_id": owner, "source": str(source), "destination": str(destination), "sha256": sha})
    for failure in failures:
        old = next((f for f in manifest["failed_requests"] if f.get("generation_wave") == 6 and f.get("journal_record") == failure["journal_record"] and f.get("source_journal") == journal_rel), None)
        if old is None:
            manifest["failed_requests"].append(failure)
        else:
            assert old == failure, "Consolidated failure changed"
    by_id = {a["id"]: a for a in active}
    reused = []
    for entry in entries:
        assets = [a for a in active if a["type"] == "expansion_character_pose" and a["entity_id"] == entry["id"]]
        entry["new_visual_assets"] = [a["id"] for a in assets]
        if entry.get("reused_visual_asset"):
            assert not assets and entry.get("generation_required") is False, "Reused catalog entry was generated again"
            assert entry["id"] == "warden_eternal_h5" and entry["reused_visual_asset"] == "boss_warden_h5_profile_v01", "Unexpected visual reuse"
            asset = by_id[entry["reused_visual_asset"]]
            assert asset.get("generation_wave") == 5 and asset["entity_id"] == "boss_warden_h5"
            entry["visual_reuse"] = {"asset_id": asset["id"], "source_entity_id": asset["entity_id"], "path": asset["path"], "sha256": asset["sha256"], "generation_wave": 5, "new_generation": False, "observed_facing": "left", "target_facing": "not_applicable_prior_reuse", "horizontal_mirror_performed": False}
            entry["visual_assets"] = [asset["id"]]
            entry["preferred_visual_asset"] = asset["id"]
            entry["art_status"] = "candidate_reused"
            reused.append(entry["id"])
        else:
            entry["visual_assets"] = [a["id"] for a in assets]
            best = preferred(assets)
            if best:
                entry["preferred_visual_asset"] = best["id"]
            else:
                entry.pop("preferred_visual_asset", None)
            entry["art_status"] = "candidate" if best else "candidate_requires_correction" if assets else "not_generated"
        entry.update({"fidelity_status": "not_certified", "animation_status": "not_animated", "integration_status": "not_integrated", "gameplay_design_status": "proposed_not_implemented"})
    chief = next(f for f in roster["fighters"] if f["id"] == "chief_infinite")
    chief_guards = [a for a in active if a.get("entity_id") == "chief_infinite" and a.get("pose_scope") == "guard_static"]
    if chief_guards:
        best_guard = preferred(chief_guards, chief.get("preferred_guard_asset"))
        chief.update({"guard_visual_assets": [a["id"] for a in chief_guards], "guard_art_status": "candidate" if best_guard else "candidate_requires_correction"})
        if best_guard:
            chief["preferred_guard_asset"] = best_guard["id"]
        else:
            chief.pop("preferred_guard_asset", None)
    wave = [a for a in active if a.get("generation_wave") == 6]
    fassets = [a for a in active if a["type"] == "fighter_pose"]
    gassets = [a for a in fassets if a.get("pose_scope") == "guard_static"]
    extassets = [a for a in active if a["type"] == "expansion_character_pose"]
    covered = [e for e in entries if e["visual_assets"]]
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    counts.update({"active_visual_candidates": len(active), "active_fighter_pose_candidates": len(fassets), "active_guard_pose_candidates": len(gassets), "fighter_entities_with_guard_candidate": len({a["entity_id"] for a in gassets}), "fighter_entities_without_guard_candidate": 24-len({a["entity_id"] for a in gassets}), "active_expansion_character_pose_candidates": len(extassets), "expansion_catalog_entries": len(entries), "expansion_catalog_entries_with_visual": len(covered), "expansion_catalog_entries_without_visual": len(entries)-len(covered), "expansion_catalog_entries_with_new_visual": sum(bool(e["new_visual_assets"]) for e in entries), "expansion_catalog_entries_with_reused_visual": len(reused), "character_catalog_total_entries_including_base": 24+len(entries), "character_catalog_entities_with_visual_including_base": 24+len(covered), "visual_candidates_pre_wave6": baseline["candidate_count"], "wave6_generation_attempts": len(records), "wave6_successful_generation_attempts": sum(not v4.is_failure(r) for r in records), "wave6_generation_failures": len(failures), "wave6_automatic_generation_rejections": sum("moderation_blocked" in str(f.get("error", "")) for f in failures), "wave6_generated_pngs": len(wave), "wave6_generated_expansion_pngs": sum(a["type"] == "expansion_character_pose" for a in wave), "wave6_generated_guard_pngs": sum(a.get("pose_scope") == "guard_static" for a in wave), "wave6_unique_expansion_entities_with_new_candidates": len({a["entity_id"] for a in wave if a["type"] == "expansion_character_pose"}), "wave6_expansion_entries_reusing_prior_asset": len(reused), "historical_generation_failures_all_waves": len(manifest["failed_requests"]), "updated_utc": stamp})
    counts.update({"expansion_catalog_entries_with_preferred_visual": sum(bool(e.get("preferred_visual_asset")) for e in entries), "expansion_catalog_entries_requiring_correction_only": sum(e["art_status"] == "candidate_requires_correction" for e in entries)})
    counts.update(design_counts(entries))
    manifest.update({"updated_utc": stamp, "generated_unique_entities": len({v4.entity_id(a) or a["id"] for a in active}), "generated_guard_entities": len({a["entity_id"] for a in gassets}), "generated_expansion_entities": len({a["entity_id"] for a in extassets}), "illustrated_expansion_catalog_entries": len(covered)})
    catalog = {"schema_version": 1, "project": "Halo Combats", "language": "fr", "updated_utc": stamp, "scope": "34 named/class entries already proposed in the expansion backlog; art catalog, not automatic activation in the base gameplay roster", "base_fighter_count": 24, "source_catalogs": catalog_inputs, "entries": entries, "unresolved_continuity_backlog": [e for e in roster["expansions"] if e.get("category") == "Autres continuités"], "fidelity_status": "not_certified"}
    summary = {"generation_wave": 6, "updated_utc": stamp, "journal_sha256": file_guards[JOURNAL], "record_sha256": hashes, "catalog_inputs": catalog_inputs, "counts": counts, "new_candidate_assets_this_run": len(added), "new_candidate_ids_this_run": added, "planned_files": plans, "failed_attempts_in_journal": failures, "duplicate_records_skipped": duplicates, "reused_prior_catalog_entries": reused, "expansion_entries_without_visual": [e["id"] for e in entries if not e["visual_assets"]], "guard_fighters_without_candidate": [f["id"] for f in roster["fighters"] if not any(a["entity_id"] == f["id"] for a in gassets)], "applied": args.apply}
    readme, report, sources, base_csv, extension_csv = make_outputs(entries, active, records, summary, counts, old_base_rows, roster, manifest["failed_requests"])
    if args.apply:
        assert all(digest(p) == sha for p, sha in file_guards.items()), "Inputs changed during consolidation"
        for plan in plans:
            destination = Path(plan["destination"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.exists():
                shutil.copyfile(plan["source"], destination)
            assert digest(destination) == plan["sha256"], "Copy differs"
        for path, value in [(MANIFEST, manifest), (FIGHTERS, roster), (COUNTS, counts), (CATALOG, catalog), (SUMMARY, summary)]:
            write_atomic(path, json_text(value))
        for path, value in [(PROJECT/"README.md", readme), (PROJECT/"README_V6.md", readme), (REPORT, report), (SOURCES, sources), (BASE_CSV, base_csv), (EXTENSION_CSV, extension_csv)]:
            write_atomic(path, value)
    print(json_text({"applied": args.apply, "attempts": len(records), "new_assets_this_run": len(added), "wave6_pngs": len(wave), "extension_entries": len(entries), "extensions_with_visual": len(covered), "reused_entries": len(reused), "base_guards": counts["fighter_entities_with_guard_candidate"], "total_candidates": len(active), "failures_all_waves": len(manifest["failed_requests"])}))


if __name__ == "__main__":
    main()
