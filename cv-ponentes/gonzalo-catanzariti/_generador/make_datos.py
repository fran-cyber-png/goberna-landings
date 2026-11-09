"""Escribe gonzalo-catanzariti-datos.json con el texto literal del Figma (532:2 / 538:2).
WJ = U+2060 (word joiner) a ambos lados de la raya en 2019–2026, como en Figma.
Resumen sin punto final y sin la viñeta suelta de la hoja (decisión del usuario)."""
import json, os
S = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(S)
WJ = '⁠'
R = ' — '  # raya entre puesto y organización
def it(b, rest): return f'<b>{b}</b>{rest}'
d = {
 "nombre": {"linea1": "GONZALO", "linea2": "CATANZARITI"},
 "titular": "Especialista en ciberinteligencia, investigación digital y análisis del cibercrimen",
 "especialidades": ["Arquitectura de Ciberseguridad", "Investigación de Ciberdelitos", "Informática Forense", "OSINT y SOCMINT"],
 "especialidades_html": ["Arquitectura de<br>Ciberseguridad", "Investigación de<br>Ciberdelitos", "Informática<br>Forense", "OSINT y SOCMINT"],
 "cifras": [["Desde 2013", "Pericias informáticas y evidencia digital"], ["Líder", "Arquitectura de Ciberseguridad en Banco Comafi"],
            ["2 licenciaturas", "Seguridad TIC y Seguridad Marítima"]],
 "resumen": {
  "negrita": "Gonzalo Catanzariti es licenciado en Seguridad en Tecnologías de la Información y las Comunicaciones y licenciado en Seguridad Marítima.",
  "resto": (" Su trayectoria combina la investigación judicial de ciberdelitos y la informática forense en la Prefectura Naval Argentina con la protección de activos"
            " de información en el sector financiero. Desde marzo de 2025 lidera el equipo de Arquitectura de Ciberseguridad de Banco Comafi, supervisando la seguridad"
            " de proyectos tecnológicos, entornos cloud, gestión de vulnerabilidades y DevSecOps. Complementa su experiencia con docencia universitaria en ciberseguridad,"
            " evidencia digital y herramientas de inteligencia")},
 "cargos": [
  it("Líder de Arquitectura de Ciberseguridad", R + "Banco Comafi (desde 2025): conducción de equipos de IT Advisor, Business Advisor y DevSecOps; definición de estándares y supervisión de implementaciones tecnológicas."),
  it("Arquitecto de Ciberseguridad", R + "Banco Comafi (desde 2022): evaluación de proyectos, planificación de pentesting y gestión de vulnerabilidades en API, microservicios y entornos cloud."),
  it("División Investigación de los Ciberdelitos", R + "Prefectura Naval Argentina (desde 2019): intervención en investigaciones judiciales sobre hacking, accesos indebidos y ataques DoS y DDoS."),
  it("Infraestructura de Sistemas", R + "Prefectura Naval Argentina (desde 2016): implementación y mantenimiento de centros de datos, virtualización y almacenamiento."),
  it("Pericias Informáticas", R + "Prefectura Naval Argentina (desde 2013): análisis de elementos sujetos a disposición judicial, preservación de evidencia digital y cadena de custodia."),
  it("Docente", R + f"Instituto Universitario de Seguridad Marítima (2019{WJ}–{WJ}2026): tecnologías de la información, cibercrimen, evidencia digital, redes, seguridad ofensiva y marcos regulatorios."),
  it("Docente", R + "Universidad Abierta Interamericana (2024): Tecnología y Herramientas de Inteligencia."),
  it("Docente", R + "GOBERNA (2026): inteligencia en fuentes abiertas digitales (OSINT) y SOCMINT."),
  it("Docente", R + "UPJET (2026): Fundamentos de Ciberseguridad.")],
 "formacion": [
  it("Licenciatura en Seguridad en Tecnologías de la Información y las Comunicaciones", R + "Instituto Universitario de la Policía Federal Argentina (2021)."),
  it("Licenciatura en Seguridad Marítima", R + "Instituto Universitario de Seguridad Marítima (2007)."),
  it("Auditor Interno de Sistemas de Gestión de Seguridad de la Información ISO 27001:2022", R + "TÜV Rheinland Argentina (2023)."),
  it("Certified in Cybersecurity (CC)", R + "ISC2 (2023)."),
  it("Certificado en Liderazgo de Ciberseguridad", R + "OEA e Instituto Jack D. Gordon de Política Pública de Florida International University (2018)."),
  it("Meya Pico Forensic Examiner Certified", R + "Meya Pico (2018)."),
  it("Formación en EnCase Computer Forensic I y II", ", administración de sistemas Linux y Ethical Hacking.")],
 "aportes": [
  it("Participación en investigaciones judiciales de ciberdelitos", " y análisis pericial de evidencia digital."),
  it("Liderazgo de equipos", " para integrar la ciberseguridad en proyectos tecnológicos y en el ciclo de vida del software."),
  it("Definición y validación de criterios de seguridad", " para API, microservicios y entornos cloud."),
  it("Planificación y supervisión de pruebas de intrusión", " y procesos de gestión de vulnerabilidades."),
  it("Formación de profesionales", " en cibercrimen, informática forense, seguridad ofensiva, OSINT y SOCMINT.")],
 "figma": {"fileKey": "VDnG8Ey0gIPBtCqea1kya9", "desktop": "532:2", "laptop": "535:2", "mobile": "538:2", "foto": ["529:1795", "529:1798", "529:1800"]}
}
json.dump(d, open(os.path.join(P, 'gonzalo-catanzariti-datos.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', json.dumps(d, ensure_ascii=False).count(WJ), 'word joiners')
