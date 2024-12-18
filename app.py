
import streamlit as st
from funciones import guardar_evaluacion
from funciones import (
    generar_pregunta,
    generar_pregunta_situacional,
    evaluar_blandas,
    evaluar_tecnicas,
)
from utils.pdf_utils import generar_pdf
from config_variables import variables_blandas, variables_tecnicas

# Inicializar el estado si no existe
if "paso_actual" not in st.session_state:
    st.session_state["paso_actual"] = 1
    st.session_state["perfil_seleccionado"] = None
    st.session_state["pregunta_situacional"] = None
    st.session_state["pregunta_tecnica_1"] = None
    st.session_state["pregunta_tecnica_2"] = None
    st.session_state["pregunta_tecnica_3"] = None
    st.session_state["respuesta_situacional"] = None
    st.session_state["respuesta_tecnica_1"] = None
    st.session_state["respuesta_tecnica_2"] = None
    st.session_state["respuesta_tecnica_3"] = None

# Función para avanzar de paso
def avanzar_paso():
    st.session_state["paso_actual"] += 1

# Mostrar el progreso como texto (arriba)
def mostrar_progreso():
    total_pasos = 5
    st.markdown(f"**Paso {st.session_state['paso_actual']} / {total_pasos}**")

# Paso 1: Bienvenida
if st.session_state["paso_actual"] == 1:
    mostrar_progreso()
    st.title("¡Bienvenido al Evaluador Virtual!")
    st.write("""Este cuestionario consta de varios pasos en los que se te harán preguntas situacionales
        y técnicas basadas en tu perfil. Sigue las instrucciones en cada paso.""")
    st.button("Iniciar", on_click=avanzar_paso, use_container_width=True)

# Paso 2: Selección de Perfil
elif st.session_state["paso_actual"] == 2:
    mostrar_progreso()
    st.title("Evaluador Virtual de Candidatos")
    st.subheader("Seleccione su perfil")
    perfiles = [
        "Seleccione un perfil...",
        "Chief Financial Officer (CFO)",
        "Chief Operating Officer (COO)",
        "Chief Marketing Officer (CMO)",
        "Chief Technology Officer (CTO)",
        "Chief Human Resources Officer (CHRO)",
    ]
    perfil = st.selectbox("Seleccione el perfil del candidato:", perfiles)

    if perfil != "Seleccione un perfil...":
        st.session_state["perfil_seleccionado"] = perfil
        st.success(f"Perfil seleccionado: {perfil}")
        st.button("Siguiente", on_click=avanzar_paso, use_container_width=True)
    else:
        st.error("⚠️ Por favor, selecciona un perfil para continuar.")

# Paso 3: Pregunta Situacional
elif st.session_state["paso_actual"] == 3:
    mostrar_progreso()
    st.title("Pregunta Situacional")
    perfil = st.session_state.get("perfil_seleccionado")

    if perfil:
        if st.session_state["pregunta_situacional"] is None:
            st.session_state["pregunta_situacional"] = generar_pregunta_situacional(perfil)

        st.write(f"{st.session_state['pregunta_situacional']}")
        respuesta = st.text_area("Escribe tu respuesta:", value=st.session_state.get("respuesta_situacional", ""))

        if respuesta:
            st.session_state["respuesta_situacional"] = respuesta
            st.button("Siguiente", on_click=avanzar_paso, use_container_width=True)
        else:
            st.button("Siguiente", disabled=True, use_container_width=True)
    else:
        st.error("⚠️ Selecciona un perfil antes de continuar.")

# Paso 4: Primera Pregunta Técnica
#elif st.session_state["paso_actual"] == 4:
#    mostrar_progreso()
#    st.title("Pregunta Técnica")
#    perfil = st.session_state.get("perfil_seleccionado")

#    if perfil:
#        if st.session_state["pregunta_tecnica_1"] is None:
#            st.session_state["pregunta_tecnica_1"] = generar_pregunta(perfil)

#        st.write(f"{st.session_state['pregunta_tecnica_1']}")
#        st.session_state["respuesta_tecnica_1"] = "..."
#        respuesta = st.text_area("Escribe tu respuesta:", value=st.session_state.get("respuesta_tecnica_1", ""))

#        if respuesta:
#            st.session_state["respuesta_tecnica_1"] = respuesta
#            st.button("Siguiente", on_click=avanzar_paso, use_container_width=True)
#        else:
#            st.button("Siguiente", disabled=True, use_container_width=True)
#    else:
#        st.error("⚠️ Selecciona un perfil antes de continuar.")

# Paso 5: Segunda Pregunta Técnica
#elif st.session_state["paso_actual"] == 5:
#    mostrar_progreso()
#    st.title("Segunda Pregunta Técnica")
#    perfil = st.session_state.get("perfil_seleccionado")

#    if perfil:
#        if st.session_state["pregunta_tecnica_2"] is None:
#            st.session_state["pregunta_tecnica_2"] = generar_pregunta(perfil)
#        st.write(f"Pregunta: {st.session_state['pregunta_tecnica_2']}")
#        st.session_state["respuesta_tecnica_2"] = "...."
#        respuesta = st.text_area("Escribe tu respuesta:", value=st.session_state.get("respuesta_tecnica_2", ""))

#        if respuesta:
#            st.session_state["respuesta_tecnica_2"] = respuesta
#            st.button("Siguiente", on_click=avanzar_paso, use_container_width=True)
#        else:
#            st.button("Siguiente", disabled=True, use_container_width=True)
#    else:
#        st.error("⚠️ Selecciona un perfil antes de continuar.")

#Paso 6: Tercera Pregunta Técnica
elif st.session_state["paso_actual"] == 4:
    mostrar_progreso()
    st.title("Pregunta Técnica")
    perfil = st.session_state.get("perfil_seleccionado")

    if perfil:
        if st.session_state["pregunta_tecnica_1"] is None:
            st.session_state["pregunta_tecnica_1"] = generar_pregunta(perfil)

        st.write(f"Pregunta: {st.session_state['pregunta_tecnica_1']}")
        st.session_state["respuesta_tecnica_1"] = "....."
        respuesta = st.text_area("Escribe tu respuesta:", value=st.session_state.get("respuesta_tecnica_1", ""))

        if respuesta:
            st.session_state["respuesta_tecnica_1"] = respuesta
            st.button("Mostrar Resultados", on_click=avanzar_paso, use_container_width=True)
        else:
            st.button("Mostrar Resultados", disabled=True, use_container_width=True)
    else:
        st.error("⚠️ Selecciona un perfil antes de continuar.")

import streamlit as st
from funciones import evaluar_blandas, evaluar_tecnicas

# Paso 5, donde se muestran las evaluaciones
if st.session_state["paso_actual"] == 5:
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

    # Guardar los datos en Firestore (Agregando esta sección)
    perfil = st.session_state.get("perfil_seleccionado", "desconocido")  # Asegúrate de tener el perfil del candidato
    guardar_evaluacion(
        perfil, evaluaciones_blandas, justificaciones_blandas, evaluaciones_tecnicas, justificaciones_tecnicas
    )

    # Mostrar las evaluaciones de habilidades blandas
    st.write("### Evaluación de Habilidades Blandas")
    for variable, resultado in evaluaciones_blandas.items():
        justificacion = justificaciones_blandas.get(variable, "No disponible")
        st.write(f"**{variable}**: {justificacion}")
        #st.write(justificacion)

    # Mostrar las evaluaciones de habilidades técnicas
    st.write("### Evaluación de Habilidades Técnicas")
    for variable, resultado in evaluaciones_tecnicas.items():
        justificacion = justificaciones_tecnicas.get(variable, "No disponible")
        st.write(f"**{variable}**: {justificacion}")
        #st.write(f"Justificación: {justificacion}")

    # Obtener las respuestas y el perfil de la sesión o variables dinámicas
    perfil = st.session_state.get("perfil_seleccionado", None)
    respuesta_situacional = st.session_state.get("respuesta_situacional", "")
    respuesta_tecnica_1 = st.session_state.get("respuesta_tecnica_1", "")
    pregunta_situacional = st.session_state.get("pregunta_situacional", "")
    pregunta_tecnica_1 = st.session_state.get("pregunta_tecnica_1", "")

    # Generar el PDF solo si todas las respuestas están presentes
    pdf_path = generar_pdf(perfil, respuesta_situacional, respuesta_tecnica_1, pregunta_situacional, pregunta_tecnica_1)

    # Mostrar el PDF generado con el botón de descarga
    st.write("### Informe de Evaluación del Candidato")
    #st.markdown(f"**Descargar Informe**: [Haz clic aquí para descargar el PDF]({pdf_path})")

    with open(pdf_path, "rb") as f:
            st.download_button("Descargar PDF", data=f, file_name="Informe_de_evaluacion.pdf", mime="application/pdf", use_container_width=True)

    # Botón para finalizar el cuestionario
    st.button("Finalizar Cuestionario", on_click=avanzar_paso, use_container_width=True)


    #pdf_output_path = generar_pdf(perfil, respuesta_situacional, respuesta_tecnica_1, respuesta_tecnica_2, respuesta_tecnica_3)

# Paso 8: Finalización
elif st.session_state["paso_actual"] == 6:
    mostrar_progreso()
    st.title("Cuestionario Completado")
    st.write("Gracias por participar. Puedes cerrar esta ventana.")
