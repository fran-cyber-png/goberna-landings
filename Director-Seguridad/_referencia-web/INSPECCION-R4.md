# Inspección ronda 4 — frame 6112:373 (1920 × 11253)

Método: render 1:1 contra `web-completa-1920.png`. Las posiciones de los fondos salen del CSS publicado de la web (`post-93575.css`), no de estimaciones. y = desde el borde superior de la sección.

**Ya están bien**: cabecera, hero (botones, iconos y brochure), barra, El diploma, plan de estudios, botones del CTA, VER TRAYECTORIA, flechas del carrusel, botón de certificación, formulario de Inversión, FAQ (título, párrafo, tarjetas y botones), play de Goberna, puntos y rutas del mapa, línea "Inteligencia • …", logos de la Alianza, fila legal y texto del pie.

## 1. Inversión (6112:937) — ERROR NUEVO
- **El precio se rompió**: "199" se parte en dos líneas ("19" arriba y "9" abajo) porque su caja es demasiado angosta. Debe ir en una línea: "199" en x ≈ 255–448, centrado en y 357–445; "$" en x 211–250, y 377–425; "USD" en x 470–563, y 385–415.

## 2. Fondos: franjas lisas que no están en la web
Al bajar las imágenes quedaron franjas de color liso arriba que en la web no existen. Estas son las colocaciones exactas según el CSS de la web. Los archivos están en `_referencia-web\assets-fondos\` y `assets-cta\`:

| Sección | Imagen | CSS de la web | Colocación en el Figma (relativa a la sección o al banner) |
|---|---|---|---|
| 08 CTA (banner 1500 × 346) | `banner-proxima-edicion-director-4.webp` (1520 × 347) | cover, center right | **x −15,6, y 0, 1515,6 × 346**. Encima, degradado horizontal #060606 al 100 % en el borde izquierdo → 0 % al 55 % del ancho |
| 06 Experiencia (1920 × 953) | `war-room-fondo-director-1.webp` (1920 × 1027) | 100 % de ancho, top center | **x 0, y 0, 1920 × 1027** (lo que sobra abajo se recorta). Hoy hay una franja negra de 40 px arriba |
| 15 Alianza (1920 × 704) | `footer.jpg` (1600 × 466) | cover, center right | **x −497, y 0, 2417 × 704** |
| 04 Metodología (1920 × 693) | `capitolio-10-1-1.webp` (1428 × 1287) | 705 px de ancho, bottom right | **x 1215, y 58, 705 × 635**. Hoy está más grande y más arriba |
| 14 FAQ (1920 × 820) | `capitolio-10-2.webp` (1428 × 1287) | 521 px de ancho, bottom left | **x 0, y 350, 521 × 470**. Hoy está a 500 × 460 en y 360 |

Nota: lo que ronda 3 midió como "40 px más arriba" en Experiencia venía de que la imagen estaba centrada en vertical. En la web va pegada arriba (top), sin franja.

## 3. Presencia (6112:563): etiquetas del mapa
- Los puntos y las rutas ya coinciden. Las etiquetas no:
  - En la web van **en MAYÚSCULAS**: el SVG lleva `text-transform: uppercase`.
  - Fuente: **Barlow 600, 20 px** (31 px × 0,645), espaciado 0,2.
  - Quedaron ~12 px más abajo que en la web.
  - El contorno oscuro #060606 de ~4 px detrás del texto sí está en la web; no hace falta quitarlo.
- Posiciones en la web (x inicial, o x final para CARIBE y PANAMÁ, y línea base):

| Etiqueta | x | Línea base y |
|---|---|---|
| MÉXICO | 1222 | 198 |
| CARIBE | termina en 1400 | 176 |
| REP. DOMINICANA | 1507 | 203 |
| PANAMÁ | termina en 1360 | 289 |
| COLOMBIA | 1465 | 334 |
| PERÚ | 1449 | 452 |
| BRASIL | 1652 | 485 |
| CHILE | 1484 | 669 |
| ARGENTINA | 1607 | 679 |

## 4. Alianza (6113:25): contactos
- Las filas de datos de **México, Perú, Ecuador, Bolivia y Brasil** están 14 px más abajo que en la web. En la web, sus centros van en y 431 (teléfono), 461 (correo) y 490 (web). Solo **Estados Unidos** baja 15 px (446 / 476 / 505), porque su título ocupa 2 líneas.
- El título "Estados / Unidos" lleva interlineado de 22 px (líneas en y ≈ 387 y 409). Hoy tiene ~28.
- Direcciones: en la web el interlineado es ~22,5 px (p. ej., Ecuador en y 519 / 541 / 564 / 586); hoy, ~17.
- Iconos de contacto: en la web miden ~14 px de alto; hoy el del teléfono mide ~22 y se ve grueso.
- El icono de "Libro de Reclamaciones" en la web es diminuto (~8 px); hoy mide ~16.

## 5. Pie (6113:65): iconos de redes
- Los 7 deben medir lo mismo, ~16 px de alto, centrados en y 38. Hoy facebook es mucho más grande (~28 px) y youtube más chico y ~4 px más arriba.

## Detalle opcional
- Play de Goberna: en la web el círculo lleva un anillo oscuro semitransparente de ~8 px alrededor. Hoy apenas se nota. No bloquea el cierre.
