import struct,zlib
exec(open('dump.py').read().split("d=open")[0])
def load(p):
    d=open(p,'rb').read();hs=struct.unpack('<I',d[4:8])[0]
    hdr=subs(d[24:24+hs]); m=[s[1].rstrip(b'\0').decode() for s in hdr if s[0]=='MAST']
    res=[];walk(d,24+hs,len(d),None,res); return m,{(r[0],r[1]):r for r in res}
