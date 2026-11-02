"""Unlink the head, eyes and teeth shapes from ABC's werewolf body so the MFA (Monster Lip Sync)
head part supplies the head. Blocks stay in the file (orphaned) - only root-node links change."""
import sys
from nif import Nif
DROP=('head','eyes','teeth')
def headless(src,dst):
    n=Nif(src); off,ch=n.node_children(0)
    keep=[c for c in ch if not (c>=0 and 'Shape' in n.btype(c) and n.name(c) and any(d in n.name(c).lower() for d in DROP))]
    n.set_children(0,keep); n.save(dst)
    return [n.name(c) for c in ch if c not in keep]
if __name__=='__main__':
    for w in '01': print(headless(sys.argv[1]+f'/malebodywerewolf_{w}.nif',sys.argv[2]+f'/malebodywerewolf_{w}.nif'))
