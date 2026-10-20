// Run after: npm install --no-save playwright; npx playwright install chromium
const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
(async()=>{
 fs.mkdirSync('artifacts',{recursive:true});
 const browser=await chromium.launch({headless:true});
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1100},acceptDownloads:true});
  const page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.resolve('FOODSHOCK_Dashboard.html')).href);
  assert((await page.locator('#cards').innerText()).includes('347'));
  await page.screenshot({path:'artifacts/overview-desktop.png',fullPage:true});
  await page.locator('#commodity').selectOption('Cocoa');
  assert((await page.locator('#cards').innerText()).includes('5,920'));
  for(const name of ['overview','forecast','scenario','method']){
   await page.locator('nav button[data-page="'+name+'"]').click();
   assert(await page.locator('#'+name).isVisible());
   assert.equal(await page.locator('#globalControls').isVisible(),['overview','forecast'].includes(name));
   for(const other of ['overview','forecast','scenario','method'].filter(x=>x!==name))assert.equal(await page.locator('#'+other).isVisible(),false);
  }
  await page.locator('nav button[data-page="scenario"]').click();
  await page.locator('#spend').fill('');
  assert.match(await page.locator('#scenarioResult').innerText(),/nonnegative/);
  await page.locator('#spend').fill('1000000');
  assert((await page.locator('#scenarioResult').innerText()).includes('1,232,000'));
  await page.screenshot({path:'artifacts/scenario-desktop.png',fullPage:true});
  await page.locator('nav button[data-page="forecast"]').click();
  await page.screenshot({path:'artifacts/forecast-desktop.png',fullPage:true});
  await page.locator('nav button[data-page="overview"]').click();
  const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#download').click()]);
  assert.equal(download.suggestedFilename(),'foodshock_Cocoa.csv');
  const bytes=fs.readFileSync(await download.path());
  assert(bytes.toString('utf8').startsWith('\uFEFF"date"'));
  assert(bytes.toString('utf8').includes('"Cocoa"'));
  await page.setViewportSize({width:390,height:844});
  await page.screenshot({path:'artifacts/overview-mobile.png',fullPage:true});
  assert(await page.locator('#commodity').isVisible());
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+2);
  if(overflow)console.log('Overflow diagnostics',await page.evaluate(()=>Array.from(document.querySelectorAll('body *')).map(e=>({tag:e.tagName,id:e.id,class:e.className,right:e.getBoundingClientRect().right,width:e.getBoundingClientRect().width})).filter(e=>e.right>innerWidth+2).slice(0,25)));
  assert.equal(overflow,false,'Unexpected whole-page horizontal overflow on mobile');
  assert.deepEqual(errors,[]);
  console.log('PASS: Chromium desktop/mobile smoke, 4 pages, scenario validation, native CSV download and zero page errors.');
 }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
