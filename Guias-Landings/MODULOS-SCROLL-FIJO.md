# Módulos con scroll fijo (sección fijada mientras la lista avanza)

Receta para aplicar en cualquier landing el mismo efecto de la sección de módulos de **Carrera Diplomática** (21 oct 2026, «propuesta A, sin barra»).

**Qué hace.** Al bajar por la página, la sección de módulos se queda fija justo debajo del header. Mientras el usuario sigue bajando, la lista de módulos (el acordeón) avanza en proporción al scroll, del primer módulo al último. Cuando la lista termina, la sección se suelta y la página sigue normal. Al subir pasa lo mismo al revés.

La página hace scroll normal: no se intercepta la rueda ni se usa `preventDefault`. Solo se relaciona el progreso del scroll de la página con el `scrollTop` de la lista.

**Dónde se activa.** Solo en desktop y laptop (≥ 1025 px), y solo si la sección cabe bajo el header. En tablet, en mobile o con «reducir movimiento» del sistema no se activa nada y la sección queda como estaba.

---

## 1. Requisitos de la página (comprobar antes)

| Requisito | Cómo es en Carrera Diplomática | Si es distinto |
|---|---|---|
| Sección de módulos con clase propia | Contenedor `ak-plan` (boxed, fila con columna izquierda y acordeón a la derecha) | Cambiar `.ak-plan` en el CSS y en el JS (sección 4). |
| Acordeón anidado de Elementor (`nested-accordion`) con **scroll interno** | En su CSS personalizado: `.e-n-accordion { max-height: 760px; overflow-y: auto; }`, con 600 px en ≤ 1366 px y sin límite en ≤ 767 px (ver 3.4) | Si la lista no tiene `max-height` y `overflow-y: auto`, no hay recorrido y el efecto no hace nada. Agregar el CSS de 3.4. |
| Header fijo | `ak-hd`: 90 px de alto en desktop y 80 px en laptop | Cambiar los `top:` del CSS (90 / 80) por la altura real del header en cada tamaño. |
| Ningún ancestro con `overflow: hidden` / `clip` ni `transform` | La página usa la plantilla Canvas; el único ancestro es el `div` del producto de WooCommerce, sin overflow | Si el tema envuelve la página en un contenedor con `overflow`, `position: sticky` no funciona. Ver «Problemas» en la sección 7. |
| El enlace del menú a los módulos | `#modulos` (el CSS ID estaba en la sección) | El CSS ID pasa al contenedor envoltorio (paso 3.1). |

---

## 2. Estructura final

```
Contenedor NUEVO  «ak-plan-pin»     ← ancho completo, sin relleno, margen ni espacio; columna
│                                      CSS ID: modulos      CSS personalizado: bloque 3.2
├── Sección de módulos «ak-plan»    ← la misma de antes, sin cambios (sin el CSS ID)
│     └── … acordeón con scroll interno
└── Widget HTML «ak-plan-pin-js»    ← el script del bloque 3.3 (no ocupa espacio)
```

---

## 3. Paso a paso en Elementor (a mano)

### 3.1 Envolver la sección

1. Agregar un **contenedor nuevo** justo antes de la sección de módulos.
2. En **Diseño**:
   - Ancho del contenido: **Ancho completo**.
   - Dirección: **Columna**.
   - Espacio entre elementos: **0**.
3. En **Avanzado**:
   - Margen y relleno: **0** en todos los lados.
   - Clases CSS: `ak-plan-pin`.
   - ID de CSS: `modulos`, o el ID al que apunte el menú.
4. **Arrastrar la sección de módulos dentro** del contenedor nuevo.
5. En la sección de módulos, **borrar su ID de CSS** si lo tenía, porque no puede haber dos iguales.

### 3.2 CSS del envoltorio

En el contenedor `ak-plan-pin` → **Avanzado → CSS personalizado**. Aquí `selector` es el propio contenedor.

```css
/* fondo igual al de la sección: cubre la franja bajo la sección mientras está fijada */
selector { background-color: #FDFCFB; }
/* Propuesta A: sección de módulos fijada mientras la lista avanza (solo desktop y laptop) */
selector.is-on > .ak-plan { position: sticky !important; }
@media (min-width: 1367px) { selector.is-on > .ak-plan { top: 90px; } }
@media (min-width: 1025px) and (max-width: 1366px) { selector.is-on > .ak-plan { top: 80px; } }
selector.is-on .e-n-accordion { overflow: hidden !important; }
selector .ak-plan-prog { display: none; position: absolute; left: 0; bottom: 0; height: 3px; width: 100%; background: #DD0005; transform-origin: 0 50%; transform: scaleX(0); pointer-events: none; }
selector.is-on .ak-plan-prog { display: block; }
```

Qué cambiar en cada landing:
- `#FDFCFB`: el color de fondo de la sección de módulos de esa landing.
- `90px` / `80px`: la altura del header en desktop y en laptop.
- `#DD0005`: el color de acento, solo si se usa la barra de progreso (ver 3.3).
- `.ak-plan`: la clase de la sección, si es otra.

### 3.3 Widget HTML con el script

Dentro de `ak-plan-pin`, **después** de la sección, agregar un widget **HTML**:
- Avanzado → Clases CSS: `ak-plan-pin-js`.
- Contenido: el script de abajo. No necesita ajustes salvo que cambie la clase de la sección.

```html
<script>
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

  // Alto del header que deja libre la sección: lo lee del CSS (top de la sección fijada)
  function stickTop() { return parseFloat(getComputedStyle(sec).top) || 0; }
  function pageTop(el) { return el.getBoundingClientRect().top + window.pageYOffset; }

  // Recorrido de la lista (cuánto puede avanzar dentro de la sección)
  function travel() { return Math.max(0, list.scrollHeight - list.clientHeight); }

  // Alto de la lista (el de diseño, o el que quepa bajo el header) y alto de la wrap.
  // Si ni con la lista en su mínimo cabe la sección bajo el header (p. ej. la columna izquierda
  // es más alta que la pantalla), no se fija: la página se ve como ahora.
  function recalc() {
    if (!on || fitting) return;
    fitting = true;
    list.style.maxHeight = '';                                  // alto de diseño (CSS)
    var nat = parseFloat(getComputedStyle(list).maxHeight) || list.offsetHeight;
    var avail = window.innerHeight - stickTop() - (sec.offsetHeight - list.offsetHeight);
    list.style.maxHeight = Math.max(240, Math.min(nat, avail)) + 'px';
    if (sec.offsetHeight > window.innerHeight - stickTop()) {   // no cabe: sin fijar
      wrap.classList.remove('is-on');
      wrap.style.height = '';
      list.style.maxHeight = '';
      on = false;
      fitting = false;
      return;
    }
    wrap.style.height = (sec.offsetHeight + travel()) + 'px';   // sección + recorrido
    fitting = false;
    update();
  }

  // Progreso del scroll de la página -> scrollTop de la lista
  function update() {
    if (!on) return;
    var t = travel();
    var start = pageTop(wrap) - stickTop();                     // scroll en el que la sección se fija
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

  // Cambios de tamaño de la sección, de la lista y de cada módulo (abrir/cerrar)
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
</script>
```

Opciones:
- `SHOW_PROGRESS = true`: muestra una barra de 3 px en el borde inferior de la sección que se llena con el progreso. En Carrera va en `false`.
- `240`: alto mínimo de la lista (en px) en pantallas bajas. Si la sección no cabe ni con ese mínimo, no se fija.
- `1025px`: desde qué ancho se activa. Debe coincidir con los `@media` del CSS (3.2).

### 3.4 CSS del acordeón (solo si la lista no tiene scroll interno)

En el widget del acordeón anidado → **Avanzado → CSS personalizado**:

```css
/* scroll vertical: se ven 4 módulos completos; sin barras */
selector .e-n-accordion { max-height: 760px; overflow-y: auto; overflow-x: hidden;
  scrollbar-width: none; -ms-overflow-style: none; }
selector .e-n-accordion::-webkit-scrollbar { display: none; width: 0; height: 0; }
@media (max-width: 1366px) { selector .e-n-accordion { max-height: 600px; } }
@media (max-width: 767px)  { selector .e-n-accordion { max-height: none; overflow: visible; } }
```

`760` y `600` son la altura visible de la lista en desktop y laptop. Hay que ajustarlos para que se vean unos 4 módulos completos con el diseño de esa landing.

---

## 4. Si la landing se genera por JSON (pipeline `transform.py` + `spec.py`)

En Carrera Diplomática está en el bloque final de `_work/spec.py` («Plan de estudios: sección fijada…»), que lee el CSS y el JS de `_work/propuestas/a-elementor.txt`. Resumen de lo que hace en el JSON:

```json
{
  "id": "<id nuevo>", "elType": "container", "isInner": false,
  "settings": {
    "content_width": "full", "flex_direction": "column",
    "css_classes": "ak-plan-pin", "_element_id": "modulos",
    "flex_gap": {"unit": "px", "size": 0, "column": "0", "row": "0", "isLinked": true},
    "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": true},
    "margin":  {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": true},
    "custom_css": "<bloque 3.2>"
  },
  "elements": [
    { "...": "la sección de módulos, con \"isInner\": true y SIN \"_element_id\"" },
    { "id": "<id nuevo>", "elType": "widget", "widgetType": "html", "isInner": false, "elements": [],
      "settings": { "html": "<script>…bloque 3.3…</script>", "_css_classes": "ak-plan-pin-js" } }
  ]
}
```

Puntos clave:
- **Va en la misma posición del `content`** de la página que ocupaba la sección. El envoltorio es el elemento de primer nivel.
- **Vista previa:** el envoltorio lleva el marcado de Elementor `e-con-full … e-con e-parent` con `id="modulos"`. La sección pasa de `e-parent` a `e-child` y pierde el `id`. También hay que añadir el CSS generado del envoltorio (variables `--gap`, `--padding-*` y `--margin-*` a 0, más `--flex-direction: column`).
- **Secciones sueltas:** en `split.py`, la sección se identifica por `ak-plan-pin`, no por `ak-plan`. El archivo de la sección debe incluir el envoltorio, la sección y el script.

---

## 5. Comprobación (obligatoria antes de entregar)

Medir con Playwright o a mano, con un módulo abierto (el primero, como queda al cargar).

| Tamaño | Qué comprobar |
|---|---|
| 1920×1080 | Al llegar, la sección queda en `top` = altura del header y la lista en 0. A mitad del recorrido, la lista está a la mitad. Al final, la lista está en su máximo (se ve el último módulo) y el borde inferior de la sección coincide con el borde de la ventana. 150 px después, la sección ya subió 150 px. |
| 1440×900 y 1366×768 | Lo mismo. La lista puede verse más baja para que la sección entera quepa. |
| 1024 (tablet) y 375 (mobile) | **Página idéntica a la versión sin el efecto:** mismas posiciones y altura de todas las secciones. |
| Pantalla baja (p. ej. 1025×700) | Si la sección no cabe, no se fija y queda como antes. |
| Enlace del menú (`#modulos`) | Lleva al inicio de la sección. |
| Subir | El recorrido se hace al revés, sin saltos. |
| Abrir o cerrar un módulo mientras está fija | El recorrido se recalcula y no hay saltos. |
| Resto de la página | Fuera de la sección, solo cambia el desplazamiento por el scroll extra. |

Referencia de Carrera Diplomática (scroll extra que añade):
- 1920×1080: 1180 px.
- 1440×900: 1326 px.
- 1366×768: 890 px.
- 1024 y 375: no se fija.

---

## 6. Decisiones de diseño (por qué está hecho así)

- **Mientras está fija, la lista lleva `overflow: hidden`.** La rueda sobre la lista mueve la página y la lista solo avanza con el progreso. Así el script y la rueda no compiten y no hace falta interceptar eventos.
- **La sección se fija con `position: sticky` sobre un envoltorio más alto**: alto de la sección + recorrido de la lista. Es scroll nativo del navegador y el JS solo calcula alturas y `scrollTop`.
- **Recalcula con `ResizeObserver`** sobre la sección, la lista y cada módulo (al abrir o cerrar cambia el recorrido), y también en `resize` y `load`.
- **El fondo del envoltorio es el de la sección**: si la sección es más baja que la pantalla, la franja de abajo no se ve blanca.
- **Funciona sin JS:** la lista queda con su scroll propio, como antes del cambio.

---

## 7. Problemas y soluciones

| Síntoma | Causa | Solución |
|---|---|---|
| La sección no se queda fija | Un ancestro tiene `overflow: hidden`, `overflow: clip` o `transform` | Buscarlo en el inspector, subiendo desde `ak-plan-pin`. Si es del tema, usar la plantilla Canvas o poner `overflow: visible` en ese contenedor solo en esta página. |
| La lista no se mueve | El acordeón no tiene `max-height` y `overflow-y: auto` | Añadir el CSS de 3.4. |
| La sección queda tapada por el header o deja un hueco | Los `top:` del CSS no coinciden con la altura real del header | Medir el header en desktop y en laptop y ajustar los `top:` del bloque 3.2. |
| Franja blanca bajo la sección mientras está fija | El envoltorio no tiene el fondo de la sección | Poner en `selector { background-color: … }` el color de fondo de la sección. |
| El menú lleva a otro sitio o no hace nada | El ID quedó en la sección o hay dos IDs iguales | El ID solo va en `ak-plan-pin`. |
| En el editor de Elementor la sección se ve más alta | El script fija el alto del envoltorio | Es normal. En el editor se puede trabajar igual. |
| No funciona con varias secciones de módulos en la misma página | El script toma el primer `.ak-plan-pin` | Para más de una, duplicar el script cambiando la clase (`ak-plan-pin-2`) o adaptarlo a `querySelectorAll`. |

Sin probar todavía: Safari y Firefox. Probado en Chromium.
