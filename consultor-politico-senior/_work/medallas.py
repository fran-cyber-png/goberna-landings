# Beneficios y reconocimientos (sección nueva, Figma 373:581 → medallas 451:104…106; modales 459:143, 460:156, 460:179, 460:198; flechas 460:230 / 460:233)
# Todo lo visible es nativo (títulos, textos, imágenes). Un solo widget HTML dentro del modal: flechas, cerrar y el script.
import lib
from lib import pre, px, box, gap, container, w_heading, w_text, w_image

RED, DARK = '#DD0005', '#0C0000'
L = lambda v: round(v * 1366 / 1920, 1)    # desktop -> laptop (Figma escalado)

MEDALS = [
    {'k': 'bronce', 'lvl': 'Bronce', 'color': '#92543B',
     'card': 'Medalla del Consultor<br> Político Empresarial', 'modal': 'Medalla del Consultor<br> Político Empresarial',
     'txt': 'Distinción a quienes culminan la primera etapa del programa y logran formalizar su firma de consultoría, desarrollar su identidad corporativa y establecer su presencia profesional.',
     'crit': 'Constitución de la empresa e implementación de la imagen de negocio.'},
    {'k': 'plata', 'lvl': 'Plata', 'color': '#646464',
     'card': 'Medalla del Arquitecto de<br> Poder Político', 'modal': 'Medalla del Arquitecto<br> de Poder Político',
     'txt': 'Distinción a los consultores que consolidan su firma mediante la instalación de una oficina, la captación de sus primeros clientes y el cierre de contratos profesionales, iniciando su trayectoria en campañas electorales o de gobierno.',
     'crit': 'Contar con oficina propia, al menos un cliente y experiencia en una campaña política o gubernamental.'},
    {'k': 'oro', 'lvl': 'Oro', 'color': '#CFA401',
     'card': 'Medalla del Arquitecto<br> de Éxito Presidencial', 'modal': 'Medalla del Arquitecto<br> de Éxito Presidencial',
     'txt': 'Distinción para quienes convierten su consultora en una organización consolidada y alcanzan uno de los mayores logros de la profesión: asesorar con éxito una campaña.',
     'crit': 'Haber contribuido a una campaña presidencial ganadora y mantener una consultora en crecimiento.'},
    {'k': 'diamante', 'lvl': 'Diamante', 'color': '#007076',
     'card': 'Medalla del Maestro<br> de Estrategias Globales', 'modal': 'Medalla del Maestro<br> de Estrategias Globales',
     'txt': 'La máxima distinción del programa. Reconoce a los estrategas que han replicado el éxito presidencial en dos o más países, demostrando liderazgo, capacidad de adaptación e influencia internacional.',
     'crit': 'Ganar campañas presidenciales en distintos países y dirigir una consultora con proyección internacional.'},
]
IMG = lambda k: f'medalla-{k}-consultor-senior.webp'
ZERO = box(0, 0, 0, 0)
FULL = {'unit': '%', 'size': 100, 'sizes': []}

# rótulos en Montserrat SemiBold 17/20, espaciado 2,38, mayúsculas (cards y modal)
LBL = dict(family='Montserrat', weight=600, transform='uppercase', size=17, lh=20, ls=2.38,
           size_laptop=L(17), lh_laptop=L(20), ls_laptop=L(2.38), size_mobile=12, lh_mobile=16, ls_mobile=1.6)

SEC_CSS = '''/* Beneficios y reconocimientos: 4 medallas; clic en una tarjeta = modal con su detalle */
selector .elementor-widget-text-editor p { margin: 0; }
selector .ak-med-title .elementor-heading-title .ak-r { color: #DD0005; }
selector .ak-med-txt { border-left: 1px solid #DD0005; padding-left: 25px; width: 746px; max-width: 746px; flex: none; }
selector .ak-med-head, selector .ak-med-grid, selector .ak-med-card, selector .ak-med-pan, selector .ak-med-pan-l, selector .ak-med-pan-r { padding: 0 !important; flex-wrap: nowrap !important; }
/* tarjetas */
selector .ak-med-card { flex: 1 1 0 !important; min-width: 0; cursor: pointer; outline: none; }
selector .ak-med-card .ak-med-img { width: 100%; }
selector .ak-med-img img { display: block; width: 100%; height: auto; }
selector .ak-med-card .ak-med-img img { transition: transform .35s ease, filter .35s ease; }
selector .ak-med-card:hover .ak-med-img img, selector .ak-med-card:focus-visible .ak-med-img img { transform: translateY(-6px); filter: drop-shadow(0 14px 18px rgba(12,0,0,.14)); }
selector .ak-med-card:focus-visible { outline: 2px solid #DD0005; outline-offset: 6px; border-radius: 12px; }
selector .ak-med-name .elementor-heading-title::after { content: ""; display: block; width: 64px; height: 2px; margin: 13px auto 0; background: currentColor; }
selector .ak-med-card .ak-med-name .elementor-heading-title { text-align: center; }
/* modal: centrado en la pantalla (fixed + flex), fondo difuminado y la tarjeta en foco */
selector .ak-med-modal { position: fixed !important; inset: 0; z-index: 100000; display: flex !important; align-items: center !important; justify-content: center !important;
  padding: 24px !important; background: rgba(12,0,0,.22); -webkit-backdrop-filter: blur(5px); backdrop-filter: blur(5px);
  opacity: 0; visibility: hidden; transition: opacity .35s ease, visibility 0s linear .35s; }
selector .ak-med-modal.is-open { opacity: 1; visibility: visible; transition: opacity .35s ease, visibility 0s; }
selector .ak-med-dlg { position: relative; width: 753px !important; max-width: calc(100vw - 172px); min-height: 424px; flex: none !important;
  display: flex !important; align-items: stretch !important; background: #F2F4F7; border: 2px solid #DD0005; border-radius: 32px;
  padding: 24.5px 30px 24.5px 25px !important; box-shadow: 0 30px 80px rgba(12,0,0,.22);
  transform: translateY(14px) scale(.97); transition: transform .45s cubic-bezier(.2,.8,.2,1); }
selector .ak-med-modal.is-open .ak-med-dlg { transform: none; }
selector .ak-med-pan { display: none !important; flex: 1 1 auto !important; align-items: center !important; gap: 15px; }
selector .ak-med-pan.is-act { display: flex !important; animation: akMedIn .35s ease both; }
@keyframes akMedIn { from { opacity: 0; } to { opacity: 1; } }
selector .ak-med-pan-l { width: 369px !important; flex: none !important; align-items: center !important; gap: 15px; }
selector .ak-med-pan-r { width: 310px !important; flex: none !important; }
selector .ak-med-pan .ak-med-name .elementor-heading-title::after { margin: 12px 0 0; }
selector .ak-med-pan .ak-med-desc { margin-top: 25px; }
selector .ak-med-desc p + p { margin-top: 26px; }
selector .ak-med-desc strong { font-weight: 700; }
/* controles (widget HTML): flechas a los costados (Figma: 43 px, a 25 px del borde) y cerrar */
selector .ak-med-js { position: absolute !important; inset: 0; pointer-events: none; margin: 0 !important; width: auto !important; }
selector .ak-med-js button { pointer-events: auto; }
selector .ak-med-nav { position: absolute; top: 50%; width: 43px; height: 43px; margin-top: -21.5px; padding: 0; border: 0; border-radius: 50%;
  background: #DD0005; color: #FFFFFF; cursor: pointer; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 6px 16px rgba(12,0,0,.18); transition: background-color .25s, color .25s, transform .25s; }
selector .ak-med-nav svg { width: 43px; height: 43px; display: block; }
selector .ak-med-prev { left: -70px; }
selector .ak-med-prev svg { transform: scaleX(-1); }
selector .ak-med-next { right: -70px; }
selector .ak-med-nav:hover { background: #B80004; }
selector .ak-med-nav:disabled { background: #FFFFFF; color: #DD0005; cursor: default; opacity: .9; }
selector .ak-med-nav:focus-visible { outline: 2px solid #FFFFFF; outline-offset: 3px; }
selector .ak-med-x:focus-visible { outline: 2px solid #DD0005; outline-offset: 1px; }
selector .ak-med-x { position: absolute; top: 16px; right: 18px; width: 32px; height: 32px; padding: 0; border: 0; border-radius: 50%; background: transparent; cursor: pointer; }
selector .ak-med-x::before, selector .ak-med-x::after { content: ""; position: absolute; left: 8px; top: 15px; width: 16px; height: 2px; background: #0C0000; opacity: .55; transform: rotate(45deg); transition: opacity .2s, background-color .2s; }
selector .ak-med-x::after { transform: rotate(-45deg); }
selector .ak-med-x:hover::before, selector .ak-med-x:hover::after { opacity: 1; background: #DD0005; }
html.ak-med-lock { overflow: hidden !important; }
/* editor de Elementor: el modal se muestra abierto y con las 4 fichas, para poder editarlas */
body.elementor-editor-active selector .ak-med-modal { position: relative !important; inset: auto; z-index: auto; opacity: 1; visibility: visible; background: none; backdrop-filter: none; -webkit-backdrop-filter: none; padding: 40px 0 0 !important; }
body.elementor-editor-active selector .ak-med-dlg { flex-direction: column !important; gap: 24px; transform: none; max-width: 100%; }
body.elementor-editor-active selector .ak-med-pan { display: flex !important; }
body.elementor-editor-active selector .ak-med-js { display: none; }
@media (max-width: 1366px) {
  selector .ak-med-txt { padding-left: 17.8px; width: 531px; max-width: 531px; }
  selector .ak-med-card .ak-med-name .elementor-heading-title::after { width: 45.5px; margin-top: 9.2px; }
}
@media (max-width: 1024px) {
  selector .ak-med-card .ak-med-name br { display: none; }
  selector .ak-med-card .ak-med-name .elementor-heading-title { text-wrap: balance; }
}
@media (max-width: 932px) {
  selector .ak-med-head { flex-direction: column !important; gap: 16px; }
  selector .ak-med-txt { width: 100%; max-width: none; padding-left: 14px; }
  selector .ak-med-grid { flex-wrap: wrap !important; column-gap: 12px; row-gap: 28px; }
  selector .ak-med-card { flex: 0 0 calc(50% - 6px) !important; }
  selector .ak-med-card .ak-med-name .elementor-heading-title::after { width: 40px; margin-top: 8px; }
  /* modal mobile: ficha en columna con alto fijo (no salta al cambiar), centrada; flechas debajo (relleno simétrico) */
  selector .ak-med-modal { padding: 76px 16px !important; }
  selector .ak-med-dlg { width: 420px !important; max-width: 100%; min-height: 0; height: min(600px, calc(100dvh - 152px)); padding: 22px 20px !important; border-radius: 24px; }
  selector .ak-med-pan { flex-direction: column !important; align-items: stretch !important; justify-content: flex-start !important; gap: 0; overflow-y: auto; overscroll-behavior: contain; }
  selector .ak-med-pan-l { width: 100% !important; gap: 8px; }
  selector .ak-med-pan-l .ak-med-img { width: 210px; max-width: 70%; }
  selector .ak-med-pan-r { width: 100% !important; margin-top: 14px; }
  selector .ak-med-pan .ak-med-name .elementor-heading-title { text-align: center; }
  selector .ak-med-pan .ak-med-name .elementor-heading-title::after { width: 48px; margin: 10px auto 0; }
  selector .ak-med-pan .ak-med-desc { margin-top: 16px; }
  selector .ak-med-desc p + p { margin-top: 14px; }
  selector .ak-med-nav { top: calc(100% + 18px); margin-top: 0; }
  selector .ak-med-prev { left: 50%; margin-left: -51px; }
  selector .ak-med-next { right: auto; left: 50%; margin-left: 8px; }
  selector .ak-med-x { top: 10px; right: 10px; }
}
@media (prefers-reduced-motion: reduce) {
  selector .ak-med-modal, selector .ak-med-dlg, selector .ak-med-card .ak-med-img img { transition: none; }
  selector .ak-med-pan.is-act { animation: none; }
}'''

# flecha del Figma (460:230 / 460:233): mismo trazo; el círculo es el fondo del botón (rojo activo, blanco sin más fichas)
CHEVRON = ('<svg viewBox="0 0 43 43" aria-hidden="true" focusable="false"><path fill="currentColor" d="M26.4023 22.1445L18.8242 29.7617C18.4336 30.1133 17.8477 30.1133 17.4961 29.7617'
           'L16.5977 28.8633C16.2461 28.5117 16.2461 27.9258 16.5977 27.5352L22.6133 21.4805L16.5977 15.4648C16.2461 15.0742 16.2461 14.4883 16.5977 14.1367'
           'L17.4961 13.2383C17.8477 12.8867 18.4336 12.8867 18.8242 13.2383L26.4023 20.8555C26.7539 21.207 26.7539 21.793 26.4023 22.1445Z"/></svg>')

MED_JS = '''<button type="button" class="ak-med-x" aria-label="Cerrar"></button>
<button type="button" class="ak-med-nav ak-med-prev" aria-label="Medalla anterior">''' + CHEVRON + '''</button>
<button type="button" class="ak-med-nav ak-med-next" aria-label="Medalla siguiente">''' + CHEVRON + '''</button>
<script>
(function () {
  'use strict';
  function init() {
    var sec = document.querySelector('.ak-med');
    if (!sec || sec.getAttribute('data-ak-med')) return;
    sec.setAttribute('data-ak-med', '1');
    if (document.body.classList.contains('elementor-editor-active')) return;   // en el editor todo queda a la vista
    var modal = sec.querySelector('.ak-med-modal'), dlg = modal && modal.querySelector('.ak-med-dlg');
    if (!dlg) return;
    var cards = [].slice.call(sec.querySelectorAll('.ak-med-card'));
    var pans = [].slice.call(dlg.querySelectorAll('.ak-med-pan'));
    var prev = dlg.querySelector('.ak-med-prev'), next = dlg.querySelector('.ak-med-next'), close = dlg.querySelector('.ak-med-x');
    var cur = 0, last = null, x0 = null, y0 = null;

    dlg.setAttribute('role', 'dialog');
    dlg.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-hidden', 'true');

    function show(i) {
      cur = Math.max(0, Math.min(pans.length - 1, i));
      pans.forEach(function (p, k) { p.classList.toggle('is-act', k === cur); });
      var h = pans[cur].querySelector('.ak-med-name .elementor-heading-title');
      if (h) dlg.setAttribute('aria-label', h.textContent.replace(/\\s+/g, ' ').trim());
      prev.disabled = cur === 0;
      next.disabled = cur === pans.length - 1;
      pans[cur].scrollTop = 0;
    }
    function open(i) {
      last = document.activeElement;
      show(i);
      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
      document.documentElement.classList.add('ak-med-lock');
      setTimeout(function () { close.focus({ preventScroll: true }); }, 30);
    }
    function shut() {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      document.documentElement.classList.remove('ak-med-lock');
      if (last && last.focus) last.focus({ preventScroll: true });
    }
    function isOpen() { return modal.classList.contains('is-open'); }

    cards.forEach(function (c, i) {
      c.setAttribute('role', 'button');
      c.setAttribute('tabindex', '0');
      c.setAttribute('aria-haspopup', 'dialog');
      c.addEventListener('click', function () { open(i); });
      c.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); }
      });
    });
    prev.addEventListener('click', function () { show(cur - 1); });
    next.addEventListener('click', function () { show(cur + 1); });
    close.addEventListener('click', shut);
    modal.addEventListener('click', function (e) { if (e.target === modal) shut(); });
    document.addEventListener('keydown', function (e) {
      if (!isOpen()) return;
      if (e.key === 'Escape') { shut(); }
      else if (e.key === 'ArrowLeft') { show(cur - 1); }
      else if (e.key === 'ArrowRight') { show(cur + 1); }
      else if (e.key === 'Tab') {
        var f = [close, prev, next].filter(function (b) { return !b.disabled; });
        var k = f.indexOf(document.activeElement);
        e.preventDefault();
        f[(k + (e.shiftKey ? f.length - 1 : 1)) % f.length].focus();
      }
    });
    // mobile: deslizar la ficha para pasar de medalla
    dlg.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
    dlg.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) show(cur + (dx < 0 ? 1 : -1));
      x0 = null;
    }, { passive: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
</script>'''


def _lvl(m, cls='ak-med-lvl'):
    return w_heading(m['lvl'], 'div', m['color'], cls=cls, **LBL)

def _card(m):
    lvl = _lvl(m)
    img = w_image(IMG(m['k']), cls='ak-med-img', _margin=box(25, 0, 0, 0), _margin_laptop=box(L(25), 0, 0, 0), _margin_mobile=box(10, 0, 0, 0))
    name = w_heading(m['card'], 'div', m['color'], cls='ak-med-name', **dict(LBL, size_mobile=11, lh_mobile=15, ls_mobile=1.2))
    name['node']['settings']['align'] = 'center'
    name_w = name
    name_w['node']['settings'].update(_margin=box(25, 0, 0, 0), _margin_laptop=box(L(25), 0, 0, 0), _margin_mobile=box(12, 0, 0, 0))
    p = pre(name_w['id'])
    name_w['css'] += [f'{p} > .elementor-widget-container{{margin:25px 0 0 0}}', f'@media(max-width:1366px){{{p} > .elementor-widget-container{{margin:{L(25)}px 0 0 0}}}}',
                      f'@media(max-width:932px){{{p} > .elementor-widget-container{{margin:12px 0 0 0}}}}']
    return container({'flex_direction': 'column', 'flex_align_items': 'center', 'flex_gap': gap(0), 'padding': ZERO,
                      'width': {'unit': '%', 'size': 25, 'sizes': []}, 'width_mobile': {'unit': '%', 'size': 48, 'sizes': []}},
                     [lvl, img, name_w], cls=f'ak-med-card ak-med-{m["k"]}')

def _panel(m):
    lvl = _lvl(m)
    img = w_image(IMG(m['k']), cls='ak-med-img')
    left = container({'flex_direction': 'column', 'flex_align_items': 'center', 'flex_gap': gap(15), 'padding': ZERO, 'width': px(369), 'width_mobile': FULL},
                     [lvl, img], cls='ak-med-pan-l')
    name = w_heading(m['modal'], 'div', m['color'], cls='ak-med-name', **dict(LBL, size_laptop=17, lh_laptop=20, ls_laptop=2.38, size_mobile=14, lh_mobile=18, ls_mobile=1.6))
    desc = w_text(f'<p>{m["txt"]}</p><p><strong>Criterio:</strong> {m["crit"]}</p>', 'rgba(6,6,6,0.75)', cls='ak-med-desc',
                  family='Inter', weight=400, size=14, lh=26, ls=0.14, size_laptop=14, lh_laptop=26, ls_laptop=0.14, size_mobile=13, lh_mobile=22, ls_mobile=0.13)
    right = container({'flex_direction': 'column', 'flex_gap': gap(0), 'padding': ZERO, 'width': px(310), 'width_mobile': FULL}, [name, desc], cls='ak-med-pan-r')
    return container({'flex_direction': 'row', 'flex_direction_mobile': 'column', 'flex_align_items': 'center', 'flex_gap': gap(15), 'padding': ZERO,
                      'width': FULL}, [left, right], cls=f'ak-med-pan ak-med-pan-{m["k"]}')


def build():
    title = w_heading('Beneficios y<br> <span class="ak-r">reconocimientos</span>', 'h2', DARK, cls='ak-med-title',
                      family='Montserrat', weight=700, size=50, lh=49, size_laptop=L(50), lh_laptop=L(49), size_mobile=26, lh_mobile=30)
    txt = w_text('<p>Quienes alcancen las máximas distinciones del programa accederán a beneficios exclusivos, como el ingreso a una red internacional de consultores, '
                 'oportunidades de participación en proyectos estratégicos y eventos políticos de alto nivel.</p>', 'rgba(0,0,0,0.75)', cls='ak-med-txt',
                 family='Inter', weight=400, size=18, lh=29, ls=0.18, size_laptop=12.8, lh_laptop=20.6, ls_laptop=0.128, size_mobile=14, lh_mobile=22, ls_mobile=0.14)
    s = txt['node']['settings']
    s.update(_element_width='initial', _element_custom_width=px(746), _element_custom_width_laptop=px(L(746)), _element_custom_width_mobile=FULL)
    head = container({'flex_direction': 'row', 'flex_direction_mobile': 'column', 'flex_justify_content': 'space-between', 'flex_align_items': 'flex-start',
                      'flex_gap': gap(24), 'flex_gap_mobile': gap(16), 'padding': ZERO, 'width': FULL}, [title, txt], cls='ak-med-head')
    grid = container({'flex_direction': 'row', 'flex_wrap': 'nowrap', 'flex_wrap_mobile': 'wrap', 'flex_align_items': 'flex-start',
                      'flex_gap': gap(15), 'flex_gap_laptop': gap(L(15)), 'flex_gap_mobile': {'column': '12', 'row': '28', 'isLinked': False, 'unit': 'px'},
                      'padding': ZERO, 'margin': box(80, 0, 0, 0), 'margin_laptop': box(L(80), 0, 0, 0), 'margin_mobile': box(32, 0, 0, 0), 'width': FULL},
                     [_card(m) for m in MEDALS], cls='ak-med-grid')
    js = lib._widget('html', {'html': MED_JS}, MED_JS, 'ak-med-js')
    dlg = container({'flex_direction': 'row', 'flex_gap': gap(0), 'padding': box(24.5, 30, 24.5, 25), 'width': px(753)},
                    [_panel(m) for m in MEDALS] + [js], cls='ak-med-dlg')
    modal = container({'flex_direction': 'row', 'flex_justify_content': 'center', 'flex_align_items': 'center', 'flex_gap': gap(0), 'padding': box(24, 24, 24, 24),
                       'width': FULL}, [dlg], cls='ak-med-modal')
    sec = container({'content_width': 'boxed', 'boxed_width': px(1520), 'flex_direction': 'column', 'flex_gap': gap(0),
                     'padding': box(87, 40, 67, 40), 'padding_laptop': box(L(87), 142, 46, 142), 'padding_tablet': box(56, 32, 40, 32), 'padding_mobile': box(48, 16, 28, 16),
                     'background_background': 'classic', 'background_color': '#DDE3EA',
                     '_element_id': 'beneficios', 'custom_css': SEC_CSS}, [head, grid, modal], parent=True, cls='ak-med')
    # vista previa: el CSS ID también en el HTML
    sec['html'] = sec['html'].replace(f'data-id="{sec["id"]}"', f'data-id="{sec["id"]}" id="beneficios"', 1)
    return sec
