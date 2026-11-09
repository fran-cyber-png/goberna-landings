# Proceso de diseño en Figma — Landings de ponentes

Guía para producir y revisar las landings de ponentes (desktop, laptop y móvil) en Figma con dos sesiones de Claude Code coordinadas.

---

## 1. Roles

| Sesión | Rol | Hace | No hace |
|---|---|---|---|
| **Diseño-Ins** | Inspector / analista | Hace las preguntas al usuario, analiza Figma, redacta tareas, revisa entregas, devuelve observaciones, aprueba y reporta al usuario | No edita Figma |
| **Diseño-Eje** | Ejecutor | Ejecuta en Figma (`use_figma`, cargando antes el skill `/figma-use`) y manda un reporte detallado al terminar | No decide alcance ni criterios; pregunta antes de improvisar |

- Comunicación: `SendMessage` entre sesiones (`to: "Diseño-Eje"` / `to: "Diseño-Ins"`), con `notify_when_idle: true` al mandar tareas.
- Diseño-Ins itera las veces necesarias y avisa al usuario **solo con el resultado final aprobado**.
- Ninguna sesión toca frames fuera del alcance de la tarea.

---

## 2. Antes de mandar cualquier tarea: preguntas obligatorias al usuario

Diseño-Ins no envía nada hasta tener respuesta a:

1. **Objetivo**: qué se hace (versión nueva, corrección, ponente nuevo, etc.).
2. **Alcance**: qué ponente o ponentes. Por defecto, **uno piloto y luego el resto**.
3. **Fuente de contenido**: de qué frame salen textos e imágenes (normalmente el desktop del ponente).
4. **Modelo de estructura**: qué plantillas se siguen. Por defecto, **al pie de la letra** las plantillas hermanas del mismo breakpoint.
5. **Modo de edición**: duplicar y luego editar (recomendado) o editar el original.
6. **Ubicación**: dónde va el frame nuevo (por defecto, a la derecha del último frame de la página).
7. **Casos especiales del archivo**: frames duplicados a medio hacer, sobrantes o capas con datos viejos. Se revisan con `get_metadata` y se consulta qué hacer con cada uno.

---

## 3. Archivo de Figma

- **Archivo:** https://www.figma.com/design/VDnG8Ey0gIPBtCqea1kya9/Foro-Ponentes
- **fileKey:** `VDnG8Ey0gIPBtCqea1kya9`

| Página | ID | Ancho de frame | Separación entre frames | Nombre de frame |
|---|---|---|---|---|
| Desktop | `0:1` | 1920 | 100 px (x de 2020 en 2020) | `PROGRAMA-ALTA-DIRECCION-LANDING-DESKTOP – <Nombre>` |
| Laptop | `1:149` | 1366 | 100 px (x de 1466 en 1466) | `PROGRAMA-ALTA-DIRECCION-LANDING-LAPTOP – <Nombre>` |
| Mobile | `1:286` | 430 | 100 px (x de 530 en 530) | `PROGRAMA-ALTA-DIRECCION-LANDING-MOBILE – <Nombre>` |

- Los frames nuevos van **a la derecha del último frame**, con `y = 0` en Laptop y Mobile, y `y = 4249` en Desktop.
- `get_metadata` de una página completa excede el límite de tokens. El resultado se guarda en un archivo y se lee con Python (ver sección 8).

### Fuente de contenido: hoja de ponentes
- **Google Sheet (vigente desde 2026-10-16):** https://docs.google.com/spreadsheets/d/1ZmKvAhy4_9JQyknhlaG5tgePoWvf6LTB. La hoja anterior (`1ha8sOy…`) queda obsoleta. Hay una pestaña por ponente con nombre, titular, 00 Áreas de especialización (partidas por comas en varias celdas), 01 Resumen ejecutivo (en párrafos), 02 Experiencia y cargos principales, 03 Formación académica, 04 Aportes destacados y publicaciones y 05 Enlaces. La pestaña ÍNDICE es el gid 207101939.
- Es pública: se lee como CSV con `https://docs.google.com/spreadsheets/d/<id>/export?format=csv&gid=<gid>`. La lista de pestañas y sus gid sale de `/htmlview`.
- **Reglas para pasar de la hoja a Figma** (deducidas de Diana y confirmadas con el usuario):
  - Resumen e ítems se copian **textuales**, con los guiones y las comillas de la hoja.
  - **Especialidades:** se eligen **4** de entre las áreas de expertiz. Diseño-Ins las propone y el usuario aprueba.
  - **Estadísticas:** **3** datos (valor + descripción) derivados del contenido. Diseño-Ins los propone y el usuario aprueba. Se verifican contra la hoja (por ejemplo, no contar una tesis como "libro").
  - **Negritas:** en el resumen, la frase inicial; en cargos, el puesto (sin fechas); en formación, el grado o título; en aportes, los títulos de obras «…» y las frases clave. Diseño-Ins manda el texto ya marcado para que Diseño-Eje no improvise.
  - **Íconos de especialidades:** se reutilizan los del archivo (capitolio, libro, escudo, proceso, pin, global).
  - **Foto:** si el usuario la pone a mano, se deja una capa vacía "Foto <Nombre> (pendiente)" del mismo tamaño y posición.
  - **Fondo del hero:** el mismo de la serie (cielo + Capitolio).
  - Al reacomodar el desktop: no cambiar el alto de las líneas ("Línea 80" es una LINE vertical con alto 0 y rotación -90°).
  - Orden de trabajo para un ponente nuevo: **desktop primero** (es la fuente), luego laptop y luego móvil.
  - **Laptop:** se duplica el desktop aprobado, se mueve a la página Laptop y se escala con `rescale(1366/1920)` (factor 0.711458). Así lo hace la plantilla de Diana `408:2`: hero de 604.74 de alto, interlineado de listas 20 y paso entre ítems ≈ 34.23.

### Frames de referencia

| Ponente | Desktop | Laptop | Mobile |
|---|---|---|---|
| Diana Carolina Pereira Cardona | `395:2` | `408:2` | `409:2` ✅ |
| Omar Karim Chehade Moya | `437:2` ✅ | `444:2` ✅ | `447:2` ✅ |
| Daniela Galván | `450:2` ✅ | `452:2` ✅ | `453:2` ✅ |
| Francisco José López | `469:2` ✅ | `472:2` ✅ | `473:2` ✅ |
| Fernando Cocho Pérez | `487:2` ✅ | `490:2` ✅ | `492:2` ✅ |
| Andrés Peñaranda | `501:2` ✅ | `506:141` ✅ | `509:168` ✅ |
| Gonzalo Catanzariti | `532:2` ✅ | `535:2` ✅ | `538:2` ✅ |
| María Herrera | `267:2` | `338:1051` | `317:382` (plantilla de medidas móvil) |
| Diego Miranda Giménez de Azcárate | `184:734` | `338:179` | `316:2` (titular de 3 líneas) |
| Camilo Bello | `279:2` | `338:1281` | `317:718` (titular de 3 líneas) |
| Roberto Bazán | `157:2` | `338:2` | `312:6` |
| Nuño Rodríguez | `376:2` | `376:488` | `376:258` |

---

## 4. Especificación de la plantilla MÓVIL (430 px)

Medida sobre `317:382` (María Herrera) y comprobada en las demás plantillas.

### Hero — "Frame 5" (0, 0, 430 × 931)
- **Logo GOBERNA**: (24, 36), 120 × 30.6.
- **Nombre**: (24, 95). Nombre en dorado y apellido en blanco, en dos líneas. Montserrat ExtraBold 30.9 / 42.
- **Titular**: (24, 181), ancho 382, interlineado 28 (de 1 a 3 líneas). El alto crece hacia abajo; **nada más se mueve**.
- **Caja "Especialidades"**: siempre en **y = 298** (382 × 181). Etiqueta en (53, 270). La posición es fija aunque el titular tenga 3 líneas (como en Diego `316:2` y Camilo `317:718`).
- **Especialidades**: cuadrícula 2x2 con divisores verticales en x = 212.86. Las etiquetas se parten en las mismas líneas que en el desktop del ponente (por ejemplo "Prevención del / Ciberdelito"), centradas en su columna (x = 120 y x = 316); nunca en una sola línea larga que se acerque al divisor. Los íconos miden **23 px de alto**, en y ≈ 329 (fila 1) y ≈ 406.5 (fila 2), centrados en su columna. Los textos van en y = 357 y y ≈ 435. El orden es el del desktop, leído de izquierda a derecha y de arriba abajo.
- **Íconos**: se clonan del desktop del ponente (mismo vector) sin modificar los originales y se llevan a 23 px con `rescale()` (no `resize()`), para que el trazo escale en proporción.
- **Foto**: caja de **350 × 389 en (40, 542)**, en modo CROP o con imageTransform. **Nunca se estira la caja.**
  - Parte de arriba del pelo en **y ≈ 545–550** (casi pegada al borde superior).
  - Cabeza, del pelo al mentón: **≈ 150–160 px**.
  - Corte a la altura del pecho o la cintura alta.
  - Centro de la cara entre x ≈ 195 y 225.
  - Sin pixelado y sin deformación.

### Tarjeta blanca — "Frame 1" (20, 951, 390 de ancho)
- Contenido en "Frame 12": (20, 51), ancho 350.
- **Resumen ejecutivo** ("Frame 10"): título con ícono y texto en (20, 66), ancho 330, Open Sans 18 con interlineado 34 y las negritas del desktop.
- **Estadísticas** ("Datos"): **debajo del resumen**, 40 px después del texto. Son 3 bloques "Dato" (valor en Montserrat + descripción) con borde dorado a la izquierda. Estructura idéntica a `317:429`.
- **Separadores** ("Línea 81/82/83"): **50 px de aire arriba y abajo**.
- **Cargos principales y trayectoria / Formación académica**:
  - Lista en (19, y), ancho 331.
  - Cada "Item" lleva un "Viñeta" de 6 × 28 con una **elipse de 6 × 6 en (0, 11)**, más el texto en x = 16, ancho 315, interlineado 28.
  - **17 px entre ítems.**
- **Aportes destacados**:
  - Cada "Item" lleva un "Viñeta" de 18 × 34 con el **vector flecha de 18 × 18 en (0, 8)**, más el texto en x = 28, ancho 303, interlineado 34.
  - **17 px entre ítems.**
  - El título es **el del desktop del ponente**. Si es "Aportes Destacados y Publicaciones", ocupa 3 líneas (alto 99) y la Lista va en y = 128, como en Diego `316:2` y Omar `447:2`.
- La tarjeta cierra con el mismo padding inferior que la plantilla. El frame termina **20 px** debajo de la tarjeta. **El alto del frame se ajusta al contenido.**

### Reglas de texto
- Textos **idénticos** al desktop: ortografía, tildes, negritas por tramo, guiones (–) y comillas.
- En el titular móvil (Manrope) el carácter «|» se confunde con una «I»: poner esas barras en Open Sans Regular con el mismo tamaño e interlineado (Tarea 13).
- Los rangos de fechas y las palabras compuestas con guion (como "Fujimori-Montesinos") no se parten entre líneas: usar **word joiner U+2060** a cada lado del guion (`2010⁠–⁠2012`), en todas las apariciones.
- Íconos clonados: **clonar sin escalar** el original para conservar el grosor del trazo. Escalar un ícono detallado lo hace verse más fino.
- Al duplicar una plantilla, revisar qué contiene de verdad cada capa de imagen: los nombres pueden mentir (por ejemplo, `395:50` "FOTO DIANA" tiene la foto de María).
- Capas con nombres limpios: el texto lleva su contenido como nombre, y foto e íconos se llaman "Foto <Nombre>" e "Ícono <Especialidad>".
- **No deben quedar** capas, textos ni imágenes ocultas del ponente original del duplicado.

---

## 5. Flujo de una tarea

1. **Preguntas** al usuario (sección 2).
2. **Inspección** (Diseño-Ins): `get_metadata` de la página y el frame, y `get_screenshot` de la fuente y de la plantilla.
3. **Envío de la tarea** a Diseño-Eje con la plantilla de la sección 6.
4. **Ejecución** (Diseño-Eje): duplicar, rellenar y verificar con su propia captura.
5. **Reporte** (Diseño-Eje), con el formato de la sección 6.
6. **Revisión** (Diseño-Ins) con el checklist de la sección 7. Si hay observaciones, se manda una "REVISIÓN N" separada en APROBADO / CORRECCIONES [IMPORTANTE | MENOR | VERIFICAR].
7. Se repiten los pasos 4–6 hasta aprobar.
8. **Aprobación**: mensaje "TAREA N APROBADA" a Diseño-Eje y **reporte final al usuario** con el link al nodo, lo revisado, lo corregido y los pendientes fuera de alcance.
9. Se registra la tarea en la sección 9 de este archivo.

> Si llega un aviso de "idle" sin reporte, se toma una captura nueva **antes** de reclamar: puede que la captura anterior se haya tomado antes de que Diseño-Eje guardara los cambios.

---

## 6. Plantillas de mensajes

### Tarea (Diseño-Ins → Diseño-Eje)
```
TAREA N (de Diseño-Ins): <qué hacer, en una línea>.

ROLES: Diseño-Ins analiza y revisa; Diseño-Eje ejecuta en Figma y reporta. Si algo no está claro, pregunta ANTES de improvisar.
ARCHIVO: https://www.figma.com/design/VDnG8Ey0gIPBtCqea1kya9/Foro-Ponentes (cargar /figma-use antes de use_figma)
FRAME A TRABAJAR: <id, página, nombre, posición; si es duplicado o nuevo>
FUENTE DE CONTENIDO: <frame>; copiar textos, foto e íconos EXACTOS.
MODELO DE ESTRUCTURA: <plantillas hermanas>; seguir al pie de la letra (ver diseño/proceso-diseno-figma.md, sección 4).
PUNTOS CLAVE: <lista por sección>
NO TOCAR: <frames fuera de alcance>
CRITERIOS DE REVISIÓN: <lista>
REPORTE: a) node ID y alto; b) cambios por sección; c) plantilla usada y ajustes por contenido; d) dudas y decisiones propias; e) confirmación de que no se tocaron otros frames.
```

### Reporte (Diseño-Eje → Diseño-Ins)
```
TAREA N lista para revisión: <frame>.
a) ID, posición y alto final
b) Cambios por sección
c) Plantilla de medidas y diferencias de contenido que obligaron a ajustar algo
d) Dudas y decisiones tomadas por cuenta propia
e) Confirmación de que no se tocaron otros frames
```

---

## 7. Checklist de revisión (Diseño-Ins)

- [ ] **Contenido**: cada texto comparado contra el desktop (palabra por palabra, negritas, tildes, guiones).
- [ ] **Sin restos** del ponente original (buscar en metadata nombres o textos del duplicado).
- [ ] **Estructura**: el árbol de capas (Frame 5 / Frame 1 / Frame 12 / Datos / Lista / Item / Viñeta) coincide con la plantilla.
- [ ] **Medidas**: posiciones fijas (titular y = 181, caja de especialidades y = 298, foto (40, 542)), separadores 50/50, 17 px entre ítems, cierre de 20 px.
- [ ] **Foto**: encuadre comparado lado a lado con 3 plantillas (cabeza ≈ 150–160 px, pelo en y ≈ 548, cara centrada).
- [ ] **Íconos**: los del ponente, en el orden del desktop, con 23 px de alto y el mismo dorado.
- [ ] **Texto**: sin desbordes, cortes ni rangos partidos.
- [ ] **Comillas**: las « » y " " de la hoja se ven en la captura (no basta con el nombre de la capa: en la Tarea 3 los títulos de Aportes de Omar las habían perdido).
- [ ] **Otros frames intactos.**

---

## 8. Herramientas de verificación

**Capturas a tamaño real:** `get_screenshot` con `maxDimension` igual al alto del frame. Se descargan con `curl` al scratchpad.

**Comparación lado a lado (Python + Pillow):**
```python
from PIL import Image, ImageChops
import math
a = Image.open('nuevo.png').convert('RGB')      # frame en revisión
b = Image.open('plantilla.png').convert('RGB')  # plantilla hermana
step = 700
for i in range(math.ceil(max(a.height, b.height) / step)):
    c = Image.new('RGB', (a.width * 2 + 20, step), 'white')
    c.paste(a.crop((0, i*step, a.width, min(a.height, (i+1)*step))), (0, 0))
    c.paste(b.crop((0, i*step, b.width, min(b.height, (i+1)*step))), (a.width + 20, 0))
    c.resize((c.width * 2, c.height * 2), Image.LANCZOS).save(f'cmp{i}.png')

# ¿Cambió algo entre dos capturas del mismo frame?
print(ImageChops.difference(a, Image.open('anterior.png').convert('RGB')).getbbox())
```

**Metadata grande:** el resultado de `get_metadata` es un JSON `[{type, text}]`. Se lee así:
```python
import json, re
t = ''.join(x['text'] for x in json.load(open(ruta, encoding='utf-8')))
for l in t.splitlines():
    if re.match(r'^  <(?!/)', l): print(l[:200])   # frames de primer nivel
```

---

## 9. Registro de tareas

| # | Fecha | Tarea | Frame | Rondas | Estado |
|---|---|---|---|---|---|
| 1 | 2026-10-14 | Versión MOBILE de Diana Pereira (fuente: desktop `395:2`; modelo: `317:382`) | `409:2` | 2 (foto re-encuadrada 1.64x, rango de fecha sin cortes) | ✅ Aprobada |
| 2 | 2026-10-14 | DESKTOP de Omar Karim Chehade Moya (nuevo; duplicado de `395:2`, contenido de la pestaña gid 1502795368; foto pendiente, la pone el usuario) | `437:2` | 2 ("Fujimori-Montesinos" sin cortes, capa vacía sobrante borrada, capitolio a 37.9 px sin escalar) | ✅ Aprobada |
| 3 | 2026-10-14 | LAPTOP de Omar Karim Chehade Moya (duplicado de `437:2` escalado con `rescale(1366/1920)`; foto vacía pendiente en (634.62, 71.86), 589.09×532.88) | `444:2` | 2 (en Aportes faltaban las comillas « » de los 3 títulos de obras; se añadieron en negrita en `437:2` y `444:2`) | ✅ Aprobada |
| 4 | 2026-10-14 | MOBILE de Omar Karim Chehade Moya (duplicado de `409:2`, contenido de `437:2`; foto vacía pendiente de 350×389 en (40, 542)) y título "Aportes Destacados y Publicaciones" en `437:2` y `444:2` (en una línea) | `447:2` | 1 | ✅ Aprobada |
| 5 | 2026-10-14 | DESKTOP de Daniela Galván (nueva; duplicado de `437:2`, pestaña gid 1474253188; especialidades e íconos pin/global/escudo/proceso; foto pendiente) | `450:2` | 2 (Línea 80 había quedado con alto 291 en vez de 0) | ✅ Aprobada |
| 6 | 2026-10-14 | LAPTOP de Daniela Galván (`450:2` escalado con `rescale(1366/1920)`) | `452:2` | 1 | ✅ Aprobada |
| 7 | 2026-10-14 | MOBILE de Daniela Galván (duplicado de `447:2`, contenido de `450:2`) | `453:2` | 2 (etiquetas de especialidades largas en 2 líneas, con los cortes del desktop) | ✅ Aprobada |
| 8 | 2026-10-16 | DESKTOP de Francisco José López (nuevo; duplicado de `450:2`, hoja nueva gid 810927693; nombre FRANCISCO / LÓPEZ sin "José"; titular de 1 línea; especialidades Criminología (libro) / Investigación Privada (pin) / Consultoría de Seguridad (escudo) / Inteligencia Aplicada (proceso); foto pendiente) | `469:2` | 2 (libro de 32.46 alineado abajo en un contenedor de 35.17×36.52, `470:6`, sin escalar ni sacarlo del auto-layout) | ✅ Aprobada |
| 9 | 2026-10-16 | LAPTOP de Francisco José López (`469:2` escalado con `rescale(1366/1920)`; alto 2438.98) | `472:2` | 1 | ✅ Aprobada |
| 10 | 2026-10-16 | MOBILE de Francisco José López (duplicado de `453:2`, contenido de `469:2`; libro = contenedor `470:6` llevado a 23 px con rescale; alto 5767) | `473:2` | 1 | ✅ Aprobada |
| 11 | 2026-10-21 | DESKTOP de Fernando Cocho Pérez (nuevo; duplicado de `469:2`, hoja gid 1858143491, texto LITERAL con erratas y notas de fuente; nombre FERNANDO / COCHO; titular de 3 líneas con "Docente UNIR" en espacio de no separación; especialidades Metodología de Inteligencia (proceso) / Inteligencia Estratégica (global `451:6`) / Seguridad Nacional (capitolio `437:112`) / Ciberinteligencia (escudo), íconos en contenedores de 37.93 apoyados abajo; cifras +30 años / 4 Másteres / Fundador; foto vacía pendiente; alto 3230.14) | `487:2` | 2 (Línea 80 alargada a 313 para pasar 8 px los Datos; resumen en un solo bloque como `469:2`; "Docente UNIR" sin cortar; etiquetas de especialidades alineadas en y = 45.93) | ✅ Aprobada |
| 12 | 2026-10-21 | LAPTOP de Fernando Cocho Pérez (`487:2` escalado con `rescale(1366/1920)`; alto 2298.11; foto vacía en (634.62, 71.86), 589.09×532.88) | `490:2` | 1 | ✅ Aprobada |
| 13 | 2026-10-21 | MOBILE de Fernando Cocho Pérez (duplicado de `473:2`, contenido de `487:2`; titular de 3 líneas que acaba en 266; contenedores de íconos `489:2–5` llevados a 23 px con rescale; foto vacía de 350×389 en (40, 542); alto 5064) | `492:2` | 2 (en Manrope la «\|» del titular parecía una «I»: las 2 barras pasan a Open Sans Regular 16 / 28 sin cambiar el texto) | ✅ Aprobada |
| 14 | 2026-10-21 | DESKTOP de Andrés Peñaranda (nuevo; duplicado de `487:2`, hoja gid 1001048987, solo contenido de la hoja; ANDRÉS / PEÑARANDA; titular de 2 líneas; especialidades Operaciones de Información (proceso) / Inteligencia Estratégica (global) / Comunicación Estratégica (libro en contenedor de 37.93) / Seguridad y Defensa Nacional (escudo); cifras +25 años / Magíster / Consultor; listas 4/2/3; foto pendiente; alto 2482.14). El frame viejo oculto `184:369` (con restos de Evan Ellis) se deja como está. | `501:2` | 1 (capa del nombre renombrada a "Nombre") | ✅ Aprobada |
| 15 | 2026-10-21 | LAPTOP de Andrés Peñaranda (`501:2` escalado con `rescale(1366/1920)`; alto 1765.94; foto vacía `506:164`) | `506:141` | 1 | ✅ Aprobada |
| 16 | 2026-10-21 | MOBILE de Andrés Peñaranda (duplicado de `492:2`, contenido de `501:2`; titular de 2 líneas todo en Manrope; contenedores del desktop llevados a 23 px; foto vacía `509:180`; alto 3841) | `509:168` | 1 | ✅ Aprobada |
| 17 | 2026-10-21 | Daniela Galvan: textos LITERALES de la hoja en las 3 versiones (GALVAN / Galvan sin tilde, "Master" en Formación y en la cifra 3, Buenos Aires sin punto final, "Belgrano..") y Especialidades alineadas con contenedores (desktop 37.93 / etiquetas en 45.93; laptop 26.986 / 32.678; contenedores `513:2–9`). Editado en su sitio, sin cambios de alto. | `450:2`, `452:2`, `453:2` | 1 | ✅ Aprobada |
| 18 | 2026-10-22 | Omar Karim Chehade Moya: textos revisados contra la hoja (coinciden, sin cambios); Especialidades alineadas con contenedores (desktop 37.93 / etiquetas 45.93; laptop 26.986 / 32.678; `524:2–9`) e íconos renombrados (Lucha Anticorrupción, Gobernanza y Políticas Públicas). Mobile sin tocar. | `437:2`, `444:2` | 1 | ✅ Aprobada |
| 19 | 2026-10-22 | DESKTOP de Gonzalo Catanzariti (nuevo; duplicado de `501:2`, hoja gid 158174956, literal salvo la «•» suelta al final de un cargo; GONZALO / CATANZARITI; titular de 2 líneas; especialidades Arquitectura de Ciberseguridad (escudo) / Investigación de Ciberdelitos (pin) / Informática Forense (proceso) / OSINT y SOCMINT (global); cifras Desde 2013 / Líder / 2 licenciaturas; listas 9/7/5; foto pendiente; alto 3540.14) | `532:2` | 2 (la etiqueta "Informática Forense y Evidencia Digital" salía en 3 líneas y desbordaba: el usuario la acortó a "Informática Forense") | ✅ Aprobada |
| 20 | 2026-10-22 | LAPTOP de Gonzalo Catanzariti (`532:2` escalado con `rescale(1366/1920)`; alto 2518.67) | `535:2` | 1 | ✅ Aprobada |
| 21 | 2026-10-22 | MOBILE de Gonzalo Catanzariti (duplicado de `509:168`, contenido de `532:2`; titular de 2 líneas; Datos en 2 líneas cada uno; listas 9/7/5; foto vacía `538:14`; alto 5609) | `538:2` | 2 (los 4 contenedores de íconos habían quedado sueltos en la raíz del frame: se movieron dentro de Frame 5 `538:3`) | ✅ Aprobada |

### Pendientes conocidos (fuera de alcance)
- Desktop `184:369` (Andrés Peñaranda, viejo y oculto, con restos de Evan Ellis): se deja como está por decisión del usuario.
- **Hay dos sesiones llamadas "Diseño-Ins"**: Diseño-Eje debe responder a la dirección `from=` del mensaje, no al nombre.
- Fotos pendientes (las pone el usuario): Francisco José López. (Gonzalo Catanzariti: puesta el 2026-10-22 y entregado a Ponentes-WP.) (Fernando Cocho, Andrés Peñaranda y Daniela Galvan: puestas el 2026-10-21; Omar Chehade: 2026-10-22. Todos entregados a Ponentes-WP.)
- En móvil, comprobar en metadata que los íconos de Especialidades sean hijos de Frame 5, no del frame raíz (Tarea 21).
- Al poner la foto en laptop, comprobar que su posición sea la del desktop × 0.711458 (en Omar quedó 51 px corrida y el usuario la ajustó).
- Página Laptop: frame sobrante `426:2` "Diana … (Laptop 1366)" en x = 0, encima de "Frame 5" (`301:2`).
- **Desktop `395:2` y laptop `408:2` de Diana:** detrás del brazo derecho de Diana se ve un trozo del blazer gris de María Herrera. Está en la capa `395:50` "FOTO DIANA … (pendiente)", que en realidad tiene la foto de María. Hay que vaciarla o borrarla en los dos frames. El móvil `409:2` está bien.
- Desktop `395:2`: algunas capas conservan nombres viejos ("ELLIS", "Foto… (pendiente)" en `395:50`); lo visible sí es de Diana.

---

## 10. Relación con Elementor

Al pasar un diseño aprobado a Elementor se aplican las reglas de la carpeta del ponente (`cv-ponentes/<slug>/`):
- Plantilla `.json` de Elementor y `<slug>-datos.json`.
- `imagenes/` en WebP de menos de 500 KB.
- `iconos/` en SVG e `iconos-webp/`.
- Columna de estadísticas *sticky* en desktop y laptop.

Las estructuras de Figma deben seguir la plantilla al pie de la letra para que esa conversión sea directa.
