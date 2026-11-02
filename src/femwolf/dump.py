import struct,zlib,sys
def subs(d):
    i=0;out=[]
    while i<len(d):
        t=d[i:i+4].decode('latin1');n=struct.unpack('<H',d[i+4:i+6])[0];out.append((t,d[i+6:i+6+n]));i+=6+n
    return out
def walk(d,i,end,want,res):
    while i<end:
        t=d[i:i+4]
        if t==b'GRUP':
            sz=struct.unpack('<I',d[i+4:i+8])[0];walk(d,i+24,i+sz,want,res);i+=sz;continue
        sz,fl,fid=struct.unpack('<III',d[i+4:i+16]);body=d[i+24:i+24+sz]
        if fl&0x40000: body=zlib.decompress(body[4:])
        res.append((t.decode(),fid,fl,subs(body)));i+=24+sz
d=open(sys.argv[1],'rb').read();hs=struct.unpack('<I',d[4:8])[0]
hdr=subs(d[24:24+hs]);print('masters',[s[1].rstrip(b'\0').decode() for s in hdr if s[0]=='MAST'])
res=[];walk(d,24+hs,len(d),None,res)
from collections import Counter;print(Counter(r[0] for r in res))
flt=sys.argv[2:] 
for t,fid,fl,ss in res:
    if flt and t not in flt: continue
    ed=next((s[1].rstrip(b'\0').decode('latin1') for s in ss if s[0]=='EDID'),'')
    if flt or 'were' in ed.lower(): print(t,hex(fid),ed,[(a,b.rstrip(b'\0').decode('latin1')) for a,b in ss if a in('MOD2','MOD3','MOD4','MOD5','MODL','RNAM','WNAM')][:12])
