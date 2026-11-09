# Fondo de Inversión como en Figma: imagen en "luz suave" sobre #15262F + degradado #15262F (transparente a la izquierda, sólido a la derecha)
import numpy as np, sys
from PIL import Image
H = 'C:/Users/Consultoría/Documents/Director-Seguridad/_work/inv/'
W, Hh, RW = 1920, 938, 1407
bg = np.array([0x15, 0x26, 0x2F], float) / 255
src = Image.open(H + 'raw1').convert('RGB').resize((RW, Hh), Image.LANCZOS)
cs = np.asarray(src, float) / 255
cb = np.broadcast_to(bg, cs.shape)
d = np.where(cb <= 0.25, ((16 * cb - 12) * cb + 4) * cb, np.sqrt(cb))
soft = np.where(cs <= 0.5, cb - (1 - 2 * cs) * cb * (1 - cb), cb + (2 * cs - 1) * (d - cb))
a = (np.arange(RW) / RW)[None, :, None]          # degradado: 0 a la izquierda, 1 en el borde derecho del rectángulo
rect = soft * (1 - a) + bg * a
out = np.empty((Hh, W, 3)); out[:] = bg; out[:, :RW] = rect
img = Image.fromarray(np.clip(out * 255 + 0.5, 0, 255).astype('uint8'))
img.save(H + 'compuesto.png')
# comparación con el render de Figma en zonas sin texto
ref = np.asarray(Image.open(H + 'sec_export.png').convert('RGB'), float)
mine = np.asarray(img, float)
for name, (x0, y0, x1, y1) in {'izq-arriba': (0, 0, 200, 90), 'izq-abajo': (0, 880, 200, 938), 'centro': (900, 300, 1020, 600), 'der': (1750, 0, 1920, 938)}.items():
    print(name, round(np.abs(ref[y0:y1, x0:x1] - mine[y0:y1, x0:x1]).mean(), 2))
