# JSON de la sección Ponentes: parte de la última base editada por el usuario y le aplica los ajustes aprobados
import json, copy
SRC = 'C:/Users/Consultoría/Downloads/elementor-93694-2026-10-16.json'
OUT = 'C:/Users/Consultoría/Documents/Director-Seguridad/ponentes-director-seguridad.json'
d = json.load(open(SRC, encoding='utf-8'))
sec = d['content'][0]
car = sec['elements'][1]
cards = [sl['elements'][0] for sl in car['elements']]

# 1) estilo de la tarjeta de Francisco López en las demás (nombre, especialidad y "Ver trayectoria")
CONTENT = {'title', 'editor', 'text', 'link', 'image', 'background_image'}
def body(c): return c['elements'][1]['elements']          # [nombre, especialidad, botón]
ref = body(cards[0])
for c in cards[1:]:
    for src, dst in zip(ref, body(c)):
        assert src.get('widgetType') == dst.get('widgetType')
        keep = {k: v for k, v in dst['settings'].items() if k in CONTENT}
        dst['settings'] = copy.deepcopy(src['settings']); dst['settings'].update(keep)

# 2) el bloque de texto apoyado en el borde inferior también en laptop y tablet (en desktop lo baja el margen
#    de 125 px del nombre; en mobile ya estaba): el nombre queda a la misma altura relativa en todos los tamaños
css = sec['settings'].get('custom_css', '')
# 3) degradado más corto (doc_grad.css), pedido por el usuario
for f in ('doc_laptop.css', 'doc_grad.css'):
    extra = open('C:/Users/Consultoría/Documents/Director-Seguridad/_work/' + f, encoding='utf-8').read()
    if extra.strip() not in css:
        css = css.rstrip() + '\n' + extra
sec['settings']['custom_css'] = css

def strip(e):
    e.pop('htmlCache', None)
    for x in e.get('elements', []): strip(x)
strip(sec)
json.dump(d, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print('ok', OUT)
