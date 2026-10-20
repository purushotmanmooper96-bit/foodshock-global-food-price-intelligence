// DOM logic checks. Browser rendering and native downloads require a browser.
const fs=require('fs'),vm=require('vm'),path=require('path'),assert=require('assert');
function runChecks(html,execute,assert){
 const nodes=new Map(),timers=[],downloads=[],revoked=[];
 function node(id=''){
  const classes=new Set();
  return {id,value:'',textContent:'',innerHTML:'',children:[],style:{},dataset:{},
   classList:{toggle(k,on){const enabled=on===undefined?!classes.has(k):on;if(enabled)classes.add(k);else classes.delete(k);return enabled},contains(k){return classes.has(k)}},
   append(o){this.children.push(o)},click(){downloads.push(this)},remove(){this.removed=true}};
 }
 function el(id){if(!nodes.has(id))nodes.set(id,node(id));return nodes.get(id)}
 const pages=['overview','forecast','scenario','method'].map(el);
 const buttons=pages.map(p=>Object.assign(node(),{dataset:{page:p.id}}));
 const document={getElementById:el,createElement:()=>node(),body:node('body'),querySelectorAll:s=>s==='nav button'?buttons:pages};
 for(const [k,v]of Object.entries({window:'60',spend:'1000000',shock:'20',fx:'10',pass:'60'}))el(k).value=v;
 let csvBlob;
 class TestBlob{constructor(parts){this.text=parts.join('');this.size=this.text.length}}
 const globals={document,Blob:TestBlob,URL:{createObjectURL(b){csvBlob=b;return 'blob:test'},revokeObjectURL(u){revoked.push(u)}},setTimeout:(fn)=>timers.push(fn),console};
 const api=execute(html.match(/<script>([\s\S]*)<\/script>/)[1],globals);
 assert.equal(el('commodity').children.length,8);
 for(const commodity of ['Cocoa','Maize','Palm oil','Rice','Soybean oil','Soybeans','Sugar','Wheat']){
  el('commodity').value=commodity;
  for(const window of ['60','120','999']){
   el('window').value=window;el('window').onchange();
   for(const id of ['cards','trend','ranking','heatmap','backtest','models']){
    assert(el(id).innerHTML.length>50);assert(!/NaN|undefined|Infinity/.test(el(id).innerHTML));
   }
  }
 }
 for(const b of buttons){b.onclick();for(const p of pages)assert.equal(p.classList.contains('hidden'),p.id!==b.dataset.page);assert.equal(el('globalControls').style.display,['overview','forecast'].includes(b.dataset.page)?'flex':'none');assert(el('subtitle').textContent.length>0)}
 assert(el('scenarioResult').innerHTML.includes('1,232,000'));
 el('fx').value='0';el('fx').oninput();assert(el('scenarioResult').innerHTML.includes('1,120,000'));
 for(const invalid of ['','-1','Infinity','NaN']){el('spend').value=invalid;el('spend').oninput();assert(el('scenarioResult').textContent.includes('nonnegative'))}
 el('spend').value='0';el('spend').oninput();assert(el('scenarioResult').innerHTML.includes('n.a.'));
 el('spend').value='1000000';el('fx').value='10';el('pass').value='101';el('pass').oninput();assert(el('scenarioResult').textContent.includes('valid finite'));
 el('pass').value='60';el('pass').oninput();
 assert(Math.abs(api.scenarioValue(1000000,.2,.1,.6)-1232000)<1e-6);
 assert.throws(()=>api.scenarioValue(Infinity,.2,.1,.6));
 assert.throws(()=>api.scenarioValue(1e308,1e308,.1,.6));
 assert.throws(()=>api.scenarioValue(1,.2,.1,1.1));
 assert.equal(api.fmt(null),'n.a.');assert.equal(api.fmt(Infinity),'n.a.');
 assert.equal(api.csvField('a,"b"'),'"a,""b"""');
 const gapChart=api.lineChart([{date:'2026-01',v:1},{date:'2026-02',v:null},{date:'2026-03',v:2}],['v'],['Value']);
 assert(!/NaN|Infinity/.test(gapChart));assert((gapChart.match(/M[0-9]/g)||[]).length>=2);
 el('download').onclick();assert(csvBlob.size>100);assert(csvBlob.text.startsWith('\uFEFF"date"'));assert(csvBlob.text.includes('\r\n'));assert.equal(revoked.length,0);assert.equal(downloads.length,1);assert(downloads[0].removed);timers.forEach(fn=>fn());assert.equal(revoked.length,1);
 return 'PASS: 8 commodities × 3 windows, navigation state, page controls, scenario validation, missing chart values, quoted UTF-8 CSV and deferred download cleanup.';
}
if(require.main===module){
 const html=fs.readFileSync(path.join(__dirname,'../FOODSHOCK_Dashboard.html'),'utf8');
 const execute=(source,globals)=>{const context=vm.createContext(globals);return vm.runInContext(source+';({scenarioValue,lineChart,fmt,csvField})',context)};
 console.log(runChecks(html,execute,assert));
}
module.exports={runChecks};
