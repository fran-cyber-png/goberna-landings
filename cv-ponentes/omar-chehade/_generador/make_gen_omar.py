"""Crea gen_omar.py a partir de gen_daniela.py (misma plantilla de Elementor) con el contenido y las medidas de Omar Chehade."""
import os
S = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(S, '..', '..', 'daniela-galvan', '_generador', 'gen_daniela.py'), encoding='utf-8').read()

def rep(a, b, n=1):
    global t
    c = t.count(a)
    assert c == n, (a[:70], c)
    t = t.replace(a, b)

rep("OUT = os.path.join(P, 'daniela-galvan.json')", "OUT = os.path.join(P, 'omar-chehade.json')")
rep("FOTO, LOGO = BIB + 'daniela-galvan.webp'", "FOTO, LOGO = BIB + 'omar-chehade.webp'")
rep("I = {k: du(k) for k in ['icono-investigacion-criminal', 'icono-inteligencia-digital', 'icono-prevencion-ciberdelito',\n                        'icono-osint-socmint',",
    "I = {k: du(k) for k in ['icono-derecho-constitucional', 'icono-derecho-penal', 'icono-lucha-anticorrupcion',\n                        'icono-gobernanza-politicas',")
rep("D = json.load(open(os.path.join(P, 'daniela-galvan-datos.json'), encoding='utf-8'))", "D = json.load(open(os.path.join(P, 'omar-chehade-datos.json'), encoding='utf-8'))")
rep("'Daniela Galvan')", "'Omar Chehade')", 2)
# medidas que cambian frente a Daniela (Figma 437:2 y 447:2)
rep("left: {L(999)}; top: {u(101)}; width: {u(721)} !important; height: {u(749)};", "left: {L(1059)}; top: {u(101)}; width: {u(661)} !important; height: {u(749)};")
rep("left: {ML(28)}; top: {m(542)}; width: {m(375)} !important; height: {m(389)};", "left: {ML(37)}; top: {m(542)}; width: {m(357)} !important; height: {m(390)};")
rep("""D_ICO = [(1, 'icono-investigacion-criminal', 36.52), (2, 'icono-inteligencia-digital', 37.82),
         (3, 'icono-prevencion-ciberdelito', 36.52), (4, 'icono-osint-socmint', 36.92)]
M_ICO = [(1, 'icono-investigacion-criminal', 23), (2, 'icono-inteligencia-digital', 23),
         (3, 'icono-prevencion-ciberdelito', 23), (4, 'icono-osint-socmint', 23)]""",
    """D_ICO = [(1, 'icono-derecho-constitucional', 37.93), (2, 'icono-derecho-penal', 37.82),
         (3, 'icono-lucha-anticorrupcion', 36.52), (4, 'icono-gobernanza-politicas', 36.92)]
M_ICO = [(1, 'icono-derecho-constitucional', 23), (2, 'icono-derecho-penal', 23),
         (3, 'icono-lucha-anticorrupcion', 23), (4, 'icono-gobernanza-politicas', 23)]""")
rep('"css_classes": "ak-dg"', '"css_classes": "ak-oc"')
rep('"title": "Daniela Galvan"', '"title": "Omar Chehade"')
for w in ['daniela', 'Daniela', 'investigacion-criminal', 'inteligencia-digital', 'prevencion-ciberdelito', 'osint-socmint']:
    assert w not in t, w
open(os.path.join(S, 'gen_omar.py'), 'w', encoding='utf-8').write(t)
print('ok')
