# Inspección ronda 3 — frame 6112:373 (1920 × 11253)

Método: render 1:1 contra `web-completa-1920.png` (ya recortada a 11253 y con la Alianza recapturada), sección por sección. También busqué el desplazamiento de cada imagen de fondo. y = desde el borde superior de la sección.

**Ya están bien**: cabecera, barra de datos, El diploma (salvo detalle), plan de estudios (salvo detalle), Docentes (salvo flecha), Certificación (salvo botón), formulario de Inversión, título de FAQ, tarjetas y botones de FAQ, escudo, San Marcos, banderas, alto del frame y posiciones de las secciones.

## Material nuevo
- `_referencia-web\iconos-fa5\`: SVG oficiales de Font Awesome 5.15.4, los mismos que usa la web:
  - `arrow-right`: botones del hero, el CTA y certificación.
  - `long-arrow-alt-right`: VER TRAYECTORIA.
  - `arrow-left` / `arrow-right`: flechas del carrusel.
  - `download`: brochure.
  - `mobile-alt`, `paper-plane` (contorno), `globe`, `map-marker-alt`: contacto de la Alianza.
  - `address-book`: Libro de Reclamaciones.
  - `facebook-f`, `twitter`, `instagram`, `linkedin`, `youtube`, `vimeo`, `telegram-plane`: redes del pie.
- `_referencia-web\assets-mapa\mapa-asesor-animado-nombres.svg`: el mapa de la web, con sus etiquetas.

## 08 CTA (6112:504) — prioridad alta
- **"RESERVA TU VACANTE" se parte en 2 líneas** ("RESERVA TU / VACANTE"). Debe ir en una línea, con el texto en x 345–547 y la flecha en x 560–574.
- Imagen del banner: ya cubre el banner, pero está ~80 px más arriba que en la web y le corta la cabeza al hombre. En la web la cabeza se ve entera, con su parte superior en y ≈ 55 del banner. Bájala ~80 px, ampliándola si hace falta para que siga cubriendo.
- Subtítulo "Inicio: 30 de noviembre | …": está ~12 px más arriba que en la web y queda pegado al título.

## 14 Preguntas frecuentes (6112:978)
- El párrafo "Aquí encontrarás…" está **26 px más arriba** y queda pegado al título. En la web sus líneas empiezan en y ≈ 518 y 551; en el Figma, en 492 y 525.

## 12 Inversión (6112:937)
- Precio: el "$" va en **negrita (700)**; hoy es regular. Los tres elementos van **centrados en vertical**; hoy están alineados por abajo. En la web, "199" ocupa y 357–445, "$" y 377–425 y "USD" y 385–415.
- "USD" va ~22 px después del "199": en la web, "199" termina en x 448 y "USD" ocupa x 470–563. Hoy va pegado.
- Triángulo de PAÍS: en la web, x ≈ 1703; en el Figma, 1692.

## 10 Presencia internacional (6112:563)
- Los puntos siguen desplazados entre 10 y 20 px (Perú, Chile, Argentina y Brasil quedan más abajo; México, más a la derecha). Las **etiquetas quedan encima del punto**; en la web van a la misma altura que el punto, ~17 px a su derecha (Caribe y Panamá, a su izquierda).
- Recomendación: importar el SVG de la web (`assets-mapa\mapa-asesor-animado-nombres.svg`, viewBox 1222 × 1287) en **x 1036, y 59 de la sección, a 788 × 830**. Con eso coinciden los puntos, las líneas y las etiquetas (Barlow 600).

## 06 Experiencia estratégica (6112:441)
- El fondo (war room con el escudo) está **40 px más arriba** que en la web. Bájalo 40 px.

## 04 Metodología (6112:411)
- El fondo del capitolio sigue ~36 px más arriba y ~8 px más a la izquierda que en la web.
- Línea "Inteligencia • …": en la web cada punto lleva **~15 px de aire a cada lado** y la línea va de x 900 a 1399. En el Figma va de 928 a 1371: está más apretada.

## 13 Experiencia Goberna (6112:971)
- **El triángulo del play apunta hacia arriba a la izquierda** (está rotado) y no está centrado. Debe ser un ▶ que apunte a la derecha, #15262F, centrado en el círculo, con el halo oscuro alrededor (en el Figma no se ve).

## 15 Alianza (6113:25)
- La textura de fondo está **40 px más arriba** que en la web.
- CCL: el PNG tiene márgenes transparentes. Para que el logo visible quede en x 1218–1421, y 134–209 como en la web, el PNG va en **x 1194, y 124, a 252 × 95**. Hoy el logo visible ocupa x 1237–1401: más pequeño.
- GO Social Suite: con el mismo cálculo, el PNG va en **x 1030, y 118, a 150 × 102**, de modo que el logo visible quede en y 126–210. Hoy está ~12 px más abajo.
- Contactos:
  - Faltan los iconos (archivos en `iconos-fa5`, dorados, ~14 px): icono en la x de la columna y texto en la columna + 22.
  - En la web la primera fila de datos va en y ≈ 431; en el Figma, en 452. Las filas van cada ~30 px.
  - En la web el texto es Lato ~14 px y las direcciones se cortan en ~160 px de ancho (4 líneas en EE. UU. y Ecuador). En el Figma el texto es más grande y ancho.
  - "Estados Unidos" va en 2 líneas ("Estados / Unidos").
- "Libro de Reclamaciones" lleva a la izquierda el icono `address-book`.

## 16 Pie (6113:65)
- Faltan los 7 iconos de redes (en `iconos-fa5`), blancos, de ~18 px, en y ≈ 38. Centros: x 1228 / 1274 / 1320 / 1366 / 1413 / 1459 / 1506.

## Iconos pendientes (con los SVG de iconos-fa5)
- Hero: flechas sólidas `arrow-right` en los 2 botones e icono `download` relleno en el brochure.
- CTA y certificación: `arrow-right` sólida. Certificación: el botón lleva una sombra suave.
- Docentes: `long-arrow-alt-right` ~20 px después del texto (en la web el texto termina y la flecha empieza 20 px después; hoy va pegada). Flechas del carrusel: `arrow-left` / `arrow-right` sólidas.
- Plan de estudios: `download` relleno en DESCARGAR BROCHURE.

## Detalles menores
- El diploma: las pestañas inactivas van en blanco al 75 % (hoy al 100 %); los chevrones, con trazo de 2 px (hoy más finos).
- Plan de estudios: el icono del grupo, más grande (~42 × 28, como en la web). Las tarjetas Aprenderás / Aplicarás llevan esquinas redondeadas (~8 px).

## No se pide
- El rectángulo gris a la izquierda del botón "HABLAR CON UN ASESOR" de certificación **no se dibuja**. WP confirmó que no es diseño: lo genera una regla "a.flag::before" del CSS adicional del sitio sobre los enlaces de WhatsApp. Ninguno de los tres botones "Hablar con un asesor" (hero, CTA, certificación) lo lleva en el Figma: solo texto + flecha.
