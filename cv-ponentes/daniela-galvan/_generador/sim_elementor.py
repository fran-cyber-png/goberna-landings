"""Simula el marcado de Elementor (contenedores flex + widgets) a partir del JSON para medirlo con Playwright.
No reemplaza a Elementor (no hay sticky de JS ni estilos del kit), pero comprueba que el CSS personalizado
coloque cada widget donde dice el Figma."""
import json, os, sys, html
S = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(S)
OUT = sys.argv[1]
d = json.load(open(os.path.join(P, 'daniela-galvan.json'), encoding='utf-8'))
root = d['content'][0]
BIB = 'https://grupogoberna.com/wp-content/uploads/2026/10/'

def loc(url):  # imágenes de la Biblioteca -> archivo local copiado junto al html
    return url.replace(BIB, 'img/')

def render(e):
    s = e['settings']
    if e['elType'] == 'container':
        cls = f"elementor-element elementor-element-{e['id']} e-con e-flex {'e-child' if e.get('isInner') else 'e-parent'} {s.get('css_classes','')}"
        st = f"--flex-direction:{s.get('flex_direction','column')};"
        if s.get('background_image'):
            st += f"background-color:{s['background_color']};background-image:url({loc(s['background_image']['url'])});background-position:{s['background_position']};background-repeat:no-repeat;background-size:cover;"
        return f'<div class="{cls}" style="{st}">' + ''.join(render(k) for k in e['elements']) + '</div>'
    w = e['widgetType']
    cls = f"elementor-element elementor-element-{e['id']} elementor-widget elementor-widget-{w} {s.get('_css_classes','')}"
    if w == 'heading':
        inner = f"<{s.get('header_size','h2')} class=\"elementor-heading-title elementor-size-default\">{s['title']}</{s.get('header_size','h2')}>"
    elif w == 'text-editor':
        inner = s['editor']
    elif w == 'image':
        inner = f"<img src=\"{loc(s['image']['url'])}\" alt=\"{html.escape(s['image'].get('alt',''))}\">"
    return f'<div class="{cls}"><div class="elementor-widget-container">{inner}</div></div>'

css = root['settings']['custom_css'].replace('selector', f".elementor-element-{root['id']}")
BASE = '''
*,*::before,*::after{box-sizing:border-box}
body{margin:0;font-family:Arial,sans-serif}
.e-con{--gap:0px;display:flex;flex-direction:var(--flex-direction);flex-wrap:nowrap;gap:var(--gap);position:relative;width:100%;max-width:100%;padding:0;min-width:0}
.e-con>.elementor-widget{max-width:100%}
.elementor-widget{position:relative}
.elementor-widget:not(:last-child){margin-bottom:20px}
.elementor-heading-title{padding:0;margin:0;line-height:1}
.elementor-widget-image{text-align:center}
.elementor img{height:auto;max-width:100%;border:none}
'''
page = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400&family=Montserrat:wght@400;700;800&family=Open+Sans:wght@400;700&family=Sora:wght@400;700&display=swap">
<style>{BASE}</style><style>{css}</style></head><body><div class="elementor">{render(root)}</div></body></html>'''
open(OUT, 'w', encoding='utf-8').write(page)
print('ok', OUT, len(page))
