# CD-WP1: íconos SVG con la paleta de Carrera (lo escribe CD-WP1)
# Archivos en carrera-diplomatica\iconos\ (versiones Carrera, según el Figma 2002:21):
#   plan (cajas #DD0005 al 80 % con ícono blanco)  -> nodos 2002:481, 2002:492, 2002:507
#   barra de datos (#DD0005)                      -> 2002:119, 2002:106, 2002:132, 2002:140
#   medalla de certificación (#DD0005)            -> 2002:416, 2002:426
# Las URL apuntan a la Biblioteca de medios con id '' (los ids reales se pondrán al subir los archivos).
icon_svg('38e590e4', 'plan-modulos-caja-4-1-carrera-diplomatica.svg')
icon_svg('9081977', 'plan-horas-caja-4-1-carrera-diplomatica.svg')
icon_svg('2d10cc66', 'plan-metodologia-caja-4-1-carrera-diplomatica.svg')
icon_svg('3e247b14', 'barra-modalidad-1-carrera-diplomatica.svg')
icon_svg('1466ad22', 'barra-inicio-1-carrera-diplomatica.svg')
icon_svg('54ba9d28', 'barra-horario-1-carrera-diplomatica.svg')
icon_svg('37b97c47', 'barra-duracion-1-carrera-diplomatica.svg')
icon_svg('940608c', 'certificacion-medalla-1-carrera-diplomatica.svg')
icon_svg('1adb523', 'certificacion-medalla-1-carrera-diplomatica.svg')

# CD-WP1 (mobile): el rótulo "Metodología práctica" traía un margen móvil de Director (top 08 / bottom -8)
# que lo bajaba 15 px y lo pegaba a "Aprende haciendo". Se iguala a los rótulos hermanos (-7 px, sin margen inferior).
# Solo cambia el breakpoint móvil (932 px en la vista previa, igual que el resto de la sección).
margin('4475c46', '_mobile', top=-7, bottom=0)

# CD-WP1 (certificación, escritorio ≥1367): el bloque de la derecha se centra verticalmente en la sección.
# Antes: 97u arriba y 17u abajo (no centrado). Ahora relleno igual arriba y abajo, 24u como mínimo;
# el justify-content:center de la columna reparte el resto. Horizontal, tamaños y espacios internos no cambian.
css_sub('54c4c5af', 'selector > .ak-cert-txt { align-items: flex-start !important; padding: calc(var(--u) * 97) calc(var(--u) * 60) calc(var(--u) * 17) calc(var(--u) * 79) !important; }',
        'selector > .ak-cert-txt { align-items: flex-start !important; padding: calc(var(--u) * 24) calc(var(--u) * 60) calc(var(--u) * 24) calc(var(--u) * 79) !important; }')
