const {Engine,EXERCISES}=require(process.cwd()+'/bank.js');const fs=require('fs');
const out=[];
for(const e of EXERCISES){ if(e.type==='cube'){out.push({id:e.id,type:'cube',s:Engine.fromDef(e)});continue;}
  const s=Engine.fromDef(e); const plays=Engine.plays(s,e.d); const m=new Map();
  for(const p of plays){const k=Engine.key(p.final); if(!m.has(k)) m.set(k,{key:k,nota:Engine.notate(p.seq),final:p.final});}
  const lk=n=>Engine.key(Engine.applyNotation(s,n));
  const listed={best:e.best.map(lk),near:(e.near||[]).map(x=>lk(x[0])),bad:(e.bad||[]).map(x=>lk(x[0]))};
  const bogus=[...listed.best,...listed.near,...listed.bad].filter(k=>!m.has(k));
  out.push({id:e.id,flag:e.flag||'',s,d:e.d,plays:[...m.values()],listed,names:{best:e.best,near:(e.near||[]).map(x=>x[0]),bad:(e.bad||[]).map(x=>x[0])},bogus});
}
fs.writeFileSync('dump.json',JSON.stringify(out));
console.log(out.filter(o=>o.bogus&&o.bogus.length).map(o=>o.id+':'+JSON.stringify(o.names)));
