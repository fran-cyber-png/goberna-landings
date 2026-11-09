# F3b – Reporte: fotos y banderas de las tarjetas de docentes · CII v1

- Copia afectada: **solo principal `4005:17`**. No se tocaron las copias 4005:587 y 4005:653.
- Textos de F3: **no tocados** (siguen como quedaron en F3).
- Estado: **parcial**. Fotos de las 3 tarjetas hechas. Banderas de tarjetas 2 y 3 hechas. **Bandera de Perú en tarjeta 1: pendiente de decisión** (ver sección 4).

## 1. Estado final de cada tarjeta

| Tarjeta | Nombre (texto de F3) | Foto | Bandera | Estado |
|---|---|---|---|---|
| 1 (`4005:533`) | ROBERTO BAZÁN / PERÚ | **Bazán** (subida, `4005:534`) | **España (sin cambio)** | foto OK; bandera pendiente |
| 2 (`4005:545`) | EDUARDO DE LA TORRE DÍAZ / COLOMBIA | **De la Torre** (copiada de tarjeta 1, `4005:546`) | **Colombia** (copiada de tarjeta 3, grupo `4005:548`) | OK |
| 3 (`4005:557`) | GONZALO CATANZARITI / ARGENTINA | **Catanzariti** (copiada de tarjeta 2, `4005:558`) | **Argentina** (copiada de tarjeta 2, grupo `4005:560`) | OK |

Foto de Aledo (hash `88bef019…`): **ya no está en ninguna tarjeta visible**. El nodo `4005:558` la reemplazó con la foto de Catanzariti. No se borró ningún recurso del archivo.

## 2. Fills ANTES (leídos antes de tocar nada)

Todas las fotos son `Foto` (FRAME 384×542) con un fill IMAGE, `scaleMode: FILL`, `imageTransform: [[1,0,0],[0,1,0]]`, opacidad 1, blend NORMAL, rotación 0, scalingFactor 1, filtros en cero.

| Nodo | Tarjeta | imageHash antes |
|---|---|---|
| `4005:534` | 1 | `d12fe786ca2fc6b661b6d8f703a42a5732fd84ce` (De la Torre) |
| `4005:546` | 2 | `0179d1f0b088ad68c868424eab8dc6e6e7170746` (Catanzariti) |
| `4005:558` | 3 | `88bef0194ba9cead1d773c7ed8057e3940b30a60` (Aledo) |

Banderas: son **GRUPOS de rectángulos sólidos**, no nodos con fill de imagen.

| Grupo | Tarjeta | Tipo | Rectángulos (id, y, alto, color) |
|---|---|---|---|
| `4005:536` "Bandera" | 1 | GROUP (23×14) | 537 (y25, h4, #AA151B) · 538 (y29, h7, #F1BF00) · 539 (y36, h4, #AA151B) → **España** |
| `4005:548` "Bandera" | 2 | GROUP (23×14) | 549 (y25, h5, #74ACDF) · 550 (y30, h5, #FFFFFF) · 551 (y34, h5, #74ACDF) → **Argentina** |
| `4005:560` "Bandera" | 3 | GROUP (23×14) | 561 (y25, h7, #FCD116) · 562 (y32, h4, #003893) · 563 (y36, h4, #CE1126) → **Colombia** |

Las mediciones de alto (h) en el grupo de Argentina salieron como 4.67 tras el cambio y como 5 antes. Eso es redondeo de Figma al leer las coordenadas, no un cambio intencionado.

## 3. Cambios aplicados

**Fotos:**
1. `4005:558` (tarjeta 3) ← fills completos de `4005:546` (Catanzariti). Hecho primero, antes de sobrescribir la tarjeta 2.
2. `4005:546` (tarjeta 2) ← fills completos de `4005:534` (De la Torre).
3. `4005:534` (tarjeta 1) ← subida de `_figma\card-roberto-bazan.png` (768×1076, 615 540 bytes) con `scaleMode FILL`. Nuevo `imageHash` **`fcaa463da0d505c38bed60f8f50a184dd9d006ad`**. Encuadre igual a las otras (imageTransform identidad, sin cortar la cabeza).

**Banderas (intercambio por contenido de grupo, sin cambiar los nodos grupo ni su posición):**
- Grupo `4005:548` (tarjeta 2) pasó de Argentina a **Colombia**: 549 → amarillo h7 y y25 · 550 → azul h3.5 y y32 · 551 → rojo h3.5 y y35.5.
- Grupo `4005:560` (tarjeta 3) pasó de Colombia a **Argentina**: 561 → azul h4.67 y y25 · 562 → blanco h4.67 y y29.67 · 563 → azul h4.67 y y34.33.

Se copiaron fills y geometría (y, alto) de los rectángulos. Los grupos mantienen su posición y su tamaño de 23×14 (salvo redondeo de 0.0002 px en uno).

## 4. Pendiente: bandera de Perú (tarjeta 1)

La bandera actual de la tarjeta 1 es España y **es un grupo de rectángulos**, no un nodo con fill de imagen. Orq pidió avisar antes de improvisar en este caso, así que **no la reemplacé**. Opciones (decide Orq/usuario):

- (a) Sustituir el contenido del grupo `4005:536` por una imagen PNG de Perú (`bandera-peru.png`, 46×28), con un nodo de imagen en las dimensiones de la bandera actual (23×14). Requiere crear o cambiar la forma del grupo.
- (b) Mantener un grupo de rectángulos y pintar las franjas de Perú (rojo / blanco / rojo) sin imagen.

Observación: `bandera-peru.png` pesa **109 bytes**. Es demasiado pequeño para una imagen de bandera real de 46×28. Conviene confirmar que el archivo es correcto antes de usarlo.

Mientras tanto, **la tarjeta 1 muestra PERÚ con bandera de España**. Es el único desajuste visible de F3b.

## 5. Verificación

- Render de `4005:530` (docentes): Bazán sobre su foto con la cabeza completa; De la Torre con bandera de Colombia; Catanzariti con bandera de Argentina. Cada nombre queda sobre su foto. Aledo ya no aparece en las tarjetas visibles.
- Alturas de las tarjetas: 542 px (sin cambio). `4005:17` = **9984** ✓.
- Nombres de capa **no cambiados**. Hay un detalle: el grupo `4005:548` sigue llamándose "Bandera Argentina franja" en sus hijos, y el `4005:560` "Bandera Colombia franja", aunque ahora muestran los colores contrarios. Orq dijo no tocar nombres de capa, así que lo dejo y lo señalo.
- Textos, fuentes y posiciones: sin cambios.
- Copias 4005:587 y 4005:653: sin tocar.

## 6. Ids tocados

- Fotos: `4005:534`, `4005:546`, `4005:558`.
- Banderas: rectángulos `4005:549`, `4005:550`, `4005:551` (grupo `4005:548`) y `4005:561`, `4005:562`, `4005:563` (grupo `4005:560`).
- Sin tocar: `4005:533`, `4005:545`, `4005:557` (tarjetas), textos, copias 587 y 653.
- Bandera de Perú (F3b-2): grupo `4005:536` y sus franjas `4005:537`, `4005:538`, `4005:539`.

---

## 7. F3b-2 · Bandera de Perú en tarjeta 1 (grupo 4005:536)

Opción (b) de F3b: tres franjas verticales de 1/3 del ancho del grupo, con el alto completo, usando los tres rectángulos que ya tenía el grupo. Orden izquierda a derecha: #D91023 · #FFFFFF · #D91023.

**Bounding box del grupo `4005:536`**

| | x | y | ancho | alto |
|---|---|---|---|---|
| Antes | 16 | 25 | 23 | 14 |
| Después | 16 | 25 | **23.0000095** | 14 |

La diferencia de ancho es de 0.0000095 px. Figma guarda las coordenadas en float32, y 23/3 no es representable exacto. Es ruido de precisión, no un hueco visible. Las tres franjas son contiguas: el borde derecho de cada una coincide con el izquierdo de la siguiente (23.6667 y 31.3333), y la última termina en 39.0000005.

**Fills y geometría de las franjas**

| Nodo | Nombre antes | Nombre después | Antes (x, y, ancho, alto, fill) | Después (x, y, ancho, alto, fill) |
|---|---|---|---|---|
| `4005:537` | Bandera España franja | **Rojo** | 16, 25, 23, 3.5, #AA151B | 16, 25, 7.6667, 14, **#D91023** |
| `4005:538` | Bandera España franja | **Blanco** | 16, 28.5, 23, 7, #F1BF00 | 23.6667, 25, 7.6667, 14, **#FFFFFF** |
| `4005:539` | Bandera España franja | **Rojo** | 16, 35.5, 23, 3.5, #AA151B | 31.3333, 25, 7.6667, 14, **#D91023** |

Todos los fills son SOLID, opacidad 1, blend NORMAL. No hay rectángulo de fondo ni borde aparte: el grupo tenía solo esas tres franjas.

**Renombrado de las franjas de las otras dos banderas (sin cambiar colores ni geometría)**

| Grupo | Bandera | Nodo | Nombre antes | Nombre después |
|---|---|---|---|---|
| `4005:548` | Colombia (tarjeta 2) | 4005:549 (arriba) | Bandera Argentina franja | **Amarillo** |
| `4005:548` | Colombia (tarjeta 2) | 4005:550 (medio) | Bandera Argentina franja | **Azul** |
| `4005:548` | Colombia (tarjeta 2) | 4005:551 (abajo) | Bandera Argentina franja | **Rojo** |
| `4005:560` | Argentina (tarjeta 3) | 4005:561 (arriba) | Bandera Colombia franja | **Celeste** |
| `4005:560` | Argentina (tarjeta 3) | 4005:562 (medio) | Bandera Colombia franja | **Blanco** |
| `4005:560` | Argentina (tarjeta 3) | 4005:563 (abajo) | Bandera Colombia franja | **Celeste** |

**Verificación**

- `4005:17` sigue en **9984**.
- Render posterior al cambio (`get_screenshot` de `4005:530`): la tarjeta 1 muestra la bandera de Perú con franjas rojo-blanco-rojo verticales; la tarjeta 2 muestra Colombia y la tarjeta 3 muestra Argentina.
- No se tocaron textos, fotos, posiciones de tarjetas ni las copias 587 y 653.
