(function (root) {
  'use strict';

  const RULES = Object.freeze({version: '10.0.0', hz: 60, health: 1000, opponentHealth: 900,
    gaugeMax: 100, gaugeInitial: 100, hitGain: 10, comboGainLimit: 25, comboReset: 90,
    normal: {duration: 40, impact: 10, damage: 80},
    assist: {cost: 25, enter: 18, active: 6, exit: 24, damage: 120, cooldown: 300},
    tag: {cost: 15, transfer: 18, duration: 36, outgoingCooldown: 120},
    taunt: {duration: 60, entry: 18, pose: 24, exit: 18, cancelAt: 42},
    super: {cost: 75, opener: 18, hitDuration: 150, blockDuration: 60, missDuration: 72, damage: 360, chip: 20},
    finisher: {window: 180, duration: 120}, hitstun: 24});
  const SAVE_VERSION = 1;
  const SAVE_KEY = 'halo-combats.extensions-v10.profile';
  const clone = value => JSON.parse(JSON.stringify(value));
  const finiteInt = (value, low, high) => Number.isInteger(value) && value >= low && value <= high;
  const clamp = (value, low, high) => Math.max(low, Math.min(high, value));
  const bool = value => value === true;
  const member = (s, id) => s.members.find(m => m.id === id);
  const active = s => member(s, s.activeId);
  const reserve = s => s.members.find(m => m.id !== s.activeId);
  const event = (s, out, type, details) => {
    const item = {id: `${s.runId}:${s.frame}:${++s.eventSeq}`, frame: s.frame, type, ...(details || {})};
    out.push(item);
    s.log.push(item);
    if (s.log.length > 32) s.log.shift();
  };
  const deny = (s, code) => ({state: s, ok: false, code, events: []});
  const succeed = (s, events) => ({state: s, ok: true, code: 'ok', events});

  function condition(profile, rule) {
    if (!rule || rule.type === 'always') return {met: true, done: 1, total: 1};
    if (rule.type === 'flag') return {met: bool(profile.progress.flags[rule.key]), done: Number(bool(profile.progress.flags[rule.key])), total: 1};
    if (rule.type === 'precision') return {met: profile.progress.precisionBest >= rule.value, done: Math.min(profile.progress.precisionBest, rule.value), total: rule.value};
    if (rule.type === 'archive') return {met: profile.progress.archives.includes(rule.key), done: Number(profile.progress.archives.includes(rule.key)), total: 1};
    if (rule.type === 'all' || rule.type === 'any') {
      const values = rule.rules.map(r => condition(profile, r));
      return {met: rule.type === 'all' ? values.every(r => r.met) : values.some(r => r.met), done: values.filter(r => r.met).length, total: rule.type === 'all' ? values.length : 1};
    }
    return {met: false, done: 0, total: 1};
  }

  function rights(profile, id, nowMs) {
    const grants = profile.grants[id] || [];
    const permanent = grants.find(g => g.type === 'permanent' && g.status === 'active');
    if (permanent) return {allowed: true, status: 'permanent', source: permanent.source};
    const temporary = grants.find(g => g.type === 'temporary' && g.status === 'active' && Number.isFinite(g.validUntil) && g.validUntil > nowMs);
    if (temporary) return {allowed: true, status: 'temporary', source: temporary.source, validUntil: temporary.validUntil};
    if (grants.some(g => g.status === 'pending')) return {allowed: false, status: 'pending'};
    if (grants.some(g => g.status === 'revoked')) return {allowed: false, status: 'revoked'};
    if (grants.some(g => g.status === 'expired' || (g.type === 'temporary' && g.status === 'active' && g.validUntil <= nowMs))) return {allowed: false, status: 'expired'};
    return {allowed: false, status: 'none'};
  }

  function continuityGroup(value) {
    if (value === 'silver' || value === 'silver_timeline') return 'silver';
    if (String(value).startsWith('fracture')) return 'fractures';
    return 'core';
  }

  function compatibility(item, profile) {
    if (item.category === 'mode') return {allowed: true, reason: null};
    if (continuityGroup(item.continuity) !== profile.context.continuity) return {allowed: false, reason: 'continuity'};
    if (profile.context.workId && item.work_id !== profile.context.workId) return {allowed: false, reason: 'era'};
    return {allowed: true, reason: null};
  }

  function contentState(item, profile, catalog, nowMs) {
    const access = rights(profile, item.id, nowMs);
    const requirement = condition(profile, item.rule);
    const discovery = access.allowed || profile.preferences.hideSecrets === false ? 'identified' : (profile.discovery[item.id] || item.discovery || 'identified');
    const technical = item.technical || (item.asset ? 'available' : 'missing_assets');
    const compatible = compatibility(item, profile);
    const dependency = (item.requires || []).find(id => {
      const parent = catalog.find(c => c.id === id);
      return !parent || !rights(profile, id, nowMs).allowed || (parent.technical || (parent.asset ? 'available' : 'missing_assets')) !== 'available';
    });
    const claimable = access.status !== 'permanent' && requirement.met && item.claimable !== false;
    const obstacles = [];
    if (!access.allowed) obstacles.push(claimable ? 'claimable' : access.status === 'none' ? 'locked' : access.status);
    if (dependency) obstacles.push('dependency');
    if (technical !== 'available') obstacles.push(technical);
    if (!compatible.allowed) obstacles.push(compatible.reason);
    return {id: item.id, discovery, access, requirement, technical, compatible, dependency: dependency || null, claimable,
      selectable: access.allowed && technical === 'available' && compatible.allowed && !dependency,
      obstacles, name: discovery === 'identified' ? item.name : item.maskedName || 'Dossier non révélé',
      asset: discovery === 'secret' ? null : item.asset,
      showSilhouette: discovery === 'hint', workTitle: discovery === 'secret' ? 'Archive classifiée' : item.work_title};
  }

  function newProfile(catalog) {
    const p = {schemaVersion: SAVE_VERSION, rulesVersion: RULES.version, grants: {}, discovery: {},
      progress: {precisionBest: 0, flags: {assist: false, tag: false, duo: false}, archives: [], appliedRuns: []},
      selection: {activeId: 'jerome_hw2', reserveId: 'alice_hw2', stageId: 'st_blood_gulch_ce', costumeId: null, modeId: 'team_lab'},
      context: {continuity: 'core', workId: null}, preferences: {hideSecrets: true, reducedMotion: false, extendedBonus: false},
      nextRun: 1};
    catalog.filter(item => item.base).forEach(item => {
      p.grants[item.id] = [{source: `base/${item.id}`, type: 'permanent', status: 'active', revision: 1}];
      p.discovery[item.id] = 'identified';
    });
    return p;
  }

  function upsertGrant(profile, id, grant, catalog) {
    if (!catalog.some(item => item.id === id) || !validGrant(grant)) return {profile, ok: false, code: 'invalid_grant'};
    const prior = (profile.grants[id] || []).find(g => g.source === grant.source);
    if (prior && prior.revision >= grant.revision) return {profile, ok: true, code: 'duplicate_or_older'};
    const p = clone(profile);
    p.grants[id] = (p.grants[id] || []).filter(g => g.source !== grant.source).concat(clone(grant));
    if (grant.status === 'active') p.discovery[id] = 'identified';
    return {profile: p, ok: true, code: 'granted'};
  }

  function claim(profile, id, catalog, nowMs) {
    const item = catalog.find(c => c.id === id);
    if (!item) return {profile, ok: false, code: 'unknown_content'};
    const status = contentState(item, profile, catalog, nowMs);
    if (status.access.status === 'permanent') return {profile, ok: true, code: 'already_claimed'};
    if (!condition(profile, item.rule).met || item.claimable === false) return {profile, ok: false, code: 'requirements'};
    return upsertGrant(profile, id, {source: `reward/${id}`, type: 'permanent', status: 'active', revision: 1}, catalog);
  }

  function choose(profile, id, slot, catalog, nowMs) {
    const item = catalog.find(c => c.id === id);
    if (!item) return {profile, ok: false, code: 'unknown_content'};
    const kinds = {activeId: 'character', reserveId: 'character', stageId: 'stage', costumeId: 'costume', modeId: 'mode'};
    if (kinds[slot] !== item.category) return {profile, ok: false, code: 'wrong_slot'};
    const status = contentState(item, profile, catalog, nowMs);
    if (!status.selectable) return {profile, ok: false, code: status.obstacles[0] || 'unavailable'};
    if ((slot === 'activeId' && profile.selection.reserveId === id) || (slot === 'reserveId' && profile.selection.activeId === id)) return {profile, ok: false, code: 'duplicate_member'};
    const p = clone(profile), old = p.selection[slot];
    p.selection[slot] = id;
    return {profile: p, ok: true, code: 'selected', events: old === id ? [] : [{type: 'deselect', id: old, slot}, {type: 'select_confirm', id, slot}, {type: 'selection_idle', id, slot}]};
  }

  function eligibleCharacters(profile, catalog, nowMs, slot) {
    const other = slot === 'activeId' ? profile.selection.reserveId : profile.selection.activeId;
    return catalog.filter(item => item.category === 'character' && item.id !== other && contentState(item, profile, catalog, nowMs).selectable).map(item => item.id);
  }

  function startFromProfile(profile, catalog, nowMs) {
    for (const slot of ['activeId', 'reserveId', 'stageId', 'modeId']) {
      const item = catalog.find(c => c.id === profile.selection[slot]);
      if (!item || !contentState(item, profile, catalog, nowMs).selectable) return {ok: false, code: 'invalid_composition', slot};
    }
    if (profile.selection.activeId === profile.selection.reserveId) return {ok: false, code: 'duplicate_member'};
    return {ok: true, state: newCombat([profile.selection.activeId, profile.selection.reserveId], {stageId: profile.selection.stageId, runId: `match-${profile.nextRun}`})};
  }

  function applyMilestones(profile, events) {
    let p = profile;
    const mapping = {assist_hit: 'assist', tag_complete: 'tag', super_hit: 'duo'};
    for (const e of events) {
      const key = mapping[e.type];
      if (key && !(e.type === 'tag_complete' && e.forced) && !p.progress.flags[key]) { if (p === profile) p = clone(profile); p.progress.flags[key] = true; }
    }
    return p;
  }

  function visitArchive(profile, nodeId) {
    const prereq = {briefing: null, armory: 'briefing', records: 'armory'};
    if (!(nodeId in prereq)) return {profile, ok: false, code: 'unknown_archive'};
    if (prereq[nodeId] && !profile.progress.archives.includes(prereq[nodeId])) return {profile, ok: false, code: 'archive_access'};
    if (profile.progress.archives.includes(nodeId)) return {profile, ok: true, code: 'already_visited'};
    const p = clone(profile); p.progress.archives.push(nodeId);
    return {profile: p, ok: true, code: 'archive_opened'};
  }

  function validGrant(g) {
    return g && typeof g.source === 'string' && /^[a-z0-9_./-]{1,120}$/i.test(g.source)
      && ['permanent', 'temporary'].includes(g.type) && ['active', 'pending', 'expired', 'revoked'].includes(g.status)
      && finiteInt(g.revision, 1, 1000000000) && (g.type !== 'temporary' || (g.status === 'pending' && g.validUntil == null) || (Number.isFinite(g.validUntil) && g.validUntil > 0));
  }

  function readProfile(raw, catalog) {
    if (raw == null) return {ok: true, profile: newProfile(catalog), code: 'new'};
    if (typeof raw !== 'string' || raw.length > 200000) return {ok: false, code: 'invalid_save'};
    let value;
    try { value = JSON.parse(raw); } catch { return {ok: false, code: 'invalid_json'}; }
    if (!value || value.schemaVersion !== SAVE_VERSION) return {ok: false, code: 'unsupported_version'};
    const ids = new Set(catalog.map(item => item.id));
    if (!value.progress || !value.preferences || !value.selection || !value.context || !value.grants || !value.discovery) return {ok: false, code: 'invalid_save'};
    if (!finiteInt(value.progress.precisionBest, 0, 12) || !value.progress.flags ||
        !['assist', 'tag', 'duo'].every(k => typeof value.progress.flags[k] === 'boolean') ||
        !Array.isArray(value.progress.archives) || !value.progress.archives.every(n => ['briefing', 'armory', 'records'].includes(n)) ||
        !Array.isArray(value.progress.appliedRuns) || value.progress.appliedRuns.length > 512 ||
        !value.progress.appliedRuns.every(s => typeof s === 'string' && /^[a-z0-9_-]{1,80}$/i.test(s))) return {ok: false, code: 'invalid_progress'};
    if (!['core', 'silver', 'fractures'].includes(value.context.continuity) || ![null, 'h3'].includes(value.context.workId) ||
        !finiteInt(value.nextRun, 1, 1000000000)) return {ok: false, code: 'invalid_context'};
    for (const [id, grants] of Object.entries(value.grants)) {
      if (!ids.has(id) || !Array.isArray(grants) || grants.length > 32 || !grants.every(validGrant) || new Set(grants.map(g => g.source)).size !== grants.length) return {ok: false, code: 'invalid_grant'};
    }
    for (const [id, state] of Object.entries(value.discovery)) if (!ids.has(id) || !['secret', 'hint', 'identified'].includes(state)) return {ok: false, code: 'invalid_discovery'};
    for (const slot of ['activeId', 'reserveId', 'stageId', 'modeId', 'costumeId']) {
      if (value.selection[slot] !== null && !ids.has(value.selection[slot])) return {ok: false, code: 'invalid_selection'};
    }
    const p = newProfile(catalog);
    p.grants = clone(value.grants); p.discovery = clone(value.discovery);
    p.progress = {precisionBest: value.progress.precisionBest, flags: {assist: bool(value.progress.flags.assist), tag: bool(value.progress.flags.tag), duo: bool(value.progress.flags.duo)},
      archives: [...new Set(value.progress.archives)], appliedRuns: [...new Set(value.progress.appliedRuns)]};
    p.selection = Object.fromEntries(['activeId', 'reserveId', 'stageId', 'modeId', 'costumeId'].map(k => [k, value.selection[k]]));
    p.context = {continuity: value.context.continuity, workId: value.context.workId};
    p.preferences = {hideSecrets: value.preferences.hideSecrets !== false, reducedMotion: bool(value.preferences.reducedMotion), extendedBonus: bool(value.preferences.extendedBonus)};
    p.nextRun = value.nextRun;
    return {ok: true, profile: p, code: 'loaded'};
  }

  function newCombat(ids, options) {
    if (!Array.isArray(ids) || ids.length !== 2 || ids[0] === ids[1] || ids.some(id => typeof id !== 'string' || !id)) throw new Error('Two distinct fighter IDs are required.');
    const opt = options || {};
    return {rulesVersion: RULES.version, runId: opt.runId || 'match-1', frame: 0, eventSeq: 0, activeId: ids[0], stageId: opt.stageId || 'st_blood_gulch_ce',
      members: ids.map(id => ({id, hp: RULES.health, cooldown: 0, ko: false})), gauge: RULES.gaugeInitial,
      opponentHp: RULES.opponentHealth, opponentKind: opt.opponentKind || 'training_construct', targetMode: 'hit',
      phase: 'fight', paused: false, hitstop: 0, activeAction: null, supportAction: null, teamAction: null,
      combo: {hits: 0, gaugeGain: 0, sinceHit: RULES.comboReset}, finisherRemaining: 0, finish: null, log: []};
  }

  function commonGate(s) {
    if (s.paused) return 'paused';
    if (s.hitstop) return 'hitstop';
    if (s.phase !== 'fight') return 'not_fighting';
    if (!active(s) || active(s).ko) return 'active_ko';
    if (s.teamAction) return 'team_busy';
    if (s.activeAction) return s.activeAction.type === 'hitstun' ? 'hitstun' : 'active_busy';
    return null;
  }
  function partnerGate(s) {
    const p = reserve(s);
    if (!p || p.ko) return 'partner_ko';
    if (s.supportAction) return 'partner_busy';
    if (p.cooldown > 0) return 'partner_cooldown';
    return null;
  }

  function resolveFinisher(s) {
    if (s.members.some(m => m.ko) || s.supportAction || reserve(s).cooldown > 0) return {type: 'normal_victory', label: 'Victoire standard', reason: 'partner_unavailable'};
    const team = s.members.map(m => m.id).sort().join('|');
    if (team === 'ntho_h3|usze_h3' && s.stageId === 'st_valhalla_h3' && s.opponentKind === 'brute_h3')
      return {type: 'specific_original', label: 'Coordination sangheili', reason: 'original_choreography_not_canon_event'};
    return {type: 'generic_original', label: 'Neutralisation coordonnée', reason: 'simulation_not_historical_scene'};
  }

  function command(input, cmd) {
    if (!cmd || typeof cmd.type !== 'string') return deny(input, 'invalid_command');
    if (cmd.type === 'pause') { const s = clone(input); s.paused = !s.paused; return succeed(s, []); }
    if (cmd.type === 'target') {
      if (!['hit', 'block', 'miss'].includes(cmd.mode)) return deny(input, 'invalid_target');
      const s = clone(input); s.targetMode = cmd.mode; return succeed(s, []);
    }
    if (cmd.type === 'damage') return applyDamage(input, cmd);
    if (cmd.type === 'skip') {
      if (input.paused) return deny(input, 'paused');
      if (!input.teamAction || !['super_scene', 'finisher'].includes(input.teamAction.type)) return deny(input, 'no_scene');
      return step(input, input.teamAction.duration - input.teamAction.elapsed);
    }
    if (cmd.type === 'cancel_taunt') {
      if (input.paused) return deny(input, 'paused');
      if (!input.activeAction || input.activeAction.type !== 'taunt' || input.activeAction.elapsed < RULES.taunt.cancelAt) return deny(input, 'taunt_cancel_window');
      const s = clone(input), out = []; s.activeAction.duration = Math.min(s.activeAction.duration, s.activeAction.elapsed + RULES.taunt.exit);
      event(s, out, 'taunt_exit', {actor: s.activeId}); return succeed(s, out);
    }
    if (cmd.type === 'finisher') {
      if (input.paused) return deny(input, 'paused');
      if (input.phase !== 'finish_window' || input.finisherRemaining <= 0) return deny(input, 'no_finish_window');
      const finish = resolveFinisher(input);
      if (finish.type === 'normal_victory') return deny(input, 'partner_unavailable');
      const s = clone(input), out = []; s.finish = finish; s.phase = 'presentation';
      s.teamAction = {type: 'finisher', elapsed: 0, duration: RULES.finisher.duration};
      event(s, out, 'finisher_begin', {scene: finish.type}); return succeed(s, out);
    }
    if (!['normal', 'taunt', 'assist', 'tag', 'super'].includes(cmd.type)) return deny(input, 'unknown_command');
    const gate = commonGate(input); if (gate) return deny(input, gate);
    if (['assist', 'tag', 'super'].includes(cmd.type)) { const partner = partnerGate(input); if (partner) return deny(input, partner); }
    const cost = ({assist: RULES.assist.cost, tag: RULES.tag.cost, super: RULES.super.cost})[cmd.type] || 0;
    if (input.gauge < cost) return deny(input, 'gauge');
    const s = clone(input), out = []; s.gauge -= cost;
    if (cmd.type === 'normal') s.activeAction = {type: 'normal', actor: s.activeId, elapsed: 0, duration: RULES.normal.duration, outcome: s.targetMode};
    if (cmd.type === 'taunt') s.activeAction = {type: 'taunt', actor: s.activeId, elapsed: 0, duration: RULES.taunt.duration};
    if (cmd.type === 'assist') s.supportAction = {type: 'assist', actor: reserve(s).id, elapsed: 0, duration: RULES.assist.enter + RULES.assist.active + RULES.assist.exit, outcome: s.targetMode};
    if (cmd.type === 'tag') s.teamAction = {type: 'tag', from: s.activeId, to: reserve(s).id, elapsed: 0, duration: RULES.tag.duration, forced: false};
    if (cmd.type === 'super') s.teamAction = {type: 'super_open', actor: s.activeId, partner: reserve(s).id, elapsed: 0, duration: RULES.super.opener, outcome: s.targetMode};
    event(s, out, `${cmd.type}_begin`, {actor: s.activeId, partner: reserve(s).id, cost});
    return succeed(s, out);
  }

  function endFight(s, out) {
    if (s.opponentHp > 0 || s.phase !== 'fight' || s.teamAction) return;
    s.phase = 'finish_window'; s.finisherRemaining = RULES.finisher.window; s.activeAction = null;
    if (s.supportAction) { member(s, s.supportAction.actor).cooldown = Math.max(member(s, s.supportAction.actor).cooldown, RULES.assist.cooldown); s.supportAction = null; }
    event(s, out, 'victory_confirmed', {winner: 'team'});
  }

  function impact(s, out, type, actor, damage, gain) {
    if (s.opponentHp <= 0 || s.phase !== 'fight') return;
    s.opponentHp = Math.max(0, s.opponentHp - damage);
    if (gain) {
      const amount = Math.min(RULES.hitGain, RULES.comboGainLimit - s.combo.gaugeGain);
      s.gauge = clamp(s.gauge + amount, 0, RULES.gaugeMax); s.combo.gaugeGain += amount;
    }
    s.combo.hits++; s.combo.sinceHit = 0;
    event(s, out, type, {actor, damage, target: 'opponent'});
  }

  function applyDamage(input, cmd) {
    if (input.paused || input.phase !== 'fight') return deny(input, input.paused ? 'paused' : 'not_fighting');
    if (input.teamAction && ['super_scene', 'finisher'].includes(input.teamAction.type)) return deny(input, 'scene_committed');
    if (!finiteInt(cmd.amount, 1, RULES.health)) return deny(input, 'invalid_damage');
    const targetId = cmd.target === 'reserve' ? reserve(input).id : input.activeId;
    if (member(input, targetId).ko) return deny(input, 'already_ko');
    if (cmd.target === 'reserve' && (!input.supportAction || input.supportAction.actor !== targetId)) return deny(input, 'reserve_offstage');
    const s = clone(input), out = [], target = member(s, targetId);
    target.hp = Math.max(0, target.hp - cmd.amount); target.ko = target.hp === 0;
    if (s.supportAction && s.supportAction.actor === targetId) {
      s.supportAction = null; target.cooldown = Math.max(target.cooldown, RULES.assist.cooldown);
      event(s, out, 'assist_interrupted', {actor: targetId});
    }
    if (targetId === s.activeId) {
      s.activeAction = target.ko ? null : {type: 'hitstun', elapsed: 0, duration: RULES.hitstun};
      if (s.teamAction) { event(s, out, 'team_interrupted', {typeInterrupted: s.teamAction.type}); s.teamAction = null; }
    }
    event(s, out, target.ko ? 'fighter_ko' : 'fighter_hit', {actor: targetId, damage: cmd.amount});
    if (s.members.every(m => m.ko)) { s.phase = 'defeat'; s.activeAction = null; s.supportAction = null; s.teamAction = null; event(s, out, 'defeat_confirmed'); }
    else if (active(s).ko) {
      if (s.supportAction) { member(s, s.supportAction.actor).cooldown = Math.max(member(s, s.supportAction.actor).cooldown, RULES.assist.cooldown); s.supportAction = null; }
      s.teamAction = {type: 'tag', from: s.activeId, to: reserve(s).id, elapsed: 0, duration: RULES.tag.duration, forced: true};
      event(s, out, 'tag_after_ko', {to: reserve(s).id, cost: 0});
    }
    return succeed(s, out);
  }

  function step(input, frames) {
    if (!finiteInt(frames, 0, 36000)) return deny(input, 'invalid_frames');
    if (input.paused || frames === 0) return succeed(input, []);
    const s = clone(input), out = [];
    for (let i = 0; i < frames; i++) {
      if (['victory', 'defeat'].includes(s.phase)) break;
      s.frame++;
      if (s.hitstop > 0) { s.hitstop--; continue; }
      const frozen = s.teamAction && ['super_scene', 'finisher'].includes(s.teamAction.type);
      if (!frozen) {
        s.members.forEach(m => { m.cooldown = Math.max(0, m.cooldown - 1); });
        s.combo.sinceHit++;
        if (s.combo.sinceHit >= RULES.comboReset) { s.combo.hits = 0; s.combo.gaugeGain = 0; }
      }
      if (s.phase === 'finish_window') {
        if (--s.finisherRemaining <= 0) { s.phase = 'victory'; s.finish = {type: 'normal_victory', label: 'Victoire standard'}; event(s, out, 'victory_presentation'); }
        continue;
      }
      if (s.activeAction && !frozen) {
        const a = s.activeAction; a.elapsed++;
        if (a.type === 'normal' && a.elapsed === RULES.normal.impact) {
          if (a.outcome === 'hit') impact(s, out, 'normal_hit', a.actor, RULES.normal.damage, true);
          else event(s, out, a.outcome === 'block' ? 'normal_blocked' : 'normal_missed', {actor: a.actor});
        }
        if (a.elapsed >= a.duration) { event(s, out, `${a.type}_complete`, {actor: a.actor || s.activeId}); s.activeAction = null; }
      }
      if (s.supportAction && !frozen) {
        const a = s.supportAction; a.elapsed++;
        if (a.elapsed === RULES.assist.enter) {
          if (a.outcome === 'hit') impact(s, out, 'assist_hit', a.actor, RULES.assist.damage, false);
          else event(s, out, a.outcome === 'block' ? 'assist_blocked' : 'assist_missed', {actor: a.actor});
        }
        if (a.elapsed >= a.duration) {
          member(s, a.actor).cooldown = Math.max(member(s, a.actor).cooldown, RULES.assist.cooldown);
          event(s, out, 'assist_exit', {actor: a.actor}); s.supportAction = null;
        }
      }
      if (s.teamAction) {
        const a = s.teamAction; a.elapsed++;
        if (a.type === 'tag' && a.elapsed === RULES.tag.transfer) {
          s.activeId = a.to;
          member(s, a.from).cooldown = Math.max(member(s, a.from).cooldown, RULES.tag.outgoingCooldown);
          event(s, out, 'control_transferred', {from: a.from, to: a.to, forced: a.forced});
        }
        if (a.elapsed >= a.duration) {
          if (a.type === 'super_open') {
            if (a.outcome === 'hit') {
              s.teamAction = {...a, type: 'super_scene', elapsed: 0, duration: RULES.super.hitDuration - RULES.super.opener};
              event(s, out, 'super_confirmed', {actor: a.actor, partner: a.partner});
            } else {
              if (a.outcome === 'block') { s.opponentHp = Math.max(0, s.opponentHp - RULES.super.chip); event(s, out, 'super_blocked', {damage: RULES.super.chip}); }
              else event(s, out, 'super_missed');
              s.teamAction = {...a, type: 'super_recovery', elapsed: 0, duration: (a.outcome === 'block' ? RULES.super.blockDuration : RULES.super.missDuration) - RULES.super.opener};
            }
          } else if (a.type === 'super_scene') {
            impact(s, out, 'super_hit', a.actor, RULES.super.damage, false);
            s.teamAction = null; event(s, out, 'super_complete', {activeId: s.activeId});
          } else if (a.type === 'finisher') {
            s.phase = 'victory'; s.teamAction = null; event(s, out, 'finisher_complete', {winner: 'team', scene: s.finish.type});
          } else {
            event(s, out, `${a.type}_complete`, {activeId: s.activeId, forced: !!a.forced}); s.teamAction = null;
          }
        }
      }
      endFight(s, out);
    }
    return succeed(s, out);
  }

  function actionAvailability(s) {
    return Object.fromEntries(['normal', 'assist', 'tag', 'super', 'taunt', 'finisher'].map(type => {
      const result = command(s, {type}); return [type, {allowed: result.ok, code: result.code}];
    }));
  }

  function newBonus(runId, extended) {
    const speed = extended ? 3 : 1;
    return {runId, frame: 0, duration: 1800 * speed, interval: 120 * speed, ttl: 240 * speed,
      planned: 12, spawned: 0, hits: 0, misses: 0, targets: [], finished: false, success: false, extended: !!extended};
  }

  function stepBonus(input, frames) {
    if (!finiteInt(frames, 0, 36000)) return {state: input, ok: false};
    if (input.finished) return {state: input, ok: true};
    const s = clone(input);
    for (let i = 0; i < frames; i++) {
      s.frame++;
      const expired = s.targets.filter(t => t.expires <= s.frame);
      s.misses += expired.length; s.targets = s.targets.filter(t => t.expires > s.frame);
      if ((s.frame === 1 || s.frame % s.interval === 0) && s.spawned < s.planned) {
        const n = ++s.spawned;
        s.targets.push({id: `${s.runId}-${n}`, number: n, x: 12 + (n * 37 % 75), y: 15 + (n * 23 % 58), expires: s.frame + s.ttl});
      }
      if (s.frame >= s.duration || (s.spawned === s.planned && s.targets.length === 0)) {
        s.misses += s.targets.length; s.targets = []; s.finished = true; s.success = s.hits >= 8; break;
      }
    }
    return {state: s, ok: true};
  }

  function hitBonus(input, id) {
    if (input.finished || !input.targets.some(t => t.id === id)) return {state: input, ok: false, code: 'target_unavailable'};
    const s = clone(input); s.targets = s.targets.filter(t => t.id !== id); s.hits++;
    if (s.spawned === s.planned && !s.targets.length) { s.finished = true; s.success = s.hits >= 8; }
    return {state: s, ok: true, code: 'target_hit'};
  }

  function recordBonus(profile, bonus) {
    if (!bonus.finished || !finiteInt(bonus.hits, 0, 12) || typeof bonus.runId !== 'string') return {profile, ok: false, code: 'unfinished_bonus'};
    if (profile.progress.appliedRuns.includes(bonus.runId)) return {profile, ok: true, code: 'duplicate_result'};
    const p = clone(profile); p.progress.precisionBest = Math.max(p.progress.precisionBest, bonus.hits);
    p.progress.appliedRuns.push(bonus.runId); if (p.progress.appliedRuns.length > 512) p.progress.appliedRuns.shift();
    return {profile: p, ok: true, code: 'bonus_recorded'};
  }

  const api = {RULES, SAVE_VERSION, SAVE_KEY, clone, condition, rights, continuityGroup, compatibility, contentState,
    newProfile, upsertGrant, claim, choose, eligibleCharacters, startFromProfile, applyMilestones, visitArchive,
    readProfile, newCombat, command, step, resolveFinisher, actionAvailability, newBonus, stepBonus, hitBonus, recordBonus};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.HaloExtensions = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
