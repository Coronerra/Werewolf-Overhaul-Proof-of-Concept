import sys,glob,struct; sys.path.insert(0,'.')
from geo import *; from nif import Nif
import numpy as np
def check(f):
    n,ss=shapes(f); _,ch=n.node_children(0); tot=0; bad=[]
    for s in ss:
        if s['k'] not in ch: continue
        si=s['si']; P=s['P']
        ok=n.btype(si['data'])=='NiSkinData' and n.btype(si['part'])=='NiSkinPartition' and si['root']==0 and all(n.btype(b)=='NiNode' for b in si['bones'])
        ok&=n.btype(s['shader'])=='BSLightingShaderProperty' and (s['alpha']<0 or n.btype(s['alpha'])=='NiAlphaProperty')
        ok&=int(P['tris'].max())<len(P['pos']) and bool(np.isfinite(P['pos']).all()) and int(P['bi'].max())<len(si['bones'])
        ok&=all(max(p['bones'])<len(si['bones']) for p in P['parts'])
        if not ok: bad.append(s['name'])
        tot+=len(P['tris'])
    return len([s for s in ss if s['k'] in ch]),tot,bad,len(n.blocks)
if __name__=='__main__':
    for f in sorted(glob.glob(sys.argv[1]+'/**/*.nif',recursive=True)): print(f.split('coronerra/')[-1],check(f))
