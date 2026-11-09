# Lado a lado Figma (izq) vs vista previa (der) por sección: python sbs.py prev.png
import sys
from PIL import Image
F = Image.open('fig1920.png').convert('RGB'); D = Image.open(sys.argv[1]).convert('RGB')
FIG = {'hd':(0,90),'hero':(90,879),'met':(969,858),'prog':(1827,717),'war':(2544,1027),'plan':(3571,956),'cta':(4527,447),
       'doc':(4974,1066),'pres':(6040,867),'cert':(6907,1056),'inv':(7963,941),'faq':(8904,780)}
PRE = eval(sys.argv[2]) if len(sys.argv) > 2 else {}
for k,(y,h) in FIG.items():
    if k not in PRE: continue
    y2,h2 = PRE[k]
    a = F.crop((0,y,1920,y+h)); b = D.crop((0,y2,1920,y2+h2))
    H = max(h,h2); im = Image.new('RGB',(3860,H),'white'); im.paste(a,(0,0)); im.paste(b,(1940,0))
    im.resize((1930, H//2)).save(f'cmp/{k}.png')
