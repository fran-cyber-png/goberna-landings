"""Pasa la plantilla de Omar Chehade (omar-tpl.html) al contenido y medidas de Gonzalo Catanzariti (Figma 532:2 / 538:2).
El contenido sale de gonzalo-catanzariti-datos.json (literal del Figma, con word joiners U+2060 en 2019–2026)."""
import re, os, json
S = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(S)
D = json.load(open(os.path.join(P, 'gonzalo-catanzariti-datos.json'), encoding='utf-8'))
p = os.path.join(S, 'gonzalo-tpl.html')
t = open(os.path.join(P, '..', 'omar-chehade', '_generador', 'omar-tpl.html'), encoding='utf-8').read()
OC = json.load(open(os.path.join(P, '..', 'omar-chehade', 'omar-chehade-datos.json'), encoding='utf-8'))

def rep(a, b, n=1):
    global t
    c = t.count(a)
    assert c == n, (a[:60], c)
    t = t.replace(a, b)

rep('<title>Omar Chehade</title>', '<title>Gonzalo Catanzariti</title>')
# foto volteada en Figma: en pantalla ocupa 1026–1720 (desktop) y 35–395 (móvil); el webp ya va volteado
rep('.foto-d{left:1059px;top:101px;width:661px;height:749px}', '.foto-d{left:1026px;top:101px;width:694px;height:749px}')
rep('.foto-m{left:37px;top:542px;width:357px;height:390px}', '.foto-m{left:35px;top:542px;width:360px;height:389px}')
# CATANZARITI lleva el tracking de 87 px con 3.48 (desktop) y 1.68 (móvil), como en Figma
rep('.name-d .n2{font:800 87px/.964 var(--display);color:#fff;letter-spacing:2.56px}', '.name-d .n2{font:800 87px/.964 var(--display);color:#fff;letter-spacing:3.48px}')
rep('.name-m .n2{font:800 42px/.964 var(--display);color:#fff;letter-spacing:1.2359px}', '.name-m .n2{font:800 42px/.964 var(--display);color:#fff;letter-spacing:1.68px}')
t = t.replace('ak-oc-', 'ak-gc-')
rep('<h1>Plantilla Omar Chehade</h1>', '<h1>Plantilla Gonzalo Catanzariti</h1>')
rep('(437:2, 444:2, 447:2)', '(532:2, 535:2, 538:2)')

rep('>OMAR</p>', f">{D['nombre']['linea1']}</p>", 2)
rep('>CHEHADE</p>', f">{D['nombre']['linea2']}</p>", 2)
rep('alt="Omar Chehade"', 'alt="Gonzalo Catanzariti"', 2)
rep('data-w="Imagen · foto 661×749"', 'data-w="Imagen · foto 694×749"')
rep('data-w="Imagen · foto 357×390"', 'data-w="Imagen · foto 360×389"')
rep(f'<p class="sub" data-w="Texto · Open Sans 28/48 · 2 líneas">{OC["titular"]}</p>',
    f'<p class="sub" data-w="Texto · Open Sans 28/48 · 2 líneas">{D["titular"]}</p>')
rep(f'<p class="abs sub-m" data-w="Texto · Manrope 16/28 · 3 líneas">{OC["titular"]}</p>',
    f'<p class="abs sub-m" data-w="Texto · Manrope 16/28 · 2 líneas">{D["titular"]}</p>')

# especialidades: token viejo -> (token nuevo, etiqueta, alto desktop, alto móvil)
ESP = D['especialidades_html']
NEW = {'__I_CON__': ('__I_ARQ__', ESP[0], '36.52px', '22.15px'), '__I_PEN__': ('__I_INV__', ESP[1], '36.52px', '22.15px'),
       '__I_LUC__': ('__I_FOR__', ESP[2], '36.92px', '22.39px'), '__I_GOB__': ('__I_OSI__', ESP[3], '37.82px', '22.94px')}
for ot, ol in zip(NEW, OC['especialidades_html']):
    nt, nl, hd, hm = NEW[ot]
    t, n = re.subn(re.escape(f'<img src="{ot}" alt="" style="height:') + r'([\d.]+px)' + re.escape(f'"></div>{ol}</div>'),
                   lambda m: f'<img src="{nt}" alt="" style="height:{hm if m.group(1) == "23px" else hd}"></div>{nl}</div>', t)
    assert n == 2, (ot, n)

RES = f"<b>{D['resumen']['negrita']}</b>{D['resumen']['resto']}"
t = re.sub(r'(<p class="res-d"[^>]*>).*?</p>', lambda m: m.group(1) + RES + '</p>', t, flags=re.S)
t = re.sub(r'(<p class="res-m"[^>]*>).*?</p>', lambda m: m.group(1) + RES + '</p>', t, flags=re.S)
rep('negrita en la 1.ª frase', 'negrita en la 1.ª oración')

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

for (ob, os_), (nb, ns) in zip(OC['cifras'], D['cifras']):
    rep(f'>{ob}</p>', f'>{nb}</p>', 2)
    rep(f'>{os_}</p>', f'>{ns}</p>', 2)

for w in ['Omar', 'OMAR', 'CHEHADE', 'Chehade', '__I_CON__', '__I_PEN__', '__I_LUC__', '__I_GOB__', 'Fujimori', 'ak-oc-']:
    assert w not in t, w
open(p, 'w', encoding='utf-8').write(t)
print('ok', len(t), 'word joiners:', t.count('⁠'))
