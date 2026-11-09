"""Escribe omar-chehade-datos.json con el texto literal del Figma (437:2).
WJ = U+2060 (word joiner) a ambos lados del guion en los rangos de fechas y en Fujimori-Montesinos, como en Figma."""
import json, os
S = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(S)
WJ = '⁠'
def r(a, b): return f'{a}{WJ}-{WJ}{b}'
FM = r('Fujimori', 'Montesinos')
d = {
 "nombre": {"linea1": "OMAR", "linea2": "CHEHADE"},
 "titular": "Abogado y político peruano. Exsegundo vicepresidente de la República y excongresista de la República del Perú.",
 "especialidades": ["Derecho Constitucional", "Derecho Penal", "Lucha Anticorrupción", "Gobernanza y Políticas Públicas"],
 "especialidades_html": ["Derecho<br>Constitucional", "Derecho Penal", "Lucha<br>Anticorrupción", "Gobernanza y<br>Políticas Públicas"],
 "cifras": [["2011-2012", "Segundo vicepresidente del Perú"], ["2 periodos", "Congresista de la República"], ["3", "Publicaciones"]],
 "resumen": {
  "negrita": "Abogado y político peruano",
  "resto": (f" con trayectoria en el Poder Ejecutivo, el Congreso de la República y la lucha anticorrupción. Fue segundo vicepresidente de la República ({r(2011, 2012)})"
            f" y congresista durante los periodos {r(2011, 2016)} y {r(2020, 2021)}, habiendo presidido la Comisión de Constitución y Reglamento."
            f" Entre 2005 y 2008 trabajó como consultor de la Procuraduría ad hoc Anticorrupción en los casos {FM}."
            " Su experiencia vincula la reforma constitucional, el derecho penal y el diseño normativo con la institucionalidad y las políticas públicas."
            " Es autor de obras sobre la extradición de Alberto Fujimori y sus memorias de gobierno.")},
 "cargos": [
  f"<b>Segundo vicepresidente de la República del Perú</b> ({r(2011, 2012)}).",
  f"<b>Congresista de la República</b> ({r(2011, 2016)} y {r(2020, 2021)}).",
  f"<b>Presidente de la Comisión de Constitución y Reglamento del Congreso de la República</b> ({r(2013, 2014)}).",
  f"<b>Consultor de la Procuraduría ad hoc Anticorrupción</b> para los casos {FM} ({r(2005, 2008)}).",
  "<b>Asesor legal en materia penal</b> del Departamento Jurídico del rectorado de la Universidad Nacional Mayor de San Marcos (2004).",
  "<b>Candidato a la Alcaldía de Lima</b> por Alianza para el Progreso (2022)."],
 "formacion": [
  "<b>Estudios de Derecho</b> en la Universidad Inca Garcilaso de la Vega.",
  "<b>Grado de bachiller en Derecho</b> (1995), con tesis titulada «Reformas necesarias al delito de asesinato en el Código Penal peruano».",
  "<b>Título profesional de abogado</b> (1996)."],
 "aportes": [
  "<b>«Reformas necesarias al delito de asesinato en el Código Penal Peruano»</b> (1995).",
  "<b>«Atrapando al fugitivo: memorias de la histórica extradición de Alberto Fujimori»</b> (2008).",
  "<b>«La gran usurpación. Memorias de gobierno»</b> (2016).",
  f"Participación en <b>tareas anticorrupción</b> vinculadas a los casos {FM} y en trabajo legislativo de <b>reforma constitucional y control político</b>.",
  "Ponente de la <b>2.ª Cumbre Global de Inteligencia + Estrategia 2025</b> de Goberna."],
 "figma": {"fileKey": "VDnG8Ey0gIPBtCqea1kya9", "desktop": "437:2", "laptop": "444:2", "mobile": "447:2", "foto": ["523:1653", "523:1656", "523:1658"]}
}
json.dump(d, open(os.path.join(P, 'omar-chehade-datos.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', json.dumps(d, ensure_ascii=False).count(WJ), 'word joiners')
