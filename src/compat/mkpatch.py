import struct,sys
sys.path.insert(0,'.')
from norm import D
MAST=['Skyrim.esm','Update.esm','Dawnguard.esm','Dragonborn.esm','JS Emissive Eyes SE - Johnskyrim.esp','Growl - Werebeasts of Skyrim.esp','MonsterLipSync1.esp']
def sub(t,b): return t.encode()+struct.pack('<H',len(b))+b
def z(s): return s.encode()+b'\0'
def rec(t,fid,subs):
    d=b''.join(sub(a,b) for a,b in subs); return t.encode()+struct.pack('<IIIIHH',len(d),0,fid,0,44,0)+d
def grp(t,r):
    d=b''.join(r); return b'GRUP'+struct.pack('<I',len(d)+24)+t.encode()+struct.pack('<IIHH',0,0,0,0)+d
JS='JS Emissive Eyes SE - Johnskyrim.esp'
assert D['JS Emissive Eyes SE - Growl.esp']['masters'][:6]==MAST[:6]
def remap_head(src,b):
    v,=struct.unpack('<I',b); m=D[src]['masters']; i=v>>24
    name=m[i] if i<len(m) else src
    return struct.pack('<I',(v&0xffffff)|(MAST.index(name)<<24))
def merged(key,headsrc):
    base=D['JS Emissive Eyes SE - Growl.esp']['recs'][key][2]
    ms=D[headsrc]['recs'][key][2]
    i0=[n for n,(a,b) in enumerate(ms) if a=='NAM0'][0]; i1=([n for n,(a,b) in enumerate(ms) if a=='NAM8' and n>i0]+[len(ms)])[0]
    head=[(a,remap_head(headsrc,b) if a=='HEAD' else b) for a,b in ms[i0:i1]]
    g={a:b for a,b in ms}
    out=[]
    for a,b in base:
        if a=='PHTN': continue
        if a in('DATA','BOD2','VNAM'): b=g[a]           # FaceGen flag, head slot, equip flags from MFA side
        if a=='VTCK':                                     # voice types (Skyrim.esm ids, index 0 in both)
            b=g[a]
        if a=='NAM8': out+=head
        out.append((a,b))
    if not any(a=='NAM8' for a,b in base): out+=head
    assert sum(a=='NAM0' for a,b in out)==2 and sum(a=='SPLO' for a,b in out)==int([b for a,b in out if a=='SPCT'][0][0])
    return out
ww=merged(('skyrim.esm',0xcdd84),'MFA-Growl-HDTWW_Patch.esp')
wb=merged(('dragonborn.esm',0x1e17b),'FemaleWerewolf_ABC_HDT_MFA.esp')
arma=D['FemaleWerewolf_ABC_HDT_MFA.esp']['recs'][('skyrim.esm',0xcdd87)][2]
hdr=[sub('HEDR',struct.pack('<fII',1.71,2,0x800)),sub('CNAM',z('That Guy (Coronerra)')),
     sub('SNAM',z('Compat: JS Emissive Eyes Growl + MFA/Growl/HDT werewolf + FemaleWerewolf v1.2. Personal use.'))]
for m in MAST: hdr+=[sub('MAST',z(m)),sub('DATA',b'\0'*8)]
d=b''.join(hdr)
out=b'TES4'+struct.pack('<IIIIHH',len(d),0x200,0,0,44,0)+d+grp('RACE',[rec('RACE',0x000cdd84,ww),rec('RACE',0x0301e17b,wb)])
import os;os.makedirs('out/compat',exist_ok=True)
open('out/compat/FemaleWerewolf_Compat_JSEyes.esp','wb').write(out)
