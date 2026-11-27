const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const { pathToFileURL } = require('node:url');
const { createHash } = require('node:crypto');
const root = path.resolve(__dirname, '../..');
const out = process.env.HALO_QA_OUTPUT_DIR || __dirname;
const reportPath = path.join(out, 'extensions_browser_results.json');
fs.mkdirSync(out, { recursive: true });
const testedPaths = ['prototype/halo_extensions_v10.html', 'prototype/extensions_v10/rules.js', 'prototype/extensions_v10/content.js', 'prototype/extensions_v10/app.js', 'prototype/extensions_v10/style.css', 'prototype/qa_v10/extensions.test.cjs', 'prototype/qa_v10/extensions.browser.cjs'];
const digests = () => Object.fromEntries(testedPaths.map(file => [file, createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex')]));
const before = digests();
const checks = [], errors = [];
const screenshots = ['roster-desktop-1365.png', 'simulation-desktop-1365.png', 'precision-desktop-1365.png', 'roster-mobile-390.png', 'simulation-mobile-390.png', 'precision-mobile-390.png'].map(name => 'extensions_' + name);
const checkedAt = new Date().toISOString();
(async()=>{
 const server=http.createServer((req,res)=>{const file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname));if(!file.startsWith(root+'/')||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404);res.end();return;}res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png'})[path.extname(file)]||'text/plain');fs.createReadStream(file).pipe(res);});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const base='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,...(process.env.HALO_CHROMIUM_PATH ? { executablePath: process.env.HALO_CHROMIUM_PATH } : {}),args:['--no-sandbox']});
 const check=(label,pass)=>{assert.ok(pass,label);checks.push(label);};
 try{
  const context=await browser.newContext({viewport:{width:1365,height:1000},deviceScaleFactor:1,reducedMotion:'reduce'});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/prototype/halo_extensions_v10.html');await page.waitForFunction(()=>window.HaloExtensionsLab);
  await page.waitForFunction(()=>[...document.querySelectorAll('img[src]')].every(i=>i.complete));
  check('Desktop: all initial images loaded',await page.locator('img[src]').evaluateAll(a=>a.every(i=>i.naturalWidth>0)));
  check('Desktop: no horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  check('Locked Arbiter cannot be selected',await page.locator('#choose-activeId').isDisabled());
  await page.screenshot({path:path.join(out,'extensions_roster-desktop-1365.png'),fullPage:true});
  await page.locator('[data-content-id="linda_h5"]').click();
  check('Secret accessible text remains neutral',!(await page.locator('[data-content-id="linda_h5"]').getAttribute('aria-label')).match(/Linda|058/i));
  check('Secret card and detail have no image',await page.locator('[data-content-id="linda_h5"] img, #detail img').count()===0);
  for(const id of ['briefing','armory','records']) await page.locator(`[data-archive="${id}"]`).click();
  check('Archive path opened in order',(await page.evaluate(()=>HaloExtensionsLab.getState().profile.progress.archives)).length===3);
  await page.locator('#launch-simulation').click();await page.locator('#auto-clock').uncheck();
  await page.locator('#action-assist').click();
  check('Concurrent tag visually disabled',await page.locator('#action-tag').isDisabled());
  check('Assist spent exactly 25 gauge',await page.evaluate(()=>HaloExtensionsLab.getState().combat.gauge===75));
  for(let i=0;i<6;i++)await page.locator('#step-simulation').click();
  await page.locator('#action-tag').click();await page.locator('#step-simulation').click();
  check('Tag changes the controlled member',await page.evaluate(()=>HaloExtensionsLab.getState().combat.activeId==='alice_hw2'));
  for(let i=0;i<2;i++){await page.locator('#action-normal').click();await page.locator('#step-simulation').click();}
  await page.locator('#action-super').click();await page.locator('#step-simulation').click();await page.locator('#skip-scene').click();
  check('All three coordination milestones earned',await page.evaluate(()=>Object.values(HaloExtensionsLab.getState().profile.progress.flags).every(Boolean)));
  await page.screenshot({path:path.join(out,'extensions_simulation-desktop-1365.png'),fullPage:true});
  await page.locator('#tab-roster').click();await page.locator('[data-content-id="arbiter_h3"]').click();await page.locator('#claim-content').click();await page.locator('#choose-activeId').click();
  check('Claimed Arbiter becomes selectable',await page.evaluate(()=>HaloExtensionsLab.getState().profile.selection.activeId==='arbiter_h3'));
  check('Selection/deselection events emitted',await page.evaluate(()=>HaloExtensionsLab.getState().menuEvents.some(e=>e.type==='deselect')&&HaloExtensionsLab.getState().menuEvents.some(e=>e.type==='select_confirm')));
  await page.locator('#tab-bonus').click();await page.locator('#start-bonus').click();
  for(let n=0;n<12;n++){const target=page.locator('.precision-target').first();await target.waitFor({state:'visible',timeout:6000});await target.click();}
  check('Precision exercise completes through real buttons',await page.evaluate(()=>HaloExtensionsLab.getState().bonus.finished&&HaloExtensionsLab.getState().bonus.hits===12));
  await page.screenshot({path:path.join(out,'extensions_precision-desktop-1365.png'),fullPage:true});
  await page.reload();await page.waitForFunction(()=>window.HaloExtensionsLab);
  check('Progress and selection survive reload',await page.evaluate(()=>HaloExtensionsLab.getState().profile.progress.precisionBest===12&&HaloExtensionsLab.getState().profile.selection.activeId==='arbiter_h3'));
  await page.locator('[data-content-id="kelly_h5"]').click();await page.locator('#claim-content').click();
  check('Earned but unproduced visual stays unselectable',await page.locator('#choose-activeId').isDisabled()&&/Visuel à produire/.test(await page.locator('#detail').innerText()));
  await page.evaluate(()=>localStorage.setItem('other-prototype-test','kept'));
  await page.locator('.preferences summary').click();await page.locator('#reset-profile').click();await page.getByRole('button',{name:'Conserver ma progression'}).click();
  check('Cancelled reset preserves progress',await page.evaluate(()=>HaloExtensionsLab.getState().profile.progress.precisionBest===12));
  await page.locator('#reset-profile').click();await page.locator('#confirm-reset').click();await page.waitForFunction(()=>HaloExtensionsLab.getState().profile.progress.precisionBest===0);
  check('Reset only clears its own profile',await page.evaluate(()=>localStorage.getItem('other-prototype-test')==='kept'&&HaloExtensionsLab.getState().profile.progress.precisionBest===0));
  await page.evaluate(()=>localStorage.setItem('halo-combats.extensions-v10.profile','{bad'));
  await page.reload();await page.waitForFunction(()=>window.HaloExtensionsLab);await page.locator('[data-archive="briefing"]').click();
  check('Corrupt save is retained and not overwritten',await page.evaluate(()=>localStorage.getItem('halo-combats.extensions-v10.profile')==='{bad')&&await page.locator('#storage-notice').isVisible());
  const mobileContext=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true,reducedMotion:'reduce'});
  const mobile=await mobileContext.newPage();mobile.on('pageerror',e=>errors.push(e.message));await mobile.goto(base+'/prototype/halo_extensions_v10.html');await mobile.waitForFunction(()=>window.HaloExtensionsLab);await mobile.waitForFunction(()=>[...document.querySelectorAll('img[src]')].every(i=>i.complete));
  await mobile.evaluate(()=>Promise.all([...document.querySelectorAll('img[src]')].map(i=>i.decode().catch(()=>{}))));
  check('Mobile images decode with their actual PNGs',await mobile.locator('img[src]').evaluateAll(a=>a.every(i=>i.naturalWidth>0)));
  check('Mobile 390px: no horizontal overflow',await mobile.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await mobile.screenshot({path:path.join(out,'extensions_roster-mobile-390.png'),fullPage:true});
  await mobile.locator('#launch-simulation').click();await mobile.locator('#auto-clock').uncheck();
  check('Mobile simulation: no horizontal overflow',await mobile.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await mobile.screenshot({path:path.join(out,'extensions_simulation-mobile-390.png'),fullPage:true});
  await mobile.locator('#tab-bonus').click();await mobile.locator('#start-bonus').click();
  check('Mobile precision target is at least 44px',await mobile.locator('.precision-target').first().evaluate(e=>{const r=e.getBoundingClientRect();return r.width>=44&&r.height>=44;}));
  await mobile.screenshot({path:path.join(out,'extensions_precision-mobile-390.png'),fullPage:true});
  const filePage=await mobileContext.newPage();filePage.on('pageerror',e=>errors.push(e.message));await filePage.goto(pathToFileURL(path.join(root,'prototype/halo_extensions_v10.html')).href);await filePage.waitForFunction(()=>window.HaloExtensionsLab);
  check('Direct file opening loads the embedded data and script',await filePage.locator('.slot-card').count()===11);
  const missing=await browser.newContext({viewport:{width:1365,height:1000}});await missing.route('**/assets/characters_wave2/jerome_hw2_neutral_right_v01.png',route=>route.fulfill({status:404,body:'missing fixture'}));const missingPage=await missing.newPage();missingPage.on('pageerror',e=>errors.push(e.message));await missingPage.goto(base+'/prototype/halo_extensions_v10.html');await missingPage.waitForFunction(()=>window.HaloExtensionsLab);await missingPage.waitForFunction(()=>document.querySelector('[data-content-id=jerome_hw2]').textContent.includes('Fichier indisponible')||document.querySelector('[data-content-id=jerome_hw2]').textContent.includes('fichier indisponible'));
  check('PNG load failure blocks launch without removing earned access',await missingPage.locator('#launch-simulation').isDisabled()&&await missingPage.evaluate(()=>HaloExtensionsLab.getState().profile.grants.jerome_hw2[0].status==='active'));
  await missingPage.locator('[data-content-id=jerome_hw2]').click();check('PNG load failure has an explicit distinct availability state',await missingPage.locator('#choose-activeId').isDisabled()&&/Fichier indisponible/.test(await missingPage.locator('#detail').innerText()));
  check('No browser script errors',errors.length===0);
  const after = digests();
  assert.deepEqual(after, before, 'The implementation must remain unchanged during verification');
  fs.writeFileSync(reportPath, JSON.stringify({
   checked_at: checkedAt,
   completed: true,
   browser: 'Chromium ' + browser.version(),
   driver: 'Playwright',
   transport: ['same-process HTTP server', 'file URL smoke check'],
   viewports: [{ width: 1365, height: 1000 }, { width: 390, height: 844 }],
   checks, passed: checks.length, errors,
   tested_files_sha256: after,
   screenshots,
   scope: 'Representative extensions laboratory: access rules, selection, team simulation, precision exercise and local persistence. Static candidate PNGs only.',
   limitations: ['No pixel-perfect or 1:1 art certification', 'No complete guide acceptance certification', 'No actual fight collision or character animation', 'No external account, payment, subscription or network integration', 'Only Chromium tested; no real gamepad or multiplayer'],
  }, null, 2) + '\n');
  console.log(JSON.stringify({ passed: checks.length, errors, screenshots: screenshots.length, report: reportPath }));
 }finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(e=>{fs.writeFileSync(reportPath, JSON.stringify({checked_at:checkedAt,completed:false,passed:checks.length,checks,errors:[...errors,e.message],tested_files_sha256:before},null,2)+'\n');console.error(e.stack);process.exitCode=1;});
