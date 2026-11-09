# Compara secciones: Figma (raw/fig1920.png) vs vista previa lado a lado. Uso: python sbs.py captura.png 'dict de posiciones' prefijo
import sys, ast
from PIL import Image
F = Image.open('raw/fig1920.png').convert('RGB'); B = Image.open(sys.argv[1]).convert('RGB')
pos = ast.literal_eval(sys.argv[2]); out = sys.argv[3]
FIG = {'ak-hero': (0, 1040), 'ak-met': (1036, 791), 'ak-prog': (1827, 717), 'ak-war': (2544, 1027), 'ak-plan': (3571, 956),
       'ak-cta': (4527, 447), 'ak-doc': (4974, 1066), 'ak-pres': (6040, 867), 'ak-cert': (6907, 1056), 'ak-inv': (7963, 941), 'ak-faq': (8904, 780)}
for n, (yf, h) in FIG.items():
    yb = 0 if n == 'ak-hero' else pos[n][0]
    a = F.crop((0, yf, 1920, yf + h)); b = B.crop((0, yb, 1920, yb + h))
    im = Image.new('RGB', (3860, h), 'white'); im.paste(a, (0, 0)); im.paste(b, (1940, 0))
    im.resize((1930, h // 2)).save(f'{out}_{n[3:]}.png')
