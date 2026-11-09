# Sección Docentes tomada de la landing publicada (export jet-woo-builder-94061, 24/10), con los cambios que pide el usuario.
# Uso: python _work/docentes.py  ->  docentes-carrera-diplomatica.json (contenedor para Plantillas guardadas)
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SRC = r'C:\Users\Consultoría\Downloads\jet-woo-builder-94061-2026-10-24.json'
DST = os.path.join(ROOT, 'docentes-carrera-diplomatica.json')
QUITAR = ['MARIA HERRERA']   # nombre tal como está en el heading de la card

J = json.load(open(SRC, encoding='utf-8'))
sec = next(c for c in J['content'] if c['settings'].get('css_classes') == 'ak-doc')

def strip(e):
    e.pop('htmlCache', None)   # HTML renderizado viejo (con las cards que se quitan); Elementor lo regenera
    for c in e.get('elements', []): strip(c)
strip(sec)

def find(e, wt):
    if e.get('widgetType') == wt: return e
    for c in e.get('elements', []):
        r = find(c, wt)
        if r: return r
car = find(sec, 'nested-carousel')
def headings(e):
    out = [e['settings'].get('title', '')] if e.get('widgetType') == 'heading' else []
    for c in e.get('elements', []): out += headings(c)
    return out

items = car['settings']['carousel_items']
assert len(items) == len(car['elements'])
keep = [k for k, sl in enumerate(car['elements']) if not any(n in headings(sl) for n in QUITAR)]
assert len(keep) == len(items) - len(QUITAR), 'no encontré a todos los que hay que quitar'
car['elements'] = [car['elements'][k] for k in keep]
car['settings']['carousel_items'] = [items[k] for k in keep]

out = {'content': [sec], 'page_settings': [], 'version': '0.4', 'title': 'docentes carrera diplomatica', 'type': 'container'}
blob = json.dumps(out, ensure_ascii=False)
assert not any(n in blob for n in QUITAR)
open(DST, 'w', encoding='utf-8').write(blob)
print('escrito', DST, len(blob) // 1024, 'KB |', len(keep), 'cards:', [headings(s)[1] for s in car['elements']])
