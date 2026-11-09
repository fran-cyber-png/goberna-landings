# Reporte para Diseño: el Figma debe coincidir con la web final

**Referencia (manda la web):** https://grupogoberna.com/diploma-de-elite-internacional-de-seguridad/ (plantilla Elementor 93575, JSON final `Downloads\jet-woo-builder-93575-2026-10-16.json`). Esta plantilla será la base de las próximas landings, por eso el Figma `DIRECTOR-SEGURIDAD-1920X1080` (4010:52, archivo UtWCaOFmeJXaBbp8BoA865) tiene que quedar igual a ella.

**Material de referencia (todo a 1920 px de ancho, 1:1):**
- Página completa: `C:\Users\Consultoría\Documents\Director-Seguridad\_referencia-web\web-completa-1920.png` (1920 × 11253)
- Captura por sección: `_referencia-web\secciones\01-header.png` … `16-footer.png`
- Medidas exactas por texto (x, y, ancho, alto, fuente, tamaño, peso, interlineado, espaciado, color): `_referencia-web\ESPEC-WEB-1920.md`
- Figma actual renderizado (para comparar): `_referencia-web\figma-actual-1920.png`
- Imágenes de la web: todas en `https://grupogoberna.com/wp-content/uploads/2026/10/<archivo>` (nombres abajo).

## Cambios globales
1. **Ancho de contenido:** en la web el contenido va de x = 210 a x = 1710 (1500 px). En el Figma va de 200 a 1720 (1520 px). Ajustar márgenes de todas las secciones.
2. **Alto total y de cada sección:** la web mide 11253 px (termina en el borde inferior del footer). Alturas y posiciones (y) de cada sección:

| Sección | y | alto |
|---|---|---|
| Header | 0 | 90 |
| Hero (debajo del header, no detrás) | 90 | 911 |
| Barra de datos (se monta 113 px sobre el hero) | 888 | 189 |
| Metodología | 1076 | 693 |
| El diploma | 1770 | 717 |
| Experiencia estratégica | 2487 | 953 |
| Plan de estudios | 3439 | 961 |
| CTA próxima edición | 4400 | 443 |
| Docentes | 4843 | 1066 |
| Presencia internacional | 5910 | 950 |
| Certificación | 6860 | 1025 |
| Inversión / Admisión | 7885 | 938 |
| Experiencia Goberna | 8823 | 818 |
| Preguntas frecuentes | 9641 | 820 |
| Alianza estratégica | 10460 | 704 |
| Footer | 11164 | 89 |

## Cambios por sección
1. **Header:**
   - Menú: METODOLOGÍA · DIPLOMA · MÓDULOS · DOCENTES · CERTIFICACIÓN · INVERSIÓN (hoy dice "ABOUT" ×6). Inter 15/500, espaciado 0.9, #15262F, centrado entre logo y botón (empieza en x = 565).
   - Botón "INSCRÍBETE AHORA": 256 × 56, x = 1454, radio 32, Inter 17/400.
2. **Hero:**
   - Empieza debajo del header (y = 90, alto 911).
   - Subtítulo: Inter 20/400, interlineado 32, espaciado 2.6.
   - Botones: 340 × 68.
   - Textos y posiciones según ESPEC.
3. **Barra de datos:**
   - Los 4 valores (ONLINE, 30 DE NOVIEMBRE, 19:00 HRS. GMT-5, 10 MÓDULOS) en Inter 16/400, espaciado 2.4, #15262F. En el Figma "19:00 HRS. GMT-5" sigue más grande.
   - Etiquetas en #808591.
   - "USD $199": 25 px.
4. **Metodología:**
   - Alto 693.
   - En lugar del video "Goberna Escuela" va una **imagen** de 720 × 405 (16:9) en x = 990, con esquinas de 17 px: `Frame-252.webp` (Director de Seguridad).
   - Título Montserrat 50/700 en **2 líneas**: "De gestionar la seguridad / a dirigirla estratégicamente".
5. **El diploma:**
   - Etiqueta "EL DIPLOMA" (hoy dice "EL PROGRAMA").
   - Título Montserrat 40/700.
6. **Experiencia estratégica:**
   - Los **4 puntos de la línea son sólidos #FFBB03** (hoy solo el primero).
   - Contenido desde x = 310. Columnas de etapas en x = 310 / 635 / 960 / 1285, de 295 de ancho.
   - Título 54/700. Alto 953.
7. **Plan de estudios:**
   - Título de cada módulo: Montserrat **23**/600, interlineado 29.
   - Alto 961.
   - Resto según captura y ESPEC.
8. **CTA próxima edición:**
   - Banner de x 210 a 1710.
   - Título 44/700.
   - Botones 340 × 68.
9. **Docentes:**
   - **6 docentes, en este orden:** Francisco López (España), Gonzalo Catanzariti (Argentina), Eduardo Velandia Becerra (Colombia), Andrés Peñaranda (Colombia), Mg. Eduardo de la Torre (Colombia), Daniela Galván (Argentina).
   - **Sin biografía.**
   - Especialidad: Barlow 15/200, blanco al 62 %.
   - Nombre: Barlow 21/700.
   - "VER TRAYECTORIA": Inder 13, espaciado 1.3, dorado.
   - Se ven 3 tarjetas de 384 × 542, separadas 50 px (la primera en x = 334).
   - Flechas de 56 px en x = 168 y x = 1696.
   - **6 puntos** de paginación.
   - Fotos de la web: `francisco-lopez.webp`, `gonzalo-catanzariti-1.webp`, `Frame-193.webp` (Eduardo Velandia), `card-andres-penaranda-1-1-1-1.webp`, `card-eduardo-de-la-torre-1-1-1-1.webp`, `card-daniela-galvan-1-1-1-1.webp`.
   - Título Montserrat 48/700.
10. **Presencia internacional:**
    - El mapa es `mapa-asesor-animado-nombres.svg`: rutas punteadas con los nombres México, Caribe, Rep. Dominicana, Panamá, Colombia, Perú, Brasil, Chile y Argentina. Reemplaza el mapa de curvas de nivel.
    - Título 56/700. Etiqueta 22 px.
    - Cifras: 54/800. Sus etiquetas: 22 px, espaciado 2.42.
    - Alto 950.
11. **Certificación:**
    - La imagen del diploma es `Gemini_Generated_Image_j14jp9j14jp9j14j-1-1.webp` (dice "DIRECTOR DE SEGURIDAD"; hoy dice "Asesor Experto en Gestión y Entornos Presidenciales").
    - Columna de texto en x = 1045. Título 50/700.
    - Textos de las tarjetas: 20 px.
    - Botón "HABLAR CON UN ASESOR" (370 × 68) dentro de la tarjeta 2.
12. **Inversión / Admisión:**
    - **Izquierda:** el par de datos es "INICIO: 30 DE NOVIEMBRE" y "DURACIÓN: 10 MÓDULOS" (hoy dice "FACILIDADES: HASTA EN 4 CUOTAS").
    - **Nota bajo "PAGAR AHORA":** "Vacantes limitadas para garantizar una formación especializada." (hoy habla del War Room).
    - **Precio:** 120 px.
    - **Botones:** "PAGAR AHORA" y "ENVIAR" de 675 × 56.
    - **Formulario:** campos con textos de ejemplo:
      - Ej. María Pérez
      - Selecciona tu país
      - Ej. +51 999 999 999
      - Ej. Jefe de seguridad
      - nombre@correo.com
    - **Columna izquierda:** en x = 210.
13. **Experiencia Goberna:**
    - **Sin "VOCES" ni las 3 miniaturas** de testimonios.
    - Un solo cuadro de 598 × 598 en x = 310 con la imagen `Frame-252.webp` y el botón de play dorado (84 px) **centrado** en el cuadro.
    - Texto a la derecha desde x = 948.
    - Fondo #F2F4F7. Alto 818.
14. **Preguntas frecuentes:**
    - Fondo #DDE3EA con el capitolio (`capitolio-10-2.webp`).
    - Título 56/700.
    - Primera pregunta abierta. Alto 820.
15. **Alianza estratégica y footer:** hoy el Figma tiene un rectángulo "Footer" de 300 px. Reemplazarlo por los dos bloques de la web, según las capturas 15 y 16:
    - **Alianza (703 px):** escudo Goberna, Fundación San Marcos, GO Social Suite, CCL y los 6 países con sus contactos.
    - **Barra negra (89 px):** "Pagado por…" y redes sociales.

**Criterio de cierre:** cada sección del Figma superpuesta a su captura de la web debe coincidir en textos, tamaños, posiciones, imágenes y colores, sin textos desbordados ni capas fuera de su sección.
