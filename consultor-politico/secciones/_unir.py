"""Vuelve a armar la landing completa a partir de las secciones.

Uso:
    python _unir.py                      -> escribe _landing-completa.json
    python _unir.py <original.json>      -> además compara con el original

El archivo completo lleva type "page" (Elementor lo importa como página
completa, con page_settings/custom_css). Sale compacto, como el original.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(HERE, "_landing-completa.json")

SECCIONES = [
    "00-header", "01-hero", "02-barra-datos", "03-metodologia",
    "04-diploma", "05-war-room", "06-plan-estudios", "07-cta",
    "08-docentes", "09-presencia", "10-certificacion", "11-inversion",
    "12-doble-certificacion", "13-testimonios", "14-faq",
    "15-newsletter", "16-footer",
]

# Metadatos de primer nivel del original (no están en las secciones)
TITLE = "Diploma Consultor Politico 2026"
TYPE = "page"


def leer(nombre):
    with open(os.path.join(HERE, nombre + ".json"), encoding="utf-8") as f:
        return json.load(f)


def unir():
    primera = leer(SECCIONES[0])
    contenido = []
    for nombre in SECCIONES:
        parte = leer(nombre)
        assert parte["version"] == primera["version"], nombre
        assert parte["template_type"] == primera["template_type"], nombre
        assert parte["type"] == "section", nombre
        assert len(parte["content"]) == 1, nombre
        contenido.append(parte["content"][0])

    with open(os.path.join(HERE, "_page-settings.json"), encoding="utf-8") as f:
        page_settings = json.load(f)

    return {
        "version": primera["version"],
        "title": TITLE,
        "type": TYPE,
        "content": contenido,
        "page_settings": page_settings,
        "template_type": primera["template_type"],
    }


def comprobar(original, completa):
    # Eje2 cambió la 04: el resto de secciones debe ser idéntico al original
    for i, (a, b) in enumerate(zip(original["content"], completa["content"])):
        if i != 4:
            assert a == b, "content[%d] distinto del original" % i
    print("content[i] == original[i] para i != 4: True")
    print("page_settings == original:", original["page_settings"] == completa["page_settings"])
    print("version/title/template_type == original:",
          all(original[k] == completa[k] for k in ("version", "title", "template_type")))


def main():
    completa = unir()
    with open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(completa, ensure_ascii=False, separators=(",", ":")))
    print("escrito:", SALIDA)

    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            original = json.load(f)
        comprobar(original, completa)


if __name__ == "__main__":
    main()
