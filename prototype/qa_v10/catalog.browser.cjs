'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const {chromium} = require('playwright');
const ROOT = path.resolve(__dirname,'../..');
const out = __dirname;
const results = [];
function check(name, ok) { assert.ok(ok,name);results.push({name,status:'passed'}); }
(async()=>{
 const server=http.createServer((req,res)=>{
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  const target=path.resolve(ROOT,'.'+pathname);
  if(!target.startsWith(ROOT+path.sep)){res.writeHead(403);res.end();return;}
  try {const ext=path.extname(target);const type={'.html':'text/html; charset=utf-8','.js':'application/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.png':'image/png','.md':'text/plain; charset=utf-8'}[ext]||'application/octet-stream';res.writeHead(200,{'Content-Type':type});res.end(fs.readFileSync(target));}
  catch {res.writeHead(404);res.end('Not found');}
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const port=server.address().port;
 let browser;
 try {
  browser=await chromium.launch({executablePath:process.env.HALO_QA_CHROMIUM||'/tmp/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
  const page=await browser.newPage({viewport:{width:1365,height:900},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto('http://127.0.0.1:'+port+'/prototype/halo_universe_v10.html');
  await page.waitForSelector('#catalogue:not([hidden])');
  check('256 fiches / 111 PNG / 172 sans visuel affichés',await page.locator('#stat-entries').textContent()==='256' && await page.locator('#stat-images').textContent()==='111' && await page.locator('#stat-missing').textContent()==='172');
  await page.screenshot({path:path.join(out,'catalog_desktop.png'),fullPage:false});
  await page.locator('[data-category="projectile"]').click();
  check('filtre des 19 projectiles',await page.locator('.entry-card').count()===19);
  await page.locator('[data-entry-id="proj_frag_infinite"]').click();
  await page.waitForFunction(()=>document.querySelector('#detail-image img')?.naturalWidth>0);
  check('image M9 réellement chargée et fiche CU32 explicite',(await page.locator('#detail-name').textContent()).includes('M9') && (await page.locator('#detail-facts').textContent()).includes('CU32'));
  await page.screenshot({path:path.join(out,'catalog_projectile_detail.png'),fullPage:false});
  await page.keyboard.press('Escape');
  check('dialogue ferme au clavier',!(await page.locator('#entry-dialog').evaluate(e=>e.open)));
  await page.locator('#missing-toggle').click();
  check('15 projectiles sans image et aucun PNG présenté comme terminé',await page.locator('.entry-card').count()===15 && await page.locator('.entry-card img').count()===0);
  await page.locator('#reset-filters').click();
  await page.locator('[data-category="vfx"]').click();
  check('filtre des 5 effets',await page.locator('.entry-card').count()===5);
  await page.locator('#reset-filters').click();
  await page.locator('#search').fill('chevalier standard');
  check('recherche retourne incarnation Halo 4',(await page.locator('.card-work').allTextContents()).every(t=>t==='Halo 4') && await page.locator('.entry-card').count()===1);
  await page.locator('#reset-filters').click();
  await page.locator('[data-category="stage"]').click();
  await page.locator('[data-entry-id="st_cartographer_ce"]').click();
  await page.waitForFunction(()=>document.querySelector('#detail-image img')?.naturalWidth>0);
  check('Cartographe marqué à corriger et image entière',await page.locator('#detail-status').textContent()==='À corriger' && await page.locator('#detail-image img').evaluate(e=>getComputedStyle(e).objectFit==='contain'));
  await page.locator('#dialog-close').click();
  await page.locator('#reset-filters').click();
  await page.locator('#search').fill('Pavium');
  await page.locator('[data-entry-id="pavium_hw2"]').click();
  await page.waitForFunction(()=>document.querySelector('#detail-image img')?.naturalWidth>0);
  check('Pavium PNG natif sans transformation miroir',await page.locator('#detail-image img').evaluate(e=>getComputedStyle(e).transform==='none'));
  await page.locator('#dialog-close').click();
  await page.setViewportSize({width:390,height:844});
  await page.locator('#reset-filters').click();
  await page.locator('[data-category="projectile"]').click();
  await page.locator('#catalogue').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(out,'catalog_mobile.png'),fullPage:true});
  check('390 px sans débordement horizontal',await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
  await page.locator('[data-entry-id="proj_plasma_grenade_infinite"]').click();
  await page.waitForFunction(()=>document.querySelector('#detail-image img')?.naturalWidth>0);
  check('fiche projectile fonctionnelle en mobile',await page.locator('#entry-dialog').evaluate(e=>e.open));
  await page.screenshot({path:path.join(out,'catalog_mobile_detail.png'),fullPage:false});
  check('aucune erreur JavaScript',errors.length===0);
  const receipt={status:'passed',date:'2026-11-27',browser:await browser.version(),viewports:[{width:1365,height:900},{width:390,height:844}],assertions:results.length,checks:results,errors,scope:'Catalogue V10 ; interface réelle, images, filtres et dialogues. Aucun test de combat animé ou de fidélité pixel 1:1.'};
  fs.writeFileSync(path.join(out,'catalog_browser_results.json'),JSON.stringify(receipt,null,2)+'\n');
  console.log(JSON.stringify(receipt));
 }catch(error){
  const receipt={status:'failed',date:'2026-11-27',checks:results,error:String(error)};
  fs.writeFileSync(path.join(out,'catalog_browser_results.json'),JSON.stringify(receipt,null,2)+'\n');
  throw error;
 }finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(e=>{console.error(e);process.exitCode=1;});
