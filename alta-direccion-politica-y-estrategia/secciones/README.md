# Secciones — Programa Superior Contrainteligencia y operaciones especiales

Origen: `jet-woo-builder-91989-2026-10-30.json` (Elementor 0.4, plantilla `jet-woo-builder`, 14 contenedores raíz).

Cada archivo es una plantilla Elementor independiente (`type: container`) con una sola sección,
importable desde **Plantillas → Plantillas guardadas → Importar plantillas**.

| # | Archivo | Sección | Contenido | Ancla | Widgets |
|---|---|---|---|---|---|
| 01 | `01-header.json` | Header / menú sticky | Logo, menú de navegación y botón «Inscríbete ahora» | — | image×1, nav-menu×1, button×1 |
| 02 | `02-hero.json` | Hero | Titular «Anticipa amenazas…», botones «Quiero información» y «Descarga brochure» | — | button×2, image×1, text-editor×1 |
| 03 | `03-datos-clave.json` | Datos clave del programa | Tarjetas con ícono: modalidad online, etc. | — | icon×4, heading×4 |
| 04 | `04-video-vision.json` | Video / magnitud del programa | «Conoce la visión detrás del programa» + video embebido (HTML) | — | heading×2, text-editor×1, html×1 |
| 05 | `05-vision-objetivos.json` | Visión del programa | Visión, objetivos y pestañas (nested-tabs) con lista de beneficios | — | heading×3, divider×3, icon×3, text-editor×3, nested-tabs×1, icon-list×1 |
| 06 | `06-metodologia.json` | Metodología de aprendizaje | #metodologia — pasos Analiza/… con imágenes | #metodologia | heading×7, image×4, text-editor×4 |
| 07 | `07-ponentes.json` | Ponentes | Carrusel (nested-carousel) de especialistas con foto, país y botones | — | image×24, text-editor×16, button×10, heading×9, nested-carousel×1, html×1 |
| 08 | `08-plan-de-estudio.json` | Plan de estudio | #programa — 4 etapas con acordeones de módulos | #programa | heading×11, text-editor×10, icon-list×4, nested-accordion×4, icon×2 |
| 09 | `09-proyecto-final.json` | Proyecto final | «Análisis estratégico de amenazas y respuesta operacional» | — | heading×7, icon×4, text-editor×1, divider×1 |
| 10 | `10-certificacion.json` | Certificación / diploma | #diploma — certificación y verificación digital | #diploma | text-editor×3, divider×2, icon×2, heading×1, image×1 |
| 11 | `11-inversion.json` | Inversión | #inversion — precio $199.00 USD, botón y formulario | #inversion | heading×6, spacer×3, divider×2, button×1, form×1 |
| 12 | `12-faq.json` | Preguntas frecuentes | Acordeón de FAQs | — | text-editor×6, heading×2, divider×1, nested-accordion×1 |
| 13 | `13-footer.json` | Footer / newsletter | Formulario de newsletter, oficinas por país y contactos | — | heading×7, icon-list×7, icon×5, form×1, image×1 |
| 14 | `14-copyright.json` | Barra de copyright | Derechos reservados + redes sociales | — | heading×1, social-icons×1 |

Nota: `13-footer.json` pesa ~1.4 MB porque los widgets de ícono guardan SVGs grandes en `htmlCache`
(caché de render de Elementor); no afecta la importación.
