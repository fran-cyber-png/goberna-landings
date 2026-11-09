# Protocolo: adaptar contenido a una plantilla Figma (SOLO REEMPLAZAR TEXTOS)

> Protocolo reutilizable para todos los proyectos de landing en los que se adapta el contenido de un documento (PDF, Word, etc.) a una plantilla de Figma existente.
> Se basa en la **v2 de "Consultor Político Senior"** (2026-10-19), que fue el método aprobado. La v1 se rechazó porque modificó el diseño.

---

## 0. Regla de oro

**Solo se cambia la propiedad `characters` de las capas de texto que ya existen. La plantilla no se toca.**

El resultado final debe ser **idéntico a la plantilla en estructura**:

- mismas secciones, frames, alturas, espaciados, posiciones, componentes, colores e imágenes;
- lo único distinto es el contenido de los textos.

> "Destruiste el diseño, la idea era SOLO REEMPLAZAR TEXTOS, no modificar el diseño de la plantilla."
> "No quiero que agregues más texto, solo reemplaza los textos que hay y que se adapte el PDF sin deformar texto ni estructura."
> "Vuelve a la estructura de la plantilla sin alargar espacios, déjalos como estaban."

---

## 1. Roles (flujo de dos sesiones)

| Sesión | Rol |
|---|---|
| **Diseño-Ins** (inspector) | Analiza el documento y la plantilla, hace las preguntas al usuario, asigna tareas a Eje, verifica cada reporte con renders y diffs e itera hasta que no haya errores, bugs ni desbordes. **No edita Figma directamente.** |
| **Diseño-Eje** (ejecutor) | Ejecuta en Figma exactamente lo que se le asigna y envía un reporte detallado. **No decide cambios de diseño por su cuenta.** |

- La comunicación es por `SendMessage`. Si Eje se reinicia, su referencia cambia: hay que responder siempre a la dirección `from` de su último mensaje.
- Si el usuario pausa a Eje, **no se le envía nada** hasta que el usuario diga que se puede retomar.

---

## 2. Antes de asignar cualquier tarea: preguntas al usuario

**Hay que hacer TODAS las preguntas antes de enviar la primera tarea a Eje** (con AskUserQuestion). No se envía nada sin alineación.

Checklist de preguntas:

1. **Archivos:** link del archivo Figma, frame base de la plantilla y ruta del documento de contenido.
2. **Estados ocultos:** ¿hay frames de estado (tabs, acordeones, variantes) que también se deban copiar y adaptar? Por ejemplo, en v2 eran "Frame 128" y "Frame 129".
3. **Secciones del documento sin espacio en la plantilla:** ¿se omiten? Ejemplo: San Marcos no iba.
4. **Secciones de la plantilla sin contenido en el documento:** ¿se dejan como están o se eliminan? Ejemplos: mapa, comunidad, estadísticas.
5. **Más ítems que slots:** por ejemplo, 11 módulos para 3 tarjetas, o 1 ponente para 3 tarjetas. ¿Se llenan solo los slots disponibles?
6. **Imágenes, logos y fotos:** por defecto están **fuera de alcance**. Solo se tocan si el usuario lo pide explícitamente.
7. **Header, footer y menú:** ¿se mantienen intactos?
8. **Textos resaltados o marcados** en el documento: ¿qué significan?
9. **Estilo de titulares:** ¿texto literal o condensado? ¿Palabras clave en rojo como en la plantilla?
10. **Aprobación:** ¿por fase o al final?

Si una respuesta implicara cambiar el diseño, **no se ofrecen opciones de rediseño**. Solo se pregunta qué hacer dentro de la estructura existente.

---

## 3. Lo que está PERMITIDO y PROHIBIDO

### Permitido
- Cambiar `characters` de capas de texto existentes, incluidas las de frames ocultos y estados.
- Mantener los estilos mixtos del texto original, como palabras en rojo, negritas o saltos de línea. Hay que reaplicarlos sobre la parte equivalente del nuevo texto.
- Renombrar capas cuyo nombre no coincide con su contenido, solo como ayuda de trabajo.
- Correcciones mínimas para que un texto **no se superponga** por culpa del auto-layout. En v2 fue el "USD" del bloque de pago, que se puso en posicionamiento absoluto conservando el gap original. Siempre hay que reportarlas.

### Prohibido (salvo pedido explícito del usuario)
- Cambiar alturas, anchos, paddings, gaps o posiciones de frames y secciones.
- Agregar capas, textos, bloques, overlays, banderas, timers, etc.
- Eliminar bloques de diseño.
- Cambiar componentes, por ejemplo carrusel → tarjeta única.
- Igualar alturas o "acomodar" secciones.
- Cambiar tamaño de fuente, interlineado, tracking o ancho de caja para que un texto entre.
- Cambiar colores, fondos o imágenes.
- Agregar texto donde la plantilla no tiene una capa.

---

## 4. Regla de ajuste del texto (la más importante)

**Cada texto nuevo debe ocupar EXACTAMENTE el mismo número de líneas y la misma altura que el texto que reemplaza.**

1. Si el texto del documento cabe igual, va **literal**.
2. Si es más largo, se **condensa usando las propias palabras del documento**:
   - sin ideas nuevas;
   - sin inventar datos;
   - se propone la versión condensada al usuario para que la apruebe.
3. Si es más corto y deja la caja con menos líneas, se ajusta con palabras del propio documento hasta igualar las líneas, o se consulta.
4. Si después de reemplazar **cambia la altura** de la capa o de su contenedor, **se restaura el texto original** y se reporta para buscar otra versión.
5. Las listas se adaptan con la misma cantidad de ítems y el mismo largo aproximado. Si sobran ítems en el documento, se pregunta cuáles van.
6. Los datos clave (fechas, precios, número de módulos, duración, modalidad) deben ser **consistentes en toda la landing**: hero, CTA, pago, módulos, etc.

---

## 5. Procedimiento de ejecución (Eje)

1. **Duplicar** el frame de la plantilla y sus frames de estado (tabs). Se nombran `NOMBRE PROYECTO – vN` y se colocan lejos de la plantilla, sin solaparse. **Nunca se trabaja sobre la plantilla original.**
2. **Volcado inicial:** listar TODAS las capas de texto de la copia, incluidas las ocultas, con `id | ruta relativa | x,y | ancho×alto | oculto | characters`.
   - ⚠️ Los nombres de capa de la plantilla **NO coinciden con su contenido**. Hay que mapear siempre por ruta y contenido, nunca por nombre.
3. **Registrar la altura original** de cada capa de texto y de cada frame de sección.
4. **Reemplazar** solo `characters` (cargando antes las fuentes) y reaplicar los rangos de estilo mixto: color rojo, negrita, etc.
5. **Validar cada capa** después del reemplazo:
   - misma altura;
   - mismo número de líneas;
   - sin desborde horizontal;
   - sin superposición con capas vecinas.
   Si falla, se restaura y se anota.
6. **Validar los frames:** la altura total de cada copia debe ser idéntica a la de la plantilla. Ejemplo v2: 10829 / 717 / 717.
7. **Reporte a Ins** con:
   - tabla `id | texto anterior | texto nuevo | altura antes → después | líneas antes → después`;
   - textos restaurados y su motivo;
   - cualquier cambio no textual, con justificación (debería ser ninguno o mínimo);
   - **volcado literal de los textos ocultos**, para que Ins los compare con el documento;
   - alturas finales de los frames.

---

## 6. Verificación (Ins)

**Nunca se acepta un reporte de Eje sin verificarlo.** Hubo afirmaciones falsas, por ejemplo:

- que el diploma decía "Director de Seguridad";
- un desplazamiento "+92 px" que el auto-layout ignoró;
- grupos ocultos con texto viejo de la plantilla.

1. **Render a resolución completa** (`get_screenshot` con `maxDimension` = alto del frame) de la plantilla y de la copia.
2. **Diff de píxeles** entre la plantilla y la copia, y entre renders sucesivos (PIL `ImageChops.difference`, umbrales 30 y 6). Solo deben cambiar las **bandas de texto previstas**: ni fondos, ni imágenes, ni espaciados.
3. **Recortes por sección** para leer cada texto y revisar:
   - errores ortográficos;
   - desbordes y cortes;
   - superposiciones;
   - texto viejo de la plantilla que haya quedado;
   - consistencia de los datos clave.
4. **Textos ocultos:** `get_screenshot` los renderiza en blanco, así que se comparan con el volcado literal que pidas a Eje.
5. **Alturas:** se comparan con `get_metadata` frente a la plantilla.
6. Si hay errores, se arma una **ronda de corrección numerada** (C1, C2…) y se repite hasta que quede limpio.
7. Al terminar, se entrega al usuario un link directo al frame y un resumen de qué textos se adaptaron, condensaron u omitieron.

---

## 7. Trampas técnicas conocidas

- **Auto-layout:** la X/Y de un hijo dentro de auto-layout se ignora. Para mover un elemento sin romper el flujo hay que usar `layoutPositioning = "ABSOLUTE"`, y solo si es imprescindible y se reporta.
- **Nombres de capa obsoletos:** en la plantilla no reflejan el contenido. Se puede renombrar en la copia para trabajar mejor.
- **Frames de estado ocultos:** los tabs son frames aparte que también hay que copiar y adaptar con los mismos textos compartidos, como el titular del programa ×3.
- **Estilos mixtos:** al reemplazar `characters` se pierde el color por rango. Hay que reaplicar el rojo a las palabras clave equivalentes.
- **Fondos:** si el diff muestra un cambio de color de fondo que nadie pidió, se investiga **sin revertir** y se pregunta al usuario si fue él.
- **Imágenes:** solo se tocan si el usuario lo pide explícitamente. Si lo pide, por ejemplo poner la foto de un ponente "con el mismo estilo que otra tarjeta", se replican:
  - el `scaleMode`/`imageTransform` y el encuadre de busto de la tarjeta de referencia;
  - el fondo (por ejemplo, degradado azul oscuro);
  - la posición del bloque de texto.
  Además, hay que verificar que el nombre y la especialidad no queden sobre la cara.

---

## 8. Datos del proyecto (rellenar en cada proyecto nuevo)

```
Proyecto:
Archivo Figma (fileKey / link):
Frame plantilla:              Frames de estado:
Documento de contenido:
Copia de trabajo (ids):
Secciones excluidas:
Secciones sin contenido (qué se hace):
Ítems > slots (decisión):
Imágenes en alcance: NO (salvo: ...)
Aprobación: por fase / al final
```

### Referencia: proyecto Consultor Político Senior (v2 aprobada como método)
- Figma `U7Yptbrr78gGs13LCGGbZ5`.
- Plantilla `310:26` + estados `318:710` / `318:775`.
- Copia v2 `357:27` (1920×10829) + `357:665` / `357:731` (1920×717).
- Contenido: `CONTENIDO LANDINGS (4).pdf`.
