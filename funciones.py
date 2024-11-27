
import openai
import streamlit as st
import re
from config_variables import variables_blandas, variables_tecnicas
import fpdf
from fpdf import FPDF
import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Configuración de claves de Firebase desde variables de entorno
firebase_config = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),  # Asegura que las líneas escapadas funcionen
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
}

# Inicialización de Firebase con el archivo de credenciales
def initialize_firebase():
    # Verifica si Firebase ya ha sido inicializado
    if not firebase_admin._apps:
      cred = credentials.Certificate(firebase_config)
      firebase_admin.initialize_app(cred)
    else:
      print("Firebase ya está inicializado")

    db = firestore.client()  # Conexión a Firestore
    return db

# Función para guardar la evaluación en Firestore
def guardar_evaluacion(perfil, evaluaciones_blandas, justificaciones_blandas, evaluaciones_tecnicas, justificaciones_tecnicas):
    db = initialize_firebase()  # Inicializa Firebase

    fecha_hora_actual = datetime.now().isoformat()  # Esto da la fecha y hora en formato ISO 8601


    # Usando el método .add() para que Firestore genere un ID único automáticamente
    doc_ref = db.collection('evaluaciones').add({
        "perfil": perfil,
        "fecha_registro": fecha_hora_actual,  # Añadimos la fecha y hora
        "habilidades_blandas": {
            "Empatía": {"calificacion": evaluaciones_blandas.get("Empatía", 0), "justificacion": justificaciones_blandas.get("Empatía", "No disponible")},
            "Colaboración": {"calificacion": evaluaciones_blandas.get("Colaboración", 0), "justificacion": justificaciones_blandas.get("Colaboración", "No disponible")},
            "Adaptabilidad": {"calificacion": evaluaciones_blandas.get("Adaptabilidad", 0), "justificacion": justificaciones_blandas.get("Adaptabilidad", "No disponible")},
            "Trabajo en equipo": {"calificacion": evaluaciones_blandas.get("Trabajo en equipo", 0), "justificacion": justificaciones_blandas.get("Trabajo en equipo", "No disponible")}
        },
        "habilidades_tecnicas": {
            "Validez Semántica": {"calificacion": evaluaciones_tecnicas.get("Validez Semántica", 0), "justificacion": justificaciones_tecnicas.get("Validez Semántica", "No disponible")},
            "Claridad": {"calificacion": evaluaciones_tecnicas.get("Claridad", 0), "justificacion": justificaciones_tecnicas.get("Claridad", "No disponible")},
            "Profundidad Técnica": {"calificacion": evaluaciones_tecnicas.get("Profundidad Técnica", 0), "justificacion": justificaciones_tecnicas.get("Profundidad Técnica", "No disponible")},
            "Nivel de Dificultad": {"calificacion": evaluaciones_tecnicas.get("Nivel de Dificultad", 0), "justificacion": justificaciones_tecnicas.get("Nivel de Dificultad", "No disponible")}
        }
    })
    print("Evaluación guardada con éxito en Firestore.")

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
        prompt = (
            f"Evalúa la siguiente respuesta según la variable '{variable}'.\n\n"
            f"Respuesta: {respuesta}\n\n"
            f"Primero, proporciona una calificación del 1 al 10, solo dame el número entero y luego, justifica brevemente si no cumple los criterios. Empieza la frase con la expresión: La valoración es y se justifica a"
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )

            response_text = response['choices'][0]['message']['content'].strip()

            #Extraer el número de la calificación (primer número)
            match = re.search(r"\d+", response_text)  # Buscar el primer número
            if match:
                calificacion = int(match.group())  # Convertir el número a entero
            else:
                calificacion = 0  # Si no se encuentra un número, asignamos 0

            evaluaciones[variable] = calificacion  # Simulación de calificación numérica
            justificaciones[variable] = response_text  # Justificación del resultado
        except Exception as e:
            evaluaciones[variable] = ""
            justificaciones[variable] = "No se pudo generar justificación."

    return evaluaciones, justificaciones

def evaluar_tecnicas(respuesta, variables_tecnicas):
    evaluaciones = {}
    justificaciones = {}

    for variable in variables_tecnicas:
        prompt = (
            f"Evalúa la siguiente respuesta según la variable '{variable}'.\n\n"
            f"Respuesta: {respuesta}\n\n"
            f"Primero, proporciona una calificación del 1 al 10, solo dame el número entero y luego, justifica brevemente si no cumple los criterios. Empieza la frase con la expresión: La valoración es y se justifica a"
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
            response_text = response['choices'][0]['message']['content'].strip()

            #Extraer el número de la calificación (primer número)
            match = re.search(r"\d+", response_text)  # Buscar el primer número
            if match:
                calificacion = int(match.group())  # Convertir el número a entero
            else:
                calificacion = 0  # Si no se encuentra un número, asignamos 0

            evaluaciones[variable] = calificacion  # Simulación de calificación numérica
            justificaciones[variable] = response_text  # Justificación del resultado
        except Exception as e:
            evaluaciones[variable] = 0
            justificaciones[variable] = "No se pudo generar justificación."

    return evaluaciones, justificaciones
