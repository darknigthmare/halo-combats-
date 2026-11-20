'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const catalog = require('../universe_v9/app.js');

const entries = [
  {id: 'arbiter-h2', name: 'Thel ’Vadam', category: 'character', work_id: 'h2', work_title: 'Halo 2', medium: 'game', continuity: 'main', art_status: 'candidate', assets: [{id: 'first', path: 'assets/thel.png'}, {id: 'preferred', path: 'assets/thel-v2.png'}], preferred_asset_id: 'preferred'},
  {id: 'dare-odst', name: 'Véronica Dare', category: 'character', work_id: 'odst', work_title: 'Halo 3: ODST', medium: 'game', continuity: 'main', art_status: 'missing', assets: []},
  {id: 'armor-silver', name: 'Armure de John', category: 'costume', work_id: 'silver', work_title: 'Halo — Série', medium: 'series', continuity: 'silver', art_status: 'needs_correction', assets: [{id: 'armor', path: 'assets/thel.png'}]},
  {id: 'arena', name: 'Arène', category: 'stage', work_id: 'h2', work_title: 'Halo 2', medium: 'game', continuity: 'main', art_status: 'missing', assets: []},
];

test('recherche sans accents et apostrophes typographiques', () => {
  assert.deepEqual(catalog.filterEntries(entries, {search: 'veronica odst'}).map(e => e.id), ['dare-odst']);
  assert.deepEqual(catalog.filterEntries(entries, {search: "thel 'vadam"}).map(e => e.id), ['arbiter-h2']);
});
test('les six filtres se combinent et les continuités restent séparées', () => {
  assert.deepEqual(catalog.filterEntries(entries, {category: 'character', work: 'odst', medium: 'game', continuity: 'main', status: 'missing', search: 'Dare'}).map(e => e.id), ['dare-odst']);
  assert.equal(catalog.filterEntries(entries, {category: 'costume', continuity: 'main'}).length, 0);
});
test('le filtre manquants exclut les candidats et les images à corriger', () => {
  assert.deepEqual(catalog.filterEntries(entries, {missingOnly: true}).map(e => e.id), ['dare-odst', 'arena']);
});
test('une image préférée est choisie sans modifier les variantes', () => {
  assert.equal(catalog.preferredAsset(entries[0]).id, 'preferred');
  assert.equal(catalog.preferredAsset(entries[1]), null);
  assert.equal(entries[0].assets[0].id, 'first');
});
test('les statistiques comptent les PNG distincts et les œuvres réellement liées', () => {
  assert.deepEqual(catalog.summarize({entries, titles: [{id: 'h2'}, {id: 'odst'}, {id: 'silver'}, {id: 'uncovered'}]}), {entries: 4, assets: 2, missing: 2, illustrated: 2, titles: 4, coveredTitles: 3});
});
test('les images utilisent uniquement des chemins locaux sans traversée', () => {
  assert.equal(catalog.assetURL('assets/élite.png'), '../assets/%C3%A9lite.png');
  for (const path of ['https://example.com/a.png', '/a.png', '../a.png', 'assets/../a.png', 'assets/%2e%2e/a.png', 'assets\\a.png', 'data:image/png;base64,A', 'assets/a.png?token=x']) assert.equal(catalog.assetURL(path), null, path);
});
test('les références autorisent uniquement les URL web explicites', () => {
  assert.equal(catalog.referenceURL('https://www.halowaypoint.com/news/test'), 'https://www.halowaypoint.com/news/test');
  for (const value of ['javascript:alert(1)', 'data:text/html,test', '/relative', null]) assert.equal(catalog.referenceURL(value), null);
});
test('le tri des résultats ne modifie pas le catalogue source', () => {
  const ids = entries.map(entry => entry.id);
  const result = catalog.filterEntries(entries, {sort: 'missing'});
  assert.equal(result[0].art_status, 'missing');
  assert.equal(result[1].art_status, 'missing');
  assert.deepEqual(entries.map(entry => entry.id), ids);
});
