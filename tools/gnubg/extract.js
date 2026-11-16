const fs=require('fs');
const html=fs.readFileSync(process.argv[2],'utf8');
const a=html.indexOf('const Engine = (() =>');
const b=html.indexOf('\n', html.indexOf('const STATS = '));
let code=html.slice(a,b).replace(/<\/script>\s*<script>/g,'');
code+='\nmodule.exports={Engine,EXERCISES,STATS};';
fs.writeFileSync('bank.js',code);
const {Engine,EXERCISES,STATS}=require(process.cwd()+'/bank.js');
// For each checker exercise compute keys and all legal plays
const out=EXERCISES.map(e=>{
  const s=Engine.fromDef(e);
  const r={...e};
  if(e.type!=='cube'){
    r.plays=Engine.plays(s,e.d);
  }
  return r;
});
fs.writeFileSync('ex.json',JSON.stringify(out));
console.log(EXERCISES.length, Object.keys(out[0]), typeof Engine.plays);
console.log(JSON.stringify(Engine.plays(Engine.fromDef(EXERCISES[0]),EXERCISES[0].d)).slice(0,500));
