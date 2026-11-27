import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { SpreadsheetFile, Workbook } from '@oai/artifact-tool';

// Run a copy of this builder from an OS tmp directory with primary-runtime
// node_modules linked there. The synchronized repository has no dependency link.
// Arguments: repository root, output directory beneath the conversation workspace.
const workspaceRoot = '/workspace/scratch/3bda832bd7dc';
const repoRoot = path.resolve(process.argv[2] || path.join(workspaceRoot, 'halo-combats'));
const outputDir = path.resolve(process.argv[3] || path.join(workspaceRoot, 'outputs/halo-combats-v10'));
const inputs = {
  catalogue: 'data/universe_catalog_v10.json',
  projectiles: 'data/projectiles_v10.json',
  coverage: 'data/combat_guide_coverage_v10.json',
};
const inputHashes = {};
const readJSON = async relative => {
  const raw=await fs.readFile(path.join(repoRoot,relative),'utf8');
  inputHashes[relative]=crypto.createHash('sha256').update(raw).digest('hex');
  return JSON.parse(raw);
};
const [catalogue, projectiles, coverage] = await Promise.all(Object.values(inputs).map(readJSON));
assert.equal(catalogue.version, 10, 'The workbook must use the final V10 catalogue.');
assert.equal(coverage.version, 10);
assert.equal(coverage.sections.length, 68);
assert.equal(coverage.requirements.length, 311);
assert.equal(new Set(coverage.requirements.map(r => r.id)).size, 311);

const projectileRows = projectiles.entries || projectiles.projectiles;
assert.ok(Array.isArray(projectileRows), 'Projectile JSON must contain entries.');
const projectileById = new Map(projectileRows.map(e => [e.id, e]));
assert.equal(projectileById.size, projectileRows.length, 'Duplicate projectile IDs.');
const entriesById = new Map(catalogue.entries.map(e => [e.id, { ...e } ]));
assert.equal(entriesById.size, catalogue.entries.length, 'Duplicate catalogue IDs.');
for (const e of projectileRows) {
  if (!entriesById.has(e.id)) entriesById.set(e.id, { ...e, work_title: e.source_version });
}
const entries = [...entriesById.values()];
assert.equal(entries.length, catalogue.counts.entries, 'Projectile entries must not be counted twice.');

const categories = {
  character: 'Personnages', costume: 'Costumes', stage: 'Arènes',
  boss: 'Boss', projectile: 'Projectiles', vfx: 'Effets', mode: 'Modes',
};
const categoryOrder = ['character', 'costume', 'stage', 'boss', 'projectile', 'vfx', 'mode'];
entries.sort((a, b) => (categoryOrder.indexOf(a.category) - categoryOrder.indexOf(b.category)) || a.name.localeCompare(b.name, 'fr'));
const presentCategories = categoryOrder.filter(c => entries.some(e => e.category === c));
for (const e of entries) assert.ok(categories[e.category], `Unmapped category ${e.category}`);

const statusText = {
  adaptation_documented_not_design_validated: 'Adaptation documentée',
  partial_v8: 'V8 partiel', partial_v9: 'Catalogue V9 partiel',
  partial_v10_logic_verified: 'V10 logique partielle testée',
  partial_v10_browser_verified: 'V10 partiel, logique et écran testés',
  partial_v10_catalogue_browser_verified: 'Catalogue V10 partiel testé',
  pending_v10_verification: 'V10 à vérifier', not_implemented: 'Non implémenté',
  document_only: 'Document / référence',
  not_claimed_by_documentation: 'Non réceptionné en production',
  not_applicable: 'Sans asset requis',
  static_candidates_partial: 'Candidats statiques partiels',
  unverified_fidelity: 'Fidélité à contrôler', animation_missing: 'Clips manquants',
  narrative_art_missing: 'Scènes narratives manquantes', flat_masters_partial: 'Masters plats partiels',
  independent_layers_missing: 'Calques indépendants manquants',
  connected_stage_art_missing: 'Transitions de décor à produire',
  animation_and_audio_missing: 'Clips et audio manquants', ui_partial: 'Interface partielle',
  tutorial_assets_missing: 'Assets pédagogiques manquants', accessibility_partial: 'Accessibilité partielle',
  progression_art_missing: 'Visuels de progression manquants',
  selection_animation_missing: 'Clips de sélection manquants', team_art_missing: 'Assets équipe manquants',
  assist_animation_missing: 'Clips assist manquants', tag_animation_missing: 'Clips relais manquants',
  duo_animation_missing: 'Clips duo manquants', finisher_animation_missing: 'Clips finisher manquants',
  clash_art_missing: 'Assets clash manquants', entity_art_missing: 'Assets entité manquants',
  bonus_art_missing: 'Décors et assets bonus manquants', hub_art_missing: 'Assets exploration manquants',
  extension_animation_missing: 'Clips extension manquants', lock_ui_partial: 'Visuels de verrou partiels',
  costume_art_partial: 'Costumes partiels', stage_art_partial: 'Arènes partielles',
  mode_art_missing: 'Visuels des modes manquants', reveal_art_missing: 'Révélation à produire',
  supporter_art_missing: 'Contenus soutien non produits',
};
const displayStatus = value => statusText[value] || value || 'Non renseigné';
const sourceLabels = {general_v1: 'Guide général', extension_01_v1: 'Extension 01', extension_02_v1: 'Extension 02'};
const artLabels = {candidate:'Candidat à contrôler', missing:'Image absente', needs_correction:'Corrections requises',
  missing_asset:'Image absente', not_generated:'Image absente', static_candidate:'Candidat statique',
  candidate_not_certified:'Candidat non certifié'};
const strings = value => Array.isArray(value) ? value.map(strings).join('\n') : value && typeof value === 'object'
  ? Object.entries(value).map(([k,v]) => `${k}: ${strings(v)}`).join('\n') : value == null ? '' : String(value);
const flattenDesign = p => p ? [
  p.identity_fact && `Identité: ${strings(p.identity_fact)}`,
  p.design_proposal?.trajectory && `Trajet proposé: ${p.design_proposal.trajectory}`,
  p.design_proposal?.lifetime_frames_proposed != null && `Durée proposée: ${p.design_proposal.lifetime_frames_proposed} frames`,
  p.design_proposal?.collision && `Collision prévue: ${p.design_proposal.collision}`,
  p.design_proposal?.ownership?.damage_credit && `Attribution: ${p.design_proposal.ownership.damage_credit}`,
  p.design_proposal?.tag_policy && `Relais: ${p.design_proposal.tag_policy}`,
  'Règles du projet à équilibrer. Collisions de projectile non implémentées.',
].filter(Boolean).join('\n') : '';

const ownedPNG = new Set();
const assetPaths = new Set();
const catalogRows = [];
for (const e of entries) {
  const p = projectileById.get(e.id);
  const assets = e.assets || p?.assets || [];
  const pngs = assets.filter(a => typeof a.path === 'string' && a.path.toLowerCase().endsWith('.png'));
  let distinct = 0;
  for (const a of pngs) {
    assert.ok((await fs.stat(path.join(repoRoot, a.path))).isFile(), `Missing PNG ${a.path}`);
    assetPaths.add(a.path);
    if (!ownedPNG.has(a.path)) { ownedPNG.add(a.path); distinct += 1; }
  }
  const main = pngs.find(a => a.id === e.preferred_asset_id) || pngs[0];
  const certified = pngs.filter(a => a.fidelity_1_to_1_certified === true).length;
  const clips = Array.isArray(e.animation_clips) ? e.animation_clips.length : Number(e.animation_clips_count || 0);
  const animation = clips ? `${clips} clip(s) déclaré(s)` : pngs.length ? 'Pose fixe, aucun clip livré' : 'Animation non produite';
  const artState = typeof (e.art_status || p?.asset_state) === 'string' ? (e.art_status || p?.asset_state) : 'Non renseigné';
  catalogRows.push([
    categories[e.category], e.id, e.name, strings(p?.source_version || e.work_title), strings(e.continuity),
    artLabels[artState] || artState, pngs.length, distinct, animation, clips,
    strings(e.visual_reference_status || e.lore_status || e.source_visual_reference_status || 'Référence à vérifier'),
    certified ? 'Certification déclarée à contrôler' : 'Non certifiée', certified,
    strings(e.implementation_status || (p ? 'Fiche de production ; collisions non implémentées' : 'Non renseigné')),
    main?.path || '', strings(e.reference_urls || p?.reference_urls || []), flattenDesign(p),
    `${inputs.catalogue}#${e.id}${p ? `\n${inputs.projectiles}#${e.id}` : ''}`,
  ]);
}
assert.equal(assetPaths.size, catalogue.counts.unique_png_assets, 'Unique PNG count must reconcile with the catalogue.');
assert.equal(catalogRows.filter(r => r[6] > 0).length, catalogue.counts.illustrated_entries);
assert.equal(catalogRows.reduce((n,r) => n+r[12],0), catalogue.counts.certified_1_to_1_assets);
assert.equal(catalogRows.reduce((n,r) => n+r[9],0), catalogue.counts.new_animation_clips);

const sourceById = new Map(coverage.sources.map(s => [s.id,s]));
const requirementById = new Map(coverage.requirements.map(r => [r.id,r]));
const requirementsRows = [];
for (const section of coverage.sections) {
  const source = sourceById.get(section.source_id);
  assert.ok(source, `Unknown source ${section.source_id}`);
  const sourceSpan = `${source.repository_path}\nLignes ${section.source_line_start}–${section.source_line_end}`;
  requirementsRows.push([
    'Section', sourceLabels[section.source_id], section.id, `Section ${section.id}`, section.title,
    section.halo_application, section.decision, section.priority, displayStatus(section.design_status),
    displayStatus(section.prototype_status), displayStatus(section.asset_status), 'Regroupement documentaire',
    strings(section.evidence_paths), `${section.requirement_ids.length} exigences détaillées ci-dessous`,
    source.source_url, sourceSpan,
  ]);
  for (const id of section.requirement_ids) {
    const r = requirementById.get(id);
    assert.ok(r, `Unknown requirement ${id}`);
    requirementsRows.push([
      'Exigence', sourceLabels[r.source_id], r.section, r.id, r.requirement, r.halo_application,
      r.decision, r.priority, displayStatus(r.design_status), displayStatus(r.prototype_status),
      displayStatus(r.asset_status), displayStatus(r.production_validation_status),
      [...(r.evidence_paths || []), r.runtime_evidence_scope || 'Fichiers témoins du point de départ. L’intégration du guide ne certifie pas le gameplay ni l’art.',r.browser_evidence_scope,r.catalogue_browser_evidence_scope].filter(Boolean).join('\n'),
      r.acceptance, source.source_url, sourceSpan,
    ]);
  }
}
assert.equal(requirementsRows.filter(r => r[0] === 'Exigence').length, 311);
assert.equal(requirementsRows.filter(r => r[0] === 'Section').length, 68);

await fs.mkdir(outputDir, { recursive: true });
const wb = Workbook.create();
const summary = wb.worksheets.add('Synthèse');
const cat = wb.worksheets.add('Catalogue');
const req = wb.worksheets.add('Exigences');
const colors = {ink:'#172D3A', accent:'#007D8A', light:'#EAF2F5', muted:'#526773', amber:'#FFF0D5', red:'#9A3412'};
for (const sheet of [summary,cat,req]) sheet.showGridLines = false;
summary.tabColor = colors.ink;
cat.tabColor = '#6E8997';
req.tabColor = '#6E8997';

function basic(sheet, range) {
  const r=sheet.getRange(range);
  r.format.font={name:'Arial',size:10,color:colors.ink};
  r.format.rowHeight=20;
  r.format.verticalAlignment='center';
}
function title(sheet,text,lastCol) {
  sheet.getRange('A2').values=[[text]];
  sheet.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:colors.ink};
  sheet.getRange(`A2:${lastCol}2`).format.rowHeight=28;
  sheet.getRange(`A4:${lastCol}4`).format.borders={bottom:{style:'thin',color:colors.accent}};
}
function header(sheet, range) {
  sheet.getRange(range).format={fill:colors.ink,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},
    rowHeight:32,wrapText:true,horizontalAlignment:'center',verticalAlignment:'center',
    borders:{insideVertical:{style:'thin',color:'#FFFFFF'}}};
}
function width(sheet,col,value,lastRow) { sheet.getRange(`${col}1:${col}${lastRow}`).format.columnWidth=value; }
function table(sheet,range,name) {
  const t=sheet.tables.add(range,true,name);
  t.showFilterButton=true;
  t.style='TableStyleLight9';
  return t;
}
function addStatusRule(sheet,range,text) {
  sheet.getRange(range).conditionalFormats.add('containsText',{text,format:{fill:colors.amber,font:{color:colors.red}}});
}

const catFirst=7,catLast=catFirst+catalogRows.length-1;
basic(cat,`A1:R${catLast}`);
title(cat,'Halo Combats — catalogue V10','R');
cat.getRange('A3').values=[['1 ligne = 1 fiche de catalogue. Les PNG et clips sont comptés séparément.']];
cat.getRange('A3').format.font={italic:true,color:colors.muted};
cat.getRange('A5').values=[['Sources: universe_catalog_v10.json et projectiles_v10.json. Références détaillées à droite.']];
cat.getRange('A6:R6').values=[['Catégorie','ID','Entrée','Œuvre / version','Continuité','État visuel','PNG présents','PNG uniques imputés','Animation','Clips livrés','État lore / référence','Fidélité 1:1','PNG certifiés','État d’implémentation','Image principale','Références','Fiche projectile / adaptation','Source des données']];
cat.getRange(`A${catFirst}:R${catLast}`).values=catalogRows;
table(cat,`A6:R${catLast}`,'CatalogueV10');
header(cat,'A6:R6');
const catWidths=[17,31,37,31,21,28,14,16,31,13,66,25,14,65,75,90,90,60];
catWidths.forEach((w,i)=>width(cat,String.fromCharCode(65+i),w,catLast));
cat.getRange(`A${catFirst}:R${catLast}`).format.wrapText=true;
cat.getRange(`A${catFirst}:R${catLast}`).format.verticalAlignment='top';
cat.getRange(`G${catFirst}:H${catLast}`).setNumberFormat('#,##0');
cat.getRange(`J${catFirst}:J${catLast}`).setNumberFormat('#,##0');
cat.getRange(`M${catFirst}:M${catLast}`).setNumberFormat('#,##0');
for(let i=0;i<catalogRows.length;i++){
  const lines=Math.max(...catalogRows[i].map((v,c)=>strings(v).split('\n').reduce((n,l)=>n+Math.max(1,Math.ceil(l.length/(catWidths[c]*1.05))),0)));
  cat.getRange(`A${catFirst+i}:R${catFirst+i}`).format.rowHeight=Math.max(42,Math.min(360,lines*13.3+8));
}
addStatusRule(cat,`F${catFirst}:F${catLast}`,'absente');
addStatusRule(cat,`F${catFirst}:F${catLast}`,'Corrections');
cat.freezePanes.freezeRows(6);
cat.freezePanes.freezeColumns(3);

const reqFirst=7,reqLast=reqFirst+requirementsRows.length-1;
basic(req,`A1:P${reqLast}`);
title(req,'Halo Combats — exigences du guide','P');
req.getRange('A3').values=[['68 sections, 311 exigences regroupées. Une adaptation documentée n’est pas une réception du jeu.']];
req.getRange('A3').format.font={italic:true,color:colors.muted};
req.getRange('A5').values=[['Source: data/combat_guide_coverage_v10.json. Les trois originaux Drive restent la référence intégrale.']];
req.getRange('A6:P6').values=[['Niveau','Guide','Section','ID','Exigence / titre','Adaptation Halo','Décision','Priorité','Conception','Prototype','Assets','Validation production','Preuves / portée','Critère de réception','Original Drive','Copie et lignes source']];
req.getRange(`A${reqFirst}:P${reqLast}`).values=requirementsRows;
table(req,`A6:P${reqLast}`,'ExigencesV10');
header(req,'A6:P6');
const reqWidths=[13,18,10,25,85,90,17,10,29,35,37,37,90,85,95,90];
reqWidths.forEach((w,i)=>width(req,String.fromCharCode(65+i),w,reqLast));
req.getRange(`A${reqFirst}:P${reqLast}`).format.wrapText=true;
req.getRange(`A${reqFirst}:P${reqLast}`).format.verticalAlignment='top';
req.getRange(`C${reqFirst}:C${reqLast}`).setNumberFormat('00');
for(let i=0;i<requirementsRows.length;i++){
  const lines=Math.max(...requirementsRows[i].map((v,c)=>strings(v).split('\n').reduce((n,l)=>n+Math.max(1,Math.ceil(l.length/(reqWidths[c]*1.05))),0)));
  const row=reqFirst+i;
  req.getRange(`A${row}:P${row}`).format.rowHeight=Math.max(50,Math.min(350,lines*13.3+8));
  if(requirementsRows[i][0]==='Section'){
    req.getRange(`A${row}:P${row}`).format.fill=colors.light;
    req.getRange(`A${row}:E${row}`).format.font={bold:true};
  }
}
addStatusRule(req,`J${reqFirst}:J${reqLast}`,'à vérifier');
addStatusRule(req,`J${reqFirst}:J${reqLast}`,'Non implémenté');
req.freezePanes.freezeRows(6);
req.freezePanes.freezeColumns(4);

const totalRow=6+presentCategories.length;
const guideHeader=totalRow+4, guideFirst=guideHeader+1, guideTotal=guideFirst+3;
const receiptRow=guideTotal+4;
basic(summary,`A1:K${receiptRow+10}`);
title(summary,'Halo Combats — production V10','K');
summary.getRange('A3').values=[['État arrêté au']];
summary.getRange('B3').values=[[new Date(`${coverage.updated_on}T12:00:00Z`)]];
summary.getRange('B3').setNumberFormat('dd/mm/yyyy');
summary.getRange('A5:G5').values=[['Catégorie','Fiches','Avec PNG','Sans PNG','PNG uniques','Clips livrés','PNG certifiés 1:1']];
header(summary,'A5:G5');
for(let i=0;i<presentCategories.length;i++){
  const r=6+i;
  summary.getRange(`A${r}`).values=[[categories[presentCategories[i]]]];
  summary.getRange(`B${r}:G${r}`).formulas=[[
    `=COUNTIF('Catalogue'!$A$${catFirst}:$A$${catLast},A${r})`,
    `=COUNTIFS('Catalogue'!$A$${catFirst}:$A$${catLast},A${r},'Catalogue'!$G$${catFirst}:$G$${catLast},">0")`,
    `=B${r}-C${r}`,
    `=SUMIF('Catalogue'!$A$${catFirst}:$A$${catLast},A${r},'Catalogue'!$H$${catFirst}:$H$${catLast})`,
    `=SUMIF('Catalogue'!$A$${catFirst}:$A$${catLast},A${r},'Catalogue'!$J$${catFirst}:$J$${catLast})`,
    `=SUMIF('Catalogue'!$A$${catFirst}:$A$${catLast},A${r},'Catalogue'!$M$${catFirst}:$M$${catLast})`,
  ]];
}
summary.getRange(`A${totalRow}`).values=[['Total catalogue V10']];
summary.getRange(`B${totalRow}:G${totalRow}`).formulas=[[...['B','C','D','E','F','G'].map(c=>`=SUM(${c}6:${c}${totalRow-1})`)]];
summary.getRange(`A${totalRow}:G${totalRow}`).format.fill=colors.light;
summary.getRange(`A${totalRow}:G${totalRow}`).format.font={bold:true};
summary.getRange(`B6:G${totalRow}`).setNumberFormat('#,##0');
summary.getRange(`A6:G${totalRow}`).format.rowHeight=27;
summary.getRange('I5').values=[['Lecture des états']];
summary.getRange('I5').format.font={bold:true};
summary.getRange('I6:I10').values=[
  ['Une image présente reste un candidat à contrôler.'],
  ['La fidélité 1:1 se valide asset par asset.'],
  ['Une pose fixe ne compte pas comme animation.'],
  ['Les fiches de catalogue ne sont pas des kits jouables.'],
  ['Les comptes mesurent des objets, pas un pourcentage du jeu.'],
];
summary.getRange('I6:I10').format.font={color:colors.muted};

summary.getRange(`A${guideHeader}:F${guideHeader}`).values=[['Source','Sections','Exigences','Adaptations documentées','V10 partiel testé','Réception finale']];
header(summary,`A${guideHeader}:F${guideHeader}`);
for(let i=0;i<coverage.sources.length;i++){
  const row=guideFirst+i;
  summary.getRange(`A${row}`).values=[[sourceLabels[coverage.sources[i].id]]];
  const common=`'Exigences'!$B$${reqFirst}:$B$${reqLast},A${row}`;
  const type=`'Exigences'!$A$${reqFirst}:$A$${reqLast}`;
  summary.getRange(`B${row}:F${row}`).formulas=[[
    `=COUNTIFS(${common},${type},"Section")`,
    `=COUNTIFS(${common},${type},"Exigence")`,
    `=COUNTIFS(${common},${type},"Exigence",'Exigences'!$I$${reqFirst}:$I$${reqLast},"Adaptation documentée")`,
    `=COUNTIFS(${common},${type},"Exigence",'Exigences'!$J$${reqFirst}:$J$${reqLast},"V10 logique partielle testée")+COUNTIFS(${common},${type},"Exigence",'Exigences'!$J$${reqFirst}:$J$${reqLast},"V10 partiel, logique et écran testés")+COUNTIFS(${common},${type},"Exigence",'Exigences'!$J$${reqFirst}:$J$${reqLast},"Catalogue V10 partiel testé")`,
    `=COUNTIFS(${common},${type},"Exigence",'Exigences'!$L$${reqFirst}:$L$${reqLast},"Réception finale validée")`,
  ]];
}
summary.getRange(`A${guideTotal}`).values=[['Total guide et extensions']];
summary.getRange(`B${guideTotal}:F${guideTotal}`).formulas=[[...['B','C','D','E','F'].map(c=>`=SUM(${c}${guideFirst}:${c}${guideTotal-1})`)]];
summary.getRange(`A${guideTotal}:F${guideTotal}`).format.fill=colors.light;
summary.getRange(`A${guideTotal}:F${guideTotal}`).format.font={bold:true};
summary.getRange(`B${guideFirst}:F${guideTotal}`).setNumberFormat('#,##0');
summary.getRange(`A${guideFirst}:F${guideTotal}`).format.rowHeight=27;
summary.getRange(`I${guideHeader}`).values=[['Périmètre des preuves']];
summary.getRange(`I${guideHeader}`).format.font={bold:true};
summary.getRange(`I${guideFirst}:I${guideFirst+2}`).values=[
  ['« Documentée » signifie que l’adaptation Halo est écrite.'],
  ['« V10 partiel testé » couvre seulement les cas rattachés.'],
  ['Une section complète conserve ses autres critères ouverts.'],
];
summary.getRange(`I${guideFirst}:I${guideFirst+2}`).format.font={color:colors.muted};
summary.getRange(`A${receiptRow}`).values=[['Réception du lot']];
summary.getRange(`A${receiptRow}`).format.font={bold:true};
summary.getRange(`A${receiptRow+1}:A${receiptRow+6}`).values=[
  [`${coverage.sources.length} originaux intégraux. Empreintes SHA-256 contrôlées.`],
  [`${catalogue.counts.independent_parallax_layers} calque de parallaxe indépendant livré dans ce catalogue.`],
  [coverage.runtime_v10.browser_verification?`Laboratoire: 30 tests Node et ${coverage.runtime_v10.browser_verification.passed} contrôles navigateur réussis.`:'Laboratoire: logique testée, contrôle navigateur en attente.'],
  ['Les simulations inter-époques et créations du projet restent signalées.'],
  ['L’onglet Exigences conserve les sources et les limites de chaque preuve.'],
  [`Catalogue: ${coverage.catalogue_v10_verification?.assertions || 'non renseigné'} contrôles navigateur réussis.`],
];
summary.getRange(`A${receiptRow+1}:A${receiptRow+6}`).format.font={color:colors.muted};
const sumWidths={A:31,B:14,C:16,D:20,E:21,F:19,G:21,H:4,I:65,J:3,K:3};
for(const [c,w] of Object.entries(sumWidths)) width(summary,c,w,receiptRow+10);
summary.getRange(`A1:K${receiptRow+10}`).format.wrapText=false;
summary.getRange('A5:G5').format.wrapText=true;
summary.getRange(`A${guideHeader}:F${guideHeader}`).format.wrapText=true;
summary.getRange(`A${guideHeader}:F${guideHeader}`).format.rowHeight=42;

// Recalculate and compare independent JSON controls with actual formula results.
wb.recalculate();
const total=summary.getRange(`B${totalRow}:G${totalRow}`).values[0];
assert.deepEqual(total,[entries.length,catalogue.counts.illustrated_entries,catalogue.counts.missing_images,
  assetPaths.size,catalogue.counts.new_animation_clips,catalogue.counts.certified_1_to_1_assets]);
const guideCounts=summary.getRange(`B${guideTotal}:D${guideTotal}`).values[0];
assert.deepEqual(guideCounts,[68,311,311]);
assert.equal(summary.getRange(`E${guideTotal}`).values[0][0],coverage.requirements.filter(r=>['partial_v10_logic_verified','partial_v10_browser_verified','partial_v10_catalogue_browser_verified'].includes(r.prototype_status)).length);
assert.equal(summary.getRange(`F${guideTotal}`).values[0][0],0);

// A live edit must flow through COUNTIFS and its dependent missing-image count.
const firstWithPNG=catalogRows.findIndex(r=>r[6]>0)+catFirst;
const originalPNG=cat.getRange(`G${firstWithPNG}`).values[0][0];
cat.getRange(`G${firstWithPNG}`).values=[[0]];
wb.recalculate();
assert.equal(summary.getRange(`C${totalRow}`).values[0][0],catalogue.counts.illustrated_entries-1);
assert.equal(summary.getRange(`D${totalRow}`).values[0][0],catalogue.counts.missing_images+1);
cat.getRange(`G${firstWithPNG}`).values=[[originalPNG]];
wb.recalculate();
assert.deepEqual(summary.getRange(`B${totalRow}:G${totalRow}`).values[0],total);

const inspection=await wb.inspect({kind:'region',sheetId:'Synthèse',range:`A5:G${guideTotal}`,
  maxChars:8500,tableMaxRows:30,tableMaxCols:7,tableMaxCellChars:70});
const errorScan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',
  options:{useRegex:true,maxResults:30},summary:'Final formula error scan'});
await fs.writeFile(path.join(outputDir,'workbook_inspection.ndjson'),inspection.ndjson+'\n'+errorScan.ndjson);
assert.ok(!/#REF!|#DIV\/0!|#VALUE!|#NAME\?|#NUM!|#NULL!|#SPILL!|#CALC!/.test(JSON.stringify(summary.getRange(`A1:G${guideTotal}`).values)), 'Formula error in summary.');

// Each new worksheet is rendered; render only useful ranges of the long tables.
const allPreviews=[
  ['Synthèse',`A1:I${receiptRow+7}`,'synthese'],
  ['Catalogue','A1:J10','catalogue'],
  ['Catalogue','K6:N10','catalogue_etats'],
  ['Exigences','A1:J10','exigences'],
  ['Exigences','K6:P10','exigences_preuves'],
];
const previews=process.argv[4]==='summary-only'?allPreviews.filter(p=>p[0]==='Synthèse'):
  process.argv[4]==='guide-only'?allPreviews.filter(p=>p[0]!=='Catalogue'):allPreviews;
for(const [sheetName,range,filename] of previews){
  const blob=await wb.render({sheetName,range,scale:1.35,format:'png'});
  await fs.writeFile(path.join(outputDir,`${filename}.png`),new Uint8Array(await blob.arrayBuffer()));
}
const xlsx=await SpreadsheetFile.exportXlsx(wb);
const exported=path.join(outputDir,'HALO_COMBATS_PRODUCTION_V10.xlsx');
await xlsx.save(exported);
const sha=crypto.createHash('sha256').update(await fs.readFile(exported)).digest('hex');
for(const p of Object.values(inputs)) assert.equal(crypto.createHash('sha256').update(await fs.readFile(path.join(repoRoot,p))).digest('hex'),inputHashes[p],`Source changed while building: ${p}`);
const receipt={created_on:coverage.updated_on,authoring_library:'@oai/artifact-tool',sources:inputs,
  source_sha256:Object.fromEntries(Object.entries(inputs).map(([k,p])=>[k,inputHashes[p]])),
  workbook:exported,sha256:sha,sheets:['Synthèse','Catalogue','Exigences'],catalogue_entries:entries.length,
  unique_png:assetPaths.size,sections:68,requirements:311,formula_controls:total,guide_formula_controls:guideCounts,
  changed_input_and_restored:true,error_scan:errorScan.ndjson,
  preview_files:previews.map(p=>`${p[2]}.png`),
  native_excel_execution:false,visual_review:'pending external review of PNG previews'};
await fs.writeFile(path.join(outputDir,'workbook_build_receipt.json'),JSON.stringify(receipt,null,2)+'\n');
console.log(JSON.stringify({workbook:exported,sha256:sha,entries:entries.length,requirements:311,sections:68,formula_controls:total,previews:receipt.preview_files},null,2));
