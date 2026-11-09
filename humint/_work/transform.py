# HUMINT: base = la landing final de Carrera Diplomática (carrera-diplomatica.json, indicada por el usuario el 27 oct).
# Etapa 1: spec_carrera.py rehace Carrera sobre Director (sale idéntico a carrera-diplomatica.json; se comprueba).
# Etapa 2: humint.py aplica el Figma TZaBinYmWvX5sD7aBTR9Hp (frame 28:592) y el PDF «CONTENIDO LANDINGS (8)».
# Cada cambio se aplica a la vez al JSON de Elementor y a la vista previa (HTML/CSS renderizado de la base).
import json, re, os, copy, random, sys
random.seed(93575)  # ids nuevos reproducibles entre corridas
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(W, '..')
HUMINT_ROOT = ROOT
BASE_ROOT = os.path.join(W, '..', '_base-carrera')  # iconos e imágenes de Carrera (los usa la etapa 1)
P = os.path.join(ROOT, '_preview')
sys.path.insert(0, W)
import page

J = json.load(open(os.path.join(W, 'base.json'), encoding='utf-8'))
HTML = open(os.path.join(W, 'base.html'), encoding='utf-8').read()
CSS_ALL = open(os.path.join(W, 'base.css'), encoding='utf-8').read()
a = CSS_ALL.find('/* post-93575.css */'); b = CSS_ALL.find('/* sticky.min.css */')
CSS_PRE, CSS, CSS_POST = CSS_ALL[:a], CSS_ALL[a:b], CSS_ALL[b:]
# El CSS personalizado de cada elemento sale del JSON: se marca su sitio y se regenera al final
CUSTOM_RE = r'/\* Start custom CSS for [\w-]+, class: \.elementor-element-([0-9a-f]+) \*/.*?/\* End custom CSS \*/'
CSS = re.sub(CUSTOM_RE, lambda m: '\x00CUSTOM:' + m.group(1) + '\x00', CSS, flags=re.S)
EXTRA_CSS = []          # reglas que en Elementor salen de los ajustes (van antes del CSS personalizado)
EXTRA_CUSTOM = []       # CSS personalizado nuevo (va al final)
LOG = []

RED, DARK = '#DD0005', '#0C0000'
WP = 'https://grupogoberna.com/wp-content/uploads/2026/10/'
# imagen nueva -> (url en WordPress, id). Se completa cuando el usuario las suba.
UPLOADS = json.load(open(os.path.join(W, 'uploads.json'), encoding='utf-8')) if os.path.exists(os.path.join(W, 'uploads.json')) else {}
# imágenes que ya están en la Biblioteca de medios del sitio (se reutilizan, no hay que subirlas)
REUSE = {}
_OLD_REUSE = {
    'testimonio-thumb-alina.webp': 'https://grupogoberna.com/wp-content/uploads/2026/09/testimonio-thumb-alina.webp',
    'testimonio-thumb-lorena.webp': 'https://grupogoberna.com/wp-content/uploads/2026/09/testimonio-thumb-lorena.webp',
    'testimonio-thumb-miguel.webp': 'https://grupogoberna.com/wp-content/uploads/2026/09/testimonio-thumb-miguel.webp',
    'bandera-colombia.png': 'https://grupogoberna.com/wp-content/uploads/2026/09/bandera-colombia.png',
    'bandera-bolivia.png': 'https://grupogoberna.com/wp-content/uploads/2026/09/bandera-bolivia.png',
    'bandera-mexico-circulo.png': 'https://grupogoberna.com/wp-content/uploads/2026/09/bandera-mexico-circulo.png',
    'experiencia-goberna-promo.webp': 'https://grupogoberna.com/wp-content/uploads/2026/09/testimonios-consultor-promo.webp',
    'card-eduardo-velandia-sitio.webp': 'https://grupogoberna.com/wp-content/uploads/2026/10/card-eduardo-velandia.webp',
}
def wp(name):
    if name in REUSE: return (REUSE[name], '')
    u = UPLOADS.get(name)
    return (u['url'], u['id']) if u else (WP + name, '')

# ---------------------------------------------------------------- índice del JSON
ELEM, PARENT = {}, {}
def index(e, parent=None):
    ELEM[e['id']] = e; PARENT[e['id']] = parent
    for c in e.get('elements', []): index(c, e)
for n in J['content']: index(n)
def S(i): return ELEM[i]['settings']
def pre(i): return '.elementor-93575 .elementor-element.elementor-element-' + i

# ---------------------------------------------------------------- utilidades HTML
def el_span(h, i):
    """(inicio, fin) del bloque <div ... data-id="i"> balanceado."""
    m = re.search(r'<div[^>]*\bdata-id="%s"' % re.escape(i), h)
    if not m: raise KeyError('no está en el HTML: ' + i)
    s = m.start(); depth = 0
    for t in re.finditer(r'<div\b|</div>', h[s:]):
        depth += 1 if t.group(0) == '<div' else -1
        if depth == 0: return s, s + t.end()
    raise ValueError(i)
def html_sub_in(i, fn):
    global HTML
    s, e = el_span(HTML, i)
    HTML = HTML[:s] + fn(HTML[s:e]) + HTML[e:]

# ---------------------------------------------------------------- operaciones
def heading(i, html):
    S(i)['title'] = html
    def f(blk):
        r, n = re.subn(r'(<(h[1-6]|p|div|span)\s+class="elementor-heading-title[^"]*">)(.*?)(</\2>)',
                       lambda m: m.group(1) + html + m.group(4), blk, count=1, flags=re.S)
        assert n, i; return r
    html_sub_in(i, f)

def text(i, html):
    S(i)['editor'] = html
    def f(blk):
        r, n = re.subn(r'(<div class="elementor-widget-container">)(.*?)(</div>)',
                       lambda m: m.group(1) + html + m.group(3), blk, count=1, flags=re.S)
        assert n, i; return r
    html_sub_in(i, f)

def button(i, txt, url=None):
    S(i)['text'] = txt
    if url is not None: S(i)['link'] = dict(S(i).get('link') or {}, url=url)
    def f(blk):
        r, n = re.subn(r'(<span class="elementor-button-text">)(.*?)(</span>)', lambda m: m.group(1) + txt + m.group(3), blk, count=1, flags=re.S)
        assert n, i
        if url is not None: r = re.sub(r'(<a class="elementor-button[^"]*" href=")[^"]*', lambda m: m.group(1) + url, r, count=1)
        return r
    html_sub_in(i, f)

def image(i, name, key='image'):
    url, iid = wp(name)
    S(i)[key] = {'url': url, 'id': iid, 'size': '', 'alt': '', 'source': 'library'}
    html_sub_in(i, lambda blk: re.sub(r'(<img\b[^>]*?\ssrc=")[^"]*', lambda m: m.group(1) + 'a/' + name, blk, count=1))

def bg_image(i, name, old_local=None, key='background_image'):
    """Fondo de contenedor: JSON + regla del CSS generado."""
    url, iid = wp(name)
    S(i)[key] = {'url': url, 'id': iid, 'size': '', 'alt': '', 'source': 'library'}
    if old_local: css_global(old_local, 'a/' + name)

def no_bg_image(i):
    for k in ('background_image', 'background_image_mobile'):
        if k in S(i): S(i)[k] = {'url': '', 'id': '', 'size': ''}
    EXTRA_CSS.append(pre(i) + ':not(.elementor-motion-effects-element-type-background){background-image:none!important}')

def icon_svg(i, fname):
    url, iid = wp(fname)
    S(i)['selected_icon'] = {'value': {'url': url, 'id': iid}, 'library': 'svg'}
    svg = open(os.path.join(ROOT, 'iconos', fname), encoding='utf-8').read()
    svg = re.sub(r'<\?xml[^>]*>\s*', '', svg)
    def f(blk):
        r, n = re.subn(r'<svg\b.*?</svg>', lambda m: svg, blk, count=1, flags=re.S)
        assert n, i; return r
    html_sub_in(i, f)

def setv(i, **kw):
    S(i).update(kw)

def color(i, c, key=None):
    """Color de texto de un heading / text-editor / botón."""
    w = ELEM[i].get('widgetType')
    if w == 'heading':
        S(i)['title_color'] = c; EXTRA_CSS.append(f'{pre(i)} .elementor-heading-title{{color:{c}}}')
    elif w == 'text-editor':
        S(i)['text_color'] = c; EXTRA_CSS.append(f'{pre(i)}{{color:{c}}} {pre(i)} p{{color:{c}}}')
    elif w == 'button':
        S(i)['button_text_color'] = c; EXTRA_CSS.append(f'{pre(i)} .elementor-button{{color:{c};fill:{c}}}')
    elif w == 'icon':
        S(i)['primary_color'] = c
        EXTRA_CSS.append(f'{pre(i)}.elementor-view-framed .elementor-icon, {pre(i)}.elementor-view-default .elementor-icon{{color:{c};border-color:{c}}} '
                         f'{pre(i)}.elementor-view-framed .elementor-icon svg, {pre(i)}.elementor-view-default .elementor-icon svg{{fill:{c}}} '
                         f'{pre(i)}.elementor-view-stacked .elementor-icon{{background-color:{c}}}')

DEV = {'': None, '_laptop': '(max-width:1366px)', '_tablet': '(max-width:1024px)', '_mobile': '(max-width:932px)'}
def typo(i, **kw):
    """kw: family, weight, transform, size, lh, lh_unit, ls (+ sufijos _laptop/_tablet/_mobile)."""
    s = S(i); w = ELEM[i].get('widgetType')
    sel = {'heading': ' .elementor-heading-title', 'text-editor': '', 'button': ' .elementor-button'}[w]
    s['typography_typography'] = 'custom'
    rules = {d: [] for d in DEV}
    for k, v in kw.items():
        base, dev = k, ''
        for d in ('_laptop', '_tablet', '_mobile'):
            if k.endswith(d): base, dev = k[:-len(d)], d
        if base == 'family':
            s['typography_font_family' + dev] = v; rules[dev].append(f'font-family:"{v}", Sans-serif')
        elif base == 'weight':
            s['typography_font_weight' + dev] = str(v); rules[dev].append(f'font-weight:{v}')
        elif base == 'transform':
            s['typography_text_transform' + dev] = v; rules[dev].append(f'text-transform:{v}')
        elif base == 'size':
            s['typography_font_size' + dev] = {'unit': 'px', 'size': v, 'sizes': []}; rules[dev].append(f'font-size:{v}px')
        elif base == 'lh':
            unit = kw.get('lh_unit', 'px')
            s['typography_line_height' + dev] = {'unit': unit, 'size': v, 'sizes': []}; rules[dev].append(f'line-height:{v}{unit}')
        elif base == 'ls':
            s['typography_letter_spacing' + dev] = {'unit': 'px', 'size': v, 'sizes': []}; rules[dev].append(f'letter-spacing:{v}px')
    for d, r in rules.items():
        if not r: continue
        rule = f'{pre(i)}{sel}{{{";".join(r)}}}'
        EXTRA_CSS.append(f'@media{DEV[d]}{{{rule}}}' if DEV[d] else rule)

def css_sub(i, old, new, count=1):
    """Cambia un trozo del CSS personalizado del elemento i (la vista previa se regenera desde el JSON)."""
    s = S(i); cc = s.get('custom_css', '')
    assert old in cc, (i, old)
    s['custom_css'] = cc.replace(old, new, count)

def css_add(i, rules):
    s = S(i); s['custom_css'] = s.get('custom_css', '').rstrip() + '\n' + rules.strip() + '\n'

def css_global(old, new):
    global CSS
    CSS = CSS.replace(old, new)

def html_global(old, new):
    global HTML
    HTML = HTML.replace(old, new)

def remove(i):
    global HTML
    p = PARENT[i]; p['elements'] = [c for c in p['elements'] if c['id'] != i]
    s, e = el_span(HTML, i); HTML = HTML[:s] + HTML[e:]

def css_rules(css):
    """(media, selector, cuerpo) de cada regla; un nivel de @media."""
    out = []; i = 0; n = len(css)
    def block(j):
        d = 0
        for k in range(j, n):
            if css[k] == '{': d += 1
            elif css[k] == '}':
                d -= 1
                if d == 0: return k
        return n - 1
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        head = css[i:j]
        head = re.sub(r'/\*.*?\*/', '', head, flags=re.S).strip()
        k = block(j)
        if head.startswith('@media'):
            inner = css[j+1:k]; t = 0
            while True:
                a2 = inner.find('{', t)
                if a2 < 0: break
                b2 = inner.find('}', a2)
                sel = re.sub(r'/\*.*?\*/', '', inner[t:a2], flags=re.S).strip()
                out.append((head, sel, inner[a2+1:b2])); t = b2 + 1
        elif not head.startswith('@'):
            out.append(('', head, css[j+1:k]))
        i = k + 1
    return out

def newid():
    while True:
        x = '%07x' % random.randrange(16**7)
        if x not in ELEM: return x

def duplicate_after(i):
    """Duplica el elemento i (con ids nuevos) justo después. Devuelve {id viejo: id nuevo}."""
    global HTML
    p = PARENT[i]; src = ELEM[i]; cp = copy.deepcopy(src); mp = {}
    def reid(e):
        n = newid(); mp[e['id']] = n; e['id'] = n
        for c in e.get('elements', []): reid(c)
    reid(cp)
    k = [c['id'] for c in p['elements']].index(i); p['elements'].insert(k + 1, cp)
    index(cp, p)
    s, e = el_span(HTML, i); blk = HTML[s:e]
    for o, n in mp.items():
        blk = blk.replace(f'elementor-element-{o} ', f'elementor-element-{n} ').replace(f'elementor-element-{o}"', f'elementor-element-{n}"').replace(f'data-id="{o}"', f'data-id="{n}"')
    HTML = HTML[:e] + blk + HTML[e:]
    # reglas del CSS generado del original -> copia (respetando los @media)
    extra = []
    for media, sel, body in css_rules(CSS):
        for o, n in mp.items():
            if re.search(r'elementor-element-%s(?![0-9a-f])' % o, sel):
                r = sel.replace('elementor-element-' + o, 'elementor-element-' + n) + '{' + body + '}'
                extra.append(media + '{' + r + '}' if media else r)
    EXTRA_CSS.insert(0, '\n'.join(extra))
    return mp

def move_after(i, ref):
    """Mueve el elemento i justo después de ref (puede cambiar de contenedor)."""
    global HTML
    p = PARENT[i]; e = ELEM[i]; q = PARENT[ref]
    p['elements'] = [c for c in p['elements'] if c['id'] != i]
    k = [c['id'] for c in q['elements']].index(ref); q['elements'].insert(k + 1, e); PARENT[i] = q
    s0, e0 = el_span(HTML, i); blk = HTML[s0:e0]; HTML = HTML[:s0] + HTML[e0:]
    s1, e1 = el_span(HTML, ref); HTML = HTML[:e1] + blk + HTML[e1:]

def set_classes(i, cls):
    """Clases CSS del widget (JSON y HTML)."""
    global HTML
    key = 'css_classes' if ELEM[i]['elType'] == 'container' else '_css_classes'
    old = S(i).get(key, ''); S(i)[key] = cls
    s0, e0 = el_span(HTML, i); blk = HTML[s0:e0]
    head = blk[:blk.index('>')]
    new = head.replace(f'elementor-element-{i} {old} ', f'elementor-element-{i} {cls} ' if cls else f'elementor-element-{i} ') if old else head.replace(f'elementor-element-{i} ', f'elementor-element-{i} {cls} ')
    HTML = HTML[:s0] + new + blk[len(head):] + HTML[e0:]

def img_width(i, **kw):
    for k, v in kw.items():
        dev = k[len('w'):]
        S(i)['width' + dev] = {'unit': 'px', 'size': v, 'sizes': []}
        rule = f'{pre(i)} img{{width:{v}px}}'
        EXTRA_CSS.append(f'@media{DEV[dev]}{{{rule}}}' if DEV[dev] else rule)

def margin(i, dev='', **kw):
    """Margen de widget (_margin) o contenedor (margin)."""
    key = ('margin' if ELEM[i]['elType'] == 'container' else '_margin') + dev
    m = dict(S(i).get(key) or {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': False})
    for k, v in kw.items(): m[k] = str(v)
    m['isLinked'] = False; S(i)[key] = m
    if ELEM[i]['elType'] == 'container':
        rule = pre(i) + '{' + ';'.join(f"--margin-{k}:{m[k]}px" for k in ('top', 'right', 'bottom', 'left')) + '}'
    else:
        rule = f"{pre(i)} > .elementor-widget-container{{margin:{m['top']}px {m['right']}px {m['bottom']}px {m['left']}px}}"
    EXTRA_CSS.append(f'@media{DEV[dev]}{{{rule}}}' if DEV[dev] else rule)

def pad(i, dev='', **kw):
    key = 'padding' + dev
    m = dict(S(i).get(key) or {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': False})
    for k, v in kw.items(): m[k] = str(v)
    m['isLinked'] = False; S(i)[key] = m
    rule = pre(i) + '{' + ';'.join(f'--padding-{k}:{m[k]}px' for k in ('top', 'right', 'bottom', 'left')) + '}'
    EXTRA_CSS.append(f'@media{DEV[dev]}{{{rule}}}' if DEV[dev] else rule)

def width_pct(i, **kw):
    for k, v in kw.items():
        dev = k[len('w'):]
        S(i)['width' + dev] = {'unit': '%', 'size': v, 'sizes': []}
        rule = f'{pre(i)}{{--width:{v}%}}'
        EXTRA_CSS.append(f'@media{DEV[dev]}{{{rule}}}' if DEV[dev] else '@media(min-width:933px){' + rule + '}')

def copy_css_rules(mp):
    extra = []
    for media, sel, body in css_rules(CSS):
        for o, n in mp.items():
            if re.search(r'elementor-element-%s(?![0-9a-f])' % o, sel):
                r = sel.replace('elementor-element-' + o, 'elementor-element-' + n) + '{' + body + '}'
                extra.append(media + '{' + r + '}' if media else r)
    EXTRA_CSS.insert(0, '\n'.join(extra))

def acc_add_item(acc_id, src_body, title):
    """Agrega un ítem al acordeón anidado copiando el ítem cuyo contenido es src_body. Devuelve {id viejo: id nuevo}."""
    global HTML
    acc = ELEM[acc_id]; cp = copy.deepcopy(ELEM[src_body]); mp = {}
    def reid(e):
        n = newid(); mp[e['id']] = n; e['id'] = n
        for c in e.get('elements', []): reid(c)
    reid(cp)
    acc['elements'].append(cp); index(cp, acc)
    acc['settings']['items'].append({'_id': newid(), 'item_title': title})
    n_items = len(acc['settings']['items'])
    def f(blk):
        ds = list(re.finditer(r'<details\b.*?</details>', blk, flags=re.S))
        src = [m for m in ds if 'data-id="%s"' % src_body in m.group(0)][0].group(0)
        new = src
        for o, n in mp.items():
            new = (new.replace(f'elementor-element-{o} ', f'elementor-element-{n} ').replace(f'elementor-element-{o}"', f'elementor-element-{n}"')
                      .replace(f'data-id="{o}"', f'data-id="{n}"'))
        old_num = re.search(r'id="e-n-accordion-item-(\d+)"', new).group(1)
        new = new.replace('e-n-accordion-item-' + old_num, 'e-n-accordion-item-%d' % (90000 + n_items))
        new = re.sub(r'data-accordion-index="\d+"', 'data-accordion-index="%d"' % n_items, new)
        new = re.sub(r'(<details\b[^>]*?)\s+open(\s*>)', r'\1\2', new, count=1)
        new = re.sub(r'(<div class="e-n-accordion-item-title-text">)(.*?)(</div>)', lambda m: m.group(1) + ' ' + title + ' ' + m.group(3), new, count=1, flags=re.S)
        last = ds[-1]
        return blk[:last.end()] + '\n' + new + blk[last.end():]
    html_sub_in(acc_id, f)
    copy_css_rules(mp)
    return mp

def carousel_rebuild(car_id, n, titles):
    """Deja el carrusel anidado con n diapositivas copiadas de la primera (misma estructura y clases).
    Devuelve la lista de mapas {id original de la diapositiva 1: id en la diapositiva k}."""
    global HTML
    car = ELEM[car_id]; first = car['elements'][0]
    # JSON
    for e in car['elements'][1:]:
        ELEM.pop(e['id'], None)
    maps = [{x: x for x in _ids(first)}]
    slides = [first]
    for k in range(1, n):
        cp = copy.deepcopy(first); mp = {}
        def reid(e):
            nid = newid(); mp[e['id']] = nid; e['id'] = nid
            for c in e.get('elements', []): reid(c)
        reid(cp); maps.append(mp); slides.append(cp)
    car['elements'] = slides
    for sl in slides: index(sl, car)
    car['settings']['carousel_items'] = [{'_id': newid(), 'slide_title': t} for t in titles]
    # HTML
    def f(blk):
        w0 = blk.index('<div class="swiper-wrapper"'); w1 = blk.index('>', w0) + 1
        # cada diapositiva es <div class="swiper-slide" ...> ... </div> balanceado
        out = []; i = w1
        m = re.search(r'<div class="swiper-slide"', blk[i:])
        s0 = i + m.start(); d = 0
        for t in re.finditer(r'<div\b|</div>', blk[s0:]):
            d += 1 if t.group(0) == '<div' else -1
            if d == 0: s1 = s0 + t.end(); break
        tpl = blk[s0:s1]
        # fin del wrapper: después de la última diapositiva
        d = 0
        for t in re.finditer(r'<div\b|</div>', blk[w0:]):
            d += 1 if t.group(0) == '<div' else -1
            if d == 0: wend = w0 + t.start(); break
        for k, mp in enumerate(maps):
            sl = tpl
            for o, nn in mp.items():
                if o == nn: continue
                sl = (sl.replace(f'elementor-element-{o} ', f'elementor-element-{nn} ').replace(f'elementor-element-{o}"', f'elementor-element-{nn}"')
                        .replace(f'data-id="{o}"', f'data-id="{nn}"'))
            sl = re.sub(r'data-slide="\d+"', f'data-slide="{k + 1}"', sl, count=1)
            sl = re.sub(r'aria-label="\d+ of \d+"', f'aria-label="{k + 1} of {n}"', sl, count=1)
            out.append(sl)
        return blk[:w1] + '\n' + '\n'.join(out) + '\n' + blk[wend:]
    html_sub_in(car_id, f)
    for mp in maps[1:]: copy_css_rules(mp)
    return maps

def _ids(e):
    r = [e['id']]
    for c in e.get('elements', []): r += _ids(c)
    return r

def replace_everywhere(pairs, json_too=True, html_too=True, css_too=True):
    """Reemplazos literales (colores, fuentes) en JSON, HTML y CSS de la plantilla."""
    global J, HTML, CSS
    if json_too:
        t = json.dumps(J, ensure_ascii=False)
        for o, n in pairs: t = re.sub(re.escape(o), lambda m, n=n: n, t, flags=re.I)
        J = json.loads(t); ELEM.clear(); PARENT.clear()
        for e in J['content']: index(e)
    for o, n in pairs:
        if html_too: HTML = re.sub(re.escape(o), lambda m, n=n: n, HTML, flags=re.I)
        if css_too: CSS = re.sub(re.escape(o), lambda m, n=n: n, CSS, flags=re.I)

PREVIEW_CSS = ''
ROOT = BASE_ROOT
exec(open(os.path.join(W, 'spec_carrera.py'), encoding='utf-8').read())
ROOT = HUMINT_ROOT
# comprobación: la etapa 1 tiene que dar exactamente la base de Carrera
def _strip0(e):
    e = dict(e); e.pop('htmlCache', None); e['elements'] = [_strip0(c) for c in e.get('elements', [])]; return e
_base = json.load(open(os.path.join(BASE_ROOT, 'carrera-diplomatica.json'), encoding='utf-8'))['content']
assert [_strip0(e) for e in J['content']] == _base, 'la etapa 1 no reproduce carrera-diplomatica.json'
LOG.append('Etapa 1 = carrera-diplomatica.json (idéntico)')
LOG_CARRERA = LOG[:]; LOG.clear()
if os.path.exists(os.path.join(W, 'humint.py')): exec(open(os.path.join(W, 'humint.py'), encoding='utf-8').read())

# ---------------------------------------------------------------- salida
def _strip_cache(e):
    e.pop('htmlCache', None)
    for c in e.get('elements', []): _strip_cache(c)
out_json = copy.deepcopy(J)
for e in out_json['content']: _strip_cache(e)
TITLE = 'HUMINT: INTELIGENCIA DE FUENTES HUMANAS'
page_json = {'version': '0.4', 'title': TITLE, 'type': 'page', 'content': out_json['content'], 'page_settings': [], 'metadata': []}
jet = dict(out_json); jet['title'] = TITLE
open(os.path.join(ROOT, 'humint.json'), 'w', encoding='utf-8').write(json.dumps(page_json, ensure_ascii=False))
open(os.path.join(ROOT, 'humint-jetwoobuilder.json'), 'w', encoding='utf-8').write(json.dumps(jet, ensure_ascii=False))
def media_end(css, head):
    i = css.find(head + '{')
    if i < 0: return None
    d = 0
    for k in range(css.find('{', i), len(css)):
        if css[k] == '{': d += 1
        elif css[k] == '}':
            d -= 1
            if d == 0: return k + 1
groups = {'': [], '(max-width:1366px)': [], '(max-width:1024px)': [], '(max-width:932px)': []}
for media, sel, body in css_rules(chr(10).join(EXTRA_CSS)):
    head = media.replace('@media', '').replace(' ', '')
    groups.setdefault(head, []).append(sel + '{' + body + '}')
NL = chr(10)
seg = CSS
desk = groups.pop('')
for head, rules in groups.items():
    e = media_end(seg, '@media' + head)
    if e is None:
        desk.append('@media' + head + '{' + NL.join(rules) + '}'); continue
    seg = seg[:e] + NL + '@media' + head + '{' + NL.join(rules) + '}' + NL + seg[e:]
k = seg.find('@media(max-width:1366px){')
seg = seg[:k] + NL + NL.join(desk) + NL + seg[k:]
# CSS personalizado desde el JSON, en su sitio original
def _custom(m):
    i = m.group(1)
    if i not in ELEM: return ''
    return _local((S(i).get('custom_css') or '').replace('selector', pre(i)))
def _local(t):
    # (vista previa) imágenes del sitio -> copia local en _preview/a (mismo nombre que usa extract.py)
    def f(m):
        y, mo, name = m.group(1), m.group(2), m.group(3)
        loc = name if (y, mo) == ('2026', '10') else y + mo + '_' + name
        return 'a/' + loc if os.path.exists(os.path.join(P, 'a', loc)) else m.group(0)
    return re.sub(r'https://grupogoberna\.com/wp-content/uploads/(\d{4})/(\d{2})/([A-Za-z0-9._-]+)', f, t)
seg = re.sub(r'\x00CUSTOM:([0-9a-f]+)\x00', _custom, seg)
css = CSS_PRE + seg + NL + NL.join(EXTRA_CUSTOM) + NL + CSS_POST + NL + PREVIEW_CSS
page.build(HTML, css, 'landing.html', 'HUMINT')
print('ok', len(HTML), len(css))
for l in LOG: print(l)
