#!/usr/bin/env python3
"""Build the auditable V10 production snapshot. Does not generate or edit pixels."""
from __future__ import annotations
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATE = "2026-11-27"
INVENTORY = "https://support.halowaypoint.com/hc/en-us/articles/6882880281364-Halo-Infinite-Weapon-Equipment-and-Vehicle-Inventory"
CU32 = "https://support.halowaypoint.com/hc/en-us/articles/25897330878868-Halo-Infinite-Banished-Honor-Update-Patch-Notes"
CU32_SANDBOX = "https://www.halowaypoint.com/news/banished-honor-sandbox"
def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))
def write(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Identity summaries are short; timing, 2D units and damage below are original design proposals.
# id, name, category, source fact, visual lock, trajectory, lifetime frames, interaction
SPECS = [
 ("proj_frag_infinite","Grenade M9","projectile","Grenade à fragmentation avec rebond.",
  "M9 Infinite : coque olive segmentée, bande rouge, fusée haute ; ne pas reprendre la silhouette d’un autre opus.",
  "ballistic_bounce",90,"explosion après temporisation ; rebonds limités et traçables"),
 ("proj_plasma_grenade_infinite","Grenade à plasma","projectile","Grenade adhésive à plasma.",
  "Sphère bleu-violet segmentée d’Infinite ; conserver les ouvertures et le matériau, sans substituer un autre modèle.",
  "ballistic_sticky",90,"attachement à une hurtbox valide ; détonation après temporisation"),
 ("proj_spike_infinite","Grenade à pointes Jovokada","projectile","Grenade adhésive projetant des éclats.",
  "Modèle Infinite : manche gainé, tête métallique et pointes asymétriques ; pas de miroir du PNG.",
  "ballistic_sticky",360,"fusée démarrant au repos ; attachement puis émission d’éclats distincts, aucune explosion en plein vol"),
 ("proj_dynamo_infinite","Grenade dynamo","projectile","Grenade électrique pouvant neutraliser les véhicules.",
  "Verrouiller le modèle Infinite par captures avant toute génération ; effets électriques séparés du corps.",
  "ballistic_bounce",180,"champ périodique ; temporisation et intervalle de dégâts bornés"),
 ("proj_needler_shard_infinite","Aiguille du Needler","projectile","Cristaux guidés, accumulation puis supercombine.",
  "Cristal magenta facetté d’Infinite ; une aiguille, pointe à droite, courte traînée distincte de la hitbox.",
  "limited_homing",75,"compter les aiguilles par cible et source ; seuil paramétré"),
 ("vfx_needler_supercombine_infinite","Supercombine du Needler","vfx","Explosion liée à l’accumulation d’aiguilles.",
  "Explosion cristalline magenta ; événements de dégâts et pixels distincts, pas de réutilisation d’un autre opus.",
  "event_radial",18,"consommer une fois le compteur admissible ; effet lié à la cible"),
 ("proj_plasma_pistol_bolt_infinite","Pistolet à plasma · tir normal","projectile","Tir plasma ; surcharge disponible.",
  "Petite décharge verte Infinite, capture de départ/vol/impact à documenter.",
  "linear",60,"dégâts au bouclier et PV par table de combat originale"),
 ("proj_plasma_pistol_overcharge_infinite","Pistolet à plasma · surcharge","projectile","Surcharge ; EMP véhicule rétabli en CU32.",
  "Orbe vert de surcharge Infinite ; comportement EMP fixé au profil CU32 (30 avril 2024), distinct du lancement.",
  "limited_homing",75,"consommer la charge ; dégâts de bouclier et EMP temporaire sur véhicules admissibles"),
 ("proj_pulse_carbine_infinite","Carabine à impulsion · décharge","projectile","Rafales de plasma légèrement guidées.",
  "Une décharge de carabine Infinite ; les rafales sont des entités répétées, pas une planche collée.",
  "limited_homing",65,"chaque décharge a son identifiant ; limite de touche par salve"),
 ("proj_ravager_bolt_infinite","Ravageur · décharge","projectile","Plasma avec dégâts de zone.",
  "Plasma rouge du Ravageur Infinite ; matière et silhouette à verrouiller sur captures.",
  "ballistic",65,"dégât direct et zone sans double comptage"),
 ("proj_ravager_charged_infinite","Ravageur · charge","projectile","Charge laissant une zone persistante.",
  "Projectile chargé rouge distinct des tirs normaux ; ne pas confondre avec un canon à combustible.",
  "ballistic",90,"créer une seule zone au contact admissible ; ne pas importer le rebond de la variante Ravager Rebound"),
 ("vfx_ravager_pool_infinite","Ravageur · nappe de plasma","vfx","Zone de plasma persistante.",
  "Nappe rouge au sol ; raccord au sol réel, sans volume flottant ni décor inclus.",
  "ground_zone",180,"intervalle de dégâts par cible ; limite de zones simultanées"),
 ("proj_cindershot_infinite","Calcineur · orbe","projectile","Grenade de lumière solide, guidage alternatif.",
  "Lumière solide Infinite ; séparer orbe, traînée et détonation.",
  "ballistic_bounce",90,"mode guidé activé à l’émission ; contrôle limité ; aucune aspiration de la cible dans le profil CU32"),
 ("proj_heatwave_infinite","Vague de chaleur · particule","projectile","Six particules, dispersion verticale ou horizontale.",
  "Une particule orange de lumière solide ; six entités dans le patron de tir, sans aplat à six projectiles.",
  "linear_bounce",50,"plafond de rebonds et de contacts ; patron choisi avant émission"),
 ("proj_hydra_infinite","Hydra · micromissile","projectile","Micromissiles ; verrouillage ou tir direct.",
  "Missile physique Infinite entier ; moteur et traînée à produire séparément.",
  "limited_homing",100,"verrouillage explicite au départ ; perte de cible sans acquisition cachée"),
 ("proj_spnkr_infinite","SPNKr · roquette","projectile","Roquette explosive.",
  "Roquette Infinite et proportions à documenter ; aucune arme entière dans le sprite de projectile.",
  "linear",100,"explosion sur premier obstacle admissible ; pas de dégâts répétés"),
 ("proj_skewer_infinite","Empaleur · pointe","projectile","Grande pointe perforante.",
  "Long projectile métallique Infinite ; pointe complète et marges, sans inversion automatique.",
  "ballistic_fast",65,"collision balayée pour éviter de traverser une cible entre deux pas"),
 ("proj_disruptor_infinite","Disrupteur · décharge","projectile","Décharge électrique ; effet sur véhicules.",
  "Décharge électrique Infinite ; aspect exact à confirmer avec captures de gameplay.",
  "linear",50,"accumulation électrique séparée des dégâts ; effet véhicule réservé aux entités admissibles"),
 ("vfx_shock_rifle_infinite","Fusil électrique · décharge","vfx","Décharge électrique capable d’EMP.",
  "Tracé électrique du fusil Infinite ; garder la résolution de touche distincte du trait lumineux.",
  "instant_trace",8,"trace instantanée proposée ; arcs limités à des cibles admissibles"),
 ("vfx_sentinel_beam_infinite","Laser de sentinelle · faisceau","vfx","Faisceau continu.",
  "Faisceau du modèle Infinite ; origine, terminaison et occlusion à relier au porteur.",
  "continuous_beam",120,"durée maximale ; arrêt sur interruption, KO ou sortie du porteur"),
 ("proj_stalker_infinite","Fusil traqueur · décharge","projectile","Tir de plasma de précision.",
  "Décharge du fusil traqueur Infinite ; ne pas réutiliser le faisceau de sentinelle.",
  "linear_fast",35,"collision balayée ; consommation du tir sur obstacle"),
 ("proj_mangler_infinite","Déchiqueteur · pointe","projectile","Projectile métallique de type pointe.",
  "Munition du Déchiqueteur Infinite ; modèle à documenter indépendamment de l’arme.",
  "ballistic_fast",45,"chute légère proposée ; une touche au maximum"),
 ("proj_spike_shrapnel_infinite","Grenade à pointes · éclat","projectile","Éclats issus de la détonation.",
  "Un éclat métallique du modèle Infinite ; forme à capturer séparément du corps de grenade.",
  "linear_bounce",30,"patron issu de la normale de surface ; plafond global de dégâts par explosion"),
 ("vfx_gravity_hammer_infinite","Marteau antigravité · onde","vfx","Impulsion gravitationnelle.",
  "Onde et poussière séparées du marteau et du sol ; incarnation Infinite explicitement verrouillée.",
  "event_radial",15,"zone évaluée une fois ; aucun rayon infini, collision par distance et angle"),
]

REFS = {
 "proj_frag_infinite": ["https://www.halopedia.org/File:HINF_FragGrenade_Cutout.png"],
 "proj_plasma_grenade_infinite": ["https://www.halopedia.org/File:HINF_plasma_grenades.png"],
 "proj_spike_infinite": ["https://www.artstation.com/artwork/qQ0ENn", "https://www.halopedia.org/File:HINF_SpikeGrenade_HiPoly_Render_1.jpg"],
 "proj_needler_shard_infinite": ["https://www.halopedia.org/File:HINF_Needler_Firing.png"],
}

def projectile(row):
    ident, name, category, fact, lock, trajectory, lifetime, interaction = row
    attached = trajectory in {"ballistic_sticky", "ground_zone"}
    beam = trajectory == "continuous_beam"
    instant = trajectory in {"instant_trace", "event_radial"}
    return {
        "id": ident, "name": name, "category": category, "work_id": "infinite",
        "work_title": "Halo Infinite", "source_version": "Halo Infinite ; visuels de cet opus et profil sandbox CU32 du 30 avril 2024, sans certification de l’équilibrage courant",
        "medium": "game", "continuity": "core", "identity_fact": fact,
        "reference_urls": list(dict.fromkeys([*REFS.get(ident, []), INVENTORY, CU32, CU32_SANDBOX])),
        "visual_lock": lock,
        "visual_reference_status": "Référence visuelle inspectée ; candidat produit, vérification fine ouverte." if ident in REFS else "Comportement officiel repéré ; dossier visuel multi-vues à constituer.",
        "art_status": "missing", "asset_state": "not_produced", "assets": [],
        "preferred_asset_id": None, "related_entity_id": None,
        "implementation_status": "Spécification V10 ; collision et intégration au combat non implémentées.",
        "design_proposal": {
            "status": "specified_not_implemented",
            "basis": "Adaptation originale Halo Combats, pas des données extraites du moteur Halo.",
            "simulation_hz": 60, "trajectory": trajectory,
            "lifetime_frames_proposed": lifetime,
            "collision": "segment balayé + première intersection admissible" if "fast" in trajectory else "forme dédiée indépendante du PNG",
            "interaction": interaction,
            "damage_values": "à équilibrer dans la table de combat ; aucune valeur présentée comme canonique",
            "ownership": {"source_fighter_id": "immuable", "team_id": "immuable", "spawn_event_id": "unique", "target_id": "optionnel et validé", "damage_credit": "source d’émission, même après tag"},
            "tag_policy": "interrompre le faisceau lorsque le porteur sort" if beam else "résoudre l’événement déjà émis sans le réémettre" if instant else "persister après changement de combattant ; durée et attribution conservées",
            "ko_policy": "interrompre le faisceau" if beam else "ne pas ressusciter le propriétaire ; entité émise persiste jusqu’à sa fin normale",
            "round_policy": "vider toutes les entités et tous les compteurs en fin de round",
            "pause_policy": "geler âge, temporisations, déplacement et dégâts",
            "cinematic_policy": "geler la simulation et reprendre l’état, sans doublon au saut de cinématique",
            "attachment_policy": "suivre le point d’attache ; à disparition, terminer ou déposer selon règle explicite" if attached else "pas d’attache implicite",
            "friendly_fire": "désactivé dans le prototype proposé ; option de mode explicite",
            "netcode": "événements et RNG déterministes prévus ; aucun rollback réseau livré",
        },
        "required_frames": [{"name": n, "status": "not_produced"} for n in (["apparition", "maintien", "dissipation"] if category == "vfx" else ["vol", "impact", "dissipation"])],
        "notes": [
            fact + " Sources : inventaire officiel Halo Infinite, corrigé par les notes CU32 lorsque le comportement a changé.",
            "Profil documentaire daté CU32 (30 avril 2024) ; les variations postérieures et la campagne ne sont pas automatiquement confondues avec ce profil multijoueur.",
            "Paramètres 2D, durées et interactions de combat : propositions de design à implémenter puis tester.",
            "Le PNG disponible, lorsqu’il existe, est une pose statique ; aucune séquence ni collision jouable n’est déduite de sa présence.",
            "La continuité et l’opus restent fixés à Halo Infinite ; ne pas mélanger les comportements d’autres jeux.",
        ],
        "catalog_origin": "V10", "new_in_wave": True
    }

def main():
    data = copy.deepcopy(read("data/universe_catalog_v9.json"))
    previous = read("data/asset_manifest_v9.json")
    reviews = read("work/wave10/asset_reviews.json")
    additions = reviews["assets"] if isinstance(reviews, dict) else reviews
    entries = data["entries"]
    for entry in entries:
        entry["new_in_wave"] = False
    knight = next(e for e in entries if e["id"] == "knight_h4")
    knight.update(work_id="h4", work_title="Halo 4")
    knight["notes"].append("V10 : œuvre corrigée de Halo 5 vers Halo 4 ; l’exclusion «pas le modèle Halo 5» avait trompé l’ancien classement textuel.")
    projectiles = [projectile(row) for row in SPECS]
    spike = next(p for p in projectiles if p['id'] == 'proj_spike_infinite')
    spike['design_proposal']['fuse_start'] = 'at_rest_or_stuck'
    spike['design_proposal']['fuse_frames_proposed'] = 72
    spike['design_proposal']['lifetime_expiry'] = 'despawn_without_explosion_if_never_at_rest'
    spike['notes'].append('CU32 : fusée après immobilisation ; 1,2 seconde de référence, soit 72 pas à 60 Hz. La limite totale de 360 pas est une proposition de nettoyage du prototype.')
    needler = next(p for p in projectiles if p['id'] == 'proj_needler_shard_infinite')
    needler['design_proposal']['target_policy'] = 'living_combatants_only; no sticking or accumulation on vehicles or structures'
    needler['design_proposal']['attachment_policy'] = 'cristal planté et compteur seulement sur combattant vivant admissible ; ni véhicule ni structure'
    needler['notes'].append('La règle de supercombine exclut véhicules et structures ; l’admissibilité des autres entités doit être déclarée explicitement.')
    entries.extend(projectiles)
    by_id = {e["id"]: e for e in entries}
    for asset in additions:
        path = ROOT / asset["path"]
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != asset["sha256"]:
            raise ValueError(f"Asset hash mismatch: {asset['path']}")
        asset.setdefault("fidelity_1_to_1_certified", False)
        asset.setdefault("animation_status", "not_animated")
        asset.setdefault("automatically_mirrored", False)
        asset.setdefault("postprocessing", "none; copied byte-for-byte")
        target = by_id[asset["entity_id"]]
        target["assets"].append(asset)
        target["preferred_asset_id"] = asset["id"]
        target["art_status"] = asset["art_status"]
        target["visual_reference_status"] = "Références inspectées et PNG contrôlé ; réserves explicites, fidélité 1:1 non certifiée."
        target["reference_urls"] = list(dict.fromkeys(target.get("reference_urls", []) + asset.get("reference_urls", [])))
        target["notes"].extend(asset.get("notes", []))
        if target["category"] in ("projectile", "vfx"):
            target["asset_state"] = "static_candidate" if asset["art_status"] == "candidate" else "static_needs_correction"
            target["required_frames"][0]["status"] = "static_candidate_not_animation"
        elif target["category"] == "stage":
            target["implementation_status"] = "Master aplati disponible ; géométrie de gameplay, six calques indépendants et parallaxe à produire."
    all_assets = previous["all_assets"] + additions
    for title in data["titles"]:
        linked = [e for e in entries if e["work_id"] == title["id"]]
        title["catalogued_entries"] = len(linked)
        title["illustrated_entries"] = sum(bool(e["assets"]) for e in linked)
        title["metadata_origin"] = "Registre V9 conservé ; le statut de publication des œuvres n’est pas un nouvel audit V10."
    attempts = []
    for p in ["work/wave10/root_generation.json", "work/wave10/root_generation_followup.json", "work/wave10/alien_generation.json"]:
        attempts += read(p)["attempts"]
    def rejected(a):
        return "moderation_blocked" in str(a.get("error", "")) or a.get("status") == "moderation_blocked"
    calls = len(attempts)
    rejections = sum(rejected(a) for a in attempts)
    successes = sum(a.get("status") in ("generated", "generated_candidate") for a in attempts)
    count = {
        "entries": len(entries), "legacy_entries": 232, "new_entries": len(projectiles),
        "titles": len(data["titles"]), "titles_with_entries": len({e["work_id"] for e in entries}),
        "announced_titles": sum(t.get("release_status") == "announced_not_released" for t in data["titles"]),
        "by_category": dict(sorted(Counter(e["category"] for e in entries).items())),
        "new_by_category": dict(sorted(Counter(e["category"] for e in projectiles).items())),
        "unique_png_assets": len({a["path"] for a in all_assets}),
        "legacy_png_assets": len(previous["all_assets"]), "new_png_assets": len(additions),
        "illustrated_entries": sum(bool(e["assets"]) for e in entries),
        "missing_images": sum(not e["assets"] for e in entries),
        "legacy_cohort_missing_before": 155,
        "legacy_cohort_missing_after": sum(not e["assets"] for e in entries[:232]),
        "new_cohort_missing": sum(not e["assets"] for e in projectiles),
        "generation_calls": calls, "generation_successes": successes,
        "generation_rejections": rejections, "generation_technical_errors": calls - rejections - successes,
        "certified_1_to_1_assets": sum(a.get("fidelity_1_to_1_certified") is True for a in all_assets),
        "new_animation_clips": 0, "independent_parallax_layers": 0
    }
    data.update(version=10, updated_on=DATE, counts=count,
                scope="Catalogue de production V10 ; intégration des trois guides, extension des projectiles/VFX et conservation des versions antérieures.",
                previous_catalogue="data/universe_catalog_v9.json",
                guide_coverage="data/combat_guide_coverage_v10.json")
    data["continuity_rules"].extend([
        "Les guides généralistes sont des spécifications de design ; leurs exemples ne créent pas de pouvoirs, alliances ou technologies canoniques.",
        "Projectiles/VFX : modèle et comportement général d’Infinite verrouillés ; valeurs de combat 2D explicitement originales.",
        "Présence de fichier, découverte de fiche, droit de déblocage et disponibilité technique sont quatre états distincts.",
        "Le statut de publication des œuvres hérité de V9 n’a pas été ré-audité pour toute la bibliographie."
    ])
    data["limitations"].extend([
        "Les deux extensions sont importées intégralement et tracées par exigence ; seule une partie possède une démonstration exécutable.",
        "Les sept PNG V10 sont statiques ; les deux nouveaux décors sont des masters aplatis sans calques indépendants.",
        "Les 24 fiches projectile/VFX sont des spécifications ; aucun système de collision de projectile n’est livré par ces fiches.",
        "Le laboratoire V10 est local, sans réseau, achat ni validation serveur d’abonnement."
    ])
    data["sources"].extend([
        {"id":"infinite_inventory_v10", "url":INVENTORY, "role":"Identités ; les comportements périmés sont corrigés par CU32."},
        {"id":"infinite_cu32_v10", "url":CU32, "role":"Profil sandbox daté ; EMP plasma, grenade à pointes et Calcineur."}
    ])
    manifest = {"version":10, "legacy_manifest":"data/asset_manifest_v9.json", "legacy_assets_count":len(previous["all_assets"]), "new_assets":additions, "all_assets":all_assets, "counts":count}
    pdoc = {"version":10, "project":"Halo Combats", "updated_on":DATE, "scope":"24 spécifications Infinite ; PNG statiques présents séparément des mécanismes non implémentés.",
            "rules":{"canon_vs_design":"Les faits d’identité sont sourcés ; tous les paramètres 2D sont des propositions originales.",
                     "asset_policy":"Un objet par image, alpha réel lorsque demandé, aucun miroir automatique.",
                     "runtime_status":"specified_not_implemented",
                     "source_wording":"Synthèses brèves non exhaustives ; consulter la source officielle pour l’inventaire complet."},
            "source_urls":[INVENTORY,CU32,CU32_SANDBOX], "entries":projectiles}
    tasks = []
    for e in entries:
        a = e["assets"]
        tasks += [
          {"id":e["id"]+"::art","entity_id":e["id"],"category":e["category"],"task":"Visuel statique","status":e["art_status"],"evidence":[x["path"] for x in a]},
          {"id":e["id"]+"::fidelity","entity_id":e["id"],"category":e["category"],"task":"Validation comparative 1:1","status":"pending","evidence":[]},
          {"id":e["id"]+"::runtime","entity_id":e["id"],"category":e["category"],"task":"Implémentation spécifique complète","status":"pending","evidence":[]},
        ]
        if e["category"] == "stage":
            tasks.append({"id":e["id"]+"::parallax","entity_id":e["id"],"category":"stage","task":"Six calques indépendants et raccords","status":"not_produced","evidence":[]})
    write("data/universe_catalog_v10.json", data)
    write("data/asset_manifest_v10.json", manifest)
    write("data/projectiles_v10.json", pdoc)
    write("data/production_tasks_v10.json", {"version":10,"updated_on":DATE,"count":len(tasks),"status_semantics":"Les tâches signalent des jalons de production, pas un pourcentage de jeu terminé.","tasks":tasks})
    out = ROOT / "prototype/universe_v10"
    out.mkdir(parents=True, exist_ok=True)
    (out/"catalog.js").write_text("window.HALO_UNIVERSE_V10 = " + json.dumps(data,ensure_ascii=False,separators=(",",":")) + ";\n",encoding="utf-8")
    write("work/wave10/catalogue_build_report.json", {"version":10,"counts":count,"previous_104_assets_preserved":True,"guide_files":3,"guide_sections":68,"guide_requirements":311,"fixed_work_id":"knight_h4: h5 → h4","generation_journals":["work/wave10/root_generation.json","work/wave10/root_generation_followup.json","work/wave10/alien_generation.json"]})
    print(json.dumps(count,ensure_ascii=False))

if __name__ == "__main__":
    main()
