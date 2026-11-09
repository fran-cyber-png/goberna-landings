# Utilidades: cada cambio se aplica a la vez al JSON de Elementor y a la vista previa (HTML/CSS renderizado de la base 93575)
import json, re, os, copy, random, html as _html

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(W, '..')
P = os.path.join(W, 'prev')
TPL = '93575'

J = json.load(open(os.path.join(W, 'base.json'), encoding='utf-8'))
HTML = open(os.path.join(W, 'base.html'), encoding='utf-8').read()
CSS_ALL = open(os.path.join(W, 'base.css'), encoding='utf-8').read()
_a = CSS_ALL.find('post-93575.css'); _a = CSS_ALL.rfind('/*', 0, _a)
_b = CSS_ALL.find('sticky.min.css'); _b = CSS_ALL.rfind('/*', 0, _b)
CSS_PRE, CSS, CSS_POST = CSS_ALL[:_a], CSS_ALL[_a:_b], CSS_ALL[_b:]
EXTRA_CSS = []      # reglas que en Elementor salen de los ajustes
EXTRA_CUSTOM = []   # CSS personalizado nuevo
LOG = []

WP = 'https://grupogoberna.com/wp-content/uploads/2026/10/'
UPLOADS = json.load(open(os.path.join(W, 'uploads.json'), encoding='utf-8')) if os.path.exists(os.path.join(W, 'uploads.json')) else {}
def wp(name):
    u = UPLOADS.get(name)
    return (u['url'], u['id']) if u else (WP + name, '')

ELEM, PARENT = {}, {}
def reindex():
    ELEM.clear(); PARENT.clear()
    def index(e, parent=None):
        ELEM[e['id']] = e; PARENT[e['id']] = parent
        for c in e.get('elements', []): index(c, e)
    for n in J['content']: index(n)
reindex()
def S(i): return ELEM[i]['settings']
def pre(i): return f'.elementor-{TPL} .elementor-element.elementor-element-' + i

_used = set(ELEM)
def nid():
    while True:
        i = '%07x' % random.randrange(0x1000000, 0xfffffff)
        if i not in _used: _used.add(i); return i

# ---------------------------------------------------------------- HTML
def el_span(h, i):
    m = re.search(r'<(div|details)[^>]*\bdata-id="%s"' % re.escape(i), h)
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
def html_global(old, new, count=-1):
    global HTML
    assert old in HTML, old[:80]
    HTML = HTML.replace(old, new) if count < 0 else HTML.replace(old, new, count)

# ---------------------------------------------------------------- operaciones de contenido
def heading(i, h):
    S(i)['title'] = h
    def f(blk):
        r, n = re.subn(r'(<(h[1-6]|p|div|span)\s+class="elementor-heading-title[^"]*">)(.*?)(</\2>)',
                       lambda m: m.group(1) + h + m.group(4), blk, count=1, flags=re.S)
        assert n, i; return r
    html_sub_in(i, f)

def text(i, h):
    S(i)['editor'] = h
    def f(blk):
        r, n = re.subn(r'(<div class="elementor-widget-container">)(.*?)(</div>)',
                       lambda m: m.group(1) + h + m.group(3), blk, count=1, flags=re.S)
        assert n, i; return r
    html_sub_in(i, f)

def button(i, txt=None, url=None):
    if txt is not None: S(i)['text'] = txt
    if url is not None: S(i)['link'] = dict(S(i).get('link') or {}, url=url)
    def f(blk):
        r = blk
        if txt is not None:
            r, n = re.subn(r'(<span class="elementor-button-text">)(.*?)(</span>)', lambda m: m.group(1) + txt + m.group(3), r, count=1, flags=re.S)
            assert n, i
        if url is not None:
            r, n = re.subn(r'(<a class="elementor-button[^"]*" href=")[^"]*', lambda m: m.group(1) + _html.escape(url), r, count=1)
            assert n, i
        return r
    html_sub_in(i, f)

def image(i, name, key='image'):
    url, iid = wp(name)
    S(i)[key] = {'url': url, 'id': iid, 'size': '', 'alt': '', 'source': 'library'}
    html_sub_in(i, lambda blk: re.sub(r'(<img\b[^>]*?\ssrc=")[^"]*', lambda m: m.group(1) + 'a/' + name, blk, count=1))

def bg_image(i, name, key='background_image', dev=''):
    """Fondo de contenedor: JSON + regla CSS de la vista previa."""
    url, iid = wp(name)
    S(i)[key] = {'url': url, 'id': iid, 'size': '', 'alt': '', 'source': 'library'}
    rule = (f'{pre(i)}:not(.elementor-motion-effects-element-type-background), {pre(i)} > .elementor-motion-effects-container > '
            f'.elementor-motion-effects-layer{{background-image:url("a/{name}")}}')
    EXTRA_CSS.append(f'@media{DEV[dev]}{{{rule}}}' if DEV[dev] else rule)

def setv(i, **kw): S(i).update(kw)

DEV = {'': None, '_laptop': '(max-width:1366px)', '_tablet': '(max-width:1024px)', '_mobile': '(max-width:932px)'}
SEL = {'heading': ' .elementor-heading-title', 'text-editor': '', 'button': ' .elementor-button'}
def typo(i, **kw):
    """kw: family, weight, transform, size, lh, lh_unit, ls (+ _laptop/_tablet/_mobile)."""
    s = S(i); w = ELEM[i].get('widgetType'); sel = SEL[w]
    s['typography_typography'] = 'custom'
    rules = {d: [] for d in DEV}
    unit = kw.pop('lh_unit', 'px')
    for k, v in kw.items():
        base, dev = k, ''
        for d in ('_laptop', '_tablet', '_mobile'):
            if k.endswith(d): base, dev = k[:-len(d)], d
        if base == 'family': s['typography_font_family' + dev] = v; rules[dev].append(f'font-family:"{v}", Sans-serif')
        elif base == 'weight': s['typography_font_weight' + dev] = str(v); rules[dev].append(f'font-weight:{v}')
        elif base == 'transform': s['typography_text_transform' + dev] = v; rules[dev].append(f'text-transform:{v}')
        elif base == 'size': s['typography_font_size' + dev] = {'unit': 'px', 'size': v, 'sizes': []}; rules[dev].append(f'font-size:{v}px')
        elif base == 'lh': s['typography_line_height' + dev] = {'unit': unit, 'size': v, 'sizes': []}; rules[dev].append(f'line-height:{v}{unit}')
        elif base == 'ls': s['typography_letter_spacing' + dev] = {'unit': 'px', 'size': v, 'sizes': []}; rules[dev].append(f'letter-spacing:{v}px')
    # las reglas nuevas van al final: repetir los valores de tablet/mobile que ya tenía el elemento
    KEYS = {'size': ('typography_font_size', lambda v: f'font-size:{v["size"]}{v["unit"]}'),
            'lh': ('typography_line_height', lambda v: f'line-height:{v["size"]}{v["unit"]}'),
            'ls': ('typography_letter_spacing', lambda v: f'letter-spacing:{v["size"]}{v["unit"]}'),
            'family': ('typography_font_family', lambda v: f'font-family:"{v}", Sans-serif'),
            'weight': ('typography_font_weight', lambda v: f'font-weight:{v}')}
    given = set(kw)
    for b in {k.split('_')[0] for k in kw}:
        if b not in KEYS: continue
        key, fn = KEYS[b]
        for d in ('_tablet', '_mobile'):
            if b + d not in given and isinstance(s.get(key + d), (dict, str)) and s.get(key + d):
                rules[d].append(fn(s[key + d]))
    for d, r in rules.items():
        if not r: continue
        rule = f'{pre(i)}{sel}{{{";".join(r)}}}'
        EXTRA_CSS.append(f'@media{DEV[d]}{{{rule}}}' if DEV[d] else rule)

def color(i, c):
    w = ELEM[i].get('widgetType')
    if w == 'heading': S(i)['title_color'] = c; EXTRA_CSS.append(f'{pre(i)} .elementor-heading-title{{color:{c}}}')
    elif w == 'text-editor': S(i)['text_color'] = c; EXTRA_CSS.append(f'{pre(i)}{{color:{c}}}')
    elif w == 'button': S(i)['button_text_color'] = c; EXTRA_CSS.append(f'{pre(i)} .elementor-button{{color:{c};fill:{c}}}')

def css_sub(i, old, new, count=1):
    """Cambia un trozo del CSS personalizado del elemento i (JSON) y la regla equivalente renderizada."""
    global CSS
    s = S(i); cc = s.get('custom_css', '')
    assert old in cc, (i, old)
    s['custom_css'] = cc.replace(old, new, count)

def css_add(i, rules):
    s = S(i); s['custom_css'] = s.get('custom_css', '').rstrip() + '\n' + rules.strip() + '\n'
    EXTRA_CUSTOM.append(rules.replace('selector', pre(i)))

def remove(i):
    global HTML
    p = PARENT[i]
    if p is None: J['content'] = [c for c in J['content'] if c['id'] != i]
    else: p['elements'] = [c for c in p['elements'] if c['id'] != i]
    s, e = el_span(HTML, i); HTML = HTML[:s] + HTML[e:]
    reindex()

def strip_html_cache(e):
    e.pop('htmlCache', None)
    for c in e.get('elements', []): strip_html_cache(c)

# ---------------------------------------------------------------- constructor de elementos nuevos (JSON + HTML + CSS)
def px(v): return {'unit': 'px', 'size': v, 'sizes': []}
def box(t, r, b, l, unit='px'): return {'unit': unit, 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': False}
def gap(v): return {'column': str(v), 'row': str(v), 'isLinked': True, 'unit': 'px', 'size': v}

def _dev_rules(i, settings, mapping):
    """mapping: key -> fn(value) -> css-declarations (con sufijos de dispositivo)."""
    out = {d: [] for d in DEV}
    for k, v in settings.items():
        base, dev = k, ''
        for d in ('_laptop', '_tablet', '_mobile'):
            if k.endswith(d): base, dev = k[:-len(d)], d
        if base in mapping and v not in ('', None):
            out[dev].append(mapping[base](v))
    return out

def _boxcss(prefix):
    return lambda v: ';'.join(f'--{prefix}-{s}:{v[s]}{v["unit"]}' for s in ('top', 'right', 'bottom', 'left'))

CON_MAP = {
    'padding': _boxcss('padding'), 'margin': _boxcss('margin'),
    'flex_direction': lambda v: f'--flex-direction:{v}',
    'flex_justify_content': lambda v: f'--justify-content:{v}',
    'flex_align_items': lambda v: f'--align-items:{v}',
    'flex_wrap': lambda v: f'--flex-wrap:{v}',
    'flex_gap': lambda v: f'--gap:{v["row"]}{v["unit"]} {v["column"]}{v["unit"]};--row-gap:{v["row"]}{v["unit"]};--column-gap:{v["column"]}{v["unit"]}',
    'min_height': lambda v: f'--min-height:{v["size"]}{v["unit"]}',
    'width': lambda v: f'--width:{v["size"]}{v["unit"]}',
    'boxed_width': lambda v: f'--content-width:{v["size"]}{v["unit"]}',
    'background_color': lambda v: f'background-color:{v}',
    'background_position': lambda v: f'background-position:{v}',
    'background_size': lambda v: f'background-size:{v}',
    'background_repeat': lambda v: f'background-repeat:{v}',
    'border_border': lambda v: f'border-style:{v}',
    'border_color': lambda v: f'border-color:{v}',
    'border_width': lambda v: 'border-width:' + ' '.join(f'{v[s]}{v["unit"]}' for s in ('top', 'right', 'bottom', 'left')) + ';' + ';'.join(f'--border-{s}-width:{v[s]}{v["unit"]}' for s in ('top', 'right', 'bottom', 'left')),
}

def container(settings, children=(), parent=False, cls='', eid=None):
    i = eid or nid()
    s = dict(settings)
    if cls: s['css_classes'] = cls
    boxed = parent and s.get('content_width', 'boxed') == 'boxed'
    if not parent: s.setdefault('content_width', 'full')
    node = {'id': i, 'elType': 'container', 'settings': s, 'elements': [c['node'] for c in children], 'isInner': not parent}
    tail = 'e-flex e-con-boxed e-con e-parent' if boxed else ('e-con-full e-flex e-con e-' + ('parent' if parent else 'child'))
    if boxed: classes = f'elementor-element elementor-element-{i} {cls + " " if cls else ""}{tail}'
    else: classes = f'elementor-element elementor-element-{i} e-con-full {cls + " " if cls else ""}e-flex e-con e-' + ('parent' if parent else 'child')
    inner = ''.join(c['html'] for c in children)
    if boxed: inner = f'<div class="e-con-inner">{inner}</div>'
    h = f'<div class="{classes}" data-id="{i}" data-element_type="container" data-e-type="container">{inner}</div>'
    base = '--display:flex;--container-widget-width:100%;--container-widget-height:initial;--container-widget-flex-grow:0;--container-widget-align-self:initial;--flex-wrap-mobile:wrap'
    rules = _dev_rules(i, s, CON_MAP)
    css = [f'{pre(i)}{{{base}}}']
    if not parent: css.append(f'{pre(i)}.e-con{{--flex-grow:0;--flex-shrink:0}}')
    for d, r in rules.items():
        if r:
            rule = f'{pre(i)}{{{";".join(r)}}}'
            css.append(f'@media{DEV[d]}{{{rule}}}' if DEV[d] else rule)
    if s.get('background_image', {}).get('url'):
        css.append(f'{pre(i)}:not(.elementor-motion-effects-element-type-background){{background-image:url("a/{s["_local_bg"]}")}}')
        s.pop('_local_bg', None)
    if s.get('custom_css'): css.append(s['custom_css'].replace('selector', pre(i)))
    for c in children: css += c['css']
    return {'node': node, 'html': h, 'css': css, 'id': i}

WID_MAP = {
    '_margin': lambda v: 'margin:' + ' '.join(f'{v[s]}{v["unit"]}' for s in ('top', 'right', 'bottom', 'left')),
    '_padding': lambda v: 'padding:' + ' '.join(f'{v[s]}{v["unit"]}' for s in ('top', 'right', 'bottom', 'left')),
}
TYP = {'typography_font_family': lambda v: f'font-family:"{v}", Sans-serif', 'typography_font_weight': lambda v: f'font-weight:{v}',
       'typography_font_size': lambda v: f'font-size:{v["size"]}{v["unit"]}', 'typography_line_height': lambda v: f'line-height:{v["size"]}{v["unit"]}',
       'typography_letter_spacing': lambda v: f'letter-spacing:{v["size"]}{v["unit"]}', 'typography_text_transform': lambda v: f'text-transform:{v}'}

def _widget(wtype, settings, inner, cls=''):
    i = nid(); s = dict(settings)
    if cls: s['_css_classes'] = cls
    node = {'id': i, 'elType': 'widget', 'settings': s, 'elements': [], 'widgetType': wtype}
    h = (f'<div class="elementor-element elementor-element-{i} {cls} elementor-widget elementor-widget-{wtype}" data-id="{i}" '
         f'data-element_type="widget" data-e-type="widget" data-widget_type="{wtype}.default"><div class="elementor-widget-container">{inner}</div></div>')
    css = []
    sel = SEL.get(wtype, '')
    for d, r in _dev_rules(i, s, TYP).items():
        if r:
            rule = f'{pre(i)}{sel}{{{";".join(r)}}}'
            css.append(f'@media{DEV[d]}{{{rule}}}' if DEV[d] else rule)
    for d, r in _dev_rules(i, s, WID_MAP).items():
        if r:
            rule = f'{pre(i)} > .elementor-widget-container{{{";".join(r)}}}'
            css.append(f'@media{DEV[d]}{{{rule}}}' if DEV[d] else rule)
    if s.get('custom_css'): css.append(s['custom_css'].replace('selector', pre(i)))
    return {'node': node, 'html': h, 'css': css, 'id': i, 'settings': s}

def w_heading(title, tag='h2', color=None, cls='', **typ):
    s = {'title': title, 'header_size': tag}
    s.update(_typ(typ))
    if color: s['title_color'] = color
    w = _widget('heading', s, f'<{tag} class="elementor-heading-title elementor-size-default">{title}</{tag}>', cls)
    if color: w['css'].append(f'{pre(w["id"])} .elementor-heading-title{{color:{color}}}')
    return w

def w_text(htmltxt, color=None, cls='', **typ):
    s = {'editor': htmltxt}; s.update(_typ(typ))
    if color: s['text_color'] = color
    w = _widget('text-editor', s, htmltxt, cls)
    if color: w['css'].append(f'{pre(w["id"])}{{color:{color}}}')
    return w

def w_image(name, cls='', **extra):
    url, iid = wp(name)
    s = {'image': {'url': url, 'id': iid, 'size': '', 'alt': '', 'source': 'library'}, 'image_size': 'full'}; s.update(extra)
    return _widget('image', s, f'<img decoding="async" src="a/{name}" alt="">', cls)

def w_button(txt, url, cls='', icon='fas fa-arrow-right', **extra):
    s = {'text': txt, 'link': {'url': url, 'is_external': 'on' if url.startswith('http') else '', 'nofollow': ''},
         'selected_icon': {'value': icon, 'library': 'fa-solid'}, 'icon_align': 'right'}
    s.update(extra)
    ext = ' target="_blank" rel="noopener"' if url.startswith('http') else ''
    inner = (f'<div class="elementor-button-wrapper"><a class="elementor-button elementor-button-link elementor-size-sm" href="{_html.escape(url)}"{ext}><span class="elementor-button-content-wrapper">'
             f'<span class="elementor-button-icon"><i aria-hidden="true" class="{icon}"></i></span>'
             f'<span class="elementor-button-text">{txt}</span></span></a></div>')
    w = _widget('button', s, inner, cls)
    if s.get('icon_align') == 'right': w['css'].append(f'{pre(w["id"])} .elementor-button-content-wrapper{{flex-direction:row-reverse}}')
    if s.get('icon_indent'): w['css'].append(f'{pre(w["id"])} .elementor-button .elementor-button-content-wrapper{{gap:{s["icon_indent"]["size"]}px}}')
    return w

def _typ(t):
    out = {}
    if not t: return out
    out['typography_typography'] = 'custom'
    unit = t.pop('lh_unit', 'px')
    for k, v in t.items():
        base, dev = k, ''
        for d in ('_laptop', '_tablet', '_mobile'):
            if k.endswith(d): base, dev = k[:-len(d)], d
        key = {'family': 'typography_font_family', 'weight': 'typography_font_weight', 'size': 'typography_font_size', 'lh': 'typography_line_height',
               'ls': 'typography_letter_spacing', 'transform': 'typography_text_transform'}[base] + dev
        if base in ('family', 'transform'): out[key] = v
        elif base == 'weight': out[key] = str(v)
        elif base == 'lh': out[key] = {'unit': unit, 'size': v, 'sizes': []}
        else: out[key] = px(v)
    return out

def collect_css(c):
    out = list(c['css'])
    for ch in c.get('_children', []): out += collect_css(ch)
    return out

def build(c_factory):
    """Devuelve el contenedor y aplana su CSS (incluido el de los hijos) en EXTRA_CUSTOM."""
    return c_factory

def insert_after(ref_id, comp):
    """Inserta un contenedor padre nuevo después de la sección ref_id (JSON + HTML + CSS)."""
    global HTML
    idx = [c['id'] for c in J['content']].index(ref_id)
    J['content'].insert(idx + 1, comp['node'])
    s, e = el_span(HTML, ref_id)
    HTML = HTML[:e] + comp['html'] + HTML[e:]
    reindex()

def replace_section(old_id, comp):
    global HTML
    idx = [c['id'] for c in J['content']].index(old_id)
    J['content'][idx] = comp['node']
    s, e = el_span(HTML, old_id)
    HTML = HTML[:s] + comp['html'] + HTML[e:]
    reindex()
