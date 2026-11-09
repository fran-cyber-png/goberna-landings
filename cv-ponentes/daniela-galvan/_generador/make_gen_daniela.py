"""Crea gen_daniela.py a partir de gen_andres.py (misma plantilla de Elementor) con el contenido y las medidas de Daniela Galvan."""
import os
S = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(S, '..', '..', 'andres-penaranda', '_generador', 'gen_andres.py'), encoding='utf-8').read()

def rep(a, b, n=1):
    global t
    c = t.count(a)
    assert c == n, (a[:70], c)
    t = t.replace(a, b)

rep("OUT = os.path.join(P, 'andres-penaranda.json')", "OUT = os.path.join(P, 'daniela-galvan.json')")
rep("FOTO, LOGO = BIB + 'andres-penaranda.webp'", "FOTO, LOGO = BIB + 'daniela-galvan.webp'")
rep("I = {k: du(k) for k in ['icono-operaciones-informacion', 'icono-inteligencia-estrategica', 'icono-comunicacion-estrategica',\n                        'icono-seguridad-defensa',",
    "I = {k: du(k) for k in ['icono-investigacion-criminal', 'icono-inteligencia-digital', 'icono-prevencion-ciberdelito',\n                        'icono-osint-socmint',")
rep("D = json.load(open(os.path.join(P, 'andres-penaranda-datos.json'), encoding='utf-8'))", "D = json.load(open(os.path.join(P, 'daniela-galvan-datos.json'), encoding='utf-8'))")
# los ítems de las listas vienen como HTML (la negrita no siempre va al principio)
rep("return '<ul>' + ''.join(f'<li><b>{b}</b>{r}</li>' for b, r in rows) + '</ul>'", "return '<ul>' + ''.join(f'<li>{x}</li>' for x in rows) + '</ul>'")
rep("ESP = ['Operaciones de<br>Información', 'Inteligencia<br>Estratégica', 'Comunicación<br>Estratégica', 'Seguridad y<br>Defensa Nacional']",
    "ESP = D['especialidades_html']")
rep("h('ANDRÉS', 'h1', 'ak-d-n1'), h('PEÑARANDA', 'h1', 'ak-d-n2')", "h(D['nombre']['linea1'], 'h1', 'ak-d-n1'), h(D['nombre']['linea2'], 'h1', 'ak-d-n2')")
rep("h('ANDRÉS', 'h1', 'ak-m-n1'), h('PEÑARANDA', 'h1', 'ak-m-n2')", "h(D['nombre']['linea1'], 'h1', 'ak-m-n1'), h(D['nombre']['linea2'], 'h1', 'ak-m-n2')")
rep("'Andrés Peñaranda')", "'Daniela Galvan')", 2)
# medidas que cambian frente a Andrés (Figma 450:2 y 453:2)
rep("font: 800 {u(87)} / 0.964 {MONT}; color: #fff; letter-spacing: {u(3.48)};", "font: 800 {u(87)} / 0.964 {MONT}; color: #fff; letter-spacing: {u(2.56)};")
rep("font: 800 {m(42)} / 0.964 {MONT}; color: #fff; letter-spacing: {m(1.68)};", "font: 800 {m(42)} / 0.964 {MONT}; color: #fff; letter-spacing: {m(1.2359)};")
rep("left: {L(928)}; top: {u(101)}; width: {u(792)} !important; height: {u(749)};", "left: {L(999)}; top: {u(101)}; width: {u(721)} !important; height: {u(749)};")
rep("left: {ML(9)}; top: {m(542)}; width: {m(412)} !important; height: {m(389)};", "left: {ML(28)}; top: {m(542)}; width: {m(375)} !important; height: {m(389)};")
rep("""D_ICO = [(1, 'icono-operaciones-informacion', 36.92), (2, 'icono-inteligencia-estrategica', 37.82),
         (3, 'icono-comunicacion-estrategica', 36.52), (4, 'icono-seguridad-defensa', 36.52)]
M_ICO = [(1, 'icono-operaciones-informacion', 22.39), (2, 'icono-inteligencia-estrategica', 22.94),
         (3, 'icono-comunicacion-estrategica', 22.15), (4, 'icono-seguridad-defensa', 22.15)]""",
    """D_ICO = [(1, 'icono-investigacion-criminal', 36.52), (2, 'icono-inteligencia-digital', 37.82),
         (3, 'icono-prevencion-ciberdelito', 36.52), (4, 'icono-osint-socmint', 36.92)]
M_ICO = [(1, 'icono-investigacion-criminal', 23), (2, 'icono-inteligencia-digital', 23),
         (3, 'icono-prevencion-ciberdelito', 23), (4, 'icono-osint-socmint', 23)]""")
rep('"css_classes": "ak-ap"', '"css_classes": "ak-dg"')
rep('"title": "Andrés Peñaranda"', '"title": "Daniela Galvan"')
for w in ['andres', 'Andrés', 'ANDRÉS', 'PEÑARANDA', 'operaciones-informacion', 'comunicacion-estrategica', 'seguridad-defensa', 'inteligencia-estrategica']:
    assert w not in t, w
open(os.path.join(S, 'gen_daniela.py'), 'w', encoding='utf-8').write(t)
print('ok')
