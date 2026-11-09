# Landings Goberna en Elementor: cómo trabajamos

Guía para continuar las landings de los diplomas en WordPress con Elementor Pro. Cada sección de la landing es un archivo `.json` que se importa como plantilla. Todas siguen las mismas reglas, así que una sección nueva se arma igual que las que ya están.

## 1. Qué hay

| Landing | Carpeta | Colores y títulos |
|---|---|---|
| Consultor Político | `consultor-elementor/` | Dorado `#C49A45` y azul `#031129`, títulos en Montserrat |
| Asesor Presidencial | `asesor-presidencial-elementor/` | Dorado de 3 tonos (`#CB861B → #F5C02F`), títulos en Montserrat |
| Crimen Organizado y Contraterrorismo | `crimen-organizado-elementor/` | Rojo `#880000` / `#8C1A17`, títulos en Oswald |

Consultor fue la primera y sirve de plantilla: Asesor y Crimen son la misma estructura con otros colores, textos e imágenes.

## 2. Qué trae cada carpeta

| Archivo o carpeta | Qué es |
|---|---|
| `header.json` | Header fijo con logo, menú y botón "Inscríbete ahora" |
| `hero.json` | Portada |
| `barra-datos.json` | Barra con inicio, duración, modalidad y horario |
| `metodologia.json` | Metodología con video |
| `el-programa.json` | El programa, en pestañas |
| `simulador-war-room.json` | War Room (pestañas en desktop, etapas en vertical en mobile) |
| `plan-estudios.json` | Módulos en acordeón (+ cerrado / − abierto) |
| `banner-proxima-edicion.json` | Banner de la próxima edición |
| `docentes.json` | Carrusel de docentes, de 3 en 3, con botones |
| `presencia-internacional.json` | Mapa animado |
| `certificacion.json` | Certificado |
| `inversion.json` | Inversión y formulario |
| `experiencia-goberna.json` | Testimonios en video (sección nueva, ver punto 7) |
| `preguntas-frecuentes.json` | Preguntas frecuentes |
| `imagenes/` | Todas las imágenes de la landing, ya optimizadas (webp/png) |
| `iconos-svg/` | Los íconos originales del diseño |
| `mapa/` | Imagen base del mapa y SVG animado de la sección Presencia internacional |

Algunas carpetas traen archivos extra:
- **Consultor:** `boton-comprar-ahora.json` y `header-css-para-pegar.css` (el CSS del header fijo).
- **Asesor:** `figma-componentes/`, con los componentes descargados del Figma.
- **Asesor (pendiente):** todavía tiene el `testimonios.json` antiguo. Falta cambiarlo por `experiencia-goberna.json`, como ya se hizo en Consultor y Crimen.

## 3. Antes de empezar

- **Elementor Pro activo:** se usan Contenedores, Pestañas anidadas, Acordeón anidado, Carrusel anidado, Formulario y CSS personalizado.
- **Breakpoint Laptop activado:** en *Ajustes del sitio → Diseño → Puntos de interrupción*. Las medidas que usamos:

  | Dispositivo | Ancho |
  |---|---|
  | Desktop | más de 1366 |
  | Laptop | hasta 1366 |
  | Tablet | hasta 1024 |
  | Mobile | hasta 767 |

- **Fuentes:** Montserrat, Inter y Oswald desde Google Fonts. Es lo que hace Elementor por defecto.

## 4. Cómo importar una sección

1. Ve a *Plantillas → Plantillas guardadas → Importar plantillas* y sube el `.json`.
2. En la página, abre la biblioteca (ícono de carpeta) y entra a *Mis plantillas*.
3. Pulsa **Insertar** en la sección.
4. Para actualizar una sección que ya está en la página, borra la vieja e inserta la nueva. Si solo cambió el CSS, a veces basta con pegarlo en *Avanzado → CSS personalizado* del contenedor.

## 5. Imágenes

- **Placeholders:** en los JSON las imágenes vienen como placeholders de `placehold.co` y cada uno muestra el nombre del archivo que va ahí, por ejemplo `testimonio-thumb-alina.webp`.
- **Reemplazo:** busca ese archivo en `imagenes/`, súbelo a la Biblioteca de medios y cámbialo en el widget o en el fondo del contenedor.
- **Íconos:** vienen como íconos de Font Awesome provisionales. Se cambian por los SVG de `iconos-svg/` con *Subir SVG* en el widget. Así no se duplican al reimportar.
- **SVG animado del mapa:** WordPress solo deja subirlo si está activada la subida de SVG, en *Elementor → Ajustes → Avanzado*.

## 6. Reglas de la estructura

Hay que respetarlas en todo lo nuevo para que las secciones se comporten igual.

1. **Contenedor en caja de 1300 px:** todas las secciones van en un contenedor padre con *Ancho del contenido: En caja* y ancho 1300.
2. **Anchos explícitos en filas:** los hijos de un contenedor en fila llevan ancho explícito (%, px o auto). Elementor les pone 100% por defecto y el contenido se desborda.
3. **Widgets nativos para el contenido:** encabezado, editor de texto, imagen, botón, pestañas, acordeón y carrusel. El widget HTML se usa solo cuando hace falta un `<script>` o un reproductor, como en Experiencia Goberna.
4. **Nada de "Ocultar en Móvil/Desktop/…":** Elementor pinta esos elementos en gris rayado en el editor. Lo que cambia por dispositivo se oculta con CSS en el *CSS personalizado* de la sección.
5. **Clases `ak-…`:** el CSS de cada sección se apoya en clases que empiezan con `ak-` (*Avanzado → Clases CSS*). Si borras o renombras una, se rompe el estilo o la función. Si duplicas un elemento, la clase se copia con él.
6. **CSS de la sección:** va en *Avanzado → CSS personalizado* del contenedor padre y usa `selector` para que solo afecte a esa sección.
7. **Mobile:** el XD mobile mide 430 px y Elementor mobile ~375. Por eso los tamaños de letra mobile van al 87% del XD, y los JSON ya los traen escalados. Revisa siempre la vista mobile a 375.
8. **Textos:** con tildes y eñes correctas. Si el diseño trae una errata (nombres, países, mayúsculas sueltas), se corrige en el JSON y se avisa.

## 7. Sección nueva: Experiencia Goberna (testimonios en video)

Reemplaza a la antigua sección de Testimonios. Ya está en Consultor y en Crimen.

### Cómo funciona

- **Izquierda:** un panel cuadrado con una imagen de la landing.
- **Derecha:** "Experiencia Goberna", el título, el párrafo, la pestaña "Voces" y 3 miniaturas.
- **Al hacer clic en una miniatura:** el video se reproduce en el panel. Lleva barra de progreso fina, pausa, volumen, tiempo y pantalla completa, con el estilo del player de cms.goberna.club. La miniatura queda marcada como "Reproduciendo".
- **Formato del video:** si es vertical, los costados del panel se rellenan con el mismo video difuminado. Los cuadrados ocupan todo el panel.
- **En mobile:**
  - el orden es texto → panel → miniaturas;
  - las miniaturas son un carrusel con 3 puntitos;
  - en el panel se puede deslizar con el dedo o usar las flechas ‹ › para pasar de un video a otro.

### Cómo está armado

- Todo lo visible es nativo: textos, miniaturas, banderas y la imagen de fondo del panel.
- Hay **un solo widget HTML**, dentro del panel, con el reproductor y el script. El script también crea los puntitos de mobile.
- Los videos **no** van por iframe. El player de cms.goberna siempre se muestra en 16:9, así que un video vertical queda chiquito con franjas negras. Por eso se usa el mp4 directo.

### Cambiar los videos

En el widget HTML, al inicio del script, está la lista `VIDEOS`, en el **mismo orden que las miniaturas**:

```js
var VIDEOS=["https://cms.goberna.club/public/01_....mp4", "...", "..."];
```

Para sacar el mp4 de un link de embed, cambia `/embed/` por `/public/` y quita el `?cfg=...`:

```
https://cms.goberna.club/embed/02_cuadrado_final_lorena.mp4?cfg=f9b4ee0a-...
→ https://cms.goberna.club/public/02_cuadrado_final_lorena.mp4
```

Si cambias una persona:
1. Cambia también su miniatura, bandera, nombre y país en la tarjeta nativa.
2. Mantén el mismo orden que en `VIDEOS`.

### Clases que no se deben tocar

| Clase | Elemento |
|---|---|
| `ak-vsec` | Contenedor padre |
| `ak-vp` | Panel |
| `ak-vr` | Columna derecha |
| `ak-veye` | Antetítulo "Experiencia Goberna" |
| `ak-vh2` | Título |
| `ak-vtxt` | Párrafo |
| `ak-vtab` | Pestaña "Voces" |
| `ak-vthumbs` | Fila de miniaturas |
| `ak-vt` | Cada tarjeta |
| `ak-vt-im` | Miniatura |
| `ak-vt-nm` | Bandera y nombre |

### Imágenes a subir

| Landing | Fondo del panel | Miniaturas | Banderas |
|---|---|---|---|
| Consultor | `testimonios-consultor-promo.webp` | `testimonio-thumb-alina/lorena/miguel.webp` | `bandera-colombia.png`, `bandera-bolivia.png`, `bandera-mexico-circulo.png` |
| Crimen | `testimonios-crimen-promo.webp` | `testimonio-thumb-dienys/francisco/pablo.webp` | `bandera-puerto-rico.png`, `bandera-bolivia.png`, `bandera-ecuador.png` |

El difuminado de los costados sale del mismo video, así que no necesita imagen aparte.

## 8. Pendientes conocidos

- **Asesor Presidencial:** cambiar `testimonios.json` por la sección Experiencia Goberna.
- **Crimen Organizado:**
  - El hero todavía usa el título antiguo. El nuevo título es "Estrategias contra el Crimen Organizado y **de** Contraterrorismo", con el tag "Diploma Internacional" incluido en la imagen.
  - Docentes: las 3 tarjetas son provisionales y faltan los docentes reales.
  - El programa: los textos de las pestañas 2 y 3 son provisionales.
  - Plan de estudios: las descripciones de los módulos 2 a 8 son una propuesta y hay que validarlas.
  - Preguntas frecuentes: las respuestas 2 a 5 son adaptadas y hay que validarlas.
  - Fechas: el XD trae "31 Oct / 4 semanas" y el hero "09 Nov / 8 módulos · 3 semanas". Se usó lo del hero; falta confirmar cuál es el correcto.
- **Antes de publicar cualquier sección nueva**, revisarla en Elementor en Desktop, Laptop (1366) y Mobile (375).
