import struct,numpy as np
from nif import Nif
def avoff(b):
    i=4; ne,=struct.unpack_from('<I',b,i); i+=4+4*ne+4
    return i  # flags start
def shape(n,k):
    b=n.blocks[k]; i=avoff(b)+4+12+36+4+4
    c=struct.unpack_from('<4f',b,i); i+=16
    skin,shader,alpha=struct.unpack_from('<3i',b,i); i+=12
    vdesc,=struct.unpack_from('<Q',b,i); i+=8
    nt,nv=struct.unpack_from('<HH',b,i); i+=4; ds,=struct.unpack_from('<I',b,i)
    return dict(k=k,name=n.name(k),skin=skin,shader=shader,alpha=alpha,vdesc=vdesc,nt=nt,nv=nv,ds=ds,offs=dict(skin=avoff(b)+4+12+36+4+4+16))
def skininst(n,k):
    b=n.blocks[k]; d,p,root,nb=struct.unpack_from('<3iI',b,0); bones=list(struct.unpack_from(f'<{nb}i',b,16))
    return dict(data=d,part=p,root=root,bones=bones)
def vlayout(desc):
    flags=desc>>44; size=(desc&0xf)*4
    nib=lambda j:((desc>>(4*j))&0xf)*4
    return dict(size=size,uv=nib(2),nrm=nib(4),tan=nib(5),col=nib(6),skin=nib(7),flags=flags,full=bool(flags&0x400) or nib(2)==16)
def partition(n,k):
    b=n.blocks[k]; npart,ds,vs=struct.unpack_from('<3I',b,0); desc,=struct.unpack_from('<Q',b,12)
    L=vlayout(desc); vd=bytes(b[20:20+ds]); nv=ds//vs if vs else 0
    a=np.frombuffer(vd,np.uint8).reshape(nv,vs)
    if L['full']: pos=np.frombuffer(a[:,0:12].tobytes(),np.float32).reshape(nv,3)
    else: pos=np.frombuffer(a[:,0:6].tobytes(),np.float16).reshape(nv,3).astype(np.float32)
    nrm=a[:,L['nrm']:L['nrm']+3].astype(np.float32)/127.5-1
    uv=np.frombuffer(a[:,L['uv']:L['uv']+4].tobytes(),np.float16).reshape(nv,2).astype(np.float32)
    w=np.frombuffer(a[:,L['skin']:L['skin']+8].tobytes(),np.float16).reshape(nv,4).astype(np.float32); bi=a[:,L['skin']+8:L['skin']+12]
    # partitions -> triangles + global bone idx
    i=20+ds; tris=[]; parts=[]
    for _ in range(npart):
        nvp,ntp,nbp,nst,nwp=struct.unpack_from('<5H',b,i); i+=10
        bones=struct.unpack_from(f'<{nbp}H',b,i); i+=2*nbp
        hm=b[i]; i+=1; vmap=struct.unpack_from(f'<{nvp}H',b,i) if hm else (); i+=2*nvp if hm else 0
        hw=b[i]; i+=1; i+=4*nvp*nwp if hw else 0
        sl=struct.unpack_from(f'<{nst}H',b,i); i+=2*nst
        hf=b[i]; i+=1
        if hf and nst==0: t=np.array(struct.unpack_from(f'<{3*ntp}H',b,i)).reshape(-1,3); i+=6*ntp
        hb=b[i]; i+=1; i+=nvp*nwp if hb else 0
        i+=2; pdesc,=struct.unpack_from('<Q',b,i); i+=8
        tt=np.array(struct.unpack_from(f'<{3*ntp}H',b,i)).reshape(-1,3); i+=6*ntp
        tris.append(tt); parts.append(dict(nv=nvp,nt=ntp,bones=bones,vmap=vmap))
    assert i==len(b),(i,len(b))
    return dict(desc=desc,L=L,vs=vs,raw=a,pos=pos,nrm=nrm,uv=uv,w=w,bi=bi,tris=np.vstack(tris).astype(np.int64),parts=parts)
def shapes(path):
    n=Nif(path); out=[]
    for k in range(len(n.blocks)):
        if n.btype(k)=='BSTriShape':
            s=shape(n,k)
            if s['skin']>=0:
                si=skininst(n,s['skin']); s['si']=si; s['P']=partition(n,si['part']); s['bonenames']=[n.name(x) for x in si['bones']]
            out.append(s)
    return n,out
