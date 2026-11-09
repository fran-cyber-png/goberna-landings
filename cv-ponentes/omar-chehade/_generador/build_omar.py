import base64, os, sys
S = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(S)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(S, 'omar-preview.html')
def uri(rel):
    b = open(os.path.join(P, rel), 'rb').read()
    return 'data:image/webp;base64,' + base64.b64encode(b).decode()
MAP = {
    '__BG_D__': 'imagenes/hero-fondo-capitolio.webp',
    '__BG_M__': 'imagenes/hero-fondo-movil.webp',
    '__FOTO__': 'imagenes/omar-chehade.webp',
    '__LOGO__': 'imagenes/logo-goberna.webp',
    '__I_CON__': 'iconos-webp/icono-derecho-constitucional.webp',
    '__I_PEN__': 'iconos-webp/icono-derecho-penal.webp',
    '__I_LUC__': 'iconos-webp/icono-lucha-anticorrupcion.webp',
    '__I_GOB__': 'iconos-webp/icono-gobernanza-politicas.webp',
    '__H_RES__': 'iconos-webp/icono-resumen.webp',
    '__H_CAR__': 'iconos-webp/icono-titulo-cargos.webp',
    '__H_FOR__': 'iconos-webp/icono-formacion.webp',
    '__H_APO__': 'iconos-webp/icono-aportes.webp',
    '__V_DOT_M__': 'iconos-webp/vineta-movil.webp',
    '__V_ARR_M__': 'iconos-webp/vineta-grande-movil.webp',
    '__V_DOT__': 'iconos-webp/vineta.webp',
    '__V_ARR__': 'iconos-webp/vineta-grande.webp',
    '__BARRA_D__': 'iconos-webp/barra-especialidades-desk.webp',
    '__BARRA_M__': 'iconos-webp/barra-especialidades-movil.webp',
}
t = open(os.path.join(S, 'omar-tpl.html'), encoding='utf-8').read()
for k, rel in MAP.items():
    n = t.count(k)
    t = t.replace(k, uri(rel))
    print(k, n)
open(OUT, 'w', encoding='utf-8').write(t)
print('bytes', len(t.encode('utf-8')), 'tokens restantes:', [x for x in MAP if x in t] or 'ninguno', '__' in t)
