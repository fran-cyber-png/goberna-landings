# T1 · Volcado inicial de textos — copia "OSINT & SOCMINT – v1"

- **Archivo Figma:** `DYHmJ4KeF8moE2rQl7Fi9i`, página "Desktop" (`0:1`)
- **Original (intacto):** `4090:16` "HUMINT – v1" — 1920×9984, 50 hijos directos, 168 capas TEXT
- **Copia de trabajo:** `4101:17` "OSINT & SOCMINT – v1" — 1920×9984, posición x=2200, y=0, 50 hijos directos, 168 capas TEXT
- **Estado:** solo volcado. No se ha cambiado ningún texto ni propiedad de la copia.

## Alturas

Coordenadas relativas a la copia (origen = esquina superior izquierda de `4101:17`).

**Frames de sección de primer nivel** (hijos directos tipo FRAME):

| id | nombre | y | alto | visible |
|---|---|---|---|---|
| 4101:24 | Frame 262 | 1827 | 717 | sí |
| 4101:52 | Frame 157 | 1086 | 628.25 | sí |
| 4101:131 | Frame 199 | 1680 | 33 | sí |
| 4101:143 | Frame 229 | 1889 | 592 | sí |
| 4101:188 | Frame 261 | 2544 | 1027 | sí |
| 4101:218 | Grupo 29210 (GROUP) | 5559 | 14 | **no** |
| 4101:222 | Grupo 29209 (GROUP) | 5228 | 56 | **no** |
| 4101:227 | Grupo 29208 (GROUP) | 5228 | 56 | **no** |
| 4101:232 | Frame 256 | 6040 | 867 | sí |
| 4101:258 | Frame 242 | 8904 | 780 | sí |
| 4101:296 | Frame 243 | 9684 | 300 | sí |
| 4101:299 | Componente 13 – 1 | 0 | 90 | sí |
| 4101:312 | Frame 258 | 7963 | 941 | sí |
| 4101:365 | Frame 263 | 319 | 308.45 | sí |
| 4101:380 | Frame 257 | 6907 | 1056 | sí |
| 4101:415 | Frame 255 | 3571 | 1403 | sí |
| 4101:520 | 09 Docentes | 4974 | 1066 | sí |
| 4101:45 | Frame 244 (dentro de bloque de precio) | 919 | 57 | sí |

Otros hijos directos (rectángulos, líneas, grupos de iconos, `capitolio`, etc.) están en el listado de la copia; no son frames de sección.

**Altura total de la copia `4101:17`: 9984** (coincide con la plantilla `4090:16`).

## Notas del volcado

- Hay **2 capas ocultas por sí mismas**: `4101:32` (lista de 4 viñetas, "Diagnostico…") y `4101:33` ("Duración").
- Hay **2 capas ocultas por ancestro**: `4101:81` y `4101:82`, dentro de `Frame 152` (`4090:76`, oculto en la plantilla).
- Hay **6 capas TEXT dentro de instancias** (`Hor Nav` en la barra superior). Sus ids son compuestos (`I4101:302;229:16`, etc.) y los 6 valen "ABOUT". Requieren override de instancia para cambiar `characters`; no se tocan en esta tarea.
- Los `characters` de todas las capas son **texto de la plantilla HUMINT**, sin cambios. Los nombres de capa no coinciden con su contenido (p. ej. `4101:36` se llama "OBJETIVO DEL PROGRAMA" y dice "OBJETIVO DEL DIPLOMA"; `4101:555` se llama en su tarjeta "EDUARDO VELANDIA BECERRA" y dice "DANIELA GALVÁN"). Se mapea por contenido.
- Las líneas renderizadas se calculan como `alto / lineHeight` cuando el lineHeight es PIXELS o PERCENT. Si es AUTO, aparece `n/a`.
- `4101:522` tiene lineHeight 56.16px y altura 112 → 1.99 líneas (redondeo de la fuente Montserrat).
- Colores: `#RRGGBB@op` = fill sólido con opacidad de paint. `tc` = textCase (ORIGINAL / UPPER).

## Tabla

Columnas: `id | ruta relativa (frames padres, desde la copia) | x,y (relativos a la copia) | ancho×alto | oculto | textAutoResize | fontName / fontSize / lineHeight | n.º líneas (alto/lh) | characters literal | segmentos de estilo`

4101:30 | (raíz) | 1002.5,2090 | 717×96 | no | HEIGHT | mixed / 18 / 32px | 3 | "Formar especialistas capaces de planificar, obtener, evaluar y transformar información proveniente de fuentes humanas en inteligencia útil para la toma de decisiones." | [0-32] "Formar especialistas capaces de " #141210@0.75 Regular tc=ORIGINAL ; [32-166] "planificar, obtener, evaluar y transformar información proveniente de fuentes humanas en inteligencia útil para la toma de decisiones." #141210@0.75 Bold tc=ORIGINAL
4101:31 | (raíz) | 1002.5,2243 | 717×96 | no | HEIGHT | Inter Regular / 18 / 32px | 3 | "Durante el diploma desarrollarás capacidades para formular requerimientos, evaluar fuentes, conducir entrevistas, gestionar riesgos, corroborar información y sustentar una misión HUMINT mediante productos profesionales de inteligencia." | 1 seg uniforme: #141210@0.75, ORIGINAL
4101:32 | (raíz) | 1002.5,2342 | 717×128 | sí | HEIGHT | Inter Regular / 18 / 32px | 4 | "-Inteligencia\n-Contrainteligencia\n-HUMINT\n-Seguridad" | 1 seg uniforme: #060606@0.75, ORIGINAL
4101:33 | (raíz) | 1399,921 | 89×25 | sí | WIDTH_AND_HEIGHT | Inter Regular / 21 / AUTO | n/a | "Duración" | 1 seg uniforme: #FFFFFF, ORIGINAL
4101:36 | (raíz) | 999,2017 | 329×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 24 / 50px | 1 | "OBJETIVO DEL DIPLOMA" | 1 seg uniforme: #00C300, UPPER
4101:37 | (raíz) | 240,926 | 114×19 | no | HEIGHT | Inter Regular / 16 / AUTO | n/a | "MODALIDAD" | 1 seg uniforme: #141210@0.75, UPPER
4101:38 | (raíz) | 551,926 | 61×19 | no | HEIGHT | Inter Regular / 16 / AUTO | n/a | "INICIO" | 1 seg uniforme: #141210@0.75, UPPER
4101:39 | (raíz) | 861,926 | 53×19 | no | HEIGHT | Inter Regular / 16 / AUTO | n/a | "HORA" | 1 seg uniforme: #141210@0.75, UPPER
4101:40 | (raíz) | 1171,926 | 101×19 | no | HEIGHT | Inter Regular / 16 / AUTO | n/a | "DURACIÓN" | 1 seg uniforme: #141210@0.75, UPPER
4101:41 | (raíz) | 240,955 | 72×19 | no | HEIGHT | Inter Regular / 16 / AUTO | n/a | "ONLINE" | 1 seg uniforme: #141210, UPPER
4101:42 | (raíz) | 551,955 | 177×19 | no | HEIGHT | Inter Regular / 16 / AUTO | n/a | "02 DE DICIEMBRE" | 1 seg uniforme: #141210, UPPER
4101:43 | (raíz) | 861,950 | 231×25 | no | HEIGHT | Inter Regular / 21 / AUTO | n/a | "19:00 HRS. GMT-5" | 1 seg uniforme: #141210, UPPER
4101:44 | (raíz) | 1171,955 | 125×19 | no | HEIGHT | Inter Regular / 16 / AUTO | n/a | "8 MÓDULOS" | 1 seg uniforme: #141210, UPPER
4101:46 | Frame 244 | 1526,919 | 105×19 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / AUTO | n/a | "INVERSIÓN" | 1 seg uniforme: #0F0F0F, UPPER
4101:47 | Frame 244 | 1506,946 | 145×30 | no | HEIGHT | Inter Regular / 25 / AUTO | n/a | "USD $199" | 1 seg uniforme: #0F0F0F, UPPER
4101:55 | Frame 157 > Frame 147 > Frame 146 | 200,1086 | 167×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 20 / 50px | 1 | "METODOLOGÍA" | 1 seg uniforme: #00C300, UPPER
4101:56 | Frame 157 > Frame 147 > Frame 146 | 200,1180 | 674×171 | no | HEIGHT | Montserrat Bold / 50 / 57px | 3 | "Del análisis de la amenaza al diseño de respuestas estratégicas" | [0-30] "Del análisis de la amenaza al " #141210 Bold tc=ORIGINAL ; [30-63] "diseño de respuestas estratégicas" #00C300 Bold tc=ORIGINAL
4101:57 | Frame 157 > Frame 147 | 200,1372 | 687×96 | no | HEIGHT | Inter Regular / 18 / 32px | 3 | "Aprende a analizar redes criminales y terroristas, interpretar sus vínculos y desarrollar estrategias de prevención, disrupción y cooperación frente a escenarios complejos." | 1 seg uniforme: #141210@0.75, ORIGINAL
4101:64 | Frame 157 > Frame 156 > Frame 155 > Frame 154 > Frame 153 | 249,1513.63 | 25×49 | no | WIDTH_AND_HEIGHT | Montserrat Regular / 43 / 49px | 1 | "+" | 1 seg uniforme: #00C300, ORIGINAL
4101:65 | Frame 157 > Frame 156 > Frame 155 > Frame 154 > Frame 153 | 282,1509.63 | 101×57 | no | WIDTH_AND_HEIGHT | Montserrat ExtraBold / 31 / 57px | 1 | "10,000" | 1 seg uniforme: #00C300, UPPER
4101:66 | Frame 157 > Frame 156 > Frame 155 > Frame 154 | 417,1518.13 | 182×40 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / 40px | 1 | "Profesionales formados" | 1 seg uniforme: #141210, ORIGINAL
4101:70 | Frame 157 > Frame 156 > Frame 155 > Frame 151 > Frame 150 | 249,1584.13 | 25×49 | no | WIDTH_AND_HEIGHT | Montserrat Regular / 43 / 49px | 1 | "+" | 1 seg uniforme: #00C300, ORIGINAL
4101:71 | Frame 157 > Frame 156 > Frame 155 > Frame 151 > Frame 150 | 278,1582.63 | 28×52 | no | WIDTH_AND_HEIGHT | Montserrat ExtraBold / 28 / 52px | 1 | "15" | 1 seg uniforme: #00C300, UPPER
4101:72 | Frame 157 > Frame 156 > Frame 155 > Frame 151 | 418.47,1588.63 | 187×40 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / 40px | 1 | "Países en Latinoamérica" | 1 seg uniforme: #141210, ORIGINAL
4101:76 | Frame 157 > Frame 156 > Frame 155 > Frame 149 > Frame 148 | 249,1652.13 | 25×49 | no | WIDTH_AND_HEIGHT | Montserrat Regular / 43 / 49px | 1 | "+" | 1 seg uniforme: #00C300, ORIGINAL
4101:77 | Frame 157 > Frame 156 > Frame 155 > Frame 149 > Frame 148 | 278,1650.63 | 36×52 | no | WIDTH_AND_HEIGHT | Montserrat ExtraBold / 28 / 52px | 1 | "20" | 1 seg uniforme: #00C300, UPPER
4101:78 | Frame 157 > Frame 156 > Frame 155 > Frame 149 | 417,1656.63 | 289×40 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / 40px | 1 | "Docentes Internacionales en ejercicio" | 1 seg uniforme: #141210, ORIGINAL
4101:81 | Frame 157 > Frame 156 > Frame 155 > Frame 152 | 249,1718.63 | 70×50 | por ancestro | WIDTH_AND_HEIGHT | Montserrat ExtraBold / 27 / 50px | 1 | "100%" | 1 seg uniforme: #FFBB03, UPPER
4101:82 | Frame 157 > Frame 156 > Frame 155 > Frame 152 | 417,1723.63 | 192×40 | por ancestro | WIDTH_AND_HEIGHT | Inter Regular / 16 / 40px | 1 | "Modalidad online en vivo" | 1 seg uniforme: #15262F, ORIGINAL
4101:132 | Frame 199 | 1008,1680 | 98×33 | no | WIDTH_AND_HEIGHT | Inter Regular / 18 / 33px | 1 | "Inteligencia" | 1 seg uniforme: #141210, ORIGINAL
4101:134 | Frame 199 | 1150,1680 | 86×33 | no | WIDTH_AND_HEIGHT | Inter Regular / 18 / 33px | 1 | "Estrategia" | 1 seg uniforme: #141210, ORIGINAL
4101:136 | Frame 199 | 1280,1680 | 85×33 | no | WIDTH_AND_HEIGHT | Inter Regular / 18 / 33px | 1 | "Liderazgo" | 1 seg uniforme: #141210, ORIGINAL
4101:138 | Frame 199 | 1409,1680 | 48×33 | no | WIDTH_AND_HEIGHT | Inter Regular / 18 / 33px | 1 | "Crisis" | 1 seg uniforme: #141210, ORIGINAL
4101:140 | Frame 199 | 1501,1680 | 93×33 | no | WIDTH_AND_HEIGHT | Inter Regular / 18 / 33px | 1 | "Tecnología" | 1 seg uniforme: #141210, ORIGINAL
4101:145 | Frame 229 > Frame 217 | 200,1889 | 581×50 | no | HEIGHT | Inter Regular / 20 / 50px | 1 | "El programa" | 1 seg uniforme: #00C300, UPPER
4101:146 | Frame 229 > Frame 217 | 200,1978 | 581×205 | no | HEIGHT | Montserrat Bold / 32 / 41px | 5 | "Analiza escenarios, anticipa riesgos y aplica inteligencia y contrainteligencia para proteger organizaciones, proyectos y decisiones estratégicas." | [0-85] "Analiza escenarios, anticipa riesgos y aplica inteligencia y contrainteligencia para " #EBEFF2 Bold tc=ORIGINAL ; [85-146] "proteger organizaciones, proyectos y decisiones estratégicas." #00C300 Bold tc=ORIGINAL
4101:156 | Frame 229 > Frame 228 > Frame 223 > Frame 220 > Frame 219 > Frame 218 | 295.03,2227.75 | 226×57 | no | WIDTH_AND_HEIGHT | Inter Medium / 20 / 57px | 1 | "¿Cuál es el objetivo?" | 1 seg uniforme: #00C300, UPPER
4101:171 | Frame 229 > Frame 228 > Frame 224 > Frame 222 > Frame 221 | 296.03,2318 | 262×57 | no | WIDTH_AND_HEIGHT | Inter Medium / 20 / 57px | 1 | "¿A quiénes está dirigido?" | 1 seg uniforme: #FFFFFF@0.75, UPPER
4101:184 | Frame 229 > Frame 228 > Frame 227 > Frame 226 > Frame 225 | 296.03,2408 | 212×57 | no | WIDTH_AND_HEIGHT | Inter Medium / 20 / 57px | 1 | "Perfil del egresado" | 1 seg uniforme: #FFFFFF@0.75, UPPER
4101:193 | Frame 261 > Frame 202 > Frame 201 > Frame 200 | 200,2631 | 369×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 20 / 50px | 1 | "METODOLOGÍA DE APRENDIZAJE" | 1 seg uniforme: #00C300, UPPER
4101:194 | Frame 261 > Frame 202 > Frame 201 | 200,2728 | 614×159 | no | HEIGHT | Montserrat Bold / 54 / 53px | 3 | "Aprendes a construir inteligencia desde las personas." | [0-21] "Aprendes a construir " #EAEFF2 Bold tc=ORIGINAL ; [21-53] "inteligencia desde las personas." #00C300 Bold tc=ORIGINAL
4101:195 | Frame 261 > Frame 202 | 200,2910 | 614×87 | no | HEIGHT | Inter Regular / 18 / 29px | 3 | "Durante todo el diploma trabajarás sobre una misión HUMINT simulada. Cada módulo generará un avance concreto que se integrará progresivamente en tu portafolio de inteligencia." | 1 seg uniforme: #FFFFFF@0.75, ORIGINAL
4101:202 | Frame 261 > Grupo 29196 | 200,3224 | 71×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / 50px | 1 | "ETAPA 1" | 1 seg uniforme: #00C300, UPPER
4101:204 | Frame 261 > Grupo 29196 > Frame 247 | 200,3276 | 123×47 | no | WIDTH_AND_HEIGHT | Montserrat Bold / 27 / 47px | 1 | "Planifica" | 1 seg uniforme: #FFFFFF, ORIGINAL
4101:205 | Frame 261 > Grupo 29196 > Frame 247 | 200,3328 | 286×96 | no | HEIGHT | Inter Regular / 18 / 32px | 3 | "Convierte necesidades de inteligencia en objetivos y un plan de obtención HUMINT." | 1 seg uniforme: #FFFFFF@0.75, ORIGINAL
4101:206 | Frame 261 > Grupo 29196 | 590,3224 | 73×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / 50px | 1 | "ETAPA 2" | 1 seg uniforme: #00C300, UPPER
4101:208 | Frame 261 > Grupo 29196 > Frame 248 | 590,3281 | 94×37 | no | WIDTH_AND_HEIGHT | Montserrat Bold / 27 / 37px | 1 | "Evalúa" | 1 seg uniforme: #FFFFFF, ORIGINAL
4101:209 | Frame 261 > Grupo 29196 > Frame 248 | 590,3323 | 320×96 | no | HEIGHT | Inter Regular / 18 / 32px | 3 | "Analiza motivaciones, confiabilidad, riesgos y patrones de comportamiento de las fuentes." | 1 seg uniforme: #FFFFFF@0.75, ORIGINAL
4101:210 | Frame 261 > Grupo 29196 | 976,3224 | 74×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / 50px | 1 | "ETAPA 3" | 1 seg uniforme: #00C300, UPPER
4101:211 | Frame 261 > Grupo 29196 | 1376,3224 | 74×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / 50px | 1 | "ETAPA 4" | 1 seg uniforme: #00C300, UPPER
4101:213 | Frame 261 > Grupo 29196 > Frame 249 | 976,3281 | 89×37 | no | WIDTH_AND_HEIGHT | Montserrat Bold / 27 / 37px | 1 | "Obtén" | 1 seg uniforme: #FFFFFF, ORIGINAL
4101:214 | Frame 261 > Grupo 29196 > Frame 249 | 976,3323 | 312×96 | no | HEIGHT | Inter Regular / 18 / 32px | 3 | "Aplica técnicas de entrevista, escucha activa y elicitación para identificar información relevante." | 1 seg uniforme: #FFFFFF@0.75, ORIGINAL
4101:216 | Frame 261 > Grupo 29196 > Frame 250 | 1376,3281 | 104×37 | no | WIDTH_AND_HEIGHT | Montserrat Bold / 27 / 37px | 1 | "Analiza" | 1 seg uniforme: #FFFFFF, ORIGINAL
4101:217 | Frame 261 > Grupo 29196 > Frame 250 | 1376,3323 | 344×96 | no | HEIGHT | Inter Regular / 18 / 32px | 3 | "Corrobora hallazgos, evalúa su credibilidad y construye conclusiones útiles para la toma de decisiones." | 1 seg uniforme: #FFFFFF@0.75, ORIGINAL
4101:238 | Frame 256 | 200,6204.08 | 647×189 | no | HEIGHT | Montserrat Bold / 56 / 63px | 3 | "Una red que habla el idioma político de Latinoamérica." | [0-28] "Una red que habla el idioma " #FDFCFB Bold tc=ORIGINAL ; [28-54] "político de Latinoamérica." #00C300 Bold tc=ORIGINAL
4101:239 | Frame 256 | 205,6405.5 | 603×64 | no | HEIGHT | Inter Regular / 20 / 32px | 2 | "Egresados en 18 países que hoy dirigen campañas, asesoran gobiernos y lideran equipos de comunicación." | 1 seg uniforme: #FDFCFB@0.75, ORIGINAL
4101:240 | Frame 256 | 200,6113.5 | 305×42 | no | WIDTH_AND_HEIGHT | Inter Regular / 22 / 42px | 1 | "PRESENCIA INTERNACIONAL" | 1 seg uniforme: #00C300, ORIGINAL
4101:242 | Frame 256 | 233,6662.92 | 87×42 | no | WIDTH_AND_HEIGHT | Inter Regular / 22 / 42px | 1 | "Países" | 1 seg uniforme: #838994, UPPER
4101:243 | Frame 256 | 702,6662.92 | 137×42 | no | WIDTH_AND_HEIGHT | Inter Regular / 22 / 42px | 1 | "Docentes" | 1 seg uniforme: #838994, UPPER
4101:244 | Frame 256 | 442,6662.92 | 208×42 | no | WIDTH_AND_HEIGHT | Inter Regular / 22 / 42px | 1 | "Profesionales" | 1 seg uniforme: #838994, UPPER
4101:246 | Frame 256 > Frame 182 | 224.83,6576.42 | 37×99 | no | WIDTH_AND_HEIGHT | Montserrat Regular / 64 / 99px | 1 | "+" | 1 seg uniforme: #00C300, ORIGINAL
4101:247 | Frame 256 > Frame 182 | 261.83,6575.92 | 74×100 | no | WIDTH_AND_HEIGHT | Montserrat ExtraBold / 54 / 100px | 1 | "15" | 1 seg uniforme: #00C300, UPPER
4101:249 | Frame 256 > Frame 185 | 693.83,6576.42 | 37×99 | no | WIDTH_AND_HEIGHT | Montserrat Regular / 64 / 99px | 1 | "+" | 1 seg uniforme: #00C300, ORIGINAL
4101:250 | Frame 256 > Frame 185 | 730.83,6575.92 | 68×100 | no | WIDTH_AND_HEIGHT | Montserrat ExtraBold / 54 / 100px | 1 | "20" | 1 seg uniforme: #00C300, UPPER
4101:253 | Frame 256 > Frame 184 > Frame 183 | 433.83,6576.42 | 37×99 | no | WIDTH_AND_HEIGHT | Montserrat Regular / 64 / 99px | 1 | "+" | 1 seg uniforme: #00C300, ORIGINAL
4101:254 | Frame 256 > Frame 184 > Frame 183 | 470.83,6575.92 | 74×100 | no | WIDTH_AND_HEIGHT | Montserrat ExtraBold / 54 / 100px | 1 | "10" | 1 seg uniforme: #00C300, UPPER
4101:255 | Frame 256 > Frame 184 | 549.83,6575.92 | 40×100 | no | WIDTH_AND_HEIGHT | Montserrat SemiBold / 54 / 100px | 1 | "K" | 1 seg uniforme: #00C300, UPPER
4101:262 | Frame 242 > Frame 246 | 200,9069 | 538×50 | no | HEIGHT | Inter Regular / 16 / 50px | 1 | "PREGUNTAS FRECUENTES" | 1 seg uniforme: #00C300, UPPER
4101:264 | Frame 242 > Frame 246 > Frame 245 | 200,9160 | 538×183 | no | HEIGHT | Montserrat Bold / 56 / 61px | 3 | "Resolvemos tus\ndudas antes de\nque decidas." | [0-20] "Resolvemos tus\ndudas" #100600+#100600 Bold tc=ORIGINAL ; [20-42] " antes de\nque decidas." #100600+#00C300 Bold tc=ORIGINAL
4101:265 | Frame 242 > Frame 246 > Frame 245 | 200,9371 | 473×64 | no | HEIGHT | Inter Regular / 22 / 32px | 2 | "Aquí encontrarás respuestas claras sobre el programa, la metodología y tu certificación." | 1 seg uniforme: #060606@0.75, ORIGINAL
4101:271 | Frame 242 > Frame 173 > Frame 177 > Frame 176 > Frame 174 | 1022,9022 | 622×22 | no | HEIGHT | Inter Regular / 18 / AUTO | n/a | "¿Cómo se realizan las clases?" | 1 seg uniforme: #100600, ORIGINAL
4101:272 | Frame 242 > Frame 173 > Frame 177 > Frame 176 > Frame 174 | 1022,9068 | 622×63 | no | HEIGHT | Inter Regular / 17 / 21px | 3 | "Las sesiones se desarrollan 100% online y en vivo vía Zoom, combinando clases participativas, análisis de casos, ejercicios de entrevista, simulaciones por roles y retroalimentación docente." | 1 seg uniforme: #060606@0.75, ORIGINAL
4101:275 | Frame 242 > Frame 173 > Frame 177 > Frame 176 > Frame 175 | 1661,9022 | 12×31 | no | WIDTH_AND_HEIGHT | Inter Regular / 26 / AUTO | n/a | "-" | 1 seg uniforme: #F2F0EA, ORIGINAL
4101:278 | Frame 242 > Frame 173 > Grupo 29223 | 1022,9193 | 230×70 | no | WIDTH_AND_HEIGHT | Inter Regular / 18 / 70px | 1 | "¿Cuánto dura el programa?" | 1 seg uniforme: #100600, ORIGINAL
4101:280 | Frame 242 > Frame 173 > Grupo 29223 | 1659,9189 | 18×70 | no | WIDTH_AND_HEIGHT | Inter Regular / 26 / 70px | 1 | "+" | 1 seg uniforme: #100600, ORIGINAL
4101:283 | Frame 242 > Frame 173 > Grupo 29224 | 1022,9297 | 240×70 | no | WIDTH_AND_HEIGHT | Inter Regular / 18 / 70px | 1 | "¿Qué incluye mi inscripción?" | 1 seg uniforme: #100600, ORIGINAL
4101:285 | Frame 242 > Frame 173 > Grupo 29224 | 1659,9293 | 18×70 | no | WIDTH_AND_HEIGHT | Inter Regular / 26 / 70px | 1 | "+" | 1 seg uniforme: #100600, ORIGINAL
4101:288 | Frame 242 > Frame 173 > Grupo 29225 | 1022,9401 | 382×70 | no | WIDTH_AND_HEIGHT | Inter Regular / 18 / 70px | 1 | "¿Necesito experiencia previa en inteligencia?" | 1 seg uniforme: #100600, ORIGINAL
4101:290 | Frame 242 > Frame 173 > Grupo 29225 | 1659,9397 | 18×70 | no | WIDTH_AND_HEIGHT | Inter Regular / 26 / 70px | 1 | "+" | 1 seg uniforme: #100600, ORIGINAL
4101:293 | Frame 242 > Frame 173 > Grupo 29226 | 1022,9505 | 226×70 | no | WIDTH_AND_HEIGHT | Inter Regular / 18 / 70px | 1 | "¿Cómo puedo inscribirme?" | 1 seg uniforme: #100600, ORIGINAL
4101:295 | Frame 242 > Frame 173 > Grupo 29226 | 1659,9501 | 18×70 | no | WIDTH_AND_HEIGHT | Inter Regular / 26 / 70px | 1 | "+" | 1 seg uniforme: #100600, ORIGINAL
4101:298 | Frame 243 | 885,9804 | 151×61 | no | WIDTH_AND_HEIGHT | Montserrat Regular / 46 / 61px | 1 | "Footer" | 1 seg uniforme: #FFFFFF, ORIGINAL
I4101:302;229:16 | Componente 13 – 1 > Hor Nav | 658.84,37 | 62×19 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / AUTO | n/a | "ABOUT" | 1 seg uniforme: #141210, ORIGINAL
I4101:303;229:16 | Componente 13 – 1 > Hor Nav | 801.84,37 | 62×19 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / AUTO | n/a | "ABOUT" | 1 seg uniforme: #141210, ORIGINAL
I4101:304;229:16 | Componente 13 – 1 > Hor Nav | 944.84,37 | 62×19 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / AUTO | n/a | "ABOUT" | 1 seg uniforme: #141210, ORIGINAL
I4101:305;229:16 | Componente 13 – 1 > Hor Nav | 1087.84,37 | 62×19 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / AUTO | n/a | "ABOUT" | 1 seg uniforme: #141210, ORIGINAL
I4101:306;229:16 | Componente 13 – 1 > Hor Nav | 1230.84,37 | 62×19 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / AUTO | n/a | "ABOUT" | 1 seg uniforme: #141210, ORIGINAL
I4101:307;229:16 | Componente 13 – 1 > Hor Nav | 1373.84,37 | 62×19 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / AUTO | n/a | "ABOUT" | 1 seg uniforme: #141210, ORIGINAL
4101:311 | Componente 13 – 1 > Grupo 29180 > Grupo 21708 | 1495.96,33 | 191×24 | no | WIDTH_AND_HEIGHT | Inter Regular / 20 / AUTO | n/a | "Inscríbete ahora" | 1 seg uniforme: #0F0F0F, UPPER
4101:316 | Frame 258 > Frame 232 | 200,8031 | 614×42 | no | HEIGHT | Inter Regular / 22 / 42px | 1 | "INVERSIÓN" | 1 seg uniforme: #00C300, ORIGINAL
4101:317 | Frame 258 > Frame 232 | 200,8118 | 669×162 | no | HEIGHT | Montserrat Bold / 48 / 54px | 3 | "ESPECIALÍZATE EN INTELIGENCIA DE FUENTES HUMANAS" | 1 seg uniforme: #EBEFF2, ORIGINAL
4101:319 | Frame 258 > Frame 233 | 252,8377 | 200×146 | no | WIDTH_AND_HEIGHT | Montserrat Bold / 120 / AUTO | n/a | "199" | 1 seg uniforme: #EBEFF2, ORIGINAL
4101:320 | Frame 258 > Frame 233 | 200,8389 | 42×79 | no | WIDTH_AND_HEIGHT | Montserrat Bold / 65 / AUTO | n/a | "$" | 1 seg uniforme: #EBEFF2, ORIGINAL
4101:321 | Frame 258 | 472,8422 | 97×54 | no | WIDTH_AND_HEIGHT | Montserrat Medium / 43 / 54px | 1 | "USD" | 1 seg uniforme: #00C300, ORIGINAL
4101:325 | Frame 258 > Frame 238 > Frame 236 | 200,8578 | 73×70 | no | WIDTH_AND_HEIGHT | Inter Regular / 18 / 70px | 1 | "Inicio" | 1 seg uniforme: #888D98, UPPER
4101:326 | Frame 258 > Frame 238 > Frame 236 | 200,8618 | 226×70 | no | WIDTH_AND_HEIGHT | Inter Regular / 20 / 70px | 1 | "02 de diciembre" | 1 seg uniforme: #EBEFF2, UPPER
4101:328 | Frame 258 > Frame 238 > Frame 237 | 530,8578 | 120×70 | no | WIDTH_AND_HEIGHT | Inter Regular / 18 / 70px | 1 | "DURACIÓN" | 1 seg uniforme: #888D98, UPPER
4101:329 | Frame 258 > Frame 238 > Frame 237 | 530,8618 | 151×70 | no | WIDTH_AND_HEIGHT | Inter Regular / 20 / 70px | 1 | "8 MÓDULOS" | 1 seg uniforme: #EBEFF2, UPPER
4101:332 | Frame 258 > Frame 210 | 444,8724 | 127×19 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / AUTO | n/a | "PAGAR AHORA" | 1 seg uniforme: #0F0F0F, UPPER
4101:333 | Frame 258 | 200,8768 | 614×70 | no | HEIGHT | Inter Regular / 16 / 70px | 1 | "Vacantes limitadas para garantizar una formación especializada." | 1 seg uniforme: #00C300, ORIGINAL
4101:335 | Frame 258 > Frame 215 | 1100,8031 | 620×42 | no | HEIGHT | Inter Regular / 22 / 42px | 1 | "ADMISIÓN" | 1 seg uniforme: #00C300, ORIGINAL
4101:338 | Frame 258 > Frame 215 > Frame 214 > Frame 203 | 1100,8120 | 620×80 | no | HEIGHT | Montserrat Bold / 41 / 40px | 2 | "¿Listo para especializarte\nen HUMINT?" | 1 seg uniforme: #EAEFF2, ORIGINAL
4101:339 | Frame 258 > Frame 215 > Frame 214 > Frame 203 | 1100,8200 | 620×50 | no | HEIGHT | Inter Regular / 15 / 50px | 1 | "Déjanos tus datos y te ayudaremos con tu inscripción." | 1 seg uniforme: #EBEFF2@0.75, UPPER
4101:343 | Frame 258 > Frame 215 > Frame 214 > Frame 213 > Frame 212 > Frame 204 | 1100,8259 | 620×50 | no | HEIGHT | Inter Regular / 15 / 50px | 1 | "NOMBRE COMPLETO" | 1 seg uniforme: #EBEFF2, ORIGINAL
4101:347 | Frame 258 > Frame 215 > Frame 214 > Frame 213 > Frame 212 > Frame 206 > Frame 205 | 1100,8338 | 37×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 15 / 50px | 1 | "PAÍS" | 1 seg uniforme: #EBEFF2, ORIGINAL
4101:351 | Frame 258 > Frame 215 > Frame 214 > Frame 213 > Frame 212 > Frame 207 | 1100,8418 | 620×50 | no | HEIGHT | Inter Regular / 15 / 50px | 1 | "TELÉFONO" | 1 seg uniforme: #EBEFF2, ORIGINAL
4101:354 | Frame 258 > Frame 215 > Frame 214 > Frame 213 > Frame 212 > Frame 208 | 1100,8497 | 620×50 | no | HEIGHT | Inter Regular / 15 / 50px | 1 | "CARGO" | 1 seg uniforme: #EBEFF2, ORIGINAL
4101:357 | Frame 258 > Frame 215 > Frame 214 > Frame 213 > Frame 212 > Frame 209 | 1100,8578 | 620×50 | no | HEIGHT | Inter Regular / 15 / 50px | 1 | "CORREO ELECTRÓNICO" | 1 seg uniforme: #EBEFF2, ORIGINAL
4101:362 | Frame 258 > Frame 215 > Frame 214 > Frame 213 > Frame 211 > Frame 210 | 1376,8724 | 67×19 | no | WIDTH_AND_HEIGHT | Inter Semi Bold / 16 / AUTO | n/a | "ENVIAR" | 1 seg uniforme: #100600+#00C300, UPPER
4101:363 | Frame 258 > Frame 215 > Frame 214 > Frame 213 > Frame 211 | 1100,8757 | 620×70 | no | HEIGHT | Inter Regular / 16 / 70px | 1 | "Tus datos se usan solo para contactarte sobre el diploma." | 1 seg uniforme: #00C300, ORIGINAL
4101:371 | Frame 263 > Frame 159 > Grupo 29197 > Grupo 29189 | 255,518.45 | 201×19 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / AUTO | n/a | "RESERVA TU VACANTE" | 1 seg uniforme: #0F0F0F, UPPER
4101:374 | Frame 263 > Frame 159 > Grupo 29197 | 595.48,518.45 | 228×19 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / AUTO | n/a | "Hablar con un asesor" | 1 seg uniforme: #FFFFFF, UPPER
4101:377 | Frame 263 > Frame 159 > Grupo 29182 | 226.45,590.45 | 321×37 | no | WIDTH_AND_HEIGHT | Inter Regular / 14 / 37px | 1 | "Descargar brochure del programa" | 1 seg uniforme: #FFFFFF@0.75, UPPER
4101:385 | Frame 257 > Frame 186 > Frame 139 > Frame 138 | 1101,6988 | 176×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 20 / 50px | 1 | "CERTIFICACIÓN" | 1 seg uniforme: #00C300, UPPER
4101:386 | Frame 257 > Frame 186 > Frame 139 > Frame 138 | 1101,7069 | 619×171 | no | HEIGHT | Montserrat Bold / 50 / 57px | 3 | "Una certificación para especialistas en inteligencia humana" | [0-23] "Una certificación para " #14262F Bold tc=ORIGINAL ; [23-59] "especialistas en inteligencia humana" #00C300 Bold tc=ORIGINAL
4101:387 | Frame 257 > Frame 186 > Frame 139 | 1101,7281 | 619×160 | no | HEIGHT | Inter Regular / 20 / 32px | 5 | "Al culminar satisfactoriamente el programa recibirás la certificación como Especialista en Inteligencia de Fuentes Humanas. Una acreditación que reconoce tu formación en planeamiento HUMINT, gestión y evaluación de fuentes, entrevista, análisis y producción de inteligencia." | 1 seg uniforme: #060606@0.75, ORIGINAL
4101:392 | Frame 257 > Frame 186 > Frame 144 > Frame 143 > Frame 230 > Frame 140 | 1167,7501 | 498×26 | no | HEIGHT | Montserrat SemiBold / 20 / 26px | 1 | "CERTIFICACIÓN INTERNACIONAL" | 1 seg uniforme: #100600, UPPER
4101:393 | Frame 257 > Frame 186 > Frame 144 > Frame 143 > Frame 230 > Frame 140 | 1167,7534 | 498×56 | no | HEIGHT | Inter Regular / 20 / 28px | 2 | "Diploma emitido por Grupo Goberna, que acredita la culminación satisfactoria del programa." | 1 seg uniforme: #060606@0.75, ORIGINAL
4101:402 | Frame 257 > Frame 186 > Frame 144 > Tarjeta Verificación digital > Frame 230 > Frame 140 | 1167,7658 | 498×26 | no | HEIGHT | Montserrat SemiBold / 20 / 26px | 1 | "VERIFICACIÓN DIGITAL" | 1 seg uniforme: #100600, UPPER
4101:403 | Frame 257 > Frame 186 > Frame 144 > Tarjeta Verificación digital > Frame 230 > Frame 140 | 1167,7691 | 498×84 | no | HEIGHT | Inter Regular / 20 / 28px | 3 | "Credencial digital verificable que facilita la validación de tu certificación y su presentación profesional." | 1 seg uniforme: #060606@0.75, ORIGINAL
4101:412 | Frame 257 > Frame 186 > Frame 144 > Tarjeta Verificación digital > Frame 137 > Frame 136 | 1208.48,7816 | 228×19 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / AUTO | n/a | "Hablar con un asesor" | 1 seg uniforme: #00C300, UPPER
4101:417 | Frame 255 | 928,3827 | 754×64 | no | HEIGHT | Inter Regular / 20 / 32px | 2 | "Comprende el papel de la inteligencia humana dentro del ciclo de inteligencia y su valor para apoyar decisiones estratégicas." | 1 seg uniforme: #141210@0.75, ORIGINAL
4101:419 | Frame 255 | 829,3731 | 57×103 | no | WIDTH_AND_HEIGHT | Montserrat Medium / 56 / 103px | 1 | "01" | 1 seg uniforme: #00C300, UPPER
4101:420 | Frame 255 | 818,3704 | 79×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / 50px | 1 | "Módulo" | 1 seg uniforme: #00C300, UPPER
4101:421 | Frame 255 | 1606,3750 | 83×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / 50px | 1 | "ocultar" | 1 seg uniforme: #141210@0.75, UPPER
4101:422 | Frame 255 | 928,3755 | 611×28 | no | HEIGHT | Montserrat SemiBold / 24 / 28px | 1 | "HUMINT: el poder de las fuentes humanas" | 1 seg uniforme: #141210, ORIGINAL
4101:426 | Frame 255 > Frame 132 > Frame 131 | 952,3969 | 338×63 | no | HEIGHT | Inter Regular / 16 / 21px | 3 | "Fundamentos de HUMINT, ciclo de inteligencia, relación con OSINT, SIGINT e IMINT, límites y principios éticos." | 1 seg uniforme: #141210@0.75, ORIGINAL
4101:427 | Frame 255 > Frame 132 > Frame 131 | 952,3924 | 120×47 | no | WIDTH_AND_HEIGHT | Montserrat SemiBold / 20 / 47px | 1 | "Aprenderás" | 1 seg uniforme: #141210, ORIGINAL
4101:430 | Frame 255 > Frame 132 > Grupo 29200 | 1357,3969 | 337×48 | no | HEIGHT | Inter Regular / 16 / 24px | 2 | "Identificación del aporte de las fuentes humanas en una necesidad de inteligencia." | 1 seg uniforme: #141210@0.75, ORIGINAL
4101:431 | Frame 255 > Frame 132 > Grupo 29200 | 1357,3924 | 95×47 | no | WIDTH_AND_HEIGHT | Montserrat SemiBold / 20 / 47px | 1 | "Aplicarás" | 1 seg uniforme: #141210, ORIGINAL
4101:437 | Frame 255 > Frame 130 > Grupo 29203 | 823,4150 | 68×103 | no | WIDTH_AND_HEIGHT | Montserrat Medium / 56 / 103px | 1 | "02" | 1 seg uniforme: #00C300, UPPER
4101:438 | Frame 255 > Frame 130 > Grupo 29203 | 818,4122.5 | 79×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / 50px | 1 | "Módulo" | 1 seg uniforme: #00C300, UPPER
4101:439 | Frame 255 > Frame 130 > Grupo 29203 | 1539,4168.5 | 150×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / 50px | 1 | "VER CONTENIDO" | 1 seg uniforme: #141210@0.75, UPPER
4101:440 | Frame 255 > Frame 130 > Grupo 29203 | 916,4172 | 603×29 | no | HEIGHT | Montserrat SemiBold / 24 / 29px | 1 | "Planeamiento de operaciones HUMINT" | 1 seg uniforme: #141210, ORIGINAL
4101:445 | Frame 255 > Frame 130 > Grupo 29203 | 823,4319 | 68×103 | no | WIDTH_AND_HEIGHT | Montserrat Medium / 56 / 103px | 1 | "03" | 1 seg uniforme: #00C300, UPPER
4101:446 | Frame 255 > Frame 130 > Grupo 29203 | 818,4291.5 | 79×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / 50px | 1 | "Módulo" | 1 seg uniforme: #00C300, UPPER
4101:447 | Frame 255 > Frame 130 > Grupo 29203 | 1539,4337.5 | 150×50 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / 50px | 1 | "VER CONTENIDO" | 1 seg uniforme: #141210@0.75, UPPER
4101:448 | Frame 255 > Frame 130 > Grupo 29203 | 916,4341 | 603×29 | no | HEIGHT | Montserrat SemiBold / 24 / 29px | 1 | "Psicología de las fuentes humanas" | 1 seg uniforme: #141210, ORIGINAL
4101:453 | Frame 255 > Frame 181 > Frame 180 > Frame 179 | 200,3658 | 527×50 | no | HEIGHT | Inter Regular / 20 / 50px | 1 | "PLAN DE ESTUDIOS" | 1 seg uniforme: #00C300, UPPER
4101:455 | Frame 255 > Frame 181 > Frame 180 > Frame 179 > Frame 178 | 200,3751 | 518×147 | no | HEIGHT | Montserrat Bold / 50 / 49px | 3 | "Una formación para trabajar con fuentes humanas" | 1 seg uniforme: #141210, ORIGINAL
4101:463 | Frame 255 > Frame 181 > Frame 180 > Frame 171 > Frame 166 > Frame 162 | 200,4024 | 28×47 | no | WIDTH_AND_HEIGHT | Montserrat Bold / 42 / 47px | 1 | "8" | 1 seg uniforme: #141210, ORIGINAL
4101:465 | Frame 255 > Frame 181 > Frame 180 > Frame 171 > Frame 166 > Frame 162 > Frame 161 | 200,4071 | 88×16 | no | HEIGHT | Montserrat Bold / 12 / 16px | 1 | "MÓDULOS" | 1 seg uniforme: #141210, ORIGINAL
4101:466 | Frame 255 > Frame 181 > Frame 180 > Frame 171 > Frame 166 > Frame 162 > Frame 161 | 200,4091 | 88×16 | no | HEIGHT | Montserrat Regular / 12 / 16px | 1 | "Especializados" | 1 seg uniforme: #141210, ORIGINAL
4101:478 | Frame 255 > Frame 181 > Frame 180 > Frame 171 > Frame 165 > Frame 164 | 370,4024 | 70×47 | no | WIDTH_AND_HEIGHT | Montserrat Bold / 42 / 47px | 1 | "120" | 1 seg uniforme: #141210, ORIGINAL
4101:480 | Frame 255 > Frame 181 > Frame 180 > Frame 171 > Frame 165 > Frame 164 > Frame 163 | 370,4071 | 63×16 | no | HEIGHT | Montserrat Bold / 12 / 16px | 1 | "HORAS" | 1 seg uniforme: #141210, ORIGINAL
4101:481 | Frame 255 > Frame 181 > Frame 180 > Frame 171 > Frame 165 > Frame 164 > Frame 163 | 370,4091 | 74×16 | no | WIDTH_AND_HEIGHT | Montserrat Regular / 12 / 16px | 1 | "Académicas" | 1 seg uniforme: #141210, ORIGINAL
4101:493 | Frame 255 > Frame 181 > Frame 180 > Frame 171 > Frame 170 > Frame 169 > Frame 167 | 524,4024 | 74×47 | no | WIDTH_AND_HEIGHT | Montserrat Bold / 42 / 47px | 1 | "100" | 1 seg uniforme: #141210, ORIGINAL
4101:494 | Frame 255 > Frame 181 > Frame 180 > Frame 171 > Frame 170 > Frame 169 > Frame 167 | 604,4024 | 37×47 | no | WIDTH_AND_HEIGHT | Montserrat Bold / 42 / 47px | 1 | "%" | 1 seg uniforme: #141210, ORIGINAL
4101:496 | Frame 255 > Frame 181 > Frame 180 > Frame 171 > Frame 170 > Frame 169 > Frame 168 | 524,4071 | 165×16 | no | HEIGHT | Montserrat Bold / 12 / 16px | 1 | "METODOLOGÍA PRÁCTICA" | 1 seg uniforme: #141210, ORIGINAL
4101:497 | Frame 255 > Frame 181 > Frame 180 > Frame 171 > Frame 170 > Frame 169 > Frame 168 | 524,4091 | 165×16 | no | HEIGHT | Montserrat Regular / 12 / 16px | 1 | "Aprende haciendo" | 1 seg uniforme: #141210, ORIGINAL
4101:500 | Frame 255 > Frame 181 > Grupo 29199 | 228,4167 | 214×19 | no | WIDTH_AND_HEIGHT | Inter Regular / 16 / AUTO | n/a | "Descargar BROCHURE" | 1 seg uniforme: #141210, UPPER
4101:510 | Frame 255 > Frame 253 | 280,4571 | 714×92 | no | HEIGHT | Montserrat Bold / 44 / 46px | 2 | "¿Quieres vivir esta experiencia en la próxima edición?" | 1 seg uniforme: #FFFFFF, ORIGINAL
4101:511 | Frame 255 > Frame 253 | 280,4651 | 613×78 | no | WIDTH_AND_HEIGHT | Inter Regular / 24 / 78px | 1 | "Inicio: 02 de diciembre | Online vía Zoom | 8 Módulos" | 1 seg uniforme: #00C300, ORIGINAL
4101:515 | Frame 255 > Frame 253 > Grupo 29212 > Grupo 29189 | 337,4789 | 201×19 | no | HEIGHT | Inter Regular / 16 / AUTO | n/a | "RESERVA TU VACANTE" | 1 seg uniforme: #0F0F0F, UPPER
4101:518 | Frame 255 > Frame 253 > Grupo 29212 | 677.48,4789 | 228×19 | no | HEIGHT | Inter Regular / 16 / AUTO | n/a | "Hablar con un asesor" | 1 seg uniforme: #FFFFFF, UPPER
4101:522 | 09 Docentes | 410,5074 | 1100×112 | no | NONE | Montserrat Bold / 48 / 56.16px | 1.99 | "Aprende de especialistas en HUMINT, inteligencia y seguridad" | [0-36] "Aprende de especialistas en HUMINT, " #F3F5F7 Bold tc=ORIGINAL ; [36-60] "inteligencia y seguridad" #00C300 Bold tc=ORIGINAL
4101:530 | 09 Docentes > Tarjeta FRANCISCO LÓPEZ | 382,5341 | 150×14 | no | NONE | Barlow Regular / 14 / 14px | 1 | "ESPAÑA" | 1 seg uniforme: #F1F7F7, UPPER
4101:531 | 09 Docentes > Tarjeta FRANCISCO LÓPEZ | 350,5729 | 352×22 | no | NONE | Montserrat Bold / 21 / 22px | 1 | "FRANCISCO LÓPEZ" | 1 seg uniforme: #F1F7F7, UPPER
4101:532 | 09 Docentes > Tarjeta FRANCISCO LÓPEZ | 350,5761 | 352×32 | no | NONE | Inter Light / 15 / 16px | 2 | "Especialista en criminología, inteligencia y análisis de fuentes humanas" | 1 seg uniforme: #FFFFFF@0.62, ORIGINAL
4101:533 | 09 Docentes > Tarjeta FRANCISCO LÓPEZ | 350,5819 | 157×21 | no | NONE | Inter Regular / 13 / 13px | 1.62 | "VER TRAYECTORIA" | 1 seg uniforme: #00C300, UPPER
4101:542 | 09 Docentes > Tarjeta GONZALO CATANZARITI | 816,5341 | 150×14 | no | NONE | Barlow Regular / 14 / 14px | 1 | "COLOMBIA" | 1 seg uniforme: #F1F7F7, UPPER
4101:543 | 09 Docentes > Tarjeta GONZALO CATANZARITI | 784,5729 | 352×22 | no | NONE | Montserrat Bold / 21 / 22px | 1 | "MG. EDUARDO DE LA TORRE" | 1 seg uniforme: #F1F7F7, UPPER
4101:544 | 09 Docentes > Tarjeta GONZALO CATANZARITI | 784,5761 | 352×32 | no | NONE | Inter Light / 15 / 16px | 2 | "Especialista en ciberseguridad, ciberdefensa y análisis digital" | 1 seg uniforme: #FFFFFF@0.62, ORIGINAL
4101:545 | 09 Docentes > Tarjeta GONZALO CATANZARITI | 784,5819 | 157×21 | no | NONE | Inter Regular / 13 / 13px | 1.62 | "VER TRAYECTORIA" | 1 seg uniforme: #00C300, UPPER
4101:554 | 09 Docentes > Tarjeta EDUARDO VELANDIA BECERRA | 1250,5341 | 150×14 | no | NONE | Barlow Regular / 14 / 14px | 1 | "ARGENTINA" | 1 seg uniforme: #F1F7F7, UPPER
4101:555 | 09 Docentes > Tarjeta EDUARDO VELANDIA BECERRA | 1218,5729 | 352×22 | no | NONE | Montserrat Bold / 21 / 22px | 1 | "DANIELA GALVÁN" | 1 seg uniforme: #F1F7F7, UPPER
4101:556 | 09 Docentes > Tarjeta EDUARDO VELANDIA BECERRA | 1218,5761 | 352×32 | no | NONE | Inter Light / 15 / 16px | 2 | "Especialista en investigación criminal e inteligencia digital" | 1 seg uniforme: #FFFFFF@0.62, ORIGINAL
4101:557 | 09 Docentes > Tarjeta EDUARDO VELANDIA BECERRA | 1218,5819 | 157×21 | no | NONE | Inter Regular / 13 / 13px | 1.62 | "VER TRAYECTORIA" | 1 seg uniforme: #00C300, UPPER
