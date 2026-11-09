import base64, json, os, random

random.seed(11)
OUT = r'C:\Users\Consultoría\Documents\cv-ponentes\diana-pereira'
GOLD, NAVY = '#D6A752', '#030A22'
MEDIA = 'https://grupogoberna.com/wp-content/uploads/2026/10/'
IMG = {
    'bg': (MEDIA + 'hero-fondo-capitolio-scaled.webp', 93357),
    'logo': (MEDIA + 'logo-goberna-1.webp', 93358),
    'foto': (MEDIA + 'diana-pereira.webp', 93356),
    'resumen': (MEDIA + 'resumen-ejecutivo.svg', 93367),
    'cargos': (MEDIA + 'cargos-trayectoria.svg', 93362),
    'formacion': (MEDIA + 'formacion-academica.svg', 93364),
    'aportes': (MEDIA + 'aportes-destacados.svg', 93370),
}


def uid():
    return '%07x' % random.getrandbits(28)


def sz(n, unit='px'):
    return {'unit': unit, 'size': n, 'sizes': []}


def pad(t, r, b, l):
    return {'unit': 'px', 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': False}


def gap(c, r=None):
    r = c if r is None else r
    return {'column': str(c), 'row': str(r), 'isLinked': c == r, 'unit': 'px'}


def media(key):
    u, i = IMG[key]
    return {'url': u, 'id': i, 'size': '', 'alt': '', 'source': 'library'}


def gapmask(x, w):
    """Borde con hueco bajo el título: recorta una franja de 3px arriba entre x y x+w (clip-path, sin máscaras)."""
    return ('-webkit-mask:none;mask:none;clip-path:polygon(0 0,%dpx 0,%dpx 3px,%dpx 3px,%dpx 0,100%% 0,100%% 100%%,0 100%%)'
            % (x, x, x + w, x + w))


def gapmask_vw(x, w):
    f = lambda v: '%.3fvw' % (v / 13.66)
    return ('-webkit-mask:none;mask:none;clip-path:polygon(0 0,%s 0,%s 3px,%s 3px,%s 0,100%% 0,100%% 100%%,0 100%%)'
            % (f(x), f(x), f(x + w), f(x + w)))


def data_uri(name):
    p = os.path.join(OUT, 'iconos-webp', name + '.webp')
    return 'data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode()


VW = False  # True mientras se arma la portada: en Laptop los valores escalan con el ancho de pantalla (1366 = diseño de Figma)


def vw(px):
    return {'unit': 'vw', 'size': round(px / 13.66, 3), 'sizes': []}


def padv(t, r, b, l):
    f = lambda v: str(round(v / 13.66, 3))
    return {'unit': 'vw', 'top': f(t), 'right': f(r), 'bottom': f(b), 'left': f(l), 'isLinked': False}


def R(s, key, desk, lap=None, mob=None, tab=None, fn=sz):
    """Valor por dispositivo: Desktop, Laptop (<=1366), Tablet (<=1024), Mobile (<=767)."""
    s[key] = fn(desk) if not isinstance(desk, dict) else desk
    if lap is not None and VW and fn is sz and not isinstance(lap, dict):
        s[key + '_laptop'] = vw(lap)
        if tab is None:
            s[key + '_tablet'] = sz(lap)  # tablet conserva los px de laptop
    elif lap is not None:
        s[key + '_laptop'] = fn(lap) if not isinstance(lap, dict) else lap
    if tab is not None:
        s[key + '_tablet'] = fn(tab) if not isinstance(tab, dict) else tab
    if mob is not None:
        s[key + '_mobile'] = fn(mob) if not isinstance(mob, dict) else mob


def typo(s, prefix, fam, size, weight, lh=None):
    """size y lh: (desktop, laptop, mobile)."""
    s[prefix + 'typography'] = 'custom'
    s[prefix + 'font_family'] = fam
    s[prefix + 'font_weight'] = weight
    R(s, prefix + 'font_size', *[size[0], size[1], size[2]])
    if lh and VW:
        s[prefix + 'line_height'] = sz(lh[0])
        s[prefix + 'line_height_laptop'] = {'unit': 'em', 'size': round(lh[1] / size[1], 4), 'sizes': []}
        s[prefix + 'line_height_tablet'] = sz(lh[1])
        s[prefix + 'line_height_mobile'] = sz(lh[2])
    elif lh:
        R(s, prefix + 'line_height', lh[0], lh[1], lh[2])


def container(settings, elements, classes=None, css=None):
    base = {'content_width': 'full'}
    base.update(settings)
    if classes:
        base['css_classes'] = classes
    if css:
        base['custom_css'] = css
    return {'id': uid(), 'elType': 'container', 'settings': base, 'elements': elements, 'isInner': False}


def widget(wt, settings, classes=None, css=None):
    if classes:
        settings['_css_classes'] = classes
    if css:
        settings['custom_css'] = css
    return {'id': uid(), 'elType': 'widget', 'widgetType': wt, 'settings': settings, 'elements': []}


def heading(text, tag, color, fam, size, weight, lh=None, classes=None, margin=None):
    s = {'title': text, 'header_size': tag, 'title_color': color}
    typo(s, 'typography_', fam, size, weight, lh)
    if margin:
        s['_margin'] = margin
    return widget('heading', s, classes)


def text(html, size, lh, color, classes=None, margin=None, left=None, width=None):
    s = {'editor': html, 'text_color': color}
    typo(s, 'typography_', 'Open Sans', size, '400', lh)
    if margin:
        s['_margin'] = margin
    if left:
        s['_padding'] = pad(0, 0, 0, left[0])
        s['_padding_laptop'] = pad(0, 0, 0, left[1])
        s['_padding_mobile'] = pad(0, 0, 0, left[2])
    if width:
        s['_element_width'] = 'initial'
        R(s, '_element_custom_width', width[0], width[1])
        s['_element_custom_width_mobile'] = sz(100, '%')
    return widget('text-editor', s, classes)


def image(key, width=None, classes=None, margin=None):
    s = {'image': media(key), 'image_size': 'full', 'align': 'left'}
    if width:
        R(s, 'width', width[0], width[1], width[2])
    if margin:
        s['_margin'] = margin[0]
        s['_margin_laptop'] = margin[1]
        if margin[1].get('unit') == 'vw':
            s['_margin_tablet'] = pad(0, 0, 31.3, 0)
        s['_margin_mobile'] = margin[2]
    return widget('image', s, classes)


HEAD_ICON = {'resumen': ('resumen-ejecutivo', 250, 256), 'cargos': ('cargos-trayectoria', 237, 193),
             'formacion': ('formacion-academica', 200, 237), 'aportes': ('aportes-destacados', 218, 200)}


def head(key, title, first=False):
    name, w, h = HEAD_ICON[key]
    k = w / h
    s = {'image': {'url': '', 'id': ''}, 'image_size': 'full', 'title_text': title, 'description_text': '', 'title_size': 'h2',
         'position': 'left', 'text_align': 'left', 'content_vertical_alignment': 'top', 'title_color': GOLD}
    typo(s, 'title_typography_', 'Montserrat', (26, 19, 22.7), '700', (31, 23, 27))
    s['_margin'] = pad(0 if first else 50, 0, 25.4, 0)
    s['_margin_laptop'] = pad(0 if first else 36, 0, 18.2, 0)
    s['_margin_mobile'] = pad(0, 0, 4, 0)
    css = ('selector .elementor-image-box-wrapper{display:flex;align-items:center;text-align:left}'
           'selector .elementor-image-box-wrapper::before{content:"";flex:none;display:block;width:%.1fpx;height:36px;margin-right:9px;'
           'background:url(%s) center/contain no-repeat}'
           'selector .elementor-image-box-content{flex:1;width:auto;text-align:left}'
           'selector .elementor-image-box-title{margin:0 !important;display:block}'
           'selector .elementor-image-box-description{display:none}'
           '@media (max-width:1366px){selector .elementor-image-box-wrapper::before{width:%.1fpx;height:26px;margin-right:6.5px}}'
           '@media (max-width:767px){selector .elementor-image-box-wrapper{align-items:flex-start}'
           'selector .elementor-image-box-wrapper::before{width:%.1fpx;height:30px;margin-right:9px}}'
           % (36 * k, data_uri(name), 26 * k, 30 * k))
    return widget('image-box', s, 'ak-dp-h2', css)


def divider():
    s = {'style': 'solid', 'weight': sz(1), 'color': '#D9DDE6', 'gap': sz(0), 'gap_mobile': sz(16),
         '_margin': pad(24.7, 0, 0, 0), '_margin_laptop': pad(17.7, 0, 0, 0), '_margin_mobile': pad(20, 0, 0, 0)}
    return widget('divider', s, 'ak-dp-linea')


LI = {'punto': ('vineta-punto', 8, 28, 5.7, 20, 6.9, 24), 'flecha': ('vineta-flecha', 18, 28, 12.9, 20, 18.6, 29)}


def bullets(items, kind, mob_lh):
    s = {'icon_list': [{'text': t, 'selected_icon': {'value': '', 'library': ''}, '_id': uid()} for t in items],
         'text_color': NAVY, 'text_indent': sz(0)}
    R(s, 'space_between', 20, 14.2, 14.8)
    typo(s, 'icon_typography_', 'Open Sans', (17.8, 12.8, 15.7), '400', (27.6, 19.9, mob_lh))
    s['_margin'] = pad(0, -12, 0, 0)
    s['_margin_laptop'] = pad(0, -8, 0, 0)
    s['_margin_mobile'] = pad(0, 0, 0, 0)
    s['_padding'] = pad(0, 0, 0, 61)
    s['_padding_laptop'] = pad(0, 0, 0, 44)
    s['_padding_mobile'] = pad(0, 0, 0, 17)
    name, wd, hd, wl, hl, wm, hm = LI[kind]
    css = ('selector .elementor-icon-list-item{align-items:flex-start}'
           'selector .elementor-icon-list-item::before{content:"";flex:none;display:block;width:%gpx;height:%gpx;margin-right:10px;'
           'background:url(%s) center/contain no-repeat}'
           '@media (max-width:1366px){selector .elementor-icon-list-item::before{width:%gpx;height:%gpx;margin-right:7.1px}}'
           '@media (max-width:767px){selector .elementor-icon-list-item::before{width:%gpx;height:%gpx;margin-right:10px}}'
           % (wd, hd, data_uri(name), wl, hl, wm, hm))
    return widget('icon-list', s, 'ak-dp-lista', css)


def stat(big, small, last=False):
    lab = text('<p>%s</p>' % small, (17.8, 12.8, 15.7), (21.7, 16.2, 19.2), NAVY, 'ak-dp-dato',
               margin=pad(0, 0, 0 if last else 38.5, 0))
    lab['settings']['_margin_laptop'] = pad(0, 0, 0 if last else 27.4, 0)
    lab['settings']['_margin_mobile'] = pad(0, 0, 0 if last else 24.4, 0)
    return [heading(big, 'h3', NAVY, 'Montserrat', (37, 27, 32.3), '800', (42.4, 30.6, 38.8), 'ak-dp-cifra'), lab]


# ============ HERO ============
VW = True
esp_items = [('Gobierno', 'gobierno-pin', 181, 231), ('Asuntos<br>Internacionales', 'asuntos-internacionales', 237, 237),
             ('Defensa y<br>Seguridad', 'defensa-seguridad', 206, 231), ('Liderazgo y<br>Gestión de Crisis', 'liderazgo-gestion-crisis', 231, 231)]
esp, esp_css, esp_css_vw = [], '', ''
for i, (label, icon, w, h) in enumerate(esp_items):
    s = {'image': {'url': '', 'id': ''}, 'image_size': 'full', 'title_text': label, 'description_text': '', 'title_size': 'div',
         'position': 'top', 'text_align': 'center', 'title_color': '#FFFFFF', 'content_vertical_alignment': 'top',
         '_element_width': 'initial', '_border_border': 'solid', '_border_color': 'rgba(255,255,255,0.25)'}
    R(s, '_element_custom_width', 25, 25, 50, fn=lambda v: sz(v, '%'))
    s['_border_width'] = pad(0, 0, 0, 0 if i == 0 else 1)
    s['_border_width_mobile'] = pad(0, 0, 0, 1 if i % 2 else 0)
    s['_padding'] = pad(0, 6, 0, 6)
    s['_padding_mobile'] = pad(0, 8, 0, 8)
    typo(s, 'title_typography_', 'Open Sans', (18, 13, 10.5), '400', (24, 17, 11.3))
    esp.append(widget('image-box', s, 'ak-dp-ico-%d' % (i + 1)))
    k = w / h
    esp_css += ('selector .ak-dp-ico-%d .elementor-image-box-wrapper::before{content:"";display:block;width:%.1fpx;height:37px;margin:0 auto 9px;'
                'background:url(%s) center/contain no-repeat}'
                '@media (max-width:1366px){selector .ak-dp-ico-%d .elementor-image-box-wrapper::before{width:%.1fpx;height:27px;margin-bottom:6px}}'
                '@media (max-width:767px){selector .ak-dp-ico-%d .elementor-image-box-wrapper::before{width:%.1fpx;height:20px;margin-bottom:4px}}'
                % (i + 1, 37 * k, data_uri(icon), i + 1, 27 * k, i + 1, 20 * k))
    esp_css_vw += ('selector .ak-dp-ico-%d .elementor-image-box-wrapper::before{width:%.3fvw;height:%.3fvw;margin-bottom:%.3fvw}'
                   % (i + 1, 27 * k / 13.66, 27 / 13.66, 6 / 13.66))

esp_label = heading('Especialidades', 'div', GOLD, 'Montserrat', (25, 18, 11.3), '400', (30, 22, 14), 'ak-dp-esp-t')
fonts_hidden = [text('<p>.</p>', (14, 14, 14), (20, 20, 20), '#000000', 'ak-dp-fuentes'),
                widget('text-editor', {'editor': '<p>.</p>', 'typography_typography': 'custom', 'typography_font_family': 'Sora',
                                       'typography_font_weight': '700'}, 'ak-dp-fuentes'),
                widget('text-editor', {'editor': '<p>.</p>', 'typography_typography': 'custom', 'typography_font_family': 'Manrope',
                                       'typography_font_weight': '400'}, 'ak-dp-fuentes')]

esp_box = container({
    'flex_direction': 'row', 'flex_wrap': 'nowrap', 'flex_wrap_mobile': 'wrap', 'flex_align_items': 'flex-start',
    'flex_justify_content': 'center', 'flex_gap': gap(0, 18), 'flex_gap_mobile': gap(0, 17.6),
    'margin': pad(82, 0, 0, 0), 'margin_laptop': padv(57.3, 0, 0, 0), 'margin_tablet': pad(57, 0, 0, 0), 'margin_mobile': pad(29, 0, 0, 0)}, [esp_label] + esp, 'ak-dp-esp')
R(esp_box['settings'], 'width', 810, 584, 333)
esp_box['settings']['width_mobile'] = sz(100, '%')
esp_box['settings']['padding'] = pad(40, 16, 32, 16)
esp_box['settings']['padding_laptop'] = padv(29, 12, 24.4, 12)
esp_box['settings']['padding_tablet'] = pad(29, 12, 24.4, 12)
esp_box['settings']['padding_mobile'] = pad(27, 0, 16, 0)

lead = text('<p>Profesional en Gobierno y Relaciones Internacionales, con experiencia en seguridad y liderazgo estratégico.</p>',
            (28, 20, 14), (47, 34.5, 24.4), '#FFFFFF', 'ak-dp-lead', margin=pad(15.8, 0, 0, 0), width=(810, 584))
lead['settings']['_margin_laptop'] = padv(11.4, 0, 0, 0)
lead['settings']['_margin_tablet'] = pad(11.4, 0, 0, 0)
lead['settings']['_margin_mobile'] = pad(14, 0, 0, 0)

hero_css = (
    'selector{position:relative}'
    'selector::before{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;background:linear-gradient(90deg,rgba(3,10,34,.4) 0,rgba(3,10,34,.15) 50%,rgba(3,10,34,0))}'
    'selector .e-con-inner>*:not(.ak-dp-foto){position:relative;z-index:2}'
    'selector .ak-dp-foto{position:absolute;top:0;left:39.5%;width:60.5%;max-width:none;z-index:1;pointer-events:none;margin:0}'
    'selector .ak-dp-foto img{width:100%;height:auto;display:block}'
    'selector .ak-dp-esp{position:relative}'
    'selector .ak-dp-esp::before{content:"";position:absolute;inset:0;border:1px solid #D6A752;border-radius:8px;pointer-events:none;'
    + gapmask(30, 210) + '}'
    'selector .ak-dp-esp-t{position:absolute !important;top:-15px;left:41px;width:auto;margin:0}'
    'selector .ak-dp-fuentes{display:none}'
    + esp_css +
    '@media (max-width:1366px){'
    'selector .ak-dp-esp::before{' + gapmask(22, 151) + '}'
    'selector .ak-dp-esp-t{top:-11px;left:30px}}'
    '@media (min-width:1025px) and (max-width:1366px){'
    + esp_css_vw +
    'selector .ak-dp-esp::before{' + gapmask_vw(22, 151) + '}'
    'selector .ak-dp-esp-t{top:-0.805vw;left:2.196vw}}'
    '@media (max-width:1024px){'
    'selector .ak-dp-foto{position:relative;left:auto;width:100%;max-height:420px;overflow:hidden;order:-1}'
    'selector .ak-dp-foto img{max-width:560px;margin:0 auto}}'
    '@media (max-width:767px){'
    'selector{background-size:1494px 841px !important;background-position:center -29px !important}'
    'selector::before{background:linear-gradient(180deg,rgba(0,0,0,.42) 0,rgba(0,0,0,0) 478px),rgba(2,7,21,.68)}'
    'selector .ak-dp-foto{position:absolute;order:0;left:auto;right:0;bottom:-1px;top:auto;width:100%;height:340px;max-height:none;overflow:hidden;z-index:1}'
    'selector .ak-dp-foto .elementor-widget-container{position:relative;height:100%}'
    'selector .ak-dp-foto img{position:absolute;max-width:none;height:160.81%;width:146.12%;left:-25.98%;top:-13.4%;margin:0}'
    'selector .ak-dp-esp::before{' + gapmask(18, 100) + '}'
    'selector .ak-dp-esp-t{top:-7px;left:25px}'
    'selector .ak-dp-esp-t .elementor-heading-title{font-family:"Sora",sans-serif}'
    'selector .ak-dp-lead p,selector .ak-dp-esp .elementor-image-box-title{font-family:"Manrope",sans-serif}}')

hero = container({
    'content_width': 'boxed', 'flex_direction': 'column', 'flex_gap': gap(0),
    'background_background': 'classic', 'background_image': media('bg'), 'background_position': 'initial',
    'background_xpos': sz(50, '%'), 'background_ypos': sz(20, '%'), 'background_size': 'cover', 'overflow': 'hidden'},
    [image('logo', (182, 131, 105), 'ak-dp-logo', margin=(pad(0, 0, 43.5, 0), padv(0, 0, 31.3, 0), pad(0, 0, 25, 0))),
     heading('DIANA', 'h1', GOLD, 'Montserrat', (63, 45, 27), '800', (62, 46, 26), 'ak-dp-nombre'),
     heading('PEREIRA', 'h1', '#FFFFFF', 'Montserrat', (86, 62, 36.6), '800', (85, 61, 35), 'ak-dp-apellido'),
     lead, esp_box, image('foto', None, 'ak-dp-foto')] + fonts_hidden,
    'ak-dp-hero', hero_css)
hero['settings']['boxed_width'] = sz(1500)
hero['settings']['boxed_width_laptop'] = sz(79, '%')
hero['settings']['boxed_width_tablet'] = sz(100, '%')
hero['settings']['boxed_width_mobile'] = sz(100, '%')
R(hero['settings'], 'min_height', 839, 604.7, 812)
hero['settings']['min_height_tablet'] = sz(0)
hero['settings']['padding'] = pad(100, 0, 40, 0)
hero['settings']['padding_laptop'] = padv(72, 0, 29, 0)
hero['settings']['padding_tablet'] = pad(72, 0, 29, 0)
hero['settings']['padding_mobile'] = pad(31, 21, 0, 21)

VW = False

# ============ TARJETA ============
resumen = text('<p><strong>Profesional en Gobierno y Relaciones Internacionales</strong>, con formación en la Escuela de Asuntos Internacionales y Públicos de la Universidad de Columbia y <strong>quince años de experiencia en el sector público colombiano</strong>. Su trayectoria comprende la gestión de crisis y el liderazgo de equipos en entornos complejos. Ha sido <strong>directora de Estudios Estratégicos del Ministerio de Defensa Nacional</strong> y <strong>asesora de la Dirección para la Ejecución de Gobierno y Áreas Estratégicas</strong> de la Presidencia de la República de Colombia. Ha participado en publicaciones del Departamento Nacional de Planeación sobre seguridad y consolidación de la paz. Es <strong>creadora de la metodología Brújula de Mando Estratégico</strong>, orientada al fortalecimiento del liderazgo corporativo e inspirada en principios de las Fuerzas Especiales.</p>',
               (17.8, 12.8, 15.7), (33.6, 24.2, 29.6), NAVY, 'ak-dp-resumen', left=(61, 44, 17))

# Datos en móvil: dentro de Resumen, justo después del texto (en Desktop y Laptop quedan ocultos)
datos_m = container({'flex_direction': 'column', 'flex_gap': gap(0), 'border_border': 'solid',
                     'border_width': pad(0, 0, 0, 2), 'border_color': GOLD,
                     'padding': pad(0, 0, 0, 17), 'margin': pad(43, 0, 0, 17)},
                    stat('15 años', 'Experiencia en el sector público') + stat('3', 'Cargos principales') +
                    stat('2010-2012', 'Columbia University', True), 'ak-dp-datos-m')
datos_m['settings']['flex_gap'] = gap(0)

main = container({'flex_direction': 'column', 'flex_gap': gap(0), 'flex_gap_mobile': gap(14), 'width_tablet': sz(100, '%'), 'width_mobile': sz(100, '%')},
                 [head('resumen', 'RESUMEN EJECUTIVO', True), resumen, datos_m, divider(),
                  head('cargos', 'CARGOS PRINCIPALES Y TRAYECTORIA'),
                  bullets(['Directora de Estudios Estratégicos – Ministerio de Defensa Nacional de Colombia.',
                           'Asesora de la Dirección para la Ejecución de Gobierno y Áreas Estratégicas – Presidencia de la República de Colombia.',
                           'Creadora de la metodología Brújula de Mando Estratégico.'], 'punto', 24.4), divider(),
                  head('formacion', 'FORMACIÓN ACADÉMICA'),
                  bullets(['Estudios en la Escuela de Asuntos Internacionales y Públicos de la Universidad de Columbia (2010–2012).',
                           'Diplomado en Gestión de Proyectos con énfasis en el Project Management Institute (PMI) – Universidad EAFIT (2022).',
                           'Programa de Liderazgo de Alto Desempeño – Blum.'], 'punto', 24.4), divider(),
                  head('aportes', 'APORTES DESTACADOS'),
                  bullets(['Desarrolló Brújula de Mando Estratégico, metodología para fortalecer el liderazgo corporativo y el funcionamiento de los equipos.',
                           'Registra en su perfil la publicación "Defense and Security Spending 1998–2013: Evolution and reflections on its sustainability", vinculada al Boletín de Seguimiento a la Consolidación de la Paz del Departamento Nacional de Planeación.',
                           'Fue entrevistada como experta para una investigación sobre reincidencia en el hurto de dispositivos móviles en Bogotá, publicada en la revista Logos, Ciencia & Tecnología.'], 'flecha', 29.6)],
                 'ak-dp-main')
R(main['settings'], 'width', 801, 578)

side = container({'flex_direction': 'column', 'flex_gap': gap(0), 'border_border': 'solid',
                  'border_width': pad(0, 0, 0, 1), 'border_color': GOLD,
                  'width_tablet': sz(100, '%'),
                  'sticky': 'top', 'sticky_on': ['desktop', 'laptop'], 'sticky_offset': 80, 'sticky_offset_laptop': 58, 'sticky_parent': 'yes'},
                 stat('15 años', 'Experiencia en el sector público') + stat('3', 'Cargos principales') +
                 stat('2010-2012', 'Columbia University', True), 'ak-dp-side')
R(side['settings'], 'width', 460, 331)
side['settings']['padding'] = pad(7, 0, 8, 78)
side['settings']['padding_laptop'] = pad(5, 0, 6, 56)
side['settings']['padding_tablet'] = pad(24, 0, 0, 0)
side['settings']['margin'] = pad(1, 0, 0, 0)
side['settings']['margin_laptop'] = pad(1, 0, 0, 0)

card_css = (
    'selector{max-width:100%}'
    'selector .ak-dp-datos-m{display:none}'
    'selector .ak-dp-fuentes{display:none}'
    'selector .ak-dp-resumen p,selector .ak-dp-dato p{margin:0}'
    '@media (max-width:767px){'
    'selector .ak-dp-datos-m{display:flex}'
    'selector .ak-dp-side{display:none}'
    'selector .ak-dp-h2 .elementor-image-box-title{font-family:"Sora",sans-serif}'
    'selector .ak-dp-resumen strong:not(:first-child){font-weight:400}'
    '}')

cols = container({'flex_direction': 'row', 'flex_direction_tablet': 'column', 'flex_direction_mobile': 'column',
                  'flex_align_items': 'flex-start', 'width': sz(100, '%'),
                  'flex_gap': gap(78, 24), 'flex_gap_laptop': gap(56, 24), 'flex_gap_mobile': gap(0, 0)},
                 [main, side], 'ak-dp-cols')

card = container({
    'flex_direction': 'column', 'flex_align_items': 'stretch',
    'background_background': 'classic', 'background_color': '#FFFFFF', 'box_shadow_box_shadow_type': 'yes',
    'box_shadow_box_shadow': {'horizontal': 0, 'vertical': 3, 'blur': 16, 'spread': 0, 'color': 'rgba(6,8,26,0.16)'}},
    [cols], 'ak-dp-card', card_css)
R(card['settings'], 'width', 1500, 1081)
card['settings']['width_tablet'] = sz(100, '%')
card['settings']['width_mobile'] = sz(100, '%')
card['settings']['padding'] = pad(79, 80, 81, 80)
card['settings']['padding_laptop'] = pad(57, 58, 58, 58)
card['settings']['padding_mobile'] = pad(44, 17, 44, 17)
card['settings']['border_radius'] = pad(20, 20, 20, 20)
card['settings']['border_radius_mobile'] = pad(17, 17, 17, 17)

fondo = container({'flex_direction': 'column', 'flex_align_items': 'center', 'background_background': 'classic',
                   'background_color': '#F3F6FB', 'padding': pad(79, 16, 79, 16), 'padding_laptop': pad(57, 16, 57, 16), 'padding_mobile': pad(17, 17, 17, 17)},
                  [card], 'ak-dp-fondo')

tpl = {'version': '0.4', 'title': 'Diana Pereira - CV Ponente', 'type': 'page', 'content': [hero, fondo],
       'page_settings': [], 'metadata': []}
path = os.path.join(OUT, 'diana-pereira.json')
json.dump(tpl, open(path, 'w', encoding='utf8'), ensure_ascii=False, indent=2)


def count(e):
    return (1 if e['elType'] == 'container' else 0) + sum(count(x) for x in e['elements'])


print('ok', os.path.getsize(path) // 1024, 'KB; contenedores:', sum(count(e) for e in tpl['content']))
