"""MOTOR de landings CV de ponentes (Figma Foro-Ponentes -> Elementor).

Uso:  python motor.py <slug>
Lee   cv-ponentes/<slug>/<slug>-datos.json          (contenido literal + ajustes de get_design_context)
      cv-ponentes/<slug>/_fuentes-figma/medidas.json (medidas automáticas: python medidas.py ...)
Crea  cv-ponentes/<slug>/<slug>.json                 (plantilla importable de Elementor)
      cv-ponentes/<slug>/_generador/sim.html        (marcado tipo Elementor para medir con verificar.py)
      cv-ponentes/<slug>/_generador/<slug>-preview.html (Artifact: Desktop 1920 / Laptop 1366 / Mobile 375 + Ver widgets)
y copia iconos e imágenes comunes a la carpeta del ponente.

Escalas: desktop 1920 y laptop = mismo diseño × 100vw/1920 (--u); móvil = diseño de 430 × 100vw/430 (--m).
>1024 px se ve la versión desktop; ≤1024 px la móvil. Columna de cifras: sticky nativo (54 desktop / 38 laptop)."""
import base64, json, os, random, re, shutil, sys

MOTOR = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(MOTOR)
REC = os.path.join(MOTOR, 'recursos')
BIB = 'https://grupogoberna.com/wp-content/uploads/2026/10/'
GOLD, INK, LINE, BG = '#d6a752', '#030a22', '#e3e7ee', '#f3f6fa'
MONT, OPEN, SORA, MANR = "'Montserrat', Arial, sans-serif", "'Open Sans', Arial, sans-serif", "'Sora', Arial, sans-serif", "'Manrope', Arial, sans-serif"

# íconos de especialidades conocidos: clave -> (archivo en recursos/iconos-webp, alto en desktop 1920)
ICONOS = {
    'escudo': ('esp-escudo', 36.52), 'pin': ('esp-pin', 36.52), 'global': ('esp-global', 37.82), 'proceso': ('esp-proceso', 36.92),
    'comunicacion': ('esp-comunicacion', 36.52), 'capitolio': ('esp-capitolio', 37.93), 'libro': ('esp-libro', 37.82),
}
ICONO_POR_NOMBRE = {'noun-security-8354638': 'escudo', 'noun_Pin_3698121': 'pin', 'noun_global_2559364': 'global',
                    'noun_process_2021778': 'proceso'}
ICONO_POR_ANCHO = {33.1: 'escudo', 28.79: 'pin', 37.82: 'global', 36.92: 'proceso', 35.17: 'comunicacion', 31.66: 'capitolio', 40.97: 'libro'}
M_ICON_ESCALA = 23 / 37.93  # móvil: contenedor de 23 frente a 37.93 en desktop

# BANNER ESTÁNDAR (regla del usuario, 2026-10-27): mismo tamaño, tipografía, colores y espacios en todos los ponentes,
# en desktop, laptop y móvil. Del Figma solo cambian el texto, las especialidades y la foto (ancho y x).
BANNER = {
    'nombre_d': (64, 87), 'tracking_d': (2.56, 2.56),            # Montserrat 800, interlineado 0.964
    'nombre_m': (30.897, 42), 'tracking_m': (1.2359, 1.2359),
    'barra_top_d': 536, 'fila_d': (42.54, 116.92), 'item_d': 116.92, 'caja_ico_d': 37.93,
    'titular_top_m': 181, 'barra_top_m': 298,
    'foto_d': (101, 749), 'foto_m': (512, 389),                   # top y alto fijos; x y ancho según la foto
    'hero_m': 901,   # pedido del usuario (27-oct): foto móvil 30 px más arriba y banner móvil 30 px más bajo (Figma: 542 y 931)
}
# nombres únicos en la Biblioteca de medios (en la web ya existían otros archivos con los nombres viejos)
IMG = {'fondo_d': 'cv-ponentes-fondo-desktop.webp', 'fondo_m': 'cv-ponentes-fondo-movil.webp', 'logo': 'logo-goberna-1-1.webp'}


def u(n): return f'calc(var(--u)*{round(n, 3)})'
def m(n): return f'calc(var(--m)*{round(n, 3)})'
def L(x): return f'calc(50% + var(--u)*{round(x - 960, 3)})'
def ML(x): return f'calc(50% + var(--m)*{round(x - 215, 3)})'
def slugify(s):
    s = s.lower()
    for a, b in zip('áéíóúüñ', 'aeiouun'):
        s = s.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', re.sub(r'<br\s*/?>', ' ', s)).strip('-')


def cargar(slug):
    P = os.path.join(RAIZ, slug)
    D = json.load(open(os.path.join(P, f'{slug}-datos.json'), encoding='utf-8'))
    M = json.load(open(os.path.join(P, '_fuentes-figma', 'medidas.json'), encoding='utf-8'))
    return P, D, M


def validar(D, M):
    err = []
    for k in ('nombre', 'titular', 'especialidades', 'cifras', 'resumen', 'cargos', 'formacion', 'aportes',
              'titulo_aportes', 'foto'):
        if k not in D: err.append(f'falta "{k}" en datos')
    if err: return err
    if len(D['especialidades']['d']) != 4 or len(D['especialidades']['m']) != 4: err.append('especialidades: 4 en "d" y 4 en "m"')
    if len(D['cifras']) != 3: err.append('cifras: tienen que ser 3')
    md, mm = M['desktop'], M['movil']
    for key, lst in (('car', 'cargos'), ('for', 'formacion'), ('apo', 'aportes')):
        nd, nm = md['secciones_d'][key]['n'], mm['secciones_m'][key]['n']
        if len(D[lst]) != nd: err.append(f'{lst}: hay {len(D[lst])} ítems y el Figma desktop tiene {nd}')
        if len(D[lst]) != nm: err.append(f'{lst}: hay {len(D[lst])} ítems y el Figma móvil tiene {nm}')
    for t in [D['titular']] + D['resumen'] + D['cargos'] + D['formacion'] + D['aportes']:
        if t.count('<b>') != t.count('</b>'): err.append(f'negritas sin cerrar: {t[:60]}')
        if re.search(r'</?(?!b>|br>|br/>|br />)[a-z]', t): err.append(f'etiqueta HTML no permitida (solo <b> y <br>): {t[:60]}')
    return err


# ------------------------------------------------------------------ parámetros derivados de las medidas
def iconos_esp(D, md):
    keys = D.get('iconos_esp')
    out = []
    for i, ic in enumerate(md['esp_iconos_d']):
        k = keys[i] if keys else (ICONO_POR_NOMBRE.get(ic['nombre']) or ICONO_POR_ANCHO.get(round(ic.get('ancho', 0), 2)))
        if not k: raise SystemExit(f'no reconozco el ícono {ic}; pon "iconos_esp" en datos')
        alto_d = ICONOS[k][1]
        caja_d = BANNER['caja_ico_d']
        out.append({'k': k, 'archivo': ICONOS[k][0], 'alto_d': alto_d, 'caja_d': caja_d})
    return out


def lista_params(sec, clave, movil=False):
    """Interlineado, separación y ajuste vertical de la viñeta de una lista."""
    arrow = clave == 'apo'
    if sec['estilo'] == 'items':
        hs = sec['item_altos']
        lh = 34 if (arrow and all(round(h) % 34 == 0 for h in hs) and any(round(h) % 28 for h in hs)) else 28
        if movil and arrow: lh = 34
        gaps = sec['gap'] or [20]
        assert len(gaps) == 1, f'separación irregular en {clave}: {gaps}'
        return {'lh': lh, 'gap': gaps[0], 'dy': 0}
    # plantilla antigua: un texto con párrafos en blanco entre ítems (la separación = una línea) y marcas sueltas
    tops = sec['marca_tops']
    lh = 34 if arrow else 28
    dif = [tops[i + 1] - tops[i] for i in range(len(tops) - 1)]
    if dif and not all(abs(d / lh - round(d / lh)) < 0.02 for d in dif):
        lh = 28 if lh == 34 else 34
    tam = sec['marca_tam'] or [8, 8]
    if arrow:
        dy = tops[0] - 5           # la flecha de vineta-grande ocupa 5..23 en su caja de 28
    else:
        dy = tops[0] - (14 - tam[1] / 2)   # el punto de vineta está centrado en 14
    return {'lh': lh, 'gap': lh, 'dy': round(dy, 2)}


def cifras_params(md):
    out = []
    for c in md['cifras_d']:
        lh = 28 if round(c['small_h']) % 28 == 0 and round(c['small_h']) % 22 else 22
        lines = round(c['small_h'] / lh)
        out.append({'alto': c['alto'], 'big': 38 if round(c['big_h']) == 46 else 37, 'top': c['small_top'], 'lh': lh,
                    'wrap': lines > 1, 'w': c['small_w']})
    return out


def datos_m_params(mm):
    out = []
    for c in mm['resumen_m']['dato']:
        lh = 28 if round(c['small_h']) % 28 == 0 and round(c['small_h']) % 22 else 22
        out.append({'big': 38 if round(c['big_h']) == 46 else 37, 'blh': c['big_h'], 'gap': round(c['small_top'] - c['big_h'], 2), 'lh': lh})
    return out


# ------------------------------------------------------------------ Elementor
class EL:
    def __init__(self):
        self.ids = set()
    def rid(self):
        while True:
            s = ''.join(random.choices('0123456789abcdef', k=8))
            if s not in self.ids:
                self.ids.add(s); return s
    def cont(self, cls, kids=(), row=False):
        s = {"content_width": "full", "flex_direction": "row" if row else "column", "flex_wrap": "nowrap",
             "flex_align_items": "stretch", "flex_gap": {"unit": "px", "column": "0", "row": "0", "isLinked": True, "size": 0},
             "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": False}, "css_classes": cls}
        return {"id": self.rid(), "elType": "container", "settings": s, "elements": list(kids), "isInner": True}
    def wid(self, kind, cls, settings):
        s = dict(settings); s["_css_classes"] = cls
        return {"id": self.rid(), "elType": "widget", "settings": s, "elements": [], "widgetType": kind}
    def h(self, text, level, cls): return self.wid('heading', cls, {"title": text, "header_size": level})
    def tx(self, html, cls): return self.wid('text-editor', cls, {"editor": html})
    def im(self, url, cls, alt):
        return self.wid('image', cls, {"image": {"url": url, "id": 0, "source": "library", "size": "", "alt": alt}, "image_size": "full"})


def construir(slug):
    P, D, M = cargar(slug)
    err = validar(D, M)
    if err:
        print('ERRORES EN LOS DATOS:'); [print(' -', e) for e in err]; sys.exit(1)
    md, mm = M['desktop'], M['movil']
    nombre_txt = D.get('nombre_completo') or ' '.join(D['nombre']['d']).title()
    cls_root = 'ak-' + ''.join(w[0] for w in slug.split('-'))[:3]

    # ---------- recursos: iconos e imágenes comunes a la carpeta del ponente
    ESP = iconos_esp(D, md)
    for d in ('iconos', 'iconos-webp', 'imagenes'):
        os.makedirs(os.path.join(P, d), exist_ok=True)
    for f in os.listdir(os.path.join(REC, 'iconos-webp')):
        if not f.startswith('esp-'):
            shutil.copy(os.path.join(REC, 'iconos-webp', f), os.path.join(P, 'iconos-webp', f))
    for f in os.listdir(os.path.join(REC, 'iconos')):
        if not f.startswith('esp-'):
            shutil.copy(os.path.join(REC, 'iconos', f), os.path.join(P, 'iconos', f))
    esp_nombres = []
    for e, lbl in zip(ESP, D['especialidades']['d']):
        nm = 'icono-' + slugify(lbl)
        esp_nombres.append(nm)
        shutil.copy(os.path.join(REC, 'iconos-webp', e['archivo'] + '.webp'), os.path.join(P, 'iconos-webp', nm + '.webp'))
        shutil.copy(os.path.join(REC, 'iconos', e['archivo'] + '.svg'), os.path.join(P, 'iconos', nm + '.svg'))
    for f in IMG.values():
        shutil.copy(os.path.join(REC, 'imagenes', f), os.path.join(P, 'imagenes', f))
    for f in ('hero-fondo-capitolio.webp', 'hero-fondo-movil.webp', 'logo-goberna.webp'):   # nombres viejos: ya no se usan
        if os.path.exists(os.path.join(P, 'imagenes', f)): os.remove(os.path.join(P, 'imagenes', f))
    foto_arch = D['foto']['archivo']
    # regla del usuario (2026-10-27): la foto del móvil va en la misma posición que en desktop
    # (misma orientación y mismo encuadre) -> siempre la misma imagen; "archivo_m" se ignora
    foto_arch_m = foto_arch
    for fa in {foto_arch, foto_arch_m}:
        fpath = os.path.join(P, 'imagenes', fa)
        if not os.path.exists(fpath):
            print(f'FALTA LA FOTO imagenes/{fa} (hazla con foto.py)'); sys.exit(1)
        if os.path.getsize(fpath) >= 500 * 1024:
            print(f'LA FOTO imagenes/{fa} PESA {os.path.getsize(fpath)//1024} KB (máximo 500)'); sys.exit(1)

    def du(name):
        return 'data:image/webp;base64,' + base64.b64encode(open(os.path.join(P, 'iconos-webp', name + '.webp'), 'rb').read()).decode()
    I = {k: du(k) for k in esp_nombres + ['icono-resumen', 'icono-titulo-cargos', 'icono-formacion', 'icono-aportes', 'vineta',
                                         'vineta-grande', 'vineta-movil', 'vineta-grande-movil', 'barra-especialidades-desk',
                                         'barra-especialidades-movil']}

    # ---------- contenido
    def lis(rows): return '<ul>' + ''.join(f'<li>{x}</li>' for x in rows) + '</ul>'
    RES = ''.join(f'<p>{p}</p>' for p in D['resumen'])
    CARGOS, FORM, APOR = lis(D['cargos']), lis(D['formacion']), lis(D['aportes'])
    SUB = f"<p>{D['titular']}</p>"
    SUB_D = f"<p>{D.get('titular_d') or D['titular']}</p>"   # titular_d: solo si el Figma desktop parte la línea a mano (<br>)
    FOTO, FOTO_M, LOGO = BIB + foto_arch, BIB + foto_arch_m, BIB + IMG['logo']
    BG_D, BG_M = BIB + IMG['fondo_d'], BIB + IMG['fondo_m']
    E = EL()

    def hero_bg(c, url, pos):
        c['settings'].update({'background_background': 'classic', 'background_color': '#020715',
                              'background_image': {'url': url, 'id': 0, 'size': '', 'alt': '', 'source': 'library'},
                              'background_position': pos, 'background_repeat': 'no-repeat', 'background_size': 'cover'})

    # ---------- DESKTOP / LAPTOP
    def d_item(n, text):
        return E.cont('ak-d-it', [E.cont(f'ak-d-ico ak-d-ico-{n}'), E.tx(f'<p>{text}</p>', 'ak-d-it-t')])
    ED = D['especialidades']['d']
    D_HERO = E.cont('ak-d-hero', [
        E.cont('ak-d-logo', [E.im(LOGO, 'ak-d-logo-img', 'Goberna')]),
        E.cont('ak-d-name', [E.h(D['nombre']['d'][0], 'h1', 'ak-d-n1'), E.h(D['nombre']['d'][1], 'h1', 'ak-d-n2'), E.tx(SUB_D, 'ak-d-sub')]),
        E.cont('ak-d-foto', [E.im(FOTO, 'ak-d-foto-img', nombre_txt)]),
        E.cont('ak-d-esp', [
            E.tx('<p>Especialidades</p>', 'ak-d-esp-lbl'),
            E.cont('ak-d-row', [d_item(1, ED[0]), E.cont('ak-d-sep'), d_item(2, ED[1]), E.cont('ak-d-sep'),
                                d_item(3, ED[2]), E.cont('ak-d-sep'), d_item(4, ED[3])], row=True)]),
    ])
    hero_bg(D_HERO, BG_D, 'center center')
    STATS = D['cifras']
    def dstat(n, c):
        return E.cont(f'ak-d-stat ak-d-st{n}', [E.h(c['big'], 'p', 'ak-d-big'), E.tx(f"<p>{c['small']}</p>", 'ak-d-small')])
    STATS_D = E.cont('ak-d-stats', [E.cont('ak-d-stats-in', [dstat(i + 1, c) for i, c in enumerate(STATS)])])
    STATS_D['settings'].update({'sticky': 'top', 'sticky_on': ['desktop', 'laptop'], 'sticky_offset': 54,
                                'sticky_offset_laptop': 38, 'sticky_parent': 'yes'})
    TA = D['titulo_aportes']
    D_BODY = E.cont('ak-d-body', [E.cont('ak-d-card', [E.cont('ak-d-cols', [
        E.cont('ak-d-main', [
            E.h('Resumen ejecutivo', 'h2', 'ak-d-h ak-d-h-res'), E.tx(RES, 'ak-d-res'), E.cont('ak-d-hr'),
            E.h('Cargos principales y trayectoria', 'h2', 'ak-d-h ak-d-h-car'), E.tx(CARGOS, 'ak-d-list ak-d-l-car'), E.cont('ak-d-hr'),
            E.h('Formación académica', 'h2', 'ak-d-h ak-d-h-for'), E.tx(FORM, 'ak-d-list ak-d-l-for'), E.cont('ak-d-hr'),
            E.h(TA, 'h2', 'ak-d-h ak-d-h-apo'), E.tx(APOR, 'ak-d-list ak-d-arrow ak-d-l-apo')]),
        STATS_D], row=True)])])

    # ---------- MÓVIL (tablet: el diseño de 430 centrado)
    def m_cell(n, text):
        return E.cont(f'ak-m-cell ak-m-cell-{n}', [E.cont(f'ak-m-ico ak-m-ico-{n}'), E.tx(f'<p>{text}</p>', 'ak-m-cell-t')])
    EM = D['especialidades']['m']
    M_HERO = E.cont('ak-m-hero', [
        E.cont('ak-m-logo', [E.im(LOGO, 'ak-m-logo-img', 'Goberna')]),
        E.cont('ak-m-name', [E.h(D['nombre']['m'][0], 'h1', 'ak-m-n1'), E.h(D['nombre']['m'][1], 'h1', 'ak-m-n2')]),
        E.tx(SUB, 'ak-m-sub'),
        E.cont('ak-m-esp', [E.tx('<p>Especialidades</p>', 'ak-m-esp-lbl'),
                            m_cell(1, EM[0]), m_cell(2, EM[1]), m_cell(3, EM[2]), m_cell(4, EM[3]),
                            E.cont('ak-m-sep ak-m-sep-1'), E.cont('ak-m-sep ak-m-sep-2')]),
        E.cont('ak-m-foto', [E.im(FOTO_M, 'ak-m-foto-img', nombre_txt)]),
    ])
    hero_bg(M_HERO, BG_M, 'top center')
    def mstat(n, c):
        return E.cont(f'ak-m-dato ak-m-d{n}', [E.h(c['big'], 'p', 'ak-m-big'), E.tx(f"<p>{c['small']}</p>", 'ak-m-small')])
    M_BODY = E.cont('ak-m-body', [E.cont('ak-m-card', [
        E.h('Resumen ejecutivo', 'h2', 'ak-m-h ak-m-h-res'), E.tx(RES, 'ak-m-res'),
        E.cont('ak-m-datos', [mstat(i + 1, c) for i, c in enumerate(STATS)]), E.cont('ak-m-hr'),
        E.h('Cargos<br>principales y<br>trayectoria', 'h2', 'ak-m-h ak-m-h-car'), E.tx(CARGOS, 'ak-m-list ak-m-l-car'), E.cont('ak-m-hr'),
        E.h('Formación académica', 'h2', 'ak-m-h ak-m-h-for'), E.tx(FORM, 'ak-m-list ak-m-l-for'), E.cont('ak-m-hr'),
        E.h(TA, 'h2', 'ak-m-h ak-m-h-apo'), E.tx(APOR, 'ak-m-list ak-m-arrow ak-m-l-apo')])])

    FONTS = E.cont('ak-fonts', [])
    for fam, w in [('Montserrat', '800'), ('Montserrat', '700'), ('Montserrat', '400'), ('Open Sans', '400'), ('Open Sans', '700'),
                   ('Sora', '700'), ('Sora', '400'), ('Manrope', '400')]:
        x = E.tx(f'<p>{fam}</p>', '')
        x['settings'].update({"typography_typography": "custom", "typography_font_family": fam, "typography_font_weight": w})
        FONTS['elements'].append(x)

    # ---------- CSS (todo con selector; medidas del Figma)
    nd1, nd2 = BANNER['nombre_d']; td1, td2 = BANNER['tracking_d']
    nm1, nm2 = BANNER['nombre_m']; tm1, tm2 = BANNER['tracking_m']
    fd = [D['foto']['d'][0], BANNER['foto_d'][0], D['foto']['d'][2], BANNER['foto_d'][1]]
    fm = [D['foto']['m'][0], BANNER['foto_m'][0], D['foto']['m'][2], BANNER['foto_m'][1]]
    barra_top = BANNER['barra_top_d']; fila_top, fila_h = BANNER['fila_d']; item_h = BANNER['item_d']
    CIF = cifras_params(md)
    lin_top, lin_h = md['linea_dorada']
    SD = md['secciones_d']
    apo = SD['apo']
    pad_bot = round(md['tarjeta_alto'] - (apo['top'] + apo['cuerpo_top'] + apo['cuerpo_alto']), 2)
    LD = {k: lista_params(SD[k], k) for k in ('car', 'for', 'apo')}
    SM = mm['secciones_m']
    LM = {k: lista_params(SM[k], k, movil=True) for k in ('car', 'for', 'apo')}
    DM = datos_m_params(mm)
    rm = mm['resumen_m']
    datos_gap = round(rm['dato'][1]['top'] - rm['dato'][0]['alto'], 2) if len(rm['dato']) > 1 else 28
    res_gap_m = round(rm['datos'][1] - (rm['texto'][0] + rm['texto'][1]), 2)
    sub_mt = round(165 - (nd1 + nd2) * 0.964, 2)

    def head_d(key, height, left, ico, ix, iy, iw, ih):
        return (f"selector .ak-d-h-{key} .elementor-heading-title {{ height: {u(height)}; padding-left: {u(left)}; }}\n"
                f"selector .ak-d-h-{key} .elementor-heading-title::before {{ left: {u(ix)}; top: {u(iy)}; width: {u(iw)}; height: {u(ih)}; background-image: url({I[ico]}); }}\n")
    def head_m(key, height, left, top, ico, ix, iy, iw, ih):
        return (f"selector .ak-m-h-{key} .elementor-heading-title {{ height: {m(height)}; padding: {m(top)} 0 0 {m(left)}; }}\n"
                f"selector .ak-m-h-{key} .elementor-heading-title::before {{ left: {m(ix)}; top: {m(iy)}; width: {m(iw)}; height: {m(ih)}; background-image: url({I[ico]}); }}\n")
    def list_css(pref, key, p, scale, dot, arrow_img, dot_w):
        s = scale
        css = f"selector .{pref}-l-{key} li {{ line-height: {s(p['lh'])}; margin-bottom: {s(p['gap'])}; }}\n"
        if key == 'apo':
            css += f"selector .{pref}-l-{key} li::before {{ top: {s(p['dy'])}; height: {s(28 if pref == 'ak-d' else 34)}; }}\n"
        else:
            css += f"selector .{pref}-l-{key} li::before {{ top: {s(p['dy'])}; }}\n"
        return css

    # alto del contenedor de cada ícono (desktop: 37.93 en la plantilla nueva, el alto del ícono en la antigua)
    d_ico_css = ''.join(f"selector .ak-d-ico-{n + 1} {{ height: {u(e['caja_d'])}; background-image: url({I[esp_nombres[n]]}); background-size: auto {u(e['alto_d'])}; }}\n"
                        for n, e in enumerate(ESP))
    m_ico_css = ''.join(f"selector .ak-m-ico-{n + 1} {{ background-image: url({I[esp_nombres[n]]}); background-size: auto {m(mi)}; }}\n"
                        for n, mi in enumerate([round(e['alto_d'] * M_ICON_ESCALA, 2) for e in ESP]))
    stat_css = ''
    for n, c in enumerate(CIF, 1):
        stat_css += f"selector .ak-d-st{n} {{ height: {u(c['alto'])}; }}\n"
        stat_css += f"selector .ak-d-st{n} .ak-d-big .elementor-heading-title {{ font-size: {u(c['big'])}; }}\n"
        stat_css += f"selector .ak-d-st{n} .ak-d-small {{ top: {u(c['top'])}; width: {u(c['w'] if c['wrap'] else 382)} !important; }}\n"
        stat_css += (f"selector .ak-d-st{n} .ak-d-small p {{ line-height: {u(c['lh'])}; white-space: {'normal' if c['wrap'] else 'nowrap'}; }}\n")
    dato_css = ''
    for n, c in enumerate(DM, 1):
        dato_css += (f"selector .ak-m-d{n} {{ gap: {m(c['gap'])} !important; }}\n"
                     f"selector .ak-m-d{n} .ak-m-big .elementor-heading-title {{ font-size: {m(c['big'])}; line-height: {m(c['blh'])}; }}\n"
                     f"selector .ak-m-d{n} .ak-m-small p {{ line-height: {m(c['lh'])}; }}\n")
    apo_m = SM['apo']
    apo_m_h = apo_m['lista_top']

    CSS = f'''
selector {{ --u: min(1px, calc(100vw / 1920)); --m: min(1px, calc(100vw / 430)); }}
selector .ak-fonts {{ display: none !important; }}
selector .elementor-widget-heading .elementor-heading-title, selector .elementor-widget-text-editor p {{ margin: 0; }}
selector .elementor-widget {{ margin-bottom: 0 !important; }}
/* ===== DESKTOP 1920 (laptop 1366 = mismo diseño × 0,7115 por --u) ===== */
selector .ak-d-hero {{ position: relative !important; width: 100% !important; height: {u(850)} !important; overflow: hidden; }}
selector .ak-d-logo {{ position: absolute !important; left: {L(200)}; top: {u(101)}; width: {u(184)} !important; height: {u(47)}; }}
selector .ak-d-name {{ position: absolute !important; left: {L(200)}; top: {u(192)}; width: {u(820)} !important; }}
selector .ak-d-n1 .elementor-heading-title {{ font: 800 {u(nd1)} / 0.964 {MONT}; color: {GOLD}; letter-spacing: {u(td1)}; white-space: nowrap; }}
selector .ak-d-n2 .elementor-heading-title {{ font: 800 {u(nd2)} / 0.964 {MONT}; color: #fff; letter-spacing: {u(td2)}; white-space: nowrap; }}
selector .ak-d-sub {{ margin-top: {u(sub_mt)} !important; }}
selector .ak-d-sub p {{ font: 400 {u(28)} / {u(48)} {OPEN}; color: #fff; }}
selector .ak-d-foto {{ position: absolute !important; left: {L(fd[0])}; top: {u(fd[1])}; width: {u(fd[2])} !important; height: {u(fd[3])}; }}
selector .ak-m-foto {{ position: absolute !important; left: {ML(fm[0])}; top: {m(fm[1])}; width: {m(fm[2])} !important; height: {m(fm[3])}; }}
selector .ak-d-logo-img, selector .ak-m-logo-img, selector .ak-d-foto-img, selector .ak-m-foto-img {{ width: 100% !important; height: 100%; }}
selector .ak-d-logo-img .elementor-widget-container, selector .ak-m-logo-img .elementor-widget-container,
selector .ak-d-foto-img .elementor-widget-container, selector .ak-m-foto-img .elementor-widget-container {{ width: 100%; height: 100%; }}
selector .ak-d-logo-img img, selector .ak-m-logo-img img {{ display: block; width: 100% !important; height: 100% !important; max-width: none !important; object-fit: contain; }}
selector .ak-d-foto-img img, selector .ak-m-foto-img img {{ display: block; width: 100% !important; height: 100% !important; max-width: none !important; object-fit: cover; object-position: center top; }}
selector .ak-d-esp {{ position: absolute !important; left: {L(200)}; top: {u(barra_top)}; width: {u(820)} !important; height: {u(170)}; background: url({I['barra-especialidades-desk']}) 0 0 / 100% 100% no-repeat; }}
selector .ak-d-esp-lbl {{ position: absolute !important; left: {u(42)}; top: {u(-16)}; width: auto !important; }}
selector .ak-d-esp-lbl p {{ font: 400 {u(25)} / normal {MONT}; color: {GOLD}; white-space: nowrap; }}
selector .ak-d-row {{ position: absolute !important; left: {u(30)}; top: {u(fila_top)}; width: {u(760)} !important; height: {u(fila_h)}; display: flex; flex-direction: row !important; align-items: center !important; gap: {u(20)} !important; }}
selector .ak-d-it {{ flex: none !important; width: {u(160)} !important; height: {u(item_h)}; display: flex; flex-direction: column !important; align-items: center !important; gap: {u(8)} !important; }}
selector .ak-d-ico {{ flex: none !important; width: 100% !important; background-repeat: no-repeat; background-position: center bottom; }}
{d_ico_css}selector .ak-d-it-t {{ width: 100% !important; }}
selector .ak-d-it-t p {{ font: 400 {u(18)} / {u(24)} {OPEN}; color: #fff; text-align: center; }}
selector .ak-d-sep {{ flex: none !important; width: 1px !important; height: {u(48.5)}; margin: 0 -0.5px !important; background: rgba(214,167,82,.7); }}
selector .ak-d-body {{ display: flex; flex-direction: column !important; align-items: center !important; width: 100% !important; padding: {u(80)} 0 !important; background: {BG}; }}
selector .ak-d-card {{ width: {u(1519)} !important; max-width: none; box-sizing: border-box; padding: {u(54)} {u(95)} {u(pad_bot)} {u(81)} !important; background: #fff; border-radius: {u(20)}; box-shadow: 0 3px 16px rgba(6,8,26,.16); }}
selector .ak-d-cols {{ display: flex; flex-direction: row !important; align-items: flex-start !important; gap: {u(79)} !important; width: 100% !important; padding: 0 !important; }}
selector .ak-d-main {{ flex: none !important; width: {u(812)} !important; padding: 0 !important; }}
selector .ak-d-h .elementor-heading-title {{ position: relative; box-sizing: border-box; font: 700 {u(26)} / {u(91)} {MONT}; color: {GOLD}; text-transform: uppercase; white-space: nowrap; }}
selector .ak-d-h .elementor-heading-title::before {{ content: ""; position: absolute; background: no-repeat center / 100% 100%; }}
''' + head_d('res', 88, 46, 'icono-resumen', -1, 21.64, 39.34, 40.36) \
        + head_d('car', 88.7, 46.34, 'icono-titulo-cargos', 0, 30.25, 38.34, 30.5) \
        + head_d('for', 89.2, 46, 'icono-formacion', 3, 17.47, 31.66, 37.93) \
        + head_d('apo', 86.2, 46.5, 'icono-aportes', 0, 26.47, 35.17, 32.46) + f'''
selector .ak-d-res p {{ margin-left: {u(61)}; width: {u(753)}; font: 400 {u(18)} / {u(34)} {OPEN}; color: {INK}; }}
selector .ak-d-res p + p {{ margin-top: {u(34)}; }}
selector .ak-d-res b, selector .ak-d-list b, selector .ak-m-res b, selector .ak-m-list b {{ font-weight: 700; }}
selector .ak-d-hr {{ width: 100% !important; height: 1px; margin: {u(25)} 0 {u(24)} !important; background: {LINE}; }}
selector .ak-d-list ul {{ list-style: none; margin: 0 0 0 {u(61)}; padding: 0; width: {u(750)}; }}
selector .ak-d-arrow ul {{ margin-left: {u(61.5)}; }}
selector .ak-d-list li {{ position: relative; padding-left: {u(18)}; margin: 0 0 {u(20)}; font: 400 {u(18)} / {u(28)} {OPEN}; color: {INK}; }}
selector .ak-d-list li:last-child, selector .ak-m-list li:last-child {{ margin-bottom: 0 !important; }}
selector .ak-d-list li::before {{ content: ""; position: absolute; left: 0; top: 0; width: {u(8)}; height: {u(28)}; background: url({I['vineta']}) center / 100% 100% no-repeat; }}
selector .ak-d-arrow li {{ padding-left: {u(28)}; }}
selector .ak-d-arrow li::before {{ width: {u(18)}; background-image: url({I['vineta-grande']}); }}
''' + list_css('ak-d', 'car', LD['car'], u, 0, 0, 0) + list_css('ak-d', 'for', LD['for'], u, 0, 0, 0) + list_css('ak-d', 'apo', LD['apo'], u, 0, 0, 0) + f'''
selector .ak-d-stats {{ flex: none !important; width: {u(452)} !important; margin: 0 !important; padding: {u(lin_top - 54)} 0 0 0 !important; }}
selector .ak-d-stats-in {{ width: 100% !important; box-sizing: border-box; height: {u(lin_h)}; padding: {u(7)} 0 0 {u(79)} !important; border-left: 1px solid {GOLD}; gap: {u(39)} !important; }}
selector .ak-d-stat {{ position: relative; width: 100% !important; flex: none !important; }}
selector .ak-d-big .elementor-heading-title {{ font: 800 {u(37)} / normal {MONT}; color: {INK}; white-space: nowrap; }}
selector .ak-d-small {{ position: absolute !important; left: 0; max-width: none !important; }}
selector .ak-d-small p {{ font: 400 {u(18)} / {u(22)} {OPEN}; color: {INK}; }}
{stat_css}/* ===== MÓVIL 430 (375 = × 0,872 por --m); tablet muestra esta versión centrada ===== */
selector .ak-m-hero {{ position: relative !important; width: 100% !important; height: {m(BANNER['hero_m'])} !important; overflow: hidden; }}
selector .ak-m-logo {{ position: absolute !important; left: {ML(24)}; top: {m(36)}; width: {m(119.92)} !important; height: {m(30.65)}; }}
selector .ak-m-name {{ position: absolute !important; left: {ML(24)}; top: {m(95)}; width: auto !important; }}
selector .ak-m-n1 .elementor-heading-title {{ font: 800 {m(nm1)} / 0.964 {MONT}; color: {GOLD}; letter-spacing: {m(tm1)}; white-space: nowrap; }}
selector .ak-m-n2 .elementor-heading-title {{ font: 800 {m(nm2)} / 0.964 {MONT}; color: #fff; letter-spacing: {m(tm2)}; white-space: nowrap; }}
selector .ak-m-sub {{ position: absolute !important; left: {ML(24)}; top: {m(BANNER['titular_top_m'])}; width: {m(382)} !important; }}
selector .ak-m-sub p {{ font: 400 {m(16)} / {m(28)} {MANR}; color: #fff; }}
selector .ak-m-esp {{ position: absolute !important; left: {ML(24)}; top: {m(BANNER['barra_top_m'])}; width: {m(382)} !important; height: {m(181)}; background: url({I['barra-especialidades-movil']}) 0 0 / 100% 100% no-repeat; }}
selector .ak-m-esp-lbl {{ position: absolute !important; left: {m(29)}; top: {m(-28)}; width: auto !important; }}
selector .ak-m-esp-lbl p {{ font: 400 {m(13)} / {m(54)} {SORA}; color: {GOLD}; white-space: nowrap; }}
selector .ak-m-cell {{ position: absolute !important; width: {m(160)} !important; margin-left: {m(-80)} !important; align-items: center !important; }}
''' + ''.join(f"selector .ak-m-cell-{n} {{ left: {m(x)}; top: {m(y)}; }}\n" for n, x, y in [(1, 96, 31), (2, 292, 31), (3, 96, 108.5), (4, 292, 108.5)]) + f'''
selector .ak-m-ico {{ flex: none !important; width: 100% !important; height: {m(23)}; margin-bottom: {m(5)} !important; background-repeat: no-repeat; background-position: center bottom; }}
{m_ico_css}selector .ak-m-cell-t {{ width: 100% !important; }}
selector .ak-m-cell-t p {{ font: 400 {m(12)} / {m(13)} {MANR}; color: #fff; text-align: center; }}
selector .ak-m-sep {{ position: absolute !important; left: {m(188.36)}; width: 1px !important; height: {m(57.5)}; background: rgba(214,167,82,.7); }}
selector .ak-m-sep-1 {{ top: {m(29)}; }} selector .ak-m-sep-2 {{ top: {m(107)}; }}
selector .ak-m-body {{ display: flex; flex-direction: column !important; align-items: center !important; width: 100% !important; padding: {m(20)} 0 !important; background: {BG}; }}
selector .ak-m-card {{ width: {m(390)} !important; max-width: none; box-sizing: border-box; padding: {m(51)} {m(20)} !important; background: #fff; border-radius: {m(20)}; box-shadow: 0 3px 16px rgba(6,8,26,.16); }}
selector .ak-m-h .elementor-heading-title {{ position: relative; box-sizing: border-box; font: 700 {m(26)} / {m(33)} {SORA}; color: {GOLD}; text-transform: uppercase; }}
selector .ak-m-h .elementor-heading-title::before {{ content: ""; position: absolute; background: no-repeat center / 100% 100%; }}
''' + head_m('res', 66, 47, 4, 'icono-resumen', 0, 0, 39.34, 40.36) \
        + head_m('car', SM['car']['lista_top'], 46, 0, 'icono-titulo-cargos', 0, 0.3, 38.34, 30.5) \
        + head_m('for', SM['for']['lista_top'], 47, 3, 'icono-formacion', 4, 0, 31.66, 37.93) \
        + head_m('apo', apo_m_h, 46.5, 0, 'icono-aportes', 0, 1, 35.17, 32.46) + f'''
selector .ak-m-res p {{ margin-left: {m(20)}; width: {m(330)}; font: 400 {m(18)} / {m(34)} {OPEN}; color: {INK}; }}
selector .ak-m-res p + p {{ margin-top: {m(34)}; }}
selector .ak-m-datos {{ width: {m(312)} !important; margin: {m(res_gap_m)} 0 0 {m(20)} !important; box-sizing: border-box; border-left: 2px solid {GOLD}; padding-left: {m(20)} !important; gap: {m(datos_gap)} !important; }}
selector .ak-m-dato {{ width: {m(290)} !important; }}
selector .ak-m-big .elementor-heading-title {{ font: 800 {m(37)} / {m(45)} {MONT}; color: {INK}; white-space: nowrap; }}
selector .ak-m-small p {{ font: 400 {m(18)} / {m(22)} {OPEN}; color: {INK}; }}
{dato_css}selector .ak-m-hr {{ width: 100% !important; height: 1px; margin: {m(50)} 0 {m(49)} !important; background: {LINE}; }}
selector .ak-m-list ul {{ list-style: none; margin: 0 0 0 {m(19)}; padding: 0; width: {m(331)}; }}
selector .ak-m-list li {{ position: relative; padding-left: {m(16)}; margin: 0 0 {m(17)}; font: 400 {m(18)} / {m(28)} {OPEN}; color: {INK}; }}
selector .ak-m-list li::before {{ content: ""; position: absolute; left: 0; top: 0; width: {m(6)}; height: {m(28)}; background: url({I['vineta-movil']}) center / 100% 100% no-repeat; }}
selector .ak-m-arrow li {{ padding-left: {m(28)}; line-height: {m(34)}; }}
selector .ak-m-arrow li::before {{ width: {m(18)}; height: {m(34)}; background-image: url({I['vineta-grande-movil']}); }}
''' + list_css('ak-m', 'car', LM['car'], m, 0, 0, 0) + list_css('ak-m', 'for', LM['for'], m, 0, 0, 0) + list_css('ak-m', 'apo', LM['apo'], m, 0, 0, 0) + f'''
/* ===== cambio de versión: >1024 desktop/laptop, ≤1024 móvil ===== */
@media (max-width: 1024px) {{ selector .ak-d-hero, selector .ak-d-body {{ display: none !important; }} }}
@media (min-width: 1025px) {{ selector .ak-m-hero, selector .ak-m-body {{ display: none !important; }} }}
'''
    root = {"id": E.rid(), "elType": "container",
            "settings": {"content_width": "full", "flex_direction": "column", "flex_wrap": "nowrap", "flex_align_items": "stretch",
                         "flex_gap": {"unit": "px", "column": "0", "row": "0", "isLinked": True, "size": 0},
                         "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
                         "css_classes": cls_root, "custom_css": CSS.strip()},
            "elements": [FONTS, D_HERO, D_BODY, M_HERO, M_BODY], "isInner": False}
    doc = {"content": [root], "page_settings": [], "version": "0.4", "title": nombre_txt, "type": "container"}
    OUT = os.path.join(P, f'{slug}.json')
    json.dump(doc, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    s = json.dumps(doc, ensure_ascii=False)
    assert '"_padding"' not in s and '"_margin"' not in s and '<svg' not in s
    print(f'ok {OUT} ({os.path.getsize(OUT)} bytes, {len(E.ids)} nodos, {s.count(chr(0x2060))} word joiners)')
    os.makedirs(os.path.join(P, '_generador'), exist_ok=True)
    import sim
    sim.render(P, slug, doc)
    return OUT


if __name__ == '__main__':
    construir(sys.argv[1])
