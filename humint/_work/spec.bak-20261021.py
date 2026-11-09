# Cambios de Carrera Diplomática sobre la base de Director de Seguridad (se ejecuta dentro de transform.py)
# Fuente: Figma nvxc199gG3N4UK6hH7DH4h, frame 2002:21 (CARRERA DIPLOMÁTICA – v1) + PDF "CONTENIDO LANDINGS (5)".
import base64, io, shutil
from PIL import Image as _Img

# imágenes nuevas -> carpeta de la vista previa
for _f in os.listdir(os.path.join(ROOT, 'imagenes')):
    shutil.copy(os.path.join(ROOT, 'imagenes', _f), os.path.join(P, 'a', _f))

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

BODY = 'rgba(6,6,6,0.75)'          # texto de párrafos del Figma (#060606 al 75 %)
LIGHT_BG, PANEL_BG = '#FDFCFB', '#F2F4F7'

# ============ 0. Secciones que no van (pedido del usuario): Experiencia Goberna, Alianza y footer
for _i in ('6a12cc55', '5b1123a8', '1222dd86'):
    remove_top(_i)
# (vista previa) restos del footer del sitio que quedan tras quitar la alianza
PREVIEW_CSS += '.elementor-93575 > .elementor-element-1222dd86{display:none!important}'

# ============ 1. Paleta (Figma: rojo #DD0005, oscuro #0C0000)
replace_everywhere([
    ('#FFBB03', RED), ('rgba(255,187,3,', 'rgba(221,0,5,'), ('rgba(255, 187, 3,', 'rgba(221, 0, 5,'),
    ('#FDC733', '#E5262B'),
    ('#15262F', DARK),
])
# fondos claros
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
# tarjetas Aprenderás / Aplicarás (Figma #EBEFF2 y #B99864 al 14 % sobre #FDFCFB)
for _acc_body in kids('5b410621'):
    _row = [k for k in kids(_acc_body) if ELEM[k]['elType'] == 'container'][0]
    _a, _b = kids(_row)
    bgc(_a, '#EBEFF2')
    bgc(_b, '#F3EEE7')

# ============ 2. Header (botón rojo, texto blanco)
setv('4aa3f0b1', hover_color='#FFFFFF', button_background_hover_color='#B80004'); color('4aa3f0b1', '#FFFFFF')

# ============ 3. Hero
heading('17c98689', 'Diploma Internacional de Inteligencia Aplicada a la Carrera Diplomática')
image('1916fb3', 'titulo-carrera-diplomatica.webp')
img_width('1916fb3', w=698, w_laptop=454, w_mobile=346)
remove('6b6388d')                                   # el Figma no trae subtítulo
bg_image('2742d6b5', 'hero-fondo-carrera-diplomatica.webp', 'a/hero-fondo-director.webp')
color('4be49e01', '#FFFFFF'); setv('4be49e01', button_background_hover_color='#B80004')
setv('9c2fe2d', border_color='#707070'); EXTRA_CSS.append(pre('9c2fe2d') + ' .elementor-button{border-color:#707070}')
button('263d369c', 'Descargar brochure del programa', '#')
button('4be49e01', 'Reserva tu vacante')

# ============ 4. Barra de datos
heading('5d6fff46', 'Online')
heading('6919d0e7', '17 de noviembre')
heading('2fda4138', '19:00 hrs. GMT-5')
heading('4209211c', '10 módulos')
heading('4c8ed0ee', 'USD $199')
for _i in ('3e247b14', '1466ad22', '54ba9d28', '37b97c47'): color(_i, RED)
color('12c0a15', '#FFFFFF'); color('4c8ed0ee', '#FFFFFF')

# ============ 5. Metodología
heading('77542da8', 'Metodología')
heading('b86c8ae', 'De la información a la<br> <span class="ak-g">decisión diplomática</span>')
text('390db8e4', '<p>Aprende a analizar escenarios internacionales y convertir evidencia en inteligencia útil para la representación y la negociación.</p>')
color('390db8e4', BODY)
image('40d9161c', 'metodologia-video-carrera-diplomatica.webp')
text('4510a4fd', '<p>Inteligencia <span>•</span> Estrategia <span>•</span> Liderazgo <span>•</span> Crisis <span>•</span> Tecnología</p>')
typo_scale('4510a4fd', 18)

# ============ 6. El programa
heading('80fac6b', 'El programa'); typo('80fac6b', weight=400)
heading('37799678', 'Desarrolla inteligencia estratégica<br class="ak-dk"> para analizar actores, anticipar<br class="ak-dk"> escenarios y <span class="ak-g">sustentar decisiones en<br class="ak-dk"> el entorno diplomático<br class="ak-dk"> internacional.</span>')
typo_scale('37799678', 32, lh=41, ls=-1.02)
css_sub('56bf8b99', 'selector .ak-gold-span .elementor-heading-title { white-space: nowrap; }', 'selector .ak-gold-span .elementor-heading-title { white-space: nowrap; }\nselector .ak-dip-intro { width: 581px !important; }')
# brillo rojo abajo a la izquierda (Figma: degradado radial #DD0005)
css_sub('56bf8b99', 'gap: 0 !important; background: #0C0000;', 'gap: 0 !important; background: radial-gradient(ellipse 540px 280px at 540px 100%, rgba(221,0,5,.22), rgba(221,0,5,0)), #0C0000;')
heading('5a5d4853', 'Objetivo del diploma')
text('1e2e258a', '<p>Formar profesionales capaces de <strong>convertir información internacional en productos de inteligencia útiles para la acción diplomática, desde la formulación de requerimientos hasta el análisis de actores, escenarios y recomendaciones.</strong></p>'
                 '<p>Durante el diploma desarrollarás capacidades para evaluar fuentes, interpretar intereses y relaciones de poder, anticipar cambios y comunicar hallazgos con claridad, trazabilidad y criterio institucional.</p>')
heading('3dff5c49', '¿Para quién es este diploma?')
text('2d2f5c00', '<p>Dirigido a:</p><ul>'
                 '<li>Diplomáticos y funcionarios de cancillerías, embajadas y consulados.</li>'
                 '<li>Profesionales vinculados a organismos internacionales y cooperación.</li>'
                 '<li>Aspirantes a la carrera diplomática.</li>'
                 '<li>Analistas y asesores de política exterior.</li>'
                 '<li>Profesionales de relaciones internacionales, ciencia política, derecho y economía.</li>'
                 '<li>Estudiantes avanzados interesados en diplomacia, inteligencia y asuntos internacionales.</li></ul>')
heading('36ba7119', 'Qué lograrás')
text('73081eaa', '<p>Al finalizar el diploma estarás preparado para analizar problemas de decisión diplomática, evaluar información, construir escenarios y elaborar productos de inteligencia para apoyar negociaciones, representación y gestión de crisis.</p>'
                 '<p>Podrás desenvolverte en:</p>'
                 '<p>Política exterior · Análisis internacional · Inteligencia diplomática · Negociación internacional · Diplomacia pública · Prospectiva · Gestión de crisis · Asuntos internacionales</p>')
for _i in ('1e2e258a', '2d2f5c00', '73081eaa'): color(_i, BODY)
recolor_datauri('56bf8b99', (221, 0, 5))           # viñeta de la lista "Dirigido a"

# ============ 7. Metodología de aprendizaje (War Room)
heading('24484833', 'Metodología de aprendizaje'); typo('24484833', weight=400)
heading('a50a77b', 'Aquí la información se<br> convierte en <span class="ak-g">decisión<br> diplomática</span>')
typo('a50a77b', ls=-1, ls_laptop=-0.7, ls_mobile=-0.5)
text('3079ff74', '<p>Trabajarás sobre un caso transversal de misión diplomática que evolucionará durante todo el programa. Cada módulo combinará herramientas, aplicación y retroalimentación hasta construir tu expediente final de inteligencia.</p>')
for _t, _h, _p in (('7a82957e', 'Investiga', 'Identifica necesidades de información y trabaja con fuentes relevantes y verificables.'),
                   ('245ad6bc', 'Analiza', 'Interpreta actores, intereses, relaciones de poder y escenarios internacionales.'),
                   ('544064c5', 'Anticipa', 'Construye escenarios, reconoce señales de cambio y establece alertas.'),
                   ('1f78edf1', 'Recomienda', 'Convierte el análisis en productos claros para sustentar decisiones diplomáticas.')):
    heading(_t, _h); typo(_t, family='Montserrat')
    _txt = [k for k in kids(PARENT[_t]['id']) if ELEM[k].get('widgetType') == 'text-editor'][0]
    text(_txt, '<p>' + _p + '</p>')
bg_image('3028d48c', 'war-room-fondo-carrera-diplomatica.webp', 'a/war-room-fondo-director-1.webp')
bg_image('3028d48c', 'war-room-fondo-movil-carrera-diplomatica.webp', key='background_image_mobile')
css_global('a/war-room-fondo-movil-director.webp', 'a/war-room-fondo-movil-carrera-diplomatica.webp')

# ============ 8. Plan de estudios
heading('1db9c1b2', '120')
button('3954484a', 'Descargar brochure', '#')
MODS = [
    ('Inteligencia y poder en la acción diplomática',
     'Comprende cómo la inteligencia fortalece la representación, la negociación y la protección de intereses nacionales.',
     'Interés nacional, política exterior, funciones diplomáticas y necesidades de conocimiento.',
     'Identificación de requerimientos de inteligencia para un caso diplomático.'),
    ('Planeamiento, obtención y validación de información diplomática',
     'Aprende a convertir una necesidad de decisión en un proceso ordenado de búsqueda, evaluación y verificación de información.',
     'Fuentes abiertas, trazabilidad, confiabilidad, contraste, sesgos, desinformación e IA aplicada.',
     'Diseño de un plan de obtención y validación de información diplomática.'),
    ('Análisis de actores, poder y redes de decisión',
     'Identifica quién influye, quién decide y cómo se relacionan los principales actores dentro de un escenario político.',
     'Mapeo de poder, intereses, capacidades, alianzas, rivalidades y análisis de redes.',
     'Construcción de una matriz de actores y centros de decisión relevantes.'),
    ('Análisis geopolítico y geoeconómico aplicado a la diplomacia',
     'Comprende cómo recursos, comercio, tecnología y rivalidades internacionales condicionan las decisiones de los Estados.',
     'Dependencias estratégicas, vulnerabilidades, rutas, capacidades de presión y factores de fricción.',
     'Evaluación geopolítica y geoeconómica de riesgos y oportunidades para la negociación.'),
    ('Inteligencia, narrativas y diplomacia pública',
     'Analiza cómo Estados y actores internacionales construyen influencia y disputan percepciones en el entorno global.',
     'Diplomacia pública, medios, plataformas digitales, narrativas, audiencias y desinformación.',
     'Análisis de narrativas y posibles impactos sobre la reputación y los intereses de un Estado.'),
    ('Prospectiva y alerta estratégica para la acción diplomática',
     'Anticipa escenarios y reconoce señales que pueden modificar los intereses o prioridades de una misión diplomática.',
     'Prospectiva, escenarios, incertidumbre, indicadores y niveles de alerta.',
     'Construcción de escenarios e indicadores para apoyar decisiones diplomáticas.'),
    ('Inteligencia para la negociación y las coaliciones internacionales',
     'Utiliza análisis de inteligencia para comprender posiciones, restricciones e intereses antes de una negociación.',
     'Negociación bilateral y multilateral, incentivos, alternativas, aliados e intereses compartidos.',
     'Mapeo de posiciones y oportunidades para construir acuerdos o coaliciones.'),
    ('Informes diplomáticos y briefing de inteligencia',
     'Transforma análisis complejos en productos claros, ejecutivos y útiles para quienes deben tomar decisiones.',
     'Síntesis, evidencia, niveles de confianza, cursos de acción y comunicación ejecutiva.',
     'Elaboración y sustentación de un briefing de inteligencia diplomática.'),
    ('Seguridad de la información y contrainteligencia defensiva',
     'Reconoce riesgos que pueden comprometer información, comunicaciones y relaciones sensibles dentro de una misión.',
     'Espionaje, ingeniería social, filtraciones, seguridad digital y confidencialidad.',
     'Definición de medidas preventivas para proteger información y comunicaciones institucionales.'),
    ('Sala de situación: inteligencia y gestión de crisis diplomáticas',
     'Integra todo el ciclo de inteligencia en un escenario de crisis donde nueva información obligará a revisar decisiones.',
     'Actualización de escenarios, coordinación institucional, priorización de respuestas y decisión bajo presión.',
     'Sustentación de un expediente de inteligencia y defensa de recomendaciones frente a una crisis simulada.'),
]
acc_titles('5b410621', [m[0] for m in MODS])
for _body, (_t, _d, _ap, _apl) in zip(kids('5b410621'), MODS):
    _intro = [k for k in kids(_body) if ELEM[k].get('widgetType') == 'text-editor'][0]
    text(_intro, '<p>' + _d + '</p>')
    _row = [k for k in kids(_body) if ELEM[k]['elType'] == 'container'][0]
    for _card, _txt in zip(kids(_row), (_ap, _apl)):
        _te = [k for k in kids(_card) if ELEM[k].get('widgetType') == 'text-editor'][0]
        text(_te, '<p>' + _txt + '</p>')
# textos de los módulos al 75 % (Figma), título del módulo 24/28 y número 56
css_sub('5b410621', 'font: 300 18px/28px Inter, sans-serif !important; letter-spacing: .01em; color: #0C0000;', 'font: 300 18px/28px Inter, sans-serif !important; letter-spacing: .01em; color: ' + BODY + ';')
css_sub('5b410621', 'font: 300 16px/24px Inter, sans-serif !important; letter-spacing: .01em; color: #0C0000;', 'font: 300 16px/24px Inter, sans-serif !important; letter-spacing: .01em; color: ' + BODY + ';')
css_sub('5b410621', 'font: 600 23px/29px Montserrat', 'font: 600 24px/28px Montserrat')
css_sub('5b410621', 'font: 500 50px/1.1 Montserrat', 'font: 500 56px/1.1 Montserrat')
css_sub('5b410621', 'font: 300 16px/24px Inter, sans-serif; letter-spacing: .1em;', 'font: 400 16px/24px Inter, sans-serif; letter-spacing: .1em;')

# ============ 9. Banner próxima edición
text('1251cd12', '<p>Inicio: 17 de noviembre | Online en vivo | 10 Módulos</p>')
bg_image('4d64e131', 'banner-proxima-edicion-carrera-diplomatica.webp', 'a/banner-proxima-edicion-director-4.webp')
color('5a7371c6', '#FFFFFF'); setv('5a7371c6', hover_color='#FFFFFF')

# ============ 10. Docentes (tarjetas como están; título del Figma)
heading('53717cd', 'Aprende de especialistas en inteligencia,<br> <span class="ak-g">diplomacia y análisis internacional</span>')

# ============ 11. Presencia internacional
heading('61338992', '<span style="font-weight:400;font-size:1.18em">+</span>10<span style="font-weight:600">K</span>')
heading('1bdbba21', 'Profesionales')
heading('1d0e6775', '<span style="font-weight:400;font-size:1.18em">+</span>20')
heading('73c91642', 'Docentes')
for _i in ('17fe3c03', '1bdbba21', '73c91642'): color(_i, '#838994')
color('389c79fe', 'rgba(253,252,251,0.75)')
typo('23841199', lh=1.125, lh_unit='em')

# ============ 12. Certificación (la imagen la sube el usuario: queda un cuadro vacío)
no_bg_image('28c43ad5')
bgc('28c43ad5', '#D9D9D9')
heading('2c9c857c', 'Una certificación para<br> quienes <span class="ak-g">analizan y<br> asesoran en el entorno<br> internacional</span>')
text('3f88c4d3', '<p>Al culminar satisfactoriamente el programa recibirás la certificación como Asesor Internacional en Asuntos Diplomáticos e Inteligencia. Una acreditación que reconoce tu formación en análisis internacional, inteligencia estratégica, prospectiva, negociación y apoyo a la decisión diplomática.</p>')
for _i in ('3f88c4d3', '334be732', '3f0fb31c'): color(_i, BODY)

# ============ 13. Inversión y admisión
heading('2d4237ac', 'PREPÁRATE PARA<br> DECIDIR EN ESCENARIOS<br> INTERNACIONALES')
heading('9030ca2', '17 de noviembre')
heading('73517676', '10 MÓDULOS')
for _i in ('6ff88f9a', '609843a9'): typo_scale(_i, 18, ls=3.6)
for _i in ('9030ca2', '73517676'): typo(_i, weight=400); typo_scale(_i, 20, ls=4)
color('79c591de', '#FFFFFF'); setv('79c591de', hover_color='#FFFFFF', button_background_hover_color='#B80004')
button('79c591de', 'Pagar ahora', '#')
heading('dc295fa', '¿Listo para fortalecer<br> tu perfil internacional?')
setv('7d4e2b0', form_name='Carrera Diplomática — Habla con un asesor', email_subject='Nuevo contacto: Diploma Internacional de Inteligencia Aplicada a la Carrera Diplomática')
html_global('name="Director de Seguridad — Habla con un asesor"', 'name="Carrera Diplomática — Habla con un asesor"')
for _f in S('7d4e2b0')['form_fields']:
    if _f.get('custom_id') == 'cargo': _f['placeholder'] = 'Ej. Analista de política exterior'
html_global('placeholder="Ej. Jefe de seguridad"', 'placeholder="Ej. Analista de política exterior"')

# ============ 14. Preguntas frecuentes (respuestas del PDF)
FAQ = [
    'Las sesiones se desarrollan 100% online y en vivo vía Zoom, combinando herramientas de análisis, ejercicios guiados, simulaciones por roles y trabajo aplicado sobre un caso de misión diplomática.',
    'El diploma contempla 120 horas académicas, desarrolladas de acuerdo con el cronograma establecido para el programa.',
    'Tu inscripción incluye acceso al programa, materiales académicos, ejercicios y simulaciones, retroalimentación de productos, desarrollo del Expediente de Inteligencia Diplomática y la certificación correspondiente.',
    'GOBERNA cuenta con diferentes alternativas de pago para sus participantes. Al iniciar tu proceso de inscripción, un asesor te indicará las opciones habilitadas según tu país.',
    'Completa tus datos en el formulario y un asesor de GOBERNA se pondrá en contacto contigo para orientarte durante el proceso.',
]
for _i, _t in zip(('ea24eba', '77b34c1f', '3a6adec1', '584613f6', '38271e76'), FAQ):
    text(_i, '<p>' + _t + '</p>'); color(_i, BODY)
color('4fe96a54', BODY)

# ============ 15. Restos de la base (enlaces de WhatsApp con el nombre del diploma)
replace_everywhere([('Diploma%20de%20%C3%89lite%20Internacional%20Director%20de%20Seguridad', 'Diploma%20Internacional%20de%20Inteligencia%20Aplicada%20a%20la%20Carrera%20Diplom%C3%A1tica')], css_too=False)
LOG.append('Enlaces que pone el usuario: brochure (2 botones) y "Pagar ahora" quedan en "#"; WhatsApp conserva el número de la base con el texto de Carrera Diplomática.')
LOG.append('Certificación: cuadro gris #D9D9D9 para subir la imagen del certificado (fondo del contenedor ak-cert-img).')

# ============ Ajustes de posición del hero (Figma 1920: título a +245, botones +25, subrayado del brochure a +531, alto 879)
pad('2742d6b5', top=245, bottom=348, left=40, right=40)
margin('571a5de0', top=25)
margin('263d369c', top=38)

# ============ Ajustes de posición de El programa (Figma: contenido a la izquierda en x=200 -> 210 en la caja de 1500;
# antetítulo a +77, título a +153, primera opción a +383)
css_sub('56bf8b99', 'selector .ak-gold-span .elementor-heading-title { white-space: nowrap; }\nselector .ak-dip-intro { width: 581px !important; }', 'selector .ak-gold-span .elementor-heading-title { white-space: nowrap; }')
css_sub('56bf8b99', 'selector .ak-dip-intro { position: absolute !important; top: 87px; left: calc(45.4% - 602px); width: 562px !important; z-index: 2; }',
        'selector .ak-dip-intro { position: absolute !important; top: 75px; left: calc(45.4% - 642px); width: 581px !important; z-index: 2; }')
css_sub('56bf8b99', 'padding: 346px 79px 100px 40px;', 'padding: 384px 121px 63px 40px;')
margin('37799678', top=42)

# ============ Ajustes de El simulador (Figma: contenido en x=200 -> caja de 1500; texto de 713 px; etapas cada 390 px)
setv('3028d48c', boxed_width={'unit': 'px', 'size': 1500, 'sizes': []}); css_var('3028d48c', '--content-width', '1500px')
setv('5b22c8d6', width={'unit': '%', 'size': 47.5, 'sizes': []}); css_var('5b22c8d6', '--width', '47.5%')
for _i in ('187af424', '1fe5f3ba', '421e5c33'):
    setv(_i, width={'unit': '%', 'size': 25.667, 'sizes': []}); css_var(_i, '--width', '25.667%')
setv('76ebc950', width={'unit': '%', 'size': 23, 'sizes': []}); css_var('76ebc950', '--width', '23%')

# posiciones verticales del simulador (Figma: antetítulo +100, título +184, párrafo +366 a 713 px, puntos +642, alto 1027)
pad('3028d48c', top=100, bottom=147, left=40, right=40)
margin('a50a77b', top=50)
setv('3079ff74', _element_custom_width={'unit': 'px', 'size': 713, 'sizes': []}, _element_custom_width_laptop={'unit': 'px', 'size': 507, 'sizes': []})
rule_sub('3079ff74', '563px', '713px'); rule_sub('3079ff74', '400px', '507px')
margin('3079ff74', top=23)
margin('6bb85ab9', top=189)
css_sub('3028d48c', 'selector .ak-war-step { position: relative; padding-top: 44px !important; }', 'selector .ak-war-step { position: relative; padding-top: 53px !important; }')
for _t in ('7a82957e', '245ad6bc', '544064c5', '1f78edf1'):
    margin(_t, top=24, bottom=-50)
    _txt = [k for k in kids(PARENT[_t]['id']) if ELEM[k].get('widgetType') == 'text-editor'][0]
    margin(_txt, top=26)
for _t in ('7a82957e', '245ad6bc', '544064c5', '1f78edf1'): margin(_t, top=14, bottom=-50)
# ancho de cada texto de etapa como en el Figma (286 / 320 / 312 / 344)
for _s, _w in (('187af424', 292), ('1fe5f3ba', 320), ('421e5c33', 312), ('76ebc950', 344)):
    pad(_s, top=44, right=(385 if _s != '76ebc950' else 345) - _w, bottom=0, left=0)

# ============ Posiciones de Metodología (Figma: antetítulo 1099, título 1180, párrafo 1315 a 687 px, barra 1409, imagen 947,1228 de 773 px)
pad('3f83c2c', top=54, bottom=119, left=40, right=40)
margin('b86c8ae', top=47)
margin('390db8e4', top=21)
setv('390db8e4', _element_custom_width={'unit': 'px', 'size': 687, 'sizes': []}); rule_sub('390db8e4', '590px', '687px')
margin('4728f10c', top=30)
setv('161b8b64', width={'unit': '%', 'size': 47.53, 'sizes': []}); css_var('161b8b64', '--width', '47.53%')
setv('74f3d431', width={'unit': '%', 'size': 50.87, 'sizes': []}); css_var('74f3d431', '--width', '50.87%')
pad('74f3d431', top=129, right=0, bottom=0, left=0)

# ============ Posiciones del Plan de estudios (Figma: íconos 3945, cifras 4026, etiquetas 4071/4091, brochure con línea en 4198;
# acordeón desde x=808 (810 en la caja) con línea superior en 3687, módulos cerrados de 169, abierto de 418)
margin('e42cc9c', top=47)
for _n in ('5d85f006', '1db9c1b2', '3121b088'): margin(_n, top=3)
for _n in ('6b4c14ba', '54ee35e9', '4475c46'): margin(_n, top=-7)
for _n in ('1f049f70', '50bb001c', '31fa5315'): margin(_n, top=-5)
margin('3954484a', top=49)
setv('6517c0d8', width={'unit': '%', 'size': 35.2, 'sizes': []}); css_var('6517c0d8', '--width', '35.2%')
setv('16e0013c', width={'unit': '%', 'size': 60, 'sizes': []}); css_var('16e0013c', '--width', '60%')
margin('16e0013c', top=15)
pad('7c39e8aa', top=100, bottom=80, left=40, right=40)
css_sub('5b410621', 'grid-template-rows: 28px 66px; column-gap: 20px;', 'grid-template-rows: 28px 80px; column-gap: 20px;')
css_sub('5b410621', 'font: 500 56px/1.1 Montserrat', 'font: 500 56px/1.38 Montserrat')
css_sub('5b410621', 'selector .e-n-accordion-item-title-header { grid-column: 2; grid-row: 2; padding-top: 8px; max-width: 560px; }',
        'selector .e-n-accordion-item-title-header { grid-column: 2; grid-row: 2; padding-top: 8px; max-width: 611px; }\n'
        'selector .e-n-accordion-item[open] > .e-n-accordion-item-title { padding-bottom: 2px !important; }')
css_sub('5b410621', 'font: 300 18px/28px Inter, sans-serif !important; letter-spacing: .01em; color: ' + BODY + ';', 'font: 300 20px/32px Inter, sans-serif !important; letter-spacing: .01em; color: ' + BODY + ';')
css_sub('5b410621', 'font: 300 16px/24px Inter, sans-serif !important; letter-spacing: .01em; color: ' + BODY + ';', 'font: 300 16px/21px Inter, sans-serif !important; letter-spacing: .01em; color: ' + BODY + ';')
css_sub('5b410621', 'selector .ak-mod-body { padding-left: 120px !important; padding-bottom: 30px !important; }', 'selector .ak-mod-body { padding-left: 120px !important; padding-bottom: 18px !important; }')
css_sub('5b410621', 'background-color: #E2DDD5 !important;', 'background-color: #F3EEE7 !important;')
css_add('5b410621', '''/* desktop como el Figma: párrafo -> tarjetas 20 px; tarjetas de 176 px con el título a 22 px del borde */
@media (min-width: 1367px) {
  selector .ak-mod-body { --gap: 20px 20px; --row-gap: 20px; }
  selector .ak-mod-body > .e-con > .e-con { min-height: 176px; --padding-top: 22px; --gap: 8px 8px; --row-gap: 8px; }
}''')

# ============ Banner próxima edición (Figma: tarjeta pegada al plan, título +44, fecha +146, botones +237; docentes 100 px debajo)
pad('66c6bdeb', top=0, bottom=100, left=40, right=40)
pad('4d64e131', top=44, bottom=42, left=80, right=80)
margin('1251cd12', top=10)

# ============ Presencia internacional (Figma: alto 867, contenido arriba; antetítulo 6122, título 6204, párrafo 6406,
# línea 6526, cifras 6597, etiquetas 6671; mapa de 690 px en x=981, y=6111)
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

# ============ Certificación: misma pantalla completa de la base, calibrada al Figma (sección 1056; imagen 1022 px;
# texto en x=1101, 619 px; antetítulo +97, título 44 px después, párrafo +41, tarjetas +36 y +20; relleno de tarjeta 24)
css_add('54c4c5af', '''/* Carrera Diplomática: medidas del Figma (1 px de diseño = --u); laptop sigue con la escala de la base */
@media (min-width: 1367px) {
  selector { --u: min(1px, calc((100vh - 90px) / 1056)); }
  selector > .ak-cert-img { --width: 53.23%; width: 53.23% !important; }
  selector > .ak-cert-txt { align-items: flex-start !important; padding: calc(var(--u) * 97) calc(var(--u) * 60) calc(var(--u) * 17) calc(var(--u) * 79) !important; }
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

# ============ Inversión y admisión (Figma: columnas de 614 y 620 -> 606 y 612; antetítulos 8039; botones en 8701 de 64 px)
pad('7a49a06a', top=76, bottom=102, left=40, right=40)
setv('298fa0cb', width={'unit': '%', 'size': 40.4, 'sizes': []}); css_var('298fa0cb', '--width', '40.4%')
setv('79a4768d', width={'unit': '%', 'size': 40.8, 'sizes': []}); css_var('79a4768d', '--width', '40.8%')
margin('2d4237ac', top=42)
margin('60f25b0f', top=110)
margin('2d183dc1', top=33)
margin('47c0a6f1', top=59)
setv('47c0a6f1', flex_justify_content='flex-start', flex_gap={'unit': 'px', 'column': '92', 'row': '92', 'isLinked': True, 'size': 92})
EXTRA_CSS.append(pre('47c0a6f1') + '{--justify-content:flex-start;--gap:92px 92px;--column-gap:92px}')
for _v in ('9030ca2', '73517676'): margin(_v, top=-14)
margin('12c8534c', top=17)
margin('dc295fa', top=44)
margin('2a8cefb0', top=14)
margin('7d4e2b0', top=-10)
margin('3e72a9d', top=17)
css_sub('7a49a06a', 'selector .ak-inv-buy .elementor-button { width: 100%; height: 56px;', 'selector .ak-inv-buy .elementor-button { width: 100%; height: 64px;')
css_sub('7a49a06a', 'selector .ak-inv-form .elementor-field-type-submit { margin-top: 48px; }', 'selector .ak-inv-form .elementor-field-type-submit { margin-top: 39px; }')
css_sub('7a49a06a', 'selector .ak-inv-form .elementor-button { height: 56px;', 'selector .ak-inv-form .elementor-button { height: 64px;')
margin('7d4e2b0', top=-6)
margin('2d183dc1', top=23)
css_sub('7a49a06a', 'selector .ak-inv-form .elementor-field-type-submit { margin-top: 39px; }', 'selector .ak-inv-form .elementor-field-type-submit { margin-top: 57px; }')
css_add('7a49a06a', '''/* título de Inversión en 3 líneas como el Figma (es más ancho que la columna) */
@media (min-width: 1025px) { selector .ak-inv-left .elementor-element-2d4237ac .elementor-heading-title { white-space: nowrap; } }''')

# ============ Preguntas frecuentes (Figma: acordeón de 750 px en x=958 desde 9002; pregunta abierta de 169 con respuesta 17/21;
# textos de la izquierda arriba: antetítulo 9084, título 9160, párrafo 9371; alto 780)
setv('821fc48', width={'unit': '%', 'size': 50, 'sizes': []}); css_var('821fc48', '--width', '50%')
setv('521f33e5', flex_align_items='flex-start'); EXTRA_CSS.append(pre('521f33e5') + '{--align-items:flex-start}')
pad('521f33e5', top=98, bottom=97, left=40, right=40)
pad('1fd97c03', top=82, right=0, bottom=0, left=0)
margin('36d376ec', top=47)
margin('4fe96a54', top=27)
css_add('266b2296', '''/* desktop como el Figma: pregunta abierta a 20 px del borde, respuesta 24 px debajo con interlineado de 21 px */
@media (min-width: 1367px) {
  selector .e-n-accordion-item[open] > .e-n-accordion-item-title { padding-top: 20px !important; padding-bottom: 0 !important; }
  selector .e-n-accordion-item > .e-con, selector .e-n-accordion-item > [role="region"] { padding: 14px 64px 38px 64px !important; }
  selector .elementor-widget-text-editor, selector .elementor-widget-text-editor p { line-height: 21px !important; }
}''')

# ============ Detalles: barra de datos (etiqueta 926, valor 955, caja de 180) y panel de El programa (título 2025, texto 2090)
for _l in ('7094f679', '38e6f601', '78e96140', '6f2e556d'): margin(_l, top=8)
for _v in ('5d6fff46', '6919d0e7', '2fda4138', '4209211c'): margin(_v, top=-1)
for _h in ('5a5d4853', '3dff5c49', '36ba7119'): margin(_h, top=17, bottom=31)
for _b in ('4e571a4a', '1e9c4dab', '21c26060', '452ae72f'): pad(_b, top=30, right=26, bottom=50, left=26)
pad('3f83c2c', top=63, bottom=119, left=40, right=40)

# ============ Repaso visual
# "Ver contenido +" / "Ocultar −" a la altura del título del módulo (Figma: 6 px por debajo del centro del título)
css_sub('5b410621', 'selector .e-n-accordion-item-title-icon { grid-column: 3; grid-row: 2; padding-top: 10px;', 'selector .e-n-accordion-item-title-icon { grid-column: 3; grid-row: 2; padding-top: 20px;')
# fondo de Presencia internacional del Figma (mármol oscuro cálido)
bg_image('63b5ee4a', 'fondo-presencia-carrera-diplomatica.webp', 'a/fondo-presencia-director-4.webp')
bgc('63b5ee4a', DARK)
# cuadrito gris del sitio en los enlaces de WhatsApp (regla a.flag::before del CSS adicional del tema)
for _sec in ('2742d6b5', '66c6bdeb', '54c4c5af'):
    css_add(_sec, 'selector a.flag::before { content: none !important; display: none !important; }')
# "USD" separado del precio como en el Figma
css_add('7a49a06a', '@media (min-width: 1367px) { selector .ak-inv-price .ak-usd { margin-left: .93em; } }')
# espaciado de letras del 1 % en los párrafos (Figma)
for _i, _ls in (('390db8e4', .18), ('3079ff74', .18), ('1e2e258a', .18), ('2d2f5c00', .18), ('73081eaa', .18),
                ('3f88c4d3', .2), ('334be732', .2), ('3f0fb31c', .2), ('389c79fe', .2), ('1251cd12', .24)):
    typo(_i, ls=_ls)
for _t in ('7a82957e', '245ad6bc', '544064c5', '1f78edf1'):
    _txt = [k for k in kids(PARENT[_t]['id']) if ELEM[k].get('widgetType') == 'text-editor'][0]
    typo(_txt, ls=.18)

# ============ Laptop (1366): hero con las proporciones del Figma laptop (alto 625; título a +174 de 497 px; botones de 242x48)
pad('2742d6b5', '_laptop', top=174, bottom=247, left=80, right=80)
img_width('1916fb3', w_laptop=497)
margin('571a5de0', '_laptop', top=18)
margin('263d369c', '_laptop', top=27)
css_sub('2742d6b5', 'selector .ak-hero-btn .elementor-button { width: 200px; height: 40px; }', 'selector .ak-hero-btn .elementor-button { width: 242px; height: 48px; }')
for _b in ('4be49e01', '9c2fe2d'): typo(_b, size_laptop=11)

# ============ Laptop: El programa (Figma laptop: título 23/29, antetítulo a +55, título a +109, opciones desde +272, x=142)
typo('37799678', size_laptop=23, lh_laptop=29)
margin('37799678', '_laptop', top=30)
css_sub('56bf8b99', 'selector .ak-dip-intro { top: 80px; left: calc(45.4% - 502px); width: 470px !important; }', 'selector .ak-dip-intro { top: 54px; left: calc(45.4% - 458px); width: 413px !important; }')
css_sub('56bf8b99', 'selector .ak-dip-tabs .e-n-tabs-heading { padding: 313px 62px 72px 40px; }', 'selector .ak-dip-tabs .e-n-tabs-heading { padding: 273px 20px 71px 40px; }')
# Laptop: simulador (puntos de 14 px como en la base; texto pegado al título)
css_add('3028d48c', '@media (min-width: 768px) and (max-width: 1366px) { selector .ak-war-step::before { width: 14px; height: 14px; } }')
for _t in ('7a82957e', '245ad6bc', '544064c5', '1f78edf1'): margin(_t, '_laptop', top=10, bottom=-25)
# Laptop: títulos de módulo en una línea (Figma laptop: 435 px)
css_sub('5b410621', 'selector .e-n-accordion-item-title-header { padding-top: 6px; max-width: 380px; }', 'selector .e-n-accordion-item-title-header { padding-top: 6px; max-width: 435px; }')
# tablet/laptop: el mapa no pasa de 788 px (como en la base)
css_add('63b5ee4a', '@media (max-width: 1366px) { selector .ak-pres-map img { max-width: 788px; } }')
# (vista previa) el botón publicado de Director usa otro texto de WhatsApp
html_global('Diploma+de+%C3%89lite+Internacional+Director+de+Seguridad', 'Diploma+Internacional+de+Inteligencia+Aplicada+a+la+Carrera+Diplom%C3%A1tica')
