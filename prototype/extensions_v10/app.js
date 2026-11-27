(function () {
  'use strict';
  const R = window.HaloExtensions, content = window.HaloExtensionsContent, catalog = content.entries;
  const $ = id => document.getElementById(id);
  const node = (tag, cls, text) => { const el = document.createElement(tag); if (cls) el.className = cls; if (text != null) el.textContent = text; return el; };
  const lookup = id => catalog.find(c => c.id === id);
  const state = {profile: R.newProfile(catalog), panel: 'roster', category: 'character', selected: 'arbiter_h3', search: '', preview: false,
    combat: null, bonus: null, menuEvents: [], storageBlocked: false, storageUnavailable: false, auto: true, brokenAssets: new Set(), toastTimer: null};
  const CATEGORY = {character: 'Personnage', costume: 'Apparence', stage: 'Stage', mode: 'Mode'};
  const STATUS = {permanent:'Acquis', temporary:'Accès temporaire actif', pending:'Vérification en attente', expired:'Accès terminé', revoked:'Accès retiré', none:'À débloquer',
    missing_assets:'Visuel à produire', file_error:'Fichier indisponible', not_implemented:'Mode à produire', dependency:'Personnage parent requis', continuity:'Autre continuité', era:'Autre incarnation', claimable:'Récompense disponible', locked:'À débloquer'};
  const REASON = {paused:'Simulation en pause',hitstop:'Arrêt sur impact',not_fighting:'Action réservée au combat',active_ko:'Combattant actif KO',team_busy:'Action collective en cours',active_busy:'Action active en cours',hitstun:'Combattant touché',partner_ko:'Partenaire KO',partner_busy:'Partenaire déjà engagé',partner_cooldown:'Partenaire en récupération',gauge:'Jauge insuffisante',partner_unavailable:'Partenaire indisponible',no_finish_window:'Après la victoire seulement',no_scene:'Aucune scène à abréger',taunt_cancel_window:'Sortie du taunt à partir de la frame 42',reserve_offstage:'Le soutien doit être présent sur le terrain',scene_committed:'Scène confirmée, résultat déjà engagé',already_ko:'Combattant déjà KO',duplicate_member:'Ce combattant occupe déjà l’autre place',wrong_slot:'Catégorie incompatible avec cette place',invalid_composition:'Remplacez les dossiers indisponibles dans votre composition',requirements:'Les conditions ne sont pas encore remplies',archive_access:'Ouvrez d’abord le dossier précédent',...STATUS};
  const ACTIONS = [{type:'normal',name:'Attaque test',key:'J',cost:'Touche : +10 jauge'},{type:'assist',name:'Assistance',key:'K',cost:'25 jauge · rappel après 5 s'},{type:'tag',name:'Relais',key:'L',cost:'15 jauge · contrôle à 0,30 s'},{type:'super',name:'Super duo',key:'U',cost:'75 jauge · confirmation requise'},{type:'taunt',name:'Taunt',key:'T',cost:'0 gain · 1 s vulnérable'},{type:'finisher',name:'Finisher d’équipe',key:'F',cost:'Après victoire · fenêtre 3 s'}];
  const EVENT_LABELS={normal_begin:'Attaque engagée',normal_hit:'Touche confirmée',normal_blocked:'Attaque gardée',normal_missed:'Attaque manquée',normal_complete:'Contrôle rétabli',assist_begin:'Soutien appelé',assist_hit:'Assistance confirmée',assist_blocked:'Assistance gardée',assist_missed:'Assistance manquée',assist_exit:'Soutien sorti · récupération',assist_interrupted:'Soutien interrompu',tag_begin:'Relais engagé',tag_complete:'Relais terminé',tag_after_ko:'Relais gratuit après KO',control_transferred:'Contrôle transféré',taunt_begin:'Taunt engagé · vulnérable',taunt_complete:'Fin du taunt',taunt_exit:'Sortie du taunt',super_begin:'Super duo engagée',super_confirmed:'Ouverture confirmée · scène',super_hit:'Super duo confirmée',super_blocked:'Super gardée · récupération courte',super_missed:'Super ratée · récupération',super_recovery_complete:'Fin de récupération de super',super_complete:'Retour au contrôle',team_interrupted:'Action collective interrompue',fighter_hit:'Impact reçu',fighter_ko:'Combattant KO',hitstun_complete:'Fin de réaction',victory_confirmed:'Victoire acquise · finisher possible',victory_presentation:'Victoire standard',defeat_confirmed:'Équipe éliminée',finisher_begin:'Présentation d’équipe engagée',finisher_complete:'Victoire présentée'};
  const view = item => {
    const v=R.contentState(item,state.profile,catalog,Date.now());
    if(item.asset && state.brokenAssets.has(item.asset.path)){v.technical='file_error';v.selectable=false;if(!v.obstacles.includes('file_error'))v.obstacles.push('file_error');}
    return v;
  };
  function safeAsset(path) {
    if(typeof path!=='string'||!path||path.startsWith('/')||path.includes('\\')||/[:?#\u0000-\u001f]/.test(path)||path.split('/').some(p=>!p||p==='.'||p==='..'||/%2e|%2f|%5c/i.test(p)))return null;
    return '../'+path.split('/').map(encodeURIComponent).join('/');
  }
  function img(asset,alt,cls){
    const src=safeAsset(asset?.path);if(!src||state.brokenAssets.has(asset.path))return null;
    const el=node('img',cls);el.src=src;el.alt=alt;el.decoding='async';
    el.addEventListener('error',()=>{state.brokenAssets.add(asset.path);for(const item of catalog)if(item.asset?.path===asset.path)item.technical='file_error';el.replaceWith(node('span','no-asset','Image liée indisponible'));renderAll();},{once:true});
    return el;
  }
  function toast(message,error){
    clearTimeout(state.toastTimer);$('toast').textContent=message;$('toast').className='toast'+(error?' error':'');$('toast').hidden=false;
    state.toastTimer=setTimeout(()=>{$('toast').hidden=true;},6000);
  }
  function save(){
    if(state.storageBlocked||state.storageUnavailable)return;
    try{localStorage.setItem(R.SAVE_KEY,JSON.stringify(state.profile));$('save-status').textContent='Progression enregistrée localement';}
    catch{state.storageUnavailable=true;$('save-status').textContent='Session sans sauvegarde';$('storage-notice').hidden=false;$('storage-notice').textContent='Le navigateur ne permet pas de sauvegarder cette session. Vous pouvez continuer à tester ; la progression ne sera pas conservée.';}
  }
  function load(){
    try{
      const r=R.readProfile(localStorage.getItem(R.SAVE_KEY),catalog);
      if(r.ok)state.profile=r.profile;
      else{state.storageBlocked=true;$('storage-notice').hidden=false;$('storage-notice').textContent='La sauvegarde de ce laboratoire est illisible ou appartient à une autre version. Elle est conservée. Cette session utilise un profil temporaire ; réinitialisez ce laboratoire uniquement si vous souhaitez remplacer cette sauvegarde.';$('save-status').textContent='Sauvegarde préservée · session temporaire';}
    }catch{state.storageUnavailable=true;$('save-status').textContent='Session sans sauvegarde';}
  }
  function mutate(result,message){
    if(!result.ok){toast(REASON[result.code]||'Cette action est indisponible dans ce contexte.',true);return false;}
    state.profile=result.profile;if(result.events)state.menuEvents=state.menuEvents.concat(result.events).slice(-30);save();renderAll();if(message)toast(message);return true;
  }
  function art(container,item,v,detail){
    if(v.discovery==='secret'){container.append(node('span','secret-symbol','?'));return;}
    if(item.category==='mode'){container.append(node('span','mode-symbol',item.id==='precision'?'⌖':item.id==='boss_rush_plan'?'◇':'Ⅱ'));return;}
    if(v.asset&&!state.brokenAssets.has(v.asset.path)){
      const silhouette=(v.showSilhouette||(!v.access.allowed&&item.category==='character'))&&!(detail&&state.preview&&v.discovery==='identified');
      const image=img(v.asset,silhouette?'Silhouette du dossier consulté':v.name,silhouette?'silhouette':'');if(image)container.append(image);
    }else{const no=node('div','no-asset');no.append(node('span','no-asset-icon','◇'),node('span','',v.technical==='missing_assets'?'VISUEL À PRODUIRE':v.technical==='file_error'?'FICHIER INDISPONIBLE':'APERÇU INDISPONIBLE'));container.append(no);}
  }
  function displayState(v){
    if(v.claimable)return {label:'Récompense disponible',cls:'ready'};
    if(!v.access.allowed)return {label:STATUS[v.access.status]||'À débloquer',cls:''};
    if(v.technical!=='available')return {label:'Acquis · '+(STATUS[v.technical]||'indisponible').toLowerCase(),cls:'pending'};
    if(v.dependency)return {label:'Acquis · personnage requis',cls:'pending'};
    if(!v.compatible.allowed)return {label:'Acquis · '+STATUS[v.compatible.reason].toLowerCase(),cls:'incompatible'};
    return {label:STATUS[v.access.status],cls:''};
  }
  function renderSummary(){
    $('owned-count').textContent=catalog.filter(c=>view(c).access.allowed).length;
    $('coord-count').textContent=Object.values(state.profile.progress.flags).filter(Boolean).length;
    $('precision-best').textContent=state.profile.progress.precisionBest;
  }
  function renderTeam(){
    const strip=$('team-selection');strip.replaceChildren();
    for(const [slot,label] of [['activeId','Actif'],['reserveId','Réserve'],['stageId','Stage']]){
      const item=lookup(state.profile.selection[slot]);if(!item)continue;const v=view(item);
      const chip=node('div','team-chip'+(slot==='stageId'?' stage-chip':''));const image=v.discovery==='secret'?null:img(v.asset,'');if(image)chip.append(image);
      const text=node('div');text.append(node('small','',label),node('span',v.selectable?'':'invalid',v.name));if(!v.selectable)text.append(node('small','invalid',displayState(v).label));chip.append(text);strip.append(chip);
    }
    const contexts={core:'Simulation principale · rencontre hypothétique','core-h3':'Incarnations Halo 3 uniquement',silver:'Silver Timeline · séparée',fractures:'Fractures · séparées'};
    const context=state.profile.context.workId?'core-h3':state.profile.context.continuity;
    $('context-select').value=context;$('context-description').textContent=contexts[context];
    const ready=R.startFromProfile(state.profile,catalog,Date.now());
    $('launch-simulation').disabled=!ready.ok;$('launch-simulation').title=ready.ok?'':'La composition doit être disponible dans le cadre choisi.';
  }
  function renderRoster(){
    const focused=document.activeElement?.dataset?.contentId;
    const query=state.search.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
    const items=catalog.filter(item=>{
      if(item.category!==state.category)return false;const v=view(item);
      return (v.name+' '+v.workTitle).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().includes(query);
    });
    const frag=document.createDocumentFragment();
    for(const item of items){
      const v=view(item),st=displayState(v),button=node('button','slot-card');button.type='button';button.dataset.contentId=item.id;button.setAttribute('aria-pressed',String(state.selected===item.id));button.setAttribute('aria-label',v.name+' — '+st.label);
      const visual=node('div','slot-art '+item.category);art(visual,item,v,false);
      if(!v.access.allowed){const lock=node('span','lock-mark');lock.setAttribute('aria-hidden','true');lock.append(node('span','lock-icon'));visual.append(lock);}
      const info=node('span','slot-info');info.append(node('strong','',v.name),node('small','',v.workTitle),node('span','slot-state '+st.cls,st.label));
      button.append(visual,info);button.addEventListener('click',()=>{state.selected=item.id;state.preview=false;state.menuEvents=state.menuEvents.concat([{type:'preselect',id:item.id}]).slice(-30);renderRoster();renderDetail();});frag.append(button);
    }
    $('gallery').replaceChildren(frag);$('gallery-empty').hidden=items.length>0;
    if(focused){const el=[...$('gallery').querySelectorAll('[data-content-id]')].find(b=>b.dataset.contentId===focused);el?.focus({preventScroll:true});}
    document.querySelectorAll('[data-category]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.category===state.category)));
  }
  function renderDetail(){
    const item=lookup(state.selected)||catalog[0],v=view(item),detail=$('detail');detail.replaceChildren();
    const visual=node('div','detail-visual '+item.category);art(visual,item,v,true);
    if(state.preview)visual.append(node('span','preview-badge','APERÇU · AUCUN DROIT ACCORDÉ'));
    const body=node('div','detail-body');body.append(node('p','eyebrow',CATEGORY[item.category]+' / DOSSIER'),node('h3','',v.name));body.querySelector('h3').id='detail-name';body.append(node('p','detail-origin',v.workTitle));
    const badges=node('div','state-list');badges.append(node('span','state-badge',v.claimable?'Récompense disponible':STATUS[v.access.status]));
    if(v.technical!=='available')badges.append(node('span','state-badge warning',STATUS[v.technical]));
    if(v.dependency)badges.append(node('span','state-badge warning','Personnage parent requis'));
    if(!v.compatible.allowed)badges.append(node('span','state-badge warning',STATUS[v.compatible.reason]));
    body.append(badges,node('p','detail-copy',v.discovery==='secret'?'L’identité reste protégée jusqu’à l’acquisition du dossier. La condition peut être consultée sans révéler son portrait, son nom ou son texte accessible.':v.discovery==='hint'?'Une silhouette permet de reconnaître la famille de combattant. Le nom complet et la fiche seront révélés à l’acquisition.':item.description));
    if(!item.base){
      const cond=node('div','condition');cond.append(node('p','eyebrow','CONDITION DE RÉCUPÉRATION'),node('p','',item.requirementLabel||'Consulter les archives'),node('small','',v.requirement.met?'Conditions remplies':`${Math.min(v.requirement.done,v.requirement.total)} / ${v.requirement.total} étape${v.requirement.total>1?'s':''}`));body.append(cond);
    }
    const actions=node('div','detail-actions');
    if(v.claimable){const claim=node('button','primary','Récupérer');claim.id='claim-content';claim.addEventListener('click',()=>{const result=R.claim(state.profile,item.id,catalog,Date.now());if(mutate(result)){toast(`${view(item).name} : acquisition conservée.`);$('detail-name').tabIndex=-1;$('detail-name').focus({preventScroll:true});}});actions.append(claim);}
    if(item.category==='character')for(const [slot,label] of [['activeId','Choisir actif'],['reserveId','Choisir réserve']]){
      const choose=node('button',v.selectable?'primary':'secondary',label);choose.id='choose-'+slot;choose.disabled=!v.selectable||state.profile.selection[slot==='activeId'?'reserveId':'activeId']===item.id;
      choose.addEventListener('click',()=>{const result=R.choose(state.profile,item.id,slot,catalog,Date.now());if(mutate(result)){toast('Choix confirmé. Événements de sélection et de désélection enregistrés ; clips à produire.');}});actions.append(choose);
    }
    if(['stage','costume','mode'].includes(item.category)){
      const slot={stage:'stageId',costume:'costumeId',mode:'modeId'}[item.category],choose=node('button','primary',item.category==='costume'?'Équiper l’apparence':'Sélectionner');choose.id='choose-content';choose.disabled=!v.selectable;choose.addEventListener('click',()=>{const result=R.choose(state.profile,item.id,slot,catalog,Date.now());if(mutate(result,'Sélection enregistrée.')){if(item.id==='precision')switchPanel('bonus');}});actions.append(choose);
    }
    if(item.asset&&v.discovery==='identified'&&!v.access.allowed){const preview=node('button','secondary',state.preview?'Fermer l’aperçu':'Voir l’aperçu');preview.id='preview-content';preview.addEventListener('click',()=>{state.preview=!state.preview;renderDetail();$('preview-content')?.focus({preventScroll:true});});actions.append(preview);}
    body.append(actions);
    const note=v.technical==='file_error'?'Le fichier lié ne peut pas être chargé. Le droit acquis est conservé ; la sélection attend le rétablissement du fichier.':v.technical!=='available'?'Le droit d’accès et la disponibilité du contenu sont deux états distincts. Réclamer ce dossier ne fabrique pas son visuel ou son mode.':item.category==='costume'?'L’aperçu ne change pas votre équipe. Cette apparence ne modifie aucune valeur de la simulation.':'La sélection utilise une pose fixe existante. Aucun clip d’entrée, de sortie ou d’attaque n’est déclaré produit.';
    body.append(node('p','detail-small',note));
    if(v.discovery==='identified'&&item.reference_urls?.length){
      try{const url=new URL(item.reference_urls[0]);if(['https:','http:'].includes(url.protocol)){const link=node('a','reference-link','Référence du catalogue ↗');link.href=url.href;link.target='_blank';link.rel='noopener noreferrer';body.append(link);}}catch{}
    }
    detail.append(visual,body);
  }
  function renderArchives(){
    const names={briefing:'Briefing',armory:'Arsenal',records:'Archives'},prereq={briefing:null,armory:'briefing',records:'armory'};
    const frag=document.createDocumentFragment();
    for(const [i,id] of Object.keys(names).entries()){
      const owned=state.profile.progress.archives.includes(id),ready=!prereq[id]||state.profile.progress.archives.includes(prereq[id]);
      const b=node('button','archive-node');b.dataset.archive=id;b.disabled=!ready;b.setAttribute('aria-pressed',String(owned));b.append(node('small','',`DOSSIER 0${i+1}`),node('strong','',names[id]),node('span','',owned?'Consulté · accès conservé':ready?'Ouvrir le dossier':`Après ${names[prereq[id]].toLowerCase()}`));
      b.addEventListener('click',()=>{if(mutate(R.visitArchive(state.profile,id),'Dossier consulté. Les récompenses éligibles peuvent être réclamées.')){$('archive-nodes').querySelector(`[data-archive="${id}"]`)?.focus({preventScroll:true});}});frag.append(b);
    }
    $('archive-nodes').replaceChildren(frag);
  }
  function renderPreferences(){
    $('hide-secrets').checked=state.profile.preferences.hideSecrets;$('reduced-motion').checked=state.profile.preferences.reducedMotion;$('extended-bonus').checked=state.profile.preferences.extendedBonus;
    document.body.classList.toggle('reduced-motion',state.profile.preferences.reducedMotion);
  }
  function renderAll(){renderSummary();renderTeam();renderRoster();renderDetail();renderArchives();renderObjectives();renderPreferences();}
  function switchPanel(panel){
    state.panel=panel;
    for(const b of document.querySelectorAll('[data-panel]')){const active=b.dataset.panel===panel;b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1;$('panel-'+b.dataset.panel).hidden=!active;}
    if(panel==='simulation'){if(state.profile.selection.modeId==='precision'){state.profile.selection.modeId='team_lab';save();renderTeam();}if(!state.combat)startCombat(false);renderCombat();}
    if(panel==='bonus')renderBonus();
  }
  function startCombat(showError){
    const result=R.startFromProfile(state.profile,catalog,Date.now());
    if(!result.ok){if(showError!==false)toast(REASON[result.code],true);return false;}
    state.combat=result.state;state.profile.nextRun++;save();renderCombat(true);return true;
  }
  function useResult(result){
    if(!result.ok){toast(REASON[result.code]||'Commande indisponible.',true);return;}
    state.combat=result.state;
    const earned=R.applyMilestones(state.profile,result.events.filter(e=>!(e.type==='tag_complete'&&e.forced)));
    if(earned!==state.profile){state.profile=earned;save();renderSummary();renderObjectives();}
    renderCombat();
  }
  function sendCommand(type,options){if(!state.combat&&!startCombat())return;useResult(R.command(state.combat,{type,...(options||{})}));}
  function memberAsset(id){
    const costume=lookup(state.profile.selection.costumeId);
    if(costume?.requires?.includes(id)&&view(costume).selectable)return costume.asset;
    return lookup(id)?.asset;
  }
  function actorState(s,m){
    if(m.ko)return 'KO';
    if(s.supportAction?.actor===m.id){const e=s.supportAction.elapsed;return e<R.RULES.assist.enter?'Arrivée du soutien':e<R.RULES.assist.enter+R.RULES.assist.active?'Intervention':'Sortie du soutien';}
    if(s.teamAction){if(s.teamAction.type==='tag')return m.id===s.teamAction.to?'Relais entrant':'Relais sortant';return 'Action collective';}
    if(m.id===s.activeId&&s.activeAction)return {normal:'Attaque test',taunt:'Taunt vulnérable',hitstun:'Réaction à l’impact'}[s.activeAction.type]||s.activeAction.type;
    return m.cooldown>0?'Récupération '+(m.cooldown/60).toFixed(1)+' s':m.id===s.activeId?'Contrôle disponible':'Disponible';
  }
  function renderActor(container,m,role,s,force){
    if(force||container.dataset.actorId!==m.id||container.dataset.costume!==String(state.profile.selection.costumeId)){
      container.replaceChildren();container.dataset.actorId=m.id;container.dataset.costume=String(state.profile.selection.costumeId);
      container.append(node('p','actor-role',role));const image=img(memberAsset(m.id),'Pose fixe de '+(lookup(m.id)?.name||m.id));if(image)container.append(image);
      container.append(node('p','actor-name',lookup(m.id)?.name||m.id),node('p','actor-life'),node('progress'),node('span','actor-state'));
      const meter=container.querySelector('progress');meter.max=R.RULES.health;meter.setAttribute('aria-label','Santé de '+(lookup(m.id)?.name||m.id));
    }
    container.classList.toggle('ko',m.ko);container.querySelector('.actor-life').textContent=`${m.hp} / ${R.RULES.health} PV`;container.querySelector('progress').value=m.hp;container.querySelector('.actor-state').textContent=actorState(s,m);
  }
  function renderCombat(force){
    const s=state.combat;if(!s)return;
    const a=s.members.find(m=>m.id===s.activeId),p=s.members.find(m=>m.id!==s.activeId);
    renderActor($('active-actor'),a,'ACTIF',s,force);renderActor($('reserve-actor'),p,'RÉSERVE / SOUTIEN',s,force);
    const stage=lookup(s.stageId),url=safeAsset(stage?.asset?.path);if(url&&$('scene-background').getAttribute('src')!==url)$('scene-background').src=url;
    $('scene-stage').textContent=stage?.name||'Simulation';
    $('scene-phase').textContent=s.paused?'Pause':({fight:'Simulation',finish_window:'Victoire acquise',presentation:'Présentation finale',victory:'Terminé · victoire',defeat:'Terminé · défaite'})[s.phase];
    const labels={tag:'Transfert de contrôle',super_open:'Ouverture de super',super_scene:'Super duo confirmée',super_recovery:'Retour après ouverture',finisher:s.finish?.label||'Finisher d’équipe',taunt:'Taunt vulnérable',normal:'Attaque test',hitstun:'Impact reçu'};
    const action=s.teamAction||s.activeAction||s.supportAction;
    $('scene-action').textContent=action?(labels[action.type]||'Soutien en intervention'):s.phase==='finish_window'?`Finisher : ${(s.finisherRemaining/60).toFixed(1)} s`:s.phase==='victory'?(s.finish?.label||'Victoire standard'):s.phase==='defeat'?'Deux membres KO':'À votre commandement';
    $('scene-time').textContent=(s.frame/60).toFixed(2).replace('.',',')+' s · '+s.frame+' frames';
    $('gauge-value').textContent=s.gauge+' / 100';$('gauge-meter').value=s.gauge;$('target-value').textContent=s.opponentHp+' / 900';$('target-meter').value=s.opponentHp;
    $('combo-status').textContent=s.combo.hits?`${s.combo.hits} touche${s.combo.hits>1?'s':''} · gain du combo ${s.combo.gaugeGain} / 25`:'Aucune touche confirmée';
    $('pause-simulation').textContent=s.paused?'Reprendre':'Mettre en pause';$('skip-scene').disabled=!s.teamAction||!['super_scene','finisher'].includes(s.teamAction.type)||s.paused;
    $('step-simulation').disabled=s.paused;$('target-mode').value=s.targetMode;
    const availability=R.actionAvailability(s);
    for(const action of ACTIONS){const button=$('action-'+action.type),result=availability[action.type];if(!button)continue;button.disabled=!result.allowed;button.querySelector('.action-reason').textContent=result.allowed?'Disponible':REASON[result.code]||result.code;}
    const logs=s.log.slice(-9).reverse(),frag=document.createDocumentFragment();
    for(const e of logs){const li=node('li');li.append(node('time','',(e.frame/60).toFixed(2)+'s'),node('span','',(EVENT_LABELS[e.type]||e.type)+(e.damage?' · '+e.damage+' PV':'')));frag.append(li);}
    if(!logs.length){const li=node('li');li.append(node('span','','Les commandes et leurs résultats apparaîtront ici.'));frag.append(li);}
    $('combat-log').replaceChildren(frag);
  }
  function renderObjectives(){
    const names={assist:'Confirmer une assistance',tag:'Terminer un relais volontaire',duo:'Confirmer une super duo'},frag=document.createDocumentFragment();
    for(const [key,label] of Object.entries(names)){const done=state.profile.progress.flags[key],li=node('li',done?'done':'');li.append(node('span','objective-check',done?'✓':'○'),node('span','',label));frag.append(li);}
    $('objectives').replaceChildren(frag);
  }
  function createActions(){
    for(const a of ACTIONS){const b=node('button','action-button');b.id='action-'+a.type;b.type='button';const top=node('span','action-top');top.append(node('span','',a.name),node('kbd','',a.key));b.append(top,node('span','action-cost',a.cost),node('span','action-reason','Disponible'));b.addEventListener('click',()=>sendCommand(a.type));$('actions').append(b);}
  }
  function finishBonusIfNeeded(){
    if(!state.bonus?.finished)return;
    const r=R.recordBonus(state.profile,state.bonus);
    if(r.ok&&r.code!=='duplicate_result'){state.profile=r.profile;save();renderSummary();toast(state.bonus.success?`Épreuve réussie : ${state.bonus.hits}/12. Les récompenses disponibles peuvent être réclamées.`:`Épreuve terminée : ${state.bonus.hits}/12. Le meilleur résultat reste conservé.`);}
  }
  function renderBonus(){
    const b=state.bonus,seconds=b?Math.max(0,(b.duration-b.frame)/60):state.profile.preferences.extendedBonus?90:30;
    $('bonus-time').textContent=seconds.toFixed(1).replace('.',',')+' s';$('bonus-score').textContent=(b?.hits||0)+' / 12 touches';$('bonus-result').textContent=!b?'Prêt':b.finished?(b.success?'Objectif atteint':'Essai terminé'):'Épreuve en cours';
    $('start-bonus').textContent=b&&!b.finished?'Recommencer l’épreuve':'Démarrer l’épreuve';$('extended-bonus').disabled=!!b&&!b.finished;
    $('bonus-placeholder').hidden=!!b&&!b.finished;
    if(b?.finished){$('bonus-placeholder').querySelector('h3').textContent=b.success?'Objectif atteint':'Essayez à nouveau';$('bonus-placeholder').querySelector('p').textContent=`${b.hits}/12 touches. Meilleur résultat conservé : ${state.profile.progress.precisionBest}/12.`;}
    const existing=new Map([...$('bonus-targets').children].map(el=>[el.dataset.targetId,el])),ids=new Set((b?.targets||[]).map(t=>t.id));
    for(const [id,el] of existing)if(!ids.has(id))el.remove();
    for(const t of b?.targets||[]){if(existing.has(t.id))continue;const button=node('button','precision-target');button.dataset.targetId=t.id;button.style.left=t.x+'%';button.style.top=t.y+'%';button.setAttribute('aria-label','Toucher la cible '+t.number);button.append(node('span','',t.number));
      button.addEventListener('click',()=>{const focused=document.activeElement===button;const result=R.hitBonus(state.bonus,t.id);if(!result.ok)return;state.bonus=result.state;finishBonusIfNeeded();renderBonus();if(focused){const next=$('bonus-targets').querySelector('button');if(next)next.focus({preventScroll:true});else $('start-bonus').focus({preventScroll:true});}});$('bonus-targets').append(button);
    }
  }
  function startBonus(){state.bonus=R.newBonus('bonus-'+state.profile.nextRun++,state.profile.preferences.extendedBonus);state.bonus=R.stepBonus(state.bonus,1).state;save();renderBonus();$('bonus-targets').querySelector('button')?.focus({preventScroll:true});}
  function bind(){
    document.querySelectorAll('[data-panel]').forEach(button=>button.addEventListener('click',()=>switchPanel(button.dataset.panel)));
    document.querySelector('.workspace-nav').addEventListener('keydown',event=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;const buttons=[...document.querySelectorAll('[data-panel]')],current=buttons.indexOf(document.activeElement);if(current<0)return;event.preventDefault();const index=event.key==='Home'?0:event.key==='End'?buttons.length-1:(current+(event.key==='ArrowRight'?1:-1)+buttons.length)%buttons.length;switchPanel(buttons[index].dataset.panel);buttons[index].focus();});
    document.querySelectorAll('[data-category]').forEach(button=>button.addEventListener('click',()=>{state.category=button.dataset.category;state.search='';$('search').value='';const first=catalog.find(c=>c.category===state.category);if(first)state.selected=first.id;state.preview=false;renderRoster();renderDetail();}));
    $('search').addEventListener('input',()=>{state.search=$('search').value;renderRoster();});
    $('context-select').addEventListener('change',()=>{const value=$('context-select').value;state.profile.context={continuity:value==='core-h3'?'core':value,workId:value==='core-h3'?'h3':null};save();renderAll();});
    $('launch-simulation').addEventListener('click',()=>{if(state.profile.selection.modeId==='precision'){switchPanel('bonus');return;}if(startCombat())switchPanel('simulation');});
    $('new-match').addEventListener('click',()=>startCombat());$('target-mode').addEventListener('change',()=>sendCommand('target',{mode:$('target-mode').value}));
    $('pause-simulation').addEventListener('click',()=>sendCommand('pause'));$('skip-scene').addEventListener('click',()=>sendCommand('skip'));$('auto-clock').addEventListener('change',()=>{state.auto=$('auto-clock').checked;});
    $('step-simulation').addEventListener('click',()=>{if(state.combat)useResult(R.step(state.combat,60));});$('cancel-taunt').addEventListener('click',()=>sendCommand('cancel_taunt'));
    document.querySelectorAll('[data-damage]').forEach(button=>button.addEventListener('click',()=>sendCommand('damage',{target:button.dataset.damage,amount:Number(button.dataset.amount)})));
    $('view-rewards').addEventListener('click',event=>{event.preventDefault();state.selected='arbiter_h3';state.category='character';switchPanel('roster');renderAll();});$('bonus-to-rewards').addEventListener('click',()=>{state.selected='dare_odst';state.category='character';switchPanel('roster');renderAll();});
    $('start-bonus').addEventListener('click',startBonus);
    for(const [id,key] of [['hide-secrets','hideSecrets'],['reduced-motion','reducedMotion'],['extended-bonus','extendedBonus']])$(id).addEventListener('change',()=>{state.profile.preferences[key]=$(id).checked;save();renderAll();if(id==='extended-bonus'&&!state.bonus)renderBonus();});
    $('reset-profile').addEventListener('click',()=>$('reset-dialog').showModal());
    $('reset-dialog').addEventListener('close',()=>{if($('reset-dialog').returnValue!=='reset')return;try{localStorage.removeItem(R.SAVE_KEY);state.storageBlocked=false;state.storageUnavailable=false;}catch{state.storageUnavailable=true;}state.profile=R.newProfile(catalog);state.combat=null;state.bonus=null;state.selected='arbiter_h3';state.category='character';state.preview=false;$('storage-notice').hidden=true;save();renderAll();switchPanel('roster');renderBonus();toast('Seule la progression du laboratoire V10 a été réinitialisée.');});
    document.addEventListener('keydown',event=>{if(state.panel!=='simulation'||event.repeat||event.altKey||event.ctrlKey||event.metaKey||/^(INPUT|TEXTAREA|SELECT)$/.test(event.target.tagName)||event.target.isContentEditable)return;const action=ACTIONS.find(a=>a.key.toLowerCase()===event.key.toLowerCase());if(action){event.preventDefault();sendCommand(action.type);}});
  }
  let last=0,accumulator=0,renderAccumulator=0;
  function frame(time){
    const delta=last?Math.min(250,time-last):0;last=time;
    const canAdvance=!document.hidden&&((state.panel==='simulation'&&state.auto&&state.combat&&!state.combat.paused)||(state.panel==='bonus'&&state.bonus&&!state.bonus.finished));
    if(canAdvance){accumulator+=delta;renderAccumulator+=delta;const count=Math.floor(accumulator/(1000/60));accumulator-=count*(1000/60);
      if(count&&state.panel==='simulation'){
        const r=R.step(state.combat,count);state.combat=r.state;const earned=R.applyMilestones(state.profile,r.events.filter(e=>!(e.type==='tag_complete'&&e.forced)));
        if(earned!==state.profile){state.profile=earned;save();renderSummary();renderObjectives();}
      }
      if(count&&state.panel==='bonus'){state.bonus=R.stepBonus(state.bonus,count).state;finishBonusIfNeeded();}
      if(renderAccumulator>90){renderAccumulator=0;if(state.panel==='simulation')renderCombat();else renderBonus();}
    }else accumulator=0;
    requestAnimationFrame(frame);
  }
  load();createActions();bind();renderAll();renderBonus();requestAnimationFrame(frame);
  window.HaloExtensionsLab={getState:()=>R.clone({profile:state.profile,combat:state.combat,bonus:state.bonus,menuEvents:state.menuEvents,panel:state.panel}),sourceVersion:content.sourceVersion};
})();
