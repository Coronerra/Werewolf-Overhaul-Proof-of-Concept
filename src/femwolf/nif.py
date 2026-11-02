import struct
class Nif:
    def __init__(s,path):
        d=open(path,'rb').read(); s.raw=d
        i=d.index(b'\n')+1; s.hstr=d[:i]
        s.ver,=struct.unpack_from('<I',d,i); i+=4; s.endian=d[i]; i+=1
        s.uver,s.nblocks=struct.unpack_from('<II',d,i); i+=8
        s.bsver,=struct.unpack_from('<I',d,i); i+=4
        for _ in range(3): n=d[i]; i+=1+n
        if s.bsver>=130: n=d[i]; i+=1+n
        s.hpre_end=i
        nt,=struct.unpack_from('<H',d,i); i+=2; s.types=[]
        for _ in range(nt):
            n,=struct.unpack_from('<I',d,i); s.types.append(d[i+4:i+4+n].decode()); i+=4+n
        s.tidx=list(struct.unpack_from(f'<{s.nblocks}H',d,i)); i+=2*s.nblocks
        s.sizes=list(struct.unpack_from(f'<{s.nblocks}I',d,i)); i+=4*s.nblocks
        ns,s.maxlen=struct.unpack_from('<II',d,i); i+=8; s.strings=[]
        for _ in range(ns):
            n,=struct.unpack_from('<I',d,i); s.strings.append(d[i+4:i+4+n].decode('latin1')); i+=4+n
        ng,=struct.unpack_from('<I',d,i); i+=4; s.groups=d[i:i+4*ng]; i+=4*ng
        s.blocks=[]
        for sz in s.sizes: s.blocks.append(bytearray(d[i:i+sz])); i+=sz
        s.footer=d[i:]
    def btype(s,k): return s.types[s.tidx[k]]
    def name(s,k):
        si,=struct.unpack_from('<i',s.blocks[k],0); return s.strings[si] if 0<=si<len(s.strings) else None
    def node_children(s,k):
        b=s.blocks[k]; i=4; ne,=struct.unpack_from('<I',b,i); i+=4+4*ne; i+=4  # controller
        i+=4+12+36+4+4   # flags, trans, rot, scale, collision
        nc,=struct.unpack_from('<I',b,i); off=i
        ch=list(struct.unpack_from(f'<{nc}i',b,i+4)); return off,ch
    def set_children(s,k,ch):
        off,old=s.node_children(k); b=s.blocks[k]
        s.blocks[k]=b[:off]+struct.pack(f'<I{len(ch)}i',len(ch),*ch)+b[off+4+4*len(old):]
    def save(s,path):
        o=bytearray(s.hstr); o+=struct.pack('<IBII',s.ver,s.endian,s.uver,len(s.blocks))
        o+=s.raw[len(s.hstr)+13:s.hpre_end]
        o+=struct.pack('<H',len(s.types))
        for t in s.types: o+=struct.pack('<I',len(t))+t.encode()
        o+=struct.pack(f'<{len(s.blocks)}H',*s.tidx); o+=struct.pack(f'<{len(s.blocks)}I',*[len(b) for b in s.blocks])
        o+=struct.pack('<II',len(s.strings),max(len(x) for x in s.strings))
        for t in s.strings: o+=struct.pack('<I',len(t))+t.encode('latin1')
        o+=struct.pack('<I',len(s.groups)//4)+s.groups
        for b in s.blocks: o+=b
        o+=s.footer; open(path,'wb').write(o)
