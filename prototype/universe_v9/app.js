(function (root) {
  'use strict';

  const CATEGORY_LABELS = {character: 'Personnage', costume: 'Costume', stage: 'Stage', boss: 'Boss'};
  const STATUS_LABELS = {candidate: 'Candidat', needs_correction: 'À corriger', missing: 'Manquant'};
  const MEDIUM_LABELS = {game: 'Jeu', games: 'Jeux', novel: 'Roman', novels: 'Romans', comic: 'BD', comics: 'BD', film: 'Film', series: 'Série', animation: 'Animation', anthology: 'Anthologie', short_story: 'Nouvelle', reference: 'Ouvrage de référence', audio: 'Audio', animated_episode: 'Épisode animé', announced_novel: 'Roman annoncé', arcade_game: 'Jeu d’arcade', audio_series: 'Série audio', campaign_mode: 'Mode campagne', cancelled_beta: 'Bêta annulée', compilation: 'Compilation', cosmetic_event: 'Événement cosmétique', dlc: 'Contenu additionnel', edition: 'Édition', editor: 'Éditeur', game_remake: 'Remake de jeu', interactive_story: 'Récit interactif', live_action: 'Prises de vues réelles', motion_comic: 'BD animée', novel_or_novella: 'Roman / roman court', promotional_film: 'Film promotionnel', reference_book: 'Ouvrage de référence', short_story_audio: 'Nouvelle audio', television: 'Série télévisée', vr_demo: 'Démonstration VR', waypoint_chronicle: 'Chronique Waypoint'};
  const CONTINUITY_LABELS = {main: 'Continuité principale', main_canon: 'Continuité principale', canon: 'Continuité principale', core: 'Continuité principale', silver: 'Silver Timeline', silver_timeline: 'Silver Timeline', fractures: 'Fractures', non_canon: 'Hors continuité', noncanonical: 'Hors continuité', core_adaptation: 'Continuité principale · adaptation', core_legends_style: 'Continuité principale · style Legends', core_simulation_frame: 'Continuité principale · récit de simulation', core_training_frame: 'Continuité principale · cadre d’entraînement', gameplay_nonhistorical_crossover: 'Crossover de gameplay · hors récit historique', legends_parody: 'Legends · parodie hors canon', fracture_entrenched: 'Fracture · Entrenched', fracture_tenrai: 'Fracture · Tenrai', mixed_core_frame_tenrai_retelling: 'Cadre principal · récit réinterprété Tenrai', archival_not_current_story: 'Archive · hors récit actuel', demo_not_history: 'Démonstration · hors récit historique', gameplay_container: 'Conteneur de gameplay', mixed_by_component: 'Continuité selon le composant'};
  const RELEASE_LABELS = {announced_not_released: 'Annoncé · à paraître', cancelled_beta: 'Bêta annulée', published_work_or_component: 'Œuvre ou composant publié'};
  const REFERENCE_LABELS = {official_extended_art_available_packet_pending: 'Illustration officielle repérée · dossier à compléter', official_portrait_partial_packet_pending: 'Portrait officiel partiel · dossier à compléter', official_screen_depiction_partial_packet_pending: 'Apparition officielle partielle à l’écran · dossier à compléter', published_location_frame_packet_pending: 'Lieu publié repéré · dossier visuel à compléter', published_screen_design_packet_pending: 'Design publié à l’écran · dossier à compléter', textual_identity_verified_visual_not_locked: 'Identité vérifiée dans le texte · apparence à documenter'};
  const collator = new Intl.Collator('fr', {sensitivity: 'base', numeric: true});

  function text(value) {
    if (value == null) return '';
    if (Array.isArray(value)) return value.map(text).filter(Boolean).join(' · ');
    if (typeof value === 'object') return Object.entries(value).map(([key, item]) => `${key} : ${text(item)}`).join(' · ');
    return String(value);
  }
  function normalize(value) { return text(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('fr').replace(/[’‘`]/g, "'").trim(); }
  function assetURL(path) {
    if (typeof path !== 'string' || !path || path.startsWith('/') || path.includes('\\') || /[:?#\u0000-\u001f]/.test(path)) return null;
    const parts = path.split('/');
    if (parts.some(part => !part || part === '.' || part === '..' || /%2e|%2f|%5c/i.test(part))) return null;
    return '../' + parts.map(encodeURIComponent).join('/');
  }
  function referenceURL(value) {
    try { const url = new URL(typeof value === 'string' ? value : value?.url); return /^(https?:)$/.test(url.protocol) ? url.href : null; }
    catch { return null; }
  }
  function assetsOf(entry) { return (Array.isArray(entry.assets) ? entry.assets : []).filter(asset => asset && assetURL(asset.path)); }
  function preferredAsset(entry) { const assets = assetsOf(entry); return assets.find(asset => asset.id === entry.preferred_asset_id) || assets[0] || null; }
  function entryStatus(entry) { return entry.art_status || (assetsOf(entry).length ? 'candidate' : 'missing'); }
  function matches(entry, filters) {
    if (filters.category && filters.category !== 'all' && entry.category !== filters.category) return false;
    if (filters.work && filters.work !== 'all' && entry.work_id !== filters.work) return false;
    if (filters.medium && filters.medium !== 'all' && entry.medium !== filters.medium) return false;
    if (filters.continuity && filters.continuity !== 'all' && entry.continuity !== filters.continuity) return false;
    if (filters.status && filters.status !== 'all' && entryStatus(entry) !== filters.status) return false;
    if (filters.missingOnly && entryStatus(entry) !== 'missing') return false;
    const query = normalize(filters.search);
    if (!query) return true;
    const haystack = normalize([entry.name, entry.id, entry.work_title, entry.work_id, entry.medium, MEDIUM_LABELS[entry.medium], entry.continuity, CONTINUITY_LABELS[entry.continuity], CATEGORY_LABELS[entry.category], entry.related_entity_id]);
    return query.split(/\s+/).every(word => haystack.includes(word));
  }
  function filterEntries(entries, filters) {
    const result = entries.filter(entry => matches(entry, filters));
    if (filters.sort === 'name') result.sort((a, b) => collator.compare(a.name, b.name));
    else if (filters.sort === 'work') result.sort((a, b) => collator.compare(a.work_title, b.work_title) || collator.compare(a.name, b.name));
    else if (filters.sort === 'missing') result.sort((a, b) => Number(entryStatus(b) === 'missing') - Number(entryStatus(a) === 'missing') || collator.compare(a.name, b.name));
    return result;
  }
  function summarize(data) {
    const entries = Array.isArray(data.entries) ? data.entries : [];
    const titles = Array.isArray(data.titles) ? data.titles : [];
    const paths = new Set(entries.flatMap(entry => assetsOf(entry).map(asset => asset.path)));
    const titleIds = new Set(titles.map(title => title.id));
    const covered = new Set(entries.map(entry => entry.work_id).filter(id => titleIds.has(id)));
    return {entries: entries.length, assets: paths.size, missing: entries.filter(entry => !assetsOf(entry).length).length, illustrated: entries.filter(entry => assetsOf(entry).length).length, titles: titles.length, coveredTitles: covered.size};
  }
  const api = {normalize, assetURL, referenceURL, assetsOf, preferredAsset, entryStatus, matches, filterEntries, summarize};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.HaloUniverseCatalog = api;
  if (!root.document) return;

  const document = root.document;
  const $ = id => document.getElementById(id);
  const pageSize = 48;
  const state = {data: null, entries: [], filtered: [], limit: pageSize, selected: null, asset: null, filters: {search: '', category: 'all', work: 'all', medium: 'all', continuity: 'all', status: 'all', missingOnly: false, sort: 'catalog'}};
  function node(tag, className, value) { const element = document.createElement(tag); if (className) element.className = className; if (value != null) element.textContent = text(value); return element; }
  function label(map, value) { return map[value] || text(value) || 'Non renseigné'; }
  function noArt(container, detail) {
    const box = node('div', 'no-art');
    box.append(node('span', 'no-art-mark', '◇'), node('strong', '', 'VISUEL À PRODUIRE'), node('small', '', detail ? 'Cette fiche est cataloguée. Aucune image locale n’est encore associée.' : 'Fiche identifiée, image manquante.'));
    container.append(box);
  }
  function image(container, asset, name, detail) {
    const src = assetURL(asset?.path);
    if (!src) { noArt(container, detail); return; }
    const img = node('img'); img.src = src; img.alt = name; img.decoding = 'async'; if (!detail) img.loading = 'lazy';
    img.addEventListener('error', () => { img.remove(); container.append(node('p', 'image-error', 'Image liée indisponible. Le fichier local est à vérifier.')); }, {once: true});
    container.append(img);
  }
  function addOptions(select, values, labels) {
    [...new Set(values.filter(Boolean))].sort((a, b) => collator.compare(label(labels || {}, a), label(labels || {}, b))).forEach(value => {
      const option = node('option', '', label(labels || {}, value)); option.value = value; select.append(option);
    });
  }
  function populateFilters() {
    const works = new Map((state.data.titles || []).map(title => [title.id, title.title]));
    state.entries.forEach(entry => { if (!works.has(entry.work_id)) works.set(entry.work_id, entry.work_title || entry.work_id); });
    [...works.entries()].filter(([id]) => id).sort((a, b) => collator.compare(a[1], b[1])).forEach(([id, title]) => {
      const option = node('option', '', title); option.value = id; $('filter-title-select').append(option);
    });
    addOptions($('filter-medium'), [...state.entries, ...(state.data.titles || [])].map(entry => entry.medium), MEDIUM_LABELS);
    addOptions($('filter-continuity'), [...state.entries, ...(state.data.titles || [])].map(entry => entry.continuity), CONTINUITY_LABELS);
    document.querySelectorAll('[data-category-count]').forEach(element => {
      const category = element.dataset.categoryCount;
      element.textContent = category === 'all' ? state.entries.length : state.entries.filter(entry => entry.category === category).length;
    });
  }
  function displaySummary() {
    const summary = summarize(state.data);
    $('stat-entries').textContent = summary.entries.toLocaleString('fr');
    $('stat-images').textContent = summary.assets.toLocaleString('fr');
    $('stat-missing').textContent = summary.missing.toLocaleString('fr');
    $('missing-badge').textContent = state.entries.filter(entry => entryStatus(entry) === 'missing').length.toLocaleString('fr');
    $('title-coverage').textContent = `${summary.coveredTitles} / ${summary.titles} œuvres ont une fiche`;
    $('image-coverage').textContent = `${summary.illustrated} / ${summary.entries} fiches illustrées`;
    $('coverage-meter').max = Math.max(1, summary.entries); $('coverage-meter').value = summary.illustrated;
  }
  function workEntries(workId) { return state.entries.filter(entry => entry.work_id === workId); }
  function sourceLinks(container, values) {
    [...new Set((values || []).map(referenceURL).filter(Boolean))].forEach((url, index) => {
      const link = node('a', '', `${index ? 'Référence ' + (index + 1) : 'Source'} · ${new URL(url).hostname.replace(/^www\./, '')} ↗`);
      link.href = url; link.title = url; link.target = '_blank'; link.rel = 'noopener noreferrer'; container.append(link);
    });
  }
  function showSelectedWork() {
    const work = (state.data.titles || []).find(item => item.id === state.filters.work);
    $('work-summary').replaceChildren(); $('work-summary').hidden = !work;
    const uncovered = work && workEntries(work.id).length === 0;
    $('empty-eyebrow').textContent = uncovered ? 'ŒUVRE RECENSÉE' : 'AUCUNE CORRESPONDANCE';
    $('empty-title').textContent = uncovered ? 'Fiches détaillées encore à établir.' : 'La sélection est vide.';
    $('empty-description').textContent = uncovered ? 'L’œuvre figure dans le registre. Ses personnages, costumes, stages et boss doivent encore être documentés.' : 'Essayez un autre nom ou retirez un filtre.';
    if (!work) return;
    $('work-summary').append(node('p', 'eyebrow', 'COUVERTURE DE L’ŒUVRE'), node('h3', '', work.title));
    $('work-summary').append(node('p', '', `${label(MEDIUM_LABELS, work.medium)} · ${label(CONTINUITY_LABELS, work.continuity)}`));
    if (work.release_status) $('work-summary').append(node('span', `release-label ${work.release_status === 'announced_not_released' ? 'announced' : ''}`, label(RELEASE_LABELS, work.release_status)));
    if (work.announced_window) $('work-summary').append(node('p', 'announced-window', work.announced_window));
    $('work-summary').append(node('p', '', uncovered ? 'Œuvre recensée, fiches détaillées encore à établir.' : `${workEntries(work.id).length} fiches reliées. La couverture de l’œuvre reste à compléter.`));
    const sources = node('div', 'work-sources'); sourceLinks(sources, work.source_urls); $('work-summary').append(sources);
  }
  function renderRegistry() {
    $('registry-count').textContent = `${state.data.titles.length} œuvres`;
    const fragment = document.createDocumentFragment();
    [...state.data.titles].sort((a, b) => collator.compare(a.title, b.title)).forEach(work => {
      const row = node('tr'); const nameCell = node('td'); const select = node('button', 'registry-work', work.title); select.type = 'button';
      select.addEventListener('click', () => { resetFilters(); state.filters.work = work.id; $('filter-title-select').value = work.id; applyFilters(); $('catalogue').scrollIntoView({block: 'start'}); });
      nameCell.append(select);
      const mediaCell = node('td'); mediaCell.append(node('span', '', label(MEDIUM_LABELS, work.medium)), node('small', '', label(CONTINUITY_LABELS, work.continuity)));
      const count = workEntries(work.id).length; const countCell = node('td'); countCell.append(node('strong', '', count), node('small', '', count ? 'reliées' : 'à établir'));
      const releaseCell = node('td'); releaseCell.append(node('span', work.release_status === 'announced_not_released' ? 'announced' : '', label(RELEASE_LABELS, work.release_status)));
      if (work.announced_window) releaseCell.append(node('small', '', work.announced_window));
      sourceLinks(releaseCell, (work.source_urls || []).slice(0, 1));
      row.append(nameCell, mediaCell, countCell, releaseCell); fragment.append(row);
    });
    $('registry-body').replaceChildren(fragment);
  }
  function card(entry) {
    const button = node('button', 'entry-card'); button.type = 'button'; button.dataset.entryId = entry.id; button.setAttribute('aria-label', `Ouvrir ${entry.name} — ${entry.work_title || ''}`);
    const preview = node('div', `card-image ${entry.category || ''}`); image(preview, preferredAsset(entry), entry.name, false);
    const info = node('div', 'card-info'); const meta = node('div', 'card-meta');
    const status = entryStatus(entry);
    meta.append(node('span', '', label(CATEGORY_LABELS, entry.category).toLocaleUpperCase('fr')), node('span', `status-label ${status}`, label(STATUS_LABELS, status)));
    const bottom = node('div', 'card-bottom'); bottom.append(node('span', '', label(MEDIUM_LABELS, entry.medium)), node('span', 'card-arrow', '↗'));
    info.append(meta, node('span', 'card-name', entry.name), node('span', 'card-work', entry.work_title), bottom);
    button.append(preview, info); button.addEventListener('click', () => openEntry(entry)); return button;
  }
  function renderGallery(append) {
    const gallery = $('gallery'); const start = append ? gallery.childElementCount : 0;
    if (!append) gallery.replaceChildren();
    const fragment = document.createDocumentFragment(); state.filtered.slice(start, state.limit).forEach(entry => fragment.append(card(entry))); gallery.append(fragment);
    $('result-count').replaceChildren(node('strong', '', state.filtered.length.toLocaleString('fr')), document.createTextNode(` fiche${state.filtered.length > 1 ? 's' : ''} sur ${state.entries.length.toLocaleString('fr')}`));
    $('empty-state').hidden = Boolean(state.filtered.length);
    $('display-count').textContent = state.filtered.length ? `${Math.min(state.limit, state.filtered.length)} / ${state.filtered.length} fiches affichées` : '';
    $('load-more').hidden = state.limit >= state.filtered.length;
    $('load-more').textContent = `Afficher ${Math.min(pageSize, Math.max(0, state.filtered.length - state.limit))} fiches de plus`;
    showSelectedWork();
  }
  function applyFilters() {
    state.limit = pageSize; state.filtered = filterEntries(state.entries, state.filters);
    $('missing-toggle').setAttribute('aria-pressed', String(state.filters.missingOnly));
    document.querySelectorAll('[data-category]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.category === state.filters.category)));
    renderGallery(false);
  }
  function resetFilters() {
    Object.assign(state.filters, {search: '', category: 'all', work: 'all', medium: 'all', continuity: 'all', status: 'all', missingOnly: false, sort: 'catalog'});
    $('search').value = ''; ['filter-title-select', 'filter-medium', 'filter-continuity', 'filter-status'].forEach(id => { $(id).value = 'all'; }); $('sort').value = 'catalog'; applyFilters();
  }
  function fact(term, value) { if (value == null || text(value) === '') return; $('detail-facts').append(node('dt', '', term), node('dd', '', value)); }
  function showAsset(asset) {
    state.asset = asset;
    $('detail-image').replaceChildren(); image($('detail-image'), asset, state.selected.name, true);
    const parts = [];
    if (asset) {
      if (asset.width && asset.height) parts.push(`${asset.width} × ${asset.height} px`);
      if (asset.observed_facing) parts.push(`Orientation observée : ${asset.observed_facing}`);
      parts.push('Affichage entier · Sans miroir');
      if (asset.notes?.length) parts.push(text(asset.notes));
    }
    $('asset-caption').textContent = parts.join(' · ');
  }
  function openEntry(entry) {
    state.selected = entry;
    $('detail-category').textContent = label(CATEGORY_LABELS, entry.category).toLocaleUpperCase('fr');
    $('detail-name').textContent = entry.name || entry.id;
    $('detail-work').textContent = entry.work_title || 'Œuvre à renseigner';
    const status = entryStatus(entry); $('detail-status').className = `status-badge ${status}`; $('detail-status').textContent = label(STATUS_LABELS, status);
    $('detail-facts').replaceChildren();
    fact('Média', label(MEDIUM_LABELS, entry.medium)); fact('Continuité', label(CONTINUITY_LABELS, entry.continuity)); fact('Référence visuelle', label(REFERENCE_LABELS, entry.visual_reference_status)); fact('Implémentation', entry.implementation_status); fact('Identifiant', entry.id); fact('Identité liée', entry.related_entity_id);
    $('detail-lock').textContent = text(entry.visual_lock); $('detail-lock-section').hidden = !text(entry.visual_lock);
    $('detail-notes').replaceChildren();
    (Array.isArray(entry.notes) ? entry.notes : [entry.notes]).filter(Boolean).forEach(note => $('detail-notes').append(node('li', '', note)));
    $('detail-notes-section').hidden = !$('detail-notes').childElementCount;
    const title = (state.data.titles || []).find(item => item.id === entry.work_id);
    const sources = [...new Set([...(entry.reference_urls || []), ...(title?.source_urls || [])].map(referenceURL).filter(Boolean))];
    $('detail-sources').replaceChildren();
    sources.forEach((url, index) => { const link = node('a', '', `${index + 1}. ${new URL(url).hostname.replace(/^www\./, '')} ↗`); link.href = url; link.title = url; link.target = '_blank'; link.rel = 'noopener noreferrer'; $('detail-sources').append(link); });
    if (!sources.length) $('detail-sources').append(node('p', '', 'Référence à documenter.'));
    const assets = assetsOf(entry); const chosen = preferredAsset(entry);
    $('asset-selector').replaceChildren();
    assets.forEach((asset, index) => { const option = node('option', '', `${index + 1}. ${asset.id || asset.path.split('/').pop()}`); option.value = String(index); option.selected = asset === chosen; $('asset-selector').append(option); });
    $('asset-selector-label').hidden = assets.length < 2;
    showAsset(chosen);
    const index = state.filtered.indexOf(entry); $('detail-position').textContent = index >= 0 ? `${index + 1} / ${state.filtered.length}` : '';
    $('previous-entry').disabled = index <= 0; $('next-entry').disabled = index < 0 || index >= state.filtered.length - 1;
    if (!$('entry-dialog').open) { $('entry-dialog').showModal(); document.body.classList.add('dialog-open'); } else $('entry-dialog').scrollTop = 0;
  }
  function bindEvents() {
    $('search').addEventListener('input', event => { state.filters.search = event.target.value; applyFilters(); });
    [['filter-title-select', 'work'], ['filter-medium', 'medium'], ['filter-continuity', 'continuity'], ['filter-status', 'status'], ['sort', 'sort']].forEach(([id, key]) => {
      $(id).addEventListener('change', event => { state.filters[key] = event.target.value; if (key === 'status' && event.target.value !== 'missing') state.filters.missingOnly = false; applyFilters(); });
    });
    document.querySelectorAll('[data-category]').forEach(button => button.addEventListener('click', () => { state.filters.category = button.dataset.category; applyFilters(); }));
    $('missing-toggle').addEventListener('click', () => { state.filters.missingOnly = !state.filters.missingOnly; if (state.filters.missingOnly) { state.filters.status = 'all'; $('filter-status').value = 'all'; } applyFilters(); });
    $('reset-filters').addEventListener('click', resetFilters); $('empty-reset').addEventListener('click', resetFilters);
    $('load-more').addEventListener('click', () => { state.limit += pageSize; renderGallery(true); });
    $('dialog-close').addEventListener('click', () => $('entry-dialog').close());
    $('entry-dialog').addEventListener('close', () => document.body.classList.remove('dialog-open'));
    $('entry-dialog').addEventListener('click', event => { if (event.target !== $('entry-dialog')) return; const box = $('entry-dialog').getBoundingClientRect(); if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) $('entry-dialog').close(); });
    $('asset-selector').addEventListener('change', event => showAsset(assetsOf(state.selected)[Number(event.target.value)] || null));
    [['previous-entry', -1], ['next-entry', 1]].forEach(([id, delta]) => $(id).addEventListener('click', () => { const next = state.filtered[state.filtered.indexOf(state.selected) + delta]; if (next) openEntry(next); }));
  }
  async function init() {
    try {
      let data = root.HALO_UNIVERSE_V9;
      if (!data) { const response = await root.fetch('../data/universe_catalog_v9.json'); if (!response.ok) throw new Error(`HTTP ${response.status}`); data = await response.json(); }
      if (!data || !Array.isArray(data.entries) || !Array.isArray(data.titles)) throw new Error('Format du catalogue invalide');
      state.data = data; state.entries = data.entries;
      populateFilters(); displaySummary(); renderRegistry(); bindEvents(); applyFilters();
      $('load-status').hidden = true; $('catalogue').hidden = false;
    } catch (error) {
      $('load-status').classList.add('error'); $('load-status').textContent = 'Le catalogue ne peut pas être chargé. Vérifiez que universe_v9/catalog.js accompagne cette page et que tous les fichiers du projet sont présents.';
      const detail = node('small', '', ` (${error.message})`); $('load-status').append(detail);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once: true}); else init();
}(typeof window !== 'undefined' ? window : globalThis));
