// Dependency-free JavaScript interaction checks; not a browser rendering test.
// Run: node tests/test_dashboard.cjs
const fs=require('fs'),vm=require('vm'),path=require('path'),assert=require('assert');
const html=fs.readFileSync(path.join(__dirname,'../FOODSHOCK_Dashboard.html'),'utf8');
const nodes=new Map();
function element(id){if(!nodes.has(id))nodes.set(id,{value:'',textContent:'',innerHTML:'',children:[],dataset:{},classList:{toggle(){}},append(o){this.children.push(o)},click(){}});return nodes.get(id)}
const pages=['overview','forecast','scenario','method'].map(id=>({...element(id),id}));
const buttons=pages.map(p=>({dataset:{page:p.id},classList:{toggle(){}},onclick:null}));
for(const [k,v]of Object.entries({window:'60',spend:'1000000',shock:'20',fx:'10',pass:'60'}))element(k).value=v;
let csvBlob;
const context={console,Blob,URL:{createObjectURL(b){csvBlob=b;return 'blob:test'},revokeObjectURL(){}},document:{getElementById:element,createElement:()=>({click(){}}),querySelectorAll:s=>s==='nav button'?buttons:pages}};
vm.createContext(context);
vm.runInContext(html.match(/<script>([\s\S]*)<\/script>/)[1],context);
assert.equal(element('commodity').children.length,8);
for(const c of ['Cocoa','Maize','Palm oil','Rice','Soybean oil','Soybeans','Sugar','Wheat']){
 element('commodity').value=c;
 for(const window of ['60','120','999']){element('window').value=window;element('window').onchange();for(const id of ['cards','trend','ranking','heatmap','backtest','models']){assert(element(id).innerHTML.length>50);assert(!/NaN|undefined/.test(element(id).innerHTML),id)}}
}
buttons.forEach(b=>{b.onclick();assert(element('pageTitle').textContent.length>0)});
assert(element('scenarioResult').innerHTML.includes('1,232,000'));
element('fx').value='0';element('fx').oninput();assert(element('scenarioResult').innerHTML.includes('1,120,000'));
element('spend').value='-1';element('spend').oninput();assert(element('scenarioResult').textContent.includes('nonnegative'));
element('download').onclick();assert(csvBlob.size>100);
console.log('PASS: 8 commodities × 3 windows, 4 pages, scenario controls, export and finite chart output. Browser rendering not tested.');
