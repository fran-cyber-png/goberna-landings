# CD-WP2: tarjeta extra de docente (lo escribe CD-WP2)
# ============ Docentes: 7.ª tarjeta = copia de la 6.ª con ids nuevos (el usuario la edita a mano en WordPress)
import html as _html
DOC_CAR, DOC_SRC = '79feacd4', '334907ee'

def _newid8(used):
    while True:
        x = '%08x' % random.randrange(16 ** 8)
        if x not in ELEM and x not in used and x not in HTML and x not in CSS: return x

def _kids(s, a, b):
    """(inicio, fin) de cada <div> hijo directo dentro de s[a:b]."""
    out = []; d = 0; st = 0
    for t in re.finditer(r'<div\b[^>]*>|</div>', s[a:b]):
        if t.group(0) == '</div>':
            d -= 1
            if d == 0: out.append((a + st, a + t.end()))
        else:
            if d == 0: st = t.start()
            d += 1
    return out

def _copy_css_clean(mp):
    """Copia las reglas del CSS generado de los elementos de mp (una copia por regla, todos los ids a la vez)."""
    extra = []
    for media, sel, body in css_rules(re.sub(r'\x00CUSTOM:[0-9a-f]+\x00', '', CSS)):
        if not any(re.search(r'elementor-element-%s(?![0-9a-f])' % o, sel) for o in mp): continue
        r = sel
        for o, n in mp.items(): r = re.sub(r'elementor-element-%s(?![0-9a-f])' % o, 'elementor-element-' + n, r)
        r = r + '{' + body + '}'
        extra.append(media + '{' + r + '}' if media else r)
    EXTRA_CSS.insert(0, '\n'.join(extra))

# 1) JSON: copia profunda de la diapositiva 6 (ids nuevos) y un ítem más en carousel_items
_car = ELEM[DOC_CAR]; _mp = {}
def _reid_card(e):
    n = _newid8(set(_mp.values())); _mp[e['id']] = n; e['id'] = n
    for c in e.get('elements', []): _reid_card(c)
_cp = copy.deepcopy(ELEM[DOC_SRC]); _reid_card(_cp)
_car['elements'].insert([c['id'] for c in _car['elements']].index(DOC_SRC) + 1, _cp); index(_cp, _car)
_car['settings']['carousel_items'].append({'_id': _newid8(set(_mp.values())), 'slide_title': 'Docente 7'})
_copy_css_clean(_mp)

# 2) HTML (vista previa): 7 diapositivas reales, sin los duplicados de bucle que trae el DOM publicado
#    (el shim inicia Swiper con loop:false, así que los duplicados se verían como tarjetas extra)
def _doc_carousel(blk):
    def _ds(m):
        d = json.loads(_html.unescape(m.group(1)))
        d['carousel_items'] = S(DOC_CAR)['carousel_items']
        t = json.dumps(d, ensure_ascii=True, separators=(',', ':'))
        return 'data-settings="' + t.replace('&', '&amp;').replace('"', '&quot;') + '"'
    blk = re.sub(r'data-settings="([^"]*)"', _ds, blk, count=1)
    w0 = blk.index('<div class="swiper-wrapper"'); w1 = blk.index('>', w0) + 1
    d = 0
    for t in re.finditer(r'<div\b|</div>', blk[w0:]):
        d += 1 if t.group(0) == '<div' else -1
        if d == 0: wend = w0 + t.start(); break
    slides = [blk[a:b] for a, b in _kids(blk, w1, wend)]
    real = [x for x in slides if 'swiper-slide-duplicate' not in re.match(r'<div class="[^"]*"', x).group(0)]
    assert len(real) == 6 and len(slides) == 12, (len(real), len(slides))
    new = real[-1]
    for o, n in _mp.items():
        new = re.sub(r'elementor-element-%s(?![0-9a-f])' % o, 'elementor-element-' + n, new)
        new = new.replace('data-id="%s"' % o, 'data-id="%s"' % n)
    new = re.sub(r'data-slide="\d+"', 'data-slide="7"', new, count=1)
    new = re.sub(r'data-swiper-slide-index="\d+"', 'data-swiper-slide-index="6"', new, count=1)
    new = re.sub(r'aria-label="\d+ / \d+"', 'aria-label="7 / 7"', new, count=1)
    out = [re.sub(r'aria-label="(\d+) / 6"', r'aria-label="\1 / 7"', x, count=1) for x in real] + [new]
    # la vista previa parte de la diapositiva 1 (sin duplicados, la 2.ª queda a 434 px = 384 + 50)
    wopen = re.sub(r'translate3d\(-?\d+px', 'translate3d(-434px', blk[w0:w1])
    blk = blk[:w0] + wopen + '\n' + '\n'.join(out) + '\n' + blk[wend:]
    # puntos: uno más, con el mismo marcado que el 6.º
    m = re.search(r'<span class="swiper-pagination-bullet"[^>]*data-bullet-index="5"[^>]*></span>', blk)
    b7 = m.group(0).replace('data-bullet-index="5"', 'data-bullet-index="6"').replace('Ir a la diapositiva 6', 'Ir a la diapositiva 7')
    return blk[:m.end()] + b7 + blk[m.end():]
html_sub_in(DOC_CAR, _doc_carousel)
# el número de docentes no está en ningún otro ajuste; el comentario del CSS sí decía "3"
css_sub('613c44c5', '/* puntos: 3, uno por docente */', '/* puntos: uno por docente */')

# ============ FAQ (266b2296): apertura y cierre sin saltos (algoritmo del handler de Elementor 4.3)
# Causa: spec.py cambiaba el padding del título (28/28 -> 20/0) y el del contenido (0 -> 14/38) al poner [open],
# y el borde degradado y el fondo del ícono cambiaban de golpe. El handler de Elementor anima la altura con
# offsetHeight (sin márgenes ni transform): un margin-top negativo en el contenido deja el final 36 px más alto
# y salta al terminar. Por eso:
#  - el ítem no tiene borde (1 px que offsetHeight cuenta y el handler no): el trazo es una sombra interior;
#  - el título tiene el mismo padding en los dos estados; el texto se desplaza -8 px con transform;
#  - el contenido abierto tiene padding 0/16 y se sube -23 px con transform (la respuesta queda a 67 px, como antes).
# Así la altura final = summary + contenido, sin salto al terminar. Las posiciones finales no cambian.
FAQ = '266b2296'
_ease = 'cubic-bezier(.22,.61,.36,1)'
css_sub(FAQ, 'selector .e-n-accordion-item { background: #FFFFFF; border: 1px solid #A1B5D3; border-radius: 15px; overflow: hidden; transition: border-color .2s; }',
        'selector .e-n-accordion-item { background: #FFFFFF; border: 0; box-shadow: inset 0 0 0 1px #A1B5D3; border-radius: 15px; overflow: hidden; position: relative; transition: box-shadow .45s %s; }' % _ease)
css_sub(FAQ, 'selector .e-n-accordion-item[open] { border-color: transparent; background: linear-gradient(#FFFFFF, #FFFFFF) padding-box, linear-gradient(#DD0005, #DD0005) border-box; }',
        'selector .e-n-accordion-item[open] { box-shadow: inset 0 0 0 1px transparent; }')
# el título compensa el borde que se quitó (+1 px arriba y abajo en cada tamaño): mismas posiciones y misma altura
css_sub(FAQ, 'padding: 28px 25px 28px 64px !important;', 'padding: 29px 25px 29px 64px !important;')
css_sub(FAQ, 'padding: 24px 20px 24px 40px !important;', 'padding: 25px 20px 25px 40px !important;')
css_sub(FAQ, 'padding: 16px 14px 16px 18px !important;', 'padding: 17px 14px 17px 18px !important;')
css_sub(FAQ, 'border-radius: 50%; background: #F3F4F8;', 'border-radius: 50%%; background-color: #F3F4F8; transition: background-color .45s %s;' % _ease)
css_sub(FAQ, 'selector .e-n-accordion-item[open] .e-n-accordion-item-title-icon > span { background: linear-gradient(#DD0005, #DD0005); }',
        'selector .e-n-accordion-item[open] .e-n-accordion-item-title-icon > span { background-color: #DD0005; }')
css_sub(FAQ, 'selector .e-n-accordion-item[open] > .e-n-accordion-item-title { padding-top: 20px !important; padding-bottom: 0 !important; }',
        'selector .e-n-accordion-item[open] > .e-n-accordion-item-title { transform: translateY(-8px); }')
css_sub(FAQ, 'selector .e-n-accordion-item[open] > .e-con { animation: ak-acc-in .45s ease both; }',
        'selector .e-n-accordion-item[open] > .e-con { animation: ak-faq-in .4s %s both; }' % _ease)
# desktop: contenido abierto con padding 0/16 (no 14/38) y subido 23 px con transform
css_sub(FAQ, 'padding: 14px 64px 38px 64px !important;', 'padding: 0 64px 16px 64px !important;')
css_add(FAQ, '''/* transiciones del acordeón de preguntas (ver comentario arriba) */
selector .e-n-accordion-item::before { content: ""; position: absolute; inset: 0; border-radius: inherit; padding: 1px; background: #DD0005;
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite: xor;
  mask: linear-gradient(#000 0 0) content-box exclude, linear-gradient(#000 0 0); opacity: 0; pointer-events: none; transition: opacity .45s EASE; }
selector .e-n-accordion-item[open]::before { opacity: 1; }
selector .e-n-accordion-item > .e-n-accordion-item-title { transition: transform .45s EASE; }
selector .e-n-accordion-item > .e-con, selector .e-n-accordion-item > [role="region"] { position: relative; }
selector .e-n-accordion-item-title-icon i, selector .e-n-accordion-item-title-icon svg, selector .e-n-accordion-item-title-icon svg path { transition: color .45s EASE, fill .45s EASE; }
@keyframes ak-faq-in { from { opacity: 0; } to { opacity: 1; } }
@media (max-width: 1366px) {
  selector .e-n-accordion-item[open] > .e-con, selector .e-n-accordion-item[open] > [role="region"] { transform: translateY(-1px); }
}
@media (min-width: 1367px) {
  selector .e-n-accordion-item[open] > .e-con, selector .e-n-accordion-item[open] > [role="region"] { transform: translateY(-23px); }
}
@media (prefers-reduced-motion: reduce) {
  selector .e-n-accordion-item, selector .e-n-accordion-item::before, selector .e-n-accordion-item > .e-n-accordion-item-title,
  selector .e-n-accordion-item-title-icon > span, selector .e-n-accordion-item-title-icon i, selector .e-n-accordion-item-title-icon svg,
  selector .e-n-accordion-item-title-icon svg path { transition: none !important; }
}'''.replace('EASE', _ease))

# ============ Acordeón de módulos (5b410621): cierre sin salto (mismo criterio que el FAQ)
# Causa: [open] > summary tenía padding-bottom 2 px (desktop 30 px cerrado): al cerrar, el handler mide el summary
# abierto (140 px) y al terminar la caja vuelve a 169 px (salto de 29 px en 1920; 21 en 1366; 17 en 375).
# Además, el borde-bottom de 1 px cuenta en offsetHeight y el handler no lo suma.
# Solución: el summary mide lo mismo abierto y cerrado; el hueco de 28/20/16 px se quita del inicio del cuerpo
# con un margin-top negativo en su primer hijo (dentro de la altura del cuerpo, así que el handler lo cuenta bien);
# el borde pasa a sombra interior y el summary gana 1 px (y el cuerpo 1 px) para que la caja total no cambie.
M = '5b410621'
_ease = 'cubic-bezier(.22,.61,.36,1)'
def _sub1(old, new):
    cc = S(M).get('custom_css', '')
    assert cc.count(old) == 1, (cc.count(old), old[:80])
    css_sub(M, old, new)
_sub1('selector .e-n-accordion-item { counter-increment: mod; border-bottom: 1px solid #CCD0D4; padding: 0 !important; margin: 0 !important; }',
      'selector .e-n-accordion-item { counter-increment: mod; box-shadow: inset 0 -1px 0 #CCD0D4; padding: 0 !important; margin: 0 !important; }')
_sub1('align-items: start; padding: 30px 0 30px 0 !important;', 'align-items: start; padding: 30px 0 31px 0 !important;')
_sub1('column-gap: 14px; padding: 22px 0 !important;', 'column-gap: 14px; padding: 22px 0 23px !important;')
_sub1('column-gap: 12px; padding: 18px 0 !important;', 'column-gap: 12px; padding: 18px 0 19px !important;')
_sub1('selector .e-n-accordion-item[open] > .e-n-accordion-item-title { padding-bottom: 2px !important; }',
      '/* (sin padding-bottom distinto en [open]: el título mide lo mismo abierto y cerrado) */')
_sub1('selector .ak-mod-body { padding-left: 120px !important; padding-bottom: 18px !important; }', 'selector .ak-mod-body { padding-left: 120px !important; padding-bottom: 19px !important; }')
_sub1('selector .ak-mod-body { padding-left: 86px !important; padding-bottom: 24px !important; }', 'selector .ak-mod-body { padding-left: 86px !important; padding-bottom: 25px !important; }')
_sub1('selector .ak-mod-body { padding-left: 0 !important; padding-bottom: 20px !important; }', 'selector .ak-mod-body { padding-left: 0 !important; padding-bottom: 21px !important; }')
# animación: solo fundido del contenido (keyframes propios; el del FAQ ya es ak-faq-in)
_sub1('selector .e-n-accordion-item[open] > .e-con { animation: ak-acc-in .45s ease both; }',
      'selector .e-n-accordion-item[open] > .e-con { animation: ak-mod-in .4s %s both; }' % _ease)
_sub1('@keyframes ak-acc-in { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: none; } }',
      '@keyframes ak-mod-in { from { opacity: 0; } to { opacity: 1; } }')
# "Ver contenido / Ocultar" y el +/−: los dos textos se cruzan con opacidad (antes cambiaban con display)
_sub1('selector .e-n-accordion-item:not([open]) .e-n-accordion-item-title-icon .e-opened,\r\nselector .e-n-accordion-item[open] .e-n-accordion-item-title-icon .e-closed { display: none !important; }', '')
_sub1('selector .e-n-accordion-item[open] .e-n-accordion-item-title-icon .e-opened,\r\nselector .e-n-accordion-item:not([open]) .e-n-accordion-item-title-icon .e-closed { display: inline-flex !important; }', '')
_sub1('selector .e-n-accordion-item:not([open]) .e-n-accordion-item-title-icon .e-opened,\nselector .e-n-accordion-item[open] .e-n-accordion-item-title-icon .e-closed { display: inline-flex !important; visibility: hidden; }', '')
css_add(M, '\n'.join([
    '/* cierre sin salto y transiciones (ver comentario arriba) */',
    'selector .ak-mod-body > :first-child { margin-top: -29px !important; }',
    '@media (max-width: 1366px) { selector .ak-mod-body > :first-child { margin-top: -21px !important; } }',
    '@media (max-width: 767px) { selector .ak-mod-body > :first-child { margin-top: -17px !important; } }',
    'selector .e-n-accordion-item-title-icon > span { display: inline-flex !important; grid-area: 1 / 1; opacity: 0; visibility: hidden; transition: opacity .45s %(e)s, visibility .45s %(e)s, color .45s %(e)s; }',
    'selector .e-n-accordion-item:not([open]) .e-n-accordion-item-title-icon .e-closed, selector .e-n-accordion-item[open] .e-n-accordion-item-title-icon .e-opened { opacity: 1; visibility: visible; }',
    '@media (prefers-reduced-motion: reduce) { selector .e-n-accordion-item-title-icon > span { transition: none !important; } }',
]).replace('%(e)s', _ease))
