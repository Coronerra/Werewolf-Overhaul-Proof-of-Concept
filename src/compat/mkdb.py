"""Parse every plugin under input/ into db.pkl (used by norm.py / mkpatch.py)."""
import esp,glob,pickle
D={}
for p in glob.glob('input/**/*.es[pml]',recursive=True):
    v=esp.load(p); D[p.replace('\\','/').split('/')[-1]]={'masters':v['masters'],'recs':v['recs'],'flags':v['flags']}
pickle.dump(D,open('db.pkl','wb'))
