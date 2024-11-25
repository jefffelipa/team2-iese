
import streamlit as st
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
    total_pasos = 8
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
        "Desarrollador de Software",
        "Consultor de Estrategia",
        "Analista de Marketing",
        "Analista de Logística",
        "Analista Financiero",
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

        st.write(f"Pregunta: {st.session_state['pregunta_situacional']}")
        respuesta = st.text_area("Escribe tu respuesta:", value=st.session_state.get("respuesta_situacional", ""))

        if respuesta:
            st.session_state["respuesta_situacional"] = respuesta
            st.button("Siguiente", on_click=avanzar_paso, use_container_width=True)
        else:
            st.button("Siguiente", disabled=True, use_container_width=True)
    else:
        st.error("⚠️ Selecciona un perfil antes de continuar.")

# Paso 4: Primera Pregunta Técnica
elif st.session_state["paso_actual"] == 4:
    mostrar_progreso()
    st.title("Primera Pregunta Técnica")
    perfil = st.session_state.get("perfil_seleccionado")

    if perfil:
        if st.session_state["pregunta_tecnica_1"] is None:
            st.session_state["pregunta_tecnica_1"] = generar_pregunta(perfil)

        st.write(f"Pregunta: {st.session_state['pregunta_tecnica_1']}")
        respuesta = st.text_area("Escribe tu respuesta:", value=st.session_state.get("respuesta_tecnica_1", ""))

        if respuesta:
            st.session_state["respuesta_tecnica_1"] = respuesta
            st.button("Siguiente", on_click=avanzar_paso, use_container_width=True)
        else:
            st.button("Siguiente", disabled=True, use_container_width=True)
    else:
        st.error("⚠️ Selecciona un perfil antes de continuar.")

# Paso 5: Segunda Pregunta Técnica
elif st.session_state["paso_actual"] == 5:
    mostrar_progreso()
    st.title("Segunda Pregunta Técnica")
    perfil = st.session_state.get("perfil_seleccionado")

    if perfil:
        if st.session_state["pregunta_tecnica_2"] is None:
            st.session_state["pregunta_tecnica_2"] = generar_pregunta(perfil)

        st.write(f"Pregunta: {st.session_state['pregunta_tecnica_2']}")
        respuesta = st.text_area("Escribe tu respuesta:", value=st.session_state.get("respuesta_tecnica_2", ""))

        if respuesta:
            st.session_state["respuesta_tecnica_2"] = respuesta
            st.button("Siguiente", on_click=avanzar_paso, use_container_width=True)
        else:
            st.button("Siguiente", disabled=True, use_container_width=True)
    else:
        st.error("⚠️ Selecciona un perfil antes de continuar.")

# Paso 6: Tercera Pregunta Técnica
elif st.session_state["paso_actual"] == 6:
    mostrar_progreso()
    st.title("Tercera Pregunta Técnica")
    perfil = st.session_state.get("perfil_seleccionado")

    if perfil:
        if st.session_state["pregunta_tecnica_3"] is None:
            st.session_state["pregunta_tecnica_3"] = generar_pregunta(perfil)

        st.write(f"Pregunta: {st.session_state['pregunta_tecnica_3']}")
        respuesta = st.text_area("Escribe tu respuesta:", value=st.session_state.get("respuesta_tecnica_3", ""))

        if respuesta:
            st.session_state["respuesta_tecnica_3"] = respuesta
            st.button("Mostrar Resultados", on_click=avanzar_paso, use_container_width=True)
        else:
            st.button("Mostrar Resultados", disabled=True, use_container_width=True)
    else:
        st.error("⚠️ Selecciona un perfil antes de continuar.")

# Paso 7: Evaluación de Respuestas
elif st.session_state["paso_actual"] == 7:
    mostrar_progreso()
    st.title("Resultados de la Evaluación")

    respuestas = {
        "Pregunta Situacional": st.session_state["respuesta_situacional"],
        "Primera Pregunta Técnica": st.session_state["respuesta_tecnica_1"],
        "Segunda Pregunta Técnica": st.session_state["respuesta_tecnica_2"],
        "Tercera Pregunta Técnica": st.session_state["respuesta_tecnica_3"],
    }

    evaluacion_blandas = evaluar_blandas(respuestas["Pregunta Situacional"], variables_blandas)
    evaluacion_tecnicas = evaluar_tecnicas(respuestas["Primera Pregunta Técnica"], variables_tecnicas)

    st.subheader("Evaluación de Habilidades Blandas")
    for variable, resultado in evaluacion_blandas.items():
        st.write(f"{variable}: {resultado}")

    st.subheader("Evaluación de Habilidades Técnicas")
    for variable, resultado in evaluacion_tecnicas.items():
        st.write(f"{variable}: {resultado}")

    if st.button("Generar Informe PDF"):
        pdf_path = generar_pdf(st.session_state["perfil_seleccionado"], respuestas)
        st.success(f"Informe generado: {pdf_path}")

# Paso 8: Finalización
elif st.session_state["paso_actual"] == 8:
    mostrar_progreso()
    st.title("Cuestionario Completado")
    st.write("Gracias por participar. Puedes cerrar esta ventana.")
