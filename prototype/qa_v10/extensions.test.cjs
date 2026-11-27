'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const R = require('../extensions_v10/rules.js');
const C = require('../extensions_v10/content.js').entries;
const now = Date.UTC(2026, 10, 27);
const profile = () => R.newProfile(C);
const fight = () => R.newCombat(['jerome_hw2', 'alice_hw2']);
const entry = id => C.find(c => c.id === id);
const advance = (s, frames) => R.step(s, frames).state;
const issue = (s, type, more) => { const result = R.command(s, {type, ...(more || {})}); assert.equal(result.ok, true, result.code); return result.state; };

test('locked information remains inspectable without changing the selected team', () => {
  const p = profile(), snapshot = JSON.stringify(p);
  const view = R.contentState(entry('arbiter_h3'), p, C, now);
  assert.equal(view.discovery, 'hint'); assert.equal(view.showSilhouette, true);
  assert.equal(R.choose(p, 'arbiter_h3', 'activeId', C, now).ok, false);
  assert.equal(JSON.stringify(p), snapshot);
});

test('a secret view exposes neither identity nor image; its clue is deliberately neutral', () => {
  const view = R.contentState(entry('linda_h5'), profile(), C, now);
  assert.equal(view.name, 'Dossier classifié'); assert.equal(view.asset, null);
  assert.equal(view.workTitle, 'Archive classifiée'); assert.equal(view.discovery, 'secret');
  assert.doesNotMatch(JSON.stringify({name:view.name,asset:view.asset,work:view.workTitle}), /Linda|058|linda/i);
});

test('AND and OR conditions have independent branches and do not grant access by preview', () => {
  let p = profile(); p.progress.archives = ['briefing', 'armory'];
  assert.equal(R.condition(p, entry('arbiter_h5_kaidon').rule).met, false);
  p.progress.flags.duo = true;
  assert.equal(R.condition(p, entry('arbiter_h5_kaidon').rule).met, true);
  p.progress.flags.duo = false; p.progress.precisionBest = 8;
  assert.equal(R.condition(p, entry('arbiter_h5_kaidon').rule).met, true);
  assert.equal(R.rights(p, 'arbiter_h5_kaidon', now).allowed, false);
});

test('claim is idempotent and an owned costume is retained while its parent is locked', () => {
  let p = profile(); p.progress.archives = ['briefing', 'armory']; p.progress.flags.duo = true;
  p = R.claim(p, 'arbiter_h5_kaidon', C, now).profile;
  const repeat = R.claim(p, 'arbiter_h5_kaidon', C, now);
  assert.equal(repeat.code, 'already_claimed'); assert.deepEqual(repeat.profile, p);
  const view = R.contentState(entry('arbiter_h5_kaidon'), p, C, now);
  assert.equal(view.access.allowed, true); assert.equal(view.dependency, 'arbiter_h3'); assert.equal(view.selectable, false);
  assert.equal(p.grants.arbiter_h5_kaidon.length, 1);
});

test('temporary expiry or revocation cannot remove a second permanent source', () => {
  let p = profile(); p.progress.precisionBest = 8;
  p = R.claim(p, 'dare_odst', C, now).profile;
  p = R.upsertGrant(p, 'dare_odst', {source:'demo/supporter', type:'temporary', status:'active', validUntil:now - 1, revision:1}, C).profile;
  assert.equal(R.rights(p, 'dare_odst', now).status, 'permanent');
  p = R.upsertGrant(p, 'dare_odst', {source:'demo/supporter', type:'temporary', status:'revoked', validUntil:now - 1, revision:2}, C).profile;
  assert.equal(R.rights(p, 'dare_odst', now).status, 'permanent');
});

test('pending verification stays unknown and older grant events are ignored', () => {
  let p = profile();
  p = R.upsertGrant(p, 'dare_odst', {source:'demo/supporter', type:'temporary', status:'pending', validUntil:null, revision:3}, C).profile;
  assert.equal(R.rights(p, 'dare_odst', now).status, 'pending');
  const older = R.upsertGrant(p, 'dare_odst', {source:'demo/supporter', type:'temporary', status:'active', validUntil:now + 1000, revision:2}, C);
  assert.equal(older.code, 'duplicate_or_older'); assert.deepEqual(older.profile, p);
});

test('earned permanent rights remain claimable during a temporary access window', () => {
  let p = profile(); p.progress.precisionBest = 8;
  p = R.upsertGrant(p, 'dare_odst', {source:'demo/supporter', type:'temporary', status:'active', validUntil:now+1000, revision:1}, C).profile;
  assert.equal(R.contentState(entry('dare_odst'), p, C, now).claimable, true);
  p = R.claim(p, 'dare_odst', C, now).profile;
  assert.equal(R.rights(p, 'dare_odst', now+2000).status, 'permanent');
});

test('an acquired missing PNG is a production issue, never a false payment lock', () => {
  let p = profile(); p.progress.precisionBest = 10;
  p = R.claim(p, 'kelly_h5', C, now).profile;
  const view = R.contentState(entry('kelly_h5'), p, C, now);
  assert.equal(view.access.allowed, true); assert.equal(view.technical, 'missing_assets');
  assert.deepEqual(view.obstacles, ['missing_assets']); assert.equal(view.selectable, false);
});

test('Silver and Fractures never leak into a principal-timeline team', () => {
  let p = profile(); p.progress.archives = ['briefing','armory','records'];
  p = R.claim(p,'kai_silver',C,now).profile;
  assert.equal(R.contentState(entry('kai_silver'),p,C,now).compatible.reason, 'continuity');
  assert.equal(R.compatibility(entry('yoroi_tenrai'),p).allowed,false);
  p.context.workId='h3';
  assert.equal(R.compatibility(entry('arbiter_h5_kaidon'),p).reason,'era');
});

test('duplicate characters and unavailable random picks are excluded', () => {
  const p=profile();
  assert.equal(R.choose(p,'alice_hw2','activeId',C,now).code,'duplicate_member');
  const ids=R.eligibleCharacters(p,C,now,'activeId');
  assert.ok(ids.includes('chief_infinite')); assert.ok(!ids.includes('alice_hw2')); assert.ok(!ids.includes('linda_h5'));
  p.selection.reserveId='linda_h5';
  assert.equal(R.startFromProfile(p,C,now).ok,false);
});

test('archive prerequisites have no circular dependency or repeated reward mutation', () => {
  let p=profile();
  assert.equal(R.visitArchive(p,'records').ok,false);
  for(const id of ['briefing','armory','records']) p=R.visitArchive(p,id).profile;
  const again=R.visitArchive(p,'armory'); assert.equal(again.code,'already_visited'); assert.deepEqual(again.profile,p);
});

test('a support cannot be committed to assist and tag in the same frame', () => {
  let s=issue(fight(),'assist'); const snapshot=JSON.stringify(s);
  const denied=R.command(s,{type:'tag'});
  assert.equal(denied.ok,false); assert.equal(denied.code,'partner_busy');
  assert.equal(JSON.stringify(denied.state),snapshot); assert.equal(s.gauge,75);
});

test('resource failure and hitstun never spend gauge', () => {
  let s=fight(); s.gauge=20;
  const failed=R.command(s,{type:'assist'}); assert.equal(failed.code,'gauge'); assert.equal(failed.state.gauge,20);
  s=issue(s,'damage',{amount:10});
  assert.equal(R.command(s,{type:'taunt'}).code,'hitstun');
  assert.equal(R.command(s,{type:'tag'}).state.gauge,20);
});

test('assist has arrival, impact, exit, then recovery rather than an instant refill', () => {
  let s=issue(fight(),'assist'); s=advance(s,17); assert.equal(s.opponentHp,900);
  s=advance(s,1); assert.equal(s.opponentHp,780); assert.equal(s.supportAction.actor,'alice_hw2');
  s=advance(s,30); assert.equal(s.supportAction,null); assert.equal(s.members[1].cooldown,300);
  assert.equal(R.command(s,{type:'assist'}).code,'partner_cooldown');
  s=advance(s,300); assert.equal(R.command(s,{type:'assist'}).ok,true);
});

test('interrupting the assistant damages its own health, retains cost and starts recovery', () => {
  let s=issue(fight(),'assist'); s=advance(s,10); s=issue(s,'damage',{target:'reserve',amount:250});
  assert.equal(s.members[1].hp,750); assert.equal(s.members[0].hp,1000);
  assert.equal(s.gauge,75); assert.equal(s.supportAction,null); assert.equal(s.members[1].cooldown,300);
  assert.equal(R.command(s,{type:'damage',target:'reserve',amount:10}).code,'reserve_offstage');
});

test('KO relay is free even when the surviving reserve is recovering', () => {
  let s=fight(); s.gauge=0; s.members[1].cooldown=300;
  s=issue(s,'damage',{amount:1000}); assert.equal(s.teamAction.forced,true); assert.equal(s.gauge,0);
  s=advance(s,18); assert.equal(s.activeId,'alice_hw2'); assert.equal(s.members[0].ko,true);
  s=advance(s,18); assert.equal(s.teamAction,null); assert.equal(s.members[1].hp,1000);
  assert.equal(R.command(s,{type:'assist'}).code,'partner_ko');
  s=issue(s,'damage',{amount:1000}); assert.equal(s.phase,'defeat');
});

test('voluntary tag transfers controls on frame 18 and preserves health and combo budget', () => {
  let s=fight(); s.gauge=50; s.members[0].hp=420;
  s=advance(issue(s,'normal'),40); assert.equal(s.combo.gaugeGain,10);
  s=issue(s,'tag'); s=advance(s,17); assert.equal(s.activeId,'jerome_hw2');
  s=advance(s,1); assert.equal(s.activeId,'alice_hw2'); assert.equal(s.members[0].hp,420);
  assert.equal(s.combo.gaugeGain,10); s=advance(s,18);
  s=advance(issue(s,'normal'),10); assert.equal(s.combo.gaugeGain,20);
});

test('normal attacks cannot exceed the shared gain cap within one combo', () => {
  let s=fight(); s.gauge=0;
  for(let i=0;i<4;i++) s=advance(issue(s,'normal'),40);
  assert.equal(s.combo.hits,4); assert.equal(s.combo.gaugeGain,25); assert.equal(s.gauge,25);
  s=advance(s,90); s=advance(issue(s,'normal'),40); assert.equal(s.gauge,35);
});

test('pause freezes frame, recoveries and state transitions', () => {
  let s=advance(issue(fight(),'assist'),48); s=issue(s,'pause');
  assert.deepEqual(advance(s,600),s); assert.equal(R.command(s,{type:'tag'}).code,'paused');
  s=issue(s,'pause'); s=advance(s,60); assert.equal(s.members[1].cooldown,240);
});

test('taunts grant nothing and a hit cancels them into hitstun', () => {
  let s=advance(issue(fight(),'taunt'),20); assert.equal(s.gauge,100);
  assert.equal(R.command(s,{type:'cancel_taunt'}).ok,false);
  s=issue(s,'damage',{amount:90}); assert.equal(s.activeAction.type,'hitstun');
  assert.equal(s.members[0].hp,910); assert.equal(s.gauge,100);
  s=advance(s,24); assert.equal(s.activeAction,null);
});

test('super confirms its scene only on hit; block and miss keep their cost and resolve quickly', () => {
  for(const [mode,duration,damage] of [['hit',150,360],['block',60,20],['miss',72,0]]) {
    let s=issue(fight(),'target',{mode}); s=issue(s,'super');
    assert.equal(s.gauge,25); s=advance(s,18);
    assert.equal(s.teamAction.type,mode==='hit'?'super_scene':'super_recovery');
    s=advance(s,duration-18); assert.equal(s.teamAction,null); assert.equal(s.opponentHp,900-damage); assert.equal(s.gauge,25);
  }
});

test('committed super scene freezes cooldowns and skip has the identical final simulation state', () => {
  let s=fight(); s.members[0].cooldown=60;
  s=advance(issue(s,'super'),18); assert.equal(s.members[0].cooldown,42);
  const waited=advance(s,132); const skipped=R.command(s,{type:'skip'}).state;
  assert.deepEqual(skipped,waited); assert.equal(waited.members[0].cooldown,42);
});

test('super startup is interruptible without refund and cannot double-spend with a tag', () => {
  let s=issue(fight(),'super'); assert.equal(R.command(s,{type:'tag'}).code,'team_busy');
  s=advance(s,5); s=issue(s,'damage',{amount:20});
  assert.equal(s.teamAction,null); assert.equal(s.gauge,25); assert.equal(s.opponentHp,900);
});

test('finisher cannot precede victory and cannot resurrect a KO partner', () => {
  let s=fight(); assert.equal(R.command(s,{type:'finisher'}).code,'no_finish_window');
  s.opponentHp=20; s.members[1].hp=0; s.members[1].ko=true;
  s=advance(issue(s,'normal'),10); assert.equal(s.phase,'finish_window');
  assert.equal(R.command(s,{type:'finisher'}).code,'partner_unavailable');
  s=advance(s,180); assert.equal(s.phase,'victory'); assert.equal(s.finish.type,'normal_victory'); assert.equal(s.members[1].hp,0);
});

test('finisher fallback and specific scene use exact duo, era, stage and opponent constraints', () => {
  let s=R.newCombat(['ntho_h3','usze_h3'],{stageId:'st_valhalla_h3',opponentKind:'brute_h3'});
  assert.equal(R.resolveFinisher(s).type,'specific_original');
  s.stageId='st_blood_gulch_ce'; assert.equal(R.resolveFinisher(s).type,'generic_original');
  s.opponentHp=20; s=advance(issue(s,'normal'),10); const hp=s.members.map(m=>m.hp);
  s=issue(s,'finisher'); s=R.command(s,{type:'skip'}).state;
  assert.equal(s.phase,'victory'); assert.deepEqual(s.members.map(m=>m.hp),hp); assert.equal(s.opponentHp,0);
});

test('selection and earned milestones are independent of image animation production', () => {
  let p=profile(), s=fight();
  const result=R.step(issue(s,'assist'),18); p=R.applyMilestones(p,result.events);
  assert.equal(p.progress.flags.assist,true); assert.equal(p.progress.flags.tag,false);
  const chosen=R.choose(p,'chief_infinite','activeId',C,now);
  assert.deepEqual(chosen.events.map(e=>e.type),['deselect','select_confirm','selection_idle']);
  assert.equal(entry('chief_infinite').fidelity,'candidate_not_certified');
});

test('precision targets accept one hit each and score can be persisted only after the run', () => {
  let b=R.stepBonus(R.newBonus('bonus-1',false),1).state;
  const id=b.targets[0].id; b=R.hitBonus(b,id).state;
  assert.equal(b.hits,1); assert.equal(R.hitBonus(b,id).ok,false);
  assert.equal(R.recordBonus(profile(),b).ok,false);
  while(!b.finished) { b=R.stepBonus(b,1).state; for(const t of b.targets) b=R.hitBonus(b,t.id).state; }
  assert.equal(b.hits,12); assert.equal(b.success,true);
  const p=R.recordBonus(profile(),b).profile; assert.equal(p.progress.precisionBest,12);
  const twice=R.recordBonus(p,b); assert.equal(twice.code,'duplicate_result'); assert.deepEqual(twice.profile,p);
});

test('missed bonus can be retried without taking away earned progress', () => {
  const failed=R.stepBonus(R.newBonus('bonus-2',true),5400).state;
  assert.equal(failed.finished,true); assert.equal(failed.success,false); assert.equal(failed.hits,0);
  let p=profile(); p.progress.precisionBest=9; p=R.recordBonus(p,failed).profile; assert.equal(p.progress.precisionBest,9);
});

test('saved progress round-trips without granting unknown IDs or accepting future/corrupt formats', () => {
  const p=profile(); p.progress.precisionBest=9;
  assert.deepEqual(R.readProfile(JSON.stringify(p),C).profile,p);
  assert.equal(R.readProfile('{bad',C).code,'invalid_json');
  assert.equal(R.readProfile(JSON.stringify({...p,schemaVersion:99}),C).code,'unsupported_version');
  const forged=R.clone(p); forged.grants.unknown=[{source:'fake',type:'permanent',status:'active',revision:1}];
  assert.equal(R.readProfile(JSON.stringify(forged),C).ok,false);
});

test('all representative PNG references exist, and all retained IDs are unique', () => {
  assert.equal(C.length,22); assert.equal(new Set(C.map(c=>c.id)).size,C.length);
  for(const item of C) if(item.asset) assert.ok(fs.existsSync(path.resolve(__dirname,'../..',item.asset.path)),item.id);
  assert.equal(R.SAVE_KEY,'halo-combats.extensions-v10.profile');
});
