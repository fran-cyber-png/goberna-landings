# Handoff para CII-WP: actualización desde `CONTENIDO LANDINGS (7).pdf` (2026-10-24)

Fuentes:
- PDF nuevo: `C:\Users\Consultoría\Downloads\CONTENIDO LANDINGS (7).pdf`
- Texto extraído en UTF-8: `_work\pdf7.txt`. Sustituye a `_work\pdf.txt`, que viene del PDF (6).

Figma: la versión desktop `4005:17` ya está actualizada y verificada (F2). El detalle está en `F2-mapa-actualizacion.md` y `F2-reporte.md`.

## Qué cambió entre el PDF (6) y el (7)
Diff de texto completo; no cambia nada más.

### 1. Fecha de inicio
La fecha pasa de **12 de octubre** a **09 de diciembre**. Hay que cambiarla en todos los lugares donde aparezca:
- barra del hero;
- CTA "Inicio: 09 de diciembre | Online vía Zoom | 8 Módulos";
- bloque de inversión;
- formulario o temporizador, si lo usan.

### 2. Módulos
Los 8 módulos tienen descripción, "Aprenderás" y "Aplicarás" nuevos. Los títulos no cambian.

| Módulo | Descripción | Aprenderás | Aplicarás |
|---|---|---|---|
| 1 · Fundamentos de Inteligencia y Contrainteligencia | Comprende cómo funciona la inteligencia y cuál es el papel de la contrainteligencia en la protección de una organización. | Principios de inteligencia, ciclo de inteligencia, fundamentos y procesos de contrainteligencia. | Análisis del ciclo de inteligencia e identificación de medidas para proteger información y capacidades críticas. |
| 2 · Inteligencia Estratégica | Transforma información en conocimiento útil para anticipar escenarios y respaldar decisiones de alto nivel. | Hipótesis, modelos de análisis, indicadores de alerta, prospectiva e inteligencia estratégica. | Construcción de escenarios e indicadores para detectar riesgos y sustentar decisiones estratégicas. |
| 3 · OSINT: Inteligencia de Fuentes Abiertas | Aprende a buscar, verificar y organizar información pública para convertirla en un insumo confiable de inteligencia. | Fuentes abiertas, motores de búsqueda, técnicas de búsqueda, validación y organización de información. | Proceso de búsqueda y verificación de información para construir un producto de análisis OSINT. |
| 4 · SOCMINT, Ciberinteligencia y Ciberseguridad | Comprende cómo el entorno digital genera nuevas fuentes de información, pero también nuevas vulnerabilidades. | SOCMINT, seguridad de la información, comunicaciones seguras, criptografía, IA, IoT y riesgos digitales. | Identificación de amenazas y vulnerabilidades digitales para fortalecer la protección de información estratégica. |
| 5 · COMINT: Inteligencia de Comunicaciones | Conoce cómo la información proveniente de comunicaciones puede convertirse en inteligencia relevante para la seguridad y la toma de decisiones. | Principios de COMINT, procesamiento de señales de comunicación, análisis de información y detección de amenazas. | Interpretación de información de comunicaciones para identificar señales y apoyar evaluaciones estratégicas. |
| 6 · HUMINT: Inteligencia de Fuentes Humanas | Comprende el valor de las fuentes humanas dentro del ciclo de inteligencia y aprende a evaluar la información que proporcionan. | Principios de HUMINT, protocolos, métodos de obtención y tipos de investigación con fuentes humanas. | Evaluación y organización de información proveniente de fuentes humanas dentro de un proceso de inteligencia. |
| 7 · Operaciones Psicológicas y Psicosociales | Analiza cómo las percepciones, narrativas y comportamientos pueden influir en escenarios políticos, sociales y de seguridad. | Operaciones psicológicas, rumor, contrapropaganda, audiencias y dinámicas de influencia. | Desarrollo de un proyecto de operaciones psicológicas y psicosociales aplicado a un escenario estratégico. |
| 8 · Inteligencia aplicada a conflictos sociales y crimen organizado | Integra capacidades de inteligencia para interpretar amenazas, anticipar escenarios críticos y apoyar respuestas coordinadas. | Análisis de amenazas, anticipación de escenarios de violencia, coordinación institucional y gestión estratégica de inteligencia. | Diseño de un plan de acción frente a un escenario de conflicto social o crimen organizado. |

## Diferencias deliberadas en Figma (no hay que copiarlas a WP)
- En Figma, el "Aplicarás" del módulo 1 se condensó a "Identificación de medidas para proteger información y capacidades críticas.", porque la caja de Figma tiene alto fijo y solo admite 2 líneas.
- En Elementor el texto fluye, así que conviene usar el **literal del PDF** (tabla de arriba), salvo que el usuario diga otra cosa.
- En Figma solo el módulo 1 está desplegado y los módulos 4 a 8 no tienen capa. En Elementor, si el acordeón tiene los 8 módulos, hay que integrar los 8.
