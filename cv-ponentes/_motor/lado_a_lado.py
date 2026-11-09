"""Revisión del orquestador: tarjeta desktop del Figma (captura de get_screenshot del nodo tarjeta) junto a la de la simulación.
Uso: python lado_a_lado.py <slug> <captura_figma.png> <salida.png> [mitad]   (mitad = arriba|abajo para ver más grande)"""
import json, os, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
slug, fig, out = sys.argv[1:4]
parte = sys.argv[4] if len(sys.argv) > 4 else None
P = os.path.join(RAIZ, slug)
M = json.load(open(os.path.join(P, '_fuentes-figma', 'medidas.json'), encoding='utf-8'))
H = round(M['desktop']['tarjeta_alto'])
cap = os.path.join(P, '_generador', 'captura-1920.png')
a, b = out + '.a.png', out + '.b.png'
# la captura de Figma del nodo tarjeta incluye 16 px de sombra alrededor: se recorta al rectángulo de 1519 x alto
w, h = map(int, subprocess.run(['magick', 'identify', '-format', '%w %h', fig], capture_output=True, text=True).stdout.split())
k = w / (1519 + 32)
subprocess.run(['magick', fig, '-crop', f'{round(1519 * k)}x{round(H * k)}+{round(16 * k)}+{round(13 * k)}', '+repage', '-resize', '1519x', a])
subprocess.run(['magick', cap, '-crop', f'1519x{H}+201+930', '+repage', b])
if parte:
    for f in (a, b):
        g = f'1519x{H // 2 + 40}+0+{0 if parte == "arriba" else H // 2 - 40}'
        subprocess.run(['magick', f, '-crop', g, '+repage', f])
subprocess.run(['magick', a, b, '+append', '-resize', '1800x', out])
os.remove(a); os.remove(b)
print('ok', out)
