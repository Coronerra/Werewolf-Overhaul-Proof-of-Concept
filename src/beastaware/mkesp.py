import struct
def sub(t,b): return t.encode()+struct.pack('<H',len(b))+b
def zs(s): return s.encode('cp1252')+b'\0'
def ws(s): b=s.encode(); return struct.pack('<H',len(b))+b
def rec(t,fid,body,flags=0): return t.encode()+struct.pack('<IIIIHH',len(body),flags,fid,0,44,0)+body
def grup(label,content): return b'GRUP'+struct.pack('<I',24+len(content))+label.encode()+struct.pack('<iHHHH',0,0,0,44,0)+content
QID=0x01000800  # local index 01 (after one master), ESL range
def objprop(name,fid): return ws(name)+bytes([1,1])+struct.pack('<HhI',0,-1,fid)
def script(name,props): return ws(name)+b'\0'+struct.pack('<H',len(props))+b''.join(props)
vmad = struct.pack('<hhH',5,2,2)
vmad += script('BA_Main',[])
vmad += script('BA_MCM',[objprop('Main',QID)])
vmad += b'\x02'+struct.pack('<H',0)+ws('')          # fragments: version 2, count 0, empty filename
vmad += struct.pack('<H',1)                          # 1 alias
vmad += struct.pack('<HhI',0,0,QID)                  # alias 0 on this quest
vmad += struct.pack('<hhH',5,2,2)+script('SKI_PlayerLoadGameAlias',[])+script('BA_PlayerAlias',[])
body = sub('EDID',zs('BA_BeastAwareQuest'))+sub('VMAD',vmad)+sub('FULL',zs('Beast Aware'))
body += sub('DNAM',bytes.fromhex('110100ff0000000000000000'))+sub('NEXT',b'')+sub('ANAM',struct.pack('<I',1))
body += sub('ALST',struct.pack('<I',0))+sub('ALID',zs('PlayerAlias'))+sub('FNAM',struct.pack('<I',0))+sub('ALFR',struct.pack('<I',0x14))+sub('VTCK',struct.pack('<I',0))+sub('ALED',b'')
q = rec('QUST',QID,body)
hedr = struct.pack('<fII',1.71,1,0x801)
tes4 = sub('HEDR',hedr)+sub('CNAM',zs('That Guy (Coronerra)'))+sub('SNAM',zs('Beast Aware v1.1 - SkyrimNet NPCs notice your beast form'))+sub('MAST',zs('Skyrim.esm'))+sub('DATA',struct.pack('<Q',0))
out = rec('TES4',0,tes4,flags=0x200)+grup('QUST',q)
open('BeastAware.esp','wb').write(out); print(len(out))
