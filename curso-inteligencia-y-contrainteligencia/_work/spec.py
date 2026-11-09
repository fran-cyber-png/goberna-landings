# Cambios de Inteligencia y Contrainteligencia sobre la base de Director de Seguridad (se ejecuta dentro de transform.py)
# Fuente: Figma 7WiwZ8uhRQiZ2LvqLtw9h9, frame 4005:17 (INTELIGENCIA Y CONTRAINTELIGENCIA – v1) + frame 357:626 (Background,
# Experiencia Goberna) + PDF "CONTENIDO LANDINGS (7)" (_work/pdf7.txt; el contenido manda: textos solo del PDF).
# El Figma de CII comparte el layout del de Carrera Diplomática: las posiciones calibradas en Carrera se repiten aquí.
import base64, io, shutil
from PIL import Image as _Img

# imágenes nuevas -> carpeta de la vista previa
for _f in os.listdir(os.path.join(ROOT, 'imagenes')):
    shutil.copy(os.path.join(ROOT, 'imagenes', _f), os.path.join(P, 'a', _f))

SLUG = 'inteligencia-contrainteligencia'
G, G_HOVER, G_LIGHT = '#00C587', '#00A673', '#33D19F'      # verde de acento del Figma
DARK = '#001710'                                          # oscuro de títulos y fondos del Figma
BODY = 'rgba(6,6,6,0.75)'                                 # texto de párrafos del Figma (#060606 al 75 %)
LIGHT_BG, PANEL_BG = '#FDFCFB', '#F2F4F7'

# imágenes que ya están en la Biblioteca de medios (se reutilizan: no hay que subirlas)
REUSE = {
    'card-eduardo-de-la-torre-1-1-1-1.webp': ('https://grupogoberna.com/wp-content/uploads/2026/10/card-eduardo-de-la-torre-1-1-1-1.webp', '93704'),
    'gonzalo-catanzariti-1.webp': ('https://grupogoberna.com/wp-content/uploads/2026/10/gonzalo-catanzariti-1.webp', '93700'),
    'card-roberto-bazan-2.webp': ('https://grupogoberna.com/wp-content/uploads/2026/10/card-roberto-bazan-2.webp', '93264'),
    'bandera-estados-unidos.png': ('https://grupogoberna.com/wp-content/uploads/2026/10/bandera-estados-unidos.png', '93236'),
    'bandera-peru-1.png': ('https://grupogoberna.com/wp-content/uploads/2026/10/bandera-peru-1.png', '93889'),
    'logo-goberna-blanco.png': ('https://grupogoberna.com/wp-content/uploads/2026/10/logo-goberna-blanco.png', '93244'),
}
def wp(name):
    if name in REUSE: return REUSE[name]
    u = UPLOADS.get(name)
    return (u['url'], u['id']) if u else (WP + name, '')

# ---------------------------------------------------------------- utilidades propias
def remove_top(i):
    """Quita una sección completa (JSON y vista previa)."""
    global HTML
    J['content'] = [c for c in J['content'] if c['id'] != i]
    try:
        s, e = el_span(HTML, i); HTML = HTML[:s] + HTML[e:]
    except KeyError:
        LOG.append('(vista previa) ' + i + ' no estaba en la página publicada')

def acc_titles(acc_id, titles):
    for k, t in enumerate(titles): S(acc_id)['items'][k]['item_title'] = t
    it = iter(titles)
    html_sub_in(acc_id, lambda blk: re.sub(r'(<div class="e-n-accordion-item-title-text">)(.*?)(</div>)',
                                           lambda m: m.group(1) + ' ' + next(it) + ' ' + m.group(3), blk, flags=re.S))

def acc_keep(acc_id, n):
    """Deja solo los primeros n ítems del acordeón anidado (JSON y vista previa)."""
    acc = ELEM[acc_id]
    acc['settings']['items'] = acc['settings']['items'][:n]
    for e in acc['elements'][n:]: ELEM.pop(e['id'], None)
    acc['elements'] = acc['elements'][:n]
    def f(blk):
        ds = list(re.finditer(r'<details\b.*?</details>', blk, flags=re.S))
        for m in reversed(ds[n:]): blk = blk[:m.start()] + blk[m.end():]
        return blk
    html_sub_in(acc_id, f)

def kids(i): return [c['id'] for c in ELEM[i].get('elements', [])]

def recolor_datauri(i, rgb):
    """Recolorea los íconos webp incrustados en el CSS personalizado del elemento i (mantiene la transparencia)."""
    cc = S(i)['custom_css']
    def f(m):
        im = _Img.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGBA')
        a = im.getchannel('A'); im = _Img.new('RGBA', im.size, rgb + (255,)); im.putalpha(a)
        b = io.BytesIO(); im.save(b, 'WEBP', lossless=True)
        return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    S(i)['custom_css'] = re.sub(r'data:image/webp;base64,([A-Za-z0-9+/=]+)', f, cc)

def typo_scale(i, size, lh=None, ls=None, lh_unit='px'):
    """Tamaño del Figma en desktop; laptop y mobile escalan con la misma proporción que tenía la base."""
    s = S(i); old = s['typography_font_size']['size']; r = size / old; kw = {'size': size}
    for d in ('_laptop', '_mobile'):
        o = s.get('typography_font_size' + d)
        if o and o.get('size'): kw['size' + d] = round(o['size'] * r, 1)
    if lh is not None:
        kw['lh'] = lh; kw['lh_unit'] = lh_unit
        if lh_unit == 'px':
            for d in ('_laptop', '_mobile'):
                if 'size' + d in kw: kw['lh' + d] = round(lh * kw['size' + d] / size, 1)
    if ls is not None:
        kw['ls'] = ls
        for d in ('_laptop', '_mobile'):
            if 'size' + d in kw: kw['ls' + d] = round(ls * kw['size' + d] / size, 2)
    typo(i, **kw)

def bgc(i, col):
    """Color de fondo de un contenedor: ajuste del JSON + la regla que genera Elementor."""
    global CSS
    setv(i, background_color=col)
    pat = r'(\.elementor-element-%s:not\(\.elementor-motion-effects-element-type-background\)[^{}]*\{[^}]*?background-color:)([^;}]+)' % i
    CSS, n = re.subn(pat, lambda m: m.group(1) + col, CSS)
    if not n: EXTRA_CSS.append(pre(i) + ':not(.elementor-motion-effects-element-type-background){background-color:' + col + '}')

def css_var(i, var, val, media='@media(min-width:933px){'):
    """Cambia una variable (--width, --content-width...) del elemento i dentro del bloque @media que genera Elementor."""
    global CSS
    k = CSS.find(media); assert k >= 0, media
    d = 0
    for e in range(k + len(media) - 1, len(CSS)):
        if CSS[e] == '{': d += 1
        elif CSS[e] == '}':
            d -= 1
            if d == 0: break
    blk = CSS[k:e]
    pat = r'(elementor-element-%s(?![0-9a-f])[^{}]*\{[^}]*?%s:)([^;}]+)' % (i, re.escape(var))
    blk2, n = re.subn(pat, lambda m: m.group(1) + val, blk)
    assert n, (i, var, media)
    CSS = CSS[:k] + blk2 + CSS[e:]

def rule_sub(i, old, new, k=0):
    """Reemplaza old por new en la k-ésima regla generada del elemento i que lo contiene (vista previa)."""
    global CSS
    rules = [m for m in re.finditer(r'[^{}]*elementor-element-%s(?![0-9a-f])[^{}]*\{[^}]*\}' % i, CSS) if old in m.group(0)]
    assert len(rules) > k, (i, old)
    m = rules[k]; CSS = CSS[:m.start()] + m.group(0).replace(old, new) + CSS[m.end():]

def img(name): return name.replace('.webp', '-' + SLUG + '.webp')

# ============ 0. Secciones que no van: Alianza y footer (no están en el Figma).
# Experiencia Goberna (6a12cc55) se queda: es el frame «Background» del Figma, adaptado a la paleta de CII.
for _i in ('5b1123a8', '1222dd86'):
    remove_top(_i)
PREVIEW_CSS += '.elementor-93575 > .elementor-element-1222dd86{display:none!important}'

# ============ 1. Paleta (Figma: verde #00C587, oscuro #001710)
replace_everywhere([
    ('#FFBB03', G), ('rgba(255,187,3,', 'rgba(0,197,135,'), ('rgba(255, 187, 3,', 'rgba(0, 197, 135,'),
    ('#FDC733', G_LIGHT), ('#FFD466', '#5BE0B5'),
    ('#15262F', DARK),
])
# fondos claros (Figma: #FDFCFB en Metodología / Plan / banner, #F2F4F7 en paneles)
bgc('3f83c2c', LIGHT_BG)
bgc('7c39e8aa', LIGHT_BG)
bgc('66c6bdeb', LIGHT_BG)
bgc('2cd97d01', PANEL_BG)
bgc('54c4c5af', PANEL_BG)
bgc('521f33e5', PANEL_BG)
for _q in ('113px', '65px', '64px', '30px'):        # barra de datos montada sobre metodología
    css_sub('58716df6', f'transparent {_q}, #F3F5F7 {_q}', f'transparent {_q}, {LIGHT_BG} {_q}')
css_sub('56bf8b99', '.e-n-tabs-content { background: #F3F5F7;', '.e-n-tabs-content { background: ' + PANEL_BG + ';')
css_sub('54c4c5af', 'linear-gradient(#F3F5F7, #F3F5F7) padding-box', 'linear-gradient(' + PANEL_BG + ', ' + PANEL_BG + ') padding-box')

# ============ 2. Header (botón verde, texto oscuro como el Figma)
setv('4aa3f0b1', button_background_hover_color=G_HOVER)

# ============ 3. Hero (PDF: «Diploma Internacional de Inteligencia y Contrainteligencia»; título en imagen del Figma)
heading('17c98689', 'Diploma Internacional de Inteligencia y Contrainteligencia')
image('1916fb3', img('titulo.webp'))
img_width('1916fb3', w=749, w_laptop=533, w_mobile=340)
remove('6b6388d')                                   # el Figma no trae subtítulo (el lema del PDF va en Metodología)
bg_image('2742d6b5', img('hero-fondo.webp'), 'a/hero-fondo-director.webp')
setv('4be49e01', button_background_hover_color=G_HOVER)
setv('9c2fe2d', border_color='#707070'); EXTRA_CSS.append(pre('9c2fe2d') + ' .elementor-button{border-color:#707070}')
button('263d369c', 'Descargar brochure del programa', '#')
button('4be49e01', 'Reserva tu vacante')

# ============ 4. Barra de datos (PDF)
heading('5d6fff46', 'Online')
heading('6919d0e7', '09 de diciembre')
heading('2fda4138', '19:00 hrs. GMT-5')
heading('4209211c', '8 módulos · 4 semanas')      # PDF: «· 120 horas académicas» no entra en la celda (va en Plan y FAQ)
heading('4c8ed0ee', 'USD $199')
color('12c0a15', '#000000'); color('4c8ed0ee', '#000000')   # caja de Inversión: texto negro (pedido del usuario)

# ============ 5. Metodología
heading('77542da8', 'Metodología')
heading('b86c8ae', 'De la información a la<br> <span class="ak-g">acción estratégica</span>')
text('390db8e4', '<p>Anticipa amenazas, protege información estratégica y convierte datos en decisiones.</p>')
color('390db8e4', BODY)
image('40d9161c', img('metodologia-video.webp'))
text('4510a4fd', '<p>Analiza <span>•</span> Anticipa <span>•</span> Protege <span>•</span> Decide</p>')
typo_scale('4510a4fd', 18)

# ============ 6. El programa (PDF: «Información del programa»)
heading('80fac6b', 'El programa'); typo('80fac6b', weight=400)
heading('37799678', 'Analiza escenarios, anticipa riesgos<br class="ak-dk"> y aplica inteligencia y<br class="ak-dk"> contrainteligencia para <span class="ak-g">proteger<br class="ak-dk"> organizaciones, proyectos y<br class="ak-dk"> decisiones estratégicas.</span>')
typo_scale('37799678', 32, lh=41, ls=-1.02)
# brillo verde abajo a la izquierda (Figma: «Enmascarar grupo 107» al 36 %)
css_sub('56bf8b99', 'gap: 0 !important; background: #001710;', 'gap: 0 !important; background: radial-gradient(ellipse 540px 280px at 540px 100%, rgba(0,197,135,.18), rgba(0,197,135,0)), #001710;')
heading('5a5d4853', 'Objetivo del diploma')
text('1e2e258a', '<p>Formarte para <strong>analizar escenarios, anticipar riesgos y aplicar herramientas de inteligencia y contrainteligencia que permitan proteger organizaciones, proyectos y decisiones estratégicas.</strong></p>'
                 '<p>Durante el diploma desarrollarás capacidades para identificar amenazas, gestionar información crítica y fortalecer la seguridad operativa en contextos de alta complejidad.</p>')
heading('3dff5c49', '¿A quiénes está dirigido?')
text('2d2f5c00', '<p>Dirigido a:</p><ul>'
                 '<li>Profesionales y funcionarios vinculados a inteligencia, seguridad y defensa.</li>'
                 '<li>Fuerzas Armadas y Policía Nacional.</li>'
                 '<li>Autoridades, asesores políticos y candidatos a cargos públicos.</li>'
                 '<li>Analistas de inteligencia, investigadores y consultores estratégicos.</li>'
                 '<li>Profesionales de seguridad corporativa, ciberseguridad y gestión de riesgos.</li>'
                 '<li>Politólogos, estudiantes y profesionales interesados en inteligencia aplicada.</li></ul>')
heading('36ba7119', 'Perfil del egresado')
text('73081eaa', '<p>Al finalizar el diploma estarás preparado para identificar amenazas, analizar información estratégica y diseñar respuestas orientadas a proteger activos críticos de una organización.</p>'
                 '<p>Podrás desenvolverte en:</p>'
                 '<p>Inteligencia estratégica · Contrainteligencia · Análisis de riesgos · Seguridad corporativa · Ciberinteligencia · Gestión de crisis · Investigación · Asesoría estratégica</p>')
for _i in ('1e2e258a', '2d2f5c00', '73081eaa'): color(_i, BODY)
recolor_datauri('56bf8b99', (0, 197, 135))         # viñeta de la lista "Dirigido a"

# ============ 7. Metodología de aprendizaje (War Room) — títulos cortos de etapa (decisión del usuario, 23 oct)
heading('24484833', 'Metodología de aprendizaje'); typo('24484833', weight=400)
heading('a50a77b', 'Aquí la información se<br> convierte en <span class="ak-g">acción<br> estratégica</span>')
typo('a50a77b', ls=-1, ls_laptop=-0.7, ls_mobile=-0.5)
text('3079ff74', '<p>El diploma combina fundamentos de inteligencia con aplicación práctica mediante la metodología Cuarteles War Room, donde los participantes desarrollan capacidades para analizar amenazas y responder ante escenarios complejos.</p>')
for _t, _h, _p in (('7a82957e', 'Aprende', 'Comprende los principios, ciclos y metodologías de inteligencia y contrainteligencia.'),
                   ('245ad6bc', 'Analiza', 'Aplica herramientas de análisis para identificar riesgos, amenazas y oportunidades.'),
                   ('544064c5', 'Trabaja', 'Desarrolla ejercicios prácticos orientados a la toma de decisiones estratégicas.'),
                   ('1f78edf1', 'Protege', 'Fortalece capacidades para prevenir filtraciones y reducir vulnerabilidades.')):
    heading(_t, _h); typo(_t, family='Montserrat')
    _txt = [k for k in kids(PARENT[_t]['id']) if ELEM[k].get('widgetType') == 'text-editor'][0]
    text(_txt, '<p>' + _p + '</p>')
bg_image('3028d48c', img('war-room-fondo.webp'), 'a/war-room-fondo-director-1.webp')
bg_image('3028d48c', img('war-room-fondo-movil.webp'), key='background_image_mobile')
css_global('a/war-room-fondo-movil-director.webp', 'a/' + img('war-room-fondo-movil.webp'))
css_global('https://grupogoberna.com/wp-content/uploads/2026/10/war-room-fondo-movil-director.webp', 'a/' + img('war-room-fondo-movil.webp'))

# ============ 8. Plan de estudios (PDF 7, 24 oct: 8 módulos con descripción, Aprenderás y Aplicarás)
heading('48da84d4', 'Una formación para entender, anticipar y proteger')
heading('5d85f006', '8')
heading('1db9c1b2', '120')
button('3954484a', 'Descargar brochure', '#')
MODS = [
    ('Fundamentos de Inteligencia y Contrainteligencia',
     'Comprende cómo funciona la inteligencia y cuál es el papel de la contrainteligencia en la protección de una organización.',
     'Principios de inteligencia, ciclo de inteligencia, fundamentos y procesos de contrainteligencia.',
     'Análisis del ciclo de inteligencia e identificación de medidas para proteger información y capacidades críticas.'),
    ('Inteligencia Estratégica',
     'Transforma información en conocimiento útil para anticipar escenarios y respaldar decisiones de alto nivel.',
     'Hipótesis, modelos de análisis, indicadores de alerta, prospectiva e inteligencia estratégica.',
     'Construcción de escenarios e indicadores para detectar riesgos y sustentar decisiones estratégicas.'),
    ('OSINT: Inteligencia de Fuentes Abiertas',
     'Aprende a buscar, verificar y organizar información pública para convertirla en un insumo confiable de inteligencia.',
     'Fuentes abiertas, motores de búsqueda, técnicas de búsqueda, validación y organización de información.',
     'Proceso de búsqueda y verificación de información para construir un producto de análisis OSINT.'),
    ('SOCMINT, Ciberinteligencia y Ciberseguridad',
     'Comprende cómo el entorno digital genera nuevas fuentes de información, pero también nuevas vulnerabilidades.',
     'SOCMINT, seguridad de la información, comunicaciones seguras, criptografía, IA, IoT y riesgos digitales.',
     'Identificación de amenazas y vulnerabilidades digitales para fortalecer la protección de información estratégica.'),
    ('COMINT: Inteligencia de Comunicaciones',
     'Conoce cómo la información proveniente de comunicaciones puede convertirse en inteligencia relevante para la seguridad y la toma de decisiones.',
     'Principios de COMINT, procesamiento de señales de comunicación, análisis de información y detección de amenazas.',
     'Interpretación de información de comunicaciones para identificar señales y apoyar evaluaciones estratégicas.'),
    ('HUMINT: Inteligencia de Fuentes Humanas',
     'Comprende el valor de las fuentes humanas dentro del ciclo de inteligencia y aprende a evaluar la información que proporcionan.',
     'Principios de HUMINT, protocolos, métodos de obtención y tipos de investigación con fuentes humanas.',
     'Evaluación y organización de información proveniente de fuentes humanas dentro de un proceso de inteligencia.'),
    ('Operaciones Psicológicas y Psicosociales',
     'Analiza cómo las percepciones, narrativas y comportamientos pueden influir en escenarios políticos, sociales y de seguridad.',
     'Operaciones psicológicas, rumor, contrapropaganda, audiencias y dinámicas de influencia.',
     'Desarrollo de un proyecto de operaciones psicológicas y psicosociales aplicado a un escenario estratégico.'),
    ('Inteligencia aplicada a conflictos sociales y crimen organizado',
     'Integra capacidades de inteligencia para interpretar amenazas, anticipar escenarios críticos y apoyar respuestas coordinadas.',
     'Análisis de amenazas, anticipación de escenarios de violencia, coordinación institucional y gestión estratégica de inteligencia.',
     'Diseño de un plan de acción frente a un escenario de conflicto social o crimen organizado.'),
]
acc_keep('5b410621', len(MODS))
acc_titles('5b410621', [m[0] for m in MODS])
for _body, (_t, _d, _ap, _apl) in zip(kids('5b410621'), MODS):
    _intro = [k for k in kids(_body) if ELEM[k].get('widgetType') == 'text-editor'][0]
    text(_intro, '<p>' + _d + '</p>')
    set_classes(_intro, 'ak-mod-intro')             # regla por clase, no por posición (guía: el editor agrega elementos)
    _row = [k for k in kids(_body) if ELEM[k]['elType'] == 'container'][0]
    _a, _b = kids(_row)
    bgc(_a, '#EBEFF2'); bgc(_b, '#F3EEE7')          # Figma: #EBEFF2 y #B99864 al 14 % sobre #FDFCFB
    for _card, _txt in zip((_a, _b), (_ap, _apl)):
        _te = [k for k in kids(_card) if ELEM[k].get('widgetType') == 'text-editor'][0]
        text(_te, '<p>' + _txt + '</p>')
# textos de los módulos al 75 % (Figma), título del módulo 24/28 y número 56
css_sub('5b410621', 'font: 300 18px/28px Inter, sans-serif !important; letter-spacing: .01em; color: #001710;', 'font: 300 18px/28px Inter, sans-serif !important; letter-spacing: .01em; color: ' + BODY + ';')
css_sub('5b410621', 'font: 300 16px/24px Inter, sans-serif !important; letter-spacing: .01em; color: #001710;', 'font: 300 16px/24px Inter, sans-serif !important; letter-spacing: .01em; color: ' + BODY + ';')
css_sub('5b410621', 'font: 600 23px/29px Montserrat', 'font: 600 24px/28px Montserrat')
css_sub('5b410621', 'font: 500 50px/1.1 Montserrat', 'font: 500 56px/1.1 Montserrat')
css_sub('5b410621', 'font: 300 16px/24px Inter, sans-serif; letter-spacing: .1em;', 'font: 400 16px/24px Inter, sans-serif; letter-spacing: .1em;')
css_sub('5b410621', 'background-color: #E2DDD5 !important;', 'background-color: #F3EEE7 !important;')
css_sub('5b410621', 'font: 300 16px/24px Inter, sans-serif !important; letter-spacing: .01em; color: ' + BODY + ';', 'font: 300 16px/21px Inter, sans-serif !important; letter-spacing: .01em; color: ' + BODY + ';')
css_add('5b410621', '''/* desktop como el Figma: párrafo -> tarjetas 20 px; tarjetas de 176 px con el título a 22 px del borde */
@media (min-width: 1367px) {
  selector .ak-mod-body { --gap: 20px 20px; --row-gap: 20px; }
  selector .ak-mod-body > .e-con > .e-con { min-height: 176px; --padding-top: 22px; --gap: 8px 8px; --row-gap: 8px; }
}''')

# ============ 9. Banner próxima edición
text('1251cd12', '<p>Inicio: 09 de diciembre | Online vía Zoom | 8 Módulos</p>')
bg_image('4d64e131', img('banner-proxima-edicion.webp'), 'a/banner-proxima-edicion-director-4.webp')
setv('5a7371c6', button_background_hover_color=G_HOVER)

# ============ 10. Docentes (los 4 del PDF, Roberto Bazán primero por pedido del usuario; fotos reales de la Biblioteca, no las del Figma)
heading('53717cd', 'Aprende de especialistas en inteligencia,<br> <span class="ak-g">seguridad y estrategia</span>')
DOCS = [  # (diapositiva, tarjeta, bandera, país, nombre, especialidad, foto, bandera nueva)
    ('183f21cd', '25393af0', '2e2bb6e9', '2a7b35b3', '4d05e8e4', '74b539d4', 'Perú', 'Roberto Bazán',
     'Especialista en inteligencia estratégica y operaciones psicológicas', 'card-roberto-bazan-2.webp', 'logo-goberna-blanco.png'),
    ('336d9ea6', '4258bba5', '6f906d2b', '2177322f', '77221cd', '763d9ecb', 'Colombia', 'Eduardo de la Torre Díaz',
     'Especialista en ciberseguridad e inteligencia', None, None),
    ('4bd7554a', '18cff345', '116184f6', '1b384167', '128f09a4', '57b5f444', 'Argentina', 'Gonzalo Catanzariti',
     'Especialista en ciberinteligencia e investigación digital', None, None),
    ('250d1da1', '29864fdc', '4294c9f', '66c8b733', '322fbe2f', '1f57d183', 'Estados Unidos', 'Roniel Aledo',
     'Especialista en inteligencia y seguridad internacional', img('card-roniel-aledo.webp'), 'bandera-estados-unidos.png'),   # foto que pasó el usuario (Descargas, 28 oct)
]
DOC_CAR = '79feacd4'
_order = [d[0] for d in DOCS]
_car = ELEM[DOC_CAR]
_by = {c['id']: c for c in _car['elements']}
for _e in _car['elements']:
    if _e['id'] not in _order: ELEM.pop(_e['id'], None)
_car['elements'] = [_by[i] for i in _order]
_car['settings']['carousel_items'] = [{'_id': newid(), 'slide_title': d[7]} for d in DOCS]
setv(DOC_CAR, infinite='')                          # sin bucle: un punto por posición real
import html as _html
def _kids_div(s, a, b):
    out = []; d = 0; st = 0
    for t in re.finditer(r'<div\b[^>]*>|</div>', s[a:b]):
        if t.group(0) == '</div>':
            d -= 1
            if d == 0: out.append((a + st, a + t.end()))
        else:
            if d == 0: st = t.start()
            d += 1
    return out
def _doc_carousel(blk):
    def _ds(m):
        d = json.loads(_html.unescape(m.group(1)))
        d['carousel_items'] = S(DOC_CAR)['carousel_items']; d['infinite'] = ''
        t = json.dumps(d, ensure_ascii=True, separators=(',', ':'))
        return 'data-settings="' + t.replace('&', '&amp;').replace('"', '&quot;') + '"'
    blk = re.sub(r'data-settings="([^"]*)"', _ds, blk, count=1)
    w0 = blk.index('<div class="swiper-wrapper"'); w1 = blk.index('>', w0) + 1
    d = 0
    for t in re.finditer(r'<div\b|</div>', blk[w0:]):
        d += 1 if t.group(0) == '<div' else -1
        if d == 0: wend = w0 + t.start(); break
    slides = [blk[a:b] for a, b in _kids_div(blk, w1, wend)]
    real = [x for x in slides if 'swiper-slide-duplicate' not in re.match(r'<div class="[^"]*"', x).group(0)]
    pick = []
    for i in _order:
        pick.append([x for x in real if 'data-id="%s"' % i in x][0])
    n = len(pick)
    pick = [re.sub(r'aria-label="\d+ / \d+"', 'aria-label="%d / %d"' % (k + 1, n), x, count=1) for k, x in enumerate(pick)]
    wopen = re.sub(r'translate3d\(-?\d+px', 'translate3d(0px', blk[w0:w1])
    return blk[:w0] + wopen + '\n' + '\n'.join(pick) + '\n' + blk[wend:]
html_sub_in(DOC_CAR, _doc_carousel)                # primero: quita las copias de bucle del DOM publicado
css_sub('613c44c5', '/* puntos: 3, uno por docente */', '/* puntos: uno por posición */')
for _sl, _card, _flag, _pais, _nom, _esp, _p, _n, _e, _foto, _band in DOCS:
    heading(_pais, _p); heading(_nom, _n); heading(_esp, _e)
    if _band: image(_flag, _band)
    if _band == 'logo-goberna-blanco.png':          # Roberto Bazán: logo de Goberna en lugar de bandera y sin país (como en Director y Crimen)
        setv(_flag, width={'unit': 'px', 'size': 101, 'sizes': []}); EXTRA_CSS.append(pre(_flag) + ' img{width:101px}')
        remove(_pais)
    if _foto == '':
        no_bg_image(_card)                          # Roniel Aledo: no hay foto real (la del Figma es de Eduardo Velandia)
    elif _foto:
        _old = re.search(r'/([^/]+)$', S(_card)['background_image']['url']).group(1)
        bg_image(_card, _foto, 'a/' + _old)

# ============ 11. Presencia internacional (textos del Figma: no están en el PDF)
heading('61338992', '<span style="font-weight:400;font-size:1.18em">+</span>10<span style="font-weight:600">K</span>')
heading('1bdbba21', 'Profesionales')
heading('1d0e6775', '<span style="font-weight:400;font-size:1.18em">+</span>20')
heading('73c91642', 'Docentes')
for _i in ('17fe3c03', '1bdbba21', '73c91642'): color(_i, '#838994')
color('389c79fe', 'rgba(253,252,251,0.75)')
typo('23841199', lh=1.125, lh_unit='em')

# ============ 12. Certificación (PDF; imagen del diploma del Figma)
bg_image('28c43ad5', img('certificado-diploma.webp'), 'a/Gemini_Generated_Image_j14jp9j14jp9j14j-1-1.webp')
heading('2c9c857c', 'Una certificación que<br> <span class="ak-g">fortalece tu perfil<br> estratégico</span>')
text('3f88c4d3', '<p>Al culminar satisfactoriamente el programa, recibirás la certificación de Asesor Estratégico Internacional en Inteligencia y Contrainteligencia, que acredita tus competencias para analizar escenarios, identificar amenazas y aplicar herramientas de inteligencia estratégica.</p>')
text('334be732', '<p>Diploma emitido por Grupo Goberna, que acredita la culminación satisfactoria del programa.</p>')
text('3f0fb31c', '<p>Credencial digital verificable para validar tu formación profesional.</p>')
for _i in ('3f88c4d3', '334be732', '3f0fb31c'): color(_i, BODY)

# ============ 13. Inversión y admisión (PDF)
heading('2d4237ac', 'ANTICÍPATE A LAS<br> AMENAZAS. DECIDE CON<br> INTELIGENCIA.')
heading('9030ca2', '09 de diciembre')
heading('73517676', '8 MÓDULOS')
for _i in ('6ff88f9a', '609843a9'): typo_scale(_i, 18, ls=3.6)
for _i in ('9030ca2', '73517676'): typo(_i, weight=400); typo_scale(_i, 20, ls=4)
setv('79c591de', button_background_hover_color=G_HOVER)
button('79c591de', 'Pagar ahora', '#')
heading('dc295fa', '¿Listo para dar el<br> siguiente paso?')
# fondo del Figma (edificio en verde, anclado abajo)
setv('7a49a06a', background_image={'url': wp(img('inversion-fondo.webp'))[0], 'id': '', 'size': '', 'alt': '', 'source': 'library'},
     background_position='bottom center', background_size='cover', background_repeat='no-repeat')
EXTRA_CSS.append(pre('7a49a06a') + ':not(.elementor-motion-effects-element-type-background){background-image:url("a/' + img('inversion-fondo.webp') + '");background-position:bottom center;background-size:cover;background-repeat:no-repeat}')
setv('7d4e2b0', form_name='Inteligencia y Contrainteligencia — Habla con un asesor', email_subject='Nuevo contacto: Diploma Internacional de Inteligencia y Contrainteligencia')
html_global('name="Director de Seguridad — Habla con un asesor"', 'name="Inteligencia y Contrainteligencia — Habla con un asesor"')
for _f in S('7d4e2b0')['form_fields']:
    if _f.get('custom_id') == 'cargo': _f['placeholder'] = 'Ej. Analista de inteligencia'
html_global('placeholder="Ej. Jefe de seguridad"', 'placeholder="Ej. Analista de inteligencia"')

# ============ 14. Experiencia Goberna (frame «Background» del Figma, con la paleta de CII)
# Portada del panel del video: «image 5» del Figma (4060:35, 598x598), en lugar de la promo de Director de Seguridad.
bg_image('5fe95b15', img('experiencia-goberna-promo.webp'), 'a/Frame-252.webp')
# Sin pestaña «Voces» ni miniaturas (el usuario pidió quitar ese bloque, 28 oct): panel con un solo video.
# Video: el de Lorena Coria (02), el único del frame que responde (01 y 03 dan 404).
VIDEO_VSEC = 'https://cms.goberna.club/public/02_cuadrado_final_lorena.mp4'
_vh = S('76cef54d')['html']
assert _vh.count('var VIDEOS=["https://cms.goberna.club/public/pedro_espinoza_vertical.mp4"];') == 1
S('76cef54d')['html'] = _vh.replace('var VIDEOS=["https://cms.goberna.club/public/pedro_espinoza_vertical.mp4"];', 'var VIDEOS=["%s"];' % VIDEO_VSEC)
html_global('var VIDEOS=["https://cms.goberna.club/public/pedro_espinoza_vertical.mp4"];', 'var VIDEOS=["%s"];' % VIDEO_VSEC)

# ============ 15. Preguntas frecuentes (PDF)
acc_titles('266b2296', ['¿Cómo se realizan las clases?', '¿Cuánto dura el programa?', '¿Qué incluye mi inscripción?',
                        '¿Necesito experiencia previa en inteligencia?', '¿Cómo puedo inscribirme?'])
FAQ = [
    'Las sesiones se desarrollan en modalidad online vía Zoom, permitiendo la interacción con docentes y participantes.',
    'El diploma tiene una duración de 4 semanas, dividido en 8 módulos y 120 horas académicas.',
    'Incluye acceso a las clases, materiales académicos y la certificación correspondiente al culminar satisfactoriamente el programa.',
    'No. El programa está dirigido tanto a profesionales vinculados a seguridad e inteligencia como a personas interesadas en desarrollar competencias estratégicas.',
    'Completa tus datos en el formulario y un asesor de GOBERNA se pondrá en contacto contigo para orientarte durante el proceso.',
]
for _i, _t in zip(('ea24eba', '77b34c1f', '3a6adec1', '584613f6', '38271e76'), FAQ):
    text(_i, '<p>' + _t + '</p>'); color(_i, BODY)
color('4fe96a54', BODY)

# ============ 16. Restos de la base (enlaces de WhatsApp con el nombre del diploma)
replace_everywhere([('Diploma%20de%20%C3%89lite%20Internacional%20Director%20de%20Seguridad', 'Diploma%20Internacional%20de%20Inteligencia%20y%20Contrainteligencia')], css_too=False)
html_global('Diploma+de+%C3%89lite+Internacional+Director+de+Seguridad', 'Diploma+Internacional+de+Inteligencia+y+Contrainteligencia')

# ============ Íconos SVG con la paleta de CII (recoloreados de los de Carrera, misma forma que el Figma)
icon_svg('38e590e4', 'plan-modulos-caja-4-1-' + SLUG + '.svg')
icon_svg('9081977', 'plan-horas-caja-4-1-' + SLUG + '.svg')
icon_svg('2d10cc66', 'plan-metodologia-caja-4-1-' + SLUG + '.svg')
icon_svg('3e247b14', 'barra-modalidad-1-' + SLUG + '.svg')
icon_svg('1466ad22', 'barra-inicio-1-' + SLUG + '.svg')
icon_svg('54ba9d28', 'barra-horario-1-' + SLUG + '.svg')
icon_svg('37b97c47', 'barra-duracion-1-' + SLUG + '.svg')
icon_svg('940608c', 'certificacion-medalla-1-' + SLUG + '.svg')
icon_svg('1adb523', 'certificacion-medalla-1-' + SLUG + '.svg')
for _i in ('3e247b14', '1466ad22', '54ba9d28', '37b97c47'): color(_i, G)

# ================================================================ posiciones (calibradas en Carrera, mismo layout del Figma)
# Hero (Figma 1920: título a +235 de 749x136, botones +25, subrayado del brochure a +530, alto 879)
pad('2742d6b5', top=230, bottom=349, left=40, right=40)      # imagen completa 749x146 (el Figma la recorta a 136)
margin('571a5de0', top=20)
margin('263d369c', top=38)

# El programa (contenido en x=200 -> 210 en la caja de 1500; antetítulo a +77, título a +153, primera opción a +383)
css_sub('56bf8b99', 'selector .ak-dip-intro { position: absolute !important; top: 87px; left: calc(45.4% - 602px); width: 562px !important; z-index: 2; }',
        'selector .ak-dip-intro { position: absolute !important; top: 75px; left: calc(45.4% - 642px); width: 581px !important; z-index: 2; }')
css_sub('56bf8b99', 'padding: 346px 79px 100px 40px;', 'padding: 384px 121px 63px 40px;')
margin('37799678', top=42)

# War Room (contenido en x=200; texto de 713 px; etapas cada 390 px)
setv('3028d48c', boxed_width={'unit': 'px', 'size': 1500, 'sizes': []}); css_var('3028d48c', '--content-width', '1500px')
setv('5b22c8d6', width={'unit': '%', 'size': 47.5, 'sizes': []}); css_var('5b22c8d6', '--width', '47.5%')
for _i in ('187af424', '1fe5f3ba', '421e5c33'):
    setv(_i, width={'unit': '%', 'size': 25.667, 'sizes': []}); css_var(_i, '--width', '25.667%')
setv('76ebc950', width={'unit': '%', 'size': 23, 'sizes': []}); css_var('76ebc950', '--width', '23%')
pad('3028d48c', top=100, bottom=147, left=40, right=40)
margin('a50a77b', top=50)
setv('3079ff74', _element_custom_width={'unit': 'px', 'size': 713, 'sizes': []}, _element_custom_width_laptop={'unit': 'px', 'size': 507, 'sizes': []})
rule_sub('3079ff74', '563px', '713px'); rule_sub('3079ff74', '400px', '507px')
margin('3079ff74', top=23)
margin('6bb85ab9', top=189)
css_sub('3028d48c', 'selector .ak-war-step { position: relative; padding-top: 44px !important; }', 'selector .ak-war-step { position: relative; padding-top: 53px !important; }')
# títulos de etapa en una línea (la base les da min-height 2.6em): mismos márgenes calibrados en Carrera
for _t in ('7a82957e', '245ad6bc', '544064c5', '1f78edf1'):
    margin(_t, top=14, bottom=-50)
    _txt = [k for k in kids(PARENT[_t]['id']) if ELEM[k].get('widgetType') == 'text-editor'][0]
    margin(_txt, top=26)
for _s, _w in (('187af424', 292), ('1fe5f3ba', 320), ('421e5c33', 312), ('76ebc950', 344)):
    pad(_s, top=44, right=(385 if _s != '76ebc950' else 345) - _w, bottom=0, left=0)

# Metodología (antetítulo 1099, título 1180, párrafo 1315 a 687 px, barra 1409, imagen 947,1228 de 773 px)
margin('b86c8ae', top=47)
margin('390db8e4', top=21)
setv('390db8e4', _element_custom_width={'unit': 'px', 'size': 687, 'sizes': []}); rule_sub('390db8e4', '590px', '687px')
margin('4728f10c', top=30)
setv('161b8b64', width={'unit': '%', 'size': 47.53, 'sizes': []}); css_var('161b8b64', '--width', '47.53%')
setv('74f3d431', width={'unit': '%', 'size': 50.87, 'sizes': []}); css_var('74f3d431', '--width', '50.87%')
pad('74f3d431', top=129, right=0, bottom=0, left=0)

# Plan de estudios (acordeón desde x=808 con línea superior en 3687; módulos cerrados de 169)
margin('e42cc9c', top=47)
for _n in ('5d85f006', '1db9c1b2', '3121b088'): margin(_n, top=3)
for _n in ('6b4c14ba', '54ee35e9', '4475c46'): margin(_n, top=-7)
for _n in ('1f049f70', '50bb001c', '31fa5315'): margin(_n, top=-5)
margin('4475c46', '_mobile', top=-7, bottom=0)
margin('3954484a', top=49)
setv('6517c0d8', width={'unit': '%', 'size': 35.2, 'sizes': []}); css_var('6517c0d8', '--width', '35.2%')
setv('16e0013c', width={'unit': '%', 'size': 60, 'sizes': []}); css_var('16e0013c', '--width', '60%')
margin('16e0013c', top=15)
pad('7c39e8aa', top=100, bottom=80, left=40, right=40)
css_sub('5b410621', 'grid-template-rows: 28px 66px; column-gap: 20px;', 'grid-template-rows: 28px 80px; column-gap: 20px;')
css_sub('5b410621', 'font: 500 56px/1.1 Montserrat', 'font: 500 56px/1.38 Montserrat')
css_sub('5b410621', 'selector .e-n-accordion-item-title-header { grid-column: 2; grid-row: 2; padding-top: 8px; max-width: 560px; }',
        'selector .e-n-accordion-item-title-header { grid-column: 2; grid-row: 2; padding-top: 8px; max-width: 611px; }')
css_sub('5b410621', 'font: 300 18px/28px Inter, sans-serif !important; letter-spacing: .01em; color: ' + BODY + ';', 'font: 300 20px/32px Inter, sans-serif !important; letter-spacing: .01em; color: ' + BODY + ';')
css_sub('5b410621', 'selector .ak-mod-body { padding-left: 120px !important; padding-bottom: 30px !important; }', 'selector .ak-mod-body { padding-left: 120px !important; padding-bottom: 19px !important; }')
css_sub('5b410621', 'selector .e-n-accordion-item-title-icon { grid-column: 3; grid-row: 2; padding-top: 10px;', 'selector .e-n-accordion-item-title-icon { grid-column: 3; grid-row: 2; padding-top: 20px;')

# Banner próxima edición (tarjeta pegada al plan, título +44, fecha +146, botones +237; docentes 100 px debajo)
pad('66c6bdeb', top=0, bottom=100, left=40, right=40)
pad('4d64e131', top=44, bottom=42, left=80, right=80)
margin('1251cd12', top=10)

# Presencia internacional (alto 867, contenido arriba; mapa de 690 px en x=981)
setv('63b5ee4a', min_height={'unit': 'px', 'size': 867, 'sizes': []}, min_height_laptop={'unit': 'px', 'size': 617, 'sizes': []}, flex_align_items='flex-start')
rule_sub('63b5ee4a', '--min-height:886px', '--min-height:867px'); rule_sub('63b5ee4a', '--min-height:700px', '--min-height:617px')
EXTRA_CSS.append(pre('63b5ee4a') + '{--align-items:flex-start}')
pad('63b5ee4a', top=71, bottom=60, left=40, right=40)
margin('75122411', top=11)
margin('23841199', top=46)
margin('389c79fe', top=13)
margin('78c22442', top=56)
margin('1d2b7c01', top=70)
for _s in ('67a7a2fb', '3b0cc897', '5255b723'):
    setv(_s, flex_gap={'unit': 'px', 'column': '6', 'row': '6', 'isLinked': True, 'size': 6}); rule_sub(_s, '--gap:14px 14px', '--gap:6px 6px'); rule_sub(_s, '--row-gap:14px', '--row-gap:6px')
css_sub('63b5ee4a', 'selector .ak-pres-map img { width: 118%; max-width: 788px; height: auto; margin-right: -12%; }',
        'selector .ak-pres-map img { width: 690px; max-width: 100%; height: auto; margin-right: 66px; }')
bg_image('63b5ee4a', img('fondo-presencia.webp'), 'a/fondo-presencia-director-4.webp')
bgc('63b5ee4a', DARK)
css_add('63b5ee4a', '@media (max-width: 1366px) { selector .ak-pres-map img { max-width: 788px; } }')

# Certificación: pantalla completa de la base calibrada al Figma (sección 1056; imagen 1022 px; texto en x=1101, 619 px),
# bloque derecho centrado en vertical
css_add('54c4c5af', '''/* medidas del Figma (1 px de diseño = --u); laptop sigue con la escala de la base */
@media (min-width: 1367px) {
  selector { --u: min(1px, calc((100vh - 90px) / 1056)); }
  selector > .ak-cert-img { --width: 53.23%; width: 53.23% !important; }
  selector > .ak-cert-txt { align-items: flex-start !important; padding: calc(var(--u) * 24) calc(var(--u) * 60) calc(var(--u) * 24) calc(var(--u) * 79) !important; }
  selector .ak-cert-in { margin-right: 0 !important; }
  selector .ak-cert-title { margin-top: calc(var(--u) * 3) !important; }
  selector .ak-cert-title .elementor-heading-title { line-height: 1.14 !important; }
  selector .ak-cert-p { margin-top: calc(var(--u) * 41) !important; }
  selector .ak-cert-p, selector .ak-cert-p p { line-height: 1.6 !important; }
  selector .ak-card { padding: calc(var(--u) * 24) calc(var(--u) * 49) calc(var(--u) * 24) calc(var(--u) * 24) !important; }
  selector .ak-cert-in > .ak-card:nth-of-type(1), selector .ak-cert-p + .ak-card { margin-top: calc(var(--u) * 36) !important; }
  selector .ak-card + .ak-card { margin-top: calc(var(--u) * 20) !important; }
  selector .ak-card-body { gap: calc(var(--u) * 7) !important; }
  selector .ak-card-body .elementor-heading-title { line-height: 1.3 !important; }
  selector .ak-card-body .elementor-widget-text-editor, selector .ak-card-body .elementor-widget-text-editor p { line-height: 1.4 !important; }
  selector .ak-cert-btn { margin-top: calc(var(--u) * 11) !important; }
  selector .ak-cert-btn .elementor-button { min-width: calc(var(--u) * 339) !important; padding: 0 calc(var(--u) * 20) !important; }
}''')

# Inversión y admisión (columnas de 614 y 620 -> 606 y 612; botones de 64 px)
pad('7a49a06a', top=76, bottom=102, left=40, right=40)
setv('298fa0cb', width={'unit': '%', 'size': 40.4, 'sizes': []}); css_var('298fa0cb', '--width', '40.4%')
setv('79a4768d', width={'unit': '%', 'size': 40.8, 'sizes': []}); css_var('79a4768d', '--width', '40.8%')
margin('2d4237ac', top=42)
margin('60f25b0f', top=110)
margin('47c0a6f1', top=59)
setv('47c0a6f1', flex_justify_content='flex-start', flex_gap={'unit': 'px', 'column': '92', 'row': '92', 'isLinked': True, 'size': 92})
EXTRA_CSS.append(pre('47c0a6f1') + '{--justify-content:flex-start;--gap:92px 92px;--column-gap:92px}')
for _v in ('9030ca2', '73517676'): margin(_v, top=-14)
margin('12c8534c', top=17)
margin('dc295fa', top=44)
margin('2a8cefb0', top=14)
margin('7d4e2b0', top=-6)
margin('2d183dc1', top=23)
margin('3e72a9d', top=17)
css_sub('7a49a06a', 'selector .ak-inv-buy .elementor-button { width: 100%; height: 56px;', 'selector .ak-inv-buy .elementor-button { width: 100%; height: 64px;')
css_sub('7a49a06a', 'selector .ak-inv-form .elementor-field-type-submit { margin-top: 48px; }', 'selector .ak-inv-form .elementor-field-type-submit { margin-top: 57px; }')
css_sub('7a49a06a', 'selector .ak-inv-form .elementor-button { height: 56px;', 'selector .ak-inv-form .elementor-button { height: 64px;')
css_add('7a49a06a', '''/* título de Inversión en 3 líneas como el Figma */
@media (min-width: 1025px) { selector .ak-inv-left .elementor-element-2d4237ac .elementor-heading-title { white-space: nowrap; } }
@media (min-width: 1367px) { selector .ak-inv-price .ak-usd { margin-left: .93em; } }''')

# Preguntas frecuentes (acordeón de 750 px en x=958; textos de la izquierda arriba; alto 780)
setv('821fc48', width={'unit': '%', 'size': 50, 'sizes': []}); css_var('821fc48', '--width', '50%')
setv('521f33e5', flex_align_items='flex-start'); EXTRA_CSS.append(pre('521f33e5') + '{--align-items:flex-start}')
pad('521f33e5', top=98, bottom=97, left=40, right=40)
pad('1fd97c03', top=82, right=0, bottom=0, left=0)
margin('36d376ec', top=47)
margin('4fe96a54', top=27)
css_add('266b2296', '''/* desktop como el Figma: respuesta 24 px debajo con interlineado de 21 px */
@media (min-width: 1367px) {
  selector .e-n-accordion-item > .e-con, selector .e-n-accordion-item > [role="region"] { padding: 0 64px 16px 64px !important; }
  selector .elementor-widget-text-editor, selector .elementor-widget-text-editor p { line-height: 21px !important; }
}''')

# Detalles: barra de datos (etiqueta 926, valor 955, caja de 180) y panel de El programa
for _l in ('7094f679', '38e6f601', '78e96140', '6f2e556d'): margin(_l, top=8)
for _v in ('5d6fff46', '6919d0e7', '2fda4138', '4209211c'): margin(_v, top=-1)
for _h in ('5a5d4853', '3dff5c49', '36ba7119'): margin(_h, top=17, bottom=31)
for _b in ('4e571a4a', '1e9c4dab', '21c26060', '452ae72f'): pad(_b, top=30, right=26, bottom=50, left=26)
pad('3f83c2c', top=63, bottom=119, left=40, right=40)

# cuadrito gris del sitio en los enlaces de WhatsApp (regla a.flag::before del CSS adicional del tema)
for _sec in ('2742d6b5', '66c6bdeb', '54c4c5af'):
    css_add(_sec, 'selector a.flag::before { content: none !important; display: none !important; }')
# espaciado de letras del 1 % en los párrafos (Figma)
for _i, _ls in (('390db8e4', .18), ('3079ff74', .18), ('1e2e258a', .18), ('2d2f5c00', .18), ('73081eaa', .18),
                ('3f88c4d3', .2), ('334be732', .2), ('3f0fb31c', .2), ('389c79fe', .2), ('1251cd12', .24)):
    typo(_i, ls=_ls)
for _t in ('7a82957e', '245ad6bc', '544064c5', '1f78edf1'):
    _txt = [k for k in kids(PARENT[_t]['id']) if ELEM[k].get('widgetType') == 'text-editor'][0]
    typo(_txt, ls=.18)

# ================================================================ Laptop (1366) = Figma 1920 × 0,7115
pad('2742d6b5', '_laptop', top=163, bottom=248, left=80, right=80)
margin('571a5de0', '_laptop', top=15)
margin('263d369c', '_laptop', top=27)
css_sub('2742d6b5', 'selector .ak-hero-btn .elementor-button { width: 200px; height: 40px; }', 'selector .ak-hero-btn .elementor-button { width: 242px; height: 48px; }')
for _b in ('4be49e01', '9c2fe2d'): typo(_b, size_laptop=11)
typo('37799678', size_laptop=23, lh_laptop=29)
margin('37799678', '_laptop', top=30)
css_sub('56bf8b99', 'selector .ak-dip-intro { top: 80px; left: calc(45.4% - 502px); width: 470px !important; }', 'selector .ak-dip-intro { top: 54px; left: calc(45.4% - 458px); width: 413px !important; }')
css_sub('56bf8b99', 'selector .ak-dip-tabs .e-n-tabs-heading { padding: 313px 62px 72px 40px; }', 'selector .ak-dip-tabs .e-n-tabs-heading { padding: 273px 20px 71px 40px; }')
css_add('3028d48c', '@media (min-width: 768px) and (max-width: 1366px) { selector .ak-war-step::before { width: 14px; height: 14px; } }')
for _t in ('7a82957e', '245ad6bc', '544064c5', '1f78edf1'): margin(_t, '_laptop', top=10, bottom=-25)
css_sub('5b410621', 'selector .e-n-accordion-item-title-header { padding-top: 6px; max-width: 380px; }', 'selector .e-n-accordion-item-title-header { padding-top: 6px; max-width: 435px; }')

# ================================================================ Acordeones sin saltos (correcciones de Carrera, 22 oct)
# FAQ (266b2296): el handler de Elementor anima a summary + contenido con offsetHeight (sin márgenes ni transform):
# título con el mismo padding abierto y cerrado (se desplaza con transform), borde como sombra interior.
FAQ_ID = '266b2296'
_ease = 'cubic-bezier(.22,.61,.36,1)'
css_sub(FAQ_ID, 'selector .e-n-accordion-item { background: #FFFFFF; border: 1px solid #A1B5D3; border-radius: 15px; overflow: hidden; transition: border-color .2s; }',
        'selector .e-n-accordion-item { background: #FFFFFF; border: 0; box-shadow: inset 0 0 0 1px #A1B5D3; border-radius: 15px; overflow: hidden; position: relative; transition: box-shadow .45s %s; }' % _ease)
css_sub(FAQ_ID, 'selector .e-n-accordion-item[open] { border-color: transparent; background: linear-gradient(#FFFFFF, #FFFFFF) padding-box, linear-gradient(%s, %s) border-box; }' % (G, G),
        'selector .e-n-accordion-item[open] { box-shadow: inset 0 0 0 1px transparent; }')
css_sub(FAQ_ID, 'padding: 28px 25px 28px 64px !important;', 'padding: 29px 25px 29px 64px !important;')
css_sub(FAQ_ID, 'padding: 24px 20px 24px 40px !important;', 'padding: 25px 20px 25px 40px !important;')
css_sub(FAQ_ID, 'padding: 16px 14px 16px 18px !important;', 'padding: 17px 14px 17px 18px !important;')
css_sub(FAQ_ID, 'border-radius: 50%; background: #F3F4F8;', 'border-radius: 50%%; background-color: #F3F4F8; transition: background-color .45s %s;' % _ease)
css_sub(FAQ_ID, 'selector .e-n-accordion-item[open] .e-n-accordion-item-title-icon > span { background: linear-gradient(%s, %s); }' % (G, G),
        'selector .e-n-accordion-item[open] .e-n-accordion-item-title-icon > span { background-color: %s; }' % G)
css_sub(FAQ_ID, 'selector .e-n-accordion-item[open] > .e-con { animation: ak-acc-in .45s ease both; }',
        'selector .e-n-accordion-item[open] > .e-con { animation: ak-faq-in .4s %s both; }' % _ease)
css_add(FAQ_ID, '''@media (min-width: 1367px) { selector .e-n-accordion-item[open] > .e-n-accordion-item-title { transform: translateY(-8px); } }
selector .e-n-accordion-item::before { content: ""; position: absolute; inset: 0; border-radius: inherit; padding: 1px; background: ACC;
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite: xor;
  mask: linear-gradient(#000 0 0) content-box exclude, linear-gradient(#000 0 0); opacity: 0; pointer-events: none; transition: opacity .45s EASE; }
selector .e-n-accordion-item[open]::before { opacity: 1; }
selector .e-n-accordion-item > .e-n-accordion-item-title { transition: transform .45s EASE; }
selector .e-n-accordion-item > .e-con, selector .e-n-accordion-item > [role="region"] { position: relative; }
selector .e-n-accordion-item-title-icon i, selector .e-n-accordion-item-title-icon svg, selector .e-n-accordion-item-title-icon svg path { transition: color .45s EASE, fill .45s EASE; }
@keyframes ak-faq-in { from { opacity: 0; } to { opacity: 1; } }
@media (max-width: 1366px) {
  selector .e-n-accordion-item[open] > .e-con, selector .e-n-accordion-item[open] > [role="region"] { transform: translateY(-1px); }
}
@media (min-width: 1367px) {
  selector .e-n-accordion-item[open] > .e-con, selector .e-n-accordion-item[open] > [role="region"] { transform: translateY(-23px); }
}
@media (prefers-reduced-motion: reduce) {
  selector .e-n-accordion-item, selector .e-n-accordion-item::before, selector .e-n-accordion-item > .e-n-accordion-item-title,
  selector .e-n-accordion-item-title-icon > span, selector .e-n-accordion-item-title-icon i, selector .e-n-accordion-item-title-icon svg,
  selector .e-n-accordion-item-title-icon svg path { transition: none !important; }
}'''.replace('EASE', _ease).replace('ACC', G))

# Módulos (5b410621): el título mide lo mismo abierto y cerrado; el borde inferior pasa a sombra interior.
M = '5b410621'
def _sub1(old, new):
    cc = S(M).get('custom_css', '')
    assert cc.count(old) == 1, (cc.count(old), old[:80])
    css_sub(M, old, new)
_sub1('selector .e-n-accordion-item { counter-increment: mod; border-bottom: 1px solid #CCD0D4; padding: 0 !important; margin: 0 !important; }',
      'selector .e-n-accordion-item { counter-increment: mod; box-shadow: inset 0 -1px 0 #CCD0D4; padding: 0 !important; margin: 0 !important; }')
_sub1('align-items: start; padding: 30px 0 30px 0 !important;', 'align-items: start; padding: 30px 0 31px 0 !important;')
_sub1('column-gap: 14px; padding: 22px 0 !important;', 'column-gap: 14px; padding: 22px 0 23px !important;')
_sub1('column-gap: 12px; padding: 18px 0 !important;', 'column-gap: 12px; padding: 18px 0 19px !important;')
_sub1('selector .ak-mod-body { padding-left: 86px !important; padding-bottom: 24px !important; }', 'selector .ak-mod-body { padding-left: 86px !important; padding-bottom: 25px !important; }')
_sub1('selector .ak-mod-body { padding-left: 0 !important; padding-bottom: 20px !important; }', 'selector .ak-mod-body { padding-left: 0 !important; padding-bottom: 21px !important; }')
_sub1('selector .e-n-accordion-item[open] > .e-con { animation: ak-acc-in .45s ease both; }',
      'selector .e-n-accordion-item[open] > .e-con { animation: ak-mod-in .4s %s both; }' % _ease)
_sub1('@keyframes ak-acc-in { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: none; } }',
      '@keyframes ak-mod-in { from { opacity: 0; } to { opacity: 1; } }')
_sub1('selector .e-n-accordion-item:not([open]) .e-n-accordion-item-title-icon .e-opened,\r\nselector .e-n-accordion-item[open] .e-n-accordion-item-title-icon .e-closed { display: none !important; }', '')
_sub1('selector .e-n-accordion-item[open] .e-n-accordion-item-title-icon .e-opened,\r\nselector .e-n-accordion-item:not([open]) .e-n-accordion-item-title-icon .e-closed { display: inline-flex !important; }', '')
css_add(M, '\n'.join([
    '/* cierre sin salto y transiciones */',
    'selector .ak-mod-body > .ak-mod-intro { margin-top: -29px !important; }',
    '@media (max-width: 1366px) { selector .ak-mod-body > .ak-mod-intro { margin-top: -21px !important; } }',
    '@media (max-width: 767px) { selector .ak-mod-body > .ak-mod-intro { margin-top: -17px !important; } }',
    'selector .e-n-accordion-item-title-icon > span { display: inline-flex !important; grid-area: 1 / 1; opacity: 0; visibility: hidden; transition: opacity .45s %(e)s, visibility .45s %(e)s, color .45s %(e)s; }',
    'selector .e-n-accordion-item:not([open]) .e-n-accordion-item-title-icon .e-closed, selector .e-n-accordion-item[open] .e-n-accordion-item-title-icon .e-opened { opacity: 1; visibility: visible; }',
    '@media (prefers-reduced-motion: reduce) { selector .e-n-accordion-item-title-icon > span { transition: none !important; } }',
]).replace('%(e)s', _ease))

# ================================================================ Plan de estudios: sección fijada mientras la lista avanza
# (Guias-Landings/MODULOS-SCROLL-FIJO.md, propuesta A sin barra). Contenedor ak-plan-pin (id «modulos») + widget HTML.
def _pin_blocks():
    t = open(os.path.join(W, 'propuestas', 'a-elementor.txt'), encoding='utf-8').read().split('\n')
    def blk(a, b):
        i = next(k for k, l in enumerate(t) if l.startswith(a)); j = next(k for k, l in enumerate(t) if l.startswith(b) and k > i)
        return '\n'.join(t[i + 1:j]).strip('\n')
    js = blk('=== JS', '=== FIN JS'); assert 'var SHOW_PROGRESS = false;' in js
    return blk('=== CSS', '=== FIN CSS'), js
PIN_CSS, PIN_JS = _pin_blocks()
PIN_CSS = PIN_CSS.replace('#DD0005', G)
PIN_CSS = '/* fondo igual al de la sección: cubre la franja bajo la sección mientras está fijada */\nselector { background-color: ' + LIGHT_BG + '; }\n' + PIN_CSS
PIN, PIN_JS_ID, PLAN = newid(), newid(), '7c39e8aa'
_z = {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}
_pin = {'id': PIN, 'elType': 'container', 'isInner': False, 'elements': [], 'settings': {
    'content_width': 'full', 'flex_direction': 'column', 'css_classes': 'ak-plan-pin', '_element_id': 'modulos',
    'flex_gap': {'unit': 'px', 'size': 0, 'column': '0', 'row': '0', 'isLinked': True},
    'padding': dict(_z), 'margin': dict(_z), 'custom_css': PIN_CSS + '\n'}}
_js = {'id': PIN_JS_ID, 'elType': 'widget', 'isInner': False, 'widgetType': 'html', 'elements': [],
       'settings': {'html': '<script>\n' + PIN_JS + '\n</script>', '_css_classes': 'ak-plan-pin-js'}}
_k = [e['id'] for e in J['content']].index(PLAN)
_plan = J['content'][_k]
_plan['isInner'] = True; _plan['settings'].pop('_element_id', None)
_pin['elements'] = [_plan, _js]; J['content'][_k] = _pin
index(_pin)
def _pin_html(blk):
    tag = re.match(r'<div[^>]*>', blk).group(0)
    assert ' id="modulos"' in tag and ' e-parent' in tag, tag
    blk = tag.replace(' id="modulos"', '', 1).replace(' e-parent', ' e-child', 1) + blk[len(tag):]
    return ('<div class="elementor-element elementor-element-%s e-con-full ak-plan-pin e-flex e-con e-parent" data-id="%s" '
            'data-element_type="container" data-e-type="container" id="modulos">\n' % (PIN, PIN) + blk +
            '\n<div class="elementor-element elementor-element-%s ak-plan-pin-js elementor-widget elementor-widget-html" data-id="%s" '
            'data-element_type="widget" data-e-type="widget" data-widget_type="html.default">'
            '<div class="elementor-widget-container"><script>\n%s\n</script></div></div>\n</div>' % (PIN_JS_ID, PIN_JS_ID, PIN_JS))
html_sub_in(PLAN, _pin_html)
EXTRA_CSS.append(pre(PIN) + '{--display:flex;--flex-direction:column;--container-widget-width:100%;--container-widget-height:initial;'
                 '--container-widget-flex-grow:0;--container-widget-align-self:initial;--flex-wrap-mobile:wrap;--gap:0px 0px;'
                 '--row-gap:0px;--column-gap:0px;--padding-top:0px;--padding-bottom:0px;--padding-left:0px;--padding-right:0px;'
                 '--margin-top:0px;--margin-bottom:0px;--margin-left:0px;--margin-right:0px;}')
EXTRA_CUSTOM.append(PIN_CSS.replace('selector', pre(PIN)))
LOG.append('Plan de estudios: contenedor ak-plan-pin %s (id modulos) + widget HTML %s con el script de fijación.' % (PIN, PIN_JS_ID))
LOG.append('Enlaces que pone el usuario: brochure (2 botones), "Pagar ahora" y "Ver trayectoria" quedan en "#".')

# Header en laptop (1281-1366): el último ítem del menú tocaba el botón (pasaba también en la base); menos espacio entre ítems
css_add('13bd66b9', '''@media (min-width: 1281px) and (max-width: 1366px) {
  selector .ak-hd-nav .elementor-nav-menu--main .elementor-nav-menu > li { margin-left: 8px !important; margin-right: 8px !important; }
}''')

# Banner en mobile: el texto queda sobre las líneas verdes de la foto; degradado oscuro moderado (guía 12.5)
css_add('66c6bdeb', '''@media (max-width: 767px) {
  selector .ak-cta-card { position: relative; }
  selector .ak-cta-card::before { content: ""; position: absolute; inset: 0; z-index: 0; border-radius: inherit; pointer-events: none;
    background: linear-gradient(180deg, rgba(6,6,6,.82) 0%, rgba(6,6,6,.72) 60%, rgba(6,6,6,.6) 100%); }
  selector .ak-cta-card > * { position: relative; z-index: 1; }
}''')

# (vista previa) esquema FAQ de SEO: Elementor lo genera desde el acordeón (faq_schema = yes); aquí se rehace con las preguntas del PDF
_qs = [it['item_title'] for it in S('266b2296')['items']]
_ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
    {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in zip(_qs, FAQ)]})
_a = HTML.find('<script type="application/ld+json">'); _b = HTML.find('</script>', _a)
assert _a > 0 and '"FAQPage"' in HTML[_a:_b]
HTML = HTML[:_a] + '<script type="application/ld+json">' + _ld + HTML[_b:]
# (vista previa) la imagen de Metodología quedó con dos src (el segundo venía del lazy-load del sitio)
HTML = HTML.replace(' src="a/Frame-252.webp"', '')
