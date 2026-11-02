from PIL import Image,ImageFilter
import numpy as np,struct
fw=np.array(Image.open('input/fluffworks/textures/actors/character/werewolf/werewolfbody_shell.dds'))
def make(diff,o):
    d=Image.open(diff).convert('RGB').resize((1024,1024),Image.LANCZOS).filter(ImageFilter.GaussianBlur(2))
    im=Image.fromarray(np.dstack([np.array(d),fw[...,3]]),'RGBA'); w,h=im.size; lv=[]; cur=im
    while True:
        lv.append(np.array(cur)[...,[2,1,0,3]].tobytes())
        if cur.size==(1,1): break
        cur=cur.resize((max(1,cur.size[0]//2),max(1,cur.size[1]//2)),Image.BOX)
    hdr=struct.pack('<4sIIIIIII44s',b'DDS ',124,0x1|0x2|0x4|0x8|0x1000|0x20000,h,w,w*4,0,len(lv),b'\0'*44)
    pf=struct.pack('<II4sIIIII',32,0x41,b'\0\0\0\0',32,0x00ff0000,0x0000ff00,0x000000ff,0xff000000)
    open(o,'wb').write(hdr+pf+struct.pack('<IIIII',0x401008,0,0,0,0)+b''.join(lv))
T='out/fluffy/textures/actors/character/werewolf/coronerra/'
make('input/HDT werewolves SMP/HDT Werewolf SSE v2.5/HDT Werewolf SSE/textures/actors/character/werewolf/FemaleWerewolfbody.dds',T+'FemaleWerewolfBody_shell.dds')
make('input/BakaFactory Animated Beasts Cocks/Textures/Actors/Character/WereWolf/werewolfbody.dds',T+'WerewolfBody_shell.dds')
for f in ['FemaleWerewolfBody_shell.dds','WerewolfBody_shell.dds']: print(f,Image.open(T+f).size)
