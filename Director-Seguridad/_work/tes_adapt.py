# Sección "Experiencia Goberna" para otra landing: estructura de 93795 (video + texto) con el estilo de 93792 (bloque testimonios)
import json, copy, re, sys
sys.stdout.reconfigure(encoding='utf-8')
STRUCT = 'C:/Users/Consultoría/Downloads/elementor-93795-2026-10-20.json'
STYLE  = 'C:/Users/Consultoría/Downloads/elementor-93792-2026-10-20.json'
OUT    = 'C:/Users/Consultoría/Documents/Director-Seguridad/otra-landing-testimonios/testimonios-video-adaptado.json'
d = json.load(open(STRUCT, encoding='utf-8'))
st = json.load(open(STYLE, encoding='utf-8'))
E = {}
def idx(e):
    E[e['id']] = e
    for x in e.get('elements', []): idx(x)
for c in st['content']: idx(c)
for c in d['content']: idx(c)
S = lambda i: E[i]['settings']

G_OLD = 'linear-gradient(to bottom right, #FFBB03 0%, #FFBB03 50%, #FFBB03 100%)'
G_NEW = 'linear-gradient(to bottom right, #CB861B 0%, #F5C02F 50%, #CB861B 100%)'

# ---- sección: caja, rellenos, separación y fondo del bloque de estilo
sec = S('230262f0'); ref = S('332c7cca')
for k in ('padding','padding_laptop','padding_tablet','padding_mobile','boxed_width','flex_gap','flex_gap_tablet','background_color'):
    sec[k] = copy.deepcopy(ref[k])
css = sec['custom_css']
css = css.replace(G_OLD, G_NEW).replace('#FFBB03', '#CB861B').replace('rgba(255,187,3,', 'rgba(203,134,27,')
css = css.replace('#E3E6EB', '#A0ABBC')
# relleno lateral de mobile pasa de 16 a 24: el carril de miniaturas se ajusta igual
css = css.replace('margin-left: -16px', 'margin-left: -24px').replace('margin-right: -16px', 'margin-right: -24px')
css = css.replace('padding-left: 16px', 'padding-left: 24px').replace('padding-right: 16px', 'padding-right: 24px')
css = css.replace('calc(100% + 32px)', 'calc(100% + 48px)').replace('scroll-margin-left: 16px', 'scroll-margin-left: 24px')
css = css.replace('/* Experiencia Goberna · nativos', '/* Experiencia Goberna · estilo de la otra landing (dorado de 3 tonos, Barlow) · nativos')
# el dorado de 3 tonos en textos, como en el bloque de estilo
css = css.replace('selector .ak-g {', 'selector .ak-oro-text .elementor-heading-title, selector .ak-g {', 1)
# saltos del título como en el bloque de estilo: el <br class="ak-dk"> solo se oculta en mobile
css = css.replace('@media (max-width: 1366px) {\n  selector .ak-dk { display: none; }\n', '@media (max-width: 1366px) {\n')
css = css.replace('@media (max-width: 767px) {\n  selector .ak-vr', '@media (max-width: 767px) {\n  selector .ak-dk { display: none; }\n  selector .ak-vr', 1)
css = css.replace('selector .ak-vh2 .elementor-heading-title { text-wrap: balance; }\n', '')
assert 'ak-dk { display: none; }\n  selector .ak-vr' in css
sec['custom_css'] = css

# ---- cuadro del video: fondo oscuro del bloque de estilo
vp = S('644daf6c'); vp['background_color'] = S('6f2a7c8b')['background_color']

# ---- etiqueta superior = "Testimonios" del bloque de estilo
TYPO = [k for k in S('e688248') if k.startswith('typography_')]
def take(dst, src, extra=()):
    s = S(dst)
    for k in [k for k in list(s) if k.startswith('typography_') or k == 'title_color' or k == 'text_color']: s.pop(k)
    for k in [k for k in S(src) if k.startswith('typography_') or k in ('title_color','text_color') or k in extra]:
        s[k] = copy.deepcopy(S(src)[k])
take('6fe388ac', 'e688248')
S('6fe388ac')['_css_classes'] = 'ak-veye ak-oro-text'
# ---- título = título del bloque de estilo (Barlow 700 mayúsculas) con sus márgenes
take('681cf146', '35f4952e', extra=('_margin','_margin_laptop','_margin_mobile'))
S('681cf146')['title'] = 'Más que un aula:<br><span class="ak-g">Una comunidad que<br class="ak-dk"> actúa</span>'
# ---- párrafo: el bloque de estilo no tiene uno; misma fuente y tamaños, en el negro del estilo
S('5bdc1bce')['text_color'] = '#060606'

# ---- reproductor (widget HTML): colores del estilo
h = S('147f379f')['html']
rep = [('#15262F','#1B2333'), ('#FFD466','#F5C02F'), ('#FFBB03','#CB861B'), ('rgba(255,187,3,','rgba(203,134,27,'), ('rgba(10,22,40,','rgba(6,6,6,')]
for a,b in rep: h = h.replace(a,b)
h = h.replace('background:linear-gradient(90deg,#CB861B,#F5C02F)', 'background:linear-gradient(90deg,#CB861B,#F5C02F,#CB861B)')
h = h.replace('border-radius:50%;background:#CB861B;box-shadow:0 0 0 10px', 'border-radius:50%;background:' + G_NEW + ';box-shadow:0 0 0 10px')
h = h.replace('fill:#1B2333}', 'fill:#060606}')
S('147f379f')['html'] = h
assert '#FFBB03' not in h and '#15262F' not in h, 'quedó un color viejo en el player'

def strip(e):
    e.pop('htmlCache', None)
    for x in e.get('elements', []): strip(x)
for c in d['content']: strip(c)
d['title'] = 'testimonios video adaptado'
json.dump(d, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print('ok', OUT)
for i in ('230262f0','6fe388ac','681cf146','5bdc1bce'): print(i, {k:v for k,v in S(i).items() if k!='custom_css'})
