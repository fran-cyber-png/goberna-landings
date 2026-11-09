# Cambios de Director de Seguridad sobre la base (se ejecuta dentro de transform.py)

# ============ 1. Paleta y fuentes (Figma: dorado #FFBB03, azul #15262F, gris claro #F3F5F7; títulos Montserrat)
replace_everywhere([
    # rojos de Crimen -> dorado
    ('#8C1A17', GOLD), ('#880000', GOLD), ('#B20505', GOLD), ('#C20000', GOLD), ('#97111E', GOLD),
    ('#A82220', GOLD), ('#A80F0F', GOLD), ('#C0707A', '#FFD466'),
    ('rgba(140,26,23,', 'rgba(255,187,3,'), ('rgba(140, 26, 23,', 'rgba(255, 187, 3,'),
    ('rgba(151,17,30,', 'rgba(255,187,3,'), ('rgba(151, 17, 30,', 'rgba(255, 187, 3,'),
    ('#F4E6E6', '#EBE8E3'), ('#EDDCDC', '#E2DDD5'),
    # negros / azules -> azul del Figma
    ('#070908', NAVY), ('#101519', NAVY), ('#031129', NAVY), ('#0C1522', NAVY), ('#070E21', NAVY),
    ('#070E20', NAVY), ('#0E1524', NAVY), ('#0B142D', NAVY), ('#0A132F', NAVY),
    # gris claro de fondo
    ('#EBEFF2', LIGHT), ('#FDFCFB', LIGHT),
    # títulos
    ('"Oswald"', '"Montserrat"'), ('Oswald', 'Montserrat'),
])

# ============ 2. Header
typo('4eed1ba', family='Inter', weight=400, ls=0)
color('4eed1ba', NAVY)

# ============ 3. Hero
heading('17c98689', 'Diploma de Élite Internacional Director de Seguridad')
image('1916fb3', 'titulo-director-seguridad.webp')
img_width('1916fb3', w=676, w_laptop=440, w_mobile=335)
sub = duplicate_after('17c98689')['17c98689']          # "-Programa internacional de GOBERNA-" (Figma)
move_after(sub, '1916fb3'); set_classes(sub, 'ak-hero-sub')
for k in [k for k in S(sub) if k.startswith('_position') or k.startswith('_offset')]: S(sub).pop(k)
html_sub_in(sub, lambda blk: blk.replace(' elementor-absolute ', ' ', 1))
heading(sub, '-Programa internacional de GOBERNA-')
typo(sub, family='Inter', weight=400, transform='uppercase', size=20, size_laptop=14, size_mobile=11, lh=32, lh_laptop=22, lh_mobile=18, ls=2.6, ls_laptop=1.8, ls_mobile=0.9)
color(sub, '#FFFFFF')
margin(sub, top=15); margin(sub, '_laptop', top=10); margin(sub, '_mobile', top=10, left=0)
margin('571a5de0', top=58)
pad('2742d6b5', bottom=265)
css_sub('2742d6b5', 'border-bottom: 1px solid rgba(184,196,222,.55)', 'border-bottom: 1px solid #FFBB03')
bg_image('2742d6b5', 'hero-fondo-director.webp', 'a/hero-fondo-1.webp')
button('263d369c', 'Descargar brochure del programa', '#')
LOG.append('PENDIENTE: link del brochure de Director de Seguridad (botones "Descargar brochure").')
color('4be49e01', NAVY)

# ============ 4. Barra de datos
heading('2cc03c73', 'Online')
heading('1c8584de', '30 de noviembre, 2026')
heading('222abf5a', '19:00 hrs. GMT-5')
heading('1354e08f', '10 módulos')
heading('462fc185', 'USD $199')
for i, f in (('462340c3', 'barra-modalidad-director.svg'), ('3ca9ff3b', 'barra-inicio-director.svg'), ('54f34de7', 'barra-horario-director.svg'), ('4831e040', 'barra-duracion-director.svg')):
    icon_svg(i, f); color(i, NAVY)
color('4169ef5a', NAVY); color('462fc185', NAVY)
for i in ('3ee52be', '440c46a7', '6ff8d16a', '6cfb208a', '4169ef5a', '2cc03c73', '1c8584de', '1354e08f'):
    typo(i, weight=400, size=16, ls=2.4, ls_laptop=1.7, ls_mobile=1.2)
typo('222abf5a', weight=400, size=16, size_laptop=11, size_mobile=10, ls=2.4, ls_laptop=1.7, ls_mobile=1.2)   # mismo tamaño que los demás valores de la barra (pedido del usuario)
typo('462fc185', weight=400, ls=3.75, ls_laptop=2.7, ls_mobile=1.8)

# ============ 5. Metodología
heading('6abc5933', 'Metodología')
heading('60bb37d3', 'De la seguridad a dirigirla<br> estratégicamente')
typo('60bb37d3', weight=700, transform='none', lh=57, lh_laptop=40, lh_mobile=32, ls=-1.5, ls_laptop=-1, ls_mobile=-0.5)
text('5c3d58bb', '<p>Desarrolla una visión integral para proteger personas, información, instalaciones y operaciones desde la dirección.</p>')
mp = duplicate_after('6619f3a1')        # 4.ª fila: 100% Modalidad online en vivo
row4 = mp['6619f3a1']
num4 = mp['3314267']; txt4 = mp['17666b64']
heading(num4, '100%'); text(txt4, '<p>Modalidad online en vivo</p>')
text('5532455', '<p>Inteligencia <span>•</span> Ciberseguridad <span>•</span> Liderazgo <span>•</span> Crisis <span>•</span> Tecnología</p>')

# ============ 6. El programa
heading('80fac6b', 'El programa'); color('80fac6b', GOLD)
heading('37799678', 'Formar directores capaces<br class="ak-dk"> de diseñar, conducir y<br class="ak-dk"> <span class="ak-g">evaluar sistemas integrales<br class="ak-dk"> de seguridad</span>')
typo('37799678', weight=700, transform='none', lh=45, lh_laptop=36, lh_mobile=27, ls=-1.28, ls_laptop=-1, ls_mobile=-0.6)
TAB_TITLES = ['¿Cuál es el objetivo?', '¿A quiénes está dirigido?', 'Perfil del egresado']
for k, t in enumerate(TAB_TITLES): S('4e1aa122')['tabs'][k]['tab_title'] = t
def _tabs(blk):
    it = iter(TAB_TITLES)
    return re.sub(r'(<span class="e-n-tab-title-text">)(.*?)(</span>)', lambda m: m.group(1) + next(it) + m.group(3), blk, flags=re.S)
html_sub_in('4e1aa122', _tabs)
heading('5a5d4853', 'Objetivo del diploma')
text('1e2e258a', '<p>Formar directores capaces de diseñar, conducir y evaluar sistemas integrales de seguridad, identificando amenazas, priorizando riesgos y tomando decisiones alineadas con los objetivos de una organización.</p>'
                 '<p>Durante el diploma desarrollarás capacidades para dirigir equipos y recursos, proteger personas, instalaciones e información, gestionar crisis y sustentar decisiones ante la alta dirección mediante un Plan Director de Seguridad.</p>'
                 '<ul><li>Dirección de seguridad</li><li>Gestión de riesgos y seguridad corporativa</li><li>Protección de instalaciones y contrainteligencia</li><li>Investigaciones y debida diligencia</li></ul>')
# contenido de las pestañas 2 y 3: PDF "CONTENIDO LANDINGS (3)" (antes: frames 128 y 129 del Figma, que traían el texto de Asesor Presidencial)
heading('3dff5c49', '¿Para quién es este diploma?')
text('2d2f5c00', '<p>Dirigido a:</p><ul>'
                 '<li>Directores, gerentes, jefes, coordinadores y supervisores de seguridad.</li>'
                 '<li>Miembros de Fuerzas Armadas, Policía y responsables de protección institucional.</li>'
                 '<li>Consultores, auditores y analistas de riesgos.</li>'
                 '<li>Profesionales de inteligencia, operaciones, tecnología y compliance.</li>'
                 '<li>Responsables de emergencias y continuidad operativa.</li>'
                 '<li>Profesionales que buscan asumir funciones de dirección y gestión de seguridad.</li>'
                 '</ul>')
heading('36ba7119', 'Qué lograrás')
text('73081eaa', '<p>Al finalizar el diploma estarás preparado para dirigir la función de seguridad de manera integral, priorizar riesgos, gestionar recursos y coordinar capacidades de protección frente a escenarios complejos.</p>'
                 '<p>Podrás desenvolverte en:</p>'
                 '<p>Dirección de seguridad · Gestión de riesgos · Seguridad corporativa · Protección de instalaciones · Contrainteligencia · Investigaciones</p>')


# ============ 7. Experiencia estratégica (War Room)
heading('2ac64e45', 'Experiencia estratégica'); color('2ac64e45', GOLD)
heading('100b98eb', 'Aquí no solo<br> estudias seguridad.<br> <span class="ak-g">Aprendes a dirigirla</span>')
typo('100b98eb', weight=700, transform='none', lh=53, lh_unit='px', lh_laptop=38, lh_mobile=30)
text('5837a4c2', '<p>La metodología está conectada con el ejercicio profesional de seguridad. Desde el primer módulo sobre una organización o caso, desarrollando productos que se integrarán progresivamente en tu Plan Director de Seguridad.</p>')
STEPS = [('7a4fdaad', '242db4c1', 'Diagnostica', 'Identifica amenazas, vulnerabilidades y riesgos que pueden comprometer a la organización.'),
         ('3b8ef21', '16d90998', 'Prioriza', 'Convierte el análisis en decisiones sobre recursos, controles y medidas de protección.'),
         ('7b493c97', '206d7f1c', 'Dirige', 'Coordina personas, proveedores, tecnología y capacidades de seguridad bajo una misma estrategia.'),
         ('c9a5787', '2364deb0', 'Responde', 'Enfrenta crisis y escenarios complejos protegiendo la continuidad de las operaciones.')]
for h, t, ht, tt in STEPS:
    heading(h, ht); typo(h, family='Barlow', weight=700, transform='none')
    text(t, f'<p>{tt}</p>')
bg_image('592e977f', 'war-room-fondo-director.webp', 'a/war-room-fondo.webp')
width_pct('7225a212', w=44)

# ============ 8. Plan de estudios
heading('7a10f30c', 'Plan de estudios')
heading('29610b73', 'Diez módulos.<br class="ak-dk"> Una sola lógica<br class="ak-dk"> de dirección.')
typo('29610b73', weight=700, transform='none', size=50, lh=0.98, lh_unit='em')
for i, t in (('6731b1fb', '10'), ('47c0bf1c', 'Módulos'), ('79958606', 'Especializados'),
             ('d847877', '200'), ('2e9f1272', 'Horas'), ('1ae69e15', 'Académicas'),
             ('135b5aeb', '100 %'), ('134cdce8', 'Metodología práctica'), ('1730263a', 'Aprende haciendo')):
    heading(i, t)
for i, f in (('7a3679d8', 'plan-modulos-caja.svg'), ('3c5b175c', 'plan-horas-caja.svg'), ('428402c6', 'plan-metodologia-caja.svg')):
    icon_svg(i, f)
button('17ca50d8', 'Descargar brochure', '#')
# Módulos: títulos del Figma (1 a 3) y contenido del PDF "CONTENIDO LANDINGS (3)" (descripciones 2 a 10, Aprenderás / Aplicarás)
MODS = [
 ('El director de seguridad: visión estratégica, gobierno y conducción',
  'Conoce el rol del director de seguridad y aprende cómo se organiza y dirige la función de seguridad desde cero.',   # Figma
  'Gobierno de seguridad, estructuras, atribuciones, políticas, responsabilidades y criterios de supervisión.',
  'Definición de la estructura, responsabilidades y criterios de conducción de la función de seguridad.'),
 ('Inteligencia de amenazas y gestión estratégica del riesgo',
  'Identifica amenazas, vulnerabilidades y escenarios para priorizar riesgos y orientar decisiones de protección.',
  'OSINT, verificación de información, indicadores, alertas tempranas y evaluación de probabilidad e impacto.',
  'Construcción de escenarios de riesgo y priorización de medidas de tratamiento.'),
 ('Gestión directiva de la seguridad',
  'Aprende a conducir equipos y administrar los recursos necesarios para ejecutar una estrategia de seguridad.',
  'Liderazgo, organización operativa, presupuestos, costos, proveedores y evaluación de desempeño.',
  'Diseño de responsabilidades, recursos, indicadores y criterios de supervisión de proveedores.'),
 ('Seguridad física y protección de instalaciones',
  'Diseña sistemas de protección capaces de integrar infraestructura, procedimientos, personas y tecnología.',
  'Defensa en profundidad, accesos, videovigilancia, detección, vigilancia humana y centros de control.',
  'Diseño de un esquema de protección física por capas según las vulnerabilidades de una instalación.'),
 ('Ciberseguridad y protección de la información crítica',
  'Comprende los riesgos digitales que pueden comprometer información, redes y continuidad de los servicios.',
  'ISO 27001, marco NIST, protección de datos, riesgos de terceros y respuesta ante incidentes.',
  'Articulación de controles físicos y digitales y definición de responsabilidades frente a riesgos tecnológicos.'),
 ('Contrainteligencia y vigilancia técnica',
  'Identifica riesgos de espionaje, obtención de información y vigilancia que pueden comprometer espacios y comunicaciones críticas.',
  'Contrainteligencia, espionaje, vulnerabilidades de información y fundamentos de TSCM.',
  'Definición de medidas de protección y criterios para implementar contramedidas de vigilancia técnica.'),
 ('Investigaciones de seguridad y debida diligencia',
  'Aprende a abordar irregularidades internas y evaluar riesgos de integridad asociados a terceros.',
  'Fraude, corrupción, hipótesis investigativas, entrevistas, evidencias, cadena de custodia y due diligence.',
  'Estructuración de una investigación y evaluación de riesgos de integridad en terceros y proveedores.'),
 ('Protección ejecutiva y seguridad de personas',
  'Gestiona los riesgos que pueden afectar a directivos, autoridades, colaboradores y personas especialmente expuestas.',
  'Protección ejecutiva, viajes, antecedentes, amenazas internas, violencia laboral, secuestro y extorsión.',
  'Evaluación de riesgos y coordinación de medidas de protección adaptadas al perfil y al escenario.'),
 ('Dirección de crisis, emergencias y continuidad operativa',
  'Prepárate para conducir la respuesta cuando un incidente amenaza operaciones, servicios o activos críticos.',
  'Comités de crisis, activación, contingencias, evacuación, comunicación, BIA y continuidad operativa.',
  'Diseño de prioridades de respuesta, continuidad y recuperación frente a una crisis.'),
 ('Proyecto Integrador: Plan Director de Seguridad',
  'Integra todas las capacidades del programa en un sistema de seguridad alineado con las necesidades reales de una organización.',
  'Integración estratégica, definición de prioridades, responsables, plazos e indicadores de seguimiento.',
  'Construcción y sustentación de un Plan Director de Seguridad ante un comité simulado.'),
]
acc = S('f8ee414')
for k in range(8): acc['items'][k]['item_title'] = MODS[k][0]
def _acc(blk):
    it = iter(m[0] for m in MODS[:8])
    return re.sub(r'(<div class="e-n-accordion-item-title-text">)(.*?)(</div>)', lambda m: m.group(1) + ' ' + next(it) + ' ' + m.group(3), blk, count=8, flags=re.S)
html_sub_in('f8ee414', _acc)
css_sub('f8ee414', 'selector .e-n-accordion-item-title-text { font: 600 24px/29px Montserrat, sans-serif !important; text-transform: uppercase;', 'selector .e-n-accordion-item-title-text { font: 600 24px/29px Montserrat, sans-serif !important; text-transform: none;')
bodies = [c['id'] for c in ELEM['f8ee414']['elements']]
for t in (MODS[8][0], MODS[9][0]):
    acc_add_item('f8ee414', bodies[7], t)          # siempre desde el módulo 8 original (sus reglas de CSS están en la base)
    bodies.append(ELEM['f8ee414']['elements'][-1]['id'])
def body_widgets(body):
    """(descripción, texto Aprenderás, texto Aplicarás) de un ítem del plan."""
    e = ELEM[body]; desc = e['elements'][0]['id']
    inner = e['elements'][1]['elements']
    return desc, inner[0]['elements'][1]['id'], inner[1]['elements'][1]['id']
for body, (title, d, apr, apl) in zip(bodies, MODS):
    di, ai, pi = body_widgets(body)
    text(di, f'<p>{d}</p>'); text(ai, f'<p>{apr}</p>'); text(pi, f'<p>{apl}</p>')

# ============ 9. Banner próxima edición
heading('70bf28fa', '¿Quieres vivir esta experiencia<br> en la próxima edición?')
typo('70bf28fa', transform='none')
text('6a3db432', '<p>Inicio: 30 de noviembre | Online en vivo | 10 Módulos</p>')
bg_image('2e83b302', 'banner-proxima-edicion-director.webp', 'a/banner-proxima-edicion_2x-1-scaled.webp')
color('1bd3966', NAVY)

# ============ 10. Presencia internacional
heading('75122411', 'Presencia internacional'); color('75122411', GOLD)
heading('23841199', 'Una red que habla el<br> idioma <span class="ak-g">político de<br> Latinoamérica.</span>')
typo('23841199', weight=700, transform='none')
bg_image('63b5ee4a', 'fondo-presencia-director.webp', 'a/fondo-presencia-1.webp')
image('52c31379', 'mapa-director-base.webp')
image('6e7fedc6', 'mapa-director-puntos.svg')

# ============ 11. Certificación
heading('1b9af742', 'Certificación')
heading('2c9c857c', 'Una formación<br class="ak-mb"> <span class="ak-g">Dos<br class="ak-dk"> formas de acreditarla.</span>')
typo('2c9c857c', weight=700, transform='none')
text('3f88c4d3', '<p>Al culminar satisfactoriamente el programa recibirás la certificación como Director de Seguridad, emitida por Grupo Goberna.<br>Además, podrás solicitar una certificación adicional respaldada por Fundación San Marcos (US$35 adicional).</p>')
heading('1b6533dd', 'GOBERNA'); typo('1b6533dd', weight=600)
text('334be732', '<p>Diploma Internacional<br>del Director de Seguridad</p>')
heading('4351992b', 'Fundación San Marcos'); typo('4351992b', weight=600)
text('3f0fb31c', '<p>Doble certificación — Adicional US$35</p>')
icon_svg('940608c', 'certificacion-medalla-dorada.svg'); icon_svg('1adb523', 'certificacion-medalla-dorada.svg')
color('940608c', GOLD); color('1adb523', GOLD)          # medalla Grupo 29508 en el amarillo del proyecto (pedido del usuario)
bg_image('28c43ad5', 'certificado-director.webp', 'a/Gemini_Generated_Image_t3fw25t3fw25t3fw-1.png')

# ============ 12. Inversión y admisión
heading('125455a4', 'Inversión')
heading('2d4237ac', 'Lidera la seguridad<br> con visión estratégica')
typo('2d4237ac', weight=700, transform='none', lh=54, lh_unit='px', lh_laptop=41, lh_mobile=26)
heading('6ff88f9a', 'Inicio'); heading('9030ca2', '30 de noviembre')
heading('609843a9', 'Facilidades'); heading('73517676', 'Hasta en 4 cuotas')
color('79c591de', NAVY)
text('12c8534c', '<p>Vacantes limitadas para garantizar la dinámica del War Room.</p>')
color('12c8534c', GOLD); typo('12c8534c', transform='none')
heading('5c314a2a', 'Admisión')
heading('dc295fa', '¿Listo para liderar la seguridad de una organización?')
typo('dc295fa', weight=700, transform='none', size=41, size_laptop=32, lh=40, lh_unit='px', lh_laptop=32, lh_mobile=26, ls=-2.05, ls_laptop=-1.5, ls_mobile=-0.8)
heading('2a8cefb0', 'Déjanos tus datos y te ayudaremos con tu inscripción.')
f = S('7d4e2b0')
for fld in f['form_fields']:
    if fld.get('field_label') == 'Cargo': fld['placeholder'] = 'Ej. Jefe de seguridad'
f['button_text'] = 'Enviar'
html_global('placeholder="Ej. Jefe de campaña"', 'placeholder="Ej. Jefe de seguridad"')
html_sub_in('7d4e2b0', lambda blk: re.sub(r'(<span class="elementor-button-text">)Quiero que me contacten(</span>)', r'\1Enviar\2', blk))
color('3e72a9d', GOLD); typo('3e72a9d', transform='none')
no_bg_image('7a49a06a')

# ============ 13. Experiencia Goberna
heading('11acca34', 'Experiencia Goberna')
heading('7d8995c7', 'Más que un aula:<br><span class="ak-g">Una comunidad<br class="ak-dk"> que actúa</span>')
typo('7d8995c7', weight=700, transform='none', size=48, lh=1.2, lh_unit='em')
for card, im, flag, nm, ct, n, fl, name, country in (
        ('6ecaea76', '755ebdd8', '57210006', '61b28769', '74c41ee3', 'testimonio-thumb-alina.webp', 'bandera-colombia.png', 'Alina Martínez', 'Colombia'),
        ('52bcbaf4', '746bcfbc', '4490d8ac', '751b50ae', '1c41a4eb', 'testimonio-thumb-lorena.webp', 'bandera-bolivia.png', 'Lorena Coria', 'Bolivia'),
        ('5363d98a', '411babc3', '5875c141', 'ac2b395', '12b6131', 'testimonio-thumb-miguel.webp', 'bandera-mexico-circulo.png', 'Miguel Figueroa', 'México')):
    image(im, n); image(flag, fl); heading(nm, name); heading(ct, country)
bg_image('5fe95b15', 'experiencia-goberna-promo.webp', 'a/testimonios-crimen-promo.webp')
VIDEOS_OLD = ['https://cms.goberna.club/public/01_dienys_vertical.mp4', 'https://cms.goberna.club/public/02_francisco_daniel_vertical.mp4', 'https://cms.goberna.club/public/03_pablo_benalcazar_vertical.mp4']
VIDEOS_NEW = ['https://cms.goberna.club/public/01_cuadrado_final_alina.mp4', 'https://cms.goberna.club/public/02_cuadrado_final_lorena.mp4', 'https://cms.goberna.club/public/03_cuadrado_final_miguel.mp4']
h = S('76cef54d')['html']
for o, n in zip(VIDEOS_OLD, VIDEOS_NEW): h = h.replace(o, n)
S('76cef54d')['html'] = h
html_sub_in('76cef54d', lambda blk: re.sub(r'(<div class="elementor-widget-container">)(.*)(</div>\s*</div>\s*)$', lambda m: m.group(1) + h + m.group(3), blk, count=1, flags=re.S))
LOG.append('POR CONFIRMAR: links mp4 de Alina y Miguel (puse 01_cuadrado_final_alina.mp4 y 03_cuadrado_final_miguel.mp4 siguiendo el patrón de Lorena).')

# ============ 14. Preguntas frecuentes
heading('2e54988f', 'Preguntas frecuentes')
heading('36d376ec', 'Resolvemos tus<br class="ak-dk"> dudas<br class="ak-mb"> <span class="ak-g">antes de<br class="ak-dk"> que decidas.</span>')
typo('36d376ec', weight=700, transform='none')
color('36d376ec', NAVY)
css_sub('521f33e5', 'selector .ak-faq-title .ak-g { color: #15262F; }', 'selector .ak-faq-title .ak-g { color: #FFBB03; }')
text('ea24eba', '<p>Las sesiones se desarrollan 100% online y en vivo vía Zoom, combinando clases especializadas, análisis de casos, talleres, ejercicios de mesa y simulaciones aplicadas a la dirección de seguridad.</p>')
# respuestas 2 a 5: PDF "CONTENIDO LANDINGS (3)"
text('77b34c1f', '<p>El diploma contempla 200 horas académicas, desarrolladas de acuerdo con el cronograma establecido para el programa.</p>')
text('3a6adec1', '<p>Tu inscripción incluye acceso al programa, materiales académicos, análisis de casos, ejercicios aplicados, acompañamiento durante el proceso formativo, desarrollo del Plan Director de Seguridad y la certificación correspondiente.</p>')
text('584613f6', '<p>GOBERNA cuenta con diferentes alternativas de pago para sus participantes. Al iniciar tu proceso de inscripción, un asesor te indicará las opciones habilitadas según tu país.</p>')
text('38271e76', '<p>Completa tus datos en el formulario y un asesor de GOBERNA se pondrá en contacto contigo para orientarte durante el proceso.</p>')

# ============ vista previa: el video de Metodología (iframe de cms.goberna) no carga dentro del Artifact
PREVIEW_CSS += '.elementor-element-68614c73 iframe{visibility:hidden}.elementor-element-68614c73 .ak-video{background:url(a/metodologia-video-poster.webp) center/cover no-repeat!important}'

# ============ ajustes de la comparación con el Figma
css_sub('56bf8b99', 'font: 500 20px/1.2 Montserrat, sans-serif !important; letter-spacing: -.64px; text-transform: uppercase; color: #F4F5F7 !important;',
        'font: 500 20px/1.2 Barlow, sans-serif !important; letter-spacing: -.64px; text-transform: uppercase; color: rgba(255,255,255,.75) !important;')
css_sub('56bf8b99', 'selector .ak-dip-tabs .e-n-tab-title-text::before { width: 34px; height: 34px; }', 'selector .ak-dip-tabs .e-n-tab-title-text::before { width: 48px; height: 48px; }')
remove('7c2a6a1f')                         # párrafo del plan: no está en el Figma
css_sub('f8ee414', 'selector .ak-mod-body > .e-con > .e-con:first-child { background-color: #F3F5F7 !important; }',
        'selector .ak-mod-body > .e-con > .e-con:first-child { background-color: #EBEFF2 !important; }')
css_sub('f8ee414', 'selector .e-n-accordion { max-height: 620px;', 'selector .e-n-accordion { max-height: 760px;')
css_sub('f8ee414', 'selector .e-n-accordion { max-height: 468px; }', 'selector .e-n-accordion { max-height: 560px; }')
setv('5837a4c2', _element_custom_width={'unit': 'px', 'size': 563, 'sizes': []}, _element_custom_width_laptop={'unit': 'px', 'size': 400, 'sizes': []})
EXTRA_CSS.append(pre('5837a4c2') + '{--container-widget-width:563px;--container-widget-flex-grow:0;width:var(--container-widget-width,563px);max-width:563px}'
                 '@media(max-width:1366px){' + pre('5837a4c2') + '{--container-widget-width:400px;width:400px;max-width:400px}}'
                 '@media(max-width:932px){' + pre('5837a4c2') + '{--container-widget-width:100%;width:100%;max-width:100%}}')
color('5837a4c2', 'rgba(255,255,255,0.75)')
for h, t, ht, tt in STEPS:
    color(t, 'rgba(255,255,255,0.75)')
css_sub('266b2296', 'font: 700 18px/1.35 Inter, sans-serif !important;', 'font: 400 18px/1.35 Inter, sans-serif !important;')
css_sub('266b2296', 'color: #FFBB03; fill: #FFBB03; }', 'color: #15262F; fill: #15262F; }')
css_sub('f8ee414', 'padding-top: 8px; max-width: 480px; }', 'padding-top: 8px; max-width: 560px; }')
bg_image('592e977f', 'war-room-fondo-movil-director.webp', 'a/war-room-fondo-movil.webp', key='background_image_mobile')
margin('37b76e9a', '_tablet', left=0)          # en la base el título de El programa queda 20px fuera de la pantalla en mobile
typo('4eed1ba', size_laptop=12)
css_sub('f8ee414', 'selector .e-n-accordion { max-height: 560px; }', 'selector .e-n-accordion { max-height: 600px; }')

# ============ Docentes: solo título y fondo del Figma (las tarjetas se dejan para el final, como pidió el usuario)
heading('1c0602e2', 'Aprende de especialistas en seguridad,<br> inteligencia y gestión de riesgos.')
typo('1c0602e2', weight=700, transform='none', size=48, size_laptop=36, lh=1.17, lh_unit='em')
bg_image('5b40c644', 'fondo-docentes-director.webp', 'a/fondo-docentes-1.webp')
typo('4eed1ba', size_laptop=11)
# Docentes: los 7 del PDF "CONTENIDO LANDINGS (3)", en su orden. Las 7 tarjetas copian la estructura de la primera de la base
# (en la base la 2.ª no tenía país y la 7.ª tenía la clase "ak-doc-e" en lugar de "ak-doc-es").
_old = {c['elements'][0]['settings'].get('background_image', {}).get('url', '').rsplit('/', 1)[-1]: c for c in ELEM['3bf0546']['elements']}
def _bg(fname):  return copy.deepcopy(_old[fname]['elements'][0]['settings']['background_image'])
def _flag(fname):
    for sl in ELEM['3bf0546']['elements']:
        im = sl['elements'][0]['elements'][0]['elements'][0]['settings'].get('image', {})
        if im.get('url', '').endswith('/' + fname): return copy.deepcopy(im)
FLAGS = {'España': _flag('bandera-espana-1.png'), 'Colombia': _flag('bandera-colombia-1.png'), 'Argentina': _flag('bandera-argentina.png')}
FLAG_FILE = {'España': 'bandera-espana-1.png', 'Colombia': 'bandera-colombia-1.png', 'Argentina': 'bandera-argentina.png'}
DOCENTES = [
 ('Francisco López', 'España', 'Especialista en dirección de seguridad, criminología y prevención del crimen',
  'Doctor en Criminología, con formación especializada en dirección y gestión de seguridad, ciberinteligencia, análisis y prevención del crimen. Su trayectoria combina investigación, seguridad empresarial y aplicación de tecnologías para la prevención del delito.',
  'card-sin-foto.webp', '#'),
 ('Gonzalo Catanzariti', 'Argentina', 'Especialista en ciberinteligencia e investigación digital',
  'Analista de amenazas y delitos informáticos, con experiencia en evidencia digital e investigación del cibercrimen.',
  'card-sin-foto.webp', '#'),
 ('Eduardo Velandia Becerra', 'Colombia', 'Especialista en inteligencia, seguridad y conducción de equipos',
  'Teniente Coronel (r) de Inteligencia del Ejército de Colombia, con más de 24 años liderando equipos en escenarios de alta complejidad.',
  'card-eduardo-velandia-sitio.webp', '#'),
 ('Andrés Peñaranda', 'Colombia', 'Especialista en operaciones de información y seguridad estratégica',
  'Asesor político y especialista en comunicación estratégica, con experiencia en operaciones de información y psicológicas en Latinoamérica.',
  'card-andres-penaranda-1.webp', '#'),
 ('Mg. Eduardo de la Torre', 'Colombia', 'Especialista en ciberseguridad, ciberdefensa y análisis digital',
  'Consultor y docente en ciberseguridad con experiencia en implementación de soluciones de seguridad y proyectos tecnológicos. Cuenta con una maestría en Ciberseguridad y Ciberdefensa, especializándose en la gestión de recursos para la defensa nacional y análisis estratégico en entornos de seguridad.',
  'card-eduardo-de-la-torre-1.webp', 'https://grupogoberna.com/eduardo-de-la-torre/'),
 ('Daniela Galván', 'Argentina', 'Especialista en investigación criminal e inteligencia digital',
  'Profesional con más de 14 años de experiencia en investigación criminal, OSINT, SOCMINT, Virtual HUMINT y ciberpatrullaje. Se desempeña en la Dirección General de Cibercrimen de la Policía Federal Argentina.',
  'card-daniela-galvan-1.webp', '#'),
 # Diego Miranda: quitado por pedido del usuario
]
_bgs = {f: _bg(f) for f in ('card-andres-penaranda-1.webp', 'card-eduardo-de-la-torre-1.webp', 'card-daniela-galvan-1.webp', 'card-diego-miranda-2.webp')}
maps = carousel_rebuild('3bf0546', len(DOCENTES), [d[0] for d in DOCENTES])
for mp, (name, country, esp, bio, card, link) in zip(maps, DOCENTES):
    g = lambda i: mp[i]
    heading(g('360eb295'), name); heading(g('768d382a'), esp); text(g('e403aaf'), f'<p>{bio}</p>')
    button(g('1f339abe'), 'Ver trayectoria', link)
    heading(g('e549d8e'), country)
    fl = FLAGS[country]; S(g('7d3d3df6'))['image'] = fl
    html_sub_in(g('7d3d3df6'), lambda blk, fn=FLAG_FILE[country]: re.sub(r'(<img\b[^>]*?\ssrc=")[^"]*', lambda m: m.group(1) + 'a/' + fn, blk, count=1))
    cid = g('6eb1afa2')
    if card in _bgs: S(cid)['background_image'] = _bgs[card]
    else:
        url, iid = wp(card); S(cid)['background_image'] = {'url': url, 'id': iid, 'size': '', 'alt': '', 'source': 'library'}
    EXTRA_CSS.append(pre(cid) + ':not(.elementor-motion-effects-element-type-background){background-image:url("a/' + card + '")}')
LOG.append('PENDIENTE: fotos de Francisco López y Gonzalo Catanzariti (las del Figma son de Roberto Bazán y Diego Miranda). Links "Ver trayectoria" de Francisco, Gonzalo, Eduardo Velandia, Andrés y Daniela.')

# ============ revisión 1 (usuario): El programa
# franja derecha del bloque de pestañas: azul como el panel oscuro (en Crimen era la franja de color)
S('4e1aa122')['_border_color'] = NAVY
EXTRA_CSS.append(pre('4e1aa122') + ' > .elementor-widget-container{border-color:#15262F}')
# misma separación barra -> ícono que ícono -> texto (5px de barra + 24px)
css_sub('56bf8b99', 'padding: 0 4px 0 12px !important;', 'padding: 0 4px 0 29px !important;')
css_add('56bf8b99', '''@media (max-width: 1366px) { selector .ak-dip-tabs .e-n-tab-title { padding-left: 23px !important; } }
@media (max-width: 1024px) { selector .ak-dip-tabs .e-n-tab-title { padding-left: 19px !important; } }''')
# pestaña 2: los ítems de la lista van con 10px entre sí (Figma, frame 128)
set_classes('2d2f5c00', 'ak-dip-list')
import base64 as _b64
_flecha = _b64.b64encode(open(os.path.join(ROOT, 'iconos-webp', 'vineta-flecha-dorada.webp'), 'rb').read()).decode()
css_add('56bf8b99', '''selector .ak-dip-list ul { list-style: none; margin: 0; padding: 0; }
selector .ak-dip-list li { position: relative; padding-left: 26px; margin-bottom: 10px; }
selector .ak-dip-list li:last-child { margin-bottom: 0; }
selector .ak-dip-list li::before { content: ""; position: absolute; left: 0; top: calc(.89em - 7px); width: 14px; height: 14px; background: url(data:image/webp;base64,''' + _flecha + ''') center / contain no-repeat; }
@media (max-width: 1366px) { selector .ak-dip-list li { padding-left: 22px; } selector .ak-dip-list li::before { width: 12px; height: 12px; top: calc(.89em - 6px); } }''')
# pestaña 1: viñetas como puntos dorados (pedido del usuario)
set_classes('1e2e258a', 'ak-dip-dots')
css_add('56bf8b99', '''selector .ak-dip-dots ul { list-style: none; margin: 0; padding: 0; }
selector .ak-dip-dots li { position: relative; padding-left: 20px; }
selector .ak-dip-dots li::before { content: ""; position: absolute; left: 2px; top: calc(.92em - 3px); width: 6px; height: 6px; border-radius: 50%; background: #FFBB03; }''')
# FAQ: "+" en azul cuando la pregunta está cerrada (Figma); el "−" abierto sigue en blanco sobre dorado
css_add('266b2296', 'selector .e-n-accordion-item:not([open]) .e-n-accordion-item-title-icon i, selector .e-n-accordion-item:not([open]) .e-n-accordion-item-title-icon svg { color: #15262F !important; fill: #15262F !important; }')

# ============ revisión: tarjetas Aprenderás / Aplicarás
# en la base las dos tarjetas miden 50% + 20px de separación y la de la derecha se salía 20px del acordeón
# (que recorta con overflow), por eso perdía las esquinas redondeadas de la derecha
css_add('f8ee414', 'selector .ak-mod-body > .e-con > .e-con { flex-shrink: 1 !important; min-width: 0; border-radius: 8px; }')

# ============ revisión: animación suave al abrir / cerrar los módulos (y las preguntas frecuentes)
# Elementor anima la altura con su JS según n_accordion_animation_duration; la dejamos explícita en 450 ms
# y el contenido entra con un fundido corto.
for acc_id in ('f8ee414', '266b2296'):
    S(acc_id)['n_accordion_animation_duration'] = {'unit': 'ms', 'size': 450, 'sizes': []}
    html_sub_in(acc_id, lambda blk: re.sub(r'(data-settings="[^"]*?)&quot;n_accordion_animation_duration&quot;:\{[^}]*\}', r'\1&quot;n_accordion_animation_duration&quot;:{&quot;unit&quot;:&quot;ms&quot;,&quot;size&quot;:450,&quot;sizes&quot;:[]}', blk, count=1))
    css_add(acc_id, '''selector .e-n-accordion-item[open] > .e-con { animation: ak-acc-in .45s ease both; }
@keyframes ak-acc-in { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: none; } }
@media (prefers-reduced-motion: reduce) { selector .e-n-accordion-item[open] > .e-con { animation: none; } }''')

# ============ revisión: el título del módulo no cambia de ancho al abrir/cerrar
# "Ver contenido +" es más ancho que "Ocultar −"; la columna del rótulo cambiaba de ancho y el título se reacomodaba.
# Las dos etiquetas ocupan ahora la misma celda (la inactiva invisible), así la columna siempre mide lo de la más ancha.
css_add('f8ee414', '''selector .e-n-accordion-item-title-icon { display: grid !important; justify-items: end; align-items: center; }
selector .e-n-accordion-item-title-icon > span { grid-area: 1 / 1; }
selector .e-n-accordion-item:not([open]) .e-n-accordion-item-title-icon .e-opened,
selector .e-n-accordion-item[open] .e-n-accordion-item-title-icon .e-closed { display: inline-flex !important; visibility: hidden; }''')
# Bios del PDF más largas que las de la base (hasta 7 líneas): el bloque de texto sube para que "Ver trayectoria"
# no se salga de la tarjeta; todas las tarjetas mantienen el nombre a la misma altura.
css_add('5b40c644', '''selector .ak-doc-card > .e-con.ak-doc-body { top: 53%; }
selector .ak-doc-card::after { background: linear-gradient(to bottom, rgba(6,6,6,0) 40%, rgba(6,6,6,.6) 56%, rgba(6,6,6,.75) 70%, rgba(6,6,6,.85) 90%); }''')
css_add('5b40c644', '''@media (max-width: 1366px) { selector .ak-doc-card > .e-con.ak-doc-body { top: 44%; } selector .ak-doc-card::after { background: linear-gradient(to bottom, rgba(6,6,6,0) 32%, rgba(6,6,6,.6) 47%, rgba(6,6,6,.75) 62%, rgba(6,6,6,.85) 88%); } }
@media (max-width: 1024px) { selector .ak-doc-card > .e-con.ak-doc-body { top: 47%; } }
@media (max-width: 932px) { selector .ak-doc-card > .e-con.ak-doc-body { top: 43%; } }
@media (max-width: 767px) { selector .ak-doc-card > .e-con.ak-doc-body { top: 45%; } }''')

# Certificación (mobile): el botón "Quiero la doble certificación" se salía 33 px de la pantalla (también en la base)
css_add('54c4c5af', '''@media (max-width: 767px) {
  selector .ak-cert-btn, selector .ak-cert-btn .elementor-button-wrapper { width: 100%; }
  selector .ak-cert-btn .elementor-button { min-width: 0 !important; width: 100% !important; height: auto !important; min-height: 44px; padding: 10px 14px !important; }
  selector .ak-cert-btn .elementor-button-text { white-space: normal !important; text-align: center; }
}''')

# ============ revisión: Inversión / Admisión — "Quiero inscribirme" alineado con "Enviar"
# Los dos botones quedan al fondo de su columna con el mismo bloque debajo: la nota de la izquierda toma
# el mismo estilo y margen que la de privacidad de la derecha (una línea, 16 px arriba).
css_sub('7a49a06a', 'selector .ak-inv-buy { margin-top: auto !important; margin-bottom: 33px !important; width: 100%; }',
        'selector .ak-inv-buy { margin-top: auto !important; margin-bottom: 0 !important; width: 100%; }')
css_sub('7a49a06a', '@media (max-width: 1366px) { selector .ak-inv-buy { margin-bottom: 31px !important; }', '@media (max-width: 1366px) { selector .ak-inv-buy { margin-bottom: 0 !important; }')
typo('12c8534c', size=14, size_laptop=12, size_mobile=10, lh=1.4, lh_unit='em', ls=0.7, ls_laptop=0.6, ls_mobile=0.5)
margin('12c8534c', top=16, bottom=0); margin('12c8534c', '_laptop', top=16, bottom=0)
# "Enviar": texto dorado como su borde
S('7d4e2b0')['button_text_color'] = GOLD
EXTRA_CUSTOM.append(pre('7d4e2b0') + ' .elementor-button[type="submit"]{color:#FFBB03}' + pre('7d4e2b0') + ' .elementor-button[type="submit"]:hover{color:#15262F}')
# entre 1025 y 1366 px la nota de la izquierda puede ocupar 2 líneas y la de la derecha 1: las dos reservan 2 líneas
css_add('7a49a06a', '@media (min-width: 1025px) and (max-width: 1366px) { selector .ak-inv-note p, selector .ak-inv-priv p { min-height: 2.8em; } }')

# ============ revisión: pestaña "Voces" — la línea dorada cae sobre la línea gris
# El span era inline-block dentro del título y el interlineado dejaba un hueco debajo; con flex el borde dorado
# baja hasta la línea gris (margin-bottom -2px lo monta sobre los 2px grises).
css_add('6a12cc55', 'selector .ak-vtab .elementor-heading-title { display: flex; line-height: 1; margin: 0 !important; }\nselector .ak-vtab > .elementor-widget-container { margin-bottom: 0 !important; padding-bottom: 0 !important; }')

# vista previa: la base usa dos imágenes distintas llamadas "capitolio-10.webp" (2026/09 para Preguntas frecuentes y
# 2026/10 para Metodología); en la vista previa se pisaban y FAQ mostraba la de Metodología. El JSON ya apunta a la correcta.
PREVIEW_CSS += '.elementor-93083 .elementor-element.elementor-element-521f33e5:not(.elementor-motion-effects-element-type-background){background-image:url("a/capitolio-10-faq.webp")}'

# ============ TEXTOS APROBADOS (Figma actualizado por Diseño con el PDF "CONTENIDO LANDINGS (3)"), sin cambiar la estructura
# Hero y barra
heading(sub, 'Prepárate para dirigir la seguridad con visión, criterio y capacidad de respuesta')
heading('6ff8d16a', 'Hora')
heading('1c8584de', '30 de noviembre')
# Metodología
heading('60bb37d3', 'De gestionar la seguridad<br> a dirigirla estratégicamente')
text('2b35130a', '<p>Países en Latinoamérica</p>')
remove(row4)                                   # "100% Modalidad online en vivo": oculta en el Figma, no está en el PDF
# El programa, pestaña 1: la lista de 4 áreas no está en el PDF (oculta en el Figma)
text('1e2e258a', '<p>Formar directores capaces de diseñar, conducir y evaluar sistemas integrales de seguridad, identificando amenazas, priorizando riesgos y tomando decisiones alineadas con los objetivos de una organización.</p>'
                 '<p>Durante el diploma desarrollarás capacidades para dirigir equipos y recursos, proteger personas, instalaciones e información, gestionar crisis y sustentar decisiones ante la alta dirección mediante un Plan Director de Seguridad.</p>')
# Experiencia estratégica
heading('100b98eb', 'Aquí no solo<br> estudias seguridad.<br> <span class="ak-g">Aprendes a dirigirla.</span>')
text('5837a4c2', '<p>La metodología está conectada con el ejercicio profesional de la dirección de seguridad. Desde el primer módulo trabajarás sobre una organización o caso, desarrollando productos que se integrarán progresivamente en tu Plan Director de Seguridad.</p>')
# ("Analiza · Prioriza · Dirige · Protege" se quitó por pedido del usuario)
# Plan de estudios
heading('29610b73', 'Una formación para<br class="ak-dk"> dirigir la seguridad<br class="ak-dk"> de forma integral')
text(body_widgets(bodies[0])[0], '<p>Comprende cómo se organiza y dirige la función de seguridad dentro de una organización y su relación con la alta dirección.</p>')
# Certificación: 2 tarjetas; el botón queda en la 2.ª (Verificación digital) y lleva a un asesor
heading('2c9c857c', 'Una certificación para<br> <span class="ak-g">quienes dirigen<br> la seguridad</span>')
text('3f88c4d3', '<p>Al culminar satisfactoriamente el programa recibirás la certificación como Director de Seguridad. Una acreditación que reconoce tu formación para conducir sistemas integrales de seguridad, gestionar riesgos y coordinar capacidades de protección dentro de organizaciones públicas, privadas e institucionales.</p>')
heading('1b6533dd', 'Certificación internacional')
text('334be732', '<p>Diploma emitido por Grupo Goberna, que acredita la culminación satisfactoria del programa.</p>')
heading('4351992b', 'Verificación digital')
text('3f0fb31c', '<p>Credencial digital verificable que facilita la validación de tu certificación y su presentación profesional.</p>')
button('2b7efae9', 'Hablar con un asesor', 'https://wa.link/y4ww8t')
S('2b7efae9')['link']['is_external'] = 'on'
# Inversión
button('79c591de', 'Pagar ahora')
# subtítulo del hero en 2 líneas, con el ancho del título como en el Figma (676 px)
setv(sub, _element_width='initial', _element_custom_width={'unit': 'px', 'size': 676, 'sizes': []},
     _element_custom_width_laptop={'unit': 'px', 'size': 480, 'sizes': []}, _element_custom_width_mobile={'unit': '%', 'size': 100, 'sizes': []})
EXTRA_CSS.append(pre(sub) + '{--container-widget-width:676px;--container-widget-flex-grow:0;width:var(--container-widget-width,676px);max-width:676px}'
                 '@media(max-width:1366px){' + pre(sub) + '{--container-widget-width:480px;width:480px;max-width:480px}}'
                 '@media(max-width:932px){' + pre(sub) + '{--container-widget-width:100%;width:100%;max-width:100%}}')

# restos de otras landings en ajustes que no se ven (nombre del formulario, asunto del correo, título del iframe)
S('7d4e2b0')['form_name'] = 'Director de Seguridad — Habla con un asesor'
S('7d4e2b0')['email_subject'] = 'Nuevo contacto: Diploma Director de Seguridad'
S('68614c73')['html'] = S('68614c73')['html'].replace('title="Asesor Presidencial"', 'title="Director de Seguridad"')

# ============ revisión en el editor de Elementor
# Dentro del editor cada contenedor lleva antes de sus hijos un div de controles (overlay), así que :first-child
# y :nth-child no apuntan al primer elemento: se cambian por selectores entre hermanos que funcionan igual en el editor y en la página.
css_sub('592e977f', 'selector .ak-war-step:first-child::before', 'selector .ak-war-step:not(.ak-war-step ~ .ak-war-step)::before')
css_sub('5a9f071d', 'selector .ak-stat:first-child {', 'selector .ak-stat:not(.ak-stat ~ .ak-stat) {')
css_sub('f8ee414', 'selector .ak-mod-body > .e-con > .e-con:first-child {', 'selector .ak-mod-body > .e-con > .e-con:not(.e-con ~ .e-con) {')
css_sub('f8ee414', 'selector .ak-mod-body > .e-con > .e-con:last-child {', 'selector .ak-mod-body > .e-con > .e-con:not(:has(~ .e-con)) {')
css_sub('1626f0ea', 'selector .ak-bar-item:nth-child(2n) {', 'selector .ak-bar-item:nth-child(2n of .ak-bar-item) {')
# Header fijo: en el editor Elementor le fija el ancho que tenía con el panel lateral abierto
css_add('6081986', 'selector.elementor-sticky--active { width: 100% !important; left: 0 !important; right: 0 !important; }')


# ============ Docentes: base editada a mano por el usuario (Downloads/elementor-93673-2026-10-16.json)
# bios recortadas y nombre con 60 px de margen superior en las 7 tarjetas
DOC_BIOS = [
 "<p>Doctor en Criminología, con formación especializada en dirección y gestión de seguridad, ciberinteligencia, análisis y prevención del crimen.</p>",
 "<p>Analista de amenazas y delitos informáticos, con experiencia en evidencia digital e investigación del cibercrimen.</p>",
 "<p>Teniente Coronel (r) de Inteligencia del Ejército de Colombia, con más de 24 años liderando equipos en escenarios de alta complejidad.</p>",
 "<p>Asesor político y especialista en comunicación estratégica, con experiencia en operaciones de información y psicológicas en Latinoamérica.</p>",
 "<p>Consultor y docente en ciberseguridad con experiencia en implementación de soluciones de seguridad y proyectos tecnológicos.</p>",
 "<p>Profesional con más de 14 años de experiencia en investigación criminal, OSINT, SOCMINT, Virtual HUMINT y ciberpatrullaje.</p>",
 "<p>Máster en Criminología y MBA por ESADE. Presidente fundador y director de Operaciones de Grupo GEES Spain.</p>"
]
for mp, bio in zip(maps, DOC_BIOS):
    text(mp['e403aaf'], bio)
    margin(mp['360eb295'], top=60)
# en mobile los 60 px empujaban la bio debajo de "Ver trayectoria": ahí el nombre vuelve a 0
for mp in maps:
    margin(mp['360eb295'], '_mobile', top=0)
# tablet (768–1024): las flechas del carrusel salían por los costados y la página se movía hacia los lados
css_add('5b40c644', '@media (max-width: 1024px) { selector { overflow: hidden; } }')

# mobile: flechas del carrusel debajo de la tarjeta (tapaban el nombre)
css_add('5b40c644', open(os.path.join(W, 'doc_mobile.css'), encoding='utf-8').read())

# (Diego Miranda se quitó del carrusel; DOC_BIOS tiene 7 entradas y zip usa solo las 6 tarjetas)

# ============ Ponentes: última base del usuario (Downloads/elementor-93694-2026-10-16.json)
# sin bio; estilo de la tarjeta de Francisco López en todas; fotos nuevas de Francisco y Gonzalo
REUSE['retrato-profesional-traje-azul-marino.webp'] = 'https://grupogoberna.com/wp-content/uploads/2026/10/retrato-profesional-traje-azul-marino.webp'
REUSE['gonzalo-catanzariti.webp'] = 'https://grupogoberna.com/wp-content/uploads/2026/10/gonzalo-catanzariti.webp'
for mp, foto in zip(maps, ['retrato-profesional-traje-azul-marino.webp', 'gonzalo-catanzariti.webp']):
    cid = mp['6eb1afa2']; url, iid = wp(foto)
    S(cid)['background_image'] = {'url': url, 'id': iid, 'size': '', 'alt': '', 'source': 'library'}
    EXTRA_CSS.append(pre(cid) + ':not(.elementor-motion-effects-element-type-background){background-image:url("a/' + foto + '")}')
for mp in maps:
    remove(mp['e403aaf'])                                   # bio
    nm, es, bt = mp['360eb295'], mp['768d382a'], mp['1f339abe']
    typo(nm, size=21, size_mobile=16); margin(nm, top=125); margin(nm, '_mobile', top=0)
    color(es, '#FFFFFF9E'); typo(es, weight=200)
    S(bt)['button_text_color'] = '#FFFFFF'
css_add('5b40c644', open(os.path.join(W, 'doc_laptop.css'), encoding='utf-8').read())
css_add('5b40c644', open(os.path.join(W, 'doc_grad.css'), encoding='utf-8').read())

# ============ barra de datos: los costados se veían blancos (la sección no tenía fondo). La parte que se monta
# sobre el hero (margen negativo) queda transparente y el resto toma el gris de Metodología (#F3F5F7).
css_add('1626f0ea', '''selector { background: linear-gradient(to bottom, transparent 113px, #F3F5F7 113px); }
@media (max-width: 1366px) { selector { background: linear-gradient(to bottom, transparent 65px, #F3F5F7 65px); } }
@media (max-width: 1024px) { selector { background: linear-gradient(to bottom, transparent 64px, #F3F5F7 64px); } }
@media (max-width: 767px) { selector { background: linear-gradient(to bottom, transparent 30px, #F3F5F7 30px); } }''')
