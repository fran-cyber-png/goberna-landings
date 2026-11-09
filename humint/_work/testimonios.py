# Sección «Testimonios en video» (de asesor-presidencial) con los tokens de Carrera Diplomática.
# Toma la tipografía y los espacios de Metodología (3f83c2c) y cambia el dorado por el rojo #DD0005.
# La imagen de fondo del cuadro del video (Frame-203.webp) y el video quedan igual: se reemplazan a mano.
# Uso: python _work/testimonios.py  ->  testimonios-video-carrera-diplomatica.json
import json, os, re, copy

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SRC = r'C:\Users\Consultoría\Documents\asesor-presidencial\secciones\13-testimonios-video.json'
DST = os.path.join(ROOT, 'testimonios-video-carrera-diplomatica.json')

RED, DARK, BODY, LIGHT_BG = '#DD0005', '#0C0000', 'rgba(6,6,6,0.75)', '#FDFCFB'
J = json.load(open(SRC, encoding='utf-8'))
sec = J['content'][0]
E = {}
def idx(e):
    e.pop('htmlCache', None)   # caché del HTML renderizado con los estilos viejos (Elementor lo regenera)
    E[e['id']] = e
    for c in e.get('elements', []): idx(c)
idx(sec)
S = lambda i: E[i]['settings']
px = lambda v: {'unit': 'px', 'size': v, 'sizes': []}
em = lambda v: {'unit': 'em', 'size': v, 'sizes': []}
box = lambda t, r, b, l: {'unit': 'px', 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': False}

def sub(s, old, new, n=None):
    c = s.count(old)
    assert c and (n is None or c == n), (c, old[:70])
    return s.replace(old, new)

# ---- sección: mismos espacios y fondo que Metodología
s = S('1cbc8be7')
assert s['css_classes'] == 'ak-vsec'
s.update(background_color=LIGHT_BG, padding=box(63, 40, 119, 40), padding_laptop=box(64, 80, 64, 80),
         padding_tablet=box(56, 32, 56, 32), padding_mobile=box(56, 16, 56, 16))
cc = s['custom_css']
cc = sub(cc, 'estilo de la otra landing (dorado de 3 tonos, Barlow)', 'tokens de Carrera Diplomática (rojo #DD0005, Montserrat e Inter)', 1)
# antetítulo y parte destacada del título: rojo plano
cc = sub(cc, 'selector .ak-oro-text .elementor-heading-title, selector .ak-g { background-image: linear-gradient(to bottom right, #CB861B 0%, #F5C02F 50%, #CB861B 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }',
         'selector .ak-vh2 .ak-g { color: %s; }' % RED, 1)
cc = cc.replace('linear-gradient(to bottom right, #CB861B 0%, #F5C02F 50%, #CB861B 100%) 1', 'linear-gradient(%s, %s) 1' % (RED, RED))
cc = cc.replace('linear-gradient(to bottom right, #CB861B 0%, #F5C02F 50%, #CB861B 100%)', RED)
cc = cc.replace('rgba(203,134,27,.45)', 'rgba(221,0,5,.45)').replace('#CB861B', RED)
# miniaturas en mobile: el margen negativo sigue el gutter de 16 px de la landing (antes 24)
cc = sub(cc, 'margin-left: -24px !important; margin-right: -24px !important;', 'margin-left: -16px !important; margin-right: -16px !important;', 1)
cc = sub(cc, 'padding-left: 24px !important; padding-right: 24px !important; width: calc(100% + 48px)', 'padding-left: 16px !important; padding-right: 16px !important; width: calc(100% + 32px)', 1)
cc = sub(cc, 'scroll-margin-left: 24px;', 'scroll-margin-left: 16px;', 1)
assert not re.search(r'CB861B|F5C02F|203,134,27|Barlow', cc), 'quedó dorado o Barlow en el CSS de la sección'
s['custom_css'] = cc

# ---- cuadro del video: la imagen se queda (se cambia a mano); el color de fondo pasa al oscuro de la landing
p = S('14570d4d')
assert p['css_classes'] == 'ak-vp' and p['background_image']['url'].endswith('Frame-203.webp')
p['background_color'] = DARK

# ---- reproductor (widget HTML): dorado -> rojo, fondo oscuro de la landing, ícono de play blanco sobre rojo
h = S('7ec20134')['html']
h = h.replace('background:#1B2333', 'background:' + DARK)
h = h.replace('linear-gradient(90deg,#CB861B,#F5C02F,#CB861B)', RED)
h = h.replace('linear-gradient(to bottom right, #CB861B 0%, #F5C02F 50%, #CB861B 100%)', RED)
h = h.replace('rgba(203,134,27,', 'rgba(221,0,5,').replace('#CB861B', RED)
h = sub(h, '.ak-vp .ak-vbig svg{width:34px;height:34px;margin-left:5px;fill:#060606}', '.ak-vp .ak-vbig svg{width:34px;height:34px;margin-left:5px;fill:#FFFFFF}', 1)
# video: el <video> necesita el .mp4 directo (/public/), no el enlace /embed/ (esa es una página HTML del reproductor)
h = sub(h, 'var VIDEOS=["https://cms.goberna.club/public/oscar_rocha_chavez.mp4"];',
        'var VIDEOS=["https://cms.goberna.club/public/testimonio_jaime.mp4"];', 1)
# editor de Elementor: al tocar el widget se vuelve a dibujar su HTML pero la sección sigue igual.
# Antes la marca de «iniciado» iba en la sección, así que el reproductor nuevo quedaba sin conectar (el video no salía).
# Ahora la marca va en cada reproductor y los eventos del cuadro se asignan (no se acumulan).
h = sub(h, 'function init(sec){\n if(sec.getAttribute("data-akv"))return;sec.setAttribute("data-akv","1");\n var m=sec.querySelector(".ak-vp"),pl=sec.querySelector(".ak-vplayer");if(!m||!pl)return;',
        'function init(pl){\n if(pl.getAttribute("data-akv"))return;\n var m=pl.closest(".ak-vp"),sec=pl.closest(".ak-vsec");if(!m||!sec)return;pl.setAttribute("data-akv","1");m.classList.remove("ak-on");', 1)
h = sub(h, ' var dots=document.createElement("div");', ' [].forEach.call(sec.querySelectorAll(".ak-vdots"),function(d){d.remove()});\n var dots=document.createElement("div");', 1)
h = sub(h, 'if(!ths.length)m.addEventListener("click",function(){if(!m.classList.contains("ak-on"))go(0)});',
        'if(!ths.length)m.onclick=function(){if(!m.classList.contains("ak-on"))go(0)};', 1)
h = sub(h, 'm.addEventListener("dragstart",function(e){e.preventDefault()});\n m.addEventListener("pointerdown",function(e){sx=e.clientX;sy=e.clientY});',
        'm.ondragstart=function(e){e.preventDefault()};\n m.onpointerdown=function(e){sx=e.clientX;sy=e.clientY};', 1)
h = sub(h, 'function boot(){[].forEach.call(document.querySelectorAll(".ak-vsec"),init)}\nif(document.readyState!=="loading")boot();else document.addEventListener("DOMContentLoaded",boot);',
        'function boot(){[].forEach.call(document.querySelectorAll(".ak-vsec .ak-vplayer"),init)}\nif(document.readyState!=="loading")boot();else document.addEventListener("DOMContentLoaded",boot);\nsetTimeout(boot,0);setTimeout(boot,600);', 1)
# cada reproductor lleva su propio video en data-videos (antes un VIDEOS global: si en la página quedaba otra
# copia del script, la primera en correr ponía su video en todos los cuadros)
h = sub(h, '<div class="ak-vplayer">', '<div class="ak-vplayer" data-videos="https://cms.goberna.club/public/testimonio_jaime.mp4">', 1)
h = sub(h, '/* Videos en el mismo orden que las miniaturas */\nvar VIDEOS=["https://cms.goberna.club/public/testimonio_jaime.mp4"];\n', '', 1)
h = sub(h, 'var m=pl.closest(".ak-vp"),sec=pl.closest(".ak-vsec");if(!m||!sec)return;',
        'var m=pl.closest(".ak-vp"),sec=pl.closest(".ak-vsec");if(!m||!sec)return;\n /* Videos (separados por coma, en el orden de las miniaturas): atributo data-videos de .ak-vplayer */\n var VIDEOS=(pl.getAttribute("data-videos")||"").split(",").map(function(s){return s.trim()}).filter(Boolean);', 1)
# video horizontal (16:9): se ve entero (contain) sobre el fondo desenfocado, en vez de recortarse a 9:16
h = sub(h, '.ak-vbb{position:absolute;', '.ak-vplayer.ak-land video{left:0;transform:none;width:100%;aspect-ratio:auto;object-fit:contain;background:transparent;box-shadow:none}\n.ak-vbb{position:absolute;', 1)
h = sub(h, ' ["timeupdate","play","pause","loadedmetadata","volumechange"].forEach(function(e){v.addEventListener(e,ui)});',
        ' ["timeupdate","play","pause","loadedmetadata","volumechange"].forEach(function(e){v.addEventListener(e,ui)});\n v.addEventListener("loadedmetadata",function(){pl.classList.toggle("ak-land",v.videoWidth>v.videoHeight)});', 1)
# si el contenedor del cuadro o la sección no tienen las clases ak-vp / ak-vsec (sección armada a mano o
# pegada en otra estructura) el cuadro pierde su proporción y queda como una franja: el script se las pone
h = sub(h, 'var m=pl.closest(".ak-vp"),sec=pl.closest(".ak-vsec");if(!m||!sec)return;',
        'var w=pl.closest(".elementor-widget-html")||pl.parentNode,m=pl.closest(".ak-vp")||(w.parentNode&&w.parentNode.closest(".e-con,.elementor-column"));if(!m)return;m.classList.add("ak-vp");\n'
        ' var sec=m.closest(".ak-vsec")||(m.parentNode&&m.parentNode.closest(".e-con,.elementor-section"))||m.parentNode;sec.classList.add("ak-vsec");', 1)
h = sub(h, 'function boot(){[].forEach.call(document.querySelectorAll(".ak-vsec .ak-vplayer"),init)}',
        'function boot(){[].forEach.call(document.querySelectorAll(".ak-vplayer"),init)}', 1)
assert 'oscar_rocha' not in h
assert not re.search(r'CB861B|F5C02F|203,134,27|1B2333', h), 'quedó dorado en el reproductor'
S('7ec20134')['html'] = h

# ---- textos: mismos tokens que Metodología (antetítulo 77542da8, título b86c8ae, párrafo 390db8e4)
e = S('be55919')
e['_css_classes'] = 'ak-veye'
e.pop('_padding_mobile', None)
e.update(title_color=RED, typography_typography='custom', typography_font_family='Inter', typography_font_weight='400',
         typography_font_size=px(20), typography_font_size_laptop=px(16), typography_font_size_mobile=px(10),
         typography_line_height=em(1.2), typography_text_transform='uppercase',
         typography_letter_spacing=px(2), typography_letter_spacing_mobile=px(2))

t = S('68fabaf6')
t.pop('_padding_mobile', None)
t.update(title_color=DARK, typography_typography='custom', typography_font_family='Montserrat', typography_font_weight='700',
         typography_font_size=px(50), typography_font_size_laptop=px(35), typography_font_size_mobile=px(28),
         typography_line_height=px(57), typography_line_height_laptop=px(40), typography_line_height_mobile=px(32),
         typography_letter_spacing=px(-1.5), typography_letter_spacing_laptop=px(-1), typography_letter_spacing_mobile=px(-0.5),
         typography_text_transform='none',
         _margin=box(47, 0, 0, 0), _margin_laptop=box(36, 0, 0, 0), _margin_mobile=box(18, 0, 0, 0))
t['header_size'] = 'h2'

x = S('4b92c5aa')
x.pop('_padding_mobile', None)
x.pop('typography_line_height_mobile', None)
x.update(text_color=BODY, typography_typography='custom', typography_font_family='Inter', typography_font_weight='400',
         typography_font_size=px(18), typography_font_size_laptop=px(16), typography_font_size_mobile=px(14),
         typography_line_height=em(1.78), typography_letter_spacing=px(0.18),
         _margin=box(21, 0, 0, 0), _margin_laptop=box(20, 0, 0, 0), _margin_mobile=box(16, 0, 0, 0))

out = {'content': [sec], 'page_settings': [], 'version': '0.4', 'title': 'testimonios video carrera diplomatica', 'type': 'container'}
blob = json.dumps(out, ensure_ascii=False)
_left = re.findall(r".{60}(?:CB861B|F5C02F|203,134,27|Barlow|1B2333).{20}", blob); assert not _left, _left
open(DST, 'w', encoding='utf-8').write(blob)
print('escrito', DST, len(blob) // 1024, 'KB')
