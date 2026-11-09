"""Crea gen_andres.py a partir de gen_fernando.py (misma plantilla de Elementor) con el contenido y las medidas de Andrés Peñaranda."""
import os
S = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(S, '..', '..', 'fernando-cocho', '_generador', 'gen_fernando.py'), encoding='utf-8').read()

def rep(a, b, n=1):
    global t
    c = t.count(a)
    assert c == n, (a[:70], c)
    t = t.replace(a, b)

rep("OUT = os.path.join(P, 'fernando-cocho.json')", "OUT = os.path.join(P, 'andres-penaranda.json')")
rep("FOTO, LOGO = BIB + 'fernando-cocho.webp'", "FOTO, LOGO = BIB + 'andres-penaranda.webp'")
rep("I = {k: du(k) for k in ['icono-metodologia-inteligencia', 'icono-inteligencia-estrategica', 'icono-seguridad-nacional',\n                        'icono-ciberinteligencia',",
    "I = {k: du(k) for k in ['icono-operaciones-informacion', 'icono-inteligencia-estrategica', 'icono-comunicacion-estrategica',\n                        'icono-seguridad-defensa',")
rep("D = json.load(open(os.path.join(P, 'fernando-cocho-datos.json'), encoding='utf-8'))", "D = json.load(open(os.path.join(P, 'andres-penaranda-datos.json'), encoding='utf-8'))")
rep('''RES = f"<p><b>{D['resumen']['negrita']}</b> {D['resumen']['resto']}</p>"''', '''RES = f"<p><b>{D['resumen']['negrita']}</b>{D['resumen']['resto']}</p>"''')
rep("SUB_M = '<p>' + D['titular'].replace(' | ', ' <span class=\"ak-pipe\">|</span> ') + '</p>'", "SUB_M = SUB_D")
rep("ESP = ['Metodología de<br>Inteligencia', 'Inteligencia<br>Estratégica', 'Seguridad<br>Nacional', 'Ciberinteligencia']",
    "ESP = ['Operaciones de<br>Información', 'Inteligencia<br>Estratégica', 'Comunicación<br>Estratégica', 'Seguridad y<br>Defensa Nacional']")
rep("STATS = [(c['valor'], c['texto']) for c in D['cifras']]", "STATS = [(b, s) for b, s in D['cifras']]")
rep("h('FERNANDO', 'h1', 'ak-d-n1'), h('COCHO', 'h1', 'ak-d-n2')", "h('ANDRÉS', 'h1', 'ak-d-n1'), h('PEÑARANDA', 'h1', 'ak-d-n2')")
rep("h('FERNANDO', 'h1', 'ak-m-n1'), h('COCHO', 'h1', 'ak-m-n2')", "h('ANDRÉS', 'h1', 'ak-m-n1'), h('PEÑARANDA', 'h1', 'ak-m-n2')")
rep("'Fernando Cocho Pérez')", "'Andrés Peñaranda')", 2)
# medidas que cambian frente a Fernando (Figma 501:2 y 509:168)
rep("font: 800 {u(87)} / 0.964 {MONT}; color: #fff; letter-spacing: {u(2.56)};", "font: 800 {u(87)} / 0.964 {MONT}; color: #fff; letter-spacing: {u(3.48)};")
rep("font: 800 {m(42)} / 0.964 {MONT}; color: #fff; letter-spacing: {m(1.2359)};", "font: 800 {m(42)} / 0.964 {MONT}; color: #fff; letter-spacing: {m(1.68)};")
rep("left: {L(982)}; top: {u(101)}; width: {u(738)} !important; height: {u(749)};", "left: {L(928)}; top: {u(101)}; width: {u(792)} !important; height: {u(749)};")
rep("left: {ML(20)}; top: {m(542)}; width: {m(391)} !important; height: {m(390)};", "left: {ML(9)}; top: {m(542)}; width: {m(412)} !important; height: {m(389)};")
rep("selector .ak-d-st2 {{ height: {u(87)}; }}", "selector .ak-d-st2 {{ height: {u(65)}; }}")
rep("selector .ak-m-sub .ak-pipe {{ font-family: {OPEN}; line-height: 1; }}\n", "")
rep("""D_ICO = [(1, 'icono-metodologia-inteligencia', 36.92), (2, 'icono-inteligencia-estrategica', 37.82),
         (3, 'icono-seguridad-nacional', 37.93), (4, 'icono-ciberinteligencia', 36.52)]
M_ICO = [(1, 'icono-metodologia-inteligencia', 22.39), (2, 'icono-inteligencia-estrategica', 22.94),
         (3, 'icono-seguridad-nacional', 23), (4, 'icono-ciberinteligencia', 22.15)]""",
    """D_ICO = [(1, 'icono-operaciones-informacion', 36.92), (2, 'icono-inteligencia-estrategica', 37.82),
         (3, 'icono-comunicacion-estrategica', 36.52), (4, 'icono-seguridad-defensa', 36.52)]
M_ICO = [(1, 'icono-operaciones-informacion', 22.39), (2, 'icono-inteligencia-estrategica', 22.94),
         (3, 'icono-comunicacion-estrategica', 22.15), (4, 'icono-seguridad-defensa', 22.15)]""")
rep('"css_classes": "ak-fc"', '"css_classes": "ak-ap"')
rep('"title": "Fernando Cocho Pérez"', '"title": "Andrés Peñaranda"')
for w in ['fernando', 'Fernando', 'FERNANDO', 'COCHO', 'ciberinteligencia', 'metodologia', 'pipe']:
    assert w not in t, w
open(os.path.join(S, 'gen_andres.py'), 'w', encoding='utf-8').write(t)
print('ok')
