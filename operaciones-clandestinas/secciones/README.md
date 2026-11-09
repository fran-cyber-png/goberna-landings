# Secciones – Operaciones Clandestinas

Origen: `jet-woo-builder-91793-2026-11-02 (1).json` (plantilla JetWooBuilder, Elementor 0.4).
Cada archivo es una sección importable por separado en Elementor (Plantillas > Importar), con `"type": "section"`.
El contenido de cada sección es idéntico al original (sin cambios).

| # | Archivo | Sección (`_title`) | ID contenedor |
|---|---------|--------------------|---------------|
| 01 | 01-menu.json | menu | 5a050fd |
| 02 | 02-hero.json | hero | 88939a1 |
| 03 | 03-informacion-rapida.json | informacion rapida | cb729d2 |
| 04 | 04-informacion-de-curso.json | informacion de curso | 975a67b |
| 05 | 05-publico-objetivo.json | publico objetivo | b485259 |
| 06 | 06-metodologia.json | metodologia | f49a1ee |
| 07 | 07-ponente.json | ponente | 5621006 |
| 08 | 08-temario.json | temario | de73b7a |
| 09 | 09-call-to-action.json | call to action | 6e7f237 |
| 10 | 10-certificacion.json | certificacion | aa5d5d5 |
| 11 | 11-inversion.json | inversion | 4d29e99 |
| 12 | 12-doble-certificacion.json | doble certificacion | cd2fd51 |
| 13 | 13-faq.json | faq | cd2a90c |
| 14 | 14-footer-newsletter.json | (sin título – newsletter, enlaces y redes) | 6ce7673c |
| 15 | 15-footer-legal.json | (sin título – copyright y redes sociales) | 5b13fa67 |

Notas de dependencias entre secciones:
- `03-informacion-rapida` se superpone al final del `02-hero` mediante margen negativo (margin top -120px escritorio/laptop, -309px móvil); revisar ambas juntas.
- `01-menu` usa margen inferior negativo (-80px escritorio / -70px móvil) para quedar encima del hero.
