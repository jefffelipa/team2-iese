
from fpdf import FPDF

# Función para generar el PDF con las evaluaciones y respuestas
def generar_pdf(perfil, respuestas):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Encabezado del informe
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Informe de Evaluación", ln=True, align='C')

    # Detalle del perfil
    pdf.set_font('Arial', size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Perfil del Candidato: {perfil}", ln=True)

    # Sección de respuestas
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, txt="Respuestas del Candidato", ln=True)
    pdf.set_font('Arial', size=12)
    for pregunta, respuesta in respuestas.items():
        pdf.ln(5)
        pdf.multi_cell(0, 10, txt=f"{pregunta}: {respuesta}")

    # Guardar el archivo PDF
    pdf_path = "/content/Informe_de_evaluacion_candidato.pdf"
    pdf.output(pdf_path)

    return pdf_path  # Devuelve la ruta del archivo generado
