# F3 – Reporte: docentes con Roberto Bazán primero · CII v1

- Copia afectada: **principal `4005:17`**. Solo se cambió `characters` de 9 capas.
- Mapa aplicado: `F2-mapa-actualizacion.md`, sección F3.
- Las 9 capas son de un solo estilo (sin rangos mixtos).
- No se tocaron fotos, banderas, nombres de capa, el titular 4005:532, "VER TRAYECTORIA" (4005:543, 4005:555, 4005:567) ni las copias 4005:587 y 4005:653.

## ⚠ Punto abierto antes de dar la tarea por cerrada

**4005:566 mide 2 líneas, no 1.** En el render, "Especialista en ciberinteligencia e investigación digital" se parte en "…investigación / digital". El texto cabe en la caja de 32 px, así que no se desborda, pero el protocolo exige que cada texto nuevo ocupe el mismo número de líneas que el original, y la capa original ("Especialista en inteligencia y seguridad internacional") ocupaba 1. **No la he restaurado todavía.** Dos opciones:
- (a) restaurar 4005:566 a "Especialista en inteligencia y seguridad internacional" (el protocolo lo marca así);
- (b) mantener el texto de 2 líneas, que cabe en la caja, y aceptarlo como excepción.

Lo decide Orq o el usuario.

## 1. Tabla de cambios

| id | texto antes | texto después | alto antes → después | líneas antes → después |
|---|---|---|---|---|
| 4005:540 | COLOMBIA | PERÚ | 14 → 14 | 1 → 1 |
| 4005:541 | EDUARDO DE LA TORRE DÍAZ | ROBERTO BAZÁN | 22 → 22 | 1 → 1 |
| 4005:542 | Especialista en ciberseguridad e inteligencia | Especialista en inteligencia estratégica y operaciones psicológicas | 32 → 32 | 1 → **2** (esperado 2; ver render) |
| 4005:552 | ARGENTINA | COLOMBIA | 14 → 14 | 1 → 1 |
| 4005:553 | GONZALO CATANZARITI | EDUARDO DE LA TORRE DÍAZ | 22 → 22 | 1 → 1 |
| 4005:554 | Especialista en ciberinteligencia e investigación digital | Especialista en ciberseguridad e inteligencia | 32 → 32 | 2 → **1** |
| 4005:564 | ESTADOS UNIDOS | ARGENTINA | 14 → 14 | 1 → 1 |
| 4005:565 | RONIEL ALEDO | GONZALO CATANZARITI | 22 → 22 | 1 → 1 |
| 4005:566 | Especialista en inteligencia y seguridad internacional | Especialista en ciberinteligencia e investigación digital | 32 → 32 | 1 → **2** ⚠ (esperado 1; pendiente, ver arriba) |

Nota: la columna de líneas se midió en render (`get_screenshot` de `4005:530`). Las cajas son de alto fijo (NONE), así que la altura de la caja no cambia y no sirve para contar líneas.

Criterios de aceptación:
- Altos: 14, 22 y 32 se mantienen en las 9 capas. ✓
- 542 en 2 líneas dentro de la caja de 32 px. ✓
- 554 en 1 línea. ✓
- Nombres y países en 1 línea. ✓
- 566: **2 líneas, no 1** (ver punto abierto).
- Ningún texto se desborda de su caja. ✓ (los 2 casos de 2 líneas caben en 32 px).
- 4005:17 sigue en **9984**. ✓

## 2. Fuentes: diferencia con el volcado de F0

Antes de tocar nada, la fuente de estas capas ya era distinta de la registrada en F0. **Esto no lo causó F3**: la lectura "antes" de cada capa en F3 ya mostraba estas fuentes. Comparado con el volcado de F0:

| id | F0 | Ahora (antes de F3) |
|---|---|---|
| 4005:541 / 553 / 565 (nombres) | Barlow Bold 21 | Montserrat Bold 21 |
| 4005:542 / 554 / 566 (descripciones) | Barlow ExtraLight 15 | Inter Light 15 |
| 4005:543 / 555 / 567 (VER TRAYECTORIA, sin tocar) | Inder Regular 13 | Inter Regular 13 |
| 4005:540 / 552 / 564 (países) | Barlow Regular 14 | Barlow Regular 14 (igual) |

Las fuentes Barlow, Inder e Inter están disponibles en el entorno. No es un problema de fuente faltante. Las capas 543/555/567 no las toqué en ninguna fase de F1 ni de F3, y aun así cambiaron. No sé qué lo causó. **No he cambiado ninguna fuente.** Hay que decidir si se restauran a Barlow / Inder.

## 3. Estado del archivo: anomalías que no causé

Al verificar la plantilla para comparar las fuentes, encontré esto:

1. **La plantilla `2002:21` "CARRERA DIPLOMÁTICA – v1" ya no está en la página Desktop.** Busqué en todas las páginas: no aparece con ese id.
2. En la página **Laptop** hay un marco nuevo: `2040:25` "CARRERA DIPLOMÁTICA – v1 (Laptop 1366)" (1920×? escalado, y=0, x=2600, h=7103). Parece una adaptación a laptop, quizá del skill `figma-laptop-adapt`, pero no lo confirmo.
3. **La copia principal `4005:17` está en x=0**, no en x=10200 como se creó en F0. En x=0 se solapa con `357:27` (CONSULTOR v2, x=86) y `310:26` (NUEVA PLANTILLA, x=15).
4. **Nueve imágenes nuevas** en Desktop: `4012:72`, `4012:73`, `4012:74`, `4012:75`, `4012:77`, `4012:78`, `4012:79`, `4012:80`, todas `img_*` tipo RECTANGLE, con coordenadas negativas o cerca de la zona de trabajo.
5. `357:626` (Background de v2) cambió de posición (de 3401,8730 a 2249,8113).
6. `2002:551`, `2002:617`, `4005:587` y `4005:653` siguen en sus posiciones.

No hice ningún cambio de posición, de borrado ni de creación de imágenes en esta fase. **Recomiendo revisar el historial de versiones de Figma** para ver quién movió o borró la plantilla y creó las imágenes. Antes de cualquier otra escritura, hay que aclarar esto.

## 4. Volcado literal de las 9 capas (después de F3)

| id | characters |
|---|---|
| 4005:540 | PERÚ |
| 4005:541 | ROBERTO BAZÁN |
| 4005:542 | Especialista en inteligencia estratégica y operaciones psicológicas |
| 4005:552 | COLOMBIA |
| 4005:553 | EDUARDO DE LA TORRE DÍAZ |
| 4005:554 | Especialista en ciberseguridad e inteligencia |
| 4005:564 | ARGENTINA |
| 4005:565 | GONZALO CATANZARITI |
| 4005:566 | Especialista en ciberinteligencia e investigación digital |

## 5. Incidencias visibles

- **Banderas no coinciden con el país** (decisión del usuario, sin tocar). Tarjeta 1: PERÚ con bandera de España. Tarjeta 2: COLOMBIA con bandera de Argentina. Tarjeta 3: ARGENTINA con bandera de Colombia. En el render se ve claramente, así que conviene confirmarlo con el usuario.
- 4005:566 queda en 2 líneas (punto abierto).
- Anomalías de la sección 3.
