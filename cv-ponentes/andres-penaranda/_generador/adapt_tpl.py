"""Pasa la plantilla de Fernando Cocho (fernando-tpl.html) al contenido y medidas de Andrés Peñaranda (Figma 501:2 / 509:168)."""
import re, os
S = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(S, 'andres-tpl.html')
t = open(os.path.join(S, '..', '..', 'fernando-cocho', '_generador', 'fernando-tpl.html'), encoding='utf-8').read()

def rep(a, b, n=1):
    global t
    c = t.count(a)
    assert c == n, (a[:60], c)
    t = t.replace(a, b)

rep('<title>Fernando Cocho Pérez</title>', '<title>Andrés Peñaranda</title>')
rep('.name-d .n2{font:800 87px/.964 var(--display);color:#fff;letter-spacing:2.56px}', '.name-d .n2{font:800 87px/.964 var(--display);color:#fff;letter-spacing:3.48px}')
rep('.foto-d{left:982px;top:101px;width:738px;height:749px}', '.foto-d{left:928px;top:101px;width:792px;height:749px}')
rep('.st2{height:87px}.st2 .big{font-size:38px}.st2 .small{top:43px;width:382px}', '.st2{height:65px}.st2 .big{font-size:38px}.st2 .small{top:43px;white-space:nowrap}')
rep('.name-m .n2{font:800 42px/.964 var(--display);color:#fff;letter-spacing:1.2359px}', '.name-m .n2{font:800 42px/.964 var(--display);color:#fff;letter-spacing:1.68px}')
rep('.sub-m .pipe{font-family:var(--body);line-height:1}\n', '')
rep('.foto-m{left:20px;top:542px;width:391px;height:390px}', '.foto-m{left:9px;top:542px;width:412px;height:389px}')
t = t.replace('ak-fc-', 'ak-ap-')
rep('<h1>Plantilla Fernando Cocho Pérez</h1>', '<h1>Plantilla Andrés Peñaranda</h1>')
rep('(487:2, 490:2, 492:2)', '(501:2, 506:141, 509:168)')

# ---- portada desktop
rep('data-w="Título h1 · Montserrat 800 64/0.964">FERNANDO</p>', 'data-w="Título h1 · Montserrat 800 64/0.964">ANDRÉS</p>')
rep('data-w="Título h1 · Montserrat 800 87/0.964">COCHO</p>', 'data-w="Título h1 · Montserrat 800 87/0.964">PEÑARANDA</p>')
t = re.sub(r'<p class="sub" data-w="[^"]*">.*?</p>', '<p class="sub" data-w="Texto · Open Sans 28/48 · 2 líneas">Especialista en Operaciones de Información e Inteligencia Estratégica</p>', t, flags=re.S)
rep('data-w="Imagen · foto 738×749"><img src="__FOTO__" alt="Fernando Cocho Pérez">', 'data-w="Imagen · foto 792×749"><img src="__FOTO__" alt="Andrés Peñaranda">')
ROW = '''<div class="esp-row-d">
      <div class="esp-it" data-w="Ícono + texto · Open Sans 18/24"><div class="esp-ico"><img src="__I_OPE__" alt="" style="height:36.92px"></div>Operaciones de<br>Información</div><div class="sep-d"></div>
      <div class="esp-it" data-w="Ícono + texto"><div class="esp-ico"><img src="__I_EST__" alt="" style="height:37.82px"></div>Inteligencia<br>Estratégica</div><div class="sep-d"></div>
      <div class="esp-it" data-w="Ícono + texto"><div class="esp-ico"><img src="__I_COM__" alt="" style="height:36.52px"></div>Comunicación<br>Estratégica</div><div class="sep-d"></div>
      <div class="esp-it" data-w="Ícono + texto"><div class="esp-ico"><img src="__I_SEG__" alt="" style="height:36.52px"></div>Seguridad y<br>Defensa Nacional</div>
    </div>
  </div>
</section>'''
t, n = re.subn(r'<div class="esp-row-d">.*?</div>\n  </div>\n</section>', lambda m: ROW, t, count=1, flags=re.S); assert n == 1

RES = ('<b>Andrés Peñaranda es consultor internacional y especialista en operaciones de información, inteligencia estratégica y comunicación estratégica, con más de 25 años de experiencia en seguridad y defensa nacional.</b>'
       ' Ha desarrollado asesorías para instituciones públicas y privadas en escenarios complejos, integrando análisis estratégico, gestión de riesgos, comunicación estratégica y planificación para la toma de decisiones. Su trayectoria está enfocada en el fortalecimiento de capacidades institucionales, análisis de amenazas y diseño de estrategias para enfrentar entornos de alta incertidumbre.')
t = re.sub(r'(<p class="res-d"[^>]*>).*?</p>', lambda m: m.group(1) + RES + '</p>', t, flags=re.S)
t = re.sub(r'(<p class="res-m"[^>]*>).*?</p>', lambda m: m.group(1) + RES + '</p>', t, flags=re.S)

CAR = [('Consultor Internacional', ' en Seguridad, Inteligencia Estratégica y Comunicación Estratégica.'),
       ('Especialista en Operaciones de Información', ' y planificación estratégica para escenarios complejos.'),
       ('Asesor en Seguridad y Defensa Nacional', ', análisis de amenazas y fortalecimiento institucional.'),
       ('Consultor en proyectos de gobernanza', ', gestión estratégica y comunicación institucional.')]
FOR = [('Magíster en Administración, Gobierno y Políticas Públicas.', ''),
       ('Formación especializada', ' en Operaciones de Información, Inteligencia Estratégica y Seguridad Nacional.')]
APO = [('Más de 25 años de experiencia', ' en seguridad, defensa, inteligencia y asesoría estratégica.'),
       ('Desarrollo de estrategias de operaciones de información y comunicación estratégica', ' para escenarios de crisis y alta complejidad.'),
       ('Participación en proyectos', ' relacionados con gobernanza, seguridad y fortalecimiento de capacidades institucionales.')]

def lis(items, cls, src, ind):
    return ''.join(f'\n{ind}<li><img class="{cls}" src="{src}" alt=""><span><b>{b}</b>{r}</span></li>' for b, r in items)

uls = list(re.finditer(r'(<ul class="list-[dm][^"]*"[^>]*>)(.*?)(\n\s*</ul>)', t, flags=re.S))
assert len(uls) == 6
specs = [(CAR, 'dot', '__V_DOT__', '        ', '4 ítems'), (FOR, 'dot', '__V_DOT__', '        ', '2 ítems'), (APO, 'arr', '__V_ARR__', '        ', '3 ítems'),
         (CAR, 'dot', '__V_DOT_M__', '      ', None), (FOR, 'dot', '__V_DOT_M__', '      ', '2 ítems'), (APO, 'arr', '__V_ARR_M__', '      ', None)]
out = []; last = 0
for m, (it, cls, src, ind, n) in zip(uls, specs):
    head = m.group(1)
    if n:
        head = re.sub(r'\d+ ítems', n, head)
    out.append(t[last:m.start()] + head + lis(it, cls, src, ind) + m.group(3)); last = m.end()
out.append(t[last:]); t = ''.join(out)

STATS = '''<div class="stat-d st1" data-w="Texto · Montserrat 800 37 / Open Sans 18/22"><p class="big">+25 años</p><p class="small">Seguridad y defensa nacional</p></div>
        <div class="stat-d st2" data-w="Texto · Montserrat 800 38 / Open Sans 18/22"><p class="big">Magíster</p><p class="small">Administración, Gobierno y Políticas Públicas</p></div>
        <div class="stat-d st3" data-w="Texto · Montserrat 800 37 / Open Sans 18/28"><p class="big">Consultor</p><p class="small">Internacional en Inteligencia Estratégica</p></div>'''
t, n = re.subn(r'<div class="stat-d st1".*?</div>\n\s*<div class="stat-d st2".*?</div>\n\s*<div class="stat-d st3".*?</div>', lambda m: STATS, t, flags=re.S); assert n == 1
rep('alto 313"', 'alto 291"')
DATOS = '''<div class="dato-m"><p class="big">+25 años</p><p class="small">Seguridad y defensa nacional</p></div>
      <div class="dato-m d2"><p class="big">Magíster</p><p class="small">Administración, Gobierno y Políticas Públicas</p></div>
      <div class="dato-m d3"><p class="big">Consultor</p><p class="small">Internacional en Inteligencia Estratégica</p></div>'''
t, n = re.subn(r'<div class="dato-m">.*?</div>\n\s*<div class="dato-m d2">.*?</div>\n\s*<div class="dato-m d3">.*?</div>', lambda m: DATOS, t, flags=re.S); assert n == 1

# ---- portada móvil
rep('data-w="Título h1 · Montserrat 800 30.9">FERNANDO</p>', 'data-w="Título h1 · Montserrat 800 30.9">ANDRÉS</p>')
rep('data-w="Título h1 · Montserrat 800 42">COCHO</p>', 'data-w="Título h1 · Montserrat 800 42">PEÑARANDA</p>')
t = re.sub(r'<p class="abs sub-m"[^>]*>.*?</p>', '<p class="abs sub-m" data-w="Texto · Manrope 16/28 · 2 líneas">Especialista en Operaciones de Información e Inteligencia Estratégica</p>', t, flags=re.S)
CELLS = '''<div class="cell" style="left:96px;top:31px"><div class="ico"><img src="__I_OPE__" alt="" style="height:22.39px"></div>Operaciones de<br>Información</div>
    <div class="cell" style="left:292px;top:31px"><div class="ico"><img src="__I_EST__" alt="" style="height:22.94px"></div>Inteligencia<br>Estratégica</div>
    <div class="cell" style="left:96px;top:108.5px"><div class="ico"><img src="__I_COM__" alt="" style="height:22.15px"></div>Comunicación<br>Estratégica</div>
    <div class="cell" style="left:292px;top:108.5px"><div class="ico"><img src="__I_SEG__" alt="" style="height:22.15px"></div>Seguridad y<br>Defensa Nacional</div>
    '''
t, n = re.subn(r'<div class="cell" style="left:96px;top:31px">.*?(?=<div class="sep-m")', lambda m: CELLS, t, count=1, flags=re.S); assert n == 1
rep('data-w="Imagen · foto 391×390"><img src="__FOTO__" alt="Fernando Cocho Pérez">', 'data-w="Imagen · foto 412×389"><img src="__FOTO__" alt="Andrés Peñaranda">')

for w in ['FERNANDO', 'COCHO', 'Fernando', 'UNIR', 'CEDEGYS', '__I_MET__', '__I_CIB__', '313', 'pipe']:
    assert w not in t, w
open(p, 'w', encoding='utf-8').write(t)
print('ok', len(t))
