import struct,numpy as np,copy
from nif import Nif
from geo import shape,skininst,partition,avoff
def add_string(n,s):
    if s in n.strings: return n.strings.index(s)
    n.strings.append(s); return len(n.strings)-1
def tidx_of(n,t):
    if t not in n.types: n.types.append(t)
    return n.types.index(t)
def build_partition(b,keep_global,off_vec):
    """rebuild NiSkinPartition block bytes: offset positions, filter triangles by set of kept global tris (as sorted tuple)"""
    npart,ds,vs=struct.unpack_from('<3I',b,0); desc,=struct.unpack_from('<Q',b,12)
    vd=np.frombuffer(bytes(b[20:20+ds]),np.uint8).reshape(-1,vs).copy()
    pos=np.frombuffer(vd[:,0:12].tobytes(),np.float32).reshape(-1,3)+off_vec
    vd[:,0:12]=np.frombuffer(pos.astype(np.float32).tobytes(),np.uint8).reshape(-1,12)
    out=bytearray(struct.pack('<3IQ',npart,ds,vs,desc))+vd.tobytes()
    i=20+ds
    for _ in range(npart):
        nvp,ntp,nbp,nst,nwp=struct.unpack_from('<5H',b,i); j=i+10
        bones=b[j:j+2*nbp]; j+=2*nbp
        hm=b[j]; j+=1; vm=b[j:j+2*nvp] if hm else b''; j+=2*nvp if hm else 0
        hw=b[j]; j+=1; wts=b[j:j+4*nvp*nwp] if hw else b''; j+=4*nvp*nwp if hw else 0
        sl=b[j:j+2*nst]; j+=2*nst
        hf=b[j]; j+=1; tl=None
        if hf and nst==0: tl=np.frombuffer(bytes(b[j:j+6*ntp]),np.uint16).reshape(-1,3); j+=6*ntp
        hb=b[j]; j+=1; bi=b[j:j+nvp*nwp] if hb else b''; j+=nvp*nwp if hb else 0
        tail=b[j:j+2]; j+=2; pdesc=b[j:j+8]; j+=8
        tc=np.frombuffer(bytes(b[j:j+6*ntp]),np.uint16).reshape(-1,3); j+=6*ntp
        m=np.array([tuple(sorted(t)) in keep_global for t in tc.tolist()],bool) if ntp else np.zeros(0,bool)
        nt2=int(m.sum())
        o=bytearray(struct.pack('<5H',nvp,nt2,nbp,nst,nwp))+bones+bytes([hm])+vm+bytes([hw])+wts+sl+bytes([hf])
        if tl is not None: o+=tl[m].astype('<u2').tobytes()
        o+=bytes([hb])+bi+tail+pdesc+tc[m].astype('<u2').tobytes()
        out+=o; i=j
    assert i==len(b)
    return out
def clone_shell(n,sk,keep_global,disp,shader_f,tex0,thresh,name,alpha_tmpl,root=0):
    """disp: per-vertex displacement array (nv,3) in partition vertex order"""
    S=shape(n,sk); K=skininst(n,S['skin'])
    base=len(n.blocks); new={}
    order=['S','K','D','P','H','T','A']
    src={'S':sk,'K':S['skin'],'D':K['data'],'P':K['part'],'H':S['shader'],'T':None,'A':alpha_tmpl}
    hb=n.blocks[S['shader']]; i=8; ne,=struct.unpack_from('<I',hb,i); i+=4+4*ne+4; i+=8+16; tsoff=i; src['T'],=struct.unpack_from('<i',hb,tsoff)
    for j,kk in enumerate(order): new[kk]=base+j
    for kk in order:
        n.blocks.append(bytearray(n.blocks[src[kk]])); n.tidx.append(n.tidx[src[kk]])
    bS=n.blocks[new['S']]; struct.pack_into('<i',bS,0,add_string(n,name))
    o=S['offs']['skin']; struct.pack_into('<3i',bS,o,new['K'],new['H'],new['A'])
    bK=n.blocks[new['K']]; struct.pack_into('<2i',bK,0,new['D'],new['P'])
    # partition with displacement
    P=n.blocks[new['P']]
    npart,ds,vs=struct.unpack_from('<3I',P,0)
    n.blocks[new['P']]=build_partition(P,keep_global,disp)
    bH=n.blocks[new['H']]; i=8; ne,=struct.unpack_from('<I',bH,i); i+=4+4*ne+4
    struct.pack_into('<II',bH,i,*shader_f); struct.pack_into('<i',bH,tsoff,new['T'])
    bT=n.blocks[new['T']]; nt,=struct.unpack_from('<I',bT,0); j=4; tex=[]
    for _ in range(nt):
        l,=struct.unpack_from('<I',bT,j); tex.append(bT[j+4:j+4+l]); j+=4+l
    tex[0]=tex0.encode('latin1')
    n.blocks[new['T']]=bytearray(struct.pack('<I',nt)+b''.join(struct.pack('<I',len(t))+t for t in tex))
    bA=n.blocks[new['A']]; bA[len(bA)-1]=thresh
    off,ch=n.node_children(root); n.set_children(root,ch+[new['S']])
    return new
