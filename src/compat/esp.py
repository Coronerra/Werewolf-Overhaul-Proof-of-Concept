import struct,zlib,os
def subs(b):
    o=0;r=[];big=None
    while o<len(b):
        t=b[o:o+4].decode('latin1');n=struct.unpack('<H',b[o+4:o+6])[0];o+=6
        if t=='XXXX': big=struct.unpack('<I',b[o:o+4])[0];o+=4;continue
        if big is not None: n=big;big=None
        r.append((t,b[o:o+n]));o+=n
    return r
def load(p):
    d=open(p,'rb').read();hs=struct.unpack('<I',d[4:8])[0];flags=struct.unpack('<I',d[8:12])[0]
    hdr=subs(d[24:24+hs]);mast=[s[1].rstrip(b'\0').decode('latin1') for s in hdr if s[0]=='MAST']
    me=os.path.basename(p);recs={}
    def res(fid):
        i=fid>>24
        return ((mast[i] if i<len(mast) else me).lower(),fid&0xFFFFFF if i<len(mast) else fid&0xFFFFFF)
    def walk(o,e):
        while o<e:
            t=d[o:o+4].decode('latin1');sz=struct.unpack('<I',d[o+4:o+8])[0]
            if t=='GRUP': walk(o+24,o+sz);o+=sz;continue
            fl,fid=struct.unpack('<II',d[o+8:o+16]);body=d[o+24:o+24+sz]
            if fl&0x40000: body=zlib.decompress(body[4:])
            ss=subs(body);ed=next((s[1].rstrip(b'\0').decode('latin1') for s in ss if s[0]=='EDID'),'')
            recs[res(fid)]=(t,ed,ss,fl)
            o+=24+sz
    walk(24+hs,len(d))
    return dict(name=me,masters=mast,recs=recs,res=res,flags=flags)
