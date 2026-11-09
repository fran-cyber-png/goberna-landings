# TAREA F1 — HD-Eje · Proyecto HUMINT (de Ins = humint-45)

**Protocolo obligatorio:** `C:\Users\Consultoría\Documents\Guias-Landings\PROTOCOLO-REEMPLAZO-TEXTOS-FIGMA.md`. Léelo completo antes de empezar.
Regla de oro: **solo cambias `characters`** de capas de texto existentes. No tocas tamaños, posiciones, fuentes, colores, imágenes ni la estructura. No decides cambios de diseño por tu cuenta.
Antes de llamar a `use_figma`, carga el skill `figma:figma-use`.

## Datos
- Figma fileKey: `TZaBinYmWvX5sD7aBTR9Hp` (Page 1)
- Plantilla: `2:16` ("INTELIGENCIA Y CONTRAINTELIGENCIA – v1", 1920×9984). **No tiene frames de estado aparte.**
- Contenido (solo referencia): `C:\Users\Consultoría\Downloads\CONTENIDO LANDINGS (8).pdf`
- Imágenes, fotos y banderas: **FUERA de alcance**. Header, menú y footer: intactos.

## Paso 1 — Duplicar
Duplica `2:16`, nombra la copia `HUMINT – v1` y colócala en x=3000, y=0. Nunca trabajes sobre `2:16`.
Haz el volcado inicial de la copia (`id | ruta | x,y | w×h | oculto | characters`) y registra la altura y las líneas de cada texto. Los ids de la copia cambian: mapea cada capa por su **posición equivalente a la de la plantilla** (te doy abajo los ids de la plantilla).

## Paso 2 — Reemplazos
Reglas generales:
- Carga **las fuentes actuales** de cada nodo (`getStyledTextSegments(['fontName'])`) antes de editar.
- Donde se indica **[COBRE]**, el texto original tiene dos segmentos: base + color cobre (144,85,50). Reaplica el **mismo color y la misma fuente** del segmento original al tramo indicado; el resto del texto lleva el estilo del primer segmento.
- Donde se indica **[BOLD]**, se replica el patrón Regular + Bold del original.
- Si hay **fallback**: prueba primero el texto A. Si cambia el número de líneas o la altura, prueba el B. Si también falla, **restaura el original** y repórtalo con las líneas y la altura que dio cada versión.
- Si una capa **sin fallback** cambia de líneas o de altura: **restaura el original** y repórtalo con las líneas y la altura que dio el texto nuevo. Excepción: las capas marcadas **(caja fija)** tienen `textAutoResize = NONE`; en esas, verifica en el render que el texto entre en la caja sin cortarse ni solaparse con su vecino y reporta las líneas.
- Las capas que no aparecen en esta lista **NO se tocan**.

| id plantilla | Actual | Nuevo |
|---|---|---|
| 2:43 | 09 DE DICIEMBRE | 02 DE DICIEMBRE |
| 2:57 [COBRE] | De la información a la **acción estratégica** | A: `Del análisis de la amenaza al diseño de respuestas estratégicas` (cobre: `diseño de respuestas estratégicas`). **Sin fallback ni condensación** por decisión del usuario: si no cabe, restaura y reporta las líneas que dio. |
| 2:58 | Anticipa amenazas, protege… | A: `Aprende a analizar redes criminales y terroristas, interpretar sus vínculos y desarrollar estrategias de prevención, disrupción y cooperación frente a escenarios complejos.` **Sin fallback** (igual que 2:57). |
| 2:30 [BOLD] | Formarte para **analizar…** | `Formar especialistas capaces de ` (Regular) + `planificar, obtener, evaluar y transformar información proveniente de fuentes humanas en inteligencia útil para la toma de decisiones.` (Bold) |
| 2:31 | Durante el diploma desarrollarás… | `Durante el diploma desarrollarás capacidades para formular requerimientos, evaluar fuentes, conducir entrevistas, gestionar riesgos, corroborar información y sustentar una misión HUMINT mediante productos profesionales de inteligencia.` |
| 2:32 (OCULTA) | -Inteligencia estratégica… | `-Inteligencia\n-Contrainteligencia\n-HUMINT\n-Seguridad` (sigue oculta) |
| 2:195 [COBRE] | Aquí la información se convierte en **acción estratégica** | A: `Aquí no solo estudias HUMINT. Aprendes a construir inteligencia desde las personas.` (cobre: `construir inteligencia desde las personas.`) · B: `Aprendes a construir inteligencia desde las personas.` (cobre: `inteligencia desde las personas.`) |
| 2:196 | El diploma combina fundamentos… | `Durante todo el diploma trabajarás sobre una misión HUMINT simulada. Cada módulo generará un avance concreto que se integrará progresivamente en tu portafolio de inteligencia.` |
| 2:205 | Aprende | `Planifica` |
| 2:206 | Comprende los principios… | `Convierte necesidades de inteligencia en objetivos, requerimientos y un plan de obtención HUMINT.` |
| 2:209 | Analiza | `Evalúa` |
| 2:210 | Aplica herramientas… | `Analiza motivaciones, confiabilidad, riesgos y patrones de comportamiento de las fuentes humanas.` |
| 2:214 | Trabaja | `Obtén` |
| 2:215 | Desarrolla ejercicios… | A: `Aplica técnicas de entrevista, escucha activa y elicitación para identificar información relevante y vacíos informativos.` · B: `Aplica técnicas de entrevista, escucha activa y elicitación para identificar información relevante.` |
| 2:217 | Protege | `Analiza` |
| 2:218 | Fortalece capacidades… | `Corrobora hallazgos, evalúa su credibilidad y construye conclusiones útiles para la toma de decisiones.` |
| 2:455 | Una formación para entender, anticipar y proteger | A: `Una formación para comprender, evaluar y trabajar con fuentes humanas` · B: `Comprender, evaluar y trabajar con fuentes humanas` |
| 2:422 | Fundamentos de Inteligencia y Contrainteligencia | `HUMINT: el poder de las fuentes humanas` (puede quedar en 1 línea donde había 2: **no restaures por eso**; reporta la altura) |
| 2:417 | Comprende cómo funciona… | `Comprende el papel de la inteligencia humana dentro del ciclo de inteligencia y su valor para apoyar decisiones estratégicas.` |
| 2:426 | Principios de inteligencia… | A: `Fundamentos de HUMINT, ciclo de inteligencia, relación con OSINT, SIGINT e IMINT, límites y principios éticos.` · B: `Fundamentos de HUMINT, ciclo de inteligencia, relación con OSINT, SIGINT e IMINT.` |
| 2:430 | Identificación de medidas… | A: `Identificación del aporte de las fuentes humanas dentro de una necesidad concreta de inteligencia.` · B: `Identificación del aporte de las fuentes humanas en una necesidad de inteligencia.` |
| 2:440 | Inteligencia Estratégica: análisis… | `Planeamiento de operaciones HUMINT` (puede quedar en 1 línea: **no restaures por eso**; reporta) |
| 2:448 | OSINT: Inteligencia de Fuentes Abiertas | A: `Psicología y comportamiento de las fuentes humanas` · B: `Psicología de las fuentes humanas` (el slot es de 1 línea) |
| 2:512 | Inicio: 09 de diciembre \| Online vía Zoom \| 8 Módulos | `Inicio: 02 de diciembre \| Online vía Zoom \| 8 Módulos` |
| 2:523 [COBRE] (caja fija) | Aprende de especialistas en inteligencia, **seguridad y estrategia** | `Aprende de especialistas en HUMINT, inteligencia y seguridad` (cobre: `inteligencia y seguridad`). Reporta dónde corta la línea. |
| 2:531 (caja fija) | PERÚ | `ESPAÑA` |
| 2:532 (caja fija) | ROBERTO BAZÁN | `FRANCISCO LÓPEZ` |
| 2:533 (caja fija) | Especialista en inteligencia estratégica y operaciones psicológicas | `Especialista en criminología, inteligencia y análisis de fuentes humanas` |
| 2:544 (caja fija) | EDUARDO DE LA TORRE DÍAZ | `MG. EDUARDO DE LA TORRE` |
| 2:545 (caja fija) | Especialista en ciberseguridad e inteligencia | `Especialista en ciberseguridad, ciberdefensa y análisis digital` (puede pasar a 2 líneas dentro de la caja de 32 px, como las otras tarjetas) |
| 2:556 (caja fija) | GONZALO CATANZARITI | `DANIELA GALVÁN` |
| 2:557 (caja fija) | Especialista en ciberinteligencia e investigación digital | `Especialista en investigación criminal e inteligencia digital` |
| 2:386 [COBRE] | Una certificación que **fortalece tu perfil estratégico** | `Una certificación para especialistas en inteligencia humana` (cobre: `especialistas en inteligencia humana`) |
| 2:387 | Al culminar satisfactoriamente… | `Al culminar satisfactoriamente el programa recibirás la certificación como Especialista en Inteligencia de Fuentes Humanas. Una acreditación que reconoce tu formación en planeamiento HUMINT, gestión y evaluación de fuentes, entrevista, análisis y producción de inteligencia.` |
| 2:403 | Credencial digital verificable para validar… | `Credencial digital verificable que facilita la validación de tu certificación y su presentación profesional.` |
| 2:318 | ANTICÍPATE A LAS AMENAZAS. DECIDE CON INTELIGENCIA. | `ESPECIALÍZATE EN INTELIGENCIA DE FUENTES HUMANAS` |
| 2:327 | 09 de diciembre | `02 de diciembre` |
| 2:339 | ¿Listo para dar el\nsiguiente paso? | A: `¿Listo para especializarte\nen HUMINT?` · B: `¿Listo para especializarte en HUMINT?` |
| 2:273 | Las sesiones se desarrollan en modalidad online… | A: `Las sesiones se desarrollan 100% online y en vivo vía Zoom, combinando clases participativas, análisis de casos, ejercicios de entrevista, simulaciones por roles y retroalimentación docente.` · B: `Las sesiones se desarrollan 100% online y en vivo vía Zoom, combinando clases participativas, análisis de casos, ejercicios de entrevista y simulaciones por roles.` |

## Paso 3 — Validación (protocolo §5.5–5.6)
- Revisa cada capa: misma altura, mismas líneas, sin desborde horizontal y sin solaparse con sus vecinas.
- La altura del frame copia debe ser **9984**.
- Para los títulos de etapa (2:205/209/214/217, ancho automático), confirma que no invadan la columna siguiente.

## Paso 4 — Reporte a humint-45 (por SendMessage)
1. Id del frame copia y su tamaño.
2. Tabla `id plantilla | id copia | versión usada (A/B/original) | alto antes → después | líneas antes → después`.
3. Textos restaurados y su motivo, con las líneas y la altura que dio cada versión.
4. Cualquier cambio no textual con su justificación (lo esperado es ninguno).
5. Volcado literal de **todas** las capas de texto de la copia (incluidas las ocultas) con `id | characters`.
