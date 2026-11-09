# F2 – Reporte de actualización (fecha y módulo 1) · CII v1

- Copia afectada: **principal `4005:17`** únicamente. Las copias `4005:587` y `4005:653` no se tocaron.
- Mapa aplicado: `F2-mapa-actualizacion.md` (fuente: `CONTENIDO LANDINGS (7).pdf`).
- Regla aplicada: solo se cambió `characters`. Las 6 capas son de un solo estilo (ninguna tenía rangos mixtos, así que no hizo falta avisar antes de tocarlas). Fuente, tamaño, color e interlineado se conservaron.
- Títulos 4005:431, 4005:449 y 4005:457 **no tocados**.

## 1. Tabla de cambios

| id | texto antes | texto después | alto antes → después | líneas | ancho antes → después |
|---|---|---|---|---|---|
| 4005:48 | 12 DE OCTUBRE | 09 DE DICIEMBRE | 19 → 19 | 1 → 1 | 177 → 177 |
| 4005:335 | 12 de octubre | 09 de diciembre | 70 → 70 | 1 → 1 | 203 → **226** |
| 4005:521 | Inicio: 12 de octubre \| Online vía Zoom \| 8 Módulos | Inicio: 09 de diciembre \| Online vía Zoom \| 8 Módulos | 78 → 78 | 1 → 1 | 585 → **614** |
| 4005:426 | Comprende el ciclo de inteligencia, sus principios, metodologías y la relación entre seguridad y contrainteligencia. | Comprende cómo funciona la inteligencia y cuál es el papel de la contrainteligencia en la protección de una organización. | 64 → 64 | 2 → 2 | 754 → 754 |
| 4005:435 | El ciclo de inteligencia, sus principios, metodologías y la relación entre seguridad y contrainteligencia. | Principios de inteligencia, ciclo de inteligencia, fundamentos y procesos de contrainteligencia. | 63 → 63 | 3 → 3 | 338 → 338 |
| 4005:439 | Herramientas de inteligencia y contrainteligencia aplicadas a la seguridad. | Identificación de medidas para proteger información y capacidades críticas. | 48 → 48 | 2 → 2 | 337 → 337 |

Criterios de aceptación:
- 426 / 435 / 439 quedan en **64 / 63 / 48** de alto, es decir **2 / 3 / 2 líneas**. Cumple.
- 48 queda en **1 línea y 19 de alto**. Cumple.
- 335 y 521 quedan en **1 línea**. Cumple.

## 2. Anchos finales

- **4005:335: 226 px.** La estimación del mapa (≈155 px) no coincide con la medición. La plantilla original con "17 de noviembre" medía 231 px, así que tampoco se acerca a 155. El texto "09 de diciembre" en Inter 20 necesita 226 px. **No se cambió nada**, porque el criterio de aceptación era 1 línea y la capa cumple. Si se quiere otra anchura, hay que decidir otro texto o tamaño, y eso no lo decido yo.
- **4005:521: 614 px.** Dentro del rango esperado (615–620; el mapa estimaba 618). Queda alineado a la izquierda (x=80 dentro de `Frame 253`).

## 3. Comprobaciones de layout

- **4005:335** está en `Frame 236` (235×120), que **no tiene auto-layout** (`layoutMode = NONE`). Al crecer de 203 a 226 px, sus hermanos (4005:334 "Inicio") no se movieron. El contenedor `Frame 236` mide igual que antes.
- **4005:337 y 4005:338** (en `Frame 237`) no cambiaron de posición.
- **4005:521** dentro de `Frame 253` (1520×347, `layoutMode = NONE`): x=80, y=124, ancho 614 → borde derecho en 694. **No se sale del bloque** (que termina en 1520 dentro de la sección) y **no hay ningún elemento a su derecha** dentro del bloque. Los únicos solapes de bounding box son el fondo `Grupo 29229` (mismo tamaño que el bloque, es fondo) y el titular `4005:520`.
- **Solape 4005:520 / 4005:521:** el bounding box de 521 empieza en y=4651 y el de 520 termina en y=4663 (12 px de solape). Viene de la plantilla, no lo causó este cambio. Se verificó con render (`get_screenshot` de `4005:512`): el texto del titular termina antes, y la línea "Inicio: 09 de diciembre…" se ve sin colisión. **Sin choque visible.**
- **Frame 255** sigue en **1403**.
- **Copia principal 4005:17** sigue en **9984**.

## 4. Volcado literal de los `characters` finales

| id | characters |
|---|---|
| 4005:48 | 09 DE DICIEMBRE |
| 4005:335 | 09 de diciembre |
| 4005:521 | Inicio: 09 de diciembre \| Online vía Zoom \| 8 Módulos |
| 4005:426 | Comprende cómo funciona la inteligencia y cuál es el papel de la contrainteligencia en la protección de una organización. |
| 4005:435 | Principios de inteligencia, ciclo de inteligencia, fundamentos y procesos de contrainteligencia. |
| 4005:439 | Identificación de medidas para proteger información y capacidades críticas. |

## 5. Incidencias

1. **4005:335 mide 226 px**, no los ≈155 px del mapa (ver sección 2). Cumple el criterio de 1 línea. Pendiente de decisión si el ancho importa.
2. **Solape de 12 px entre 4005:520 y 4005:521**: viene de la plantilla, no es visible en render. Sin cambios.
3. **Nombres de capa obsoletos**: 4005:335 se llama "31 de octubre" y 4005:521 se llama "Inicio: 31 de octubre | Online en vivo | 4 semanas". No afecta al contenido. No se renombró porque no estaba en el alcance.
4. Ningún cambio no textual.
