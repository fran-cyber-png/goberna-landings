"""Pasa la plantilla de Daniela Galvan (daniela-tpl.html) al contenido y medidas de Omar Chehade (Figma 437:2 / 447:2).
El contenido sale de omar-chehade-datos.json (literal del Figma, con word joiners U+2060 en las fechas)."""
import re, os, json
S = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(S)
D = json.load(open(os.path.join(P, 'omar-chehade-datos.json'), encoding='utf-8'))
p = os.path.join(S, 'omar-tpl.html')
t = open(os.path.join(P, '..', 'daniela-galvan', '_generador', 'daniela-tpl.html'), encoding='utf-8').read()
DG = json.load(open(os.path.join(P, '..', 'daniela-galvan', 'daniela-galvan-datos.json'), encoding='utf-8'))

def rep(a, b, n=1):
    global t
    c = t.count(a)
    assert c == n, (a[:60], c)
    t = t.replace(a, b)

rep('<title>Daniela Galvan</title>', '<title>Omar Chehade</title>')
rep('.foto-d{left:999px;top:101px;width:721px;height:749px}', '.foto-d{left:1059px;top:101px;width:661px;height:749px}')
rep('.foto-m{left:28px;top:542px;width:375px;height:389px}', '.foto-m{left:37px;top:542px;width:357px;height:390px}')
t = t.replace('ak-dg-', 'ak-oc-')
rep('<h1>Plantilla Daniela Galvan</h1>', '<h1>Plantilla Omar Chehade</h1>')
rep('(450:2, 452:2, 453:2)', '(437:2, 444:2, 447:2)')

rep('>DANIELA</p>', f">{D['nombre']['linea1']}</p>", 2)
rep('>GALVAN</p>', f">{D['nombre']['linea2']}</p>", 2)
rep('alt="Daniela Galvan"', 'alt="Omar Chehade"', 2)
rep('data-w="Imagen · foto 721×749"', 'data-w="Imagen · foto 661×749"')
rep('data-w="Imagen · foto 375×389"', 'data-w="Imagen · foto 357×390"')
rep(f'<p class="sub" data-w="Texto · Open Sans 28/48 · 1 línea">{DG["titular"]}</p>',
    f'<p class="sub" data-w="Texto · Open Sans 28/48 · 2 líneas">{D["titular"]}</p>')
rep(f'<p class="abs sub-m" data-w="Texto · Manrope 16/28 · 2 líneas">{DG["titular"]}</p>',
    f'<p class="abs sub-m" data-w="Texto · Manrope 16/28 · 3 líneas">{D["titular"]}</p>')

# especialidades: token viejo -> (token nuevo, etiqueta, alto desktop)
ESP = D['especialidades_html']
NEW = {'__I_INV__': ('__I_CON__', ESP[0], '37.93px'), '__I_DIG__': ('__I_PEN__', ESP[1], '37.82px'),
       '__I_PRE__': ('__I_LUC__', ESP[2], '36.52px'), '__I_OSI__': ('__I_GOB__', ESP[3], '36.92px')}
for ot, ol in zip(NEW, DG['especialidades_html']):
    nt, nl, hd = NEW[ot]
    t, n = re.subn(re.escape(f'<img src="{ot}" alt="" style="height:') + r'([\d.]+px)' + re.escape(f'"></div>{ol}</div>'),
                   lambda m: f'<img src="{nt}" alt="" style="height:{"23px" if m.group(1) == "23px" else hd}"></div>{nl}</div>', t)
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

for (ob, os_), (nb, ns) in zip(DG['cifras'], D['cifras']):
    rep(f'>{ob}</p>', f'>{nb}</p>', 2)
    rep(f'>{os_}</p>', f'>{ns}</p>', 2)

for w in ['Daniela', 'DANIELA', 'GALVAN', '__I_INV__', '__I_DIG__', '__I_PRE__', '__I_OSI__', 'Cibercrimen', 'ak-dg-']:
    assert w not in t, w
open(p, 'w', encoding='utf-8').write(t)
print('ok', len(t), 'word joiners:', t.count('⁠'))
