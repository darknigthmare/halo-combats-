#!/usr/bin/env python3
"""Archive les personnages Halo Combats V2, après update_wave2.py --apply.

Utilisation, uniquement après consolidation :
    python3 work/wave2/package_characters.py

Ne génère ni ne retouche aucune image. Les nombres sont recalculés à partir du
roster, du journal, du manifeste et des octets effectivement placés dans le ZIP.
Le script utilise exclusivement la bibliothèque standard Python.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import struct
import sys
import tempfile
import zipfile


PROJECT = Path(__file__).resolve().parents[2]
ARCHIVE_NAME = "HALO_COMBATS_PERSONNAGES_V2.zip"
ARCHIVE_ROOT = "Halo_Combats_Personnages_V2"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
REQUIRED_FILES = (
    "data/fighters.json",
    "data/asset_manifest.json",
    "data/fighter_sources.json",
    "data/animation_plan.json",
    "data/characters_visual_inventory.csv",
    "docs/HALO_COMBATS_PERSONNAGES_V2.md",
    "work/wave2/human_prompts.json",
    "work/wave2/alien_prompts.json",
    "work/wave2/generation_results.json",
    "work/wave2/qa_wave2.json",
    "work/wave2/consolidation_summary.json",
    "work/wave2/update_wave2.py",
    "work/wave2/package_characters.py",
)
OPTIONAL_FILES = (
    "work/wave2/neutral_reference_prompts.json",
    "docs/source_registry.json",
    "work/roster/source_registry.json",
    "data/animation_plan.csv",
    "data/delivery_counts.json",
    "docs/ETAT_PRODUCTION_V2.md",
    "docs/HALO_COMBATS_PRODUCTION_V2.xlsx",
    "docs/HALO_COMBATS_PERSONNAGES_V2.xlsx",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def as_records(value: object, key: str) -> list[dict]:
    records = value.get(key) if isinstance(value, dict) else value
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError(f"Format invalide : liste de fiches attendue pour {key}.")
    return records


def entity_id(record: dict) -> str:
    return str(record.get("entity_id") or record.get("fighter_id") or record.get("id") or "")


def is_failure(record: dict) -> bool:
    status = str(record.get("status", "")).lower()
    return bool(record.get("error")) or any(
        token in status for token in ("fail", "error", "reject", "block")
    )


def failure_kind(record: dict) -> str:
    text = json.dumps(record, ensure_ascii=False).lower()
    if "moderation_blocked" in text or "moderation rejection" in text:
        return "automatic_moderation_rejection"
    return "generation_error"


def failure_label(record: dict) -> str:
    if failure_kind(record) == "automatic_moderation_rejection":
        category = " ; catégorie « other »" if "other" in str(record.get("error", "")).lower() else ""
        return f"Refus automatique — moderation_blocked{category} ; motif précis non fourni."
    return "Échec de génération ; détail technique conservé dans le journal."


def md(value: object) -> str:
    return str(value).replace("|", "/").replace("\r", " ").replace("\n", " ")


def pose_intent(candidate: dict, journal: list[dict]) -> str:
    """Classe le brief demandé, sans prétendre inspecter le résultat visuel."""
    index = candidate.get("journal_record")
    record = journal[index] if isinstance(index, int) and 0 <= index < len(journal) else {}
    if record and entity_id(record) != entity_id(candidate):
        raise ValueError(f"Lien de journal incohérent pour {entity_id(candidate)}.")
    kind = str(record.get("attempt_kind") or candidate.get("attempt_kind") or "").lower()
    if kind == "neutral_unarmed":
        return "unarmed_neutral_reference_requested"
    prompt = str(record.get("prompt") or candidate.get("prompt") or "").lower()
    if any(token in prompt for token in ("no weapons", "empty hands", "unarmed")):
        return "unarmed_neutral_reference_requested"
    if record and prompt:
        return "armed_character_pose_requested"
    return "pose_intent_not_classified"


def pose_label(value: str) -> str:
    return {
        "unarmed_neutral_reference_requested": "Référence neutre sans arme demandée",
        "armed_character_pose_requested": "Pose armée demandée",
        "pose_intent_not_classified": "Type de pose à vérifier",
    }[value]


def readme_text(summary: dict, inventory: list[dict], failures: list[dict]) -> str:
    lines = [
        "# Halo Combats — personnages V2",
        "",
        f"Archive constituée le {summary['created_utc']}.",
        "",
        "Cette livraison rassemble les images de combattants réellement obtenues, leurs prompts, leurs références et le suivi de production. Elle comprend des poses candidates issues de briefs armés et des références neutres sans arme. **Ces images ne sont pas toutes des poses de combat prêtes à intégrer** ; leur présence ne signifie pas qu'un personnage jouable complet est terminé.",
        "",
        "## Résultat réel de cette livraison",
        "",
        "| Indicateur | Nombre |",
        "|---|---:|",
        f"| Combattants distincts du roster | {summary['roster_count']} |",
        f"| Fichiers images de combattants dans cette archive | {summary['fighter_image_file_count']} |",
        f"| Personnages possédant au moins une image candidate | {summary['fighter_entities_with_images']} |",
        f"| Personnages restant sans image candidate | {summary['fighter_entities_without_images_count']} |",
        f"| Fichiers candidats issus de la vague 2 | {summary['wave2_image_file_count']} |",
        f"| Fichiers candidats antérieurs conservés | {summary['prior_image_file_count']} |",
        f"| Images issues d'un brief de pose armée | {summary['armed_pose_request_image_count']} |",
        f"| Images issues d'un brief neutre sans arme | {summary['unarmed_neutral_request_image_count']} |",
        f"| Images dont le type de brief reste non classé | {summary['unclassified_pose_request_image_count']} |",
        f"| Tentatives consignées dans le journal de la vague 2 | {summary['wave2_journal_record_count']} |",
        f"| Identifiants de personnages distincts tentés dans la vague 2 | {summary['wave2_attempted_entity_count']} |",
        f"| Tentatives de la vague 2 avec la variante neutre sans arme | {summary['wave2_neutral_unarmed_attempt_count']} |",
        f"| Refus automatiques consignés dans cette vague | {summary['wave2_moderation_rejection_count']} |",
        f"| Personnages distincts ayant au moins un refus dans cette vague | {summary['wave2_refused_entity_count']} |",
        f"| Autres échecs consignés dans cette vague | {summary['wave2_other_error_count']} |",
        f"| Refus automatiques historiques antérieurs à cette vague | {summary['prior_moderation_rejection_count']} |",
        f"| Personnages actuellement présents malgré un refus historique | {len(summary['entities_present_despite_refusals'])} |",
        f"| Personnages actuellement manquants avec un refus historique | {len(summary['missing_entities_with_historical_refusal'])} |",
        f"| Prompts de base préparés dans les fichiers humains et aliens | {summary['prepared_base_prompt_count']} |",
        f"| Variantes de prompts neutres préparées | {summary['prepared_neutral_prompt_count']} |",
        f"| Personnages distincts couverts par les prompts | {summary['prepared_unique_fighter_prompt_count']} |",
        f"| Poses marquées certifiées dans le manifeste | {summary['certified_pose_count_in_manifest']} |",
        f"| Poses marquées animées dans le manifeste | {summary['animated_pose_count_in_manifest']} |",
        f"| Poses marquées intégrées au moteur dans le manifeste | {summary['integrated_pose_count_in_manifest']} |",
        "",
        "Les comptes séparent les tentatives, les identifiants distincts, l'historique des refus et les images présentes maintenant. Plusieurs tentatives peuvent concerner un même personnage. **Une réussite après un refus compte comme une image présente**, et non comme un personnage encore manquant. Les refus restent dans l'historique sans être convertis en réussites.",
        "",
        "La distinction armée / neutre décrit le brief de génération et reste à confronter à l'image et à sa QA. Une référence neutre sans arme aide à contrôler le personnage ; elle ne remplace pas une garde de combat, l'arme dédiée, les attaques ni les animations.",
        "",
        "## Limites de production",
        "",
    ]
    if summary["certified_pose_count_in_manifest"] == 0:
        lines.append("**Aucune fidélité 1:1 n'est certifiée.** Les armures, armes, proportions, asymétries, silhouettes et versions de jeu demandent encore une validation comparative sur les références de chaque épisode.")
    else:
        lines.append("Les statuts de fidélité déclarés dans le manifeste sont reproduits dans l'inventaire. L'archivage contrôle les fichiers, pas la fidélité visuelle : il ne constitue pas une nouvelle certification 1:1.")
    lines.append("")
    if summary["animated_pose_count_in_manifest"] == 0:
        lines.append("**Aucun jeu d'animations de combattant n'est livré.** Les images sont des poses statiques. Les mouvements, attaques, réactions, transitions, finishers et deux orientations corrigées restent à produire. Le plan d'animation décrit un travail prévu, pas des sprites déjà dessinés.")
    else:
        lines.append("Cette archive de personnages contient des images de poses et le plan d'animation ; elle ne prétend pas fournir un jeu complet d'animations. Les statuts déclarés sont conservés dans l'inventaire.")
    lines += [
        "",
        "L'intégration au moteur, les collisions, les hitboxes et le contrôle en jeu restent des étapes distinctes. Les réserves de cadrage, de profil et de détourage figurent dans le suivi Markdown et les rapports de QA. Un canal alpha présent ne garantit pas, à lui seul, un contour prêt pour la production.",
        "",
        "Les images sont archivées sans retouche, recadrage, redimensionnement ou recompression de leurs octets. La définition native de chaque fichier est indiquée dans l'inventaire ; la mention UHD dans un prompt n'est pas une mesure de la résolution obtenue.",
        "",
        "## Fichiers réellement disponibles, personnage par personnage",
        "",
        "| Personnage | ID | Images incluses | Fichiers | Types demandés | État actuel |",
        "|---|---|---:|---|---|---|",
    ]
    for row in inventory:
        paths = "; ".join(f"`{md(a['path'])}`" for a in row["images"]) or "—"
        kinds = "; ".join(sorted({pose_label(a["pose_intent"]) for a in row["images"]})) or "—"
        state = ("Présent malgré refus historique ; validation requise" if row["historical_moderation_rejections"] else "Présent ; validation requise") if row["images"] else (
            "Toujours sans image ; refus automatique historique" if row["historical_moderation_rejections"] else
            "Sans image ; échec consigné" if row["failed_records"] else
            "Sans image ; aucune tentative consignée dans cette vague"
        )
        lines.append(f"| {md(row['name'])} | `{md(row['entity_id'])}` | {len(row['images'])} | {paths} | {kinds} | {state} |")
    lines += ["", "## Refus et autres échecs de la vague 2", ""]
    if failures:
        lines.append("Les refus ci-dessous sont des réponses du service de génération. La catégorie « other », lorsqu'elle est fournie, n'indique pas une cause précise ; aucune cause supplémentaire n'est supposée. Aucun fichier image n'a été fourni pour ces tentatives.")
        lines.append("")
        for failure in failures:
            present = next(row for row in inventory if row["entity_id"] == entity_id(failure))["images"]
            current = "Image désormais présente grâce à une autre tentative." if present else "Personnage toujours sans image candidate."
            variant = "variante neutre sans arme" if failure.get("attempt_kind") == "neutral_unarmed" else "brief initial"
            lines.append(f"- Entrée {failure['journal_record'] + 1}, `{md(entity_id(failure))}` ({variant}) : {failure_label(failure)} {current}")
    else:
        lines.append("Aucun échec n'est consigné dans le journal de cette vague.")
    lines += [
        "",
        f"L'historique antérieur à cette vague comporte {summary['prior_failed_record_count']} entrée(s) en échec, dont {summary['prior_moderation_rejection_count']} refus automatique(s). Ces entrées restent dans `data/asset_manifest.json` et dans `data/package_failure_history.json` ; elles ne sont pas ajoutées une deuxième fois aux comptes de la vague 2. Un refus plus ancien ne définit pas l'état actuel du personnage.",
        "",
        "## Organisation de l'archive",
        "",
        "- `assets/` : tous les fichiers candidats de combattants présents dans le manifeste consolidé, y compris la pose de l'Arbiter héritée de V1 lorsqu'elle est disponible.",
        "- `work/wave2/human_prompts.json` et `alien_prompts.json` : prompts, verrous visuels et références des personnages manquants.",
        "- `work/wave2/neutral_reference_prompts.json`, s'il est présent : variantes de références neutres sans arme ; les armes citées dans les verrous d'identité restent des références du personnage, pas une promesse de présence dans ces variantes.",
        "- `docs/HALO_COMBATS_PERSONNAGES_V2.md` : suivi de couverture et réserves par personnage.",
        "- `data/package_status.json` et `package_fighter_inventory.json` : comptes recalculés et inventaire des fichiers réellement placés dans ce ZIP.",
        "- `data/package_fighter_inventory.csv` : le même inventaire dans un tableau simple.",
        "- `data/package_failure_history.json` : refus et autres échecs, séparés entre historique antérieur et vague 2, avec l'état actuel de disponibilité des images.",
        "- `data/asset_manifest.json`, `fighters.json` et `characters_visual_inventory.csv` : données de statut consolidées.",
        "- `data/fighter_sources.json` et registres de sources disponibles : références et portée des vérifications.",
        "- `work/wave2/generation_results.json`, `qa_wave2.json` et `consolidation_summary.json` : journal des tentatives, observations sur les images et résultat de consolidation.",
        "- `data/animation_plan.json` et son CSV, s'il est présent : plan de travail des animations.",
        "- `SHA256SUMS.txt` : empreintes de tous les autres fichiers de l'archive, avec chemins relatifs.",
        "",
        "Le manifeste général peut mentionner des décors et boss produits dans V1 : leurs images ne font pas partie de cette archive centrée sur les combattants. Les anciens chemins absolus `source_path` sont conservés à titre de provenance ; utiliser les chemins relatifs `path` pour ouvrir les fichiers livrés.",
        "",
        "## Reproductibilité",
        "",
        "Les scripts de consolidation et d'archivage sont inclus. L'archive vérifie les empreintes des candidats, leur appartenance au roster et la présence du suivi consolidé, puis contrôle les CRC et les octets du ZIP. Elle ne transforme aucun refus en réussite et ne crée aucune image de remplacement.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--force", action="store_true", help="Remplacer une archive de même nom déjà présente.")
    args = parser.parse_args()
    project = args.project_root.resolve()
    output = (args.output_dir or project.parent / "outputs" / "halo_combats_v2").resolve()
    archive_path = output / ARCHIVE_NAME
    if archive_path.exists() and not args.force:
        raise FileExistsError(f"Archive déjà présente : {archive_path}. Utiliser --force pour la remplacer.")

    payloads: dict[str, bytes] = {}
    source_paths: dict[str, Path] = {}

    def snapshot(relative: str, required: bool = True) -> bytes | None:
        path = (project / relative).resolve()
        if not path.is_relative_to(project):
            raise ValueError(f"Chemin hors du projet : {relative}")
        if not path.is_file():
            if required:
                raise FileNotFoundError(f"Fichier requis absent : {path}. Exécuter d'abord update_wave2.py --apply après le lot de générations.")
            return None
        relative = path.relative_to(project).as_posix()
        if relative not in payloads:
            payloads[relative] = path.read_bytes()
            source_paths[relative] = path
        return payloads[relative]

    for relative in REQUIRED_FILES:
        snapshot(relative)
    for relative in OPTIONAL_FILES:
        snapshot(relative, required=False)

    def parsed(relative: str) -> object:
        return json.loads(payloads[relative].decode("utf-8-sig"))

    fighters = as_records(parsed("data/fighters.json"), "fighters")
    ids = [str(f.get("id", "")) for f in fighters]
    if not all(ids) or len(ids) != len(set(ids)):
        raise ValueError("Le roster comporte des identifiants absents ou dupliqués.")
    known = set(ids)
    manifest = parsed("data/asset_manifest.json")
    if not isinstance(manifest, dict):
        raise ValueError("Le manifeste doit être un objet JSON.")
    candidates = [c for c in as_records(manifest, "active_candidates") if c.get("type") == "fighter_pose"]
    journal = as_records(parsed("work/wave2/generation_results.json"), "results")
    consolidation = parsed("work/wave2/consolidation_summary.json")
    prompts = as_records(parsed("work/wave2/human_prompts.json"), "prompts") + as_records(parsed("work/wave2/alien_prompts.json"), "prompts")
    prompt_ids = [entity_id(p) for p in prompts]
    if len(prompt_ids) != len(set(prompt_ids)) or any(p not in known for p in prompt_ids):
        raise ValueError("Les prompts comportent des identifiants dupliqués ou hors roster.")
    neutral_path = "work/wave2/neutral_reference_prompts.json"
    neutral_prompts = as_records(parsed(neutral_path), "prompts") if neutral_path in payloads else []
    neutral_ids = [entity_id(p) for p in neutral_prompts]
    if len(neutral_ids) != len(set(neutral_ids)) or any(p not in known for p in neutral_ids):
        raise ValueError("Les prompts neutres comportent des identifiants dupliqués ou hors roster.")
    all_prompt_ids = set(prompt_ids) | set(neutral_ids)
    failures = []
    for index, record in enumerate(journal):
        if entity_id(record) not in known:
            raise ValueError(f"Entrée de journal hors roster : {entity_id(record)!r}")
        if is_failure(record):
            failures.append({**record, "journal_record": index})
    if not isinstance(consolidation, dict) or len(consolidation.get("failed_attempts_in_journal", [])) != len(failures):
        raise ValueError("Le journal et la consolidation ne correspondent plus. Rejouer update_wave2.py --apply avant l'archivage.")
    # Le manifeste conserve aussi les refus V1. Les copies des entrées de vague 2
    # déjà présentes dans le journal ne doivent pas être comptées deux fois.
    prior_failures = [
        record for record in manifest.get("failed_requests", [])
        if isinstance(record, dict) and entity_id(record) in known
        and str(record.get("generation_wave", "")) != "2"
    ]

    assets = []
    occupied_paths: set[str] = set()
    content_owners: dict[str, str] = {}
    for candidate in candidates:
        owner = entity_id(candidate)
        if owner not in known:
            raise ValueError(f"Candidat hors roster : {owner!r}")
        raw_path = candidate.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            raise ValueError(f"Chemin de candidat absent pour {owner}.")
        path = (project / raw_path).resolve()
        if not path.is_relative_to(project) or path.suffix.lower() not in IMAGE_SUFFIXES:
            raise ValueError(f"Chemin d'image invalide pour {owner} : {raw_path}")
        relative = path.relative_to(project).as_posix()
        if relative in occupied_paths:
            raise ValueError(f"Un fichier est référencé plusieurs fois : {relative}")
        occupied_paths.add(relative)
        data = snapshot(relative)
        assert data is not None
        digest = sha256(data)
        if candidate.get("sha256") and candidate["sha256"] != digest:
            raise ValueError(f"Empreinte différente du manifeste : {relative}")
        if digest in content_owners and content_owners[digest] != owner:
            raise ValueError(f"Les mêmes octets ont été attribués à deux personnages : {owner} / {content_owners[digest]}")
        content_owners[digest] = owner
        width, height = candidate.get("width"), candidate.get("height")
        if path.suffix.lower() == ".png":
            if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data) < 24 or data[12:16] != b"IHDR":
                raise ValueError(f"Le fichier n'est pas un PNG valide : {relative}")
            width, height = struct.unpack(">II", data[16:24])
        assets.append({
            "asset_id": candidate.get("id"), "entity_id": owner, "path": relative,
            "sha256": digest, "bytes": len(data), "width": width, "height": height,
            "generation_wave": candidate.get("generation_wave", 1),
            "pose_intent": pose_intent(candidate, journal),
            "fidelity_status": candidate.get("fidelity_status", "not_certified"),
            "animation_status": candidate.get("animation_status", "not_animated"),
            "integration_status": candidate.get("integration_status", "not_integrated"),
            "visual_review_status": candidate.get("visual_review_status", "not_reviewed_in_wave2"),
            "qa": candidate.get("qa", ""),
        })

    # Les dossiers de personnages ne doivent pas dissimuler une sortie oubliée
    # du manifeste. On refuse l'archive plutôt que de lui inventer un propriétaire.
    for directory in (project / "assets/characters_wave2", project / "assets/characters"):
        if directory.is_dir():
            for path in directory.rglob("*"):
                if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
                    relative = path.resolve().relative_to(project).as_posix()
                    if relative not in occupied_paths:
                        raise ValueError(f"Image de personnage non consolidée : {relative}. Mettre à jour le manifeste avant l'archive.")

    # Toute réussite du journal doit avoir une copie consolidée, byte-identique.
    for index, record in enumerate(journal):
        if is_failure(record):
            continue
        owner = entity_id(record)
        matches = [a for a, c in zip(assets, candidates) if a["entity_id"] == owner and (
            c.get("journal_record") == index or c.get("source_path") == record.get("source_path")
        )]
        if not matches:
            raise ValueError(f"Réussite du journal non retrouvée dans les candidats consolidés : entrée {index + 1}, {owner}.")
        raw_source = record.get("source_path")
        if raw_source and Path(raw_source).is_file():
            digest = sha256(Path(raw_source).read_bytes())
            if not any(a["sha256"] == digest for a in matches):
                raise ValueError(f"La copie consolidée diffère de la génération : {owner}.")

    by_id = {fid: [a for a in assets if a["entity_id"] == fid] for fid in ids}
    missing = [fid for fid in ids if not by_id[fid]]
    if consolidation.get("fighter_candidate_asset_count") != len(assets) or consolidation.get("fighter_entities_with_candidates") != len(ids) - len(missing):
        raise ValueError("Les comptes de consolidation et les fichiers présents diffèrent. Rejouer la consolidation.")
    historical_failures = prior_failures + failures
    attempted_ids = {entity_id(r) for r in journal}
    refused_ids = {entity_id(r) for r in failures if failure_kind(r) == "automatic_moderation_rejection"}
    historically_refused_ids = {entity_id(r) for r in historical_failures if failure_kind(r) == "automatic_moderation_rejection"}
    inventory = [{
        "entity_id": f["id"], "name": f.get("name", f["id"]), "era": f.get("era", ""),
        "images": by_id[f["id"]], "prepared_prompt": f["id"] in all_prompt_ids,
        "prepared_base_prompt": f["id"] in prompt_ids,
        "prepared_neutral_prompt": f["id"] in neutral_ids,
        "journal_records": sum(entity_id(r) == f["id"] for r in journal),
        "failed_records": sum(entity_id(r) == f["id"] for r in failures),
        "moderation_rejections": sum(entity_id(r) == f["id"] and failure_kind(r) == "automatic_moderation_rejection" for r in failures),
        "historical_moderation_rejections": sum(entity_id(r) == f["id"] and failure_kind(r) == "automatic_moderation_rejection" for r in historical_failures),
        "currently_present": bool(by_id[f["id"]]),
        "currently_present_despite_refusal": bool(by_id[f["id"]]) and f["id"] in historically_refused_ids,
    } for f in fighters]
    summary = {
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "archive_name": ARCHIVE_NAME,
        "roster_count": len(fighters),
        "fighter_image_file_count": len(assets),
        "fighter_entities_with_images": len(ids) - len(missing),
        "fighter_entities_without_images_count": len(missing),
        "fighter_entities_without_images": missing,
        "wave2_image_file_count": sum(a["generation_wave"] == 2 for a in assets),
        "prior_image_file_count": sum(a["generation_wave"] != 2 for a in assets),
        "armed_pose_request_image_count": sum(a["pose_intent"] == "armed_character_pose_requested" for a in assets),
        "unarmed_neutral_request_image_count": sum(a["pose_intent"] == "unarmed_neutral_reference_requested" for a in assets),
        "unclassified_pose_request_image_count": sum(a["pose_intent"] == "pose_intent_not_classified" for a in assets),
        "wave2_journal_record_count": len(journal),
        "wave2_attempted_entity_count": len(attempted_ids),
        "wave2_attempted_entity_ids": [fid for fid in ids if fid in attempted_ids],
        "wave2_neutral_unarmed_attempt_count": sum(r.get("attempt_kind") == "neutral_unarmed" for r in journal),
        "wave2_initial_attempt_count": sum(r.get("attempt_kind") != "neutral_unarmed" for r in journal),
        "wave2_failed_record_count": len(failures),
        "wave2_moderation_rejection_count": sum(failure_kind(r) == "automatic_moderation_rejection" for r in failures),
        "wave2_refused_entity_count": len(refused_ids),
        "wave2_refused_entity_ids": [fid for fid in ids if fid in refused_ids],
        "wave2_other_error_count": sum(failure_kind(r) == "generation_error" for r in failures),
        "wave2_successful_record_count": len(journal) - len(failures),
        "prior_failed_record_count": len(prior_failures),
        "prior_moderation_rejection_count": sum(failure_kind(r) == "automatic_moderation_rejection" for r in prior_failures),
        "historical_moderation_rejection_count": sum(failure_kind(r) == "automatic_moderation_rejection" for r in historical_failures),
        "historical_refused_entity_ids": [fid for fid in ids if fid in historically_refused_ids],
        "entities_present_despite_refusals": [fid for fid in ids if by_id[fid] and fid in historically_refused_ids],
        "missing_entities_with_historical_refusal": [fid for fid in missing if fid in historically_refused_ids],
        "missing_entities_not_attempted_this_wave": [fid for fid in missing if fid not in attempted_ids],
        "prepared_prompt_count": len(prompts) + len(neutral_prompts),
        "prepared_base_prompt_count": len(prompts),
        "prepared_neutral_prompt_count": len(neutral_prompts),
        "prepared_unique_fighter_prompt_count": len(all_prompt_ids),
        "prepared_human_prompt_count": len(as_records(parsed("work/wave2/human_prompts.json"), "prompts")),
        "prepared_alien_prompt_count": len(as_records(parsed("work/wave2/alien_prompts.json"), "prompts")),
        "certified_pose_count_in_manifest": sum(a["fidelity_status"] == "certified" for a in assets),
        "animated_pose_count_in_manifest": sum(a["animation_status"] == "animated" for a in assets),
        "integrated_pose_count_in_manifest": sum(a["integration_status"] == "integrated" for a in assets),
        "images_bytes": sum(a["bytes"] for a in assets),
        "source_files_preserved_byte_for_byte": True,
        "package_is_full_animation_set": False,
        "package_is_new_fidelity_certification": False,
    }
    readme = readme_text(summary, inventory, failures).encode("utf-8")
    payloads["README.md"] = readme
    payloads["data/package_status.json"] = json_bytes(summary)
    payloads["data/package_fighter_inventory.json"] = json_bytes(inventory)
    payloads["data/package_failure_history.json"] = json_bytes({
        "counting_rule": "Historique avant vague 2 plus journal de vague 2 ; aucune copie du journal dans le manifeste n'est recomptée. La disponibilité actuelle dépend seulement des fichiers candidats présents.",
        "previous_failures": [{
            **r, "currently_present": bool(by_id[entity_id(r)]),
            "failure_kind": failure_kind(r),
        } for r in prior_failures],
        "wave2_failures": [{
            **r, "currently_present": bool(by_id[entity_id(r)]),
            "failure_kind": failure_kind(r),
        } for r in failures],
    })
    table = io.StringIO(newline="")
    columns = ["entity_id", "name", "era", "image_count", "image_paths", "pose_intents", "prepared_prompt", "prepared_base_prompt", "prepared_neutral_prompt", "journal_records", "failed_records", "moderation_rejections", "historical_moderation_rejections", "currently_present", "currently_present_despite_refusal"]
    writer = csv.DictWriter(table, fieldnames=columns)
    writer.writeheader()
    for row in inventory:
        writer.writerow({**{key: row[key] for key in columns if key in row},
                         "image_count": len(row["images"]),
                         "image_paths": ";".join(a["path"] for a in row["images"]),
                         "pose_intents": ";".join(sorted({a["pose_intent"] for a in row["images"]}))})
    payloads["data/package_fighter_inventory.csv"] = ("\ufeff" + table.getvalue()).encode("utf-8")
    payloads["SHA256SUMS.txt"] = ("\n".join(f"{sha256(data)}  {name}" for name, data in sorted(payloads.items())) + "\n").encode("utf-8")

    # Une consolidation qui évolue pendant l'archivage invaliderait le résultat.
    for relative, path in source_paths.items():
        if not path.is_file() or sha256(path.read_bytes()) != sha256(payloads[relative]):
            raise RuntimeError(f"Fichier modifié pendant la préparation : {relative}. Reprendre après consolidation stable.")

    output.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(prefix="halo_characters_", suffix=".zip", dir=output, delete=False) as handle:
            temporary = Path(handle.name)
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            for relative, data in sorted(payloads.items()):
                archive.writestr(f"{ARCHIVE_ROOT}/{relative}", data)
        with zipfile.ZipFile(temporary) as archive:
            bad = archive.testzip()
            if bad:
                raise RuntimeError(f"Échec CRC dans l'archive : {bad}")
            if len(archive.namelist()) != len(payloads):
                raise RuntimeError("Nombre de fichiers ZIP incorrect.")
            for relative, data in payloads.items():
                if archive.read(f"{ARCHIVE_ROOT}/{relative}") != data:
                    raise RuntimeError(f"Octets altérés dans l'archive : {relative}")
        temporary.replace(archive_path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)

    (output / "HALO_COMBATS_PERSONNAGES_V2_README.md").write_bytes(readme)
    (output / "HALO_COMBATS_PERSONNAGES_V2_STATUS.json").write_bytes(json_bytes(summary))
    report = {**summary, "path": str(archive_path), "archive_file_count": len(payloads),
              "archive_bytes": archive_path.stat().st_size,
              "archive_sha256": sha256(archive_path.read_bytes()),
              "verification": "CRC ZIP et comparaison des octets de chaque fichier réussis"}
    (output / "HALO_COMBATS_PERSONNAGES_V2_PACKAGE_REPORT.json").write_bytes(json_bytes(report))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"Archivage interrompu : {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
