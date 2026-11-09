# Cierre de inspección — Figma Director de Seguridad vs. web final

**Resultado: aprobado.** El frame `DIRECTOR-SEGURIDAD-WEB-1920` (6112:373, archivo UtWCaOFmeJXaBbp8BoA865, página Desktop) coincide con la web publicada (https://grupogoberna.com/diploma-de-elite-internacional-de-seguridad/, plantilla 93575) sección por sección, sin textos desbordados ni capas fuera de su sección.

## Método
- Render del frame a 1:1 (1920 × 11253) comparado con `web-completa-1920.png` (recortada a 11253, con la Alianza recapturada por WP), sección por sección: lado a lado, superposición y diferencia por píxel.
- Fondos e imágenes: colocación tomada del CSS publicado (`post-93575.css`) y verificada con un ajuste de desplazamiento contra la captura.
- Textos: filas de tinta medidas en ambas imágenes.
- 6 rondas: R1 (diferencias que no estaban en el reporte), R2–R6 sobre el frame nuevo. Detalle en `INSPECCION-R2.md`, `R3`, `R4` y en los mensajes de las rondas 5 y 6.

## Diferencia final por sección (media absoluta por píxel, 0–255)
| Sección | Dif. | Nota |
|---|---|---|
| 01 Cabecera | 1,7 | |
| 02 Hero | 5,7 | La imagen de fondo coincide al píxel; la diferencia viene del suavizado del texto grande |
| 03 Barra de datos | 2,5 | |
| 04 Metodología | 3,4 | Capitolio en su posición exacta |
| 05 El diploma | 3,5 | |
| 06 Experiencia estratégica | 3,4 | Fondo en su posición exacta |
| 07 Plan de estudios | 1,8 | |
| 08 CTA | 1,8 | Imagen con diferencia 0 |
| 09 Docentes | 13,2 | **Esperado**: la captura de la web salió a mitad del carrusel. El Figma muestra el estado inicial acordado (Francisco López, Gonzalo Catanzariti, Eduardo Velandia; 1.er punto activo). Título, tarjetas, flechas y puntos coinciden |
| 10 Presencia internacional | 3,0 | El halo de los puntos del mapa en la web es una animación (pulso) |
| 11 Certificación | 2,7 | |
| 12 Inversión / Admisión | 1,4 | |
| 13 Experiencia Goberna | 1,4 | |
| 14 Preguntas frecuentes | 2,6 | |
| 15 Alianza estratégica | 6,4 | Filas de contacto a ±1 px; la diferencia restante viene del suavizado de Lato |
| 16 Pie | 3,5 | |

## Decisiones tomadas durante la inspección
- Alto del frame: 11253 (la franja blanca bajo el pie de la captura original no era de la plantilla; confirmado por WP).
- Alianza: empieza en y 10460 y mide 704 (recaptura de WP).
- El rectángulo gris de los botones "Hablar con un asesor" no se dibuja: es una regla `a.flag::before` del CSS adicional del sitio, ajena a la plantilla (confirmado por WP).
- Plan de estudios: solo se ven los módulos 01–03, igual que en la web.
- CTA: sin degradado. En el escritorio la opacidad de la capa es 0; el 0,6 es solo para móvil.

## Material que queda en `_referencia-web\`
- `assets-alianza\`: logos (escudo, San Marcos, GO Social Suite, CCL) y banderas.
- `assets-fondos\`, `assets-cta\`, `assets-mapa\`: fondos, banner del CTA y SVG del mapa originales de la web.
- `iconos-fa5\`: iconos de Font Awesome 5.15.4 que usa la web.

## Pendiente fuera de la inspección
- El frame viejo `DIRECTOR-SEGURIDAD-1920X1080` (4010:52) sigue en la página sin cambios. Diseño consultó si reemplazarlo o eliminarlo; lo decide WP o el usuario.
