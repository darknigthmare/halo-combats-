'use strict';
/* Run only in an environment that permits Chromium to start. This V8 script is supplied without any browser execution in V8.
 * The V7 browser failure is historical evidence, not a V8 launch attempt. */
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const { pathToFileURL } = require('node:url');
const root = path.resolve(__dirname, '../..');
const checks = [], scriptErrors = [];
let browser = null, browserOpened = false;
function playwrightModule() {
  const candidates = [process.env.HALO_PLAYWRIGHT_MODULE, 'playwright'];
  if (process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES) candidates.push(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES, 'playwright'));
  for (const candidate of candidates.filter(Boolean)) { try { return require(candidate); } catch (_) {} }
  throw new Error('Playwright is not available. Install it in your test environment or set HALO_PLAYWRIGHT_MODULE to its module path.');
}
function testedFiles() {
  return ['prototype/halo_combats_lab_v8.html','prototype/lab_v8/app.js','prototype/lab_v7/style.css','prototype/lab_v8/catalog.js','data/prototype_asset_bindings_v8.json'].map(file => ({path:file,sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex')}));
}
async function check(name, fn) { await fn(); checks.push({name,status:'passed'}); }
async function screenshot(page, name) { if (!process.env.HALO_QA_SCREENSHOT_DIR) return; const directory=path.resolve(process.env.HALO_QA_SCREENSHOT_DIR);fs.mkdirSync(directory,{recursive:true});await page.screenshot({path:path.join(directory,name+'.png'),fullPage:true}); }
(async () => {
  const {chromium}=playwrightModule();
  const executablePath=process.env.HALO_CHROMIUM_PATH||(fs.existsSync('/usr/bin/chromium')?'/usr/bin/chromium':undefined);
  browser=await chromium.launch({headless:true,executablePath,args:['--no-sandbox']});browserOpened=true;
  const page=await browser.newPage({viewport:{width:1440,height:1000}});page.on('pageerror',error=>scriptErrors.push(error.message));
  await page.addInitScript(()=>{window.requestAnimationFrame=()=>0;});
  await page.goto(process.env.HALO_TEST_URL||pathToFileURL(path.join(root,'prototype/halo_combats_lab_v8.html')).href);
  await page.waitForFunction(()=>window.HaloCombatsLabTest?.snapshot().ready);
  await page.waitForFunction(()=>HaloCombatsLabTest.cacheStats().loading===0&&HaloCombatsLabTest.cacheStats().queued===0);
  await check('Local bootstrap and actual PNGs load',async()=>{assert.equal(await page.title(),'Halo Combats — Laboratoire V8');const snapshot=await page.evaluate(()=>HaloCombatsLabTest.snapshot());assert(snapshot.ready);assert(snapshot.imageDrawCalls>0);assert.equal(await page.locator('#p1-select option').count(),24);assert.equal(await page.locator('#p2-select option').count(),24);assert.equal(await page.locator('#stage-select option').count(),2);assert.deepEqual(scriptErrors,[]);});
  await check('Keyboard move and jump work on the canvas',async()=>{await page.locator('#game').focus();const before=await page.evaluate(()=>HaloCombatsTest.snapshot().player.x);await page.keyboard.down('ArrowRight');await page.evaluate(()=>HaloCombatsTest.step(30));await page.keyboard.up('ArrowRight');assert((await page.evaluate(()=>HaloCombatsTest.snapshot().player.x))>before+100);await page.keyboard.press('Space');await page.evaluate(()=>HaloCombatsTest.step(10));assert((await page.evaluate(()=>HaloCombatsTest.snapshot().player.y))<515);});
  await check('Space activates focused Pause button without triggering a jump',async()=>{await page.evaluate(()=>HaloCombatsTest.reset('training'));await page.locator('#pause').focus();await page.keyboard.press('Space');assert(await page.evaluate(()=>HaloCombatsTest.snapshot().paused));await page.keyboard.press('Space');assert.equal(await page.evaluate(()=>HaloCombatsTest.snapshot().paused),false);});
  await check('Selection changes labels and guard uses its available candidate',async()=>{await page.selectOption('#p1-select','kat_reach');await page.waitForFunction(()=>HaloCombatsLabTest.cacheStats().loading===0&&HaloCombatsLabTest.cacheStats().queued===0);await page.evaluate(()=>{HaloCombatsTest.hold('guard');HaloCombatsTest.step();});assert((await page.locator('#player-name').textContent()).includes('Kat'));assert((await page.locator('#pose-state').textContent()).includes('garde'));});
  await check('Scarab sequence remains completable by melee',async()=>{const state=await page.evaluate(()=>{const t=HaloCombatsTest;t.reset('boss');for(const x of [1365,2095]){t.place(x);t.face(1);for(let n=0;n<4;n++){t.action('heavy');t.step(52);}}if(t.snapshot().boss.phase!==2)throw Error('Leg phase failed');t.place(1750);t.action('interact');t.step(2);if(t.snapshot().boss.phase!==3)throw Error('Boarding failed');t.place(1790,268);t.face(1);for(let n=0;n<6;n++){t.action('heavy');t.step(55);}return t.snapshot();});assert.equal(state.boss.core.hp,0);assert(state.ended);});
  await page.evaluate(()=>{HaloCombatsTest.reset('training');HaloCombatsTest.step(10);});await screenshot(page,'desktop_lab');
  await check('Catalogue correction filter selects six affected entries',async()=>{await page.click('#tab-catalog');await page.selectOption('#catalog-status','needs_correction');assert.equal(await page.locator('.catalog-card').count(),6);assert.equal(await page.locator('.catalog-card[aria-pressed="true"]').count(),1);assert.equal(await page.locator('#detail-status').textContent(),'À corriger');});
  await check('Dinh is labeled and displayed as a correction candidate',async()=>{await page.fill('#catalog-search','Dinh');await page.waitForFunction(()=>HaloCombatsLabTest.cacheStats().loading===0&&HaloCombatsLabTest.cacheStats().queued===0);assert.equal(await page.locator('#detail-name').textContent(),'Hieu Dinh');assert((await page.locator('#detail-warning').textContent()).includes('à corriger'));assert(await page.locator('#catalog-preview img').evaluate(img=>img.complete&&img.naturalWidth>0));});
  await check('Missing character has an explicit empty state, no fabricated image',async()=>{await page.selectOption('#catalog-status','all');await page.fill('#catalog-search','Kelly');assert.equal(await page.locator('#catalog-preview img').count(),0);assert((await page.locator('#catalog-preview').textContent()).includes('Visuel manquant'));});
  await check('Search P text does not toggle gameplay pause',async()=>{const before=await page.evaluate(()=>HaloCombatsTest.snapshot().paused);await page.fill('#catalog-search','');await page.locator('#catalog-search').focus();await page.keyboard.press('p');assert.equal(await page.evaluate(()=>HaloCombatsTest.snapshot().paused),before);});
  await page.fill('#catalog-search','Dinh');await screenshot(page,'desktop_catalog');
  await check('Desktop has no horizontal overflow',async()=>assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false));
  await page.setViewportSize({width:390,height:844});
  await check('Mobile catalogue has no horizontal overflow',async()=>assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false));await screenshot(page,'mobile_catalog');
  await page.click('#tab-lab');await page.evaluate(()=>HaloCombatsTest.reset('training'));
  await check('Mobile lab has no horizontal overflow and tactile jump works',async()=>{assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await page.locator('[data-action="jump"]').click();await page.evaluate(()=>HaloCombatsTest.step(10));assert((await page.evaluate(()=>HaloCombatsTest.snapshot().player.y))<515);});await screenshot(page,'mobile_lab');
  assert.deepEqual(scriptErrors,[]);
  fs.writeFileSync(path.join(__dirname,'browser_results.json'),JSON.stringify({status:'passed',browser:await browser.version(),checks,passed:checks.length,scriptErrors,visual_review:'Screenshots, if requested, still require a human visual review.',tested_files:testedFiles()},null,2)+'\n');
  console.log(JSON.stringify({status:'passed',passed:checks.length,scriptErrors},null,2));
})().catch(error=>{fs.writeFileSync(path.join(__dirname,'browser_results.json'),JSON.stringify({status:browserOpened?'failed':'blocked_before_page_load',checks,error:error.stack,scriptErrors,tested_files:testedFiles()},null,2)+'\n');console.error(error.stack);process.exitCode=browserOpened?1:2;}).finally(async()=>{if(browser)await browser.close();});
