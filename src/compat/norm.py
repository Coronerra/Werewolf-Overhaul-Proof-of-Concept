import pickle,struct,collections
D=pickle.load(open('db.pkl','rb'))
FID={'SPLO':[0],'KWDA':'all','VTCK':[0,4],'QNAM':[0],'HEAD':[0],'ATKD':[8],'WNAM':[0],'RNAM':[0],'NAM8':[0],'ATKR':[0],'GNAM':[0],'NAM4':[0],'NAM5':[0],'NAM7':[0],'ONAM':[0],'LNAM':[0],'UNES':[0],'DNAM':[0],'HNAM':'all','ENAM':'all','TINP':[],'FTSM':[0],'FTSF':[0],'DFTM':[0],'DFTF':[0],'SNAM':[0],'PNAM':[],'NAM3':[]}
def rf(p,f):
    m=D[p]['masters'];i=f>>24
    return (m[i] if i<len(m) else p, f&0xffffff) if f else 0
def norm(p,t,v):
    spec=FID.get(t)
    if not spec or len(v)%4 and spec=='all': return v.hex()
    offs=range(0,len(v),4) if spec=='all' else spec
    out=[];last=0
    for o in offs:
        if o+4>len(v): continue
        out.append(v[last:o].hex());f=struct.unpack('<I',v[o:o+4])[0];out.append(str(rf(p,f)));last=o+4
    out.append(v[last:].hex());return '|'.join(out)
def grouped(p,k):
    g=collections.OrderedDict()
    for t,v in D[p]['recs'][k][2]: g.setdefault(t,[]).append(norm(p,t,v))
    return g
