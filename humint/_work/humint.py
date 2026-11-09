# HUMINT: cambios sobre la landing final de Carrera Diplomática (se ejecuta dentro de transform.py, después de spec_carrera.py).
# Fuentes: Figma TZaBinYmWvX5sD7aBTR9Hp, frame 28:592 («HUMINT – v1», mismo layout que CII y Carrera)
#          + PDF «CONTENIDO LANDINGS (8)» (_work/pdf8.txt). En Elementor el texto fluye: textos literales del PDF.
# Decisiones del usuario (27 oct): los 6 ponentes del PDF; los 8 módulos y las listas de El programa del PDF;
# sin Experiencia Goberna (Carrera ya no la tiene); las 5 preguntas del PDF, sin San Marcos.
import shutil, urllib.parse

# imágenes nuevas -> carpeta de la vista previa
for _f in os.listdir(os.path.join(ROOT, 'imagenes')):
    shutil.copy(os.path.join(ROOT, 'imagenes', _f), os.path.join(P, 'a', _f))

CU, CU_HOVER = '#905532', '#74431F'     # cobre del Figma y su tono para hover
DARK_H = '#100600'                      # oscuro de fondos del Figma (Frame 262, Frame 258, textos del FAQ)
U10 = 'https://grupogoberna.com/wp-content/uploads/2026/10/'

# ---------------------------------------------------------------- utilidades propias
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

def lib_image(i, url, iid, local):
    """Imagen que ya está en la Biblioteca de medios (url + id reales); en la vista previa, la copia local."""
    S(i)['image'] = {'url': url, 'id': iid, 'size': '', 'alt': '', 'source': 'library'}
    html_sub_in(i, lambda blk: re.sub(r'(<img\b[^>]*?\ssrc=")[^"]*', lambda m: m.group(1) + 'a/' + local, blk, count=1))

def card_photo(i, url, local):
    """Foto de fondo de una tarjeta de docente (JSON + regla de la vista previa solo para ese elemento)."""
    S(i)['background_image'] = {'url': url, 'id': '', 'size': '', 'alt': '', 'source': 'library'}
    EXTRA_CSS.append(pre(i) + ':not(.elementor-motion-effects-element-type-background){background-image:url("a/' + local + '")}')

# ============ 1. Paleta (Figma: cobre #905532; oscuros #141210 / #100600)
replace_everywhere([
    ('#DD0005', CU), ('rgba(221,0,5,', 'rgba(144,85,50,'), ('rgba(221, 0, 5,', 'rgba(144, 85, 50,'),
    ('#B80004', CU_HOVER),
    ('#0C0000', DARK_H),
])
recolor_datauri('56bf8b99', (144, 85, 50))          # viñeta de la lista "Dirigido a"
# (vista previa) las reglas que la etapa de Carrera dejó en EXTRA_CSS / EXTRA_CUSTOM también pasan a la paleta nueva
def _pal(t):
    for o, n in (('#DD0005', CU), ('rgba(221,0,5,', 'rgba(144,85,50,'), ('#B80004', CU_HOVER), ('#0C0000', DARK_H)):
        t = re.sub(re.escape(o), n, t, flags=re.I)
    return t
EXTRA_CSS[:] = [_pal(x) for x in EXTRA_CSS]; EXTRA_CUSTOM[:] = [_pal(x) for x in EXTRA_CUSTOM]; PREVIEW_CSS = _pal(PREVIEW_CSS)
# íconos SVG en cobre (mismas formas que los de Carrera)
for _i, _f in (('38e590e4', 'plan-modulos-caja-4-1-humint.svg'), ('9081977', 'plan-horas-caja-4-1-humint.svg'),
               ('2d10cc66', 'plan-metodologia-caja-4-1-humint.svg'), ('3e247b14', 'barra-modalidad-1-humint.svg'),
               ('1466ad22', 'barra-inicio-1-humint.svg'), ('54ba9d28', 'barra-horario-1-humint.svg'),
               ('37b97c47', 'barra-duracion-1-humint.svg'), ('940608c', 'certificacion-medalla-1-humint.svg'),
               ('1adb523', 'certificacion-medalla-1-humint.svg')):
    icon_svg(_i, _f)

# ============ 2. Hero (PDF: «Diploma Internacional en HUMINT: Inteligencia de Fuentes Humanas»; título en imagen del Figma)
heading('17c98689', 'Diploma Internacional en HUMINT: Inteligencia de Fuentes Humanas')
image('1916fb3', 'titulo-humint.webp')
# Figma: título de 749x254 (la imagen del Figma está estirada en horizontal); el original sin estirar a 254 de alto = 696 px
img_width('1916fb3', w=696, w_laptop=495, w_mobile=300)
bg_image('2742d6b5', 'hero-fondo-humint.webp', 'a/hero-fondo-carrera-diplomatica.webp')
# Figma: título a +177 del borde del hero (Carrera: +245 con un título 59 px más bajo); el alto total no cambia (879)
pad('2742d6b5', top=177, bottom=289, left=40, right=40)
pad('2742d6b5', '_laptop', top=126, bottom=198, left=80, right=80)

# ============ 3. Barra de datos (PDF)
heading('5d6fff46', 'Online')
heading('6919d0e7', '02 de diciembre')
heading('2fda4138', '19:00 hrs. GMT-5')
heading('4209211c', '8 módulos · 3 semanas')
heading('4c8ed0ee', 'USD $199')

# ============ 4. Metodología (Spot principal del PDF)
heading('b86c8ae', 'Del análisis de la amenaza<br> al <span class="ak-g">diseño de respuestas<br> estratégicas</span>')
text('390db8e4', '<p>Aprende a analizar redes criminales y terroristas, interpretar sus vínculos y desarrollar estrategias de prevención, disrupción y cooperación frente a escenarios complejos.</p>')
# El cuadro del video pasa a ser un contenedor vacío para poner una imagen a mano (pedido del usuario, 28 oct), como el del
# certificado: Estilo -> Fondo -> Imagen. Gris #D9D9D9 mientras no tenga imagen, 16:9 y esquinas de 17 px como el diseño.
MET = '40d9161c'
_z0 = {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}
MET_CSS = ('/* cuadro para la imagen de Metodología (la imagen va como fondo del contenedor) */' + chr(10) +
           'selector { aspect-ratio: 16 / 9; min-height: 0; overflow: hidden; }' + chr(10))
_e = ELEM[MET]; _e.pop('widgetType', None)
_e.update({'elType': 'container', 'isInner': True, 'elements': [], 'settings': {
    'content_width': 'full', 'css_classes': 'ak-met-img', 'flex_direction': 'column',
    'flex_gap': {'unit': 'px', 'size': 0, 'column': '0', 'row': '0', 'isLinked': True},
    'padding': dict(_z0), 'margin': dict(_z0),
    'background_background': 'classic', 'background_color': '#D9D9D9',
    'background_image': {'url': '', 'id': '', 'size': ''},
    'background_position': 'center center', 'background_size': 'cover', 'background_repeat': 'no-repeat',
    'border_radius': {'unit': 'px', 'top': '17', 'right': '17', 'bottom': '17', 'left': '17', 'isLinked': True},
    'custom_css': MET_CSS}})
_s, _f = el_span(HTML, MET)
HTML = HTML[:_s] + ('<div class="elementor-element elementor-element-%s ak-met-img e-con-full e-flex e-con e-child" data-id="%s" '
                    'data-element_type="container" data-e-type="container"></div>' % (MET, MET)) + HTML[_f:]
EXTRA_CSS.append(pre(MET) + '{--display:flex;--flex-direction:column;--container-widget-width:100%;--container-widget-height:initial;'
                 '--container-widget-flex-grow:0;--container-widget-align-self:initial;--gap:0px 0px;--row-gap:0px;--column-gap:0px;'
                 '--padding-top:0px;--padding-bottom:0px;--padding-left:0px;--padding-right:0px;--margin-top:0px;--margin-bottom:0px;'
                 '--margin-left:0px;--margin-right:0px;--border-radius:17px 17px 17px 17px;border-radius:17px}')
EXTRA_CSS.append(pre(MET) + ':not(.elementor-motion-effects-element-type-background){background-color:#D9D9D9;background-position:center center;background-repeat:no-repeat;background-size:cover}')
EXTRA_CUSTOM.append(MET_CSS.replace('selector', pre(MET)))
LOG.append('Metodología: cuadro gris 16:9 (contenedor ak-met-img) para poner la imagen a mano como fondo.')

# ============ 5. El programa (PDF: «Información del programa»)
# Título: no está en el PDF; va el del Figma (viene de la plantilla de CII).
heading('37799678', 'Analiza escenarios, anticipa riesgos<br class="ak-dk"> y aplica inteligencia y<br class="ak-dk"> contrainteligencia para <span class="ak-g">proteger<br class="ak-dk"> organizaciones, proyectos y<br class="ak-dk"> decisiones estratégicas.</span>')
heading('5a5d4853', 'Objetivo del diploma')
text('1e2e258a', '<p>Formar especialistas capaces de <strong>planificar, obtener, evaluar y transformar información proveniente de fuentes humanas en inteligencia útil para la toma de decisiones.</strong></p>'
                 '<p>Durante el diploma desarrollarás capacidades para formular requerimientos, evaluar fuentes, conducir entrevistas, gestionar riesgos, corroborar información y sustentar una misión HUMINT mediante productos profesionales de inteligencia.</p>')
heading('3dff5c49', '¿A quiénes está dirigido?')
text('2d2f5c00', '<p>Dirigido a:</p><ul>'
                 '<li>Analistas y profesionales de inteligencia y contrainteligencia.</li>'
                 '<li>Miembros de Fuerzas Armadas y Policía.</li>'
                 '<li>Responsables de seguridad institucional y corporativa.</li>'
                 '<li>Especialistas en riesgos, compliance e investigación.</li>'
                 '<li>Funcionarios y asesores vinculados a seguridad y defensa.</li>'
                 '<li>Investigadores privados y periodistas de investigación.</li>'
                 '<li>Profesionales y estudiantes de relaciones internacionales, ciencia política, criminología y áreas afines.</li></ul>')
heading('36ba7119', 'Perfil del egresado')
text('73081eaa', '<p>Al finalizar el diploma estarás preparado para planificar una misión HUMINT, evaluar fuentes humanas, conducir procesos de entrevista y transformar hallazgos en productos de inteligencia confiables.</p>'
                 '<p>Podrás desenvolverte en:</p>'
                 '<p>Inteligencia · Contrainteligencia · HUMINT · Seguridad · Gestión de riesgos · Investigación · Due diligence · Análisis estratégico</p>')

# ============ 6. Metodología de aprendizaje (PDF; títulos de etapa cortos como el Figma: «Planifica · Evalúa · Obtén · Analiza»)
heading('a50a77b', 'Aquí no solo estudias HUMINT. Aprendes a construir <span class="ak-g">inteligencia desde las personas.</span>')
text('3079ff74', '<p>Durante todo el diploma trabajarás sobre una misión HUMINT simulada. Cada módulo generará un avance concreto que se integrará progresivamente en tu portafolio de inteligencia.</p>')
for _t, _h, _p in (('7a82957e', 'Planifica', 'Convierte necesidades de inteligencia en objetivos, requerimientos y un plan de obtención HUMINT.'),
                   ('245ad6bc', 'Evalúa', 'Analiza motivaciones, confiabilidad, riesgos y patrones de comportamiento de las fuentes humanas.'),
                   ('544064c5', 'Obtén', 'Aplica técnicas de entrevista, escucha activa y elicitación para identificar información relevante y vacíos informativos.'),
                   ('1f78edf1', 'Analiza', 'Corrobora hallazgos, evalúa su credibilidad y construye conclusiones útiles para la toma de decisiones.')):
    heading(_t, _h)
    _txt = [k for k in kids(PARENT[_t]['id']) if ELEM[k].get('widgetType') == 'text-editor'][0]
    text(_txt, '<p>' + _p + '</p>')
bg_image('3028d48c', 'war-room-fondo-humint.webp', 'a/war-room-fondo-carrera-diplomatica.webp')
bg_image('3028d48c', 'war-room-fondo-movil-humint.webp', key='background_image_mobile')
css_global('a/war-room-fondo-movil-carrera-diplomatica.webp', 'a/war-room-fondo-movil-humint.webp')
# la sección es más alta que la imagen (el título del PDF tiene una línea más): fondo del color del Figma (#141210), el mismo del borde de la imagen
bgc('3028d48c', '#141210')

# ============ 7. Plan de estudios (PDF: 8 módulos con descripción, Aprenderás y Aplicarás)
heading('48da84d4', 'Una formación para comprender, evaluar y trabajar con fuentes humanas')
heading('5d85f006', '8')
MODS = [
    ('HUMINT: el poder de las fuentes humanas',
     'Comprende el papel de la inteligencia humana dentro del ciclo de inteligencia y su valor para apoyar decisiones estratégicas.',
     'Fundamentos de HUMINT, ciclo de inteligencia, relación con OSINT, SIGINT e IMINT, límites y principios éticos.',
     'Identificación del aporte de las fuentes humanas dentro de una necesidad concreta de inteligencia.'),
    ('Planeamiento de operaciones HUMINT',
     'Convierte una necesidad de inteligencia en un plan estructurado de obtención mediante fuentes humanas.',
     'Requerimientos, objetivos, selección de fuentes, recursos, equipos, riesgos y medidas de seguridad.',
     'Diseño de un plan de obtención HUMINT para una misión simulada.'),
    ('Psicología y comportamiento de las fuentes humanas',
     'Comprende qué motiva a las personas y cómo factores psicológicos y sociales influyen en su comportamiento y disposición a brindar información.',
     'Motivaciones, confianza, factores emocionales, sesgos cognitivos, intereses y patrones de comportamiento.',
     'Análisis del perfil, motivaciones y riesgos de una fuente humana dentro de un escenario de inteligencia.'),
    ('Captación, reclutamiento y manejo de fuentes humanas',
     'Conoce cómo se estructura el ciclo de gestión de una fuente desde su identificación hasta su seguimiento.',
     'Identificación, selección, aproximación, captación, reclutamiento, seguimiento y protección de fuentes.',
     'Diseño de criterios de gestión, contacto, continuidad y resguardo para una fuente HUMINT.'),
    ('Técnicas de entrevista y obtención de información',
     'Desarrolla habilidades para conducir conversaciones orientadas a necesidades específicas de inteligencia.',
     'Escucha activa, preguntas, elicitación, entrevistas estructuradas, aclaración y registro de información.',
     'Simulación de una entrevista HUMINT para identificar hallazgos y vacíos informativos.'),
    ('Virtual HUMINT: fuentes humanas en entornos digitales',
     'Comprende cómo cambia la interacción con fuentes cuando el contacto ocurre mediante redes, plataformas y comunidades digitales.',
     'Virtual HUMINT, identidad digital, diferencias con OSINT y SOCMINT, verificación de interlocutores y riesgos de suplantación.',
     'Evaluación de una fuente digital y definición de criterios seguros para gestionar la interacción.'),
    ('Contrainteligencia aplicada a HUMINT',
     'Identifica engaños, infiltraciones y amenazas que pueden comprometer a las fuentes, operadores y procesos de obtención.',
     'Agentes dobles, insiders, manipulación, desinformación, contravigilancia y protección de información sensible.',
     'Evaluación de riesgos de engaño y diseño de medidas preventivas para proteger una misión HUMINT.'),
    ('Evaluación de información HUMINT y misión integradora',
     'Transforma la información obtenida en un producto de inteligencia claro, sustentado y útil para la toma de decisiones.',
     'Fiabilidad de fuentes, credibilidad de información, corroboración, hipótesis, niveles de confianza e informes de inteligencia.',
     'Elaboración de un Informe de Inteligencia HUMINT y sustentación mediante un briefing ejecutivo.'),
]
acc_keep('5b410621', len(MODS))
acc_titles('5b410621', [m[0] for m in MODS])
for _body, (_t, _d, _ap, _apl) in zip(kids('5b410621'), MODS):
    _intro = [k for k in kids(_body) if ELEM[k].get('widgetType') == 'text-editor'][0]
    text(_intro, '<p>' + _d + '</p>')
    _row = [k for k in kids(_body) if ELEM[k]['elType'] == 'container'][0]
    for _card, _txt in zip(kids(_row), (_ap, _apl)):
        _te = [k for k in kids(_card) if ELEM[k].get('widgetType') == 'text-editor'][0]
        text(_te, '<p>' + _txt + '</p>')

# ============ 8. Banner próxima edición (Figma)
text('1251cd12', '<p>Inicio: 02 de diciembre | Online vía Zoom | 8 Módulos</p>')
bg_image('4d64e131', 'banner-proxima-edicion-humint.webp', 'a/banner-proxima-edicion-carrera-diplomatica.webp')

# ============ 9. Docentes (los 6 del PDF, en su orden; fotos reales de la Biblioteca, no las del Figma)
heading('53717cd', 'Aprende de especialistas en HUMINT,<br> <span class="ak-g">inteligencia y seguridad</span>')
FLAG = {'España': (U10 + 'bandera-espana-1-1-1-1.png', 93697, 'bandera-espana-1-1-1-1.png'),
        'Colombia': (U10 + 'bandera-colombia-1-1-1-1.png', 93701, 'bandera-colombia-1-1-1-1.png'),
        'Argentina': (U10 + 'bandera-argentina-1-1-1.png', 93699, 'bandera-argentina-1-1-1.png'),
        'Estados Unidos': (U10 + 'bandera-estados-unidos.png', 93236, 'bandera-estados-unidos.png')}
DOCS = [  # (país, nombre, especialidad, foto en la Biblioteca)
    ('España', 'Francisco López', 'Especialista en criminología, inteligencia y análisis de fuentes humanas', 'francisco-lopez.webp'),
    ('Colombia', 'Camilo Bello', 'Especialista en operaciones especiales y liderazgo táctico', 'card-camilo-bello-1.webp'),
    ('España', 'Fernando Cocho', 'Especialista en inteligencia, análisis estratégico y prospectiva', 'card-fernando-cocho.webp'),
    ('Colombia', 'Mg. Eduardo de la Torre', 'Especialista en ciberseguridad, ciberdefensa y análisis digital', 'card-eduardo-de-la-torre-1-1-1-1.webp'),
    ('Colombia', 'Eduardo Velandia Becerra', 'Especialista en inteligencia, estrategia y liderazgo', 'Frame-193.webp'),
    ('Argentina', 'Daniela Galván', 'Especialista en investigación criminal e inteligencia digital', 'card-daniela-galvan-1-1-1-1.webp'),
    # 2026-11-02: el usuario pidió sumar a Diego Miranda y Roniel Aledo (no están en el PDF).
    # Miranda: especialidad de su ficha en el contenido de Director de Seguridad; foto ya en la Biblioteca (Director).
    # Aledo: especialidad y foto de su tarjeta en Inteligencia y Contrainteligencia; card-roniel-aledo.webp es imagen nueva, para subir.
    ('España', 'Diego Miranda', 'Especialista en inteligencia, contrainteligencia y seguridad estratégica', 'card-diego-miranda-2.webp'),
    ('Estados Unidos', 'Roniel Aledo', 'Especialista en inteligencia y seguridad internacional', 'card-roniel-aledo.webp'),
]
# diapositivas 6.ª en adelante = copias de la 5.ª con ids nuevos (funciones de spec_wp2.py)
_car = ELEM[DOC_CAR]; _src = _car['elements'][-1]['id']; _n0 = len(_car['elements']); _mps = []
for _k in range(_n0, len(DOCS)):
    _mp = {}
    def _reid(e):
        n = _newid8(set(_mp.values())); _mp[e['id']] = n; e['id'] = n
        for c in e.get('elements', []): _reid(c)
    _cp = copy.deepcopy(ELEM[_src]); _reid(_cp)
    _car['elements'].append(_cp); index(_cp, _car)
    _car['settings']['carousel_items'].append({'_id': _newid8(set(_mp.values())), 'slide_title': 'Docente %d' % (_k + 1)})
    _copy_css_clean(_mp); _mps.append(_mp)
def _add_slide(blk):
    w0 = blk.index('<div class="swiper-wrapper"'); w1 = blk.index('>', w0) + 1
    d = 0
    for t in re.finditer(r'<div\b|</div>', blk[w0:]):
        d += 1 if t.group(0) == '<div' else -1
        if d == 0: wend = w0 + t.start(); break
    slides = [blk[a:b] for a, b in _kids(blk, w1, wend)]
    assert len(slides) == _n0, len(slides)
    for _mp in _mps:
        new = slides[_n0 - 1]
        for o, n in _mp.items():
            new = re.sub(r'elementor-element-%s(?![0-9a-f])' % o, 'elementor-element-' + n, new)
            new = new.replace('data-id="%s"' % o, 'data-id="%s"' % n)
        slides.append(new)
    out = [re.sub(r'aria-label="\d+ / \d+"', 'aria-label="%d / %d"' % (k + 1, len(slides)), x, count=1) for k, x in enumerate(slides)]
    return blk[:w1] + '\n' + '\n'.join(out) + '\n' + blk[wend:]
html_sub_in(DOC_CAR, _add_slide)
for _k, (_slide, (_pais, _nom, _esp, _foto)) in enumerate(zip(_car['elements'], DOCS)):
    _card = _slide['elements'][0]
    _flagrow, _body = _card['elements'][0], _card['elements'][1]
    _flag, _country = [c['id'] for c in _flagrow['elements']]
    _name, _es, _btn = [c['id'] for c in _body['elements']]
    card_photo(_card['id'], U10 + _foto, _foto)
    lib_image(_flag, *FLAG[_pais])
    heading(_country, _pais); heading(_name, _nom); heading(_es, _esp)
    _car['settings']['carousel_items'][_k]['slide_title'] = _nom
# Fernando Cocho: no había foto de tarjeta. card-fernando-cocho.webp (imagen nueva, para subir) es el recorte de su CV
# (fernando-cocho.webp, fondo transparente) sobre el fondo azul de las demás tarjetas, con la cabeza a la misma escala
# y altura (coronilla a ~120 px y mentón a ~690 px de 1076, centrada).
LOG.append('Docentes: 8 tarjetas (López, Bello, Cocho, De la Torre, Velandia, Galván, Miranda, Aledo). Aledo: card-roniel-aledo.webp (de Inteligencia y Contrainteligencia), para subir. Cocho: card-fernando-cocho.webp, armada con la foto de su CV en formato tarjeta.')

# ============ 10. Presencia internacional (textos del Figma, iguales a Carrera; fondo del Figma)
bg_image('63b5ee4a', 'fondo-presencia-humint.webp', 'a/fondo-presencia-carrera-diplomatica.webp')

# ============ 11. Certificación (PDF). La imagen del Figma es el diploma de CII: queda el cuadro gris para la imagen real.
heading('2c9c857c', 'Una certificación para<br> <span class="ak-g">especialistas en<br> inteligencia humana</span>')
text('3f88c4d3', '<p>Al culminar satisfactoriamente el programa recibirás la certificación como Especialista en Inteligencia de Fuentes Humanas. Una acreditación que reconoce tu formación en planeamiento HUMINT, gestión y evaluación de fuentes, entrevista, análisis y producción de inteligencia.</p>')
LOG.append('Certificación: cuadro gris para el certificado de HUMINT (la imagen del Figma es el diploma de Inteligencia y Contrainteligencia).')

# ============ 12. Inversión y admisión (PDF; fondo del Figma anclado abajo, como en CII)
heading('2d4237ac', 'ESPECIALÍZATE EN<br> INTELIGENCIA DE<br> FUENTES HUMANAS')
heading('9030ca2', '02 de diciembre')
heading('73517676', '8 MÓDULOS')
heading('dc295fa', '¿Listo para especializarte<br> en HUMINT?')
setv('7a49a06a', background_image={'url': wp('inversion-fondo-humint.webp')[0], 'id': '', 'size': '', 'alt': '', 'source': 'library'},
     background_position='bottom center', background_size='cover', background_repeat='no-repeat')
EXTRA_CSS.append(pre('7a49a06a') + ':not(.elementor-motion-effects-element-type-background){background-image:url("a/inversion-fondo-humint.webp");background-position:bottom center;background-size:cover;background-repeat:no-repeat}')
setv('7d4e2b0', form_name='HUMINT — Habla con un asesor', email_subject='Nuevo contacto: Diploma Internacional en HUMINT: Inteligencia de Fuentes Humanas')
html_global('name="Carrera Diplomática — Habla con un asesor"', 'name="HUMINT — Habla con un asesor"')
for _f in S('7d4e2b0')['form_fields']:
    if _f.get('custom_id') == 'cargo': _f['placeholder'] = 'Ej. Analista de inteligencia'
html_global('placeholder="Ej. Analista de política exterior"', 'placeholder="Ej. Analista de inteligencia"')

# ============ 13. Preguntas frecuentes (las 5 del PDF; las preguntas ya son las mismas en Carrera)
acc_titles('266b2296', ['¿Cómo se realizan las clases?', '¿Cuánto dura el programa?', '¿Qué incluye mi inscripción?',
                        '¿Cuáles son los medios de pago disponibles?', '¿Cómo puedo inscribirme?'])
FAQ = [
    'Las sesiones se desarrollan 100% online y en vivo vía Zoom, combinando clases participativas, análisis de casos, ejercicios de entrevista, simulaciones por roles y retroalimentación docente.',
    'El diploma tiene una duración de 3 semanas y 120 horas académicas, desarrolladas de acuerdo con el cronograma establecido.',
    'Tu inscripción incluye acceso al programa, materiales académicos, ejercicios aplicados, simulaciones, desarrollo progresivo de una misión HUMINT y la certificación correspondiente.',
    'GOBERNA cuenta con diferentes alternativas de pago para sus participantes. Al iniciar tu proceso de inscripción, un asesor te indicará las opciones habilitadas según tu país.',
    'Completa tus datos en el formulario y un asesor de GOBERNA se pondrá en contacto contigo para orientarte durante el proceso.',
]
for _i, _t in zip(('ea24eba', '77b34c1f', '3a6adec1', '584613f6', '38271e76'), FAQ):
    text(_i, '<p>' + _t + '</p>')

# ============ 14. Restos de Carrera (texto de los enlaces de WhatsApp)
_CD = 'Diploma Internacional de Inteligencia Aplicada a la Carrera Diplomática'
_HU = 'Diploma Internacional en HUMINT: Inteligencia de Fuentes Humanas'
replace_everywhere([(urllib.parse.quote(_CD), urllib.parse.quote(_HU))], css_too=False)
html_global(urllib.parse.quote_plus(_CD), urllib.parse.quote_plus(_HU))
LOG.append('Enlaces que pone el usuario: brochure (2 botones) y "Pagar ahora" quedan en "#".')

# comentario del CSS de Certificación con el nombre de Carrera
css_sub('54c4c5af', '/* Carrera Diplomática: medidas del Figma', '/* HUMINT: medidas del Figma')

# ============ 15. Enlaces (28 oct)
# WhatsApp: los 3 «Hablar con un asesor» llevan el número de la base (+51 970 356 062) con el mensaje adaptado a HUMINT.
# En la vista previa, el HTML publicado traía el mensaje del sitio; se iguala al del JSON.
WA = 'https://wa.me/51970356062?text=' + urllib.parse.quote('¡Hola! Deseo más información sobre el ' + _HU + '.')
for _b in ('9c2fe2d', '16c985f5', '2b7efae9'):
    assert S(_b)['link']['url'] == WA, (_b, S(_b)['link']['url'])
    button(_b, S(_b)['text'], WA)
# «Ver trayectoria»: cada tarjeta a la página del CV del docente (como De la Torre en la base).
# La 6.ª tarjeta es copia de la de De la Torre y había heredado su enlace.
CV = {'Francisco López': 'francisco-lopez', 'Camilo Bello': 'camilo-bello', 'Fernando Cocho': 'fernando-cocho',
      'Mg. Eduardo de la Torre': 'eduardo-de-la-torre', 'Eduardo Velandia Becerra': 'eduardo-velandia', 'Daniela Galván': 'daniela-galvan',
      'Diego Miranda': 'diego-miranda-2', 'Roniel Aledo': 'roniel-aledo'}
for _slide, (_pais, _nom, _esp, _foto) in zip(_car['elements'], DOCS):
    _btn = _slide['elements'][0]['elements'][1]['elements'][2]['id']
    S(_btn)['link'] = dict(S('2589e64c')['link'])
    button(_btn, S(_btn)['text'], 'https://grupogoberna.com/%s/' % CV[_nom])
# «Inscríbete ahora» (header) apuntaba a #inscripcion, que no existe en la página: va al formulario, como «Reserva tu vacante»
assert S('4aa3f0b1')['link']['url'] == '#inscripcion'
button('4aa3f0b1', S('4aa3f0b1')['text'], '#doble')
