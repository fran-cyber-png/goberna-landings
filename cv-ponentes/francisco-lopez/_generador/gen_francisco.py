import base64, json, os, random, re

P = r'C:\Users\Consultoría\Documents\cv-ponentes\francisco-lopez'
TPL = r'C:\Users\Consultoría\AppData\Local\Temp\claude\C--Users-Consultor-a-Documents-cv-ponentes\4557f3d6-2c21-49e4-8d5c-886b5592b83e\scratchpad\francisco-tpl.html'
OUT = os.path.join(P, 'francisco-lopez.json')
BIB = 'https://grupogoberna.com/wp-content/uploads/2026/10/'
MARCO, FOTO, LOGO = BIB + 'fondo-hero-marco.webp', BIB + 'foto-francisco.webp', BIB + 'logo-goberna.webp'
GOLD, INK, LINE = '#d6a752', '#030a22', '#e3e7ee'

def du(n):
    return 'data:image/webp;base64,' + base64.b64encode(open(os.path.join(P, 'iconos-webp', n + '.webp'), 'rb').read()).decode()

I = {k: du(k) for k in ['icono-criminologia', 'icono-investigacion', 'icono-consultoria', 'icono-inteligencia',
                        'icono-resumen', 'icono-titulo-cargos', 'icono-formacion', 'icono-aportes', 'vineta', 'vineta-grande',
                        'barra-especialidades-desk', 'barra-especialidades-movil']}

def u(n): return f'calc(var(--u)*{n})'
def m(n): return f'calc(var(--m)*{n})'
def L(x): return f'calc(50% + var(--u)*{x-960})'
def ML(x): return f'calc(50% + var(--m)*{x-215})'

# ---------- contenido: mismo texto que la vista previa aprobada ----------
T = open(TPL, encoding='utf-8').read()
def clean(s):
    s = re.sub(r'\s+', ' ', s).strip()
    return s
res_d = clean(re.search(r"<div class=\"blk resumen-d\".*?<p>(.*?)</p>", T, re.S).group(1))
res_m = clean(re.search(r"<div class=\"blk-m resumen-m\".*?<p>(.*?)</p>", T, re.S).group(1))
uls = re.findall(r'<ul class="list-[dm][^"]*"[^>]*>(.*?)</ul>', T, re.S)
assert len(uls) == 6, len(uls)
def items(ul):
    out = []
    for li in re.findall(r'<li[^>]*>(.*?)</li>', ul, re.S):
        li = re.sub(r'<img[^>]*>', '', li)
        li = re.sub(r'</?span>', '', li)
        out.append(clean(li))
    return ''.join(f'<li>{x}</li>' for x in out)
LD = [items(x) for x in uls[:3]]
LM = [items(x) for x in uls[3:]]

# ---------- utilidades de Elementor ----------
IDS = set()
def rid():
    while True:
        s = ''.join(random.choices('0123456789abcdef', k=8))
        if s not in IDS:
            IDS.add(s); return s
def pad0(): return {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
def cont(cls, kids=(), inner=True):
    s = {"content_width": "full", "flex_direction": "column", "flex_wrap": "nowrap", "flex_align_items": "stretch",
         "flex_gap": {"unit": "px", "column": "0", "row": "0", "isLinked": True, "size": 0},
         "padding": pad0(), "css_classes": cls}
    return {"id": rid(), "elType": "container", "settings": s, "elements": list(kids), "isInner": inner}
def wid(kind, cls, settings):
    s = dict(settings); s["_css_classes"] = cls
    return {"id": rid(), "elType": "widget", "settings": s, "elements": [], "widgetType": kind}
def h(text, level, cls): return wid('heading', cls, {"title": text, "header_size": level})
def tx(html, cls): return wid('text-editor', cls, {"editor": html})
def im(url, cls): return wid('image', cls, {"image": {"url": url, "id": 0, "source": "library", "size": ""}, "image_size": "full"})

# ---------- escritorio ----------
D_HERO = cont('ak-d-hero', [
    cont('ak-d-logo', [im(LOGO, 'ak-d-logo-img')]),
    cont('ak-d-name', [h('FRANCISCO', 'h1', 'ak-d-n1'), h('LÓPEZ', 'h1', 'ak-d-n2'),
                       tx('<p>Doctor en Criminología y detective privado habilitado</p>', 'ak-d-sub')]),
    cont('ak-d-foto', [im(FOTO, 'ak-d-foto-img')]),
    cont('ak-d-esp', [
        tx('<p>Especialidades</p>', 'ak-d-esp-lbl'),
        cont('ak-d-row', [
            cont('ak-d-it ak-d-it-1', [cont('ak-d-ico ak-d-ico-1'), tx('<p>Criminología</p>', 'ak-d-it-t')]), cont('ak-d-sep'),
            cont('ak-d-it ak-d-it-2', [cont('ak-d-ico ak-d-ico-2'), tx('<p>Investigación Privada</p>', 'ak-d-it-t')]), cont('ak-d-sep'),
            cont('ak-d-it ak-d-it-3', [cont('ak-d-ico ak-d-ico-3'), tx('<p>Consultoría de Seguridad</p>', 'ak-d-it-t')]), cont('ak-d-sep'),
            cont('ak-d-it ak-d-it-4', [cont('ak-d-ico ak-d-ico-4'), tx('<p>Inteligencia Aplicada</p>', 'ak-d-it-t')]),
        ]),
    ]),
])

def dstat(big, small):
    return cont('ak-d-stat', [h(big, 'h3', 'ak-d-big'), tx(f'<p>{small}</p>', 'ak-d-small')])

D_BODY = cont('ak-d-body', [
    cont('ak-d-card', [
        cont('ak-d-cols', [
            cont('ak-d-main', [
                cont('ak-d-res', [h('RESUMEN EJECUTIVO', 'h2', 'ak-d-h ak-d-h-res'), tx(f'<p>{res_d}</p>', 'ak-d-res-p')]),
                cont('ak-d-hr'),
                cont('ak-d-cargo', [h('CARGOS PRINCIPALES Y TRAYECTORIA', 'h2', 'ak-d-h ak-d-h-cargo'), tx(f'<ul>{LD[0]}</ul>', 'ak-d-list')]),
                cont('ak-d-hr'),
                cont('ak-d-form', [h('FORMACIÓN ACADÉMICA', 'h2', 'ak-d-h ak-d-h-form'), tx(f'<ul>{LD[1]}</ul>', 'ak-d-list')]),
                cont('ak-d-hr'),
                cont('ak-d-apor', [h('APORTES DESTACADOS Y PUBLICACIONES', 'h2', 'ak-d-h ak-d-h-apor'),
                                   tx(f'<ul>{LD[2]}</ul>', 'ak-d-list ak-d-arrow')]),
            ]),
            cont('ak-d-stats', [cont('ak-d-stats-in', [dstat('Doctor', 'Criminología – Universidad de Granada'),
                                dstat('Desde 2007', 'Investigación privada y servicios de seguridad'),
                                dstat('3 Másteres', 'Crimen, Ciberinteligencia y Seguridad Internacional')])]),
        ]),
    ]),
])
# sticky nativo de Elementor (como en Diana): solo desktop y laptop, dentro de ak-d-cols
D_BODY['elements'][0]['elements'][0]['elements'][1]['settings'].update({
    'sticky': 'top', 'sticky_on': ['desktop', 'laptop'], 'sticky_offset': 54, 'sticky_offset_laptop': 38, 'sticky_parent': 'yes'})
D_BODY['elements'][0]['elements'][0]['settings']['flex_direction'] = 'row'

def hero_bg(c, xpos):
    c['settings'].update({'background_background': 'classic', 'background_color': '#06101F',
        'background_image': {'url': MARCO, 'id': 0, 'size': '', 'alt': '', 'source': 'library'},
        'background_position': 'initial', 'background_xpos': {'unit': '%', 'size': xpos, 'sizes': []},
        'background_ypos': {'unit': '%', 'size': 50, 'sizes': []}, 'background_repeat': 'no-repeat', 'background_size': 'cover'})
hero_bg(D_HERO, 50)

# ---------- móvil ----------
M_HERO = cont('ak-m-hero', [
    cont('ak-m-logo', [im(LOGO, 'ak-m-logo-img')]),
    cont('ak-m-name', [h('FRANCISCO', 'h1', 'ak-m-n1'), h('LÓPEZ', 'h1', 'ak-m-n2')]),
    tx('<p>Doctor en Criminología y detective privado habilitado</p>', 'ak-m-sub'),
    cont('ak-m-esp', [
        tx('<p>Especialidades</p>', 'ak-m-esp-lbl'),
        cont('ak-m-grid', [
            cont('ak-m-cell ak-m-it-1', [cont('ak-m-ico ak-m-ico-1'), tx('<p>Criminología</p>', 'ak-m-cell-t')]),
            cont('ak-m-cell ak-m-it-2', [cont('ak-m-ico ak-m-ico-2'), tx('<p>Investigación Privada</p>', 'ak-m-cell-t')]),
            cont('ak-m-cell ak-m-it-3', [cont('ak-m-ico ak-m-ico-3'), tx('<p>Consultoría de Seguridad</p>', 'ak-m-cell-t')]),
            cont('ak-m-cell ak-m-it-4', [cont('ak-m-ico ak-m-ico-4'), tx('<p>Inteligencia Aplicada</p>', 'ak-m-cell-t')]),
        ]),
    ]),
    cont('ak-m-foto', [im(FOTO, 'ak-m-foto-img')]),
])

def mstat(big, small):
    return cont('ak-m-stat', [h(big, 'h3', 'ak-m-big'), tx(f'<p>{small}</p>', 'ak-m-small')])

M_BODY = cont('ak-m-body', [
    cont('ak-m-card', [
        cont('ak-m-res', [h('RESUMEN EJECUTIVO', 'h2', 'ak-m-h ak-m-h-res'), tx(f'<p>{res_m}</p>', 'ak-m-res-p'),
                          cont('ak-m-stats', [mstat('Doctor', 'Criminología – Universidad de Granada'),
                                              mstat('Desde 2007', 'Investigación privada y servicios de seguridad'),
                                              mstat('3 Másteres', 'Crimen, Ciberinteligencia y Seguridad Internacional')])]),
        cont('ak-m-hr ak-m-hr1'),
        cont('ak-m-cargo', [h('CARGOS PRINCIPALES Y TRAYECTORIA', 'h2', 'ak-m-h ak-m-h-cargo'), tx(f'<ul>{LM[0]}</ul>', 'ak-m-list')]),
        cont('ak-m-hr ak-m-hr2'),
        cont('ak-m-form', [h('FORMACIÓN ACADÉMICA', 'h2', 'ak-m-h ak-m-h-form'), tx(f'<ul>{LM[1]}</ul>', 'ak-m-list')]),
        cont('ak-m-hr ak-m-hr3'),
        cont('ak-m-apor', [h('APORTES DESTACADOS Y PUBLICACIONES', 'h2', 'ak-m-h ak-m-h-apor'),
                           tx(f'<ul>{LM[2]}</ul>', 'ak-m-list ak-m-arrow')]),
    ]),
])

hero_bg(M_HERO, 40)

# cargas de fuentes: widgets ocultos (como en la plantilla de Diana)
FONTS = cont('ak-fonts', [
    h('Montserrat', 'p', ''), h('Montserrat', 'p', ''),
    tx('<p>Open Sans</p>', ''), tx('<p>Open Sans</p>', ''),
])
FONTS['elements'][0]['settings'].update({"typography_typography": "custom", "typography_font_family": "Montserrat", "typography_font_weight": "800"})
FONTS['elements'][1]['settings'].update({"typography_typography": "custom", "typography_font_family": "Montserrat", "typography_font_weight": "700"})
FONTS['elements'][2]['settings'].update({"typography_typography": "custom", "typography_font_family": "Open Sans", "typography_font_weight": "400"})
FONTS['elements'][3]['settings'].update({"typography_typography": "custom", "typography_font_family": "Open Sans", "typography_font_weight": "700"})

# ---------- CSS ----------
CSS = f'''
selector {{ --u: min(1px, calc(100vw / 1920)); --m: min(1px, calc(100vw / 430)); }}
selector .ak-fonts {{ display: none; }}
selector .elementor-widget-heading .elementor-heading-title, selector .elementor-widget-text-editor p {{ margin: 0; }}
selector .ak-d-hero, selector .ak-m-hero, selector .ak-d-body, selector .ak-m-body {{ width: 100%; }}
/* ===== ESCRITORIO (1920 de diseño, escala con --u) ===== */
selector .ak-d-hero {{ position: relative; height: {u(850)}; overflow: hidden; }}
selector .ak-d-logo {{ position: absolute; left: {L(200)}; top: {u(101)}; width: {u(184)}; height: {u(47)}; }}
selector .ak-d-logo img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
selector .ak-d-name {{ position: absolute; left: {L(200)}; top: {u(192)}; width: {u(820)}; }}
selector .ak-d-n1 .elementor-heading-title {{ font: 800 {u(64)} / 0.964 'Montserrat', Arial, sans-serif; color: {GOLD}; letter-spacing: {u(2.56)}; }}
selector .ak-d-n2 .elementor-heading-title {{ font: 800 {u(87)} / 0.964 'Montserrat', Arial, sans-serif; color: #fff; }}
selector .ak-d-sub p {{ font: 400 {u(28)} / {u(48)} 'Open Sans', Arial, sans-serif; color: #fff; margin-top: {u(16)} !important; }}
selector .ak-d-foto {{ position: absolute; left: {L(947)}; top: {u(101)}; width: {u(773)}; height: {u(749)}; overflow: hidden; }}
selector .ak-d-foto-img, selector .ak-m-foto-img {{ position: absolute !important; left: -5.05%; top: -13.5%; width: 114.62% !important; height: 141.95%; max-width: none !important; margin: 0 !important; }}
selector .ak-d-foto-img .elementor-widget-container, selector .ak-m-foto-img .elementor-widget-container {{ width: 100%; height: 100%; }}
selector .ak-d-foto-img img, selector .ak-m-foto-img img {{ width: 100% !important; height: 100% !important; max-width: none !important; object-fit: cover; display: block; }}
selector .ak-d-esp {{ position: absolute; left: {L(200)}; top: {u(536)}; width: {u(820)}; height: {u(170)}; background: url({I['barra-especialidades-desk']}) 0 0 / 100% 100% no-repeat; }}
selector .ak-d-esp-lbl {{ position: absolute; left: {u(29)}; top: {u(-14)}; }}
selector .ak-d-esp-lbl p {{ font: 400 {u(25)} / 1.2 'Montserrat', Arial, sans-serif; color: {GOLD}; padding: 0 {u(10)}; }}
selector .ak-d-row {{ position: absolute; left: {u(29)}; top: {u(41)}; display: flex; flex-direction: row; align-items: flex-start; gap: {u(20)}; }}
selector .ak-d-it {{ width: {u(160)}; flex: none; display: flex; flex-direction: column; align-items: center; gap: {u(8)}; }}
selector .ak-d-ico {{ flex: none; width: 100%; height: {u(36)}; background: no-repeat center / auto {u(36)}; }}
selector .ak-d-ico-1 {{ background-image: url({I['icono-criminologia']}); }}
selector .ak-d-ico-2 {{ background-image: url({I['icono-investigacion']}); }}
selector .ak-d-ico-3 {{ background-image: url({I['icono-consultoria']}); }}
selector .ak-d-ico-4 {{ background-image: url({I['icono-inteligencia']}); }}
selector .ak-d-it-t p {{ font: 400 {u(18)} / {u(24)} 'Open Sans', Arial, sans-serif; color: #fff; text-align: center; }}
selector .ak-d-sep {{ flex: none; width: {u(1)}; height: {u(48)}; margin-top: {u(34)}; background: rgba(214,167,82,.7); }}
selector .ak-d-h .elementor-heading-title {{ display: flex; align-items: center; gap: {u(14)}; height: {u(88)}; font: 700 {u(26)} / 1 'Montserrat', Arial, sans-serif; color: {GOLD}; text-transform: uppercase; margin: 0; }}
selector .ak-d-h .elementor-heading-title::before {{ content: ""; flex: none; height: {u(36)}; background: no-repeat center / contain; }}
selector .ak-d-h-res .elementor-heading-title::before {{ width: {u(35)}; background-image: url({I['icono-resumen']}); }}
selector .ak-d-h-cargo .elementor-heading-title::before {{ width: {u(45)}; background-image: url({I['icono-titulo-cargos']}); }}
selector .ak-d-h-form .elementor-heading-title::before {{ width: {u(30)}; background-image: url({I['icono-formacion']}); }}
selector .ak-d-h-apor .elementor-heading-title::before {{ width: {u(39)}; background-image: url({I['icono-aportes']}); }}
selector .ak-d-res-p p {{ margin: 0 0 0 {u(62)}; width: {u(753)}; font: 400 {u(18)} / {u(34)} 'Open Sans', Arial, sans-serif; color: {INK}; }}
selector .ak-d-res-p b, selector .ak-d-list b {{ font-weight: 700; }}
selector .ak-d-list ul {{ list-style: none; margin: 0 0 0 {u(61)}; padding: 0; width: {u(750)}; }}
selector .ak-d-list li {{ position: relative; padding-left: {u(18)}; margin-bottom: {u(20)}; font: 400 {u(18)} / {u(28)} 'Open Sans', Arial, sans-serif; color: {INK}; }}
selector .ak-d-list li:last-child {{ margin-bottom: 0; }}
selector .ak-d-list li::before {{ content: ""; position: absolute; left: 0; top: 0; width: {u(8)}; height: {u(28)}; background: url({I['vineta']}) center / contain no-repeat; }}
selector .ak-d-arrow li::before {{ width: {u(18)}; background-image: url({I['vineta-grande']}); }}
selector .ak-d-stat {{ margin-bottom: {u(39)}; }}
selector .ak-d-body {{ display: flex; flex-direction: column; align-items: center; padding: {u(80)} 0 {u(80)} 0 !important; background: #f3f6fa; }}
selector .ak-d-card {{ width: {u(1519)} !important; max-width: none; box-sizing: border-box; padding: {u(54)} {u(95)} {u(82)} {u(81)} !important; background: #fff; border-radius: {u(20)}; box-shadow: 0 3px 16px rgba(6,8,26,.16); }}
selector .ak-d-cols {{ display: flex; flex-direction: row; align-items: flex-start; gap: {u(79)} !important; width: 100%; padding: 0 !important; }}
selector .ak-d-main {{ flex: none; width: {u(812)} !important; padding: 0 !important; }}
selector .ak-d-stats {{ flex: none; width: {u(452)} !important; margin: 0 !important; padding: {u(27)} 0 0 0 !important; }}
selector .ak-d-stats-in {{ width: 100%; box-sizing: border-box; padding: {u(7)} 0 {u(8)} {u(79)} !important; border-left: 1px solid {GOLD}; }}
selector .ak-d-hr {{ width: 100%; height: 1px; margin: {u(25)} 0; background: {LINE}; }}
selector .ak-d-big .elementor-heading-title {{ font: 800 {u(37)} / 1.1 'Montserrat', Arial, sans-serif; color: {INK}; }}
selector .ak-d-small p {{ font: 400 {u(18)} / {u(22)} 'Open Sans', Arial, sans-serif; color: {INK}; }}
/* ===== MÓVIL (430 de diseño, escala con --m) ===== */
selector .ak-m-hero {{ position: relative; height: {m(931)}; overflow: hidden; }}
selector .ak-m-logo {{ position: absolute; left: {ML(24)}; top: {m(36)}; width: {m(120)}; height: {m(31)}; }}
selector .ak-m-logo img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
selector .ak-m-name {{ position: absolute; left: {ML(24)}; top: {m(95)}; width: {m(382)}; }}
selector .ak-m-n1 .elementor-heading-title {{ font: 800 {m(36)} / 0.964 'Montserrat', Arial, sans-serif; color: {GOLD}; letter-spacing: {m(1)}; }}
selector .ak-m-n2 .elementor-heading-title {{ font: 800 {m(36)} / 0.964 'Montserrat', Arial, sans-serif; color: #fff; }}
selector .ak-m-sub {{ position: absolute; left: {ML(24)}; top: {m(181)}; width: {m(382)}; }}
selector .ak-m-sub p {{ font: 400 {m(16)} / {m(28)} 'Open Sans', Arial, sans-serif; color: #fff; }}
selector .ak-m-esp {{ position: absolute; left: {ML(24)}; top: {m(298)}; width: {m(382)}; height: {m(181)}; background: url({I['barra-especialidades-movil']}) 0 0 / 100% 100% no-repeat; }}
selector .ak-m-esp-lbl {{ position: absolute; left: {m(19)}; top: {m(-13)}; }}
selector .ak-m-esp-lbl p {{ font: 400 {m(16)} / 1.2 'Montserrat', Arial, sans-serif; color: {GOLD}; padding: 0 {m(10)}; }}
selector .ak-m-grid {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; box-sizing: border-box; padding: {m(20)} {m(12)}; display: flex; flex-direction: row; flex-wrap: wrap; }}
selector .ak-m-cell {{ width: 50%; height: 50%; box-sizing: border-box; flex: none; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: {m(4)}; }}
selector .ak-m-ico {{ flex: none; width: 100%; height: {m(23)}; background: no-repeat center / auto {m(23)}; }}
selector .ak-m-ico-1 {{ background-image: url({I['icono-criminologia']}); }}
selector .ak-m-ico-2 {{ background-image: url({I['icono-investigacion']}); }}
selector .ak-m-ico-3 {{ background-image: url({I['icono-consultoria']}); }}
selector .ak-m-ico-4 {{ background-image: url({I['icono-inteligencia']}); }}
selector .ak-m-cell-t p {{ font: 400 {m(14)} / {m(18)} 'Open Sans', Arial, sans-serif; color: #fff; text-align: center; }}
selector .ak-m-foto {{ position: absolute; left: {ML(8)}; top: {m(542)}; width: {m(415)}; height: {m(389)}; overflow: hidden; }}
selector .ak-m-body {{ position: relative; height: {m(5767)}; background: #f3f6fa; }}
selector .ak-m-card {{ position: absolute; left: calc(50% + var(--m)*-195); top: {m(20)}; width: {m(390)}; height: {m(4796)}; background: #fff; border-radius: {m(16)}; box-shadow: 0 3px 16px rgba(6,8,26,.16); }}
selector .ak-m-res {{ position: absolute; left: 0; top: {m(51)}; width: {m(350)}; }}
selector .ak-m-cargo {{ position: absolute; left: 0; top: {m(1279)}; width: {m(350)}; }}
selector .ak-m-form {{ position: absolute; left: 0; top: {m(2348)}; width: {m(350)}; }}
selector .ak-m-apor {{ position: absolute; left: 0; top: {m(3393)}; width: {m(350)}; }}
selector .ak-m-hr {{ position: absolute; left: 0; width: {m(350)}; height: 1px; background: {LINE}; }}
selector .ak-m-hr1 {{ top: {m(1229)}; }}
selector .ak-m-hr2 {{ top: {m(2298)}; }}
selector .ak-m-hr3 {{ top: {m(3343)}; }}
selector .ak-m-h .elementor-heading-title {{ display: flex; align-items: center; gap: {m(12)}; font: 700 {m(22)} / {m(30)} 'Montserrat', Arial, sans-serif; color: {GOLD}; text-transform: uppercase; margin: 0; height: {m(99)}; }}
selector .ak-m-h .elementor-heading-title::before {{ content: ""; flex: none; height: {m(30)}; background: no-repeat center / contain; }}
selector .ak-m-h-res .elementor-heading-title {{ height: {m(66)}; }}
selector .ak-m-h-res .elementor-heading-title::before {{ width: {m(29)}; background-image: url({I['icono-resumen']}); }}
selector .ak-m-h-cargo .elementor-heading-title::before {{ width: {m(38)}; background-image: url({I['icono-titulo-cargos']}); }}
selector .ak-m-h-form .elementor-heading-title::before {{ width: {m(25)}; background-image: url({I['icono-formacion']}); }}
selector .ak-m-h-apor .elementor-heading-title::before {{ width: {m(33)}; background-image: url({I['icono-aportes']}); }}
selector .ak-m-res-p p {{ margin: 0; width: {m(350)}; font: 400 {m(16)} / {m(26)} 'Open Sans', Arial, sans-serif; color: {INK}; }}
selector .ak-m-res-p b, selector .ak-m-list b {{ font-weight: 700; }}
selector .ak-m-stats {{ margin: {m(28)} 0 0 {m(20)}; width: {m(312)}; }}
selector .ak-m-stat {{ margin-bottom: {m(22)}; }}
selector .ak-m-big .elementor-heading-title {{ font: 800 {m(28)} / 1.1 'Montserrat', Arial, sans-serif; color: {INK}; }}
selector .ak-m-small p {{ font: 400 {m(15)} / {m(22)} 'Open Sans', Arial, sans-serif; color: {INK}; }}
selector .ak-m-list {{ margin-top: {m(29)}; }}
selector .ak-m-list ul {{ list-style: none; margin: 0 0 0 {m(19)}; padding: 0; width: {m(331)}; }}
selector .ak-m-list li {{ position: relative; padding-left: {m(16)}; margin-bottom: {m(17)}; font: 400 {m(16)} / {m(26)} 'Open Sans', Arial, sans-serif; color: {INK}; }}
selector .ak-m-list li:last-child {{ margin-bottom: 0; }}
selector .ak-m-list li::before {{ content: ""; position: absolute; left: 0; top: 0; width: {m(6)}; height: {m(26)}; background: url({I['vineta']}) center / contain no-repeat; }}
selector .ak-m-arrow li::before {{ width: {m(18)}; height: {m(28)}; background-image: url({I['vineta-grande']}); }}
/* ===== cambio de versión ===== */
@media (max-width: 1024px) {{
  selector .ak-d-hero, selector .ak-d-body {{ display: none; }}
}}
@media (min-width: 1025px) {{
  selector .ak-m-hero, selector .ak-m-body {{ display: none; }}
}}
'''

root = {
    "id": rid(), "elType": "container",
    "settings": {"content_width": "full", "flex_direction": "column", "flex_wrap": "nowrap", "flex_align_items": "stretch",
                 "flex_gap": {"unit": "px", "column": "0", "row": "0", "isLinked": True, "size": 0},
                 "padding": pad0(), "css_classes": "ak-fr", "custom_css": CSS.strip()},
    "elements": [FONTS, D_HERO, D_BODY, M_HERO, M_BODY],
    "isInner": False,
}
doc = {"content": [root], "page_settings": [], "version": "0.4", "title": "Francisco José López", "type": "container"}
json.dump(doc, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', OUT, os.path.getsize(OUT), 'bytes; ids', len(IDS))
