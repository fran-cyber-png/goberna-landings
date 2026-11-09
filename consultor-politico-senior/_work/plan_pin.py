# Módulos con scroll fijo (Guias-Landings/MODULOS-SCROLL-FIJO.md, «propuesta A, sin barra»):
# envoltorio ak-plan-pin (id modulos) + la sección ak-plan sin id + widget HTML con el script.
import re
import lib
from lib import pre, nid, el_span

PIN_CSS = '''/* fondo igual al de la sección: cubre la franja bajo la sección mientras está fijada */
selector { background-color: #F3F5F7; }
/* Propuesta A: sección de módulos fijada mientras la lista avanza (solo desktop y laptop) */
selector.is-on > .ak-plan { position: sticky !important; }
@media (min-width: 1367px) { selector.is-on > .ak-plan { top: 90px; } }
@media (min-width: 1025px) and (max-width: 1366px) { selector.is-on > .ak-plan { top: 80px; } }
selector.is-on .e-n-accordion { overflow: hidden !important; }
selector .ak-plan-prog { display: none; position: absolute; left: 0; bottom: 0; height: 3px; width: 100%; background: #DD0005; transform-origin: 0 50%; transform: scaleX(0); pointer-events: none; }
selector.is-on .ak-plan-prog { display: block; }'''

PIN_JS = r'''<script>
(function () {
  'use strict';
  var SHOW_PROGRESS = false;              // true = barra roja de progreso (opcional)

  var wrap = document.querySelector('.ak-plan-pin');
  if (!wrap) return;
  var sec = wrap.querySelector('.ak-plan');
  var list = sec && sec.querySelector('.e-n-accordion');
  if (!sec || !list) return;
  var items = [].slice.call(list.querySelectorAll('details'));
  var mqDesk = window.matchMedia('(min-width: 1025px)');
  var mqReduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var on = false, fitting = false, ticking = false, bar = null;

  if (SHOW_PROGRESS) {
    bar = document.createElement('i');
    bar.className = 'ak-plan-prog';
    sec.appendChild(bar);
  }

  function stickTop() { return parseFloat(getComputedStyle(sec).top) || 0; }
  function pageTop(el) { return el.getBoundingClientRect().top + window.pageYOffset; }
  function travel() { return Math.max(0, list.scrollHeight - list.clientHeight); }

  function recalc() {
    if (!on || fitting) return;
    fitting = true;
    list.style.maxHeight = '';
    var nat = parseFloat(getComputedStyle(list).maxHeight) || list.offsetHeight;
    var avail = window.innerHeight - stickTop() - (sec.offsetHeight - list.offsetHeight);
    list.style.maxHeight = Math.max(240, Math.min(nat, avail)) + 'px';
    if (sec.offsetHeight > window.innerHeight - stickTop()) {
      wrap.classList.remove('is-on');
      wrap.style.height = '';
      list.style.maxHeight = '';
      on = false;
      fitting = false;
      return;
    }
    wrap.style.height = (sec.offsetHeight + travel()) + 'px';
    fitting = false;
    update();
  }

  function update() {
    if (!on) return;
    var t = travel();
    var start = pageTop(wrap) - stickTop();
    var p = t > 0 ? (window.pageYOffset - start) / t : 0;
    p = Math.min(1, Math.max(0, p));
    list.scrollTop = p * t;
    if (bar) bar.style.transform = 'scaleX(' + p + ')';
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { ticking = false; update(); });
  }

  function setOn(v) {
    if (v === on) return;
    on = v;
    if (on) {
      wrap.classList.add('is-on');
    } else {
      wrap.classList.remove('is-on');
      wrap.style.height = '';
      list.style.maxHeight = '';
      if (bar) bar.style.transform = 'scaleX(0)';
    }
  }

  function sync() {
    setOn(mqDesk.matches && !mqReduce.matches);
    recalc();
  }

  if ('ResizeObserver' in window) {
    var ro = new ResizeObserver(function () { recalc(); });
    ro.observe(sec); ro.observe(list);
    items.forEach(function (d) { ro.observe(d); });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', sync, { passive: true });
  window.addEventListener('load', sync);
  if (mqDesk.addEventListener) { mqDesk.addEventListener('change', sync); mqReduce.addEventListener('change', sync); }
  sync();
})();
</script>'''

ZERO = {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}

def apply(plan_id='7c39e8aa'):
    """Envuelve la sección de módulos (JSON + vista previa) y devuelve el envoltorio."""
    J = lib.J
    idx = [c['id'] for c in J['content']].index(plan_id)
    plan = J['content'][idx]
    anchor = plan['settings'].pop('_element_id', None) or 'modulos'
    plan['isInner'] = True
    wid, hid = nid(), nid()
    html_w = {'id': hid, 'elType': 'widget', 'widgetType': 'html', 'isInner': False, 'elements': [],
              'settings': {'html': PIN_JS, '_css_classes': 'ak-plan-pin-js'}}
    wrap = {'id': wid, 'elType': 'container', 'isInner': False, 'elements': [plan, html_w],
            'settings': {'content_width': 'full', 'flex_direction': 'column', 'css_classes': 'ak-plan-pin', '_element_id': anchor,
                         'flex_gap': {'unit': 'px', 'size': 0, 'column': '0', 'row': '0', 'isLinked': True},
                         'padding': dict(ZERO), 'margin': dict(ZERO), 'custom_css': PIN_CSS}}
    J['content'][idx] = wrap
    # vista previa: la sección pasa a hija y pierde el id; el envoltorio la contiene junto con el script
    s, e = el_span(lib.HTML, plan_id)
    blk = lib.HTML[s:e]
    head_end = blk.find('>') + 1
    head = blk[:head_end].replace(' e-parent', ' e-child').replace(f' id="{anchor}"', '')
    blk = head + blk[head_end:]
    html_widget = (f'<div class="elementor-element elementor-element-{hid} ak-plan-pin-js elementor-widget elementor-widget-html" data-id="{hid}" '
                   f'data-element_type="widget" data-e-type="widget" data-widget_type="html.default"><div class="elementor-widget-container">{PIN_JS}</div></div>')
    wrapper = (f'<div class="elementor-element elementor-element-{wid} e-con-full ak-plan-pin e-flex e-con e-parent" data-id="{wid}" '
               f'data-element_type="container" data-e-type="container" id="{anchor}">{blk}{html_widget}</div>')
    lib.HTML = lib.HTML[:s] + wrapper + lib.HTML[e:]
    p = pre(wid)
    css = [f'{p}{{--display:flex;--flex-direction:column;--container-widget-width:100%;--container-widget-height:initial;--container-widget-flex-grow:0;'
           f'--container-widget-align-self:initial;--flex-wrap-mobile:wrap;--gap:0px 0px;--row-gap:0px;--column-gap:0px;'
           f'--padding-top:0px;--padding-right:0px;--padding-bottom:0px;--padding-left:0px;--margin-top:0px;--margin-right:0px;--margin-bottom:0px;--margin-left:0px}}',
           PIN_CSS.replace('selector', p)]
    lib.EXTRA_CUSTOM.extend(css)
    lib.reindex()
    return wrap
