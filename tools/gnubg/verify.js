// Compares every checker exercise with GNU BG (res.json from analyze.py).
// Rule: best = within 0.01 equity of GNU BG's top move (0.005 rolls for pure bear-off),
//       near = within 0.04 (0.05 rolls), anything worse = wrong. Every move inside the near window must be listed.
const { Engine, EXERCISES, STATS } = require(process.cwd() + '/bank.js'); const R = require(process.cwd() + '/res.json');
let n = 0;
for (const e of EXERCISES) {
  if (e.type === 'cube' || !R[e.id]) continue;
  const s = Engine.fromDef(e), K = m => Engine.key(Engine.applyNotation(s, m));
  const rows = R[e.id], top = rows[0][0], kind = rows[0][3], loss = Object.fromEntries(rows.map(r => [r[1], top - r[0]]));
  const B = kind === 'eq' ? 0.01 : 0.005, N = kind === 'eq' ? 0.04 : 0.05, out = [];
  for (const m of e.best) if (loss[K(m)] > B + 1e-9) out.push(`best ${m} loses ${loss[K(m)].toFixed(3)}`);
  for (const [m] of e.near || []) if (loss[K(m)] <= B || loss[K(m)] > N) out.push(`near ${m} loses ${loss[K(m)].toFixed(3)}`);
  for (const [m] of e.bad || []) if (loss[K(m)] <= N) out.push(`bad ${m} loses only ${loss[K(m)].toFixed(3)}`);
  const listed = [...e.best, ...(e.near || []).map(x => x[0])].map(K);
  for (const r of rows) if (top - r[0] <= N && !listed.includes(r[1])) out.push(`missing ${r[2]} (loses ${(top - r[0]).toFixed(3)})`);
  if (out.length) { n++; console.log('FIX ' + e.id + ' | GNU top: ' + rows[0][2] + '\n   ' + out.join('\n   ')); }
}
console.log(n ? n + ' exercises need fixing' : 'all checker exercises agree with GNU BG');
