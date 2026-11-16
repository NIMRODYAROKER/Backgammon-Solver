import json, sys, functools
import os
sys.path.insert(0,os.environ.get('GNUBG_BUILD','/tmp/gbuild'))
import gnubg_nn as g
D=json.load(open('dump.json'))
PLY=2
def boards(s):
    me=[0]*25; op=[0]*25
    for p in range(1,25):
        v=s['pts'][p]
        if v>0: me[p-1]=v
        elif v<0: op[24-p]=-v
    me[24]=s['wb']; op[24]=s['bb']
    return me,op
def eq(pr): w,wg,wbg,lg,lbg=pr; return 2*w-1+wg+wbg-lg-lbg
def contact(me,op):
    # my furthest-back checker vs opponent's furthest-back
    mb=max([i for i in range(25) if me[i]]+[-1]); ob=max([i for i in range(25) if op[i]]+[-1])
    return mb+ob>=23  # indices from own side; contact if they pass each other
# one-sided expected rolls
@functools.lru_cache(None)
def erolls(pos):  # pos: tuple of 24 counts, index0=pt1
    if sum(pos)==0: return 0.0
    if all(c==0 for c in pos[6:]):
        pr=g.bearoff_probabilities(tuple(pos[:6])); return sum(i*p for i,p in enumerate(pr))
    tot=0
    for a in range(1,7):
        for b in range(1,7):
            tot+=min(erolls(n) for n in onesided_plays(pos,a,b))
    return 1+tot/36
def onesided_plays(pos,a,b):
    dice=[a]*4 if a==b else [a,b]
    res=set()
    def rec(p,ds):
        moved=False
        for i,d in enumerate(ds):
            if i>0 and d==ds[0] and a==b: break
            for n in steps(p,d):
                moved=True; rec(n,ds[:i]+ds[i+1:])
        if not moved: res.add(p)
    rec(pos,dice if a==b else dice)
    if a!=b: rec(pos,[b,a])
    return res
def steps(p,d):
    out=[]; home=all(c==0 for c in p[6:]); hi=max([i for i in range(24) if p[i]]+[-1])
    for i in range(24):
        if not p[i]: continue
        t=i-d
        if t>=0: q=list(p); q[i]-=1; q[t]+=1; out.append(tuple(q))
        elif home and (t==-1 or i==hi): q=list(p); q[i]-=1; out.append(tuple(q))
    return out
res={}
for ex in D:
    if ex.get('type')=='cube': continue
    rows=[]
    for pl in ex['plays']:
        me,op=boards(pl['final'])
        if ex['flag']=='bear' and not contact(me,op) and me[24]==0:
            v=-erolls(tuple(me[:24])); kind='rolls'
        else:
            pr=g.probabilities([me,op][::-1] if False else [me,op],PLY)  # [not-on-roll=me, on-roll=op]
            v=-eq(pr); kind='eq'
        rows.append((v,pl['key'],pl['nota'],kind))
    rows.sort(key=lambda r:-r[0])
    res[ex['id']]=rows
    print(ex['id'],len(rows),rows[0][2],round(rows[0][0],3),file=sys.stderr)
json.dump(res,open('res.json','w'))
