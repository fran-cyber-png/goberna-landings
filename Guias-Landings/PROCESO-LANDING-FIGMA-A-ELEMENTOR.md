# Proceso general: Landing de Figma → Artifact → plantilla de Elementor

Versión para **cualquier proyecto** (landing, programa, curso, página de evento…). Nace de la landing de Diana Pereira (`PROCESO-CV-PONENTE-ELEMENTOR.md` tiene el caso concreto con todas sus medidas). Aquí van el método, las fórmulas y los errores, sin cifras de un proyecto en particular.

Sitio: WordPress + Elementor Pro. Guía base de landings del usuario: `GUIA-LANDINGS-ELEMENTOR.md` (contenedores en caja, widgets nativos, clases con prefijo del proyecto `ak-…`, CSS en "CSS personalizado" con `selector`, nada de "Ocultar en…", mobile al 87 %).

Idioma de trabajo: español. Regla de oro del usuario: **ver primero el Artifact, aprobarlo, y solo después recibir el JSON**.

### Base de las landings (desde el 16 de octubre de 2026)

**Toda landing nueva de programa, diploma o curso parte de la plantilla final de Director de Seguridad**, no de cero ni de bases anteriores (Crimen Organizado, 93083):

- **Base:** `C:\Users\Consultoría\Documents\Director-Seguridad\plantilla-base-director-seguridad-jetwoobuilder.json` (copia de `jet-woo-builder-93575-2026-10-16.json`, plantilla Elementor 93575).
- **Publicada en:** https://grupogoberna.com/diploma-de-elite-internacional-de-seguridad/
- **Figma que coincide con ella:** frame `DIRECTOR-SEGURIDAD-WEB-1920` (6112:373), archivo `UtWCaOFmeJXaBbp8BoA865`. Medidas y capturas en `Director-Seguridad\_referencia-web\`.
- **La base no se modifica nunca:** el usuario lo pidió explícitamente ("No toques nada del json"). Se trabaja siempre sobre una copia en la carpeta del proyecto nuevo.
- **Qué se cambia sobre la copia:** textos, imágenes, colores, ítems repetidos (módulos, docentes, preguntas) y lo que el Figma del proyecto nuevo pida. La estructura, las clases `ak-…`, el CSS y los ajustes ya corregidos (sección 12) se mantienen. Si el usuario pasa una exportación nueva de una sección, esa exportación pasa a ser la base de esa sección.
- **Al entregar:** quitar `htmlCache`, buscar restos de "Director de Seguridad" en todo el JSON y dar el tipo importable (sección 6).
- La sección 10, con el generador `_plantilla-cv-ponente/`, sigue siendo para los **CV de ponentes**.

---

## 1. Qué se entrega y dónde

Todo proyecto (curso, programa, CV, landing) se guarda en **su propia carpeta de proyecto**: `C:\Users\Consultoría\Documents\<carpeta-del-proyecto>\` (por ejemplo `Documents\curso-inteligencia-y-contrainteligencia\`, `Documents\Director-Seguridad\`). Si la sesión ya se abrió en la carpeta del proyecto, se trabaja ahí mismo. **No** se usa `cv-ponentes\` para proyectos nuevos (desde el 23 de octubre de 2026); esa carpeta solo conserva los proyectos anteriores y el generador `_plantilla-cv-ponente/`.

Dentro de la carpeta del proyecto:

| Archivo / carpeta | Contenido |
|---|---|
| `<slug>.json` | Plantilla de Elementor importable: `{"version":"0.4","title":"…","type":"page","content":[…],"page_settings":[],"metadata":[]}` |
| `<slug>-datos.json` | Los datos del proyecto (textos, cifras). **Solo datos**: importarlo da "Invalid Content In File". |
| `imagenes/` | `.webp`, **cada una < 500 KB** sin bajar calidad ni resolución (probar q90+ a la resolución original; si no entra, webp casi sin pérdida). Reportar el peso de cada una. |
| `iconos/` | Íconos `.svg` con nombres descriptivos. |
| `iconos-webp/` | Los mismos íconos en webp sin pérdida (`magick -density 600 icono.svg icono.webp`; si sale en blanco, quitar el `<mask>` del SVG). Son los que se incrustan en el JSON. |

Nunca usar placeholders ni inventar imágenes o íconos "para saber qué reemplazar": se usan los reales del Figma.

Herramientas reutilizables: `C:\Users\Consultoría\Documents\cv-ponentes\_plantilla-cv-ponente\` (`gen_final.py` generador del JSON, `tpl.html` + `build.py` plantilla del Artifact, `a/` recursos). Se copia y se adapta (sección 10).

---

## 2. Flujo completo (en este orden)

1. **Recoger insumos**: copia de la **plantilla base** (ver "Base de las landings" arriba), URL de Figma (frames desktop y móvil), contenido (hoja de Google Sheet de ponentes u otro), imágenes e íconos. No guardar nunca tokens de Figma (`figd_…`) pegados en el chat: no usarlos y recomendar revocarlos.
2. **Leer el Figma** con `get_metadata` (posiciones, tamaños, textos) y `get_screenshot`. Para código usar `get_design_context` (antes cargar la guía `figma-design-to-code`).
3. **Crear la versión laptop** en Figma con la skill `figma-laptop-adapt` (clona el frame de 1920 y le aplica `rescale(1366/1920)` en la página "Laptop"). Es la referencia exacta de 1366.
4. **Convertir medidas** a valores de Elementor (secciones 3 y 4).
5. **Construir el Artifact** con selector Desktop / Laptop / Mobile y modo "Ver widgets" (cada elemento marcado con su widget de Elementor, fuente, tamaño y valor de Figma).
6. **Medir el Artifact con Playwright** a 1366 y 1920 y comparar con el Figma (sección 7). Corregir hasta que cuadre. **Este paso evita casi todas las iteraciones.** Después pasar la **revisión de detalles que el Figma no muestra** (sección 12): son las correcciones que el usuario tuvo que pedir a ojo.
7. **Publicar el Artifact y esperar aprobación.** (Si el usuario envía capturas, medir otra vez en lugar de ajustar a ojo.)
8. **Generar el JSON** desde el generador, copiarlo a la carpeta del proyecto y dar la ruta + instrucción de importación.
9. Si el usuario manda capturas de Elementor, buscar primero la causa en la tabla de errores (sección 6).
10. Guardar las lecciones nuevas en este `.md` y en la memoria.

---

## 3. Escalas Figma → Elementor

| Elementor | Origen | Factor |
|---|---|---|
| Laptop (≤1366) | Frame laptop de Figma (1366) | **1:1** |
| Desktop (>1366) | Frame de 1920 px | **ancho de la caja de Elementor ÷ ancho del contenido en Figma** (en Diana: 1500 / 1519 = **0,987**) |
| Mobile (≤767, ancho 375) | Frame móvil (430) | **375 / 430 = 0,872** |
| Tablet (≤1024) | Normalmente no hay Figma | Diseño propio; hereda de laptop |

Breakpoints: Desktop >1366 · Laptop ≤1366 · Tablet ≤1024 · Mobile ≤767. Cada valor se hereda hacia abajo (desktop → laptop → tablet → mobile): lo que no se redefine en un nivel viene del anterior. Por eso, al introducir valores nuevos en laptop (por ejemplo `vw`), hay que copiar los valores antiguos a tablet para que no cambie.

Cálculo del factor desktop: medir el ancho del contenido principal en Figma (p. ej. tarjeta 1519) y compararlo con el ancho que quieras en Elementor (p. ej. 1500). Todas las medidas de desktop = Figma × factor.

### Cómo leer posiciones en Figma
- `get_metadata` da `x, y, width, height` de cada nodo, relativos a su padre. Sumar las posiciones del padre para tener coordenadas absolutas.
- **Separación entre dos elementos** = `y` del siguiente − (`y` + alto) del anterior.
- Una caja de texto puede ser más alta que su línea (títulos con alto fijo de 65/91 px): el texto está centrado verticalmente. Medir desde el **centro** del título, no desde la caja.
- Altura de texto de N líneas ÷ N = interlineado. Un texto de 242 px con 10 líneas = 24,2 px.
- Separación entre ítems de una lista = `y` del ítem siguiente − (`y` + alto) del anterior.
- Líneas separadoras (`line`) tienen alto 0: su posición `y` es el centro de la línea.
- Los nombres de capa pueden venir de otra plantilla (restos como "ELLIS"): el texto real es el que se ve en el screenshot.

---

## 4. Estructura típica de una landing en Elementor

```
<prefijo>-hero    (contenedor boxed, fondo imagen, overflow hidden)
 ├─ logo (imagen) · título (heading h1) · texto (editor de texto)
 ├─ caja con ítems / íconos (contenedor + cajas de imagen)
 ├─ foto (imagen anclada al hero)
 └─ textos ocultos que cargan fuentes extra (Sora, Manrope…)
<prefijo>-fondo   (fondo de color, centra la tarjeta)
 └─ <prefijo>-card (tarjeta blanca; content_width full + width en px)
      └─ <prefijo>-cols (fila; envuelve texto + columna fija)
           ├─ <prefijo>-main (secciones: título con ícono, texto, divisor, lista)
           └─ <prefijo>-side (columna derecha, sticky)
```

Reglas:
- Pocos contenedores (la guía lo pide). Cada sección repetida usa los mismos widgets: caja de imagen (título + ícono), editor de texto, divisor, lista de iconos.
- Clases `ak-<prefijo>-…` en `css_classes` del contenedor o `_css_classes` del widget. CSS en `custom_css` con `selector`.
- **Sticky**: `sticky: top`, `sticky_on: [desktop, laptop]`, `sticky_parent: yes`, `sticky_offset` = la misma distancia que el elemento tiene en reposo respecto al borde de su tarjeta. **El sticky de Elementor usa el borde exterior del padre**: para que quede el relleno inferior, el padre inmediato debe ser un contenedor interior **sin relleno** (`-cols`), y el relleno va en la tarjeta.
- Lo que cambia por dispositivo (p. ej. un bloque de datos que en móvil va dentro de otra sección) se resuelve con dos copias y CSS de media query (`display:none` / `flex`), no con "Ocultar en…".

---

## 5. Imágenes, íconos y fuentes

- **Fondo, logo y fotos**: `webp` que sube el usuario a la Biblioteca de medios (URL `https://grupogoberna.com/wp-content/uploads/AAAA/MM/…` + id). El JSON las referencia: `image: {url, id, size:'', alt:'', source:'library'}`. Entregar al usuario la lista de archivos de `imagenes/` que debe subir y pedirle las URLs/ids.
- **Íconos de barras, títulos y viñetas**: fondo CSS con data URI webp dentro del `custom_css` del widget (`::before`). **No** subirlos a la Biblioteca y **no** usar widgets de imagen con SVG o data URI: Elementor no los muestra (solo funcionan bien los webp por URL de la Biblioteca).
- **Fuentes**: Elementor solo carga las fuentes que algún widget usa. Para fuentes que solo se aplican por CSS (por ejemplo, solo en móvil), añadir widgets de texto ocultos con esa fuente y clase `…-fuentes{display:none}`.

---

## 6. Errores de Elementor ya vistos (síntoma → causa → solución)

| Síntoma | Causa | Solución |
|---|---|---|
| "Invalid Content In File" | Se importó el JSON de datos | Importar la plantilla `<slug>.json`. |
| "This source does not support import" | Importar desde la pestaña Cloud | Plantillas → **Plantillas guardadas** → Importar desde el equipo. |
| La clase de un contenedor no se aplica | Estaba en `_css_classes` | Contenedor: **`css_classes`**. Widget: `_css_classes`. |
| **Un margen/relleno de contenedor "no se ve"** | Se usó `_margin` / `_padding` | Contenedor: **`margin` / `padding`**. Widget: `_margin` / `_padding`. |
| Tarjeta anidada a pantalla completa | Contenedor anidado con `content_width: boxed` | `content_width: full` + `width` en px, dentro de un padre `flex_align_items: center`. |
| Íconos en gris o ausentes | Elementor ignora SVG y data URI en widgets de imagen | Fondo CSS con data URI webp. |
| Foto en el lado equivocado | Posicionamiento absoluto con ancla incorrecta | Anclar al hero completo (`left` y `width` en %, `top:0`). |
| Contenido de laptop pegado al borde | En el editor la vista Laptop mide el ancho de la ventana (p. ej. 1010 px), no 1366 | Medidas de la portada de laptop en `vw` (px ÷ 13,66), ancho de contenido en % (≈79 %), copiar los px a tablet. |
| Borde con hueco (título que lo corta) cruzado por el texto | El recorte con `mask-composite` se pierde al redefinir `mask` en otro breakpoint | `clip-path: polygon(0 0,Xpx 0,Xpx 3px,X+Wpx 3px,X+Wpx 0,100% 0,100% 100%,0 100%)`. |
| Texto de la caja de imagen más alto que el ícono | `margin-bottom:10px` del título de la caja de imagen | `selector .elementor-image-box-title{margin:0 !important}` y ocultar la descripción vacía. |
| Columna sticky pegada al borde inferior | Sticky usa el borde exterior del padre | Contenedor interior sin relleno (`-cols`). |
| Interlineado en `vw` ignorado | El control no siempre acepta `vw` | Usar `em` (lh / tamaño) en laptop y px en los demás. |
| Saltos de línea distintos al Figma | Tamaños de texto redondeados (18 / 13) un poco más anchos | Usar 17,8 / 12,8 (= tamaño × factor) y dar holgura derecha a las listas (margen derecho −12 px desktop / −8 px laptop). |
| Hueco inesperado entre bloques | Párrafos con margen inferior y `flex_gap` por defecto | `selector p{margin:0}` en los textos; `flex_gap` explícito en cada contenedor y espacios con márgenes de widget. |
| "Tipo de plantilla no válido" al importar | El JSON heredó `"type": "jet-woo-builder"` de la base | Entregar dos archivos: uno con `type: page` (o `container` si es una sección) para *Plantillas guardadas* y otro en formato JetWooBuilder para *JetWooBuilder → Templates*. |
| Textos viejos de la base en el editor | Cada widget trae `htmlCache` con el HTML del proyecto anterior | Quitar `htmlCache` de todos los nodos antes de entregar. |
| Regla de "el primero" que funciona en la vista previa y falla en el editor | `:first-child` / `:nth-child`: dentro del editor Elementor inserta un elemento de controles antes de cada bloque | Reglas por clase propia (`ak-…`), nunca por posición. |
| Header fijo más angosto que la pantalla en el editor | El sticky toma el ancho que tenía con el panel lateral abierto | `width:100% !important` en el contenedor del header. |
| Imagen gris al importar | La imagen no existe todavía en `uploads/AAAA/MM/` | Comprobar con HTTP que cada URL del JSON responde **antes** de entregar y listar las que faltan subir. Elementor añade `-1` al nombre cada vez que reimporta una imagen. |
| Cuadro gris vacío a la izquierda de un botón con enlace `wa.me` | **No es de la plantilla:** un script del sitio pone la clase `flag` a los enlaces de WhatsApp y el "CSS adicional" del tema dibuja `a.flag::before` (recuadro de bandera de 18 × 12) | Avisar al usuario que es del sitio. Para anularlo solo en la landing: `selector a.flag::before{content:none}` (sin probar). |
| Íconos con los colores de la landing anterior en WordPress (en la vista previa se veían bien) | Los widgets de ícono apuntan a los SVG de la base en la Biblioteca. La vista previa recolorea el SVG incrustado, pero WordPress usa el archivo original | Crear SVG propios (`<nombre>-<slug>.svg` en `iconos\`) con los colores del Figma y que la vista previa incruste esos archivos. Elementor dibuja el SVG **por su id**: con `id: ''` no se ve, así que hay que poner los ids reales después de que el usuario los suba. |
| El acordeón (nested-accordion) salta al terminar de abrir o cerrar | El JS de Elementor anima a `summary.offsetHeight + contenido.offsetHeight` (al cerrar, solo el summary aún abierto). `offsetHeight` no incluye márgenes, y los bordes del ítem no se suman | Summary con la misma altura abierto y cerrado (desplazar el texto con `transform`), sin márgenes en el contenido (márgenes negativos solo en hijos internos), bordes como `box-shadow inset`. La vista previa debe imitar ese mismo cálculo. |
| Textos nuevos que no aparecen en las tarjetas del carrusel (vista previa) | El DOM publicado trae copias de bucle (`swiper-slide-duplicate`) antes de las reales y el reemplazo cae en la copia | Quitar primero las copias del carrusel y después cambiar los textos. |
| Títulos largos que pisan el texto de abajo (etapas del War Room) | La base usa `_margin` inferior de −50 px pensando en títulos de una línea | Margen inferior 0 y el texto 5 px debajo (Figma); compensar el alto con el relleno de la sección. |
| Contenedores nuevos con relleno de 10 px o envueltos en mobile | Elementor pone `--padding:10px` y `--flex-wrap-mobile: wrap` por defecto | En el CSS de la sección: `padding:0 !important` y `flex-wrap:nowrap !important` en esos contenedores. |
| El Artifact no se publica | Archivos `.eot` o fuentes `.svg` con DOCTYPE en `_preview/a` | No subirlos: el navegador usa woff2. |
| Franja blanca de ~25 px bajo el footer | Iframes y divs de pasarelas de pago del sitio (Openpay / Culqi) | No es de la plantilla. Al medir la página, cortar en el borde inferior del footer. |

Datos de la vista previa capturada del sitio (grupogoberna.com):
- El CSS personalizado de cada elemento va entre `/* Start custom CSS for X, class: .elementor-element-ID */` y `/* End custom CSS */`. Se reemplaza entero por el `custom_css` del JSON.
- Los anchos de contenedor van dentro de `@media(min-width:933px){`. El mobile del sitio es `max-width:932px`, no 767.
- Al exportar una imagen del Figma con transparencia, revisar que no quede aplanada sobre un fondo opaco.
- El generador de ids nuevos usa semilla fija (`random.seed`) para que el JSON salga igual en cada corrida.
- Además de la página completa, entregar `secciones\NN-<sección>-<slug>.json` (una plantilla `type: container` por sección, mismo formato que las de Director).

Formato de valores en el JSON:
- Tamaños: `{"unit":"px","size":N,"sizes":[]}`.
- Márgenes / rellenos: `{"unit":"px","top":"N","right":"N","bottom":"N","left":"N","isLinked":false}` (números como texto).
- Por dispositivo: sufijos `_laptop`, `_tablet`, `_mobile` (desktop sin sufijo).
- `flex_gap`: `{"column":"N","row":"N","isLinked":false,"unit":"px"}`.
- Cada nodo lleva `id` (7 caracteres hex únicos), `elType`, `settings`, `elements` e `isInner`.

---

## 7. Verificación del Artifact contra el Figma (obligatoria)

1. Servir `dianapereira.html` (o el equivalente) en local con `python -m http.server` en una carpeta y abrirlo con Playwright (`file:` está bloqueado: usar `http://127.0.0.1:PUERTO/…`).
2. Viewport **1366** (modo laptop) y **1920** (modo desktop); **375** para móvil.
3. `evaluate` midiendo `getBoundingClientRect()` relativo al contenedor `#stage` de: hero, logo, títulos, textos, caja de especialidades, tarjeta, títulos de sección, párrafos, listas, columna fija y cifras.

```js
() => { const st=document.getElementById('stage'), o=st.getBoundingClientRect();
  const R=(sel,i=0)=>{const e=document.querySelectorAll(sel)[i]; if(!e) return null;
    const b=e.getBoundingClientRect(); return [b.left-o.left,b.top-o.top,b.width,b.height].map(v=>+v.toFixed(1))};
  return {hero:R('.hero'), card:R('.card'), ul2:R('.sec ul',0), side:R('.side')}; }
```

4. Comparar con Figma: laptop = Figma literal; desktop = Figma × factor desktop.
5. Tolerancias: ≤ 2 px en posiciones; alturas de listas con el mismo número de líneas. Comprobar también que el centro del ícono coincide con el del título.
6. Qué hacer si no cuadra: ajustar primero el Artifact; el JSON se genera después con los mismos números.

---

## 8. Técnicas de CSS ya probadas

- **Borde de caja con título que lo corta** (tipo fieldset): `::before` con `border:1px solid color; border-radius; inset:0` + `clip-path` (sección 6). El título es un widget con `position:absolute !important; top:-Npx; left:Npx`.
- **Íconos como fondo**: `selector .ak-xx-ico .elementor-image-box-wrapper::before{content:"";display:block;width:Wpx;height:Hpx;margin:0 auto 9px;background:url(data:image/webp;base64,…) center/contain no-repeat}` con medias queries.
- **Portada escalable en laptop**: valores en `vw` dentro de `@media (min-width:1025px) and (max-width:1366px)`, con un bloque `@media (max-width:1366px)` previo en px (que usa tablet).
- **Viñetas de lista**: `.elementor-icon-list-item::before` con fondo webp, `flex:none`, `margin-right` por dispositivo.
- **Foto anclada al hero**: `position:absolute; top:0; left:X%; width:Y%; z-index:1; pointer-events:none` y el resto de hijos con `position:relative; z-index:2`.

---

## 9. Reglas permanentes del usuario

- Todo curso, programa o CV de docente va a **su propia carpeta de proyecto** (`Documents\<carpeta-del-proyecto>\`) con la estructura de la sección 1. Nada nuevo en `cv-ponentes\`.
- En todo CV de ponente: columna derecha (3 estadísticas, borde dorado izquierdo de 1 px) **siempre fija (sticky)** en desktop y laptop, solo dentro de su sección.
- Artifact primero, aprobación, luego JSON.
- No inventar imágenes ni íconos; pocos contenedores; widgets nativos; mobile al 87 %; nada de "Ocultar en…".
- Contenido de las landings desde la **hoja de ponentes (Google Sheet)**, una pestaña por ponente (se lee como CSV).
- Flujo Diseño-Ins / Diseño-Eje (preguntar todo antes de mandar tareas en Figma): ver la memoria `flujo-diseno-ins-eje`.

---

## 10. Cómo arrancar un proyecto nuevo (paso a paso)

1. En la carpeta del proyecto (`Documents\<carpeta-del-proyecto>\`) crear `imagenes/`, `iconos/`, `iconos-webp/` y `secciones/`.
2. Copiar `cv-ponentes\_plantilla-cv-ponente\` a una carpeta de trabajo dentro del proyecto (o al scratchpad) y adaptar:
   - **Generador (`gen_final.py`)**: `OUT`, `IMG` (URLs e ids de la Biblioteca de medios), textos, `esp_items` / `HEAD_ICON` / `LI` (íconos con su ancho y alto), colores y fuentes. Si el diseño es otro, rehacer los bloques del hero y la tarjeta con las funciones `container()`, `widget()`, `heading()`, `text()`, `image()`, `bullets()`, `divider()`, `stat()`.
   - **Artifact (`tpl.html`)**: sustituir textos e imágenes (marcadores `{{BG}}`, `{{LOGO}}`, `{{HYSA}}`…) y las reglas `#stage.desk`, `#stage.lap`, `#stage.mob` con las medidas nuevas; `build.py` incrusta los assets de `a/`.
3. Medir el Figma y rellenar una tabla propia con las medidas de desktop, laptop y móvil (copiar la tabla del documento de Diana y reemplazar los números).
4. Construir y verificar el Artifact (sección 7); publicar; esperar aprobación.
5. Ejecutar el generador; comprobar el JSON (tamaño, claves de contenedor, sin referencias a `.svg`); copiarlo a la carpeta del proyecto.
6. Entregar al usuario: ruta del JSON, lista de imágenes que debe subir, instrucciones de importación.

---

## 11. Checklist antes de dar el JSON

- [ ] Todo guardado en la carpeta del proyecto (nada en `cv-ponentes\`).
- [ ] Armado sobre una copia de la plantilla base; la base original sin tocar.
- [ ] Artifact aprobado.
- [ ] Medidas verificadas en Playwright (1366, 1920 y 375).
- [ ] Contenedores con `margin`/`padding` y `css_classes`; widgets con `_margin`/`_padding` y `_css_classes`.
- [ ] Sin SVG ni data URI en widgets de imagen; íconos como fondo CSS.
- [ ] Portada laptop en `vw` y tablet con los px antiguos; interlineados en `em`.
- [ ] Columna fija con padre interior sin relleno y `sticky_offset` igual a su distancia en reposo.
- [ ] Sin párrafos con margen inferior inesperado; `flex_gap` explícito.
- [ ] Imágenes `.webp` < 500 KB en `imagenes/`; lista de lo que debe subir el usuario.
- [ ] Ruta del JSON + instrucciones: Plantillas → Plantillas guardadas → Importar.
- [ ] Revisión de la sección 12 hecha en 1920, 1366, 1024 y 375.
- [ ] Sin `htmlCache`, sin `:first-child` / `:nth-child`, tipo de plantilla importable (`page` / `container`).
- [ ] Sin restos del proyecto base (grep del nombre anterior en todo el JSON).
- [ ] Todas las URLs de imágenes y videos responden (sin 404).

---

## 12. Detalles que el Figma no muestra (revisar siempre)

Salieron de la landing Director de Seguridad (oct. 2026): el usuario los tuvo que corregir **a ojo** porque en el diseño no se veían o el diseño los traía mal. Revisarlos en el Artifact antes de publicarlo, en desktop, laptop, tablet y mobile.

### 12.1 Contenido
- **El Figma puede traer textos de relleno o de otro proyecto:** menú con "ABOUT", frames auxiliares con el texto de otra landing, fotos de otros docentes. El texto oficial es el del documento de contenido del usuario (PDF/Word). Si no coinciden, armar una tabla *Figma vs. documento* y preguntar cuál manda; no mezclar.
- **Restos de la base en ajustes que no se ven:** nombre del formulario, asunto del correo, título del video, textos alternativos. Buscar el nombre del proyecto base en todo el JSON y reemplazarlo.
- **Textos de tarjetas con foto:** que no tapen la cara ni empujen el botón fuera de la tarjeta. El usuario prefiere bios cortas (≈110–140 caracteres) o sin bio. Al acortar, no repetir lo que ya dice la línea de arriba.
- No agregar contenido que no esté en el documento (filas de cifras, lemas bajo una sección): el usuario los quita.
- **Fotos de docentes del Figma:** comparar cada foto con las de la Biblioteca. En Inteligencia y Contrainteligencia (oct. 2026) dos tarjetas tenían la foto de otro docente (el nombre de la capa delataba de quién era).
- **Varias landings comparten el layout del Figma** (CII = Carrera Diplomática): si las alturas de las secciones coinciden, reutilizar las posiciones ya calibradas del `spec.py` anterior.

### 12.2 Consistencia (el Figma suele tener un elemento distinto a sus vecinos)
- **Valores de una misma fila** (barra de datos): mismo tamaño, espaciado y altura, aunque en el Figma uno sea más grande.
- **Tarjetas de un mismo grupo:** idéntico estilo en todos los breakpoints. Copiar los ajustes de la tarjeta de referencia a las demás y conservar solo el contenido (título, texto, enlace, imagen).
- **Marcadores de un grupo** (puntos de una línea de tiempo, viñetas): todos iguales y sólidos en el color de acento, no solo el primero.
- **Botón con borde de color:** texto del mismo color que el borde.
- **Espacios simétricos:** en pestañas con barra + ícono + texto, la separación barra–ícono = ícono–texto.
- **Colores heredados de la paleta de la base** (bordes, franjas, "+" de acordeones): revisar cada uno contra la paleta nueva; en la base había un borde de 40 px del widget de pestañas en el color del proyecto anterior.
- **Botones en columnas paralelas** (pagar / enviar): a la misma altura. Anclarlos al fondo de su columna con el mismo bloque debajo; si una nota puede pasar a dos líneas en algún ancho, reservar dos líneas en ambas.
- **Viñetas de listas:** el usuario las quiere como puntos o íconos en el color de acento, por CSS de la sección (cambian solas al agregar ítems).

### 12.3 Uniones, bordes y fondos
- **Sección montada sobre otra con margen negativo** (barra de datos sobre el hero): a los costados se ve el blanco de la página. Fondo con `linear-gradient(to bottom, transparent Npx, <color de la sección siguiente> Npx)`, con N = lo que se monta en cada breakpoint.
- **Subrayado de color que debe calzar sobre una línea gris:** quitar el margen inferior del título y ajustar el interlineado; el borde de color termina exactamente donde la línea gris.
- **Dos tarjetas al 50 % + separación** se salen del contenedor y el `overflow` les recorta las esquinas: usar `flex:1 1 0`. Comprobar que se vean las 4 esquinas redondeadas.
- **Imágenes con el mismo nombre en distintos meses** (`AAAA/MM`): en el Artifact se pisan. Usar la ruta completa como clave.

### 12.4 Interacción y estados (el Figma es estático)
- **Acordeones y pestañas:** abrir y cerrar con animación suave (≈450 ms y un fundido del contenido).
- **El título no debe cambiar de ancho al abrir o cerrar:** los rótulos alternos ("Ver contenido +" / "Ocultar −") ocupan el mismo ancho (superpuestos en una grilla o con `min-width`).
- **Header fijo que se encoge** (`.elementor-sticky--effects`): el botón de acción también reduce su alto, ancho y tipografía (al tamaño del menú), con transición; definirlo por breakpoint.
- **Logo del header centrado en vertical:** `selector .<logo> .elementor-widget-container{line-height:0}` y `selector .<logo> a{display:block}` (la imagen en línea deja un espacio debajo).
- **Botón de play:** centrado exacto en el cuadro (`left:50%; top:50%` y margen negativo de la mitad), en todos los tamaños.
- **Reproductor de videos:** comprobar que cada mp4 responde. Si queda un solo video, ocultar flechas, puntos y avisos de "desliza". Si no hay miniaturas, el video se inicia con un clic en el cuadro grande.

### 12.5 Mobile y tablet (el Figma móvil no cubre todo)
- **Tarjetas de carrusel en mobile:** a todo el ancho del contenedor, sin flechas (se pasa deslizando o con los puntos), alto proporcional a la foto y texto pegado al borde inferior.
- **Flechas de carrusel en tablet:** se salen por los costados y la página se desplaza hacia los lados. Recortar lo que sobra (`overflow:hidden` en la sección).
- **Márgenes grandes de desktop** (p. ej. 60–125 px sobre un nombre) no sirven en mobile: revisar en 375.
- **Botones de ancho fijo:** que no se salgan de la pantalla en 360–414.
- **Degradado oscuro sobre fotos:** intensidad moderada (≈60–85 %) y que empiece donde empieza el texto; si se quita un texto, acortar el degradado.
- En mobile, título y subtítulo del hero con la misma alineación.

### 12.6 La vista previa del Artifact
- Los componentes simulados (carrusel) deben recalcularse al cambiar de dispositivo con el selector; si no, se deforman al pasar de mobile a desktop.
- En la vista de una sola sección, el fondo de la página debe ser el de la sección; si no, aparece una "línea blanca" abajo.
- Decir siempre si una diferencia es solo de la vista previa o también del JSON.

### 12.7 Imágenes
- Originales en ×4: para llegar a < 500 KB, **primero bajar la resolución** (a ×2, la medida de las demás imágenes del mismo tipo) con calidad 90–92; bajar la calidad solo si no alcanza. Reportar medidas y peso.
- Si el usuario pide "sin pérdida" y pasa de 500 KB, entregarla igual y avisar, ofreciendo la versión con calidad 95.
- Nombres de archivo únicos y descriptivos (sin espacios), para no chocar con imágenes de otras landings en la Biblioteca.

### 12.8 Figma con Diseño / Diseño-Ins
- Al cambiar el alto del frame, las capas con restricción vertical *Stretch* se estiran: pedir que queden en *Top*.
- Comparar cada versión completa contra la anterior: aparecen restos sueltos o piezas borradas (rayitas, una aguja de un ícono).
- **Cuando el usuario cierra la plantilla, la web manda:** el Figma se actualiza desde la página publicada. Capturar a 1920 sin barra de desplazamiento (`html{scrollbar-width:none}`), con las imágenes diferidas ya cargadas y los carruseles en su primera diapositiva.
