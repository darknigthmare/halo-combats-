/* Halo Combats V7. Local static study poses over the V1 mechanical simulation.
 * PNGs are always drawn complete, with positive dimensions and their native facing.
 * The V1 attack timings/collisions remain shared by all 24 selectable identities.
 */
(() => {
'use strict';
const lab = { data: null, ready: false, view: 'lab', p1: null, p2: null, stage: null, catalog: [], selected: null, variant: null, previewToken: 0, poseText: '', renderCalls: 0 };
const repoRoot = new URL('../', window.location.href);
const statusLabels = { candidate: 'Candidat', needs_correction: 'À corriger', missing: 'Manquant' };
const facingLabels = { right: 'Droite', left: 'Gauche', front: 'Face', unknown: 'Non déterminée' };
const kindLabels = { base: 'ROSTER DE BASE', expansion: 'EXTENSION · CATALOGUE', boss: 'BOSS / VÉHICULE', stage: 'DÉCOR' };
function localAssetURL(path) {
  if (typeof path !== 'string' || !path || path.startsWith('/') || path.includes('\\') || path.split('/').includes('..') || /^[a-z][a-z\d+.-]*:/i.test(path)) throw new Error('Chemin local invalide');
  return new URL(path, repoRoot).href;
}
function textNode(tag, text = '', className = '') { const el = document.createElement(tag); el.textContent = text; if (className) el.className = className; return el; }
function statusOf(entry) { return statusLabels[entry?.status] ? entry.status : entry?.path ? 'candidate' : 'missing'; }
function resolveAsset(ref) {
  if (!ref) return null;
  const record = typeof ref === 'string' ? lab.data?.assets_index?.[ref] : ref;
  if (!record) return null;
  const full = lab.data?.assets_index?.[record.asset_id || record.id];
  return full ? { ...full, ...record } : record;
}
function preferredAsset(entity) { return resolveAsset(entity?.preferred_asset) || resolveAsset(entity?.variants?.find(v => v.preferred)) || resolveAsset(entity?.variants?.[0]); }

// At most 10 decoded images are retained; two image requests may be in flight.
// Only the current fighters, background, boss and catalogue preview are pinned.
class ImageCache {
  constructor(limit = 10, concurrent = 2) { this.limit = limit; this.concurrent = concurrent; this.records = new Map(); this.queue = []; this.active = 0; this.serial = 0; this.pins = new Set(); }
  pin(paths) {
    this.pins = new Set(paths.filter(Boolean));
    // Rapid selection changes discard requests that have not started, so the
    // current roster does not wait behind an obsolete catalogue queue.
    this.queue = this.queue.filter(record => {
      if (this.pins.has(record.path)) return true;
      record.state = 'cancelled'; this.records.delete(record.path); record.resolve(record); return false;
    });
    this.trim();
  }
  get(asset) {
    if (!asset?.path) return { state: 'missing', image: null };
    let record = this.records.get(asset.path);
    if (!record) {
      record = { path: asset.path, state: 'queued', image: null, used: ++this.serial, error: null, promise: null };
      record.promise = new Promise(resolve => { record.resolve = resolve; });
      this.records.set(asset.path, record); this.queue.push(record); this.pump();
    }
    record.used = ++this.serial;
    return record;
  }
  pump() {
    while (this.active < this.concurrent && this.queue.length) {
      const record = this.queue.shift(); this.active++; record.state = 'loading';
      const image = new Image(); image.decoding = 'async';
      const done = (ok, error) => {
        image.onload = image.onerror = null;
        record.state = ok ? 'ready' : 'error'; record.image = ok ? image : null;
        record.error = ok ? null : String(error || 'Fichier image indisponible');
        this.active--; this.trim(); record.resolve(record); this.pump();
        if (lab.ready) { updatePoseReadout(); draw(); }
      };
      image.onload = () => { if (image.naturalWidth && image.naturalHeight) done(true); else done(false, 'Image sans dimensions'); };
      image.onerror = () => done(false, 'Le PNG local ne peut pas être chargé');
      try { image.src = localAssetURL(record.path); } catch (error) { done(false, error.message); }
    }
  }
  trim() {
    let ready = [...this.records.values()].filter(r => r.state === 'ready');
    while (ready.length > this.limit) {
      const candidates = ready.filter(r => !this.pins.has(r.path)).sort((a, b) => a.used - b.used);
      const victim = candidates[0] || ready.slice().sort((a, b) => a.used - b.used)[0];
      victim.image = null; this.records.delete(victim.path); ready = ready.filter(r => r !== victim);
    }
  }
  stats() { const rows = [...this.records.values()]; return { maxRetained: this.limit, maxConcurrent: this.concurrent, ready: rows.filter(r => r.state === 'ready').length, loading: this.active, queued: this.queue.length, errors: rows.filter(r => r.state === 'error').length, estimatedDecodedBytes: rows.reduce((n, r) => n + (r.image ? r.image.naturalWidth * r.image.naturalHeight * 4 : 0), 0) }; }
}
const imageCache = new ImageCache();

// V1 mechanical rules, retained without fighter-specific movesets.
const canvas=document.getElementById('game'),ctx=canvas.getContext('2d');
const $=id=>document.getElementById(id), W=1280,H=650,FLOOR=515,WORLD=3100;
const input={held:new Set(),queue:[]};let tick=0,mode='training',paused=false,ended=false,hitstop=0,shake=0,camera=0,roundTimer=99*60,lastTime=0,accumulator=0,particles=[],shots=[],zones=[],combo=0,comboUntil=0,roundNotice=0,seed=9517;
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));const rnd=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296};
const actions={light:{startup:6,active:4,recovery:10,reach:85,damage:48,stun:16,push:8},heavy:{startup:16,active:5,recovery:22,reach:120,damage:112,stun:26,push:18},shoot:{startup:9,active:1,recovery:19},grenade:{startup:15,active:1,recovery:28},special:{startup:12,active:6,recovery:30,reach:190,damage:175,stun:35,push:25},dash:{startup:0,active:12,recovery:8}};
function fighter(x,elite=false){return{x,y:FLOOR,vx:0,vy:0,w:52,h:98,face:elite?-1:1,hp:1000,maxhp:1000,shield:200,maxshield:200,energy:0,grenades:2,grenadeRegen:0,stun:0,guard:false,action:null,cooldown:0,hitAt:-999,elite,dead:false,aiNext:0};}
let p,e,boss;
function reset(next=mode){mode=next;tick=0;seed=9517;paused=false;ended=false;hitstop=0;shake=0;shots=[];particles=[];zones=[];input.held.clear();input.queue=[];combo=0;comboUntil=0;roundTimer=99*60;p=fighter(mode==='boss'?1170:1100);e=fighter(1540,true);camera=mode==='boss'?820:720;boss={phase:1,legs:[{x:1430,hp:320,max:320},{x:2160,hp:320,max:320}],core:{x:1860,y:225,hp:450,max:450},nextAttack:140,attacks:0};roundNotice=100;$('banner').classList.add('hidden');$('pause').textContent='Pause';document.querySelectorAll('[data-mode]').forEach(b=>b.classList.toggle('active',b.dataset.mode===mode));document.querySelectorAll('.touch .held').forEach(b=>b.classList.remove('held'));$('mode-label').textContent=mode==='boss'?'BOSS BATTLE':mode==='duel'?'DUEL':'ENTRAÎNEMENT';$('enemy-name').textContent=mode==='boss'?'SCARAB · STRUCTURE':mode==='duel'?'ELITE · IA':'ELITE · MANNEQUIN';$('report-label').textContent=mode==='boss'?'LECTURE DU BOSS':'RETOUR D ENTRAÎNEMENT';$('status').textContent=mode==='boss'?'Évitez le marquage rouge. Les jambes brillantes sont vulnérables.':'Approchez votre adversaire. Les impacts alimentent votre énergie.';updateHUD();refreshFighterLabels();draw();}
function enqueue(a){if(paused||ended)return;input.queue.push({a,expires:tick+8});if(input.queue.length>12)input.queue.shift();}
function start(f,a){if(f.dead||f.stun||f.action||f.cooldown)return false;if(a==='jump'){if(Math.abs(f.y-ground(f))>.1)return false;f.vy=-13.4;return true;}if(a==='interact'){if(mode==='boss'&&(boss.phase===2||(boss.phase===3&&f.y>400))&&Math.abs(f.x-1750)<135){f.x=1700;f.y=268;f.vy=0;boss.phase=3;boss.nextAttack=tick+140;$('status').textContent='Pont atteint. Le noyau magenta est vulnérable aux coups, tirs et grenades.';return true;}return false;}if(!actions[a])return false;if(a==='grenade'&&f.grenades<1)return false;if(a==='special'&&f.energy<100){if(f===p)$('status').textContent='Impulsion : une barre d’énergie est nécessaire.';return false;}if(a==='grenade'){f.grenades--;f.grenadeRegen=0;}if(a==='special')f.energy-=100;f.action={type:a,frame:0,hit:new Set()};f.guard=false;return true;}
function ground(f){return mode==='boss'&&boss.phase===3&&f.x>=1440&&f.x<=2190&&f.y<330?268:FLOOR;}
function pushParticle(x,y,col,count=10){for(let i=0;i<count;i++)particles.push({x,y,vx:(rnd()-.5)*7,vy:(rnd()-.6)*7,life:18+rnd()*15,col});}
function damage(f,amount,sourceX,push=5,stun=10){if(f.dead)return 0;const block=f.guard&&Math.sign(sourceX-f.x)===f.face;amount=Math.round(amount*(block?.18:1));const absorbed=Math.min(f.shield,amount);f.shield-=absorbed;f.hp=Math.max(0,f.hp-(amount-absorbed));f.hitAt=tick;f.stun=block?7:stun;if(!block)f.action=null;f.vx=Math.sign(f.x-sourceX)*push*(block?.3:1);f.energy=clamp(f.energy+amount*.12,0,300);pushParticle(f.x,f.y-60,absorbed?'#8cf1f3':'#ffb976',block?5:12);hitstop=block?2:4;shake=block?1:4;if(f.hp===0){f.dead=true;f.stun=90;}return amount;}
function attackBoss(x,y,reach,amount,owner,hitset,tag){if(owner!==p||mode!=='boss')return;let hit=false;if(boss.phase===1){boss.legs.forEach((l,i)=>{if(l.hp>0&&Math.abs(x-l.x)<reach+45&&y>365&&!hitset.has('leg'+i)){hitset.add('leg'+i);l.hp=Math.max(0,l.hp-amount);pushParticle(l.x,FLOOR-40,'#8ff0cf',17);hit=true;}});if(boss.legs.every(l=>l.hp===0)){boss.phase=2;zones=[];shots=shots.filter(s=>s.owner===p);$('status').textContent='Scarab immobilisé. Rejoignez la balise centrale puis E ou Monter.';}}else if(boss.phase===3&&Math.abs(x-boss.core.x)<reach+45&&Math.abs(y-(boss.core.y-18))<120&&!hitset.has('core')){hitset.add('core');boss.core.hp=Math.max(0,boss.core.hp-amount);pushParticle(boss.core.x,boss.core.y-35,'#f6a2ff',22);hit=true;if(boss.core.hp===0)finish(true,'SCARAB NEUTRALISÉ','Jambes brisées, pont atteint et noyau détruit.');}if(hit){p.energy=clamp(p.energy+amount*.2,0,300);hitstop=4;shake=4;combo++;comboUntil=tick+90;$('report').textContent='Impact sur '+(boss.phase===3?'le noyau':'la jambe')+' · '+amount+' dégâts. '+(tag==='special'?'Impulsion consommée.':'');}}
function updateAction(f){if(!f.action)return;let a=f.action,def=actions[a.type];a.frame++;if(a.type==='dash'){f.vx=f.face*12;if(a.frame>=20)f.action=null;return;}if(a.frame===def.startup){if(a.type==='shoot'){shots.push({x:f.x+f.face*45,y:f.y-63,vx:f.face*15,vy:0,r:5,life:85,damage:42,owner:f,type:'bolt',hits:new Set()});}if(a.type==='grenade'){shots.push({x:f.x+f.face*35,y:f.y-68,vx:f.face*6.3,vy:-8,r:8,life:70,damage:155,owner:f,type:'grenade',hits:new Set()});}}
if(def.reach&&a.frame>=def.startup&&a.frame<def.startup+def.active){let hx=f.x+f.face*def.reach*.6,hy=f.y-50,enemy=f===p?e:p;if(mode!=='boss'&&Math.abs(enemy.x-hx)<def.reach*.7+enemy.w/2&&Math.abs((enemy.y-50)-hy)<75&&!a.hit.has(enemy)){a.hit.add(enemy);const dealt=damage(enemy,def.damage,f.x,def.push,def.stun);f.energy=clamp(f.energy+dealt*.22,0,300);if(f===p){combo++;comboUntil=tick+90;$('report').textContent='Enchaînement '+combo+' · '+dealt+' dégâts · '+a.type+' ('+def.startup+' frames de démarrage).';}}if(mode==='boss'){attackBoss(hx,hy,def.reach*.65,def.damage,f,a.hit,a.type);}}
if(a.frame>=def.startup+def.active+def.recovery)f.action=null;}
function updateFighter(f){if(f.stun>0)f.stun--;if(f.cooldown>0)f.cooldown--;if(tick-f.hitAt>240&&!f.dead)f.shield=clamp(f.shield+1.15,0,f.maxshield);if(++f.grenadeRegen>420&&f.grenades<2){f.grenades++;f.grenadeRegen=0;}updateAction(f);f.x+=f.vx;f.y+=f.vy;f.vy+=.7;f.vx*=.78;f.x=clamp(f.x,60,WORLD-60);let floor=ground(f);if(f.y>=floor){f.y=floor;f.vy=0;}if(f.y>FLOOR){f.y=FLOOR;f.vy=0;}}
function ai(){if(mode!=='duel'||e.dead||e.stun)return;const d=p.x-e.x;e.face=Math.sign(d)||e.face;if(e.action)return;e.guard=tick<(e.guardUntil||0);if(e.guard)return;if(tick<e.aiNext){if(Math.abs(d)>125)e.vx=e.face*2.4;return;}e.aiNext=tick+20+Math.floor(rnd()*28);if(p.action&&Math.abs(d)<170&&rnd()<.3){e.guard=true;e.guardUntil=tick+18;e.aiNext=tick+18;}else if(Math.abs(d)<110)start(e,rnd()<.7?'light':'heavy');else if(Math.abs(d)<500&&rnd()<.6)start(e,'shoot');else{e.vx=e.face*3.3;if(rnd()<.13)start(e,'grenade');}}
function explosion(s){pushParticle(s.x,s.y,'#ffcb76',35);shake=7;const target=s.owner===p?e:p;if(mode!=='boss'&&Math.hypot(target.x-s.x,target.y-50-s.y)<155)damage(target,s.damage,s.x,16,24);if(mode==='boss')attackBoss(s.x,s.y,150,s.damage,s.owner,s.hits,'grenade');}
function updateShots(){for(const s of shots){s.life--;s.x+=s.vx;s.y+=s.vy;if(s.type==='grenade'){s.vy+=.35;const floor=mode==='boss'&&boss.phase===3&&s.x>1440&&s.x<2190&&s.y<330?268:FLOOR;if(s.y>floor-8){s.y=floor-8;s.vy*=-.42;s.vx*=.8;}if(s.life<=0)explosion(s);}else{let target=s.owner===p?e:p;if(mode!=='boss'&&Math.abs(s.x-target.x)<target.w/2+s.r&&s.y>target.y-target.h&&s.y<target.y){damage(target,s.damage,s.x,5,9);s.owner.energy=clamp(s.owner.energy+9,0,300);s.life=0;}if(mode==='boss'&&s.owner===p){let count=s.hits.size;attackBoss(s.x,s.y,10,s.damage,s.owner,s.hits,'shoot');if(s.hits.size>count)s.life=0;}if(mode==='boss'&&s.owner!==p&&Math.abs(s.x-p.x)<p.w/2+s.r&&s.y>p.y-p.h&&s.y<p.y){damage(p,s.damage,s.x,10,15);s.life=0;}}}shots=shots.filter(s=>s.life>0&&s.x>-100&&s.x<WORLD+100);}
function bossAI(){if(mode!=='boss'||ended||boss.phase===2)return;if(tick>=boss.nextAttack){boss.attacks++;let kind=boss.phase===3?'pulse':boss.attacks%3===0?'stomp':'beam',x=p.x,width=kind==='stomp'?190:kind==='pulse'?150:110;zones.push({x,width,kind,start:tick,impact:tick+(kind==='beam'?85:65),life:tick+(kind==='beam'?105:80),hit:false});boss.nextAttack=tick+(boss.phase===3?155:185);}$('report').textContent=boss.phase===1?'Phase 1 · Approchez une jambe lumineuse et attaquez. Les attaques lourdes suffisent.':boss.phase===3?'Phase 3 · Détruisez le noyau. Quittez les zones rouges avant l’impact.':'Phase 2 · Boarding';}
function updateZones(){for(const z of zones){if(tick>=z.impact&&!z.hit){z.hit=true;shake=8;pushParticle(z.x,ground(p)-10,'#ff7777',25);if(Math.abs(p.x-z.x)<z.width/2+p.w/2&&(z.kind==='beam'||p.y>=ground(p)-65))damage(p,z.kind==='beam'?155:120,z.x+1,16,24);}}zones=zones.filter(z=>tick<z.life);}
function finish(win,title,body){ended=true;input.held.clear();input.queue=[];$('banner-title').textContent=title||(win?'VICTOIRE':'DÉFAITE');$('banner-text').textContent=body||'Recommencer pour lancer une nouvelle manche.';$('banner').classList.remove('hidden');$('status').textContent=win?'Objectif accompli. Vous pouvez relancer ou changer de mode.':'Manche terminée. Recommencer pour réessayer.';}
function step(){if(paused||ended)return;tick++;if(hitstop){hitstop--;return;}if(combo&&tick>comboUntil)combo=0;if(roundNotice>0)roundNotice--;if(p.stun===0&&!p.dead){const left=input.held.has('left'),right=input.held.has('right');p.guard=input.held.has('guard')&&!p.action&&p.y===ground(p);if(!p.action){if(left!==right){p.face=right?1:-1;p.vx=p.face*(p.guard?1.5:4.4);}else p.vx*=.7;}input.queue=input.queue.filter(q=>q.expires>=tick);for(let i=0;i<input.queue.length;i++)if(start(p,input.queue[i].a)){input.queue.splice(i,1);break;}}ai();updateFighter(p);if(mode!=='boss'){updateFighter(e);if(!p.action&&!input.held.has('left')&&!input.held.has('right'))p.face=Math.sign(e.x-p.x)||p.face;if(Math.abs(p.x-e.x)<49&&Math.abs(p.y-e.y)<70){const diff=49-Math.abs(p.x-e.x),side=Math.sign(p.x-e.x)||-1;p.x+=side*diff/2;e.x-=side*diff/2;}}bossAI();updateShots();updateZones();for(const pt of particles){pt.x+=pt.vx;pt.y+=pt.vy;pt.vy+=.1;pt.life--;}particles=particles.filter(pt=>pt.life>0);if(shake>0)shake*=.8;
if(mode==='training'){p.energy=300;if(e.dead&&e.stun===0){e=fighter(1540,true);p=fighter(1100);p.energy=300;combo=0;shots=[];$('status').textContent='Mannequin réinitialisé. Recommencez un enchaînement.';}if(p.dead&&p.stun===0){p=fighter(1100);p.energy=300;}}else if(mode==='duel'){roundTimer--;if(e.dead)finish(true);else if(p.dead)finish(false);else if(roundTimer<=0)finish(p.hp+p.shield>=e.hp+e.shield,'TEMPS ÉCOULÉ',p.hp+p.shield>=e.hp+e.shield?'Victoire aux points de vie restants.':'Défaite aux points de vie restants.');}else if(p.dead)finish(false,'JOUEUR HORS COMBAT','Recommencer relance le Scarab depuis les jambes.');camera+=(clamp(p.x-W*.38,0,WORLD-W)-camera)*.08;updateHUD();}
function updateHUD(){const bar=(id,v,max)=>$(id).style.width=clamp(v/max*100,0,100)+'%';bar('phealth',p.hp,p.maxhp);bar('pshield',p.shield,p.maxshield);$('pvalue').textContent=Math.ceil(p.hp)+' PV · '+Math.ceil(p.shield)+' bouclier';if(mode==='boss'){let v=boss.phase<3?boss.legs.reduce((s,l)=>s+l.hp,0):boss.core.hp,max=boss.phase<3?640:450;bar('ehealth',v,max);bar('eshield',0,1);$('evalue').textContent=boss.phase===1?'Jambes '+v+' / 640':boss.phase===2?'Structure immobilisée':'Noyau '+v+' / 450';$('objective-title').textContent=boss.phase===1?'1 / 3 · Briser les jambes':boss.phase===2?'2 / 3 · Monter à bord':'3 / 3 · Détruire le noyau';$('objective-text').textContent=boss.phase===1?'Jambes aux balises cyan · Éviter le marquage rouge':boss.phase===2?'Balise centrale · E / Monter à proximité':'Noyau magenta · Accessible au corps à corps';}else{bar('ehealth',e.hp,e.maxhp);bar('eshield',e.shield,e.maxshield);$('evalue').textContent=Math.ceil(e.hp)+' PV · '+Math.ceil(e.shield)+' bouclier';$('objective-title').textContent=mode==='training'?'Entraînement libre':'Duel contre l’IA';$('objective-text').textContent=mode==='training'?'Énergie illimitée · Mannequin réinitialisé après KO':'Une manche · 99 secondes · Gérez votre bouclier';}$('timer').textContent=mode==='duel'?Math.ceil(roundTimer/60):'∞';$('resources').textContent='Grenades '+p.grenades+' · Énergie '+Math.floor(p.energy/100)+' / 3';document.querySelectorAll('.energy i').forEach((el,i)=>el.classList.toggle('on',p.energy>=(i+1)*100));}

function refreshFighterLabels() {
  $('player-name').textContent = `${lab.p1?.name || 'JOUEUR 1'} · P1`;
  $('enemy-name').textContent = mode === 'boss' ? 'SCARAB · STRUCTURE' : `${lab.p2?.name || 'ADVERSAIRE'} · ${mode === 'duel' ? 'IA' : 'MANNEQUIN'}`;
  $('p2-select').disabled = !lab.ready || mode === 'boss';
  document.querySelectorAll('[data-mode]').forEach(el => el.setAttribute('aria-pressed', String(el.dataset.mode === mode)));
  updatePoseReadout();
}
function selectedPose(f) {
  const entity = f === p ? lab.p1 : lab.p2;
  const neutral = resolveAsset(entity?.assets?.neutral) || preferredAsset(entity);
  const guard = resolveAsset(entity?.assets?.guard);
  return { entity, asset: f.guard && guard?.path ? guard : neutral, guardMissing: Boolean(f.guard && !guard?.path), pose: f.guard && guard?.path ? 'garde' : 'neutre' };
}
function pinCurrentImages() {
  const refs = [lab.p1?.assets?.neutral, lab.p1?.assets?.guard, lab.p2?.assets?.neutral, lab.p2?.assets?.guard, preferredAsset(lab.stage)];
  if (mode === 'boss') refs.push(preferredAsset(lab.data?.bosses.find(b => b.id === 'boss_scarab_h3')));
  if (lab.variant) refs.push(lab.variant);
  imageCache.pin(refs.map(r => resolveAsset(r)?.path));
  refs.forEach(ref => { const asset = resolveAsset(ref); if (asset?.path) imageCache.get(asset); });
}
function updatePoseReadout() {
  if (!p || !e) return;
  const label = (f, name) => {
    const pose = selectedPose(f), record = imageCache.get(pose.asset), native = facingLabels[pose.asset?.native_facing] || facingLabels.unknown;
    const state = record.state === 'ready' ? `${pose.pose} · orientation ${native.toLowerCase()}` : record.state === 'error' || record.state === 'missing' ? 'image indisponible · repère technique' : 'chargement PNG';
    return `${name} : ${state}${pose.guardMissing ? ' · garde sans pose dédiée' : ''}`;
  };
  const current = label(p, 'P1') + (mode === 'boss' ? ' | Scarab : illustration entière statique' : ' | ' + label(e, 'P2'));
  if (current !== lab.poseText) { $('pose-state').textContent = current; lab.poseText = current; }
}
function drawCompleteImage(asset, image, centerX, feetY, height) {
  const iw = image.naturalWidth, ih = image.naturalHeight;
  const box = Array.isArray(asset?.alpha_bbox) && asset.alpha_bbox.length === 4 ? asset.alpha_bbox : [0, 0, iw, ih];
  const bh = Math.max(1, box[3] - box[1]), scale = height / bh;
  // Entire source image, five-argument drawImage. BBox only anchors feet and scale.
  ctx.drawImage(image, centerX - (box[0] + box[2]) / 2 * scale, feetY - box[3] * scale, iw * scale, ih * scale);
  lab.renderCalls++;
}
function backdrop() {
  const gradient = ctx.createLinearGradient(0, 0, 0, H); gradient.addColorStop(0, '#16333f'); gradient.addColorStop(1, '#081a1d');
  ctx.fillStyle = gradient; ctx.fillRect(0, 0, W, H);
  const asset = preferredAsset(lab.stage), record = imageCache.get(asset);
  if (record.state === 'ready') {
    const image = record.image, scale = Math.min(W / image.naturalWidth, H / image.naturalHeight);
    ctx.drawImage(image, (W - image.naturalWidth * scale) / 2, (H - image.naturalHeight * scale) / 2, image.naturalWidth * scale, image.naturalHeight * scale);
    ctx.fillStyle = '#06151d55'; ctx.fillRect(0, 0, W, H);
  }
  const overlay = ctx.createLinearGradient(0, 0, 0, H); overlay.addColorStop(0, '#041418dd'); overlay.addColorStop(.25, '#04141800'); overlay.addColorStop(.8, '#04141822'); overlay.addColorStop(1, '#041418ee'); ctx.fillStyle = overlay; ctx.fillRect(0, 0, W, H);
  const caption = lab.stage ? `${lab.stage.name} · 1 plan de fond${record.state === 'ready' ? '' : record.state === 'error' ? ' · image indisponible' : ' · chargement'}` : 'Fond technique · aucun master disponible';
  if ($('stage-state').textContent !== caption) $('stage-state').textContent = caption;
}
function technicalFigure(f, pending) {
  const x = f.x - camera, y = f.y;
  ctx.strokeStyle = f === p ? '#a4d6bf' : '#bba8d9'; ctx.lineWidth = 2;
  ctx.strokeRect(x - f.w / 2, y - f.h, f.w, f.h);
  ctx.beginPath(); ctx.arc(x, y - f.h - 12, 9, 0, Math.PI * 2); ctx.stroke();
  ctx.font = '9px system-ui'; ctx.textAlign = 'center'; ctx.fillStyle = '#e2ebe4';
  ctx.fillText(pending ? 'CHARGEMENT PNG' : 'IMAGE INDISPONIBLE', x, y - f.h - 30);
  ctx.fillText('REPÈRE TECHNIQUE', x, y - f.h - 19);
}
function artHeight(entity) { return ['hunter_h3', 'tartarus_h2', 'atriox_hw2', 'decimus_hw2', 'escharum_infinite'].includes(entity?.id) ? 183 : 153; }
function drawFighter(f) {
  const pose = selectedPose(f), record = imageCache.get(pose.asset), x = f.x - camera;
  if (record.state === 'ready') drawCompleteImage(pose.asset, record.image, x, f.y, artHeight(pose.entity));
  else technicalFigure(f, ['queued', 'loading'].includes(record.state));
  // Mechanical facing stays independent of the immutable pose orientation.
  ctx.strokeStyle = f === p ? '#bce7cd' : '#d6bced'; ctx.fillStyle = ctx.strokeStyle; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(x - f.face * 16, f.y + 11); ctx.lineTo(x + f.face * 22, f.y + 11); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(x + f.face * 24, f.y + 11); ctx.lineTo(x + f.face * 16, f.y + 7); ctx.lineTo(x + f.face * 16, f.y + 15); ctx.closePath(); ctx.fill();
  ctx.font = 'bold 9px system-ui'; ctx.textAlign = 'center'; ctx.fillText(f === p ? 'P1' : mode === 'duel' ? 'IA' : 'P2', x, f.y + 28);
  if (f.guard) { ctx.strokeStyle = '#a3e6e1aa'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(x, f.y - 63, 57, f.face > 0 ? -1.05 : 2.1, f.face > 0 ? 1.05 : 4.2); ctx.stroke(); }
  if (f.action) {
    const def = actions[f.action.type];
    if (def.reach && f.action.frame >= def.startup && f.action.frame < def.startup + def.active) {
      ctx.strokeStyle = f.action.type === 'special' ? '#f3c47dcc' : '#d7edc8aa'; ctx.lineWidth = f.action.type === 'heavy' ? 5 : 3;
      ctx.beginPath(); ctx.moveTo(x, f.y - 57); ctx.lineTo(x + f.face * def.reach, f.y - 57); ctx.stroke();
    }
  }
  if ($('hitboxes').checked) { ctx.strokeStyle = '#f6cf7d'; ctx.lineWidth = 1; ctx.strokeRect(x - f.w / 2, f.y - f.h, f.w, f.h); }
}
function drawBoss() {
  const entity = lab.data?.bosses.find(b => b.id === 'boss_scarab_h3'), asset = preferredAsset(entity), record = imageCache.get(asset);
  if (record.state === 'ready') {
    const image = record.image, width = 880, height = image.naturalHeight * width / image.naturalWidth;
    ctx.drawImage(image, 1360 - camera, FLOOR - height + 2, width, height);
  } else {
    ctx.strokeStyle = '#b7a1cc'; ctx.lineWidth = 2; ctx.strokeRect(1380 - camera, 160, 820, 345);
    ctx.fillStyle = '#d5c5e5'; ctx.font = '13px system-ui'; ctx.textAlign = 'center'; ctx.fillText('SCARAB · REPÈRE MÉCANIQUE / IMAGE INDISPONIBLE', 1790 - camera, 190);
  }
  ctx.setLineDash([7, 6]); ctx.strokeStyle = '#80e9d98c'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(1440 - camera, 268); ctx.lineTo(2190 - camera, 268); ctx.stroke(); ctx.setLineDash([]);
  ctx.font = '10px system-ui'; ctx.textAlign = 'left'; ctx.fillStyle = '#aee4d5'; ctx.fillText('PONT DE SIMULATION', 1450 - camera, 260);
  boss.legs.forEach((leg, i) => {
    const x = leg.x - camera, color = leg.hp ? '#9effdc' : '#708e87';
    ctx.strokeStyle = color; ctx.fillStyle = '#0b2729bb'; ctx.lineWidth = 2; ctx.strokeRect(x - 40, FLOOR - 88, 80, 82); ctx.fillRect(x - 40, FLOOR - 88, 80, 82);
    ctx.fillStyle = color; ctx.fillRect(x - 35, FLOOR - 83, 70 * leg.hp / leg.max, 4); ctx.font = 'bold 10px system-ui'; ctx.textAlign = 'center'; ctx.fillText(leg.hp ? `CIBLE ${i + 1}` : 'BRISÉE', x, FLOOR - 60); ctx.font = '9px system-ui'; ctx.fillText(`${leg.hp} / ${leg.max}`, x, FLOOR - 44);
  });
  if (boss.phase >= 2) {
    const x = 1750 - camera; ctx.fillStyle = '#7aead329'; ctx.fillRect(x - 65, 270, 130, FLOOR - 270); ctx.strokeStyle = '#9de9d2'; ctx.setLineDash([4, 5]); ctx.strokeRect(x - 65, 270, 130, FLOOR - 270); ctx.setLineDash([]); ctx.fillStyle = '#c1f5df'; ctx.textAlign = 'center'; ctx.font = 'bold 12px system-ui'; ctx.fillText('E / MONTER', x, FLOOR - 18);
  }
  if (boss.phase === 3) {
    const x = boss.core.x - camera; ctx.fillStyle = '#4c2341d9'; ctx.fillRect(x - 45, boss.core.y - 69, 90, 68); ctx.strokeStyle = '#f4a2e7'; ctx.lineWidth = 2; ctx.strokeRect(x - 45, boss.core.y - 69, 90, 68); ctx.fillStyle = '#efb5ed'; ctx.fillRect(x - 39, boss.core.y - 63, 78 * boss.core.hp / boss.core.max, 5); ctx.textAlign = 'center'; ctx.font = 'bold 10px system-ui'; ctx.fillText('CIBLE NOYAU', x, boss.core.y - 38); ctx.font = '9px system-ui'; ctx.fillText(`${boss.core.hp} / 450`, x, boss.core.y - 20);
  }
}
function fighterRenderBounds(f) {
  const pose = selectedPose(f), asset = pose.asset, width = asset?.dimensions?.width || 1024, height = asset?.dimensions?.height || 1536;
  const box = Array.isArray(asset?.alpha_bbox) ? asset.alpha_bbox : [0, 0, width, height], scale = artHeight(pose.entity) / Math.max(1, box[3] - box[1]);
  const left = f.x - (box[0] + box[2]) / 2 * scale, top = f.y - box[3] * scale;
  return { left, right: left + width * scale, top, bottom: Math.max(f.y + 30, top + height * scale) };
}
function cameraView() {
  const first = fighterRenderBounds(p);
  // The complete Scarab image plus the player stay in the viewport, including a
  // jump above the deck. This changes projection only, never collision positions.
  const other = mode === 'boss' ? { left: 1360, right: 2240, top: FLOOR - 440 + 2, bottom: FLOOR + 30 } : fighterRenderBounds(e);
  const bounds = { left: Math.min(first.left, other.left), right: Math.max(first.right, other.right), top: Math.min(first.top, other.top), bottom: Math.max(first.bottom, other.bottom) };
  const desired = mode === 'boss' ? 1 : $('zoom').checked ? 1.8 : 1;
  const zoom = Math.min(desired, (W - 100) / (bounds.right - bounds.left + 35), (H - 200) / (bounds.bottom - bounds.top + 20));
  const viewWidth = W / zoom, center = (bounds.left + bounds.right) / 2;
  return { zoom, camera: center - viewWidth / 2, originY: bounds.bottom + 10 - (H - 100) / zoom, bounds };
}
function draw() {
  if (!p || !e) return;
  ctx.clearRect(0, 0, W, H); backdrop();
  const view = cameraView(), simulationCamera = camera; camera = view.camera;
  ctx.save(); ctx.scale(view.zoom, view.zoom); ctx.translate(0, -view.originY);
  if ($('motion').checked && shake > 1 && !paused) ctx.translate(Math.sin(tick * 7) * shake, Math.cos(tick * 11) * shake * .4);
  ctx.strokeStyle = '#b4deca55'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(-camera, FLOOR + 1); ctx.lineTo(WORLD - camera, FLOOR + 1); ctx.stroke();
  if (mode === 'boss') drawBoss();
  for (const zone of zones) {
    const x = zone.x - camera, g = ground(p), progress = clamp((tick - zone.start) / (zone.impact - zone.start), 0, 1);
    ctx.fillStyle = zone.hit ? '#ff6b6b90' : '#ff5e5e30'; ctx.fillRect(x - zone.width / 2, g - 9, zone.width, 12); ctx.strokeStyle = '#ff9898'; ctx.lineWidth = 2; ctx.strokeRect(x - zone.width / 2, g - 9, zone.width, 12); ctx.fillStyle = '#ffc0b8'; ctx.font = 'bold 11px system-ui'; ctx.textAlign = 'center'; ctx.fillText(zone.kind === 'beam' ? 'FAISCEAU' : zone.kind === 'stomp' ? 'ÉCRASEMENT' : 'IMPULSION', x, g - 24); ctx.fillRect(x - zone.width / 2, g + 7, zone.width * progress, 3);
    if (zone.hit && zone.kind === 'beam') { ctx.fillStyle = '#e3ffac99'; ctx.fillRect(x - 30, 0, 60, g); }
  }
  drawFighter(p); if (mode !== 'boss') drawFighter(e);
  for (const shot of shots) {
    ctx.fillStyle = shot.owner === p ? shot.type === 'grenade' ? '#ffc879' : '#e4fbbb' : '#c7a8ff'; ctx.beginPath(); ctx.arc(shot.x - camera, shot.y, shot.r, 0, Math.PI * 2); ctx.fill();
    if (shot.type === 'bolt') { ctx.strokeStyle = ctx.fillStyle; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(shot.x - camera, shot.y); ctx.lineTo(shot.x - camera - shot.vx, shot.y); ctx.stroke(); }
  }
  for (const particle of particles) { ctx.globalAlpha = clamp(particle.life / 20, 0, 1); ctx.fillStyle = particle.col; ctx.fillRect(particle.x - camera, particle.y, 3, 3); }
  ctx.globalAlpha = 1; ctx.restore(); camera = simulationCamera;
  if (combo > 1) { ctx.fillStyle = '#f2c789'; ctx.font = 'bold 25px system-ui'; ctx.textAlign = 'left'; ctx.fillText(`${combo} IMPACTS`, 30, 145); }
  if (roundNotice > 0) { ctx.fillStyle = '#d0eeea'; ctx.font = 'bold 14px system-ui'; ctx.textAlign = 'center'; ctx.fillText(mode === 'boss' ? 'CIBLES DE SIMULATION · BRISER / MONTER / NEUTRALISER' : 'POSES STATIQUES · MÉCANIQUE COMMUNE', W / 2, 117); }
  updatePoseReadout();
}
function pause(value = !paused) {
  if (ended) return; paused = value; $('pause').textContent = paused ? 'Reprendre' : 'Pause'; input.held.clear(); input.queue = [];
  document.querySelectorAll('.touch .held').forEach(el => el.classList.remove('held'));
  if (paused) { $('banner-title').textContent = 'PAUSE'; $('banner-text').textContent = 'P ou Reprendre pour continuer.'; $('banner').classList.remove('hidden'); }
  else { $('banner').classList.add('hidden'); lastTime = 0; accumulator = 0; }
}
function setView(view) {
  lab.view = view; if (view === 'catalog') pause(true);
  $('lab-view').hidden = view !== 'lab'; $('catalog-view').hidden = view !== 'catalog';
  document.querySelectorAll('[data-view]').forEach(el => { el.classList.toggle('active', el.dataset.view === view); el.setAttribute('aria-pressed', String(el.dataset.view === view)); });
  pinCurrentImages(); if (view === 'catalog') renderCatalog(); else draw();
}
function option(value, label) { const el = textNode('option', label); el.value = value; return el; }
function setSelection(p1id, p2id) {
  const first = lab.data.base_fighters.find(f => f.id === p1id), second = lab.data.base_fighters.find(f => f.id === p2id);
  if (!first || !second || first.playable !== true || second.playable !== true) throw new Error('Seules les 24 identités de base sont sélectionnables');
  lab.p1 = first; lab.p2 = second; $('p1-select').value = first.id; $('p2-select').value = second.id;
  $('p1-source').textContent = first.source_game; $('p2-source').textContent = second.source_game;
  reset(mode); pinCurrentImages(); refreshFighterLabels(); draw();
}
function filteredCatalog() {
  const query = $('catalog-search').value.trim().toLocaleLowerCase('fr'), kind = $('catalog-kind').value, status = $('catalog-status').value;
  return lab.catalog.filter(entry => (kind === 'all' ? entry.kind !== 'stage' : entry.kind === kind) && (status === 'all' || statusOf(entry) === status || entry.variants?.some(ref => statusOf(ref) === status)) && (!query || `${entry.name} ${entry.source_game} ${entry.id}`.toLocaleLowerCase('fr').includes(query)));
}
function renderCatalog() {
  const rows = filteredCatalog(); $('catalog-count').textContent = `${rows.length} entrée${rows.length > 1 ? 's' : ''}`; $('catalog-empty').hidden = Boolean(rows.length);
  if (rows.length && !rows.some(row => row.id === lab.selected?.id)) selectCatalog(rows[0].id, false);
  else if (rows.length && $('catalog-status').value !== 'all' && statusOf(lab.variant) !== $('catalog-status').value) selectCatalog(lab.selected.id, false);
  else if (!rows.length) { lab.selected = null; lab.variant = null; clearDetail(); }
  $('catalog-list').replaceChildren();
  rows.forEach((entry, i) => {
    const button = textNode('button', '', 'catalog-card'); button.type = 'button'; button.dataset.entityId = entry.id; button.classList.toggle('active', lab.selected?.id === entry.id); button.setAttribute('aria-pressed', String(lab.selected?.id === entry.id));
    button.appendChild(textNode('span', String(i + 1).padStart(2, '0'), 'entry-number'));
    const name = textNode('span'); name.appendChild(textNode('span', entry.name, 'card-name')); name.appendChild(textNode('span', entry.source_game || entry.source || '', 'card-origin')); button.appendChild(name);
    const state = $('catalog-status').value !== 'all' && entry.variants?.some(ref => statusOf(ref) === $('catalog-status').value) ? $('catalog-status').value : statusOf(entry);
    button.appendChild(textNode('span', statusLabels[state], `card-state status-${state}`)); button.onclick = () => selectCatalog(entry.id); $('catalog-list').appendChild(button);
  });
}
function clearDetail() {
  $('detail-name').textContent = 'Aucun résultat'; $('detail-kind').textContent = ''; $('detail-origin').textContent = ''; $('detail-status').textContent = ''; $('variant-select').replaceChildren(); $('detail-warning').hidden = true; $('detail-facts').replaceChildren(); $('detail-notes').replaceChildren(); $('detail-sources').replaceChildren(); previewMessage('Aucune entrée', 'Modifiez la recherche ou les filtres.'); lab.previewToken++;
}
function selectCatalog(id, rerender = true) {
  const entry = lab.catalog.find(row => row.id === id); if (!entry) return;
  lab.selected = entry; const refs = entry.variants || [];
  $('detail-kind').textContent = kindLabels[entry.kind]; $('detail-name').textContent = entry.name; $('detail-origin').textContent = entry.source_game || '';
  $('detail-status').textContent = statusLabels[statusOf(entry)]; $('detail-status').className = `status-pill status-${statusOf(entry)}`;
  $('variant-select').replaceChildren(...refs.map((ref, i) => option(ref.asset_id || ref.id, `${i + 1} / ${refs.length} · ${ref.pose === 'guard_static' ? 'Garde statique' : ref.label || ref.pose || ref.id}${ref.preferred ? ' · retenue' : ''}`)));
  $('variant-select').disabled = refs.length < 2;
  if (!refs.length) $('variant-select').appendChild(option('', 'Aucune image générée'));
  const filteredVariant = $('catalog-status').value !== 'all' ? refs.find(ref => statusOf(ref) === $('catalog-status').value) : null;
  const preferred = filteredVariant || refs.find(ref => (ref.asset_id || ref.id) === entry.preferred_asset) || refs[0];
  $('variant-select').value = preferred?.asset_id || preferred?.id || '';
  showVariant(preferred);
  if (rerender) renderCatalog();
}
function previewMessage(title, detail) { const box = textNode('div', '', 'preview-message'); box.appendChild(textNode('strong', title)); box.appendChild(textNode('span', detail)); $('catalog-preview').replaceChildren(box); }
function addFact(name, value) { $('detail-facts').appendChild(textNode('dt', name)); $('detail-facts').appendChild(textNode('dd', value || 'Non renseigné')); }
function showVariant(ref) {
  const entry = lab.selected, asset = resolveAsset(ref); lab.variant = asset; const token = ++lab.previewToken; pinCurrentImages();
  const shownStatus = asset ? statusOf(asset) : statusOf(entry);
  $('detail-status').textContent = statusLabels[shownStatus]; $('detail-status').className = `status-pill status-${shownStatus}`;
  $('detail-facts').replaceChildren(); $('detail-notes').replaceChildren(); $('detail-sources').replaceChildren();
  addFact('Disponibilité', shownStatus === 'needs_correction' ? 'Variante consultable uniquement · non retenue en combat' : entry.kind === 'base' ? 'Sélectionnable · mécanique commune' : entry.kind === 'boss' && entry.mechanic_playable ? 'Rencontre Scarab partielle' : 'Consultation seulement');
  addFact('Orientation native', facingLabels[asset?.native_facing] || facingLabels.unknown);
  addFact('Fichier', asset?.path || 'Aucun PNG');
  if (asset?.dimensions) addFact('Dimensions', `${asset.dimensions.width} × ${asset.dimensions.height} px`);
  addFact('Animation', 'Aucune · pose statique');
  if (asset?.complete_silhouette === false) addFact('Représentation', 'Module partiel · silhouette complète indisponible');
  if (asset?.depicted_region) addFact('Zone représentée', asset.depicted_region);
  if (asset?.source) addFact('Provenance', asset.source);
  const correction = statusOf(entry) === 'needs_correction' || statusOf(asset) === 'needs_correction';
  $('detail-warning').hidden = !correction && asset?.complete_silhouette !== false;
  $('detail-warning').textContent = asset?.complete_silhouette === false ? 'Module partiel uniquement. Le PNG est affiché entier ; la silhouette totale de cette entité n’est pas disponible.' : entry.id === 'dinh_infinite' ? 'Hieu Dinh : candidat à corriger. Cette image n’est pas retenue comme visuel préféré et n’est pas disponible en combat.' : 'Variante à corriger : consulter les réserves de QA avant toute utilisation.';
  const qaNotes = asset?.qa?.notes?.length ? asset.qa.notes : [asset?.qa?.summary];
  const notes = [...qaNotes, ...(asset?.qa?.technical_warnings || []), ...(asset?.limitations || [])].filter(item => typeof item === 'string' && item.trim());
  [...new Set(notes)].forEach(note => $('detail-notes').appendChild(textNode('p', note)));
  const links = [...(asset?.sources || []), ...(entry.sources || [])], used = new Set();
  links.forEach(source => {
    const url = typeof source === 'string' ? source : source.url;
    if (!url || used.has(url)) return;
    try { const parsed = new URL(url); if (!['https:', 'http:'].includes(parsed.protocol)) return; used.add(url); const link = textNode('a', `Source ${used.size} · ${parsed.hostname.replace(/^www\./, '')}`); link.href = url; link.target = '_blank'; link.rel = 'noopener noreferrer'; link.title = url; $('detail-sources').appendChild(link); } catch (_) { /* Non-URL provenance remains in the facts. */ }
  });
  if (!used.size) $('detail-sources').appendChild(textNode('span', 'Référence de jeu indiquée ; lien documentaire absent.'));
  if (!asset?.path) { previewMessage('Visuel manquant', 'Cette identité est documentée, mais aucun PNG n’est disponible.'); return; }
  previewMessage('Chargement du PNG', 'Le fichier local est affiché entier, sans miroir.');
  const record = imageCache.get(asset);
  const show = ready => {
    if (token !== lab.previewToken || lab.variant?.path !== asset.path) return;
    if (ready.state !== 'ready') { previewMessage('Image indisponible', 'Le fichier référencé ne peut pas être chargé. Le catalogue conserve sa source et son état.'); return; }
    const img = ready.image; img.alt = `${entry.name} — ${asset.pose || 'pose candidate'} — orientation native conservée`; img.draggable = false; $('catalog-preview').replaceChildren(img);
  };
  if (record.state === 'ready' || record.state === 'error') show(record); else record.promise.then(show);
}
function validateBindings(data) {
  if (data?.schema_version !== 1 || !Array.isArray(data.base_fighters) || data.base_fighters.length !== 24 || !Array.isArray(data.expansion_characters) || data.expansion_characters.length !== 34 || !data.assets_index) throw new Error('Catalogue V7 absent ou incompatible');
  if (data.base_fighters.some(f => f.playable !== true) || data.expansion_characters.some(f => f.playable !== false)) throw new Error('Contrat de jouabilité invalide');
  return data;
}
async function loadData() {
  try {
    let data = window.HALO_COMBATS_DATA;
    if (!data) {
      if (window.location.protocol === 'file:') throw new Error('catalog.js est absent. Conservez le dossier lab_v7 complet à côté du HTML.');
      const response = await fetch(new URL('data/prototype_asset_bindings_v7.json', repoRoot)); if (!response.ok) throw new Error(`Catalogue HTTP ${response.status}`); data = await response.json();
    }
    lab.data = validateBindings(data); lab.ready = true;
    lab.catalog = [...data.base_fighters.map(x => ({ ...x, kind: 'base' })), ...data.expansion_characters.map(x => ({ ...x, kind: 'expansion' })), ...data.bosses.map(x => ({ ...x, kind: 'boss' })), ...data.stages.map(x => ({ ...x, kind: 'stage' }))];
    $('count-base').textContent = data.base_fighters.length; $('count-catalog').textContent = data.base_fighters.length + data.expansion_characters.length; $('count-boss').textContent = data.bosses.length;
    ['p1-select', 'p2-select'].forEach(id => { $(id).replaceChildren(...data.base_fighters.map(f => option(f.id, f.name))); $(id).disabled = false; });
    const stages = data.stages.filter(stage => preferredAsset(stage)?.path); $('stage-select').replaceChildren(...stages.map(stage => option(stage.id, stage.name))); $('stage-select').disabled = !stages.length; lab.stage = stages[0] || null;
    setSelection(data.base_fighters[0].id, data.base_fighters[1].id); if (lab.stage) $('stage-select').value = lab.stage.id;
    $('load-message').hidden = true; selectCatalog(data.base_fighters[0].id, false); renderCatalog();
    $('status').textContent = 'Images candidates chargées à la demande. Approchez puis testez léger, lourd et garde.';
  } catch (error) { $('load-message').hidden = false; $('load-message').classList.add('error'); $('load-message').textContent = `Catalogue indisponible : ${error.message} Les repères techniques restent visibles, mais aucune identité n’est inventée.`; $('status').textContent = 'Le catalogue local doit être présent pour sélectionner les identités.'; }
}
const keymap = { ArrowLeft:'left',KeyA:'left',KeyQ:'left',ArrowRight:'right',KeyD:'right',Space:'jump',ArrowUp:'jump',KeyW:'jump',KeyZ:'jump',ShiftLeft:'dash',ShiftRight:'dash',KeyJ:'light',KeyK:'heavy',KeyL:'shoot',KeyU:'grenade',KeyI:'special',KeyO:'guard',KeyE:'interact' };
function isEditing(target) { return target instanceof HTMLInputElement || target instanceof HTMLSelectElement || target?.isContentEditable; }
window.addEventListener('keydown', event => {
  if (isEditing(event.target) || $('help-dialog').open || lab.view !== 'lab') return;
  if (['Space', 'Enter'].includes(event.code) && (['BUTTON', 'A'].includes(event.target?.tagName) || event.target?.closest?.('button,a,[role="button"]'))) return;
  if (event.code === 'KeyP') { if (!event.repeat) pause(); return; }
  const action = keymap[event.code]; if (!action) return; event.preventDefault(); if (event.repeat) return;
  input.held.add(action); if (!['left', 'right', 'guard'].includes(action)) enqueue(action);
});
window.addEventListener('keyup', event => { const action = keymap[event.code]; if (action) input.held.delete(action); });
window.addEventListener('blur', () => pause(true)); document.addEventListener('visibilitychange', () => { if (document.hidden) pause(true); });
document.querySelectorAll('[data-mode]').forEach(el => { el.onclick = () => { reset(el.dataset.mode); pinCurrentImages(); refreshFighterLabels(); draw(); canvas.focus({ preventScroll: true }); }; });
document.querySelectorAll('[data-view]').forEach(el => { el.onclick = () => setView(el.dataset.view); });
$('restart').onclick = () => { reset(); refreshFighterLabels(); }; $('pause').onclick = () => pause(); $('help').onclick = () => { pause(true); $('help-dialog').showModal(); }; $('help-close').onclick = () => $('help-dialog').close();
$('p1-select').onchange = () => setSelection($('p1-select').value, $('p2-select').value); $('p2-select').onchange = $('p1-select').onchange;
$('stage-select').onchange = () => { lab.stage = lab.data.stages.find(stage => stage.id === $('stage-select').value); pinCurrentImages(); draw(); };
$('catalog-search').oninput = renderCatalog; $('catalog-kind').onchange = renderCatalog; $('catalog-status').onchange = renderCatalog;
$('variant-select').onchange = () => showVariant(lab.selected?.variants.find(ref => (ref.asset_id || ref.id) === $('variant-select').value));
document.querySelectorAll('.touch button').forEach(el => {
  const action = el.dataset.action;
  el.addEventListener('pointerdown', event => { event.preventDefault(); if (paused || ended) return; el.setPointerCapture(event.pointerId); el.classList.add('held'); input.held.add(action); if (!['left', 'right', 'guard'].includes(action)) enqueue(action); });
  const release = () => { input.held.delete(action); el.classList.remove('held'); }; el.addEventListener('pointerup', release); el.addEventListener('pointercancel', release); el.addEventListener('lostpointercapture', release);
});
function frame(now) { if (!lastTime) lastTime = now; accumulator += Math.min(.1, (now - lastTime) / 1000); lastTime = now; let loops = 0; while (accumulator >= 1 / 60 && loops++ < 6) { if (lab.view === 'lab') step(); accumulator -= 1 / 60; } if (lab.view === 'lab') draw(); requestAnimationFrame(frame); }
reset(); const ready = loadData(); requestAnimationFrame(frame);
// Deterministic harness; production has no remote service or gameplay API.
window.HaloCombatsTest = { snapshot: () => ({ mode, tick, paused, ended, player: { x:p.x,y:p.y,hp:p.hp,shield:p.shield,energy:p.energy,grenades:p.grenades,guard:p.guard,face:p.face }, enemy: { x:e.x,hp:e.hp,shield:e.shield }, boss:JSON.parse(JSON.stringify(boss)),shots:shots.length }), reset: (next) => { reset(next); refreshFighterLabels(); }, step: (n=1) => { for(let i=0;i<n;i++) step(); draw(); }, hold:(a,v=true)=>v?input.held.add(a):input.held.delete(a), action:enqueue, place:(x,y=FLOOR)=>{p.x=x;p.y=y;p.vx=p.vy=0;}, face:v=>p.face=v, pause, damagePlayer:v=>damage(p,v,p.x+1), strikeObjective:(x,y,amount)=>attackBoss(x,y,5,amount,p,new Set(),'test'), constants:{FLOOR,WORLD,simulationHz:60,inputBufferFrames:8} };
window.HaloCombatsLabTest = { ready, snapshot: () => ({ ready:lab.ready, view:lab.view, p1:lab.p1?.id, p2:lab.p2?.id, selected:lab.selected?.id, variant:lab.variant?.id, counts:lab.data?.counts, catalogueEntries:lab.catalog.length, filteredEntries:lab.ready?filteredCatalog().length:0, cache:imageCache.stats(), imageDrawCalls:lab.renderCalls, camera:cameraView(), renderPolicy:'native_pose_no_horizontal_mirroring' }), setSelection, selectCatalog, setView, filter:({query='',kind='all',status='all'}={})=>{$('catalog-search').value=query;$('catalog-kind').value=kind;$('catalog-status').value=status;renderCatalog();return filteredCatalog().map(e=>e.id);}, cacheAsset:ref=>imageCache.get(resolveAsset(ref)), cacheStats:()=>imageCache.stats(), localAssetURL, draw };
})();
