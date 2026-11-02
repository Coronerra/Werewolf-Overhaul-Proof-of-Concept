import sys,os,struct,numpy as np
sys.path.insert(0,'.')
from nif import Nif; from geo import *; from shell import *
from PIL import Image,ImageDraw
FW='input/fluffworks/meshes/actors/werewolfbeast/character assets/malebodywerewolf_1.nif'
# UV coverage mask from Fluffworks body shell
R=1024; mask=Image.new('L',(R,R),0); d=ImageDraw.Draw(mask)
n,ss=shapes(FW); sh=[s for s in ss if s['name']=='WereWolfShell.001'][0]['P']
for t in sh['tris']:
    d.polygon([tuple(sh['uv'][v]*R) for v in t],fill=255)
mask=np.array(mask.filter(__import__('PIL.ImageFilter').ImageFilter.MaxFilter(5)))>0
Image.fromarray((mask*255).astype(np.uint8)).save('out/uvmask.png')
LAYERS=10; STEP=0.44
F1F2=(0x82400303,0x00208001)
def welded_normals(pos,nrm):
    key=np.round(pos,3); _,inv=np.unique(key,axis=0,return_inverse=True); inv=inv.ravel()
    acc=np.zeros((inv.max()+1,3)); np.add.at(acc,inv,nrm); acc/=np.linalg.norm(acc,axis=1,keepdims=True)+1e-9
    return acc[inv]
def fluff(src,dst,targets,alpha_from,tex0,sel=None,exclude=(),exr=7.0,kc=None):
    n=Nif(src); _,ss=shapes(src); S={s['name']:s for s in ss}
    akey=S[alpha_from]['alpha']
    root_off,ch=n.node_children(0); linked=set(ch)
    stats=[]
    for name in targets:
        s=S[name]; assert s['k'] in linked,name
        P=s['P']; uv=P['uv']; tr=P['tris']
        c=uv[tr].mean(1); px=np.clip((c*R).astype(int),0,R-1); m=mask[px[:,1],px[:,0]]
        if exclude:
            from scipy.spatial import cKDTree
            ex=np.vstack([S[e]['P']['pos'] for e in exclude]); dd,_=cKDTree(ex).query(P['pos'][tr].mean(1)); m&=dd>exr
        keep={tuple(sorted(t)) for t in tr[m].tolist()}
        if kc is not None:
            if name in kc: keep=kc[name]
            else: kc[name]=keep
        nr=welded_normals(P['pos'],P['nrm'])
        for L in range(1,LAYERS+1):
            clone_shell(n,s['k'],keep,(nr*STEP*L).astype(np.float32),F1F2,tex0,min(240,24*L),f'{name}Shell.{L:03d}',akey)
        stats.append((name,len(tr),int(m.sum())))
    os.makedirs(os.path.dirname(dst),exist_ok=True); n.save(dst); return stats
if __name__=='__main__':
    C='out/common/meshes/actors/werewolfbeast/character assets/coronerra/'
    O='out/fluffy/meshes/actors/werewolfbeast/character assets/coronerra/fluffy/'
    kc={}
    for w in '10':
        print(fluff(C+f'malebodywerewolf_{w}.nif',O+f'malebodywerewolf_{w}.nif',['WereWolfBody'],'WereWolfBodyFur',exclude=['WereWolfSheath','WereWolfPenisTip'],tex0=r'textures\actors\character\werewolf\coronerra\WerewolfBody_shell.dds',kc=kc))
    PT='input/MFA and Growl Patch/meshes/actors/werewolfbeast/character assets/'
    for v in ['','2T/','6T/']:
        kc={}
        for w in '10':
            src=PT+v+f'femalebodywerewolf_{w}.nif'
            _,ss=shapes(src); names=[s['name'] for s in ss if s['name'].startswith('Werewolf ')]
            print(v,w,fluff(src,O+v+f'femalebodywerewolf_{w}.nif',names,'Werewolf Skin Dark',r'textures\actors\character\werewolf\coronerra\FemaleWerewolfBody_shell.dds',kc=kc))
