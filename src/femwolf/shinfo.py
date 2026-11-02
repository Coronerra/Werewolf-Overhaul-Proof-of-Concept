import struct
def shader(n,k):
    b=n.blocks[k]; st,=struct.unpack_from('<I',b,0); i=8; ne,=struct.unpack_from('<I',b,i); i+=4+4*ne+4
    f1,f2=struct.unpack_from('<II',b,i); i+=8; uv=struct.unpack_from('<4f',b,i); i+=16; ts,=struct.unpack_from('<i',b,i); i+=4
    i+=16; i+=4; al,ref,gl=struct.unpack_from('<3f',b,i)
    tb=n.blocks[ts]; nt,=struct.unpack_from('<I',tb,0); j=4; tex=[]
    for _ in range(nt):
        l,=struct.unpack_from('<I',tb,j); tex.append(tb[j+4:j+4+l].decode('latin1')); j+=4+l
    return dict(type=st,f1=f1,f2=f2,uv=uv,ts=ts,alpha=al,gloss=gl,tex=tex)
def alpha(n,k):
    a=n.blocks[k]; f,th=struct.unpack_from('<HB',a,len(a)-3); return f,th
