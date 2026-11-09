# Vista previa de la sección adaptada: markup y CSS reales de la página publicada + los ajustes nuevos del JSON
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
W = 'C:/Users/Consultoría/Documents/Director-Seguridad/'
SP = 'C:/Users/Consultoría/AppData/Local/Temp/claude/C--Users-Consultor-a-Documents-Director-Seguridad/67a11d1e-d5e0-4ea7-95a2-fbb026e1dd03/scratchpad/'
live = open(SP + 'live.html', encoding='utf-8').read()
css = json.loads(open(W + '_work/tes_live.css', encoding='utf-8').read())
J = json.load(open(W + 'otra-landing-testimonios/testimonios-video-adaptado.json', encoding='utf-8'))
MAP = {'230262f0':'6a12cc55','644daf6c':'5fe95b15','147f379f':'76cef54d','71a592ce':'1b13e5f3','6fe388ac':'11acca34','681cf146':'7d8995c7','5bdc1bce':'63b3d02a'}
E = {}
def idx(e):
    E[e['id']] = e
    for x in e.get('elements', []): idx(x)
idx(J['content'][0]); S = lambda i: E[i]['settings']

def span(h, i):
    m = re.search(r'<div[^>]*\bdata-id="%s"' % i, h); s = m.start(); d = 0
    for t in re.finditer(r'<div\b|</div>', h[s:]):
        d += 1 if t.group(0) == '<div' else -1
        if d == 0: return s, s + t.end()
a, b = span(live, MAP['230262f0']); sec = live[a:b]
sec = re.sub(r'<noscript>.*?</noscript>', '', sec, flags=re.S)
# reproductor nuevo
wa, wb = span(sec, MAP['147f379f'])
w = sec[wa:wb]; k = w.index('<div class="elementor-widget-container">') + len('<div class="elementor-widget-container">')
sec = sec[:wa] + w[:k] + S('147f379f')['html'] + '</div></div>' + sec[wb:]
# textos nuevos
def set_heading(i, html):
    global sec
    x, y = span(sec, MAP[i]); blk = sec[x:y]
    blk = re.sub(r'(class="elementor-heading-title[^"]*">)(.*?)(</(?:h[1-6]|p)>)', lambda m: m.group(1) + html + m.group(3), blk, count=1, flags=re.S)
    sec = sec[:x] + blk + sec[y:]
set_heading('681cf146', S('681cf146')['title'])
x, y = span(sec, MAP['6fe388ac']); sec = sec[:x] + sec[x:y].replace('class="elementor-element elementor-element-11acca34 ak-veye', 'class="elementor-element elementor-element-11acca34 ak-veye ak-oro-text') + sec[y:]

P = '.elementor-93575 .elementor-element.elementor-element-'
def px(v): return v['size'] if 'size' in v else None
def box(v): return ' '.join(f"{v[s]}{v['unit']}" for s in ('top','right','bottom','left'))
BP = {'': None, '_laptop': 1366, '_tablet': 1024, '_mobile': 767}
out = []
def rule(bp, sel, decl):
    decl = ';'.join(x + ' !important' for x in decl.split(';') if x)
    r = f'{sel}{{{decl}}}'
    out.append(r if not BP[bp] else f'@media (max-width:{BP[bp]}px){{{r}}}')
s = S('230262f0'); sel = P + MAP['230262f0']
for bp in BP:
    if 'padding' + bp in s:
        v = s['padding' + bp]; rule(bp, sel, ';'.join(f"--padding-{k}:{v[k]}px" for k in ('top','right','bottom','left')))
    if 'flex_gap' + bp in s:
        v = s['flex_gap' + bp]; rule(bp, sel, f"--gap:{v['row']}px {v['column']}px;--row-gap:{v['row']}px;--column-gap:{v['column']}px")
rule('', sel, f"--content-width:{s['boxed_width']['size']}px;background-color:{s['background_color']}")
rule('', P + MAP['644daf6c'], f"background-color:{S('644daf6c')['background_color']}")
def typo(i):
    s = S(i); sel = P + MAP[i] + ' .elementor-heading-title' if E[i]['widgetType'] == 'heading' else P + MAP[i]
    col = s.get('title_color') or s.get('text_color')
    rule('', sel, f"color:{col}")
    for bp in BP:
        d = []
        if bp == '':
            d += [f"font-family:'{s['typography_font_family']}',sans-serif", f"font-weight:{s['typography_font_weight']}"]
            d.append(f"text-transform:{s.get('typography_text_transform','none')}")
        for k, css_k in (('typography_font_size','font-size'), ('typography_line_height','line-height'), ('typography_letter_spacing','letter-spacing')):
            if k + bp in s:
                v = s[k + bp]; d.append(f"{css_k}:{v['size']}{v['unit'] if v['unit']!='em' or css_k!='line-height' else 'em'}")
        if d: rule(bp, sel, ';'.join(d))
        if '_margin' + bp in s:
            rule(bp, P + MAP[i] + ' > .elementor-widget-container', f"margin:{box(s['_margin'+bp])}")
for i in ('6fe388ac','681cf146','5bdc1bce'): typo(i)
# letter-spacing que el estilo no define en el título: Elementor no lo pone
rule('', P + MAP['681cf146'] + ' .elementor-heading-title', 'letter-spacing:normal;text-wrap:wrap')
rule('', P + MAP['5bdc1bce'], "font-family:'Inter',sans-serif;font-weight:400")
# CSS personalizado nuevo de la sección (va después del viejo, que queda pisado)
cc = S('230262f0')['custom_css'].replace('selector', P + MAP['230262f0'])
cc += '\n@media (min-width:768px) and (max-width:1366px){' + P + MAP['230262f0'] + ' .ak-dk{display:inline}}'

FONTS = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@400;600;700&family=Barlow:wght@400;700;800&display=swap'
page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Testimonios adaptado</title><link rel="stylesheet" href="{FONTS}">
<style>{css}</style><style>{chr(10).join(out)}
{cc}
html,body{{margin:0;background:#FDFCFB!important}}</style></head>
<body class="elementor-default elementor-kit-5 e--ua-blink e--ua-chrome e--ua-webkit">
<div data-elementor-id="93575" class="elementor elementor-93575">{sec}</div>
</body></html>'''
open(W + '_artifact_tes/seccion.html', 'w', encoding='utf-8').write(page)
print(len(page), len(out))

# para el Artifact: la imagen de portada incrustada (el visor bloquea imágenes de otros dominios)
import base64
b64 = base64.b64encode(open(W + 'imagenes/Frame-252.webp', 'rb').read()).decode()
art = page.replace('https://grupogoberna.com/wp-content/uploads/2026/10/Frame-252.webp', 'data:image/webp;base64,' + b64)
open(W + '_artifact_tes/seccion.html', 'w', encoding='utf-8').write(art)
print('artifact', len(art))
