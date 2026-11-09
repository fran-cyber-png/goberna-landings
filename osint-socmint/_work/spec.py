# OSINT & SOCMINT sobre Carrera Diplomática (se ejecuta dentro de transform.py, después de spec_carrera.py)
# Fuentes: Figma DYHmJ4KeF8moE2rQl7Fi9i, frame 4101:17 «OSINT & SOCMINT – v1» + PDF «CONTENIDO LANDINGS (9)».
# Criterio de textos: lo que muestra el Figma manda; lo que el Figma no muestra (módulos 4-7, pestañas 2 y 3,
# respuestas 2-5) sale literal del PDF. Los títulos de los módulos van literales del PDF en los 7.

GREEN, DARK_G = '#00C300', '#011000'
INK = '#0F0F0F'                      # texto sobre botones verdes (Figma)
BODY_G = 'rgba(20,18,16,0.75)'       # párrafos sobre fondo claro (Figma #141210 al 75 %)
WA = ('https://api.whatsapp.com/send/?phone=51941251506&text=Buen+d%C3%ADa+Goberna%2C+necesito+informaci%C3%B3n+de+Diploma+t%C3%A9cnico+en+Osint+%26+Socmint.'
      '%0A%0Ahttps%3A%2F%2Fgrupogoberna.com%2Fdiploma-tecnico-en-osint-socmint%2F&type=phone_number&app_absent=0')

# imágenes nuevas de OSINT -> carpeta de la vista previa
for _f in os.listdir(os.path.join(ROOT, 'imagenes')):
    shutil.copy(os.path.join(ROOT, 'imagenes', _f), os.path.join(P, 'a', _f))
# imágenes que ya están en la Biblioteca de medios del sitio
REUSE.update({
    'Rectangle-8-7.webp': 'https://grupogoberna.com/wp-content/uploads/2026/09/Rectangle-8-7.webp',          # tarjeta de Ausejo
    'card-roberto-bazan-2.webp': 'https://grupogoberna.com/wp-content/uploads/2026/10/card-roberto-bazan-2.webp',  # tarjeta de Bazán (la de la base)
    'bandera-peru-1.png': 'https://grupogoberna.com/wp-content/uploads/2026/10/bandera-peru-1.png',
})
for _n, _u in REUSE.items():
    if not os.path.exists(os.path.join(P, 'a', _n)):
        import urllib.request
        urllib.request.urlretrieve(_u, os.path.join(P, 'a', _n))
WP = 'https://grupogoberna.com/wp-content/uploads/2026/11/'   # las imágenes nuevas se suben en noviembre

def bg_set(i, name, key='background_image', css_key='background-image', media=None, pos=None):
    """Fondo de contenedor: JSON + regla en la vista previa (gana a la regla generada)."""
    url, iid = wp(name)
    S(i)[key] = {'url': url, 'id': iid, 'size': '', 'alt': '', 'source': 'library'}
    S(i)['background_background'] = 'classic'
    rule = pre(i) + ':not(.elementor-motion-effects-element-type-background){background-image:url("a/' + name + '")!important' + (';background-position:' + pos + '!important' if pos else '') + '}'
    EXTRA_CSS.append('@media' + media + '{' + rule + '}' if media else rule)

# ============ 1. Paleta (Figma: verde #00C300, oscuro #011000)
PALETTE = [
    ('#DD0005', GREEN), ('rgba(221,0,5,', 'rgba(0,195,0,'), ('rgba(221, 0, 5,', 'rgba(0, 195, 0,'),
    ('#E5262B', '#2BD42B'), ('#B80004', '#00A300'),
    ('#0C0000', DARK_G),
]
replace_everywhere(PALETTE)
# (vista previa) las reglas que generó spec_carrera.py todavía traen la paleta roja
def _pal(s):
    for o, n in PALETTE: s = re.sub(re.escape(o), lambda m, n=n: n, s, flags=re.I)
    return s
EXTRA_CSS[:] = [_pal(x) for x in EXTRA_CSS]; EXTRA_CUSTOM[:] = [_pal(x) for x in EXTRA_CUSTOM]; PREVIEW_CSS = _pal(PREVIEW_CSS)
recolor_datauri('56bf8b99', (0, 195, 0))            # viñeta de la lista "Dirigido a"
bgc('3f83c2c', '#FFFFFF')                           # Metodología: fondo blanco en el Figma
for _q in ('113px', '65px', '64px', '30px'):        # barra de datos montada sobre metodología
    css_sub('58716df6', f'transparent {_q}, {LIGHT_BG} {_q}', f'transparent {_q}, #FFFFFF {_q}')
css_sub('56bf8b99', '.e-n-tabs-content { background: ' + PANEL_BG + ';', '.e-n-tabs-content { background: #EBF2EA;')
# tarjetas Aprenderás / Aplicarás (Figma #EEEEEE y #E5FFE5)
for _acc_body in kids('5b410621'):
    _row = [k for k in kids(_acc_body) if ELEM[k]['elType'] == 'container'][0]
    _a, _b = kids(_row)
    bgc(_a, '#EEEEEE'); bgc(_b, '#E5FFE5')
css_sub('5b410621', 'background-color: #F3EEE7 !important;', 'background-color: #E5FFE5 !important;')
# texto oscuro sobre los botones y cajas verdes
for _b in ('4aa3f0b1', '4be49e01', '5a7371c6', '79c591de'):
    color(_b, INK); setv(_b, hover_color=INK)
color('12c0a15', INK); color('4c8ed0ee', INK)

# ============ 2. Íconos SVG con la paleta de OSINT
for _i, _f in (('3e247b14', 'barra-modalidad'), ('1466ad22', 'barra-inicio'), ('54ba9d28', 'barra-horario'), ('37b97c47', 'barra-duracion'),
               ('38e590e4', 'plan-modulos'), ('9081977', 'plan-semanas'), ('2d10cc66', 'plan-metodologia'),
               ('940608c', 'certificacion-medalla'), ('1adb523', 'certificacion-medalla')):
    icon_svg(_i, _f + '-osint-socmint.svg')

# ============ 3. Hero
heading('17c98689', 'Diploma Técnico en OSINT &amp; SOCMINT')
image('1916fb3', 'titulo-osint-socmint.webp')
img_width('1916fb3', w=749, w_laptop=533, w_mobile=340)
bg_set('2742d6b5', 'hero-fondo-osint-socmint.webp')

# ============ 4. Barra de datos
heading('6919d0e7', '16 de setiembre')
heading('4209211c', '7 módulos')

# ============ 5. Metodología
heading('b86c8ae', 'Convierte información<br> digital en <span class="ak-g">inteligencia<br> estratégica</span>')
text('390db8e4', '<p>La metodología combina formación práctica, herramientas profesionales y simulación de casos reales para desarrollar capacidades aplicadas de investigación digital, monitoreo y análisis de información.</p>')
color('390db8e4', BODY_G)
# sin spot de OSINT todavía: vuelve a ser el widget de imagen nativo con la portada del Figma
_e = ELEM['40d9161c']; _e['widgetType'] = 'image'
_e['settings'] = {'image': {'url': '', 'id': '', 'size': '', 'alt': '', 'source': 'library'}, 'image_size': 'full',
                  '_css_classes': 'ak-met-img', 'width': {'unit': '%', 'size': 100, 'sizes': []}}
def _met_img(blk):
    blk = blk.replace('elementor-widget-html"', 'elementor-widget-image"').replace('data-widget_type="html.default"', 'data-widget_type="image.default"')
    r, n = re.subn(r'(<div class="elementor-widget-container">).*?(</div>\s*</div>\s*$)', lambda m: m.group(1) + '<img width="1546" height="868" src="a/metodologia-video-osint-socmint.webp" class="attachment-full size-full" alt="">' + m.group(2), blk, count=1, flags=re.S)
    assert n; return r
html_sub_in('40d9161c', _met_img)
image('40d9161c', 'metodologia-video-osint-socmint.webp')
css_add('3f83c2c', 'selector .ak-met-img img { display: block; width: 100%; height: auto; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 17px; background: ' + DARK_G + '; }')
text('4510a4fd', '<p>Recolecta <span>•</span> Monitorea <span>•</span> Conecta <span>•</span> Analiza <span>•</span> Genera</p>')

# ============ 6. El programa
heading('37799678', 'Recolecta, analiza y transforma<br class="ak-dk"> información de fuentes abiertas y<br class="ak-dk"> redes sociales en <span class="ak-g">inteligencia útil<br class="ak-dk"> para la investigación, seguridad y<br class="ak-dk"> toma de decisiones.</span>')
text('1e2e258a', '<p>Formar especialistas capaces de <strong>recolectar, analizar y transformar información de fuentes abiertas y redes sociales en inteligencia útil para la investigación, seguridad y toma de decisiones.</strong></p>'
                 '<p>Durante el programa desarrollarás habilidades prácticas en OSINT y SOCMINT mediante herramientas profesionales para identificar actores, patrones, relaciones y señales digitales, simulando una unidad operativa de análisis e inteligencia.</p>')
text('2d2f5c00', '<p>Dirigido a:</p><ul>'
                 '<li>Analistas de inteligencia, contrainteligencia, seguridad y ciberinteligencia.</li>'
                 '<li>Profesionales de ciberseguridad, gestión de riesgos, fraude, compliance y due diligence.</li>'
                 '<li>Consultores en análisis político, comunicación estratégica, asuntos públicos y gestión de crisis.</li>'
                 '<li>Periodistas de investigación, investigadores privados, abogados y académicos.</li>'
                 '<li>Profesionales de comunicación, marketing e inteligencia de mercados interesados en analizar audiencias, conversaciones y tendencias digitales.</li></ul>')
text('73081eaa', '<p>Al finalizar el diploma estarás preparado para investigar, monitorear y analizar entornos digitales utilizando herramientas OSINT y SOCMINT para generar productos de inteligencia aplicados.</p>'
                 '<p>Podrás desenvolverte en:</p>'
                 '<p>Investigación digital · Inteligencia OSINT/SOCMINT · Monitoreo de redes sociales · Análisis de actores y nodos de influencia · Threat Intelligence · Inteligencia competitiva · Gestión de crisis digitales · Análisis de datos</p>')
for _i in ('1e2e258a', '2d2f5c00', '73081eaa'): color(_i, BODY_G)

# ============ 7. Metodología de aprendizaje
heading('a50a77b', 'Aquí no solo aprendes<br> herramientas.<br> <span class="ak-g">Generas inteligencia.</span>')
text('3079ff74', '<p>Al finalizar el diploma estarás preparado para investigar, monitorear y analizar entornos digitales utilizando herramientas OSINT y SOCMINT para generar productos de inteligencia aplicados.</p>')
for _t, _h, _p in (('7a82957e', 'Recolecta información', 'Aprende a identificar fuentes, extraer datos y utilizar herramientas OSINT.'),
                   ('245ad6bc', 'Monitorea el entorno', 'Analiza redes sociales, conversaciones y señales digitales para detectar patrones.'),
                   ('544064c5', 'Conecta datos y actores', 'Utiliza análisis de redes y visualización para descubrir relaciones y nodos de influencia.'),
                   ('1f78edf1', 'Genera inteligencia', 'Transforma información dispersa en productos analíticos útiles para la toma de decisiones.')):
    heading(_t, _h)
    _txt = [k for k in kids(PARENT[_t]['id']) if ELEM[k].get('widgetType') == 'text-editor'][0]
    text(_txt, '<p>' + _p + '</p>')
bg_set('3028d48c', 'war-room-fondo-osint-socmint.webp')
bg_set('3028d48c', 'war-room-fondo-movil-osint-socmint.webp', key='background_image_mobile', media='(max-width:932px)')

# ============ 8. Plan de estudios (7 módulos)
heading('48da84d4', 'Una formación para generar inteligencia')
heading('5d85f006', '7')
heading('1db9c1b2', '3')
heading('54ee35e9', 'Semanas')
MODS = [
    ('Recolección automatizada de información y minería de datos',
     'Aprende a obtener y organizar grandes volúmenes de información pública de manera más eficiente para tus investigaciones digitales.',
     'Web scraping, minería de datos, metadatos, dominios, direcciones IP y automatización de búsquedas OSINT.',
     'Recolección automatizada de información para construir una base de datos útil para una investigación.'),
    ('Monitoreo de redes sociales en tiempo real (SOCMINT)',
     'Convierte conversaciones, menciones y tendencias digitales en información relevante para comprender lo que ocurre en el entorno social.',
     'Monitoreo SOCMINT, seguimiento de cuentas, hashtags, menciones, conversaciones y alertas digitales.',
     'Configuración de un sistema de monitoreo para detectar actores, tendencias y señales relevantes en tiempo real.'),
    ('Exploración de Deep Web y Dark Web con fines de inteligencia',
     'Comprende cómo investigar entornos digitales no indexados y reconocer información relevante desde una perspectiva de inteligencia.',
     'Deep Web, Dark Web, navegación mediante Tor, búsqueda especializada y criterios de privacidad y seguridad digital.',
     'Exploración estructurada de fuentes y contenidos relevantes dentro de entornos digitales ocultos.'),
    ('Análisis de contenido y seguridad en entornos digitales ocultos',
     'Aprende a examinar archivos y contenidos digitales para identificar metadatos, patrones y posibles riesgos durante una investigación.',
     'Metadatos, verificación de archivos, análisis de datos, patrones digitales y herramientas de seguridad.',
     'Evaluación de contenidos digitales para extraer información relevante y reconocer posibles indicadores de riesgo.'),
    ('Análisis de redes, influencia y nodos sociales (OSINT/SOCMINT avanzado)',
     'Descubre cómo se conectan actores, comunidades y estructuras de influencia dentro del entorno digital.',
     'Análisis de redes, grafos, centralidad, comunidades, relaciones entre actores y visualización de conexiones.',
     'Construcción de un mapa de relaciones para identificar actores clave, nodos de influencia y estructuras digitales.'),
    ('PSYOPS: Diseño de campañas de influencia basadas en OSINT y SOCMINT',
     'Comprende cómo la información obtenida mediante OSINT y SOCMINT puede utilizarse para analizar narrativas, audiencias y dinámicas de influencia.',
     'Segmentación de audiencias, análisis de comportamiento, narrativas, percepción e impacto comunicacional.',
     'Análisis de una estrategia de influencia digital a partir de información obtenida en fuentes abiertas y redes sociales.'),
    ('Análisis y visualización de datos complejos aplicado a OSINT',
     'Transforma grandes volúmenes de información en visualizaciones claras que permitan reconocer patrones y apoyar decisiones.',
     'Dashboards, visualización de datos, identificación de patrones, relaciones entre actores y representación de información compleja.',
     'Construcción de un dashboard para presentar hallazgos y convertir datos OSINT/SOCMINT en inteligencia visual.'),
]
def acc_keep(acc_id, n):
    """Deja los n primeros ítems del acordeón anidado (JSON y vista previa)."""
    acc = ELEM[acc_id]
    drop = [c['id'] for c in acc['elements'][n:]]
    acc['elements'] = acc['elements'][:n]; acc['settings']['items'] = acc['settings']['items'][:n]
    def f(blk):
        for d in drop:
            blk, k = re.subn(r'\s*<details\b(?:(?!</details>).)*?data-id="%s".*?</details>' % d, '', blk, count=1, flags=re.S)
            assert k, d
        return blk
    html_sub_in(acc_id, f)
acc_keep('5b410621', len(MODS))
acc_titles('5b410621', [m[0] for m in MODS])
for _body, (_t, _d, _ap, _apl) in zip(kids('5b410621'), MODS):
    _intro = [k for k in kids(_body) if ELEM[k].get('widgetType') == 'text-editor'][0]
    text(_intro, '<p>' + _d + '</p>')
    _row = [k for k in kids(_body) if ELEM[k]['elType'] == 'container'][0]
    for _card, _txt in zip(kids(_row), (_ap, _apl)):
        _te = [k for k in kids(_card) if ELEM[k].get('widgetType') == 'text-editor'][0]
        text(_te, '<p>' + _txt + '</p>')

# ============ 9. Banner próxima edición
text('1251cd12', '<p>Inicio: 16 de setiembre | Online vía Zoom | 7 Módulos</p>')
bg_set('4d64e131', 'banner-proxima-edicion-osint-socmint.webp')

# ============ 10. Docentes (los 4 del PDF; Bazán primero, pedido del usuario)
heading('53717cd', 'Aprende de especialistas en<br> <span class="ak-g">inteligencia digital y ciberseguridad</span>')
bg_set('613c44c5', 'fondo-docentes-osint-socmint.webp'); bgc('613c44c5', DARK_G)
DOC_CAR = '79feacd4'
DOC_ORDER = ['183f21cd', '195a4326', '336d9ea6', '4bd7554a']   # diapositivas: (Andrés Peñaranda ->) Bazán, (Francisco López ->) Ausejo, De la Torre, Catanzariti
_car = ELEM[DOC_CAR]
_items = {sl['id']: it for sl, it in zip(_car['elements'], _car['settings']['carousel_items'])}
_slides = {sl['id']: sl for sl in _car['elements']}
_car['elements'] = [_slides[i] for i in DOC_ORDER]
_car['settings']['carousel_items'] = [_items[i] for i in DOC_ORDER]
for _i, _t in zip(DOC_ORDER, ('Roberto Bazán', 'Rafael Ausejo', 'Eduardo de la Torre', 'Gonzalo Catanzariti')): _items[_i]['slide_title'] = _t
def _doc_html(blk):
    w0 = blk.index('<div class="swiper-wrapper"'); w1 = blk.index('>', w0) + 1
    d = 0
    for t in re.finditer(r'<div\b|</div>', blk[w0:]):
        d += 1 if t.group(0) == '<div' else -1
        if d == 0: wend = w0 + t.start(); break
    sl = {}
    for a, b in _kids(blk, w1, wend):
        m = re.search(r'data-id="([0-9a-f]+)"', blk[a:b]); sl[m.group(1)] = blk[a:b]
    out = []
    for k, i in enumerate(DOC_ORDER):
        x = re.sub(r'aria-label="\d+ / \d+"', 'aria-label="%d / %d"' % (k + 1, len(DOC_ORDER)), sl[i], count=1)
        out.append(x)
    blk = blk[:w1] + '\n' + '\n'.join(out) + '\n' + blk[wend:]
    return blk
html_sub_in(DOC_CAR, _doc_html)
# tarjeta 1: Ausejo (España)
heading('6680ceb3', 'Ing. Rafael Ausejo')
heading('79769873', 'Experto en ciberseguridad, inteligencia e inteligencia artificial')
# tarjeta de Ausejo de las otras landings (Alta Dirección, Programa de Inteligencia): 2026/09/Rectangle-8-7.webp.
# Trae las esquinas redondeadas transparentes: el fondo de la tarjeta toma el azul de la foto para que no se noten.
bg_set('dba40cc', 'Rectangle-8-7.webp')
bgc('dba40cc', '#07161F')
button('75a74c29', 'Ver trayectoria', 'https://grupogoberna.com/rafael-ausejo/')
# tarjeta 2: De la Torre (Colombia) -- ya trae su foto y su enlace
heading('77221cd', 'Mg. Eduardo de la Torre')
# tarjeta 3: Catanzariti (Argentina)
heading('128f09a4', 'Ing. Gonzalo Catanzariti')
button('53554299', 'Ver trayectoria', 'https://grupogoberna.com/gonzalo-catanzariti/')
# tarjeta 4: Bazán (Perú) -- foto de tarjeta y bandera que ya están en la Biblioteca
image('2e2bb6e9', 'bandera-peru-1.png')
heading('2a7b35b3', 'Perú')
heading('4d05e8e4', 'Roberto Bazán')
heading('74b539d4', 'Especialista en inteligencia estratégica y operaciones psicológicas')
bg_set('25393af0', 'card-roberto-bazan-2.webp')
button('2ea3bff', 'Ver trayectoria', 'https://grupogoberna.com/roberto-bazan/')
LOG.append('Docentes: 4 tarjetas (Bazán, Ausejo, De la Torre, Catanzariti). Fotos: las tarjetas que usan las otras landings.')

# ============ 11. Presencia internacional (textos intactos; fondo del Figma)
bg_set('63b5ee4a', 'fondo-presencia-osint-socmint.webp'); bgc('63b5ee4a', '#031202')

# ============ 12. Certificación (imagen del Figma)
bgc('28c43ad5', DARK_G)
setv('28c43ad5', background_xpos={'unit': '%', 'size': 0, 'sizes': []}, background_ypos={'unit': '%', 'size': 50, 'sizes': []})
bg_set('28c43ad5', 'certificado-osint-socmint.webp', pos='0% 50%')
heading('2c9c857c', 'Una certificación para<br> <span class="ak-g">quienes dominan la<br> investigación digital</span>')
text('3f88c4d3', '<p>Al culminar satisfactoriamente el programa recibirás la certificación como <strong class="ak-g">Asesor Especializado en Osint y Socmint</strong>. Una acreditación que reconoce tu formación en recolección de información, monitoreo de redes sociales, análisis digital y generación de productos de inteligencia.</p>')
css_add('54c4c5af', 'selector .ak-cert-p strong.ak-g { color: ' + GREEN + '; font-weight: 700; }')
text('3f0fb31c', '<p>Credencial digital verificable para validar tu formación profesional.</p>')
for _i in ('3f88c4d3', '334be732', '3f0fb31c'): color(_i, 'rgba(6,6,6,0.75)')

# ============ 13. Inversión y admisión
bg_set('7a49a06a', 'inversion-fondo-osint-socmint.webp'); bgc('7a49a06a', '#000300')
heading('2d4237ac', 'CONVIÉRTETE EN UN<br> ESPECIALISTA EN<br> INVESTIGACIÓN DIGITAL')
heading('9030ca2', '16 de setiembre')
heading('73517676', '7 MÓDULOS')
heading('dc295fa', '¿Listo para especializarte<br> en OSINT y SOCMINT?')
setv('7d4e2b0', form_name='OSINT & SOCMINT — Habla con un asesor', email_subject='Nuevo contacto: Diploma Técnico en OSINT & SOCMINT')
html_global('name="Carrera Diplomática — Habla con un asesor"', 'name="OSINT &amp; SOCMINT — Habla con un asesor"')
for _f in S('7d4e2b0')['form_fields']:
    if _f.get('custom_id') == 'cargo': _f['placeholder'] = 'Ej. Analista de inteligencia'
html_global('placeholder="Ej. Analista de política exterior"', 'placeholder="Ej. Analista de inteligencia"')

# ============ 14. Preguntas frecuentes (respuestas del PDF)
FAQ = [
    'Las sesiones se desarrollan 100% online y en vivo vía Zoom, combinando clases prácticas, demostraciones de herramientas, análisis de casos y ejercicios aplicados de investigación digital.',
    'El diploma tiene una duración de 3 semanas y está compuesto por 7 módulos, desarrollados de acuerdo con el cronograma establecido para el programa.',
    'Incluye acceso a las clases, materiales académicos y la certificación correspondiente al culminar satisfactoriamente el programa.',
    'Goberna cuenta con diferentes alternativas de pago para sus participantes. Al iniciar tu proceso de inscripción, un asesor te indicará las opciones habilitadas según tu país.',
    'Completa tus datos en el formulario y un asesor de GOBERNA se pondrá en contacto contigo para orientarte durante el proceso.',
]
for _i, _t in zip(('ea24eba', '77b34c1f', '3a6adec1', '584613f6', '38271e76'), FAQ):
    text(_i, '<p>' + _t + '</p>')

# ============ 15. Botones de contacto -> WhatsApp de OSINT (pedido del usuario)
for _b in ('9c2fe2d', '16c985f5', '2b7efae9'):
    button(_b, S(_b)['text'], WA)
    S(_b)['link']['is_external'] = 'on'
_old = [u for u in set(re.findall(r'https://wa\.me/[^"\s\\]+', json.dumps(J, ensure_ascii=False)))]
LOG.append('WhatsApp: %d enlace(s) wa.me restantes en el JSON: %s' % (len(_old), _old))
html_global('https://wa.me/51970356062?text=%C2%A1Hola%21%20Deseo%20m%C3%A1s%20informaci%C3%B3n%20sobre%20el%20Diploma%20Internacional%20de%20Inteligencia%20Aplicada%20a%20la%20Carrera%20Diplom%C3%A1tica.', WA.replace('&', '&amp;'))
LOG.append('Enlaces que pone el usuario: brochure (2 botones) y "Pagar ahora" siguen en "#".')

# ============ Posiciones del hero (Figma 1920: título a +229 del hero, 749x149; alto 879)
pad('2742d6b5', top=229, bottom=341, left=40, right=40)
pad('2742d6b5', '_laptop', top=163, bottom=247, left=80, right=80)

# ============ Metodología de aprendizaje: títulos de etapa en una línea como el Figma (desktop y laptop);
# en tablet el margen inferior negativo de la base (pensado para títulos de una palabra) pasa a 0
css_add('3028d48c', '@media (min-width: 1025px) { selector .ak-war-step h3 { white-space: nowrap; } }')
for _t in ('7a82957e', '245ad6bc', '544064c5', '1f78edf1'): margin(_t, '_tablet', top=10, bottom=0)

# ============ Plan de estudios: título en 3 líneas como el Figma (caja de 518 px)
css_add('7c39e8aa', '@media (min-width: 1367px) { selector .elementor-element-48da84d4 { max-width: 518px; } }')

# ============ Docentes: título partido como el Figma
heading('53717cd', 'Aprende de especialistas en <span class="ak-g">inteligencia<br> digital y ciberseguridad</span>')

# ============ Metodología de aprendizaje: color de fondo = el del Figma (donde la imagen no llega: tablet y mobile)
bgc('3028d48c', DARK_G)

# ============ Restos de la base en comentarios del CSS
css_sub('54c4c5af', '/* Carrera Diplomática: medidas del Figma', '/* OSINT & SOCMINT: medidas del Figma')
