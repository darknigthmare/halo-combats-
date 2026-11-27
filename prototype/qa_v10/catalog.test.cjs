'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const vm = require('node:vm');
const ROOT = path.resolve(__dirname, '../..');
const read = p => JSON.parse(fs.readFileSync(path.join(ROOT,p),'utf8'));
const sha = p => crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT,p))).digest('hex');
const data = read('data/universe_catalog_v10.json');
const old = read('data/universe_catalog_v9.json');
const manifest = read('data/asset_manifest_v10.json');
const previous = read('data/asset_manifest_v9.json');
const projectiles = read('data/projectiles_v10.json');
const catalog = require('../universe_v10/app.js');

test('les 104 PNG et enregistrements historiques sont conservés, les 7 nouveaux correspondent à leurs empreintes', () => {
  assert.equal(previous.all_assets.length,104);
  assert.equal(manifest.new_assets.length,7);
  for(const asset of previous.all_assets) {
    assert.deepEqual(manifest.all_assets.find(a=>a.id===asset.id),asset);
    assert.equal(sha(asset.path),asset.sha256,asset.path);
  }
  for(const asset of manifest.new_assets) {
    assert.equal(sha(asset.path),asset.sha256,asset.path);
    assert.equal(asset.fidelity_1_to_1_certified,false);
    assert.equal(asset.automatically_mirrored,false);
    assert.equal(asset.animation_status,'not_animated');
    assert.ok(asset.reference_urls.length>0);
  }
  assert.equal(new Set(manifest.all_assets.map(a=>a.path)).size,111);
});
test('les 232 identités restent, la seule correction d’œuvre héritée est le Chevalier Halo 4', () => {
  assert.equal(new Set(data.entries.map(e=>e.id)).size,256);
  for(const entry of old.entries) {
    const next=data.entries.find(e=>e.id===entry.id);
    assert.ok(next,entry.id);assert.equal(next.name,entry.name);
    assert.equal(next.work_id,entry.id==='knight_h4'?'h4':entry.work_id,entry.id);
    assert.equal(next.continuity,entry.continuity);
  }
  assert.equal(data.entries.find(e=>e.id==='knight_h4').work_title,'Halo 4');
});
test('les compteurs distinguent la cohorte héritée de la nouvelle liste de production', () => {
  assert.deepEqual(catalog.summarize(data),{entries:256,assets:111,missing:172,illustrated:84,titles:112,coveredTitles:50});
  const older = data.entries.filter(e=>old.entries.some(o=>o.id===e.id));
  assert.equal(older.filter(e=>!e.assets.length).length,152);
  assert.equal(projectiles.entries.filter(e=>!e.assets.length).length,20);
  assert.equal(data.counts.legacy_cohort_missing_before,155);
  assert.equal(data.counts.new_animation_clips,0);
  assert.equal(data.counts.certified_1_to_1_assets,0);
  assert.equal(data.counts.generation_calls,13);
  assert.equal(data.counts.generation_rejections,5);
  assert.equal(data.counts.generation_technical_errors,1);
});
test('les catégories projectile et VFX sont filtrables sans doublon ni fausse jouabilité', () => {
  assert.equal(catalog.filterEntries(data.entries,{category:'projectile'}).length,19);
  assert.equal(catalog.filterEntries(data.entries,{category:'vfx'}).length,5);
  assert.equal(catalog.filterEntries(data.entries,{category:'projectile',missingOnly:true}).length,15);
  for(const entry of projectiles.entries) {
    assert.deepEqual(entry,data.entries.find(e=>e.id===entry.id));
    assert.equal(entry.design_proposal.status,'specified_not_implemented');
    assert.equal(entry.design_proposal.simulation_hz,60);
    assert.match(entry.source_version,/CU32/);
    assert.equal(entry.design_proposal.ownership.source_fighter_id,'immuable');
    assert.ok(entry.reference_urls.every(url=>catalog.referenceURL(url)));
  }
});
test('le profil CU32 évite de reprendre une description officielle périmée', () => {
  const plasma=projectiles.entries.find(e=>e.id==='proj_plasma_pistol_overcharge_infinite');
  const spike=projectiles.entries.find(e=>e.id==='proj_spike_infinite');
  const cindershot=projectiles.entries.find(e=>e.id==='proj_cindershot_infinite');
  assert.match(plasma.identity_fact,/EMP véhicule rétabli/);
  assert.doesNotMatch(JSON.stringify(plasma),/aucun EMP véhicule/);
  assert.equal(spike.design_proposal.fuse_start,'at_rest_or_stuck');
  assert.equal(spike.design_proposal.fuse_frames_proposed,72);
  assert.match(cindershot.design_proposal.interaction,/aucune aspiration/);
  assert.ok(plasma.reference_urls.some(url=>url.includes('25897330878868')));
});
test('la version embarquée hors ligne contient exactement le JSON V10', () => {
  const context={window:{}};
  vm.runInNewContext(fs.readFileSync(path.join(ROOT,'prototype/universe_v10/catalog.js'),'utf8'),context);
  assert.deepEqual(JSON.parse(JSON.stringify(context.window.HALO_UNIVERSE_V10)),data);
});
test('les trois guides intégrés sont les originaux intégraux et toutes leurs sections sont tracées', () => {
  const files = {
    'Combat_Games_Guide_General_v1.0.txt':'4844584616072ac0d52d37c2fab4365e1ec489240f17a721ee216e223b0355b7',
    'Combat_Games_Extension_01_Tag_Taunts_Bonus_v1.0.txt':'330fb7485a7a52b2a20f855646c940aaac0fcd9510032bc84b2e17c518edd25f',
    'Combat_Games_Extension_02_Slots_Verrouilles_Deblocages_Abonnes_v1.0.txt':'08b57ea542e83c487fef3276997a612d4657f2ee9ed4f8e46b0bf65a2778038b'
  };
  for(const [name,hash] of Object.entries(files)) assert.equal(sha('docs/guides_combat/'+name),hash,name);
  const coverage=read('data/combat_guide_coverage_v10.json');
  assert.equal(coverage.sections.length,68);
  assert.equal(coverage.requirements.length,311);
  assert.equal(coverage.counts.source_files,3);
});
test('aucun refus de génération n’est transformé en nouveau PNG et les réserves restent exposées', () => {
  for(const id of ['kelly_h5','romeo_odst','agryna_infinite','grunt_heavy_reach','spark_h3'])
    assert.equal(manifest.new_assets.some(a=>a.entity_id===id),false,id);
  const ce=data.entries.find(e=>e.id==='st_cartographer_ce');
  assert.equal(ce.art_status,'needs_correction');
  assert.equal(ce.assets.at(-1).fidelity_1_to_1_certified,false);
  for(const entry of data.entries) {
    for(const asset of entry.assets) assert.ok(manifest.all_assets.some(a=>a.id===asset.id && a.sha256===asset.sha256));
  }
});
