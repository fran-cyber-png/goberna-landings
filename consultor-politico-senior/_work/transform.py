# Consultor Político Senior: aplica el Figma v2 (357:27) sobre la copia de la base Director de Seguridad (93575).
# Cada cambio se aplica a la vez al JSON y a la vista previa (HTML/CSS renderizado de la base).
import sys, os, re, json, copy, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import *
import random
random.seed(20261105)   # ids nuevos iguales en cada corrida (guía, sección 6)

RED, DARK, WHITE = '#DD0005', '#0C0000', '#FFFFFF'
NAME = 'Diploma Internacional de Consultor Político Senior'
WA = 'https://api.whatsapp.com/send/?phone=51986855496&text=Buen+d%C3%ADa+Goberna%2C+necesito+informaci%C3%B3n+de+Diploma+Internacional+Consultor+Pol%C3%ADtico+Senior.https%3A%2F%2Fgrupogoberna.com%2Fdiploma-internacional-consultor-politico-senior%2F&type=phone_number&app_absent=0'
CHECKOUT = 'https://grupogoberna.com/checkout/?add-to-cart=91119&quantity=1'
BROCHURE = 'https://grupogoberna.com/wp-content/uploads/2026/07/Brochure_ConsultorPolitico-Senior-1.pdf'
CV_ROBERTO = 'https://grupogoberna.com/roberto-bazan/'

# ================================================================ 1. paleta (dorado -> rojo, azul -> casi negro)
HEX = [('#FFBB03', RED), ('#15262F', DARK)]
RGB = [('255, 187, 3', '221, 0, 5'), ('255,187,3', '221,0,5'), ('21, 38, 47', '12, 0, 0'), ('21,38,47', '12,0,0')]
def recolor(s):
    for a, b in HEX: s = re.sub(re.escape(a), b, s, flags=re.I)
    for a, b in RGB: s = s.replace(a, b)
    return s
def recolor_json(o):
    if isinstance(o, dict): return {k: recolor_json(v) for k, v in o.items()}
    if isinstance(o, list): return [recolor_json(v) for v in o]
    if isinstance(o, str): return recolor(o)
    return o
lib.J['content'] = recolor_json(lib.J['content']); reindex()
lib.CSS = recolor(lib.CSS)
# en el HTML no se tocan los SVG en línea: son el contenido de los archivos de la Biblioteca de medios (se cambian por archivo, ver icon_svg)
_parts = re.split(r'(<svg\b.*?</svg>)', lib.HTML, flags=re.S)
lib.HTML = ''.join(p if p.startswith('<svg') else recolor(p) for p in _parts)

def icon_svg(i, fname):
    """Ícono SVG de la Biblioteca: JSON (url del archivo nuevo) + SVG en línea de la vista previa."""
    url, iid = wp(fname)
    S(i)['selected_icon'] = {'value': {'url': url, 'id': iid}, 'library': 'svg'}
    svg = open(os.path.join(ROOT, 'iconos', fname), encoding='utf-8').read()
    svg = re.sub(r'<\?xml[^>]*>\s*', '', svg)
    def f(blk):
        r, n = re.subn(r'<svg\b.*?</svg>', lambda m: svg, blk, count=1, flags=re.S)
        assert n, i; return r
    html_sub_in(i, f)

def css_replace(i, old, new):
    """CSS personalizado: cambia el texto en el JSON y añade la regla nueva a la vista previa (va después y gana)."""
    s = S(i); cc = s.get('custom_css', '')
    assert old in cc, (i, old[:60])
    s['custom_css'] = cc.replace(old, new, 1)
    # se repite el bloque completo para conservar el orden de sus media queries
    EXTRA_CUSTOM.append(s['custom_css'].replace('selector', pre(i)))

def _emit(i, kw, mapping, tail=''):
    """CSS de la vista previa para kw y, como las reglas nuevas van al final, se repiten los valores de
    tablet/mobile que ya tenía el elemento para que la regla de desktop/laptop no los pise."""
    s = S(i); full = dict(kw)
    bases = {k.replace('_laptop', '') for k in kw if not k.endswith(('_tablet', '_mobile'))}
    for b in bases:
        for d in ('_tablet', '_mobile'):
            if b + d in s and b + d not in kw: full[b + d] = s[b + d]
    rules = lib._dev_rules(i, full, mapping)
    for d in DEV:
        if rules[d]:
            rule = f'{pre(i)}{tail}{{{";".join(rules[d])}}}'
            EXTRA_CSS.append(f'@media{DEV[d]}{{{rule}}}' if DEV[d] else rule)

def cset(i, **kw):
    """Ajustes de contenedor (JSON) + su CSS equivalente en la vista previa."""
    S(i).update(kw); _emit(i, kw, lib.CON_MAP)

def wmargin(i, **kw):
    """_margin de widget (JSON) + CSS."""
    S(i).update(kw); _emit(i, kw, lib.WID_MAP, ' > .elementor-widget-container')

def wwidth(i, desk, lap=None):
    """Ancho personalizado de widget (px) en desktop y laptop."""
    S(i)['_element_width'] = 'initial'; S(i)['_element_custom_width'] = px(desk)
    EXTRA_CSS.append(f'{pre(i)}{{--container-widget-width:{desk}px;--container-widget-flex-grow:0;width:var(--container-widget-width,{desk}px);max-width:{desk}px}}')
    if lap is not None:
        S(i)['_element_custom_width_laptop'] = px(lap)
        EXTRA_CSS.append(f'@media(max-width:1366px){{{pre(i)}{{--container-widget-width:{lap}px;width:var(--container-widget-width,{lap}px);max-width:{lap}px}}}}')
    for d in ('_tablet', '_mobile'):
        v = S(i).get('_element_custom_width' + d)
        if v: EXTRA_CSS.append(f'@media{DEV[d]}{{{pre(i)}{{--container-widget-width:{v["size"]}{v["unit"]};width:var(--container-widget-width,{v["size"]}{v["unit"]});max-width:{v["size"]}{v["unit"]}}}}}')

L = lambda v: round(v * 1366 / 1920, 1)    # desktop -> laptop (el laptop es el Figma escalado)

# botones y textos que estaban en azul sobre dorado: ahora blanco sobre rojo (como el Figma)
def white_on_red(*ids):
    for i in ids: color(i, WHITE)
for i, e in list(ELEM.items()):
    s = e['settings']
    if e.get('widgetType') == 'button' and s.get('background_color', '').upper() == RED and s.get('button_text_color', '').upper() == DARK:
        white_on_red(i)
        if s.get('hover_color', '').upper() in (DARK, '#FFFFFF', '#F3F5F7'): s['hover_color'] = WHITE
        if s.get('button_background_hover_color', '').upper() == RED: s['button_background_hover_color'] = '#B80004'
        EXTRA_CSS.append(f'{pre(i)} .elementor-button:hover, {pre(i)} .elementor-button:focus{{color:{WHITE};background-color:#B80004}}')

# ================================================================ 0. header (no se toca salvo la paleta)
# ================================================================ 2. hero
heading('17c98689', NAME)
image('1916fb3', 'titulo-consultor-senior.webp')
remove('6b6388d')                                   # el Figma no lleva subtítulo bajo el título
button('9c2fe2d', url=WA)
button('263d369c', url=BROCHURE)
bg_image('2742d6b5', 'hero-fondo-consultor-senior.webp')

# ================================================================ 3. barra de datos
heading('6919d0e7', '21 de octubre')
heading('4209211c', '11 módulos')
heading('4c8ed0ee', 'US$ 1000')
white_on_red('12c0a15', '4c8ed0ee')

# ================================================================ 4. metodología
heading('b86c8ae', 'Formamos estrategas que<br> <span class="ak-g">transforman la política.</span>')
text('390db8e4', '<p>De consultor político a director de una firma con proyección internacional.</p>')
image('40d9161c', 'metodologia-video-consultor-senior.webp')
text('4510a4fd', '<p>Inteligencia <span>•</span> Estrategia <span>•</span> Liderazgo <span>•</span> Crisis <span>•</span> Tecnología</p>')

# ================================================================ 5. el programa
heading('80fac6b', 'El programa')
heading('37799678', 'Formar consultores senior<br class="ak-dk"> capaces de fundar, <span class="ak-g">dirigir y<br class="ak-dk"> proyectar su propia firma de<br class="ak-dk"> consultoría</span>')
text('1e2e258a', '<p>Formar consultores políticos de nivel senior capaces de <strong>fundar, dirigir y proyectar internacionalmente su propia firma de consultoría como una empresa estructurada, rentable y tecnológicamente automatizada.</strong></p>'
                 '<p>Durante el programa transformarás tu experiencia en un modelo empresarial con posicionamiento, servicios, estructura operativa, sistema comercial y herramientas para escalar una consultora política.</p>')
text('2d2f5c00', '<p>Dirigido a:</p><ul>'
                 '<li>Egresados del Diploma Internacional del Consultor Político.</li>'
                 '<li>Consultores políticos certificados en la metodología War Room de Goberna.</li>'
                 '<li>Jefes de campaña, estrategas y asesores políticos en ejercicio.</li>'
                 '<li>Profesionales que trabajan en campañas electorales, gobiernos o espacios parlamentarios.</li>'
                 '<li>Consultores que buscan convertir su experiencia en una firma profesional de consultoría.</li></ul>')
text('73081eaa', '<p>Al finalizar el diploma estarás preparado para dirigir una firma de consultoría política como una empresa profesional, rentable y con capacidad de expansión internacional.</p>'
                 '<p>Podrás desenvolverte como:</p>'
                 '<p>Director de consultoría política · Fundador de firma consultora · Director de campañas · Estratega senior · Consultor internacional</p>')

# ================================================================ 6. experiencia estratégica
heading('a50a77b', 'Aquí no solo aprendes<br> consultoría. <span class="ak-g">Construyes<br> una firma</span>')
text('3079ff74', '<p>La metodología está orientada a la creación real de una consultora política. Cada módulo genera un componente concreto de tu firma y las entregas se convierten en activos acumulables para la sustentación final.</p>')
for (t_id, x_id), (t, x) in zip([('7a82957e', '71560803'), ('245ad6bc', '746d9382'), ('544064c5', '6d95755b'), ('1f78edf1', '5f510898')], [
        ('Define tu modelo', 'Construye el posicionamiento, nicho y propuesta de valor de tu consultora.'),
        ('Diseña tu estructura', 'Desarrolla servicios, procesos, equipos y herramientas para operar profesionalmente.'),
        ('Construye tu mercado', 'Crea sistemas comerciales para captar clientes y generar nuevas oportunidades.'),
        ('Proyecta tu firma', 'Presenta tu consultora ante un jurado internacional y desarrolla una visión de crecimiento.')]):
    heading(t_id, t); text(x_id, f'<p>{x}</p>')
    typo(t_id, family='Montserrat', weight=700)       # el Figma usa Montserrat Bold (la base, Barlow)
bg_image('3028d48c', 'war-room-fondo-consultor-senior.webp')
# en mobile solo el color de fondo: se quita la foto de la base y se anula la herencia de la de desktop
S('3028d48c').pop('background_image_mobile', None)
css_add('3028d48c', '@media (max-width: 767px) { selector:not(.elementor-motion-effects-element-type-background) { background-image: none !important; } }')

# ================================================================ 6b. Proyecto final (sección nueva, Figma 373:597)
PF_CSS = '''selector { position: relative; overflow: hidden; }
selector::before { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(12,0,0,0) 0%, #0C0000 100%); pointer-events: none; }
selector > .e-con-inner { position: relative; z-index: 1; }
selector .elementor-heading-title { white-space: nowrap; }
selector .elementor-widget-text-editor p { margin: 0; }
@media (max-width: 767px) {
  selector { background-size: auto 230px !important; background-position: left top !important; }
  selector::before { background: linear-gradient(180deg, rgba(12,0,0,0) 96px, #0C0000 226px); }
  selector .elementor-heading-title { white-space: normal; text-wrap: balance; }
}'''
url_pf, id_pf = wp('proyecto-final-fondo-consultor-senior.webp')
pf_k = w_heading('PROYECTO FINAL', 'div', RED, family='Montserrat', weight=700, size=27, lh=37, size_laptop=19.2, lh_laptop=26.3, size_mobile=18, lh_mobile=24)
pf_h = w_heading('Sustentación de tu firma de consultoría política', 'h3', WHITE, family='Montserrat', weight=700, size=27, lh=37, size_laptop=19.2, lh_laptop=26.3, size_mobile=18, lh_mobile=24)
pf_p = w_text('<p>Presenta la estructura completa de tu consultora: posicionamiento, servicios, modelo comercial, operación, estrategia de crecimiento y proyección internacional.</p>',
              'rgba(255,255,255,0.75)', family='Inter', weight=400, size=18, lh=32, ls=0.18, size_laptop=12.8, lh_laptop=22.8, ls_laptop=0.128, size_mobile=13, lh_mobile=22, ls_mobile=0.13)
pf_p['node']['settings']['_margin_mobile'] = box(8, 0, 0, 0); pf_p['css'].append(f'@media(max-width:932px){{{pre(pf_p["id"])} > .elementor-widget-container{{margin:8px 0 0 0}}}}')
pf_txt = container({'flex_direction': 'column', 'flex_gap': gap(5), 'flex_gap_laptop': gap(3.6), 'flex_gap_mobile': gap(4),
                    'width': px(675), 'width_laptop': px(480), 'width_mobile': {'unit': '%', 'size': 100, 'sizes': []},
                    'padding': box(0, 0, 0, 0)}, [pf_k, pf_h, pf_p], cls='ak-pf-txt')
pf = container({'content_width': 'boxed', 'boxed_width': px(1520), 'flex_direction': 'column', 'flex_justify_content': 'center', 'flex_align_items': 'flex-end',
                'flex_align_items_mobile': 'stretch', 'flex_gap': gap(0),
                'min_height': px(340), 'min_height_laptop': px(242), 'min_height_mobile': px(0),
                'padding': box(0, 40, 0, 40), 'padding_laptop': box(0, 142, 0, 142), 'padding_tablet': box(0, 32, 0, 32), 'padding_mobile': box(196, 16, 48, 16),
                'background_background': 'classic', 'background_color': DARK,
                'background_image': {'url': url_pf, 'id': id_pf, 'size': '', 'alt': '', 'source': 'library'}, '_local_bg': 'proyecto-final-fondo-consultor-senior.webp',
                'background_position': 'center 83%', 'background_repeat': 'no-repeat', 'background_size': 'cover',
                'custom_css': PF_CSS}, [pf_txt], parent=True, cls='ak-pf')
insert_after('3028d48c', pf); EXTRA_CUSTOM.extend(pf['css'])

# ================================================================ 7. plan de estudios (11 módulos)
heading('48da84d4', 'Una ruta para<br class="ak-dk"> construir y dirigir<br class="ak-dk"> tu propia firma')
heading('5d85f006', '11')
button('3954484a', url=BROCHURE)
MODS = [
 ('Fundamentos de la firma: identidad, nicho y diferenciación', 'Define qué consultora quieres construir, a quién atenderás y cómo te diferenciarás dentro del mercado.',
  'Nicho, propuesta de valor, posicionamiento, identidad, diferenciación y criterios éticos de la firma.', 'Definición del posicionamiento, propuesta de valor y código institucional de tu consultora.'),
 ('Constitución legal, marca y propiedad intelectual', 'Convierte tu consultora en una empresa formal y protege los activos que sostienen su crecimiento.',
  'Constitución legal, régimen tributario, marca, presencia institucional y propiedad intelectual.', 'Estructura legal de la consultora y protección de marca, metodologías y activos intangibles.'),
 ('Productización de la oferta: catálogo y líneas de servicio', 'Transforma tu conocimiento en servicios claros, vendibles y capaces de escalar.',
  'Diseño de líneas de servicio, niveles, alcance, precios de referencia y productización.', 'Construcción de un catálogo de servicios con productos definidos y replicables.'),
 ('Precios, cotización y economía de la firma', 'Aprende a cobrar con criterio y a construir una consultora financieramente sostenible.',
  'Honorarios, cotizaciones, márgenes, flujo de caja, rentabilidad y reinversión.', 'Modelo de precios y estructura financiera para proteger la rentabilidad de cada servicio.'),
 ('Oficina y equipo: War Room operativo', 'Construye la estructura desde donde tu firma ejecutará proyectos y coordinará múltiples clientes.',
  'War Room, estructura de equipos, roles, confidencialidad y gestión simultánea de proyectos.', 'Diseño de la estructura operativa, equipos y protocolos internos de trabajo.'),
 ('Infraestructura tecnológica e IA', 'Integra tecnología e inteligencia artificial para aumentar la capacidad y escalabilidad de tu consultora.',
  'Automatización, IA, monitoreo, OSINT, producción de contenido y herramientas para War Room.', 'Definición de un stack tecnológico y desarrollo de una línea de servicio potenciada con IA.'),
 ('Motor comercial y cierre de contratos', 'Construye un sistema para captar oportunidades, presentar propuestas y convertirlas en clientes.',
  'Prospección, generación de demanda, adquisición de clientes, negociación y cierre.', 'Creación de una propuesta técnica, contrato tipo y proceso comercial replicable.'),
 ('Gestión de la entrega y del cliente', 'Aprende a dirigir la relación con el cliente sin convertirte nuevamente en el operador de cada tarea.',
  'Entrega del servicio, estándares de calidad, coordinación, gestión de crisis y cierre de relaciones.', 'Protocolo de entrega y política de gestión del cliente para proteger calidad, reputación y rentabilidad.'),
 ('Reputación, ética y blindaje de la firma', 'Protege la reputación y reduce los riesgos legales que pueden comprometer años de trabajo.',
  'Ética, límites legales, confidencialidad, contratos, riesgos reputacionales y manejo de crisis.', 'Protocolo de riesgo, ética y blindaje contractual para fortalecer la protección institucional.'),
 ('Desarrollo de negocio y relacionamiento institucional', 'Convierte reputación, relaciones y posicionamiento en nuevas oportunidades para la consultora.',
  'Networking estratégico, relaciones institucionales, referidos y construcción de redes de negocio.', 'Mapa de relacionamiento institucional y plan de referidos para generar crecimiento sostenido.'),
 ('Alianzas y expansión internacional', 'Diseña la ruta para llevar tu consultora más allá de su mercado de origen.',
  'Alianzas transfronterizas, coinversión, rondas de negocio y operación regional.', 'Estrategia de expansión y propuesta de alianza internacional para abrir nuevos mercados.'),
]
ACC = '5b410621'
def clone_item(src_cid, idx):
    """Duplica el ítem src_cid del acordeón (JSON con ids nuevos + <details> del HTML)."""
    src = ELEM[src_cid]; new = copy.deepcopy(src); idmap = {}
    def renum(e):
        old = e['id']; e['id'] = nid(); idmap[old] = e['id']
        for c in e.get('elements', []): renum(c)
    renum(new)
    ELEM[ACC]['elements'].append(new)
    h = lib.HTML; i, j = lib.el_span(h, ACC)
    dets = [m for m in re.finditer(r'<details id="(e-n-accordion-item-\d+)"', h[i:j])]
    last = dets[-1]; s = i + last.start(); e = h.find('</details>', s) + len('</details>')
    blk = h[s:e]
    old_item = last.group(1); new_item = 'e-n-accordion-item-%d' % (9000 + idx)
    blk = blk.replace(old_item, new_item).replace(' open=""', '')
    blk = re.sub(r'data-accordion-index="\d+"', f'data-accordion-index="{idx}"', blk).replace('aria-expanded="true"', 'aria-expanded="false"')
    for o, n in idmap.items(): blk = blk.replace(f'elementor-element-{o} ', f'elementor-element-{n} ').replace(f'data-id="{o}"', f'data-id="{n}"')
    lib.HTML = h[:e] + blk + h[e:]
    # CSS de la vista previa: copiar las reglas generadas de cada elemento clonado
    # solo las reglas de cada elemento clonado, cada una dentro de su misma media query
    blocks = re.findall(r'(@media[^{]+)\{((?:[^{}]*\{[^{}]*\})*)\s*\}|([^{}@]+\{[^{}]*\})', lib.CSS)
    for o, n in idmap.items():
        pat = re.compile(r'elementor-element-%s(?![0-9a-f])' % o)
        for media, inner, plain in blocks:
            if plain:
                if pat.search(plain.split('{')[0]): EXTRA_CSS.append(pat.sub('elementor-element-' + n, plain.strip()))
            else:
                mine = [r.strip() for r in re.findall(r'[^{}]+\{[^{}]*\}', inner) if pat.search(r.split('{')[0])]
                if mine: EXTRA_CSS.append(media.strip() + '{' + pat.sub('elementor-element-' + n, ' '.join(mine)) + '}')
    reindex()
    return new['id']
items = S(ACC)['items']
while len(ELEM[ACC]['elements']) < len(MODS):
    cid = clone_item(ELEM[ACC]['elements'][-1]['id'], len(ELEM[ACC]['elements']) + 1)
    items.append({'_id': nid()[:7], 'item_title': ''})
def item_title(k, t):
    items[k]['item_title'] = t
    h = lib.HTML; i = h.find('data-id="%s"' % ACC)
    ms = list(re.finditer(r'(<div class="e-n-accordion-item-title-text">)(.*?)(</div>)', h[i:], re.S))
    m = ms[k]; s = i + m.start(2); e = i + m.end(2)
    lib.HTML = h[:s] + ' ' + t + ' ' + h[e:]
for k, (t, d, a1, a2) in enumerate(MODS):
    item_title(k, t)
    body = ELEM[ACC]['elements'][k]
    txts = []
    def walk(e):
        if e.get('widgetType') == 'text-editor': txts.append(e['id'])
        for c in e.get('elements', []): walk(c)
    walk(body)
    assert len(txts) == 3, (k, txts)
    text(txts[0], f'<p>{d}</p>'); text(txts[1], f'<p>{a1}</p>'); text(txts[2], f'<p>{a2}</p>')

# ================================================================ 8. CTA próxima edición
text('1251cd12', '<p>Inicio: 21 de octubre | Online en vivo | 11 Módulos</p>')
button('16c985f5', url=WA)
bg_image('4d64e131', 'banner-proxima-edicion-consultor-senior.webp')

# ================================================================ 9. ponente (sección nueva: un solo docente, Figma 357:45)
DOC_CSS = '''selector { position: relative; overflow: hidden; }
selector .ak-ponente-title .elementor-heading-title .ak-g { color: #DD0005; }
selector .ak-ponente-foto img { display: block; width: 100%; height: auto; }
selector .ak-ponente-btn .elementor-button { width: 266px; height: 56px; display: inline-flex; align-items: center; justify-content: space-between; padding: 0 32px; border: 1px solid #F5F7FA; border-radius: 32px; }
selector .ak-ponente-btn .elementor-button-content-wrapper { width: 100%; justify-content: space-between; }
selector .ak-ponente-btn .elementor-button:hover { background: #F5F7FA; color: #0C0000; }
selector .elementor-widget-text-editor p { margin: 0; }
@media (max-width: 1366px) { selector .ak-ponente-btn .elementor-button { width: 190px; height: 40px; padding: 0 23px; } }
@media (max-width: 767px) {
  selector .ak-ponente-title br { display: none; }
  selector .ak-ponente-row { flex-direction: column !important; align-items: center !important; }
  selector .ak-ponente-txt { align-items: center !important; text-align: center; }
  selector .ak-ponente-foto { margin: 0 0 -4px !important; }
  selector .ak-ponente-foto > .elementor-widget-container { margin: 0 !important; }
  selector .ak-ponente-btn { align-self: center !important; }
  selector .ak-ponente-btn .elementor-button { width: 200px; height: 44px; padding: 0 24px; }
}'''
url_doc, id_doc = wp('fondo-docente-consultor-senior.webp')
d_title = w_heading('Aprende de un especialista en<br> <span class="ak-g">consultoría y estrategia política</span>', 'h2', WHITE, cls='ak-ponente-title',
                    family='Montserrat', weight=700, size=56, lh=56, size_laptop=39.8, lh_laptop=39.8, size_mobile=26, lh_mobile=30)
d_title['node']['settings']['align'] = 'center'; d_title['css'].append(f'{pre(d_title["id"])}{{text-align:center}}')
d_name = w_heading('Roberto Bazán', 'h3', '#F5F7FA', family='Montserrat', weight=700, size=72, lh=1.22, lh_unit='em', size_laptop=51.2, size_mobile=36)
d_role = w_heading('Estratega político senior y especialista en inteligencia aplicada a la consultoría política', 'div', 'rgba(255,255,255,0.75)',
                   family='Montserrat', weight=500, size=22, lh=1.22, lh_unit='em', size_laptop=15.6, size_mobile=15)
d_bio = w_text('<p>Magíster en Inteligencia Estratégica, abogado y politólogo. Estratega político con experiencia en América Latina, asesorando gobiernos y líderes. Especialista en inteligencia y PSYOPS en campañas electorales.</p>',
               '#F2F4F8', family='Inter', weight=400, size=20, lh=32, ls=0.2, size_laptop=14.2, lh_laptop=22.8, ls_laptop=0.14, size_mobile=14, lh_mobile=22, ls_mobile=0.14)
d_btn = w_button('Saber más', CV_ROBERTO, cls='ak-ponente-btn', button_text_color='#F5F7FA', background_color='#FFFFFF00', hover_color=DARK,
                 button_background_hover_color='#F5F7FA', icon_indent=px(14),
                 typography_typography='custom', typography_font_family='Inter', typography_font_weight='400', typography_font_size=px(18),
                 typography_font_size_laptop=px(12.8), typography_font_size_mobile=px(13))
d_btn['css'] += [f'{pre(d_btn["id"])} .elementor-button{{background-color:transparent;color:#F5F7FA;font-family:"Inter", Sans-serif;font-size:18px;font-weight:400;line-height:1}}',
                 f'@media(max-width:1366px){{{pre(d_btn["id"])} .elementor-button{{font-size:12.8px}}}}', f'@media(max-width:932px){{{pre(d_btn["id"])} .elementor-button{{font-size:13px}}}}']
d_head = container({'flex_direction': 'column', 'flex_gap': gap(10), 'flex_gap_laptop': gap(7), 'flex_gap_mobile': gap(6), 'padding': box(0, 0, 0, 0), 'width': {'unit': '%', 'size': 100, 'sizes': []}}, [d_name, d_role])
# línea roja bajo el cargo (Figma 394:31: 554 x 1 px, #DD0005), widget Divisor nativo
d_line = lib._widget('divider', {'color': RED, 'weight': px(1), 'width': px(554), 'width_laptop': px(394), 'width_mobile': {'unit': '%', 'size': 100, 'sizes': []},
                                 'gap': px(0), 'align_mobile': 'center'},
                     '<div class="elementor-divider"><span class="elementor-divider-separator"></span></div>', 'ak-ponente-linea')
_L = pre(d_line['id'])
d_line['css'] += [f'{_L}{{--divider-border-style:solid;--divider-color:{RED};--divider-border-width:1px;width:100%}}',
                  f'{_L} .elementor-divider-separator{{width:554px;margin:0}}', f'{_L} .elementor-divider{{padding-block-start:0;padding-block-end:0;display:flex}}',
                  f'@media(max-width:1366px){{{_L} .elementor-divider-separator{{width:394px}}}}',
                  f'@media(max-width:932px){{{_L} .elementor-divider-separator{{width:100%}}}}']
d_headgrp = container({'flex_direction': 'column', 'flex_gap': gap(40), 'flex_gap_laptop': gap(28), 'flex_gap_mobile': gap(20), 'padding': box(0, 0, 0, 0),
                       'width': {'unit': '%', 'size': 100, 'sizes': []}}, [d_head, d_line])
d_body = container({'flex_direction': 'column', 'flex_gap': gap(37), 'flex_gap_laptop': gap(26), 'flex_gap_mobile': gap(22), 'flex_align_items': 'flex-start',
                    'padding': box(0, 0, 0, 0), 'width': {'unit': '%', 'size': 100, 'sizes': []}}, [d_bio, d_btn])
d_txt = container({'flex_direction': 'column', 'flex_gap': gap(50), 'flex_gap_laptop': gap(36), 'flex_gap_mobile': gap(24), 'flex_align_items': 'flex-start',
                   'width': px(571), 'width_laptop': px(406), 'width_mobile': {'unit': '%', 'size': 100, 'sizes': []},
                   'padding': box(0, 0, 0, 0), 'margin': box(126, 0, 0, 128), 'margin_laptop': box(90, 0, 0, 91), 'margin_mobile': box(0, 0, 40, 0)},
                  [d_headgrp, d_body], cls='ak-ponente-txt')
d_foto = w_image('docente-roberto-bazan-v2-consultor-senior.webp', cls='ak-ponente-foto',
                 _margin=box(0, 0, -4, 0), _margin_laptop=box(0, 0, -3, 0), _element_width='initial',
                 _element_custom_width=px(583), _element_custom_width_laptop=px(415), _element_custom_width_mobile={'unit': '%', 'size': 86, 'sizes': []})
d_foto['css'] += [f'{pre(d_foto["id"])}{{width:583px;max-width:583px}}', f'@media(max-width:1366px){{{pre(d_foto["id"])}{{width:415px}}}}',
                  f'@media(max-width:932px){{{pre(d_foto["id"])}{{width:86%}}}}']
d_row = container({'flex_direction': 'row', 'flex_wrap': 'nowrap', 'flex_align_items': 'flex-start', 'flex_gap': gap(66), 'flex_gap_laptop': gap(47), 'flex_gap_mobile': gap(0), 'padding': box(0, 0, 0, 0),
                   'margin': box(49, 0, 0, 0), 'margin_laptop': box(35, 0, 0, 0), 'margin_mobile': box(28, 0, 0, 0),
                   'width': {'unit': '%', 'size': 100, 'sizes': []}}, [d_txt, d_foto], cls='ak-ponente-row')
doc = container({'content_width': 'boxed', 'boxed_width': px(1520), 'flex_direction': 'column', 'flex_gap': gap(0),
                 'padding': box(151, 40, 0, 40), 'padding_laptop': box(107, 142, 0, 142), 'padding_tablet': box(80, 32, 0, 32), 'padding_mobile': box(56, 16, 0, 16),
                 'background_background': 'classic', 'background_color': '#090909',
                 'background_image': {'url': url_doc, 'id': id_doc, 'size': '', 'alt': '', 'source': 'library'}, '_local_bg': 'fondo-docente-consultor-senior.webp',
                 'background_position': 'top center', 'background_repeat': 'no-repeat', 'background_size': 'cover',
                 'border_border': 'solid', 'border_width': box(0, 0, 4, 0), 'border_color': RED,
                 '_element_id': 'docentes', 'custom_css': DOC_CSS}, [d_title, d_row], parent=True, cls='ak-ponente')
replace_section('613c44c5', doc); EXTRA_CUSTOM.extend(doc['css'])

# ================================================================ 10. presencia internacional
bg_image('63b5ee4a', 'fondo-presencia-consultor-senior.webp')

# ================================================================ 11. certificación
heading('2c9c857c', 'Una certificación para<br> quienes <span class="ak-g">lideran la<br> consultoría política</span>')
text('3f88c4d3', '<p>Al culminar satisfactoriamente el programa recibirás la certificación como Director de Consultoría Política. Una acreditación que reconoce tu capacidad para dirigir una firma profesional de consultoría política, gestionar clientes, estructurar servicios y desarrollar operaciones estratégicas a nivel internacional.</p>')
text('334be732', '<p>Diploma emitido por Grupo Goberna, que acredita la culminación del programa y tus competencias.</p>')
text('3f0fb31c', '<p>Credencial digital verificable que facilita la validación de tu certificación y su presentación en tu perfil profesional.</p>')
bg_image('28c43ad5', 'certificado-consultor-senior.webp')
button('2b7efae9', url=WA)

# ================================================================ 12. inversión y admisión
heading('2d4237ac', 'Conviértete en el director<br> de tu propia firma de<br> consultoría política')
heading('60f25b0f', '<span class="ak-cur">$</span>1000<span class="ak-usd">USD</span>')
heading('9030ca2', '21 de octubre')
heading('73517676', '11 MÓDULOS')
button('79c591de', url=CHECKOUT)
heading('dc295fa', '¿Listo para dar<br> el siguiente paso?')
f = S('7d4e2b0')
f['form_name'] = 'Consultor Político Senior — Habla con un asesor'
f['email_subject'] = 'Nuevo contacto: Diploma Internacional de Consultor Político Senior'
for fld in f['form_fields']:
    if fld.get('custom_id') == 'cargo': fld['placeholder'] = 'Ej. Consultor político'
lib.HTML = lib.HTML.replace('placeholder="Ej. Jefe de seguridad"', 'placeholder="Ej. Consultor político"')

# ================================================================ 13. Experiencia Goberna: no está en el Figma v2
remove('6a12cc55')

# ================================================================ 14. preguntas frecuentes
FAQ = ['Las sesiones se desarrollan 100% online y en vivo vía Zoom, combinando clases magistrales, análisis de casos reales, talleres de producción y desarrollo de componentes concretos para la firma.',
       'El diploma tiene una duración de 11 módulos y 200 horas académicas, desarrollados según el cronograma establecido del programa.',
       'Tu inscripción incluye acceso al programa, materiales académicos, talleres aplicados, desarrollo progresivo de activos para tu consultora, acompañamiento durante el proceso formativo y la certificación correspondiente.',
       'GOBERNA cuenta con diferentes alternativas de pago para sus participantes. Al iniciar tu proceso de inscripción, un asesor te indicará las opciones habilitadas según tu país.',
       'Completa tus datos en el formulario y un asesor de GOBERNA se pondrá en contacto contigo para orientarte y ayudarte a completar tu inscripción.']
for i, t in zip(['ea24eba', '77b34c1f', '3a6adec1', '584613f6', '38271e76'], FAQ): text(i, f'<p>{t}</p>')
setv('521f33e5', background_color='#F2F4F7'); EXTRA_CSS.append(f'{pre("521f33e5")}:not(.elementor-motion-effects-element-type-background){{background-color:#F2F4F7}}')

# ================================================================ AJUSTES AL FIGMA v2 (medidos en Playwright; laptop = desktop × 0,7115)
# hero: título a 145 px del header y alto total 879 (la barra se monta 113 px)
cset('2742d6b5', padding=box(145, 40, 255, 40))
# barra: ícono abajo a 60 px, etiqueta a 70 y valor a 99 (caja de 180)
for it in ('4e571a4a', '1e9c4dab', '21c26060', '452ae72f'):
    cset(it, padding=box(28, 26, 49, 26), padding_laptop=box(20, 24, 35, 24))
for lb in ('7094f679', '38e6f601', '78e96140', '6f2e556d'):
    wmargin(lb, _margin=box(10, 0, 0, 0), _margin_laptop=box(7, 0, 0, 0))
for vl in ('5d6fff46', '6919d0e7', '2fda4138', '4209211c'):
    wmargin(vl, _margin=box(0, 0, 0, 0), _margin_laptop=box(0, 0, 0, 0))

# metodología
cset('3f83c2c', padding=box(63, 40, 114, 40), padding_laptop=box(45, 80, 81, 80))
cset('161b8b64', width={'unit': '%', 'size': 46.5, 'sizes': []}, width_laptop={'unit': '%', 'size': 46.5, 'sizes': []})
cset('74f3d431', width={'unit': '%', 'size': 51.5, 'sizes': []}, width_laptop={'unit': '%', 'size': 51.5, 'sizes': []},
     padding=box(129, 0, 0, 0), padding_laptop=box(92, 0, 0, 0))
wwidth('390db8e4', 687, L(687)); wmargin('390db8e4', _margin=box(21, 0, 0, 0), _margin_laptop=box(15, 0, 0, 0))
cset('4728f10c', margin=box(30, 0, 0, 0), margin_laptop=box(21, 0, 0, 0))
typo('4510a4fd', size=18, size_laptop=12.8, lh=1.83, lh_unit='em')
wmargin('4510a4fd', _margin=box(18, 0, 0, 0), _margin_laptop=box(13, 0, 0, 0))

# el programa
wmargin('37799678', _margin=box(44, 0, 0, 0), _margin_laptop=box(31, 0, 0, 0))
css_replace('56bf8b99', 'padding: 346px 79px 100px 40px;', 'padding: 370px 148px 77px 40px;')
# panel oscuro de 872 px como el Figma (la base tenía 853) y título/pestañas desde x = 200
css_replace('56bf8b99', 'grid-template-columns: 45.4% 54.6%;', 'grid-template-columns: 46.4% 53.6%;')
css_replace('56bf8b99', 'padding: 101px 40px 80px 154px;', 'padding: 101px 40px 80px 131px;')
css_replace('56bf8b99', 'left: calc(45.4% - 602px); width: 562px !important;', 'left: calc(46.4% - 672px); width: 581px !important;')
css_replace('56bf8b99', 'url(data:image/webp;base64,UklGRmABAABXRUJQVlA4TFMBAAAvNUANECeioG0jx8ef0xG734PD/BtI2yb771/yxyCSpEa14N8fLjJ83Jt1yKeJhiYIgnADgB8AgBfgAfgAALhgBAJc+HEj8MGoGDA2/ruAcaGgIQD8BQHuW6QXgINc/gEE23bTRoWZMnOHmTnDTNr/mkKy9LKBiP47cNvGkWhor/d7heT3cdCrUWvt3uX9nzdq4DbyPtdq6BTLYpSOiyFfR9PhyLfxoGEh5bfnF9den/brGm6/Z51aAX5OmjUNmgpvNsmgW17vZNDdV7Yz6GQ1iy4PTsGmQVOR6cACqCIJwc4HUYVBGTBZIJkQgf7UjPxZOYvEzHvezpmD71YP13kXTz6OW52MLeK8zLlZ8zMGsD0bwRTo51j7fzhV9zLoRC5TIzz5Oux3t66Cf19iK48378FXpVZc36faq5Iu2sojUAMlVjsfbDe1/iC0aLNWm98KTQAA)', 'url(data:image/webp;base64,UklGRkgBAABXRUJQVlA4TDsBAAAvNUANEBciEEjy136I6TaQtm0o234FbRu5wU/7ez+LXwcEHwCBoAEAkFABQAHIAAAYQLj4aHAhRAwYGw9GglAR94MgeMWCrQAAxEaSFEl9+Mx/z8zMzD/+O7XU05XrQET/HbiNpEhuZfEY/2DNmTr6SNT8nK40dbb/EjhXTZM3CR3HbTs6++2wiYPH1xdtnt/+Iqw7Mz8nzezC8b+Hm/7OV2rB2N5v8qC58B6eauhu189q6JZ75zV0Nqyja4JzsHnQXGQ+sAyqkeVg21lUeVABTBFIIUQxQEF6UfKHKkzdjhMTaGcV0rZESSOcFQW7K1KFk0XTBQPEbo0QCjS273w+5P/3kxo6s83KC55NHL5/XmxkP77EDBbXprP3Sk17je9690ra+naugXpzYn03g51WrpeMNrpM6X7VaAYA)')  # vineta de las listas (ak-dip-list): flecha roja #DD0005 como el Figma (la base la trae dorada)
color('390db8e4', 'rgba(6,6,6,0.75)')
for h3 in ('5a5d4853', '3dff5c49', '36ba7119'):
    wmargin(h3, _margin=box(17, 0, 22, 0), _margin_laptop=box(12, 0, 16, 0))
for tx in ('1e2e258a', '2d2f5c00', '73081eaa'):
    color(tx, 'rgba(6,6,6,0.75)')

# experiencia estratégica: caja de 1500 como el resto (en la base era 1300) y textos a 713 px
cset('3028d48c', boxed_width=px(1500), padding=box(100, 40, 100, 40), padding_laptop=box(71, 80, 70, 80), padding_mobile=box(56, 16, 56, 16),
     min_height=px(1027), min_height_laptop=px(L(1027)))
wmargin('a50a77b', _margin=box(50, 0, 0, 0), _margin_laptop=box(36, 0, 0, 0))
cset('6bb85ab9', margin=box(189, 0, 0, 0), margin_laptop=box(134, 0, 0, 0))
# el CSS personalizado de la sección fija el relleno superior de cada etapa con !important
css_replace('3028d48c', 'selector .ak-war-step { position: relative; padding-top: 44px !important; }', 'selector .ak-war-step { position: relative; padding-top: 53px !important; }')
css_replace('3028d48c', 'selector .ak-war-step { padding-top: 30px !important; }', 'selector .ak-war-step { padding-top: 38px !important; }')
for tx in ('71560803', '746d9382', '6d95755b', '5f510898'):
    wmargin(tx, _margin=box(19, 0, 0, 0), _margin_laptop=box(14, 0, 0, 0))
cset('5b22c8d6', width=px(713), width_laptop=px(L(713)))
wwidth('3079ff74', 713, L(713)); wmargin('3079ff74', _margin=box(19, 0, 0, 0), _margin_laptop=box(14, 0, 0, 0))
for t_id in ('7a82957e', '245ad6bc', '544064c5', '1f78edf1'):
    typo(t_id, lh=1.37, lh_unit='em')

# plan de estudios: columnas como el Figma (527 / 913) e íconos rojos con figura blanca
cset('6517c0d8', width={'unit': '%', 'size': 35.1, 'sizes': []}, width_laptop={'unit': '%', 'size': 35.1, 'sizes': []})
cset('16e0013c', width={'unit': '%', 'size': 60.9, 'sizes': []}, width_laptop={'unit': '%', 'size': 60.9, 'sizes': []})
icon_svg('38e590e4', 'plan-modulos-caja-consultor-senior.svg')
icon_svg('9081977', 'plan-horas-caja-consultor-senior.svg')
icon_svg('2d10cc66', 'plan-metodologia-caja-consultor-senior.svg')

# presencia: contenido arriba (no centrado), mapa del Figma (con los puntos) a 690 px
cset('63b5ee4a', min_height=px(867), min_height_laptop=px(617), flex_align_items='flex-start',
     padding=box(71, 40, 70, 40), padding_laptop=box(51, 80, 50, 80))
cset('6d3759be', padding=box(12, 0, 0, 0), padding_laptop=box(9, 0, 0, 0))
typo('23841199', lh=1.125, lh_unit='em')
for lb in ('17fe3c03', '1bdbba21', '73c91642'): color(lb, '#838994')
image('bd987de', 'mapa-consultor-senior.webp')
remove('c43e5a5')                                   # el Figma no lleva el SVG animado con nombres
css_replace('63b5ee4a', 'selector .ak-pres-map img { width: 118%; max-width: 788px; height: auto; margin-right: -12%; }',
            'selector .ak-pres-map img { width: 690px; max-width: 100%; height: auto; margin-right: 39px; }')
css_replace('63b5ee4a', 'selector .ak-pres-map img { width: 112%; margin-right: -8%; }',
            'selector .ak-pres-map img { width: 491px; margin-right: 28px; }')

# plan: estadísticas, descarga y acordeón a la altura del Figma
cset('e42cc9c', margin=box(47, 0, 0, 0), margin_laptop=box(33, 0, 0, 0))
wmargin('5d85f006', _margin=box(7, 0, 0, 0), _margin_laptop=box(5, 0, 0, 0)); typo('5d85f006', lh=1.12, lh_unit='em')
wmargin('6b4c14ba', _margin=box(0, 0, 0, 0))
wmargin('3954484a', _margin=box(60, 0, 0, 0), _margin_laptop=box(43, 0, 0, 0))
cset('16e0013c', padding=box(15, 0, 0, 0), padding_laptop=box(11, 0, 0, 0))

# certificación: la sección se escala con --u (CSS personalizado con !important); bloque de texto a 97 px y espacios del Figma
css_replace('54c4c5af', 'selector > .ak-cert-txt { padding: calc(var(--u) * 52) calc(var(--u) * 60) calc(var(--u) * 38) calc(var(--u) * 60) !important; }',
            'selector > .ak-cert-txt { padding: calc(var(--u) * 71) calc(var(--u) * 60) calc(var(--u) * 71) calc(var(--u) * 60) !important; justify-content: center !important; }')  # Figma 20-oct: bloque centrado en vertical
css_replace('54c4c5af', 'selector .ak-cert-p { margin-top: calc(var(--u) * 28) !important; }', 'selector .ak-cert-p { margin-top: calc(var(--u) * 13) !important; }')
css_replace('54c4c5af', 'selector .ak-cert-in > .ak-card:nth-of-type(1), selector .ak-cert-p + .ak-card { margin-top: calc(var(--u) * 32) !important; }',
            'selector .ak-cert-in > .ak-card:nth-of-type(1), selector .ak-cert-p + .ak-card { margin-top: calc(var(--u) * 29) !important; }')
css_replace('54c4c5af', 'selector .ak-card + .ak-card { margin-top: calc(var(--u) * 21) !important; }', 'selector .ak-card + .ak-card { margin-top: calc(var(--u) * 9) !important; }')

# preguntas frecuentes: columna izquierda arriba (no centrada) y pregunta abierta como el Figma (169 px)
cset('521f33e5', flex_align_items='flex-start', padding=box(100, 40, 95, 40), padding_laptop=box(71, 80, 68, 80))
cset('1fd97c03', padding=box(78, 0, 0, 0), padding_laptop=box(55, 0, 0, 0))
css_add('266b2296', '''selector .e-n-accordion-item[open] > .e-con, selector .e-n-accordion-item[open] > [role="region"] { padding-bottom: 16px !important; }
@media (max-width: 1366px) {
  selector .e-n-accordion-item[open] > .e-con, selector .e-n-accordion-item[open] > [role="region"] { padding-bottom: 26px !important; }
}''')

# inversión
cset('7a49a06a', padding=box(76, 40, 80, 40), padding_laptop=box(54, 80, 64, 80))

# preguntas frecuentes: respuesta con interlineado de 21 px
for i in ['ea24eba', '77b34c1f', '3a6adec1', '584613f6', '38271e76']:
    typo(i, lh=1.24, lh_unit='em')

# ---- segunda pasada de medidas (Playwright vs Figma)
# experiencia estratégica: ancho de cada texto de etapa como en el Figma
for tx, w in zip(('71560803', '746d9382', '6d95755b', '5f510898'), (286, 320, 312, 344)): wwidth(tx, w, L(w))
# plan: número pegado al ícono, etiqueta pegada al número (los títulos <p> del tema llevan 10 px abajo)
for n in ('5d85f006', '1db9c1b2', '3121b088'):
    wmargin(n, _margin=box(0, 0, 0, 0), _margin_laptop=box(0, 0, 0, 0)); typo(n, lh=1.12, lh_unit='em')
for lb in ('6b4c14ba', '54ee35e9', '4475c46'): wmargin(lb, _margin=box(-10, 0, 0, 0))
for sb in ('1f049f70', '50bb001c', '31fa5315'): wmargin(sb, _margin=box(-6, 0, 0, 0))
wmargin('3954484a', _margin=box(27, 0, 0, 0), _margin_laptop=box(19, 0, 0, 0))
# presencia
wmargin('389c79fe', _margin=box(14, 0, 0, 0), _margin_laptop=box(10, 0, 0, 0)); color('389c79fe', 'rgba(253,252,251,0.75)')
wmargin('78c22442', _margin=box(56, 0, 0, 0), _margin_laptop=box(40, 0, 0, 0))
cset('1d2b7c01', margin=box(52, 0, 0, 0), margin_laptop=box(37, 0, 0, 0))
for st in ('67a7a2fb', '3b0cc897', '5255b723'): cset(st, flex_gap=gap(24), flex_gap_laptop=gap(17))
# certificación (unidades --u del CSS personalizado)
css_replace('54c4c5af', 'selector .ak-cert-title { margin-top: calc(var(--u) * 31) !important; }', 'selector .ak-cert-title { margin-top: calc(var(--u) * 3) !important; }')
css_replace('54c4c5af', 'selector .ak-cert-p { margin-top: calc(var(--u) * 13) !important; }', 'selector .ak-cert-p { margin-top: calc(var(--u) * 41) !important; }')
css_replace('54c4c5af', 'selector .ak-card { padding: calc(var(--u) * 30) calc(var(--u) * 24) calc(var(--u) * 30) calc(var(--u) * 24) !important;',
            'selector .ak-card { padding: calc(var(--u) * 24) calc(var(--u) * 24) calc(var(--u) * 24) calc(var(--u) * 24) !important;')
css_replace('54c4c5af', 'selector .ak-cert-p + .ak-card { margin-top: calc(var(--u) * 29) !important; }', 'selector .ak-cert-p + .ak-card { margin-top: calc(var(--u) * 36) !important; }')
css_replace('54c4c5af', 'selector .ak-card + .ak-card { margin-top: calc(var(--u) * 9) !important; }', 'selector .ak-card + .ak-card { margin-top: calc(var(--u) * 20) !important; }')
css_replace('54c4c5af', 'selector .ak-cert-btn { margin-top: calc(var(--u) * 28) !important; }', 'selector .ak-cert-btn { margin-top: calc(var(--u) * 16) !important; }')
# inversión (el botón de pago sigue anclado a la altura de «Enviar», regla de la base)
wmargin('2d4237ac', _margin=box(43, 0, 0, 0), _margin_laptop=box(31, 0, 0, 0))
wmargin('60f25b0f', _margin=box(101, 0, 0, 0), _margin_laptop=box(72, 0, 0, 0))
wmargin('2d183dc1', _margin=box(23, 0, 0, 0), _margin_laptop=box(16, 0, 0, 0))
cset('47c0a6f1', flex_justify_content='flex-start', flex_gap=gap(150), flex_gap_laptop=gap(107))
wmargin('12c8534c', _margin=box(30, 0, 0, 0), _margin_laptop=box(21, 0, 0, 0))
wmargin('3e72a9d', _margin=box(30, 0, 0, 0), _margin_laptop=box(21, 0, 0, 0))
wmargin('dc295fa', _margin=box(45, 0, 0, 0), _margin_laptop=box(32, 0, 0, 0))
wmargin('2a8cefb0', _margin=box(15, 0, 0, 0), _margin_laptop=box(11, 0, 0, 0))
# preguntas frecuentes
wmargin('36d376ec', _margin=box(49, 0, 0, 0), _margin_laptop=box(35, 0, 0, 0))
wmargin('4fe96a54', _margin=box(28, 0, 0, 0), _margin_laptop=box(20, 0, 0, 0))

# laptop (1281–1366): el menú tocaba el botón «Inscríbete ahora» (se montaban 3 px)
css_replace('13bd66b9', 'margin-left: 16px !important; margin-right: 16px !important;', 'margin-left: 13px !important; margin-right: 13px !important;')
# CTA: «Hablar con un asesor» en una sola línea también en laptop
css_add('66c6bdeb', 'selector .ak-btn .elementor-button-text { white-space: nowrap; }\n@media (max-width: 1366px) { selector .ak-btn .elementor-button { padding: 0 14px; } }')

# ---- mobile (375)
# plan: los títulos de módulo son largos; en mobile queda solo el signo +/−, sin «Ver contenido / Ocultar»
css_add('5b410621', '@media (max-width: 767px) { selector .e-n-accordion-item-title-icon .e-closed::before, selector .e-n-accordion-item-title-icon .e-opened::before { content: none; } selector .e-n-accordion-item-title-icon > span { gap: 0; } }')
# CTA mobile (≤932, el breakpoint móvil de esta base): la foto vuelve a verse (center right, como la base) y el texto
# queda sobre una superposición opaca; la foto se ve en la franja inferior, bajo los botones
CTA_XPOS = 80   # % horizontal de la foto en mobile (como la base: 'initial' + xpos); deja ver la mano escribiendo
setv('4d64e131', background_position_mobile='initial', background_xpos_mobile={'unit': '%', 'size': CTA_XPOS, 'sizes': []}, background_ypos_mobile={'unit': '%', 'size': 50, 'sizes': []})
css_add('4d64e131', '@media (max-width: 932px) { selector:not(.elementor-motion-effects-element-type-background), selector > .elementor-motion-effects-container > .elementor-motion-effects-layer { background-position: ' + f'{CTA_XPOS}% 50%' + '; } }')
cset('4d64e131', padding_mobile=box(40, 16, 150, 16))
css_add('4d64e131', '@media (max-width: 932px) { selector::before { background-image: linear-gradient(180deg, #060606 0, #060606 262px, rgba(6,6,6,0) 100%) !important; opacity: 1 !important; } }')
# CTA mobile: los dos botones con el mismo ancho y alto, texto y flecha dentro del borde (de 360 a 414)
css_add('66c6bdeb', '@media (max-width: 767px) { selector .ak-title br { display: none; } }')
css_add('66c6bdeb', '@media (max-width: 932px) { selector .ak-btn-row { width: 100% !important; align-items: stretch !important; } selector .ak-btn { width: 100% !important; max-width: 280px; }selector .ak-btn .elementor-button { width: 100% !important; height: 44px; padding: 0 16px; } }')
# presencia: «+300» se cortaba a 375
for n in ('151ee21e', '61338992', '1d0e6775'): typo(n, size_mobile=28)
# inversión: inicio y duración a los extremos en mobile (como la base)
cset('47c0a6f1', flex_gap_mobile=gap(24), flex_justify_content_mobile='space-between')
# la base tenía -25 px en todos los dispositivos: en mobile el valor se montaba sobre la etiqueta
for v in ('9030ca2', '73517676'):
    wmargin(v, _margin=box(-16, 0, 0, 0), _margin_laptop=box(-12, 0, 0, 0), _margin_mobile=box(0, 0, 0, 0))

# barra de datos: íconos en rojo
for ic, n in (('3e247b14', 'modalidad'), ('1466ad22', 'inicio'), ('54ba9d28', 'horario'), ('37b97c47', 'duracion')):
    icon_svg(ic, f'barra-{n}-consultor-senior.svg'); setv(ic, primary_color=RED)
    EXTRA_CSS.append(f'{pre(ic)}.elementor-view-framed .elementor-icon, {pre(ic)}.elementor-view-default .elementor-icon{{color:{RED};border-color:{RED}}} '
                     f'{pre(ic)}.elementor-view-framed .elementor-icon svg, {pre(ic)}.elementor-view-default .elementor-icon svg{{fill:{RED}}}')

# certificación: medalla roja
for m in ('940608c', '1adb523'): icon_svg(m, 'certificacion-medalla-consultor-senior.svg')

# pie «Alianza estratégica» (5b1123a8): en tablet (768–1024) los contenedores llevaban 1300 px fijos y se salían de la página
css_add('5b1123a8', '''@media (min-width: 768px) and (max-width: 1024px) {
  selector .elementor-element-4910e412, selector .elementor-element-4d8e8e9f, selector .elementor-element-2b717ba7 { width: 100% !important; max-width: 100%; }
  selector .elementor-element-4910e412 { flex-direction: column !important; }
  selector .elementor-element-7a5d8ad8, selector .elementor-element-234056e8 { width: 100% !important; max-width: 100%; }
  selector .elementor-element-234056e8 { flex-wrap: wrap !important; row-gap: 24px; }
  selector .elementor-element-234056e8 > .elementor-element { width: calc(50% - 8px) !important; }
  selector .elementor-element-4d8e8e9f { display: flex !important; flex-wrap: wrap !important; row-gap: 24px; }
  selector .elementor-element-4d8e8e9f > .elementor-element { width: calc(33.333% - 5px) !important; }
  selector .elementor-element-17b98aed { flex-wrap: wrap !important; row-gap: 16px; }
  selector .elementor-element-47c63207 { max-width: 100%; }
  selector .elementor-element-47c63207 img { max-width: 100%; height: auto; }
  selector .elementor-element-1c4af563 .elementor-icon-list-items { margin-left: -10px !important; margin-right: -10px !important; }
}''')

# ================================================================ módulos con scroll fijo (Guias-Landings/MODULOS-SCROLL-FIJO.md)
import plan_pin
PIN_WRAP = plan_pin.apply('7c39e8aa')

# ================================================================ beneficios y reconocimientos (sección nueva, Figma 373:581; modal por medalla)
import medallas
MED = medallas.build()
insert_after(PIN_WRAP['id'], MED); EXTRA_CUSTOM.extend(MED['css'])
# el CTA comparte el fondo gris de la sección de medallas (Figma #DDE3EA)
cset('66c6bdeb', background_color='#DDE3EA')
EXTRA_CSS.append(f"{pre('66c6bdeb')}:not(.elementor-motion-effects-element-type-background){{background-color:#DDE3EA}}")   # solo vista previa: la regla renderizada de la base es más específica

# ================================================================ restos de la base
J = lib.J
for e in J['content']: strip_html_cache(e)
J['title'] = 'CONSULTOR POLÍTICO SENIOR'
dump = json.dumps(J, ensure_ascii=False)
rest = [m.start() for m in re.finditer(r'Director de Seguridad|seguridad', dump, re.I)]
LOG.append(f'restos "seguridad" en el JSON: {len(rest)}')
for p in rest[:20]: LOG.append('  ' + dump[max(0, p - 90):p + 40].replace('\n', ' '))

# ================================================================ salida
OUT = os.path.join(ROOT, 'consultor-politico-senior-jetwoobuilder.json')
json.dump(J, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
J2 = {'version': '0.4', 'title': J['title'], 'type': 'page', 'content': J['content'], 'page_settings': [], 'metadata': []}
json.dump(J2, open(os.path.join(ROOT, 'consultor-politico-senior.json'), 'w', encoding='utf-8'), ensure_ascii=False)
# sección suelta: módulos con scroll fijo (envoltorio + sección + script), importable como contenedor
os.makedirs(os.path.join(ROOT, 'secciones'), exist_ok=True)
json.dump({'version': '0.4', 'title': 'CONSULTOR SENIOR - Módulos (scroll fijo)', 'type': 'container', 'content': [PIN_WRAP], 'page_settings': [], 'metadata': []},
          open(os.path.join(ROOT, 'secciones', 'modulos-scroll-fijo-consultor-senior.json'), 'w', encoding='utf-8'), ensure_ascii=False)
_med = [c for c in J['content'] if c['id'] == MED['id']][0]
json.dump({'version': '0.4', 'title': 'CONSULTOR SENIOR - Beneficios y reconocimientos (medallas)', 'type': 'container', 'content': [_med], 'page_settings': [], 'metadata': []},
          open(os.path.join(ROOT, 'secciones', 'beneficios-medallas-consultor-senior.json'), 'w', encoding='utf-8'), ensure_ascii=False)
_cert = [c for c in J['content'] if c['id'] == '54c4c5af'][0]
json.dump({'version': '0.4', 'title': 'CONSULTOR SENIOR - Certificación', 'type': 'container', 'content': [_cert], 'page_settings': [], 'metadata': []},
          open(os.path.join(ROOT, 'secciones', 'certificacion-consultor-senior.json'), 'w', encoding='utf-8'), ensure_ascii=False)

import page
css = lib.CSS_PRE + lib.CSS + '\n'.join(EXTRA_CSS) + '\n' + '\n'.join(EXTRA_CUSTOM) + '\n' + lib.CSS_POST
page.build(lib.HTML, css, 'landing.html', 'Consultor Político Senior')
print('\n'.join(LOG))
