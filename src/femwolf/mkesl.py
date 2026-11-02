import struct,sys
exec(open('recs.py').read())
_,M=load("input/Monster Lip Sync/MonsterLipSync1.esp")
_,G=load("input/Growl - Werebeasts of Skyrim/Growl - Werebeasts of Skyrim.esp")
MAST=['Skyrim.esm','Update.esm','Dawnguard.esm','Dragonborn.esm','Growl - Werebeasts of Skyrim.esp','MonsterLipSync1.esp']
def sub(t,b): return t.encode()+struct.pack('<H',len(b))+b
def z(s): return s.encode()+b'\0'
def rec(t,fid,subs,flags=0):
    d=b''.join(sub(a,b) for a,b in subs)
    return t.encode()+struct.pack('<IIIIHH',len(d),flags,fid,0,44,0)+d
def grp(t,recs):
    d=b''.join(recs); return b'GRUP'+struct.pack('<I',len(d)+24)+t.encode()+struct.pack('<IIHH',0,0,0,0)+d
def build(female,male=r'actors\werewolfbeast\character assets\coronerra\malebodywerewolf_1.nif',fprefix='actors\\werewolfbeast\\character assets\\'):
    # ARMA: MFA's record (winning, head-compatible BOD2) with paths swapped
    arma=[]
    for a,b in M[('ARMA',0xcdd87)][3]:
        if a in('MO2T','MO3T'): continue          # texture hash lists dropped (optional, stale)
        if a=='DNAM': b=b[:2]+b'\x02\x02'+b[4:]    # enable weight slider m/f (meshes have _0/_1)
        if a=='MOD2': b=z(male)
        if a=='BOD2': b=struct.pack('<I',0x59c)+b[4:]   # 32,33,34,37,38,40 (no head 30)
        if a=='MOD3': b=z(fprefix+female+'femalebodywerewolf_1.nif')
        arma.append((a,b))
    # Werebear RACE: Growl base + MFA head data
    gs=[(a,b) for a,b in G[('RACE',0x301e17b)][3] if a!='PHTN']
    ms=M[('RACE',0x301e17b)][3]
    i0=[n for n,(a,b) in enumerate(ms) if a=='NAM0'][0]; i1=[n for n,(a,b) in enumerate(ms) if a=='NAM8'][0]
    head=[]
    for a,b in ms[i0:i1]:
        if a=='HEAD':  # MFA own index 04 -> 05 in our master list
            v,=struct.unpack('<I',b); 
            if v>>24==4: v=(v&0xffffff)|0x05000000
            elif v>>24>4: raise SystemExit('unexpected master')
            b=struct.pack('<I',v)
        head.append((a,b))
    mdat=[b for a,b in ms if a=='DATA'][0]
    out=[]
    for a,b in gs:
        if a=='DATA':
            b=bytearray(b); fl,=struct.unpack_from('<I',b,32); struct.pack_into('<I',b,32,fl|2)
            b[68:76]=mdat[68:76]; b=bytes(b)
        if a=='NAM8': out+=head
        out.append((a,b))
    assert any(a=='NAM8' for a,b in out)
    hdr=[sub('HEDR',struct.pack('<fII',1.71,2,0x800)),sub('CNAM',z('That Guy (Coronerra)')),
         sub('SNAM',z('Female werewolf HDT body + headless ABC male + MFA/Growl werebear merge. Personal use.'))]
    for m in MAST: hdr+= [sub('MAST',z(m)),sub('DATA',b'\0'*8)]
    d=b''.join(hdr)
    tes4=b'TES4'+struct.pack('<IIIIHH',len(d),0x200,0,0,44,0)+d
    return tes4+grp('RACE',[rec('RACE',0x0301e17b,out)])+grp('ARMA',[rec('ARMA',0x000cdd87,arma)])
import os
O='out/'
for body,male,fp in [('smooth',r'actors\werewolfbeast\character assets\coronerra\malebodywerewolf_1.nif','actors\\werewolfbeast\\character assets\\'),('fluffy',r'actors\werewolfbeast\character assets\coronerra\fluffy\malebodywerewolf_1.nif','actors\\werewolfbeast\\character assets\\coronerra\\fluffy\\')]:
    for opt,fem in [('Default',''),('2T','2T\\'),('6T','6T\\')]:
        p=O+f'esp/{body}_{opt}/FemaleWerewolf_ABC_HDT_MFA.esp'; os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'wb').write(build(fem,male,fp))
