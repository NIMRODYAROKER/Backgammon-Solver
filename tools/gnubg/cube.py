# GNU BG cube decisions for every type:'cube' exercise (money approximated by a 25-point match, 2-ply).
import sys, os, json, subprocess
sys.path.insert(0, os.environ.get('GNUBG_BUILD', '/tmp/gbuild')); import gnubg_nn as g
D = [e for e in json.load(open('dump.json')) if e.get('type') == 'cube']
Q = {q['id']: q for q in json.loads(subprocess.check_output(['node', '-e', "const {EXERCISES}=require(process.cwd()+'/bank.js');console.log(JSON.stringify(EXERCISES.filter(e=>e.type=='cube').map(e=>({id:e.id,q:e.q,opts:e.opts.map(o=>[o[0],o[1]])}))))"]))}
def boards(s):
    me = [0]*25; op = [0]*25
    for p in range(1, 25):
        v = s['pts'][p]
        if v > 0: me[p-1] = v
        elif v < 0: op[24-p] = -v
    me[24] = s['wb']; op[24] = s['bb']; return me, op
g.set.score(25, 25); out = {}
for e in D:
    q = Q[e['id']]; me, op = boards(e['s']); labels = [o[0] for o in q['opts']]
    take_q = 'לקבל' in labels
    on, oth = (op, me) if take_q else (me, op)
    owns = 'כבר אצלכם' in q['q']            # player already owns the cube (redouble)
    if owns: g.set.cube(2, b'X')
    dbl, take, tg, nd, dt, dp = g.evaluate_cube_decision(g.key_of_board([on, oth]), n=2, s=b'X', i=1)
    if owns: g.set.cube(1)
    want = ('לקבל' if take else 'לוותר') if take_q else ('לא להכפיל – לשחק על גמון' if tg else 'להכפיל' if dbl else 'לא להכפיל')
    site = next(o[0] for o in q['opts'] if o[1])
    out[e['id']] = dict(want=want, site=site)
    print(('OK  ' if want == site else 'FIX ') + e['id'], '| GNU:', want, '| site:', site)
json.dump(out, open('cube.json', 'w'), ensure_ascii=False)
