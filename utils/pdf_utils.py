
import matplotlib.pyplot as plt
import openai
import numpy as np
from fpdf import FPDF
import streamlit as st
from funciones import (
    generar_pregunta,
    generar_pregunta_situacional,
    evaluar_blandas,
    evaluar_tecnicas,
)

def crear_spider(datos, categorias, titulo, nombre_archivo):
    valores = list(datos.values())
    valores += valores[:1]  # Volver al inicio
    categorias += categorias[:1]  # Repetir la primera categoría

    angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=True)
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    ax.fill(angulos, valores, color='blue', alpha=0.3)
    ax.plot(angulos, valores, color='blue', linewidth=2)
    ax.set_yticks(range(1, 11))
    ax.set_yticklabels(range(1, 11), fontsize=8, color="gray")
    ax.set_xticks(angulos)
    ax.set_xticklabels(categorias, fontsize=10, color="black")
    ax.set_title(titulo, size=12, color="blue", pad=20)
    plt.savefig(nombre_archivo, dpi=150, bbox_inches='tight', transparent=True)
    plt.close()

# Función para generar el PDF
def generar_pdf(perfil, respuesta_situacional, respuesta_tecnica_1, pregunta_situacional, pregunta_tecnica_1):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    #copiado de otra funcion
    # Evaluar habilidades blandas y técnicas
    variables_blandas = ["Empatía", "Colaboración", "Adaptabilidad", "Trabajo en equipo"]
    variables_tecnicas = ["Validez Semántica", "Claridad", "Profundidad Técnica", "Nivel de Dificultad"]

    # Evaluación de las respuestas
    evaluaciones_blandas, justificaciones_blandas = evaluar_blandas(
        st.session_state["respuesta_situacional"], variables_blandas
    )
    evaluaciones_tecnicas, justificaciones_tecnicas = evaluar_tecnicas(
        st.session_state["respuesta_tecnica_1"], variables_tecnicas
    )

    #elminado copiado

    # Configurar el título y agregar logo en la parte superior
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 30, txt="Informe de Evaluación", ln=True, align='C')

    # Agregar logo en la parte superior derecha
    pdf.image("IESE_LOGO_UPDATED_2023 (1).png", 150, 8, 33)

    # Margen superior
    pdf.ln(2)

    # Evaluación final del candidato
    #evaluacion_blanda, justificaciones_blandas = evaluar_blandas(respuesta_situacional, {})
    #evaluacion_tecnica, justificaciones_tecnicas = evaluar_tecnicas(respuesta_tecnica_1, {})

    habilidades_blandas_apto = all([evaluacion >= 7 for evaluacion in evaluaciones_blandas.values()])
    habilidades_tecnicas_apto = all([evaluacion >= 7 for evaluacion in evaluaciones_tecnicas.values()])
    evaluacion_final = "Apto" if habilidades_blandas_apto and habilidades_tecnicas_apto else "No Apto"

    # prompt para dar descripcion del informe final
    prompt = (
            f"Eres un especialista en reclutamiento y necesitas dar una breve descripción para dar paso al informe detallado de un postulante cuyo resultado es '{evaluacion_final}'.\n\n"
            f"Sin saltos de líneas, y con no más de 120 palabras describe el resultado considerando una breve descripción de habilidades duras y blandas, no entres en detalles, solo algo general y menciona dentro de la respuesta si s apto o no. "
        )

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=250
        )
    response_text = response['choices'][0]['message']['content'].strip()
    #cierre prompt

    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt=f"Evaluación final del candidato:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"{response_text}")

    # Evaluación de habilidades blandas
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Evaluación de habilidades blandas", ln=True)
    pdf.set_font("Arial", size=12)

    # Crear gráfico spider para habilidades blandas
    crear_spider(evaluaciones_blandas, list(evaluaciones_blandas.keys()), "Habilidades Blandas", "blandas_spider.png")
    pdf.image("blandas_spider.png", x=60, y=None, w=90)

    for variable, evaluacion in evaluaciones_blandas.items():
        pdf.set_font("Arial", 'U', 12)  # Subrayar el nombre de la variable
        pdf.cell(0, 10, txt=f"{variable}: {evaluacion}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=f"{justificaciones_blandas.get(variable, 'No disponible')}")

    # Evaluación de habilidades técnicas
    pdf.ln(5)  # Reducir espacio entre secciones
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Evaluación de habilidades técnicas", ln=True)
    pdf.set_font("Arial", size=12)

    # Crear gráfico spider para habilidades técnicas
    crear_spider(evaluaciones_tecnicas, list(evaluaciones_tecnicas.keys()), "Habilidades Técnicas", "tecnicas_spider.png")
    pdf.image("tecnicas_spider.png", x=60, y=None, w=90)
    for variable, evaluacion in evaluaciones_tecnicas.items():
        pdf.set_font("Arial", 'U', 12)  # Subrayar el nombre de la variable
        pdf.cell(0, 10, txt=f"{variable}: {evaluacion}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=f"{justificaciones_tecnicas.get(variable, 'No disponible')}")

    # Recomendación final
    #pdf.ln(10)
    #pdf.set_font("Arial", 'B', 12)
    #pdf.cell(200, 10, txt="Recomendación final:", ln=True)
    #pdf.set_font("Arial", size=12)
    #pdf.multi_cell(0, 10, txt="Basado en la evaluación técnica y blanda, el candidato tiene un buen desempeño general. Se recomienda su contratación, aunque sugerimos capacitación en habilidades blandas para mejorar la empatía y creatividad.")

    # Configurar el título y agregar logo en la parte superior
    #pdf.add_page()
    #pdf.set_font('Arial', 'B', 16)
    #pdf.cell(200, 30, txt="Anexo: Respuestas del candidato", ln=True, align='C')
    #pdf.set_font("Arial", size=12)
    #pdf.multi_cell(0, 10, txt=f"Pregunta situacional \n {pregunta_situacional} \n Respuesta: {respuesta_situacional}")
    #pdf.multi_cell(0, 10, txt=f"Pregunta técnica 1:\n {pregunta_tecnica_1} \n Respuesta {respuesta_tecnica_1}")

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 30, txt="Anexo: Respuestas del candidato", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.set_font("Arial", 'BU', 12)
    pdf.multi_cell(0, 10, txt="Pregunta situacional")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"{pregunta_situacional} \nRespuesta del candidato: {respuesta_situacional}")
    pdf.set_font("Arial", 'BU', 12)
    pdf.multi_cell(0, 10, txt="Pregunta técnica:")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"{pregunta_tecnica_1} \nRespuesta del candidato: {respuesta_tecnica_1}")


    pdf_output_path = "Informe_de_evaluacion_candidato.pdf"
    pdf.output(pdf_output_path)

    return pdf_output_path

# Valores fijos para pruebas
#perfil = "Desarrollador de Software"
#respuesta_situacional = "Utilizaría la mediación y la comunicación abierta para resolver el conflicto."
#respuesta_tecnica_1 = "Aplicaría metodologías ágiles para abordar el problema."
#respuesta_tecnica_2 = "Realizaría un análisis de rendimiento detallado utilizando herramientas específicas."
#respuesta_tecnica_3 = "Implementaría un plan de contingencia para minimizar el impacto."

# Llamada a la función con valores fijos
#pdf_output_path = generar_pdf(perfil, respuesta_situacional, respuesta_tecnica_1, respuesta_tecnica_2, respuesta_tecnica_3)
#print(f"El PDF ha sido generado y guardado en: {pdf_output_path}")
