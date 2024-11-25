
import openai
import streamlit as st
import re
from config_variables import variables_blandas, variables_tecnicas
import fpdf
from fpdf import FPDF
import os

# Configurar la clave de API desde las variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

# Verificar si la clave de API está configurada
if not openai.api_key:
    raise ValueError("La clave de API de OpenAI no está configurada.")

# Función para generar pregunta técnica
def generar_pregunta(perfil, respuesta_anterior=None):
    prompt = f"Genera una pregunta técnica robusta y situacional de al menos 5 lineas para un candidato con el perfil de {perfil}."
    if respuesta_anterior:
        prompt += f"\nTen en cuenta esta respuesta previa: {respuesta_anterior}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error al generar la pregunta: {e}"

# Función para generar pregunta situacional
def generar_pregunta_situacional(perfil):
    prompt = (
        f"Basándote en el perfil de {perfil}, genera una pregunta situacional relacionada con trabajo en equipo, colaboración y adaptación al cambio. "
        f"El contexto debe tener al menos 7 líneas de detalle, y la pregunta debe ser breve y clara al final."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error al generar la pregunta situacional: {e}"

import openai

def evaluar_blandas(respuesta, variables_blandas):
    evaluaciones = {}
    justificaciones = {}

    for variable in variables_blandas:
        prompt = f"Califica la siguiente respuesta sobre '{variable}' del 1 al 10. Respuesta: {respuesta}"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
            response_text = response['choices'][0]['message']['content'].strip()
            evaluaciones[variable] = 0  # Simulación de calificación numérica
            justificaciones[variable] = response_text  # Justificación del resultado
        except Exception as e:
            evaluaciones[variable] = 0
            justificaciones[variable] = "No se pudo generar justificación."

    return evaluaciones, justificaciones

def evaluar_tecnicas(respuesta, variables_tecnicas):
    evaluaciones = {}
    justificaciones = {}

    for variable in variables_tecnicas:
        prompt = f"Califica la siguiente respuesta sobre '{variable}' del 1 al 10. Respuesta: {respuesta}"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
            response_text = response['choices'][0]['message']['content'].strip()
            evaluaciones[variable] = 0  # Simulación de calificación numérica
            justificaciones[variable] = response_text  # Justificación del resultado
        except Exception as e:
            evaluaciones[variable] = 0
            justificaciones[variable] = "No se pudo generar justificación."

    return evaluaciones, justificaciones
