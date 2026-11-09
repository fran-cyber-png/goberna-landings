import base64, json, os, random

S = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(S)
OUT = os.path.join(P, 'daniela-galvan.json')
BIB = 'https://grupogoberna.com/wp-content/uploads/2026/10/'
BG_D, BG_M = BIB + 'hero-fondo-capitolio.webp', BIB + 'hero-fondo-movil.webp'
FOTO, LOGO = BIB + 'daniela-galvan.webp', BIB + 'logo-goberna.webp'
GOLD, INK, LINE, NIGHT, BG = '#d6a752', '#030a22', '#e3e7ee', '#020715', '#f3f6fa'
MONT, OPEN, SORA, MANR = "'Montserrat', Arial, sans-serif", "'Open Sans', Arial, sans-serif", "'Sora', Arial, sans-serif", "'Manrope', Arial, sans-serif"

def du(n):
    return 'data:image/webp;base64,' + base64.b64encode(open(os.path.join(P, 'iconos-webp', n + '.webp'), 'rb').read()).decode()
I = {k: du(k) for k in ['icono-investigacion-criminal', 'icono-inteligencia-digital', 'icono-prevencion-ciberdelito',
                        'icono-osint-socmint', 'icono-resumen', 'icono-titulo-cargos', 'icono-formacion', 'icono-aportes',
                        'vineta', 'vineta-grande', 'vineta-movil', 'vineta-grande-movil',
                        'barra-especialidades-desk', 'barra-especialidades-movil']}

def u(n): return f'calc(var(--u)*{n})'
def m(n): return f'calc(var(--m)*{n})'
def L(x): return f'calc(50% + var(--u)*{x - 960})'
def ML(x): return f'calc(50% + var(--m)*{x - 215})'

# ---------- contenido (texto literal del Figma, guardado en el json de datos) ----------
D = json.load(open(os.path.join(P, 'daniela-galvan-datos.json'), encoding='utf-8'))
def lis(rows):
    return '<ul>' + ''.join(f'<li>{x}</li>' for x in rows) + '</ul>'
RES = f"<p><b>{D['resumen']['negrita']}</b>{D['resumen']['resto']}</p>"
CARGOS, FORM, APOR = lis(D['cargos']), lis(D['formacion']), lis(D['aportes'])
SUB_D = '<p>' + D['titular'] + '</p>'
SUB_M = SUB_D
ESP = D['especialidades_html']
STATS = [(b, s) for b, s in D['cifras']]

# ---------- utilidades de Elementor ----------
IDS = set()
def rid():
    while True:
        s = ''.join(random.choices('0123456789abcdef', k=8))
        if s not in IDS:
            IDS.add(s); return s
def pad0(): return {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
def cont(cls, kids=(), row=False):
    s = {"content_width": "full", "flex_direction": "row" if row else "column", "flex_wrap": "nowrap",
         "flex_align_items": "stretch", "flex_gap": {"unit": "px", "column": "0", "row": "0", "isLinked": True, "size": 0},
         "padding": pad0(), "css_classes": cls}
    return {"id": rid(), "elType": "container", "settings": s, "elements": list(kids), "isInner": True}
def wid(kind, cls, settings):
    s = dict(settings); s["_css_classes"] = cls
    return {"id": rid(), "elType": "widget", "settings": s, "elements": [], "widgetType": kind}
def h(text, level, cls): return wid('heading', cls, {"title": text, "header_size": level})
def tx(html, cls): return wid('text-editor', cls, {"editor": html})
def im(url, cls, alt): return wid('image', cls, {"image": {"url": url, "id": 0, "source": "library", "size": "", "alt": alt},
                                                 "image_size": "full"})
def hero_bg(c, url, pos):
    c['settings'].update({'background_background': 'classic', 'background_color': '#020715',
        'background_image': {'url': url, 'id': 0, 'size': '', 'alt': '', 'source': 'library'},
        'background_position': pos, 'background_repeat': 'no-repeat', 'background_size': 'cover'})

# ---------- DESKTOP / LAPTOP ----------
def d_item(n, text):
    return cont(f'ak-d-it', [cont(f'ak-d-ico ak-d-ico-{n}'), tx(f'<p>{text}</p>', 'ak-d-it-t')])
D_HERO = cont('ak-d-hero', [
    cont('ak-d-logo', [im(LOGO, 'ak-d-logo-img', 'Goberna')]),
    cont('ak-d-name', [h(D['nombre']['linea1'], 'h1', 'ak-d-n1'), h(D['nombre']['linea2'], 'h1', 'ak-d-n2'), tx(SUB_D, 'ak-d-sub')]),
    cont('ak-d-foto', [im(FOTO, 'ak-d-foto-img', 'Daniela Galvan')]),
    cont('ak-d-esp', [
        tx('<p>Especialidades</p>', 'ak-d-esp-lbl'),
        cont('ak-d-row', [d_item(1, ESP[0]), cont('ak-d-sep'), d_item(2, ESP[1]), cont('ak-d-sep'),
                          d_item(3, ESP[2]), cont('ak-d-sep'), d_item(4, ESP[3])], row=True),
    ]),
])
hero_bg(D_HERO, BG_D, 'center center')

def dstat(n, big, small):
    return cont(f'ak-d-stat ak-d-st{n}', [h(big, 'p', 'ak-d-big'), tx(f'<p>{small}</p>', 'ak-d-small')])
STATS_D = cont('ak-d-stats', [cont('ak-d-stats-in', [dstat(i + 1, *s) for i, s in enumerate(STATS)])])
# sticky nativo (como Diana y Francisco): solo desktop y laptop, sin márgenes, dentro de la fila ak-d-cols
STATS_D['settings'].update({'sticky': 'top', 'sticky_on': ['desktop', 'laptop'], 'sticky_offset': 54,
                            'sticky_offset_laptop': 38, 'sticky_parent': 'yes'})
D_BODY = cont('ak-d-body', [
    cont('ak-d-card', [
        cont('ak-d-cols', [
            cont('ak-d-main', [
                h('Resumen ejecutivo', 'h2', 'ak-d-h ak-d-h-res'), tx(RES, 'ak-d-res'),
                cont('ak-d-hr'),
                h('Cargos principales y trayectoria', 'h2', 'ak-d-h ak-d-h-car'), tx(CARGOS, 'ak-d-list'),
                cont('ak-d-hr'),
                h('Formación académica', 'h2', 'ak-d-h ak-d-h-for'), tx(FORM, 'ak-d-list'),
                cont('ak-d-hr'),
                h('Aportes destacados y publicaciones', 'h2', 'ak-d-h ak-d-h-apo'), tx(APOR, 'ak-d-list ak-d-arrow'),
            ]),
            STATS_D,
        ], row=True),
    ]),
])

# ---------- MÓVIL (y tablet: el diseño de 430 centrado) ----------
def m_cell(n, text):
    return cont(f'ak-m-cell ak-m-cell-{n}', [cont(f'ak-m-ico ak-m-ico-{n}'), tx(f'<p>{text}</p>', 'ak-m-cell-t')])
M_HERO = cont('ak-m-hero', [
    cont('ak-m-logo', [im(LOGO, 'ak-m-logo-img', 'Goberna')]),
    cont('ak-m-name', [h(D['nombre']['linea1'], 'h1', 'ak-m-n1'), h(D['nombre']['linea2'], 'h1', 'ak-m-n2')]),
    tx(SUB_M, 'ak-m-sub'),
    cont('ak-m-esp', [tx('<p>Especialidades</p>', 'ak-m-esp-lbl'),
                      m_cell(1, ESP[0]), m_cell(2, ESP[1]), m_cell(3, ESP[2]), m_cell(4, ESP[3]),
                      cont('ak-m-sep ak-m-sep-1'), cont('ak-m-sep ak-m-sep-2')]),
    cont('ak-m-foto', [im(FOTO, 'ak-m-foto-img', 'Daniela Galvan')]),
])
hero_bg(M_HERO, BG_M, 'top center')

def mstat(n, big, small):
    return cont(f'ak-m-dato ak-m-d{n}', [h(big, 'p', 'ak-m-big'), tx(f'<p>{small}</p>', 'ak-m-small')])
M_BODY = cont('ak-m-body', [
    cont('ak-m-card', [
        h('Resumen ejecutivo', 'h2', 'ak-m-h ak-m-h-res'), tx(RES, 'ak-m-res'),
        cont('ak-m-datos', [mstat(i + 1, *s) for i, s in enumerate(STATS)]),
        cont('ak-m-hr'),
        h('Cargos<br>principales y<br>trayectoria', 'h2', 'ak-m-h ak-m-h-car'), tx(CARGOS, 'ak-m-list'),
        cont('ak-m-hr'),
        h('Formación académica', 'h2', 'ak-m-h ak-m-h-for'), tx(FORM, 'ak-m-list'),
        cont('ak-m-hr'),
        h('Aportes destacados y publicaciones', 'h2', 'ak-m-h ak-m-h-apo'), tx(APOR, 'ak-m-list ak-m-arrow'),
    ]),
])

# widgets ocultos que hacen que Elementor cargue las fuentes (como en Diana)
FONTS = cont('ak-fonts', [])
for fam, w in [('Montserrat', '800'), ('Montserrat', '700'), ('Montserrat', '400'), ('Open Sans', '400'), ('Open Sans', '700'),
               ('Sora', '700'), ('Sora', '400'), ('Manrope', '400')]:
    x = tx(f'<p>{fam}</p>', '')
    x['settings'].update({"typography_typography": "custom", "typography_font_family": fam, "typography_font_weight": w})
    FONTS['elements'].append(x)

# ---------- CSS ----------
def head_d(key, height, left, ico, ix, iy, iw, ih):
    return (f"selector .ak-d-h-{key} .elementor-heading-title {{ height: {u(height)}; padding-left: {u(left)}; }}\n"
            f"selector .ak-d-h-{key} .elementor-heading-title::before {{ left: {u(ix)}; top: {u(iy)}; width: {u(iw)}; height: {u(ih)}; background-image: url({I[ico]}); }}\n")
def head_m(key, height, left, top, ico, ix, iy, iw, ih):
    return (f"selector .ak-m-h-{key} .elementor-heading-title {{ height: {m(height)}; padding: {m(top)} 0 0 {m(left)}; }}\n"
            f"selector .ak-m-h-{key} .elementor-heading-title::before {{ left: {m(ix)}; top: {m(iy)}; width: {m(iw)}; height: {m(ih)}; background-image: url({I[ico]}); }}\n")
D_ICO = [(1, 'icono-investigacion-criminal', 36.52), (2, 'icono-inteligencia-digital', 37.82),
         (3, 'icono-prevencion-ciberdelito', 36.52), (4, 'icono-osint-socmint', 36.92)]
M_ICO = [(1, 'icono-investigacion-criminal', 23), (2, 'icono-inteligencia-digital', 23),
         (3, 'icono-prevencion-ciberdelito', 23), (4, 'icono-osint-socmint', 23)]
M_CELL = [(1, 96, 31), (2, 292, 31), (3, 96, 108.5), (4, 292, 108.5)]

CSS = f'''
selector {{ --u: min(1px, calc(100vw / 1920)); --m: min(1px, calc(100vw / 430)); }}
selector .ak-fonts {{ display: none !important; }}
selector .elementor-widget-heading .elementor-heading-title, selector .elementor-widget-text-editor p {{ margin: 0; }}
selector .elementor-widget {{ margin-bottom: 0 !important; }}
/* ===== DESKTOP 1920 (laptop 1366 = mismo diseño × 0,7115 por --u) ===== */
selector .ak-d-hero {{ position: relative !important; width: 100% !important; height: {u(850)} !important; overflow: hidden; }}
selector .ak-d-logo {{ position: absolute !important; left: {L(200)}; top: {u(101)}; width: {u(184)} !important; height: {u(47)}; }}
selector .ak-d-name {{ position: absolute !important; left: {L(200)}; top: {u(192)}; width: {u(820)} !important; }}
selector .ak-d-n1 .elementor-heading-title {{ font: 800 {u(64)} / 0.964 {MONT}; color: {GOLD}; letter-spacing: {u(2.56)}; }}
selector .ak-d-n2 .elementor-heading-title {{ font: 800 {u(87)} / 0.964 {MONT}; color: #fff; letter-spacing: {u(2.56)}; }}
selector .ak-d-sub {{ margin-top: {u(19.4)} !important; }}
selector .ak-d-sub p {{ font: 400 {u(28)} / {u(48)} {OPEN}; color: #fff; }}
selector .ak-d-foto {{ position: absolute !important; left: {L(999)}; top: {u(101)}; width: {u(721)} !important; height: {u(749)}; }}
selector .ak-m-foto {{ position: absolute !important; left: {ML(28)}; top: {m(542)}; width: {m(375)} !important; height: {m(389)}; }}
selector .ak-d-logo-img, selector .ak-m-logo-img, selector .ak-d-foto-img, selector .ak-m-foto-img {{ width: 100% !important; height: 100%; }}
selector .ak-d-logo-img .elementor-widget-container, selector .ak-m-logo-img .elementor-widget-container,
selector .ak-d-foto-img .elementor-widget-container, selector .ak-m-foto-img .elementor-widget-container {{ width: 100%; height: 100%; }}
selector .ak-d-logo-img img, selector .ak-m-logo-img img {{ display: block; width: 100% !important; height: 100% !important; max-width: none !important; object-fit: contain; }}
selector .ak-d-foto-img img, selector .ak-m-foto-img img {{ display: block; width: 100% !important; height: 100% !important; max-width: none !important; object-fit: cover; object-position: center top; }}
selector .ak-d-esp {{ position: absolute !important; left: {L(200)}; top: {u(536)}; width: {u(820)} !important; height: {u(170)}; background: url({I['barra-especialidades-desk']}) 0 0 / 100% 100% no-repeat; }}
selector .ak-d-esp-lbl {{ position: absolute !important; left: {u(42)}; top: {u(-16)}; width: auto !important; }}
selector .ak-d-esp-lbl p {{ font: 400 {u(25)} / normal {MONT}; color: {GOLD}; white-space: nowrap; }}
selector .ak-d-row {{ position: absolute !important; left: {u(30)}; top: {u(42.54)}; width: {u(760)} !important; height: {u(116.92)}; display: flex; flex-direction: row !important; align-items: center !important; gap: {u(20)} !important; }}
selector .ak-d-it {{ flex: none !important; width: {u(160)} !important; height: {u(116.92)}; display: flex; flex-direction: column !important; align-items: center !important; gap: {u(8)} !important; }}
selector .ak-d-ico {{ flex: none !important; width: 100% !important; height: {u(37.93)}; background-repeat: no-repeat; background-position: center bottom; }}
''' + ''.join(f"selector .ak-d-ico-{n} {{ background-image: url({I[k]}); background-size: auto {u(hh)}; }}\n" for n, k, hh in D_ICO) + f'''
selector .ak-d-it-t {{ width: 100% !important; }}
selector .ak-d-it-t p {{ font: 400 {u(18)} / {u(24)} {OPEN}; color: #fff; text-align: center; }}
selector .ak-d-sep {{ flex: none !important; width: 1px !important; height: {u(48.5)}; margin: 0 -0.5px !important; background: rgba(214,167,82,.7); }}
selector .ak-d-body {{ display: flex; flex-direction: column !important; align-items: center !important; width: 100% !important; padding: {u(80)} 0 !important; background: {BG}; }}
selector .ak-d-card {{ width: {u(1519)} !important; max-width: none; box-sizing: border-box; padding: {u(54)} {u(95)} {u(82)} {u(81)} !important; background: #fff; border-radius: {u(20)}; box-shadow: 0 3px 16px rgba(6,8,26,.16); }}
selector .ak-d-cols {{ display: flex; flex-direction: row !important; align-items: flex-start !important; gap: {u(79)} !important; width: 100% !important; padding: 0 !important; }}
selector .ak-d-main {{ flex: none !important; width: {u(812)} !important; padding: 0 !important; }}
selector .ak-d-h .elementor-heading-title {{ position: relative; box-sizing: border-box; font: 700 {u(26)} / {u(91)} {MONT}; color: {GOLD}; text-transform: uppercase; white-space: nowrap; }}
selector .ak-d-h .elementor-heading-title::before {{ content: ""; position: absolute; background: no-repeat center / 100% 100%; }}
''' + head_d('res', 88, 46, 'icono-resumen', -1, 21.64, 39.34, 40.36) \
    + head_d('car', 88.7, 46.34, 'icono-titulo-cargos', 0, 30.25, 38.34, 30.5) \
    + head_d('for', 89.2, 46, 'icono-formacion', 3, 17.47, 31.66, 37.93) \
    + head_d('apo', 86.2, 46.5, 'icono-aportes', 0, 26.47, 35.17, 32.46) + f'''
selector .ak-d-res p {{ margin-left: {u(61)}; width: {u(753)}; font: 400 {u(18)} / {u(34)} {OPEN}; color: {INK}; }}
selector .ak-d-res b, selector .ak-d-list b, selector .ak-m-res b, selector .ak-m-list b {{ font-weight: 700; }}
selector .ak-d-hr {{ width: 100% !important; height: 1px; margin: {u(25)} 0 {u(24)} !important; background: {LINE}; }}
selector .ak-d-list ul {{ list-style: none; margin: 0 0 0 {u(61)}; padding: 0; width: {u(750)}; }}
selector .ak-d-arrow ul {{ margin-left: {u(61.5)}; }}
selector .ak-d-list li {{ position: relative; padding-left: {u(18)}; margin: 0 0 {u(20)}; font: 400 {u(18)} / {u(28)} {OPEN}; color: {INK}; }}
selector .ak-d-list li:last-child, selector .ak-m-list li:last-child {{ margin-bottom: 0; }}
selector .ak-d-list li::before {{ content: ""; position: absolute; left: 0; top: 0; width: {u(8)}; height: {u(28)}; background: url({I['vineta']}) center / 100% 100% no-repeat; }}
selector .ak-d-arrow li {{ padding-left: {u(28)}; }}
selector .ak-d-arrow li::before {{ width: {u(18)}; background-image: url({I['vineta-grande']}); }}
selector .ak-d-stats {{ flex: none !important; width: {u(452)} !important; margin: 0 !important; padding: {u(27)} 0 0 0 !important; }}
selector .ak-d-stats-in {{ width: 100% !important; box-sizing: border-box; padding: {u(7)} 0 {u(8)} {u(79)} !important; border-left: 1px solid {GOLD}; gap: {u(39)} !important; }}
selector .ak-d-stat {{ position: relative; width: 100% !important; }}
selector .ak-d-st1 {{ height: {u(65)}; }} selector .ak-d-st2 {{ height: {u(65)}; }} selector .ak-d-st3 {{ height: {u(68)}; }}
selector .ak-d-big .elementor-heading-title {{ font: 800 {u(37)} / normal {MONT}; color: {INK}; white-space: nowrap; }}
selector .ak-d-st2 .ak-d-big .elementor-heading-title {{ font-size: {u(38)}; }}
selector .ak-d-small {{ position: absolute !important; left: 0; top: {u(43)}; width: {u(382)} !important; max-width: none !important; }}
selector .ak-d-st3 .ak-d-small {{ top: {u(40)}; }}
selector .ak-d-small p {{ font: 400 {u(18)} / {u(22)} {OPEN}; color: {INK}; }}
selector .ak-d-st3 .ak-d-small p {{ line-height: {u(28)}; }}
/* ===== MÓVIL 430 (375 = × 0,872 por --m); tablet muestra esta versión centrada ===== */
selector .ak-m-hero {{ position: relative !important; width: 100% !important; height: {m(931)} !important; overflow: hidden; }}
selector .ak-m-logo {{ position: absolute !important; left: {ML(24)}; top: {m(36)}; width: {m(119.92)} !important; height: {m(30.65)}; }}
selector .ak-m-name {{ position: absolute !important; left: {ML(24)}; top: {m(95)}; width: auto !important; }}
selector .ak-m-n1 .elementor-heading-title {{ font: 800 {m(30.897)} / 0.964 {MONT}; color: {GOLD}; letter-spacing: {m(1.2359)}; white-space: nowrap; }}
selector .ak-m-n2 .elementor-heading-title {{ font: 800 {m(42)} / 0.964 {MONT}; color: #fff; letter-spacing: {m(1.2359)}; white-space: nowrap; }}
selector .ak-m-sub {{ position: absolute !important; left: {ML(24)}; top: {m(181)}; width: {m(382)} !important; }}
selector .ak-m-sub p {{ font: 400 {m(16)} / {m(28)} {MANR}; color: #fff; }}
selector .ak-m-esp {{ position: absolute !important; left: {ML(24)}; top: {m(298)}; width: {m(382)} !important; height: {m(181)}; background: url({I['barra-especialidades-movil']}) 0 0 / 100% 100% no-repeat; }}
selector .ak-m-esp-lbl {{ position: absolute !important; left: {m(29)}; top: {m(-28)}; width: auto !important; }}
selector .ak-m-esp-lbl p {{ font: 400 {m(13)} / {m(54)} {SORA}; color: {GOLD}; white-space: nowrap; }}
selector .ak-m-cell {{ position: absolute !important; width: {m(160)} !important; margin-left: {m(-80)} !important; align-items: center !important; }}
''' + ''.join(f"selector .ak-m-cell-{n} {{ left: {m(x)}; top: {m(y)}; }}\n" for n, x, y in M_CELL) + f'''
selector .ak-m-ico {{ flex: none !important; width: 100% !important; height: {m(23)}; margin-bottom: {m(5)} !important; background-repeat: no-repeat; background-position: center bottom; }}
''' + ''.join(f"selector .ak-m-ico-{n} {{ background-image: url({I[k]}); background-size: auto {m(hh)}; }}\n" for n, k, hh in M_ICO) + f'''
selector .ak-m-cell-t {{ width: 100% !important; }}
selector .ak-m-cell-t p {{ font: 400 {m(12)} / {m(13)} {MANR}; color: #fff; text-align: center; }}
selector .ak-m-sep {{ position: absolute !important; left: {m(188.36)}; width: 1px !important; height: {m(57.5)}; background: rgba(214,167,82,.7); }}
selector .ak-m-sep-1 {{ top: {m(29)}; }} selector .ak-m-sep-2 {{ top: {m(107)}; }}
selector .ak-m-body {{ display: flex; flex-direction: column !important; align-items: center !important; width: 100% !important; padding: {m(20)} 0 !important; background: {BG}; }}
selector .ak-m-card {{ width: {m(390)} !important; max-width: none; box-sizing: border-box; padding: {m(51)} {m(20)} !important; background: #fff; border-radius: {m(20)}; box-shadow: 0 3px 16px rgba(6,8,26,.16); }}
selector .ak-m-h .elementor-heading-title {{ position: relative; box-sizing: border-box; font: 700 {m(26)} / {m(33)} {SORA}; color: {GOLD}; text-transform: uppercase; }}
selector .ak-m-h .elementor-heading-title::before {{ content: ""; position: absolute; background: no-repeat center / 100% 100%; }}
''' + head_m('res', 66, 47, 4, 'icono-resumen', 0, 0, 39.34, 40.36) \
    + head_m('car', 128, 46, 0, 'icono-titulo-cargos', 0, 0.3, 38.34, 30.5) \
    + head_m('for', 98, 47, 3, 'icono-formacion', 4, 0, 31.66, 37.93) \
    + head_m('apo', 128, 46.5, 0, 'icono-aportes', 0, 1, 35.17, 32.46) + f'''
selector .ak-m-res p {{ margin-left: {m(20)}; width: {m(330)}; font: 400 {m(18)} / {m(34)} {OPEN}; color: {INK}; }}
selector .ak-m-datos {{ width: {m(312)} !important; margin: {m(40)} 0 0 {m(20)} !important; box-sizing: border-box; border-left: 2px solid {GOLD}; padding-left: {m(20)} !important; gap: {m(28)} !important; }}
selector .ak-m-dato {{ width: {m(290)} !important; gap: {m(2)} !important; }}
selector .ak-m-big .elementor-heading-title {{ font: 800 {m(37)} / {m(45)} {MONT}; color: {INK}; white-space: nowrap; }}
selector .ak-m-d2 .ak-m-big .elementor-heading-title {{ font-size: {m(38)}; line-height: {m(46)}; }}
selector .ak-m-small p {{ font: 400 {m(18)} / {m(22)} {OPEN}; color: {INK}; }}
selector .ak-m-d3 .ak-m-small p {{ line-height: {m(28)}; }}
selector .ak-m-hr {{ width: 100% !important; height: 1px; margin: {m(50)} 0 {m(49)} !important; background: {LINE}; }}
selector .ak-m-list ul {{ list-style: none; margin: 0 0 0 {m(19)}; padding: 0; width: {m(331)}; }}
selector .ak-m-list li {{ position: relative; padding-left: {m(16)}; margin: 0 0 {m(17)}; font: 400 {m(18)} / {m(28)} {OPEN}; color: {INK}; }}
selector .ak-m-list li::before {{ content: ""; position: absolute; left: 0; top: 0; width: {m(6)}; height: {m(28)}; background: url({I['vineta-movil']}) center / 100% 100% no-repeat; }}
selector .ak-m-arrow li {{ padding-left: {m(28)}; line-height: {m(34)}; }}
selector .ak-m-arrow li::before {{ width: {m(18)}; height: {m(34)}; background-image: url({I['vineta-grande-movil']}); }}
/* ===== cambio de versión: >1024 desktop/laptop, ≤1024 móvil ===== */
@media (max-width: 1024px) {{ selector .ak-d-hero, selector .ak-d-body {{ display: none !important; }} }}
@media (min-width: 1025px) {{ selector .ak-m-hero, selector .ak-m-body {{ display: none !important; }} }}
'''

root = {
    "id": rid(), "elType": "container",
    "settings": {"content_width": "full", "flex_direction": "column", "flex_wrap": "nowrap", "flex_align_items": "stretch",
                 "flex_gap": {"unit": "px", "column": "0", "row": "0", "isLinked": True, "size": 0},
                 "padding": pad0(), "css_classes": "ak-dg", "custom_css": CSS.strip()},
    "elements": [FONTS, D_HERO, D_BODY, M_HERO, M_BODY],
    "isInner": False,
}
doc = {"content": [root], "page_settings": [], "version": "0.4", "title": "Daniela Galvan", "type": "container"}
json.dump(doc, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', OUT, os.path.getsize(OUT), 'bytes; ids', len(IDS))
