# Proceso para crear el CV / landing de un ponente (Figma → Artifact → Elementor)

Documento de referencia hecho con la landing de **Diana Pereira** (carpeta `diana-pereira/`). Sigue estos pasos en orden para no iterar: casi todo el vaivén de esa landing vino de errores que ya están listados aquí.

Todo se escribe en español. El usuario quiere **ver primero el Artifact y aprobarlo**, y solo después recibir el JSON de Elementor.

---

## 0. Qué se entrega y dónde

Carpeta propia del ponente en `C:\Users\Consultoría\Documents\cv-ponentes\<slug>\`:

| Archivo / carpeta | Contenido |
|---|---|
| `<slug>.json` | Plantilla de Elementor **importable** (`version: "0.4"`, `type: "page"`, `content: [contenedores]`). |
| `<slug>-datos.json` | Los datos del ponente (texto, cifras). Es solo datos: importarlo en Elementor da "Invalid Content In File". |
| `imagenes/` | Fotos y fondos en `.webp`, **cada una < 500 KB**, sin bajar calidad ni resolución (probar q90+ a resolución original; si no entra, webp casi sin pérdida). Reportar el peso de cada una. |
| `iconos/` | Íconos `.svg` con nombres descriptivos. |
| `iconos-webp/` | Los mismos íconos renderizados a webp sin pérdida (`magick -density 600`; si sale en blanco, quitar el `<mask>` del SVG). Son los que van dentro del JSON. |

Nunca usar placeholders: el JSON lleva las imágenes e íconos reales.

Las herramientas para regenerar todo están en `_plantilla-cv-ponente/`:
- `gen_final.py` — genera el JSON de Elementor (ahora apunta a Diana; ver sección 9 para adaptarlo).
- `tpl.html` + `build.py` + carpeta `a/` — plantilla del Artifact (`build.py` incrusta los assets en base64 y genera `dianapereira.html`, el archivo que se publica).

---

## 1. Flujo recomendado (en este orden)

1. **Leer el Figma** del ponente (frames desktop 1920 y móvil 430; ver sección 2). Con `get_metadata` sacar posiciones, tamaños y textos de cada nodo. Con `get_screenshot` ver el diseño.
2. **Crear la página Laptop** con la skill `figma-laptop-adapt` (clona el frame de 1920 y le aplica `rescale(1366/1920)`). Así el Figma laptop es la referencia exacta de 1366.
3. **Convertir las medidas** a valores de Elementor (sección 3 y 4).
4. **Construir el Artifact** (`tpl.html` → `build.py` → publicar). Tiene selector Desktop / Laptop / Mobile y un modo "Ver widgets" que muestra qué widget de Elementor es cada cosa.
5. **Medir el Artifact con Playwright** a 1366 y 1920 px y comparar con el Figma (sección 8). Corregir hasta que cuadre. **Esto evita casi todas las iteraciones.**
6. Publicar el Artifact y **esperar la aprobación del usuario**.
7. Solo entonces generar el JSON (`gen_final.py`), copiarlo a la carpeta del ponente y dar la ruta.
8. Si el usuario manda capturas de Elementor, el problema casi siempre está en la sección 6 (errores ya vistos).

---

## 2. Figma

- Archivo de referencia: `Foro-Ponentes`, fileKey `VDnG8Ey0gIPBtCqea1kya9`. Página "Desktop" (frame 1920 px), página "Mobile" (frame 430 px) y página "Laptop" (clon escalado a 1366).
- Diana: desktop `395:2`, laptop `426:2`, móvil `409:2`.
- Los nombres de capa pueden tener restos de otra plantilla (por ejemplo "ELLIS"): el texto real es el que se ve en el screenshot / `get_design_context`.
- **Nunca pegar ni guardar tokens de Figma** (`figd_…`) en archivos. Si el usuario pega uno en el chat, no usarlo y recomendar revocarlo (Figma → Settings → Security).
- Para `get_design_context` hay que cargar antes la guía `figma-design-to-code` (si no está como skill, leer `skill://figma/figma-design-to-code/SKILL.md`). Para solo medir, `get_metadata` + `get_screenshot` bastan.

### Escalas entre Figma y Elementor (clave)

| Elementor | Origen | Factor |
|---|---|---|
| **Laptop (≤1366)** | Frame laptop de Figma (1366) | **1:1** — usar los valores tal cual |
| **Desktop (>1366)** | Frame 1920 de Figma | **× 0,987** (tarjeta 1519 → 1500 px) |
| **Mobile (≤767, 375)** | Frame móvil 430 | **× 0,872** (la guía dice: mobile al 87 %) |
| Tablet (≤1024) | No hay Figma | Diseño propio de una columna; hereda de laptop |

Breakpoints de Elementor: Desktop >1366 · Laptop ≤1366 · Tablet ≤1024 · Mobile ≤767. Cada valor se hereda hacia abajo (desktop → laptop → tablet → mobile), así que lo que no se redefine en un nivel viene del anterior.

---

## 3. Medidas de referencia (Diana; valen como punto de partida)

Sacadas del Figma. Elementor desktop = Figma × 0,987; laptop = Figma literal.

### Portada (hero)
| | Desktop | Laptop |
|---|---|---|
| Alto mínimo | 839 | 604,7 |
| Ancho del contenido | 1500 (boxed) | 79 % de la pantalla (= 1081 a 1366) |
| Relleno superior | 100 | 72 |
| Logo (ancho) / margen inferior | 182 / 43,5 | 131 / 31,3 |
| DIANA tamaño / interlínea | 63 / 62 | 45 / 46 |
| PEREIRA tamaño / interlínea | 86 / 85 | 62 / 61 |
| Frase: tamaño / interlínea / ancho | 28 / 47 / 810 | 20 / 34,5 / 584 |
| Separación nombre → frase | 15,8 | 11,4 |
| Separación frase → barra Especialidades | **82** | **57,3** |
| Barra: relleno | 40 16 32 16 | 29 12 24,4 12 |
| Título "Especialidades" | 25 / lh 30 | 18 / lh 22 |
| Textos de la barra | 18 / 24 | 13 / 17 |
| Foto (anclada al hero completo) | left 39,5 %, width 60,5 %, top 0 | igual |

Móvil: hero 812, nombre 27 / 36,6, frase 14 / 24,4 (Manrope), barra 2×2 de 333 px, margen frase → barra 29, foto 340 px de alto recortada (imagen al 146 %, izq. −26 %, arriba −13 %).

### Tarjeta blanca
| | Desktop | Laptop |
|---|---|---|
| Portada → tarjeta y bajo la tarjeta (relleno del fondo) | 79 | 57 |
| Ancho de la tarjeta | 1500 | 1081 |
| Relleno tarjeta (arriba / lados / abajo) | 79 / 80 / 81 | 57 / 58 / 58 |
| Columnas: texto · separación · datos | 801 · 78 · 460 | 578 · 56 · 331 |
| Datos: relleno izquierdo (tras el borde dorado) | 78 | 56 |
| Datos: relleno arriba / abajo | 7 / 8 | 5 / 6 |
| Margen superior de la columna de datos | 1 | 1 |
| Datos fijos (sticky) a | 80 | 58 |
| Ícono del título (alto) | 36 | 26 |
| Título H2 (tamaño / interlínea) | 26 / 31 | 19 / 23 |
| Título → texto (margen inferior del título) | 25,4 | 18,2 |
| Texto → línea (margen sup. del divisor) | 24,7 | 17,7 |
| Línea → título siguiente (margen sup. del título) | 50 | 36 |
| Texto CV (tamaño / interlínea) | **17,8** / 33,6 | **12,8** / 24,2 |
| Sangría de texto y listas | 61 | 44 |
| Listas: interlínea · separación entre ítems | 27,6 · 20 | 19,9 · 14,2 |
| Cifras (tamaño / interlínea) | 37 / 42,4 | 27 / 30,6 |
| Etiquetas de cifras | 17,8 / 21,7 | 12,8 / 16,2 |
| Separación entre cifras | 38,5 | 27,4 |

Móvil: tarjeta ancho 100 % con 17 de margen, radio 17, relleno 44/17; H2 22,7 (Sora); texto 15,7 / 29,6; listas 15,7 / 24,4 con separación 14,8; datos dentro de Resumen tras el texto con borde dorado de 2 px, cifra 32,3 / 38,8, etiqueta 15,7 / 19,2, separación 24,4, **sin sticky**.

**Por qué 17,8 y 12,8 y no 18 y 13:** con 18 / 13 el texto es un poco más ancho que en Figma y se parte una línea de más en las listas. Con 17,8 / 12,8 las alturas de las listas coinciden con el Figma. Además se da 12 px (desktop) / 8 px (laptop) de holgura a la derecha de las listas con margen derecho negativo, para que la primera lista de Cargos conserve las mismas líneas que el diseño.

---

## 4. Estructura de la plantilla Elementor (8 contenedores)

```
ak-dp-hero (boxed, fondo imagen, overflow hidden)
 ├─ logo (imagen)
 ├─ DIANA (h1) · PEREIRA (h1)
 ├─ ak-dp-lead (texto)
 ├─ ak-dp-esp (contenedor barra Especialidades)
 │    ├─ ak-dp-esp-t (título "Especialidades", absolute sobre el borde)
 │    └─ 4 × ak-dp-ico-N (caja de imagen sin imagen; ícono = ::before CSS)
 ├─ ak-dp-foto (imagen anclada al hero)
 └─ 3 × ak-dp-fuentes (textos ocultos que cargan Sora y Manrope)
ak-dp-fondo (fondo #F3F6FB, centra la tarjeta)
 └─ ak-dp-card (blanca, sombra, radio 20; width 1500 / 1081, content_width full)
      └─ ak-dp-cols (fila; tablet/mobile en columna)  ← envuelve main + side
           ├─ ak-dp-main (texto)
           │    ├─ ak-dp-h2 (caja de imagen: título + ícono)  ×4
           │    ├─ ak-dp-resumen (texto)
           │    ├─ ak-dp-datos-m (cifras, SOLO móvil, dentro de Resumen)
           │    ├─ ak-dp-linea (divisor) ×3
           │    └─ ak-dp-lista (lista de iconos) ×3
           └─ ak-dp-side (columna derecha: borde dorado 1 px, sticky, 3 cifras)
```

Convenciones: clases `ak-<proyecto>-…` en `css_classes` del contenedor o en el campo "Clase CSS" del widget; CSS en "CSS personalizado" con `selector`; sin "Ocultar en…" (si algo no va en un dispositivo se oculta con CSS de media query o se hace distinto por dispositivo).

Por qué `ak-dp-cols` envuelve a main + side: el **sticky de Elementor usa el borde exterior del padre** (ignora su relleno). Si el padre es la tarjeta, la columna se pega abajo al borde de la tarjeta sin dejar el relleno inferior. Con un contenedor interior sin relleno, el relleno de abajo queda fuera y la columna se detiene donde termina el texto.

**Columna derecha siempre fija (sticky)** en desktop y laptop (regla permanente del usuario): `sticky: top`, `sticky_on: [desktop, laptop]`, `sticky_parent: yes`, `sticky_offset` = distancia de reposo (80 desktop / 58 laptop). No sticky en tablet/móvil.

---

## 5. Imágenes e íconos: cómo se cargan

- **Fondo, logo y foto** son `webp` subidos por el usuario a la Biblioteca de medios (URL `https://grupogoberna.com/wp-content/uploads/AAAA/MM/…` + id). El JSON las referencia por URL+id (`image: {url, id, source:'library'}`). Si cambia el ponente, hay que pedir al usuario que suba las nuevas y dar las URLs/ids, o dejarle la lista de archivos de `imagenes/` para subir.
- **Íconos de la barra Especialidades, de los títulos H2 y las viñetas** van como **fondo CSS con data URI webp** dentro del `custom_css` del widget (`::before`). No subirlos a la Biblioteca y no usar widgets de imagen con SVG/data URI: Elementor no los muestra.
- Diana: `hero-fondo-capitolio.webp` (4096×2304, q90, 471 KB), `diana-pereira.webp` (1656², 179 KB), `logo-goberna.webp` (892×228, 44 KB).
- Fuentes: Montserrat (nombre, títulos, cifras), Open Sans (cuerpo), Sora y Manrope (solo móvil). Sora y Manrope se cargan con 3 widgets de texto ocultos (`display:none`, clase `ak-dp-fuentes`) porque Elementor solo carga las fuentes que algún widget usa.

---

## 6. Errores de Elementor ya vistos (y su causa) — leer antes de generar el JSON

| Síntoma | Causa | Solución |
|---|---|---|
| "Invalid Content In File" al importar | Se importó el JSON de datos, no la plantilla | Importar `<slug>.json` (plantilla). |
| "This source does not support import" | Importar desde la pestaña Cloud | Plantillas → **Plantillas guardadas** → Importar desde el equipo. |
| El borde dorado / clase no se aplica en un contenedor | La clase estaba en `_css_classes` | En contenedores la clase va en **`css_classes`**; `_css_classes` es de widgets. |
| **Un margen/relleno de contenedor "no se ve"** | Se usó `_margin` / `_padding` | En contenedores: **`margin` / `padding`**. `_margin`/`_padding` son de widgets. (Esto hizo perder varias iteraciones con la barra de Especialidades.) |
| Tarjeta anidada a pantalla completa (fondo, sombra) | Contenedor anidado con `content_width: boxed` | `content_width: full` + `width` en px, dentro de un padre `flex_align_items: center`. |
| Íconos en gris o ausentes | Elementor ignora SVG y data URI en widgets de imagen | Íconos como fondo CSS con data URI webp (sección 5). |
| Foto a un lado equivocado | Posicionamiento absoluto con ancla incorrecta | Anclar al ancho completo del hero: `left:39,5%; width:60,5%; top:0`. |
| Contenido de laptop pegado al borde izquierdo | En el editor la vista Laptop mide el **ancho de la ventana** (p. ej. 1010 px), no 1366; el ancho fijo de 1081 px no cabía | En la portada de laptop usar `vw` (px / 13,66) y `em` para el interlineado; copiar los px a tablet para que no cambie. Ancho del contenido de laptop como **79 %**. |
| Borde dorado cruzado por el título "Especialidades" | El recorte con `mask-composite` se pierde al redefinir `mask` en otro breakpoint (el shorthand reinicia el composite) | Usar **`clip-path: polygon(...)`** para abrir el hueco: `polygon(0 0,Xpx 0,Xpx 3px,X+Wpx 3px,X+Wpx 0,100% 0,100% 100%,0 100%)`. |
| Texto del título más arriba que el ícono (caja de imagen) | Elementor pone `margin-bottom:10px` al título de la caja de imagen | CSS: `selector .elementor-image-box-title{margin:0 !important}` y ocultar `.elementor-image-box-description`. |
| Columna sticky pegada al borde inferior de la tarjeta | Sticky usa el borde exterior del padre | Contenedor interior `ak-dp-cols` (sección 4). |
| Interlineado en `vw` ignorado | El control de interlineado no siempre acepta `vw` | Usar `em` (proporción lh/tamaño) en laptop; px en las demás. |
| Saltos de línea distintos al Figma | Texto 18 / 13 px un poco más ancho que el de Figma | Tamaños 17,8 / 12,8 + holgura derecha en listas. |

Valores en Elementor: tamaños con `{'unit':'px','size':N,'sizes':[]}`; márgenes con `{'unit':'px','top':'N','right':'N','bottom':'N','left':'N','isLinked':false}` (números como texto). Claves por dispositivo con sufijo `_laptop`, `_tablet`, `_mobile` (desktop sin sufijo). Los contenedores usan `flex_gap` `{'column','row','isLinked','unit'}`.

---

## 7. Técnicas de CSS que se usan

- **Borde de la barra "Especialidades" con hueco bajo el título:** `::before` del contenedor con `border:1px solid #D6A752; border-radius:8px; inset:0` + `clip-path` que abre una franja de 3 px arriba entre X y X+W (desktop 30/210, laptop 22/151, móvil 18/100). El título es un widget con `position:absolute !important; top:-15px; left:41px` (desktop; laptop −11/30; móvil −7/25).
- **Íconos como fondo:** `selector .ak-dp-ico-N .elementor-image-box-wrapper::before{content:"";display:block;width:..;height:37px;margin:0 auto 9px;background:url(data:image/webp;base64,…) center/contain no-repeat}` con medias queries para laptop y móvil. Lo mismo en `.elementor-image-box-wrapper::before` de los títulos H2 (alineados al centro en desktop/laptop, arriba en móvil) y en `.elementor-icon-list-item::before` para las viñetas.
- **Portada escalable en laptop:** en el rango 1025–1366 los valores van en `vw`; el bloque CSS correspondiente va en `@media (min-width:1025px) and (max-width:1366px)`, y un bloque `@media (max-width:1366px)` anterior conserva los px (para tablet).
- **Ocultar/mostrar por dispositivo sin "Ocultar en…":** `ak-dp-datos-m` oculto con CSS en desktop y visible en móvil; `ak-dp-side` oculto en móvil.
- **Párrafos sin margen inferior:** `selector .ak-dp-resumen p, selector .ak-dp-dato p{margin:0}`, para que el espacio entre bloques sea el calculado.

---

## 8. Cómo verificar el Artifact contra el Figma (evita iterar)

1. Servir `dianapereira.html` en local (`python -m http.server` en una carpeta) y abrirlo con Playwright con viewport **1366** (modo laptop) y **1920** (modo desktop).
2. Con `evaluate` medir `getBoundingClientRect()` de: hero, logo, h1, lead, `.esp-b`, tarjeta, cada `.sh` (título), `.sec p`, cada `ul`, `.side`, cada `.stat`.
3. Comparar contra Figma:
   - Laptop: posiciones absolutas = Figma 1366 literal.
   - Desktop: Figma × 0,987.
4. Tolerancias razonables: ≤2 px en posiciones, ≤1 línea de diferencia en listas. Alturas de las listas (laptop): 108,5 / 128,5 / 188,5; (desktop ×0,987): 150 / 177,7 / 260,6.
5. Comprobar que el centro del ícono coincide con el centro del título en los 4 H2.
6. Para móvil: viewport 375 y comparar con el frame móvil escalado ×0,872.

El modo **"Ver widgets"** del Artifact lista cada widget con su fuente, tamaño y valor de Figma; sirve para que el usuario valide y para derivar el JSON.

---

## 9. Reutilizar `gen_final.py` para otro ponente

1. Copiar `_plantilla-cv-ponente/` o trabajar sobre su copia.
2. Cambiar al inicio: `OUT` (carpeta del ponente), `IMG` (URLs e ids de la Biblioteca de medios del nuevo ponente), y los textos (nombre, frase, especialidades, resumen, cargos, formación, aportes, cifras).
3. Íconos: renderizar los SVG nuevos a `iconos-webp/` y actualizar `esp_items`, `HEAD_ICON` y `LI` (nombre, ancho, alto).
4. Si las medidas del Figma del nuevo ponente cambian, actualizar las tablas de la sección 3 (no inventar: medir con `get_metadata`).
5. Ejecutar `python gen_final.py` → escribe `<OUT>\<slug>.json`. Abrirlo y comprobar tamaño (~160 KB) y que no queden referencias a `.svg`.
6. Reconstruir el Artifact con `tpl.html` + `build.py` (poner antes los assets del nuevo ponente en `a/`).
7. Guardar siempre en la carpeta del ponente: `.json`, `-datos.json`, `imagenes/`, `iconos/`, `iconos-webp/`.

Notas del generador:
- `R(...)` pone un valor por dispositivo (desktop, laptop, tablet, mobile). Con la bandera global `VW = True` convierte los valores de laptop a `vw` y copia los px a tablet.
- `typo(...)` fija fuente, tamaño e interlineado por dispositivo (con `VW` el interlineado de laptop sale en `em`).
- `container(settings, elements, classes, css)` y `widget(tipo, settings, classes, css)` crean los nodos; en `widget` las clases van en `_css_classes`, en `container` en `css_classes`.
- Las funciones `gapmask(x, w)` y `gapmask_vw(x, w)` generan el `clip-path` del borde con hueco.

---

## 10. Reglas permanentes del usuario (resumen)

- Cualquier curso, programa o CV de docente se guarda en `cv-ponentes` con carpeta propia + `.json` + `imagenes/` + `iconos/` (+ `iconos-webp/`).
- Columna derecha (3 estadísticas, borde dorado a la izquierda de 1 px) **siempre fija (sticky)** en desktop/laptop, solo dentro de su sección.
- Ver el Artifact primero y esperar aprobación antes de dar JSON.
- No crear imágenes o íconos inventados "para saber qué reemplazar": usar los reales del Figma.
- Pocos contenedores, widgets nativos, clases `ak-…`, mobile al 87 %, nada de "Ocultar en…".
- El contenido de las landings sale de la **hoja de ponentes (Google Sheet)** — una pestaña por ponente, se lee como CSV.
- No guardar ni usar tokens de Figma pegados en el chat.

---

## 11. Checklist final antes de dar el JSON

- [ ] Artifact aprobado por el usuario.
- [ ] Medidas verificadas con Playwright a 1366 y 1920.
- [ ] En el JSON: contenedores con `margin`/`padding` (no `_margin`/`_padding`) y `css_classes`.
- [ ] Sin SVG ni data URI en widgets de imagen; íconos como fondo CSS.
- [ ] Portada laptop en `vw`, tablet con px.
- [ ] `ak-dp-cols` envolviendo main + side; sticky con offsets 80/58 (o los del nuevo diseño).
- [ ] Imágenes `.webp` < 500 KB en `imagenes/`; lista de lo que el usuario debe subir a la Biblioteca de medios.
- [ ] Ruta del JSON entregada al usuario con instrucciones: Plantillas → Plantillas guardadas → Importar.
