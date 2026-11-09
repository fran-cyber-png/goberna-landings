# Propuesta A (sección Plan de estudios: la lista se desplaza mientras la sección queda fija).
# Lee _preview/landing.html SIN modificarlo y escribe _preview/propuesta-a.html.
# El CSS y el JS salen de a-elementor.txt (los mismos bloques que irán al custom_css y al widget HTML de Elementor).
# Uso: python build_a.py            -> propuesta-a.html (barra de progreso desactivada)
#      python build_a.py --progress -> propuesta-a-progreso.html (barra de progreso activada, para probarla)
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SRC = os.path.join(ROOT, '_preview', 'landing.html')
DST_DIR = os.path.join(ROOT, '_preview')
TXT = os.path.join(HERE, 'a-elementor.txt')
SECTION_ID = '7c39e8aa'

def block(txt, start, end):
    """Texto entre la línea que empieza por `start` y la que empieza por `end` (sin esas líneas)."""
    lines = txt.split('\n')
    i = next(k for k, l in enumerate(lines) if l.startswith(start))
    j = next(k for k, l in enumerate(lines) if l.startswith(end) and k > i)
    return '\n'.join(lines[i + 1:j]).strip('\n')

def section_span(html, sid):
    """(inicio, fin) del bloque <div ... data-id="sid"> balanceado, y el texto de su etiqueta de apertura."""
    m = re.search(r'<div\b[^>]*\bdata-id="%s"[^>]*>' % re.escape(sid), html)
    if not m:
        raise KeyError('no está en el HTML: ' + sid)
    s = m.start(); depth = 0
    for t in re.finditer(r'<div\b|</div>', html[s:]):
        depth += 1 if t.group(0) == '<div' else -1
        if depth == 0:
            return s, s + t.end(), m.group(0)
    raise ValueError(sid)

def build(progress=False):
    html = open(SRC, encoding='utf-8').read()
    txt = open(TXT, encoding='utf-8').read()
    css = block(txt, '=== CSS', '=== FIN CSS').replace('selector', '.ak-plan-pin')
    js = block(txt, '=== JS', '=== FIN JS')
    if progress:
        js = js.replace('var SHOW_PROGRESS = false;', 'var SHOW_PROGRESS = true;')
        assert 'SHOW_PROGRESS = true' in js

    s, e, tag = section_span(html, SECTION_ID)
    assert 'ak-plan' in tag, 'la etiqueta del bloque no es la sección de módulos'
    # el ID «modulos» pasa al contenedor exterior (el enlace del menú sigue apuntando al inicio)
    assert ' id="modulos"' in tag, 'la sección no tiene id="modulos"'
    new_tag = tag.replace(' id="modulos"', '', 1)
    section = new_tag + html[s + len(tag):e]
    wrapped = ('<div class="ak-plan-pin" id="modulos">\n' + section + '\n</div>\n'
               '<script id="propuesta-a-js">\n' + js + '\n</script>\n')
    out = html[:s] + wrapped + html[e:]

    style = '<style id="propuesta-a-css">\n' + css + '\n</style>\n'
    assert '</head>' in out, 'no hay </head>'
    out = out.replace('</head>', style + '</head>', 1)

    name = 'propuesta-a-progreso.html' if progress else 'propuesta-a.html'
    open(os.path.join(DST_DIR, name), 'w', encoding='utf-8').write(out)
    print('escrito', os.path.join(DST_DIR, name), len(out))

if __name__ == '__main__':
    build(progress='--progress' in sys.argv[1:])
