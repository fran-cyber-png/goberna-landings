# PSYOPS sobre OSINT & SOCMINT (se ejecuta dentro de transform.py, después de spec_carrera.py y spec.py)
# Fuentes: Figma FoHQXVRKZS32dsFjh8fNHt, frame 13:17 «PSYOPS – v1» + PDF «CONTENIDO LANDINGS (10)».
# Criterio de textos (el mismo de OSINT): lo que muestra el Figma manda; lo que el Figma no muestra (módulos 2-8,
# pestañas 2 y 3, respuestas, docentes 4-6) sale literal del PDF. Los títulos de los módulos van literales del PDF en los 8.

PGREEN, PDARK = '#359742', '#0E160F'
P_INK = '#FFFFFF'                    # texto sobre botones y cajas verdes (Figma PSYOPS: blanco)
WA_P = ('https://api.whatsapp.com/send/?phone=51983469091&text=Buen+d%C3%ADa+Goberna%2C+necesito+informaci%C3%B3n+del+Diploma+Internacional+en+PSYOPS%3A+'
        'Operaciones+Psicol%C3%B3gicas+y+Psicosociales+contra+el+Crimen+Organizado.&type=phone_number&app_absent=0')

# imágenes nuevas de PSYOPS -> carpeta de la vista previa
for _f in os.listdir(os.path.join(ROOT, 'imagenes')):
    shutil.copy(os.path.join(ROOT, 'imagenes', _f), os.path.join(P, 'a', _f))
# fotos de tarjeta y banderas que ya están en la Biblioteca de medios del sitio
_UP = 'https://grupogoberna.com/wp-content/uploads/2026/10/'
for _n in ('card-roberto-bazan-2.webp', 'card-andres-penaranda-1-1-1-1.webp', 'card-daniela-galvan-1-1-1-1.webp',
           'card-eduardo-de-la-torre-1-1-1-1.webp', 'card-eduardo-velandia.webp', 'card-fernando-cocho.webp',
           'bandera-peru-1.png', 'bandera-colombia-1-1-1-1.png', 'bandera-argentina-1-1-1.png', 'bandera-espana-1-1-1-1.png',
           'logo-goberna-blanco.png'):
    REUSE[_n] = _UP + _n
    if not os.path.exists(os.path.join(P, 'a', _n)):
        import urllib.request
        urllib.request.urlretrieve(_UP + _n, os.path.join(P, 'a', _n))

# ============ 1. Paleta (Figma PSYOPS: verde #359742, oscuro #0E160F, texto blanco sobre verde)
PAL_P = [
    ('#00C300', PGREEN), ('rgba(0,195,0,', 'rgba(53,151,66,'), ('rgba(0, 195, 0,', 'rgba(53, 151, 66,'),
    ('#2BD42B', '#3FAE4E'), ('#00A300', '#2B7E37'),
    ('#011000', PDARK), ('#E5FFE5', '#F0F5F0'), ('#EBF2EA', '#F0F5F0'), ('#031202', PDARK),
]
replace_everywhere(PAL_P)
def _palp(s):
    for o, n in PAL_P: s = re.sub(re.escape(o), lambda m, n=n: n, s, flags=re.I)
    return s
EXTRA_CSS[:] = [_palp(x) for x in EXTRA_CSS]; EXTRA_CUSTOM[:] = [_palp(x) for x in EXTRA_CUSTOM]; PREVIEW_CSS = _palp(PREVIEW_CSS)
recolor_datauri('56bf8b99', (53, 151, 66))          # viñeta de la lista "Dirigido a"
# texto blanco sobre los botones y cajas verdes (en OSINT era #0F0F0F)
for _b in ('4aa3f0b1', '4be49e01', '5a7371c6', '79c591de'):
    color(_b, P_INK); setv(_b, hover_color=P_INK)
color('12c0a15', P_INK); color('4c8ed0ee', P_INK)

# ============ 2. Íconos SVG con la paleta de PSYOPS
for _i, _f in (('3e247b14', 'barra-modalidad'), ('1466ad22', 'barra-inicio'), ('54ba9d28', 'barra-horario'), ('37b97c47', 'barra-duracion'),
               ('38e590e4', 'plan-modulos'), ('9081977', 'plan-semanas'), ('2d10cc66', 'plan-metodologia'),
               ('940608c', 'certificacion-medalla'), ('1adb523', 'certificacion-medalla')):
    icon_svg(_i, _f + '-psyops.svg')

# ============ 3. Hero (título en imagen: 749x340 a +134 del hero en el Figma; alto del hero 880)
heading('17c98689', 'Diploma Internacional en PSYOPS: Operaciones Psicológicas y Psicosociales contra el Crimen Organizado')
image('1916fb3', 'titulo-psyops.webp')
img_width('1916fb3', w=749, w_laptop=533, w_mobile=340)
bg_set('2742d6b5', 'hero-fondo-psyops.webp')
pad('2742d6b5', top=134, bottom=246, left=40, right=40)
pad('2742d6b5', '_laptop', top=95, bottom=179, left=80, right=80)

# ============ 4. Barra de datos
heading('6919d0e7', '08 de diciembre')
heading('2fda4138', '19:00 h (GMT-5)')
heading('4209211c', '8 módulos')
heading('4c8ed0ee', 'US$ 199')

# ============ 5. Metodología
heading('b86c8ae', 'Comprende la influencia<br> criminal y diseña<br> <span class="ak-g">respuestas institucionales</span>')
text('390db8e4', '<p>Aprende a identificar cómo las organizaciones criminales construyen miedo, reputación y control social, y a formular respuestas de prevención, disuasión y comunicación institucional.</p>')
image('40d9161c', 'metodologia-video-psyops.webp')
html_global('a/metodologia-video-osint-socmint.webp', 'a/metodologia-video-psyops.webp')
remove('4510a4fd')                                  # lema bajo la portada: el Figma PSYOPS no lo trae (pedido del usuario)

# ============ 6. El programa
heading('80fac6b', 'El diploma')
heading('37799678', 'Analiza las dimensiones psicológica,<br class="ak-dk"> psicosocial e informativa del crimen<br class="ak-dk"> organizado y <span class="ak-g">sus mecanismos de<br class="ak-dk"> influencia sobre personas e<br class="ak-dk"> instituciones.</span>')
text('1e2e258a', '<p>Formar profesionales capaces de <strong>comprender y analizar las dimensiones psicológica, psicosocial e informativa del crimen organizado y sus mecanismos de influencia.</strong></p>'
                 '<p>Durante la formación desarrollarás capacidades para identificar audiencias, examinar narrativas y señales de riesgo, elaborar productos de inteligencia y formular respuestas de prevención, disuasión y comunicación de crisis.</p>')
text('2d2f5c00', '<p>Dirigido a:</p><ul>'
                 '<li>Profesionales de inteligencia, contrainteligencia y análisis criminal.</li>'
                 '<li>Miembros de las Fuerzas Armadas y la Policía.</li>'
                 '<li>Funcionarios de fiscalías, justicia y entidades de prevención y seguridad.</li>'
                 '<li>Especialistas en seguridad, defensa y gestión de riesgos.</li>'
                 '<li>Profesionales de comunicación estratégica y gestión pública.</li>'
                 '<li>Especialistas en derecho, criminología y relaciones internacionales.</li>'
                 '<li>Profesionales de ciberseguridad, investigación y consultoría.</li></ul>')
text('73081eaa', '<p>Al finalizar el diploma estarás preparado para analizar dinámicas de influencia criminal, interpretar factores psicológicos y sociales, evaluar fuentes y evidencias, y formular productos de inteligencia y respuestas institucionales fundamentadas. Podrás integrar criterios de prevención, comunicación, disuasión y evaluación en escenarios complejos, con atención a los riesgos legales y operativos.</p>'
                 '<p>Podrás desenvolverte en:</p>'
                 '<p>Inteligencia estratégica · Análisis criminal · Seguridad institucional · Gestión de riesgos · Comunicación estratégica · Prevención del crimen · Cooperación interinstitucional</p>')

# ============ 7. Metodología de aprendizaje
heading('a50a77b', 'Analiza el escenario,<br> construye inteligencia<br> <span class="ak-g">y evalúa respuestas.</span>')
text('3079ff74', '<p>Aprenderás mediante clases participativas, casos documentados y ejercicios guiados. Un escenario académico sobre crimen organizado articula los ocho módulos, con retroalimentación docente.</p>')
for _t, _h, _p in (('7a82957e', 'Comprende la amenaza', 'Examina fundamentos de PSYOPS y factores que sostienen la influencia criminal.'),
                   ('245ad6bc', 'Analiza actores y riesgos', 'Identifica mecanismos de poder y control territorial; organiza señales de alerta.'),
                   ('544064c5', 'Diseña la respuesta', 'Examina posibilidades de disuasión y formula un plan PSYOPS en un escenario ficticio.'),
                   ('1f78edf1', 'Ejecuta y evalúa', 'Participa en un ejercicio académico guiado, documenta decisiones y valora resultados.')):
    heading(_t, _h)
    _txt = [k for k in kids(PARENT[_t]['id']) if ELEM[k].get('widgetType') == 'text-editor'][0]
    text(_txt, '<p>' + _p + '</p>')
bg_set('3028d48c', 'war-room-fondo-psyops.webp')
bg_set('3028d48c', 'war-room-fondo-movil-psyops.webp', key='background_image_mobile', media='(max-width:932px)')

# ============ 8. Plan de estudios (8 módulos, 120 horas)
heading('48da84d4', 'Una formación para responder con estrategia')
heading('5d85f006', '8')
heading('1db9c1b2', '120')
heading('54ee35e9', 'Horas')
MODS_P = [
    ('Fundamentos de las operaciones psicológicas (PSYOPS)',
     'Comprende las bases doctrinales y psicológicas de las PSYOPS y su función de apoyo a operaciones de seguridad frente al crimen organizado.',
     'Origen y evolución de las PSYOPS, principios, objetivos, tipos, modalidades, percepción, emoción, motivación, persuasión y límites legales de su aplicación policial y militar.',
     'Identificación de componentes psicológicos y límites de actuación en un escenario académico de amenaza criminal.'),
    ('Cultura criminal y comportamiento delictivo',
     'Analiza cómo las culturas criminales influyen en la identidad, las conductas y la permanencia de integrantes de organizaciones delictivas.',
     'Factores psicológicos, sociales y criminológicos; códigos, símbolos, rituales, jerarquías, lealtades, subculturas criminales, narcocultura y normalización de la violencia.',
     'Elaboración de un análisis de cultura criminal que identifique creencias, conductas y factores de cohesión dentro del escenario académico.'),
    ('Poder criminal: intimidación, reclutamiento y control territorial',
     'Examina cómo las organizaciones delictivas construyen autoridad e influencia mediante coerción, dependencia y control de comunidades y territorios.',
     'Intimidación, amenazas, demostraciones de fuerza, reclutamiento, legitimación social, provisión de recursos y uso de símbolos, narrativas y plataformas digitales.',
     'Construcción de un mapa de poder criminal que relacione actores, mecanismos de control y vínculos con la comunidad.'),
    ('Inteligencia estratégica contra el crimen organizado',
     'Desarrolla capacidades para analizar estructuras delictivas, vínculos y amenazas emergentes, y convertir hallazgos en insumos para decisiones institucionales.',
     'Uso de OSINT, SOCMINT, análisis de actores y redes, patrones delictivos, economías ilegales, dinámicas territoriales, hipótesis, vacíos de información y alerta temprana.',
     'Elaboración de un informe de inteligencia que distinga hechos, inferencias y riesgos, e incluya alertas tempranas para el escenario académico.'),
    ('Disuasión e influencia psicológica contra el crimen organizado',
     'Analiza los efectos psicológicos de las intervenciones institucionales y de su comunicación sobre las organizaciones criminales y la población.',
     'Disuasión, proyección de autoridad estatal, comunicación de resultados, TIC, recursos audiovisuales, experiencias internacionales y límites operativos y legales.',
     'Análisis de una intervención de seguridad para identificar componentes operativos y digitales, efectos esperados y riesgos asociados.'),
    ('Planeamiento de operaciones psicológicas (PSYOPS)',
     'Aprende a estructurar planes PSYOPS de apoyo a respuestas institucionales, considerando audiencias, inteligencia disponible y gestión de riesgos.',
     'Apreciación de la situación, objetivos psicológicos, características de audiencias, líneas de acción, recursos, competencias institucionales y riesgos legales e informativos.',
     'Elaboración de un plan PSYOPS para un escenario ficticio, con objetivos, líneas de acción, recursos y medidas de mitigación.'),
    ('Taller de ejecución de operaciones psicológicas (PSYOPS)',
     'Integra los componentes de planeamiento, información y comunicación institucional en un ejercicio académico de ejecución y ajuste de decisiones.',
     'Organización de equipos, flujos de información, prioridades, briefings, verificación de información, atención de incidencias y documentación de acciones.',
     'Desarrollo de un ejercicio guiado de ejecución de PSYOPS en el escenario académico, con decisiones documentadas y ajustes ante incidencias.'),
    ('Evaluación estratégica de las operaciones psicológicas (PSYOPS)',
     'Evalúa resultados y limitaciones de las respuestas institucionales mediante evidencias e indicadores de efectividad.',
     'Indicadores de percepciones, confianza, comportamientos protectores, calidad de información y coordinación; análisis de encuestas, informes operativos y efectos no previstos.',
     'Evaluación de una operación psicológica mediante indicadores y evidencias, con conclusiones sobre objetivos alcanzados y recomendaciones de mejora.'),
]
while len(ELEM['5b410621']['elements']) < len(MODS_P):
    acc_add_item('5b410621', ELEM['5b410621']['elements'][-1]['id'], '…')
acc_titles('5b410621', [m[0] for m in MODS_P])
for _body, (_t, _d, _ap, _apl) in zip(kids('5b410621'), MODS_P):
    _intro = [k for k in kids(_body) if ELEM[k].get('widgetType') == 'text-editor'][0]
    text(_intro, '<p>' + _d + '</p>')
    _row = [k for k in kids(_body) if ELEM[k]['elType'] == 'container'][0]
    for _card, _txt in zip(kids(_row), (_ap, _apl)):
        _te = [k for k in kids(_card) if ELEM[k].get('widgetType') == 'text-editor'][0]
        text(_te, '<p>' + _txt + '</p>')

# ============ 9. Banner próxima edición
text('1251cd12', '<p>Inicio: 08 de diciembre | Online vía Zoom | 8 Módulos</p>')
bg_set('4d64e131', 'banner-proxima-edicion-psyops.webp')

# ============ 10. Docentes: los 6 ponentes del PDF que tienen foto de tarjeta en la Biblioteca
# (Mauricio Quiroga queda fuera: no hay foto de tarjeta en el sitio)
heading('53717cd', 'Aprende de especialistas en <span class="ak-g">inteligencia,<br> PSYOPS y seguridad</span>')
bg_set('613c44c5', 'fondo-docentes-psyops.webp'); bgc('613c44c5', PDARK)
DOCS_P = [
    ('Roberto Bazán', 'Especialista en inteligencia estratégica, PSYOPS y consultoría política', 'Perú', 'bandera-peru-1.png', 'card-roberto-bazan-2.webp', 'https://grupogoberna.com/roberto-bazan/'),
    ('Andrés Peñaranda', 'Especialista en operaciones psicológicas y comunicación estratégica institucional', 'Colombia', 'bandera-colombia-1-1-1-1.png', 'card-andres-penaranda-psyops.webp', 'https://grupogoberna.com/andres-penaranda/'),   # foto nueva del Figma (61:44)
    ('Daniela Galván', 'Investigadora criminal especializada en inteligencia digital y análisis de fuentes', 'Argentina', 'bandera-argentina-1-1-1.png', 'card-daniela-galvan-1-1-1-1.webp', 'https://grupogoberna.com/daniela-galvan/'),
    ('Eduardo de la Torre', 'Experto en ciberseguridad, ciberdefensa e inteligencia estratégica', 'Colombia', 'bandera-colombia-1-1-1-1.png', 'card-eduardo-de-la-torre-1-1-1-1.webp', 'https://grupogoberna.com/eduardo-de-la-torre/'),
    ('Eduardo Velandia', 'Especialista en inteligencia, operaciones conjuntas y liderazgo de equipos', 'Colombia', 'bandera-colombia-1-1-1-1.png', 'card-eduardo-velandia.webp', 'https://grupogoberna.com/eduardo-velandia/'),
    ('Fernando Cocho', 'Analista de inteligencia y especialista en riesgos de seguridad nacional', 'España', 'bandera-espana-1-1-1-1.png', 'card-fernando-cocho.webp', 'https://grupogoberna.com/fernando-cocho/'),
    # 7.ª: copia de la tarjeta de Cocho con los textos de Quiroga; el usuario pone la foto y el enlace a mano en WordPress
    ('Mauricio Quiroga', 'Especialista en seguridad ciudadana, inteligencia estratégica y gestión pública', 'Perú', 'bandera-peru-1.png', 'card-fernando-cocho.webp', '#'),
]
# todas las tarjetas copian la de Bazán (misma estructura y clases); después se rellena cada una
_maps = carousel_rebuild(DOC_CAR, len(DOCS_P), [d[0] for d in DOCS_P])
for _mp, (_nm, _es, _pais, _flag, _card, _url) in zip(_maps, DOCS_P):
    _m = lambda i: _mp.get(i, i)
    bg_set(_m('25393af0'), _card)
    image(_m('2e2bb6e9'), _flag)
    heading(_m('2a7b35b3'), _pais)
    heading(_m('4d05e8e4'), _nm)
    heading(_m('74b539d4'), _es)
    button(_m('2ea3bff'), 'Ver trayectoria', _url)
# Roberto Bazán: logo de Goberna en lugar de bandera y sin país (como en Director, Crimen e Inteligencia y Contrainteligencia)
image('2e2bb6e9', 'logo-goberna-blanco.png')
S('2e2bb6e9')['image']['id'] = 93244
setv('2e2bb6e9', width={'unit': 'px', 'size': 101, 'sizes': []}); EXTRA_CSS.append(pre('2e2bb6e9') + ' img{width:101px}')
remove('2a7b35b3')
LOG.append('Docentes: 7 tarjetas (Bazán, Peñaranda, Galván, De la Torre, Velandia, Cocho y Quiroga). Quiroga: foto de Cocho y enlace "#" provisionales.')

# ============ 11. Presencia internacional (textos intactos; fondo del Figma PSYOPS)
bg_set('63b5ee4a', 'fondo-presencia-psyops.webp'); bgc('63b5ee4a', PDARK)

# ============ 12. Certificación (imagen del Figma, recorte centrado como en el diseño)
setv('28c43ad5', background_xpos={'unit': '%', 'size': 50, 'sizes': []}, background_ypos={'unit': '%', 'size': 50, 'sizes': []})
bg_set('28c43ad5', 'certificado-psyops.webp', pos='50% 50%')
heading('2c9c857c', 'Certifica tu formación<br> en <span class="ak-g">PSYOPS contra el<br> crimen organizado</span>')
text('3f88c4d3', '<p>Al culminar satisfactoriamente el programa obtendrás la certificación como <strong class="ak-g">Asesor estratégico en Operaciones Psicológicas contra el Crimen Organizado</strong>. Esta formación reconoce conocimientos en fundamentos de PSYOPS, cultura y poder criminal, inteligencia estratégica y disuasión.</p>')
text('334be732', '<p>Certificación: Asesor estratégico en Operaciones Psicológicas contra el Crimen Organizado.</p>')
text('3f0fb31c', '<p>Credencial digital verificable que facilita la validación de tu certificación.</p>')

# ============ 13. Inversión y admisión
bg_set('7a49a06a', 'inversion-fondo-psyops.webp')
heading('2d4237ac', 'ESPECIALÍZATE EN<br> PSYOPS CONTRA EL<br> CRIMEN ORGANIZADO')
heading('9030ca2', '08 de diciembre')
heading('73517676', '8 MÓDULOS')
heading('dc295fa', '¿Listo para especializarte<br> en PSYOPS?')
setv('7d4e2b0', form_name='PSYOPS — Habla con un asesor', email_subject='Nuevo contacto: Diploma Internacional en PSYOPS')
html_global('name="OSINT &amp; SOCMINT — Habla con un asesor"', 'name="PSYOPS — Habla con un asesor"')

# ============ 14. Preguntas frecuentes (respuestas del PDF)
FAQ_P = [
    'Las sesiones se desarrollan 100% online y en vivo vía Zoom, combinando clases participativas, análisis de casos documentados, ejercicios guiados, elaboración de reportes de inteligencia y revisión de productos aplicados con retroalimentación docente.',
    'El diploma consta de 8 módulos y 120 horas académicas, desarrollados de acuerdo con el cronograma establecido, con sesiones los martes, jueves y sábados de 19:00 a 21:00 h (GMT-5).',
    'Tu inscripción incluye acceso al programa, clases participativas, análisis de casos documentados, ejercicios guiados, desarrollo progresivo de productos de inteligencia y de un plan PSYOPS dentro de un escenario académico, retroalimentación docente y la certificación correspondiente.',
    'GOBERNA cuenta con diferentes alternativas de pago para sus participantes. Al iniciar tu proceso de inscripción, un asesor te indicará las opciones habilitadas según tu país.',
    'Completa tus datos en el formulario y un asesor de GOBERNA se pondrá en contacto contigo para orientarte durante el proceso.',
]
for _i, _t in zip(('ea24eba', '77b34c1f', '3a6adec1', '584613f6', '38271e76'), FAQ_P):
    text(_i, '<p>' + _t + '</p>')

# ============ 15. Botones de contacto -> WhatsApp con el mensaje de PSYOPS
for _b in ('9c2fe2d', '16c985f5', '2b7efae9'):
    button(_b, S(_b)['text'], WA_P)
    S(_b)['link']['is_external'] = 'on'
html_global(WA.replace('&', '&amp;'), WA_P.replace('&', '&amp;'))
LOG.append('WhatsApp: +51 983 469 091 con el mensaje de PSYOPS (pedido del usuario).')

# ============ 16. Botones de brochure (hero y plan de estudios) -> PDF de PSYOPS en pestaña nueva
BROCHURE = 'https://cms.goberna.club/d/brochure_psyops.pdf'
for _b in ('263d369c', '3954484a'):
    button(_b, S(_b)['text'], BROCHURE)
    S(_b)['link']['is_external'] = 'on'
    html_sub_in(_b, lambda blk: blk if 'target="_blank"' in blk else blk.replace('href="' + BROCHURE + '"', 'href="' + BROCHURE + '" target="_blank"', 1))

# ============ Restos de OSINT en comentarios del CSS
for _i in list(ELEM):
    _cc = S(_i).get('custom_css') or ''
    if 'OSINT & SOCMINT' in _cc: S(_i)['custom_css'] = _cc.replace('OSINT & SOCMINT', 'PSYOPS')

# ============ 17. «Inscríbete ahora» del header: #inscripcion no existe en la página -> sección de Inversión y admisión
button('4aa3f0b1', S('4aa3f0b1')['text'], '#inversion')
html_global('href="#inscripcion"', 'href="#inversion"')   # (vista previa) la copia del header fijo
