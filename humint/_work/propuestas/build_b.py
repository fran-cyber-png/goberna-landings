# Propuesta B · vista previa: copia _preview/landing.html (sin tocarlo) e inyecta el CSS y el widget
# de b-elementor.txt. Resultado: _preview/propuesta-b.html.
# Uso: python build_b.py   (desde cualquier carpeta)
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SRC = os.path.join(ROOT, '_preview', 'landing.html')
OUT = os.path.join(ROOT, '_preview', 'propuesta-b.html')
FUENTE = os.path.join(HERE, 'b-elementor.txt')
SECTION_ID = '7c39e8aa'   # #modulos (ak-plan)

def partes(txt):
    """Devuelve (css, widget) según los marcadores ### CSS y ### WIDGET HTML (solo al inicio de línea:
    la cabecera del archivo también menciona estos textos)."""
    m_css = re.search(r'^### CSS$', txt, re.M)
    m_w = re.search(r'^### WIDGET HTML$', txt, re.M)
    assert m_css and m_w and m_css.end() < m_w.start(), 'marcadores ### CSS / ### WIDGET HTML no encontrados'
    css = txt[m_css.end():m_w.start()].strip('\n')
    widget = txt[m_w.end():].strip('\n')
    return css, widget

def main():
    txt = open(FUENTE, encoding='utf-8').read()
    css, widget = partes(txt)
    # en Elementor, «selector» es el elemento de la sección; en la vista previa, su clase
    css = css.replace('selector', '.elementor-element.elementor-element-%s' % SECTION_ID)
    html = open(SRC, encoding='utf-8').read()
    assert html.count('</head>') == 1 and html.count('</body>') == 1, 'estructura inesperada'
    assert 'data-id="%s"' % SECTION_ID in html, 'no está la sección de módulos'
    html = html.replace('</head>', '<style id="ak-plan-b">\n' + css + '\n</style>\n</head>')
    html = html.replace('</body>', widget + '\n</body>')
    open(OUT, 'w', encoding='utf-8').write(html)
    print('ok', OUT, len(html))

if __name__ == '__main__':
    main()
