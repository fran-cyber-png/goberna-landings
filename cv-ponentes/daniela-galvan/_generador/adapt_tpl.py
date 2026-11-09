"""Pasa la plantilla de Andrés Peñaranda (andres-tpl.html) al contenido y medidas de Daniela Galvan (Figma 450:2 / 453:2).
El contenido sale de daniela-galvan-datos.json (texto literal del Figma, con las erratas que el usuario decidió conservar)."""
import re, os, json
S = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(S)
D = json.load(open(os.path.join(P, 'daniela-galvan-datos.json'), encoding='utf-8'))
p = os.path.join(S, 'daniela-tpl.html')
t = open(os.path.join(P, '..', 'andres-penaranda', '_generador', 'andres-tpl.html'), encoding='utf-8').read()

def rep(a, b, n=1):
    global t
    c = t.count(a)
    assert c == n, (a[:60], c)
    t = t.replace(a, b)

rep('<title>Andrés Peñaranda</title>', '<title>Daniela Galvan</title>')
rep('.name-d .n2{font:800 87px/.964 var(--display);color:#fff;letter-spacing:3.48px}', '.name-d .n2{font:800 87px/.964 var(--display);color:#fff;letter-spacing:2.56px}')
rep('.foto-d{left:928px;top:101px;width:792px;height:749px}', '.foto-d{left:999px;top:101px;width:721px;height:749px}')
rep('.name-m .n2{font:800 42px/.964 var(--display);color:#fff;letter-spacing:1.68px}', '.name-m .n2{font:800 42px/.964 var(--display);color:#fff;letter-spacing:1.2359px}')
rep('.foto-m{left:9px;top:542px;width:412px;height:389px}', '.foto-m{left:28px;top:542px;width:375px;height:389px}')
t = t.replace('ak-ap-', 'ak-dg-')
rep('<h1>Plantilla Andrés Peñaranda</h1>', '<h1>Plantilla Daniela Galvan</h1>')
rep('(501:2, 506:141, 509:168)', '(450:2, 452:2, 453:2)')

N1, N2 = D['nombre']['linea1'], D['nombre']['linea2']
rep('>ANDRÉS</p>', f'>{N1}</p>', 2)
rep('>PEÑARANDA</p>', f'>{N2}</p>', 2)
rep('alt="Andrés Peñaranda"', 'alt="Daniela Galvan"', 2)
rep('data-w="Imagen · foto 792×749"', 'data-w="Imagen · foto 721×749"')
rep('data-w="Imagen · foto 412×389"', 'data-w="Imagen · foto 375×389"')
TIT = D['titular']
rep('<p class="sub" data-w="Texto · Open Sans 28/48 · 2 líneas">Especialista en Operaciones de Información e Inteligencia Estratégica</p>',
    f'<p class="sub" data-w="Texto · Open Sans 28/48 · 1 línea">{TIT}</p>')
rep('<p class="abs sub-m" data-w="Texto · Manrope 16/28 · 2 líneas">Especialista en Operaciones de Información e Inteligencia Estratégica</p>',
    f'<p class="abs sub-m" data-w="Texto · Manrope 16/28 · 2 líneas">{TIT}</p>')

# especialidades: (token, etiqueta, alto desktop, alto móvil)
ESP = D['especialidades_html']
OLD = [('__I_OPE__', 'Operaciones de<br>Información'), ('__I_EST__', 'Inteligencia<br>Estratégica'),
       ('__I_COM__', 'Comunicación<br>Estratégica'), ('__I_SEG__', 'Seguridad y<br>Defensa Nacional')]
NEW = [('__I_INV__', ESP[0], '36.52px', '23px'), ('__I_DIG__', ESP[1], '37.82px', '23px'),
       ('__I_PRE__', ESP[2], '36.52px', '23px'), ('__I_OSI__', ESP[3], '36.92px', '23px')]
for (ot, ol), (nt, nl, hd, hm) in zip(OLD, NEW):
    t, n = re.subn(re.escape(f'<img src="{ot}" alt="" style="height:') + r'[\d.]+px' + re.escape(f'"></div>{ol}</div>'),
                   lambda m, nt=nt, nl=nl, hd=hd, hm=hm: f'<img src="{nt}" alt="" style="height:{hd if "esp-ico" in t[max(0, m.start()-60):m.start()] else hm}"></div>{nl}</div>', t)
    assert n == 2, (ot, n)

RES = f"<b>{D['resumen']['negrita']}</b>{D['resumen']['resto']}"
t = re.sub(r'(<p class="res-d"[^>]*>).*?</p>', lambda m: m.group(1) + RES + '</p>', t, flags=re.S)
t = re.sub(r'(<p class="res-m"[^>]*>).*?</p>', lambda m: m.group(1) + RES + '</p>', t, flags=re.S)

def lis(items, cls, src, ind):
    return ''.join(f'\n{ind}<li><img class="{cls}" src="{src}" alt=""><span>{h}</span></li>' for h in items)
uls = list(re.finditer(r'(<ul class="list-[dm][^"]*"[^>]*>)(.*?)(\n\s*</ul>)', t, flags=re.S))
assert len(uls) == 6
CAR, FOR, APO = D['cargos'], D['formacion'], D['aportes']
specs = [(CAR, 'dot', '__V_DOT__', '        ', f'{len(CAR)} ítems'), (FOR, 'dot', '__V_DOT__', '        ', f'{len(FOR)} ítems'), (APO, 'arr', '__V_ARR__', '        ', f'{len(APO)} ítems'),
         (CAR, 'dot', '__V_DOT_M__', '      ', None), (FOR, 'dot', '__V_DOT_M__', '      ', f'{len(FOR)} ítems'), (APO, 'arr', '__V_ARR_M__', '      ', None)]
out = []; last = 0
for m, (it, cls, src, ind, n) in zip(uls, specs):
    head = m.group(1)
    if n:
        head = re.sub(r'\d+ ítems', n, head)
    out.append(t[last:m.start()] + head + lis(it, cls, src, ind) + m.group(3)); last = m.end()
out.append(t[last:]); t = ''.join(out)

(b1, s1), (b2, s2), (b3, s3) = D['cifras']
for old, new in [('+25 años', b1), ('Seguridad y defensa nacional', s1), ('Magíster', b2), ('Administración, Gobierno y Políticas Públicas', s2),
                 ('Consultor', b3), ('Internacional en Inteligencia Estratégica', s3)]:
    rep(f'>{old}</p>', f'>{new}</p>', 2)

for w in ['Andrés', 'ANDRÉS', 'PEÑARANDA', 'Peñaranda', '__I_OPE__', '__I_COM__', '__I_EST__', '__I_SEG__', 'Magíster', 'ak-ap-']:
    assert w not in t, w
open(p, 'w', encoding='utf-8').write(t)
print('ok', len(t))
