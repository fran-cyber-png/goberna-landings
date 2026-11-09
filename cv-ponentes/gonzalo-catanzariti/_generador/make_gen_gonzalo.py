"""Crea gen_gonzalo.py a partir de gen_omar.py (misma plantilla de Elementor) con el contenido y las medidas de Gonzalo Catanzariti."""
import os
S = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(S, '..', '..', 'omar-chehade', '_generador', 'gen_omar.py'), encoding='utf-8').read()

def rep(a, b, n=1):
    global t
    c = t.count(a)
    assert c == n, (a[:70], c)
    t = t.replace(a, b)

rep("OUT = os.path.join(P, 'omar-chehade.json')", "OUT = os.path.join(P, 'gonzalo-catanzariti.json')")
rep("FOTO, LOGO = BIB + 'omar-chehade.webp'", "FOTO, LOGO = BIB + 'gonzalo-catanzariti.webp'")
rep("I = {k: du(k) for k in ['icono-derecho-constitucional', 'icono-derecho-penal', 'icono-lucha-anticorrupcion',\n                        'icono-gobernanza-politicas',",
    "I = {k: du(k) for k in ['icono-arquitectura-ciberseguridad', 'icono-investigacion-ciberdelitos', 'icono-informatica-forense',\n                        'icono-osint-socmint',")
rep("D = json.load(open(os.path.join(P, 'omar-chehade-datos.json'), encoding='utf-8'))", "D = json.load(open(os.path.join(P, 'gonzalo-catanzariti-datos.json'), encoding='utf-8'))")
rep("'Omar Chehade')", "'Gonzalo Catanzariti')", 2)
# medidas que cambian frente a Omar (Figma 532:2 y 538:2); la foto está volteada en Figma y el webp ya va volteado
rep("left: {L(1059)}; top: {u(101)}; width: {u(661)} !important; height: {u(749)};", "left: {L(1026)}; top: {u(101)}; width: {u(694)} !important; height: {u(749)};")
rep("left: {ML(37)}; top: {m(542)}; width: {m(357)} !important; height: {m(390)};", "left: {ML(35)}; top: {m(542)}; width: {m(360)} !important; height: {m(389)};")
# CATANZARITI: tracking 3.48 (desktop) y 1.68 (móvil), como en Figma
rep("font: 800 {u(87)} / 0.964 {MONT}; color: #fff; letter-spacing: {u(2.56)};", "font: 800 {u(87)} / 0.964 {MONT}; color: #fff; letter-spacing: {u(3.48)};")
rep("font: 800 {m(42)} / 0.964 {MONT}; color: #fff; letter-spacing: {m(1.2359)};", "font: 800 {m(42)} / 0.964 {MONT}; color: #fff; letter-spacing: {m(1.68)};")
# la descripción de «Líder» mide 411 (más que la caja de 382): en una línea, desbordando a la derecha como en Figma
rep("selector .ak-d-small p {{ font: 400 {u(18)} / {u(22)} {OPEN}; color: {INK}; }}", "selector .ak-d-small p {{ font: 400 {u(18)} / {u(22)} {OPEN}; color: {INK}; white-space: nowrap; }}")
rep("""D_ICO = [(1, 'icono-derecho-constitucional', 37.93), (2, 'icono-derecho-penal', 37.82),
         (3, 'icono-lucha-anticorrupcion', 36.52), (4, 'icono-gobernanza-politicas', 36.92)]
M_ICO = [(1, 'icono-derecho-constitucional', 23), (2, 'icono-derecho-penal', 23),
         (3, 'icono-lucha-anticorrupcion', 23), (4, 'icono-gobernanza-politicas', 23)]""",
    """D_ICO = [(1, 'icono-arquitectura-ciberseguridad', 36.52), (2, 'icono-investigacion-ciberdelitos', 36.52),
         (3, 'icono-informatica-forense', 36.92), (4, 'icono-osint-socmint', 37.82)]
M_ICO = [(1, 'icono-arquitectura-ciberseguridad', 22.15), (2, 'icono-investigacion-ciberdelitos', 22.15),
         (3, 'icono-informatica-forense', 22.39), (4, 'icono-osint-socmint', 22.94)]""")
rep('"css_classes": "ak-oc"', '"css_classes": "ak-gc"')
rep('"title": "Omar Chehade"', '"title": "Gonzalo Catanzariti"')
for w in ['omar', 'Omar', 'chehade', 'derecho-', 'lucha-', 'gobernanza-', 'ak-oc']:
    assert w not in t, w
open(os.path.join(S, 'gen_gonzalo.py'), 'w', encoding='utf-8').write(t)
print('ok')
