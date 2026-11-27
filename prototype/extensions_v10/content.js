(function(root){ 'use strict';
const entries = [
  {
    "id": "chief_infinite",
    "name": "John 117 le Major",
    "category": "character",
    "work_id": "infinite",
    "work_title": "Halo Infinite",
    "continuity": "core",
    "asset": {
      "path": "assets/characters_wave4/chief_infinite_neutral_right_v01.png",
      "id": "chief_infinite_neutral_right_v01",
      "sha256": "3963bb6268be816657bace42669dfa614eee0864863fea63b252c51340845e9e"
    },
    "art_status": "candidate",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halowaypoint.com/news/customization-overview-season-5"
    ],
    "visual_lock": "Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "jerome_hw2",
    "name": "Jerome 092",
    "category": "character",
    "work_id": "hw2",
    "work_title": "Halo Wars 2",
    "continuity": "core",
    "asset": {
      "path": "assets/characters_wave2/jerome_hw2_neutral_right_v01.png",
      "id": "jerome_hw2_neutral_right_v01",
      "sha256": "0559322aa3a021736df018fcb9d8f51bd9e19fd960cad43eed05c5098136675d"
    },
    "art_status": "candidate",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halowaypoint.com/news/anniversary-angle-march-of-the-dream-teams"
    ],
    "visual_lock": "Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "alice_hw2",
    "name": "Alice 130",
    "category": "character",
    "work_id": "hw2",
    "work_title": "Halo Wars 2",
    "continuity": "core",
    "asset": {
      "path": "assets/characters_wave3/alice_hw2_neutral_right_v01.png",
      "id": "alice_hw2_neutral_right_v01",
      "sha256": "95e8e93a88c344191a9f85eee86cab72e2546dd5c86dced7cdb9bbb2003b1f40"
    },
    "art_status": "candidate",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halowaypoint.com/news/womens-history-month-2024"
    ],
    "visual_lock": "Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "buck_odst",
    "name": "Edward Buck ODST",
    "category": "character",
    "work_id": "odst",
    "work_title": "Halo 3: ODST",
    "continuity": "core",
    "asset": {
      "path": "assets/characters_wave2/buck_odst_neutral_right_v01.png",
      "id": "buck_odst_neutral_right_v01",
      "sha256": "72a05937f61306306e063487b3cff33b789bfd993ff05113d3b47b5c26e45155"
    },
    "art_status": "candidate",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halowaypoint.com/news/anniversary-angle-march-of-the-dream-teams"
    ],
    "visual_lock": "Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "arbiter_h3",
    "name": "Thel 'Vadam l’Arbiter",
    "category": "character",
    "work_id": "h3",
    "work_title": "Halo 3",
    "continuity": "core",
    "asset": {
      "path": "assets/candidates/arbiter_halo3_neutral_right_v2.png",
      "id": "arbiter_h3_neutral_v2",
      "sha256": "23ac61d89be17a710936a693879ec7ddd7ce700faf4c9e9ee9c371c4e9b18486"
    },
    "art_status": "candidate",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halowaypoint.com/news/sweet-sixteenth"
    ],
    "visual_lock": "Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "ntho_h3",
    "name": "N’tho ’Sraom",
    "category": "character",
    "work_id": "h3",
    "work_title": "Halo 3",
    "continuity": "core",
    "asset": {
      "path": "assets/characters_wave9/ntho_h3_initial_right_v01.png",
      "id": "ntho_h3_initial_right_v01",
      "sha256": "6506925630945ad5f9ca0ee30e156112170148528663cce12e8636854ef78355"
    },
    "art_status": "candidate",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halopedia.org/File:Halo3-N%27tho_%27Sraom.png",
      "https://www.halopedia.org/images/6/60/Halo3-N%27tho_%27Sraom.png?c440f"
    ],
    "visual_lock": "Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "usze_h3",
    "name": "Usze ’Taham",
    "category": "character",
    "work_id": "h3",
    "work_title": "Halo 3",
    "continuity": "core",
    "asset": {
      "path": "assets/characters_wave9/usze_h3_initial_right_v01.png",
      "id": "usze_h3_initial_right_v01",
      "sha256": "5111b31fa3fbb307ad0bcccd3cb80a07901665bf9e7de38555b754b966fb9fc1"
    },
    "art_status": "candidate",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halopedia.org/File:H3-Usze_Taham_Portrait.png",
      "https://www.halopedia.org/images/9/97/H3-Usze_Taham_Portrait.png?ff5cd",
      "https://www.halopedia.org/File:UszeTaham_-_Profile.png",
      "https://www.halopedia.org/images/e/e7/UszeTaham_-_Profile.png?fce87"
    ],
    "visual_lock": "Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "dare_odst",
    "name": "Veronica Dare",
    "category": "character",
    "work_id": "odst",
    "work_title": "Halo 3: ODST",
    "continuity": "core",
    "asset": {
      "path": "assets/characters_wave9/dare_odst_initial_right_v01.png",
      "id": "dare_odst_initial_right_v01",
      "sha256": "0bb2c2cb63b046591d2fc8a184aae49abe4f2c4703f6ee4fff7f6cca9bed04bf"
    },
    "art_status": "candidate",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halopedia.org/File:Halo3_ODST_Dare.png",
      "https://www.halopedia.org/images/a/a8/Halo3_ODST_Dare.png?342e9",
      "https://files.bungie.org/odst_assets/"
    ],
    "visual_lock": "Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "linda_h5",
    "name": "Linda-058",
    "category": "character",
    "work_id": "h5",
    "work_title": "Halo 5: Guardians",
    "continuity": "core",
    "asset": {
      "path": "assets/characters_wave9/linda_h5_initial_right_v01.png",
      "id": "linda_h5_initial_right_v01",
      "sha256": "c73debf68dd6f42590c38ffaad703b6a1e9b0da6850603e57e527b01693436e4"
    },
    "art_status": "candidate",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halopedia.org/File:H5G-Render-Linda.png",
      "https://www.halopedia.org/images/2/21/H5G-Render-Linda.png?65c35",
      "https://web.archive.org/web/20150629031730/https://www.halowaypoint.com/en-us/games/halo-5-guardians/xbox-one"
    ],
    "visual_lock": "Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "kelly_h5",
    "name": "Kelly-087",
    "category": "character",
    "work_id": "h5",
    "work_title": "Halo 5: Guardians",
    "continuity": "core",
    "asset": null,
    "art_status": "missing",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halopedia.org/File:H5G-Render-Kelly.png",
      "https://www.halopedia.org/images/b/b6/H5G-Render-Kelly.png?71a63",
      "https://web.archive.org/web/20150629031730/https://www.halowaypoint.com/en-us/games/halo-5-guardians/xbox-one"
    ],
    "visual_lock": "Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "kai_silver",
    "name": "Kai-125 — Silver Timeline",
    "category": "character",
    "work_id": "silver_s1",
    "work_title": "Halo — Television Series, Season One",
    "continuity": "silver",
    "asset": null,
    "art_status": "missing",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halowaypoint.com/news/silver-debrief-a-new-beginning"
    ],
    "visual_lock": "Conserver le modèle de la série ; l’identité Silver ne remplace pas une éventuelle incarnation core.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "arbiter_h5_kaidon",
    "name": "Thel ’Vadam — Halo 5",
    "category": "costume",
    "work_id": "h5",
    "work_title": "Halo 5: Guardians",
    "continuity": "core",
    "asset": {
      "path": "assets/costumes_wave9/arbiter_h5_kaidon_initial_right_v01.png",
      "id": "arbiter_h5_kaidon_initial_right_v01",
      "sha256": "15a89b2e1d6c3ed7b62adaf90adfba26e0cb00fc951581d1f86187bdb047707a"
    },
    "art_status": "candidate",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halopedia.org/Campaign",
      "https://www.halopedia.org/File:H5G_Arbiter_Render_1.jpg",
      "https://www.halopedia.org/images/5/5c/H5G_Arbiter_Render_1.jpg?289ab",
      "https://www.artstation.com/artwork/eA553"
    ],
    "visual_lock": "Verrouiller l’armure de cette incarnation ; pas un recoloriage du harnais Halo 3.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "costume_chief_ce_mark_v",
    "name": "John-117 — Mark V CE classique",
    "category": "costume",
    "work_id": "ce",
    "work_title": "Halo: Combat Evolved",
    "continuity": "core",
    "asset": null,
    "art_status": "missing",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halopedia.org/Campaign"
    ],
    "visual_lock": "Version historique déjà évoquée dans fighters.json ; formaliser une fiche visuelle propre.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "yoroi_tenrai",
    "name": "YOROI — configuration Tenrai de base",
    "category": "costume",
    "work_id": "tenrai",
    "work_title": "Halo Infinite — Fracture: Tenrai",
    "continuity": "fracture_tenrai",
    "asset": null,
    "art_status": "missing",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halowaypoint.com/en-us/news/fracture-tenrai-event-launch"
    ],
    "visual_lock": "Configuration cosmétique anonyme ; ce n’est pas un personnage canonique nommé.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "st_blood_gulch_ce",
    "name": "Blood Gulch",
    "category": "stage",
    "work_id": "ce",
    "work_title": "Halo: Combat Evolved",
    "continuity": "core",
    "asset": {
      "path": "assets/stages_wave9/blood_gulch_ce_master_v01.png",
      "id": "blood_gulch_ce_master_v01",
      "sha256": "86a2aae9835ea55784a8646fdc4ad410e3af8763642ff1cf33a6d467929bf0b9"
    },
    "art_status": "candidate",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halopedia.org/File:Blood_gulch.jpg",
      "https://www.halopedia.org/images/a/a5/Blood_gulch.jpg?495b7"
    ],
    "visual_lock": "Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "st_valhalla_h3",
    "name": "Valhalla",
    "category": "stage",
    "work_id": "h3",
    "work_title": "Halo 3",
    "continuity": "core",
    "asset": {
      "path": "assets/candidates/valhalla_halo3_master_v2.png",
      "id": "valhalla_h3_master_v2",
      "sha256": "a429c7661d32d116b0558d7af0a9174a1f6da72b858c532692bb351ef275f97d"
    },
    "art_status": "candidate",
    "fidelity": "candidate_not_certified",
    "reference_urls": [],
    "visual_lock": "Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "st_lockout_h2",
    "name": "Lockout",
    "category": "stage",
    "work_id": "h2",
    "work_title": "Halo 2",
    "continuity": "core",
    "asset": {
      "path": "assets/stages_wave9/lockout_h2_master_v01.png",
      "id": "lockout_h2_master_v01",
      "sha256": "b61d5759329aee887a3a3c79185d8e6d129498a95b5cd212d71c8cccc452546b"
    },
    "art_status": "candidate",
    "fidelity": "candidate_not_certified",
    "reference_urls": [
      "https://www.halopedia.org/File:H2_Lockout_Overview.png",
      "https://www.halopedia.org/images/0/03/H2_Lockout_Overview.png?0545e"
    ],
    "visual_lock": "Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.",
    "source_catalog": "data/universe_catalog_v9.json"
  },
  {
    "id": "st_mombasa_odst",
    "name": "Rues de Mombasa",
    "category": "stage",
    "work_id": "odst",
    "work_title": "Halo 3: ODST",
    "continuity": "core",
    "asset": {
      "path": "assets/candidates/mombasa_odst_night_master_v2.png",
      "id": "mombasa_odst_master_v2",
      "sha256": "d9efeaa25e0a50f56a74405c01a69067c8814e0609a86c986dd647244d4657da"
    },
    "art_status": "candidate",
    "fidelity": "candidate_not_certified",
    "reference_urls": [],
    "visual_lock": "Conserver l’incarnation exacte indiquée et ses asymétries ; ne pas mélanger les versions.",
    "source_catalog": "data/universe_catalog_v9.json"
  }
];
const flag = key => ({type: 'flag', key});
const precision = value => ({type: 'precision', value});
const archive = key => ({type: 'archive', key});
const all = (...rules) => ({type: 'all', rules});
const any = (...rules) => ({type: 'any', rules});
const configs = {
  chief_infinite: {base:true,rule:{type:'always'},description:'GEN3 Mark VI de Halo Infinite. Pose fixe candidate. Sélection possible dans la simulation principale.'},
  jerome_hw2: {base:true,rule:{type:'always'},description:'Jerome-092, incarnation Halo Wars 2. Combattant actif par défaut du laboratoire.'},
  alice_hw2: {base:true,rule:{type:'always'},description:'Alice-130, incarnation Halo Wars 2. Partenaire de Red Team ; les actions collectives du laboratoire restent originales.'},
  buck_odst: {base:true,rule:{type:'always'},description:'Buck dans Halo 3: ODST. Aucun bouclier énergétique ajouté par ce laboratoire.'},
  arbiter_h3: {discovery:'hint',maskedName:'Dossier Sangheili',rule:all(flag('assist'),flag('tag')),requirementLabel:'Réussir une assistance ET terminer un relais volontaire.',description:'Thel ’Vadam dans Halo 3. Une équipe avec une incarnation d’une autre époque appartient à la simulation, pas à une campagne historique.'},
  ntho_h3: {rule:flag('assist'),requirementLabel:'Réussir une assistance dans le laboratoire.',description:'N’tho ’Sraom, incarnation Halo 3. L’assistance et la chorégraphie de duo sont des propositions de cette adaptation.'},
  usze_h3: {rule:flag('tag'),requirementLabel:'Terminer un relais volontaire dans le laboratoire.',description:'Usze ’Taham, incarnation Halo 3. Chaque action conserve son propriétaire lors d’un relais.'},
  dare_odst: {rule:precision(8),requirementLabel:'Toucher au moins 8 cibles sur 12 dans une épreuve de précision.',description:'Veronica Dare, incarnation Halo 3: ODST. Les droits acquis ici concernent uniquement ce laboratoire local.'},
  linda_h5: {discovery:'secret',maskedName:'Dossier classifié',rule:all(archive('records'),precision(8)),requirementLabel:'Ouvrir les archives puis réussir l’épreuve de précision (8/12).',description:'Linda-058, incarnation Halo 5: Guardians. Récompense à réclamer une fois les deux conditions réunies.'},
  kelly_h5: {rule:precision(10),requirementLabel:'Toucher au moins 10 cibles sur 12.',description:'Kelly-087, incarnation Halo 5: Guardians. Le dossier peut être acquis ; le visuel de ce catalogue V9 reste à produire.'},
  kai_silver: {rule:archive('records'),requirementLabel:'Ouvrir le dernier dossier des archives.',description:'Kai-125 relève de la Silver Timeline. Elle reste séparée de la continuité principale et son visuel V9 est absent.'},
  arbiter_h5_kaidon: {rule:all(archive('armory'),any(precision(8),flag('duo'))),requires:['arbiter_h3'],requirementLabel:'Ouvrir l’arsenal ET (réussir 8 cibles OU une super duo). L’Arbiter est requis pour équiper cette apparence.',description:'Incarnation de Halo 5, adaptée comme apparence dans la simulation. Aucune statistique du laboratoire ne change. Exclue du profil strict Halo 3.'},
  costume_chief_ce_mark_v: {rule:archive('records'),requires:['chief_infinite'],requirementLabel:'Ouvrir le dernier dossier des archives.',description:'Mark V de Halo CE : référence de costume distincte. Visuel absent du catalogue V9 ; aucune apparence improvisée ne le remplace.'},
  yoroi_tenrai: {rule:archive('records'),requirementLabel:'Ouvrir le dernier dossier des archives.',description:'YOROI appartient à la Fracture Tenrai. Dossier alternatif séparé, visuel V9 encore absent ; aucun avantage d’abonnement.'},
  st_blood_gulch_ce: {base:true,rule:{type:'always'},description:'Master fixe candidat de Blood Gulch (CE). Fond de laboratoire ; géométrie 3D adaptée, sans calques parallaxe séparés.'},
  st_valhalla_h3: {rule:archive('armory'),requirementLabel:'Consulter l’arsenal des archives.',description:'Valhalla de Halo 3. Le master fixe existant est présenté sans prétendre à des interactions de décor implémentées.'},
  st_lockout_h2: {rule:precision(8),requirementLabel:'Réussir l’épreuve de précision (8/12).',description:'Lockout de Halo 2. Le droit d’accès inclut la présentation statique, sans condition supplémentaire de confort.'},
  st_mombasa_odst: {rule:all(flag('assist'),flag('tag'),flag('duo')),requirementLabel:'Réussir assistance, relais volontaire ET super duo.',description:'Mombasa de Halo 3: ODST. Le laboratoire n’affirme pas que cette composition inter-époques se déroule dans la chronologie officielle.'}
};
for (const e of entries) Object.assign(e,{discovery:'identified',claimable:true,base:false,technical:e.asset?'available':'missing_assets'},configs[e.id]);
entries.push(
  {id:'team_lab',name:'Simulation en équipe',category:'mode',base:true,discovery:'identified',rule:{type:'always'},technical:'available',work_title:'Halo Combats · adaptation originale',description:'Modèle hybride à deux membres. Commandes, jauge, états et résultats calculés ; les images restent fixes.',asset:null},
  {id:'precision',name:'Épreuve de précision',category:'mode',base:true,discovery:'identified',rule:{type:'always'},technical:'available',work_title:'Halo Combats · entraînement original',description:'12 cibles de simulation, objectif 8 touches. Temps étendu accessible en solo, mêmes récompenses locales.',asset:null},
  {id:'coordination',name:'Défi de coordination',category:'mode',rule:all(flag('assist'),flag('tag')),discovery:'identified',technical:'available',requirementLabel:'Réussir une assistance ET terminer un relais volontaire.',work_title:'Halo Combats · défi original',description:'Objectif : confirmer une super duo après avoir réalisé assistance et relais. Même simulation, pas une seconde campagne.',asset:null},
  {id:'boss_rush_plan',name:'Boss Rush',category:'mode',rule:all(flag('assist'),flag('tag'),flag('duo')),discovery:'identified',technical:'not_implemented',requirementLabel:'Terminer les trois objectifs de coordination.',work_title:'Halo Combats · mode planifié',description:'Condition de droit démontrée. Le mode complet et ses rencontres ne sont pas produits par ce laboratoire ; il ne peut donc pas être lancé.',asset:null}
);
const content={version:10,sourceVersion:9,scope:'22 dossiers représentatifs ; les droits de ce laboratoire sont locaux et séparés du jeu complet.',entries};
if(typeof module!=='undefined'&&module.exports)module.exports=content;
root.HaloExtensionsContent=content;
})(typeof globalThis!=='undefined'?globalThis:this);
