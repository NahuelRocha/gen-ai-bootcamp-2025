import streamlit as st
import requests
import httpx
import json
import os
import asyncio
from dotenv import load_dotenv
import base64
import time

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

# Configuración de la página
st.set_page_config(
    page_title="Listening Practice App",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS con colores mejorados para mayor contraste
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0d47a1;  /* Azul más oscuro para mejor contraste */
        text-align: center;
        margin-bottom: 1rem;
    }
    .exercise-title {
        font-size: 1.8rem;
        color: #212121;  /* Negro más oscuro */
        margin-bottom: 0.5rem;
    }
    .exercise-description {
        font-size: 1.2rem;
        color: #212121;  /* Negro más oscuro en vez de #555 */
        margin-bottom: 1.5rem;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 5px;
    }
    .dialog-text {
        font-size: 1.1rem;
        padding: 15px;
        background-color: #e3f2fd;  /* Fondo azul más claro */
        border-left: 5px solid #0d47a1;  /* Borde más oscuro */
        border-radius: 5px;
        margin-bottom: 1.5rem;
        color: #212121;  /* Texto oscuro para contraste */
    }
    .question-text {
        font-size: 1.2rem;
        font-weight: 600;  /* Más negrita */
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        color: #212121;  /* Negro más oscuro */
    }
    .correct-answer {
        color: #1b5e20;  /* Verde más oscuro */
        font-weight: bold;
    }
    .incorrect-answer {
        color: #b71c1c;  /* Rojo más oscuro */
        font-weight: bold;
    }
    .result-summary {
        font-size: 1.3rem;
        padding: 15px;
        background-color: #e8f5e9;
        border-radius: 5px;
        margin-top: 1.5rem;
        color: #212121;  /* Negro más oscuro */
    }
    .audio-container {
        padding: 10px;
        background-color: #e3f2fd;
        border-radius: 5px;
        margin-bottom: 1.5rem;
    }
    .difficulty-tag {
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-right: 10px;
        color: #212121;  /* Color de texto oscuro para todos los tags */
    }
    .easy {
        background-color: #a5d6a7;  /* Verde más oscuro que el original */
    }
    .medium {
        background-color: #fff59d;  /* Amarillo más intenso */
    }
    .hard {
        background-color: #ffab91;  /* Naranja más intenso */
    }
</style>
""", unsafe_allow_html=True)

# Funciones para interactuar con la API (versión sincrónica)
def get_all_exercises():
    """Obtiene todos los ejercicios disponibles"""
    try:
        response = requests.get(f"{API_URL}/exercises")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener ejercicios: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

def get_exercise_by_id(exercise_id):
    """Obtiene un ejercicio específico con sus preguntas y opciones"""
    try:
        response = requests.get(f"{API_URL}/exercises/{exercise_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener el ejercicio: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

def get_exercise_audio(exercise_id):
    """Obtiene la URL del audio de un ejercicio"""
    try:
        response = requests.get(f"{API_URL}/exercises/{exercise_id}/audio")
        if response.status_code == 200:
            return response.json()["audio_url"]
        else:
            st.warning("Este ejercicio no tiene audio disponible.")
            return None
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

def generate_exercise(language, difficulty, scenario, num_questions):
    """Genera un nuevo ejercicio"""
    data = {
        "language": language,
        "difficulty": difficulty,
        "scenario": scenario,
        "num_questions": num_questions
    }
    try:
        response = requests.post(f"{API_URL}/exercises/generate", json=data)
        if response.status_code == 200:
            result = response.json()
            # Generar audio para el ejercicio recién creado
            generate_audio(result["exercise"]["id"])
            return result["exercise"]["id"]
        else:
            st.error(f"Error al generar el ejercicio: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

def generate_audio(exercise_id):
    """Genera audio para un ejercicio específico"""
    try:
        response = requests.post(f"{API_URL}/exercises/{exercise_id}/generate_audio")
        if response.status_code == 200:
            return response.json()["audio_url"]
        else:
            st.warning(f"No se pudo generar el audio: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

# Función para mostrar el reproductor de audio
def display_audio_player(audio_url):
    """Muestra un reproductor de audio para la URL proporcionada"""
    if audio_url:
        st.markdown('<div class="audio-container">', unsafe_allow_html=True)
        st.audio(f"{API_URL.replace('/api', '')}/static/audio/{audio_url}", format="audio/wav")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No hay audio disponible para este ejercicio.")

# Función para mostrar la etiqueta de dificultad
def display_difficulty_tag(difficulty):
    """Muestra una etiqueta de dificultad con formato"""
    difficulty_class = {
        "easy": "easy",
        "fácil": "easy",
        "medium": "medium",
        "intermedio": "medium",
        "hard": "hard",
        "difícil": "hard"
    }.get(difficulty.lower(), "medium")
    
    st.markdown(f'<span class="difficulty-tag {difficulty_class}">{difficulty.upper()}</span>', unsafe_allow_html=True)

# Función para mostrar un ejercicio
def display_exercise(exercise):
    """Muestra un ejercicio con su diálogo y preguntas"""
    # Título y descripción
    st.markdown(f'<h1 class="exercise-title">{exercise["title"]}</h1>', unsafe_allow_html=True)
    
    # Información del ejercicio
    col1, col2 = st.columns([1, 3])
    with col1:
        display_difficulty_tag(exercise["difficulty"])
        st.write(f"**Idioma:** {exercise['language']}")
    with col2:
        st.markdown(f'<div class="exercise-description">{exercise["description"]}</div>', unsafe_allow_html=True)
    
    # Formatear el diálogo con saltos de línea para cada participante
    formatted_dialog = format_dialog(exercise["dialog"])
    
    # Diálogo
    with st.expander("Ver diálogo completo", expanded=False):
        st.markdown(f'<div class="dialog-text">{formatted_dialog}</div>', unsafe_allow_html=True)
    
    # Reproducir audio
    st.subheader("🎧 Escucha el diálogo")
    if exercise.get("audio_path"):
        display_audio_player(exercise["audio_path"])
    else:
        st.info("Este ejercicio no tiene audio. Genera el audio primero.")
        if st.button("Generar audio para este ejercicio"):
            with st.spinner("Generando audio..."):
                audio_url = generate_audio(exercise["id"])
                if audio_url:
                    st.success("¡Audio generado correctamente!")
                    st.experimental_rerun()
    
    # Preguntas
    st.subheader("📝 Responde las preguntas")
    
    # Inicializar respuestas en la sesión si no existen
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    
    # Inicializar verificación en la sesión
    if "checked" not in st.session_state:
        st.session_state.checked = False
    
    # Mostrar preguntas
    for i, question in enumerate(exercise["questions"]):
        st.markdown(f'<p class="question-text">{i+1}. {question["question_text"]}</p>', unsafe_allow_html=True)
        
        # Obtener opciones y la correcta
        options = question["options"]
        correct_option = next((o for o in options if o["is_correct"] == 1), None)
        
        # ID único para esta pregunta
        question_id = question["id"]
        
        # Inicializar respuesta para esta pregunta si no existe
        if question_id not in st.session_state.user_answers:
            st.session_state.user_answers[question_id] = None
        
        # Mostrar opciones como radio buttons
        selected_option = st.radio(
            f"Pregunta {i+1}",
            options=[o["option_text"] for o in options],
            index=None,
            key=f"q_{question_id}",
            label_visibility="collapsed"
        )
        
        # Guardar respuesta seleccionada
        if selected_option:
            selected_index = [o["option_text"] for o in options].index(selected_option)
            st.session_state.user_answers[question_id] = options[selected_index]
        
        # Mostrar retroalimentación si se ha verificado
        if st.session_state.checked and st.session_state.user_answers[question_id]:
            user_option = st.session_state.user_answers[question_id]
            if user_option["is_correct"] == 1:
                st.markdown(f'<p class="correct-answer">✓ ¡Correcto!</p>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<p class="incorrect-answer">✗ Incorrecto. La respuesta correcta es: {correct_option["option_text"]}</p>',
                    unsafe_allow_html=True
                )
        
        st.markdown("---")
    
    # Botones para verificar respuestas y reiniciar
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Verificar respuestas"):
            st.session_state.checked = True
            st.experimental_rerun()
    
    with col2:
        if st.button("Reiniciar ejercicio"):
            st.session_state.user_answers = {}
            st.session_state.checked = False
            st.experimental_rerun()
    
    # Mostrar resultados si se ha verificado
    if st.session_state.checked:
        correct_count = sum(1 for q_id, ans in st.session_state.user_answers.items() 
                            if ans and ans["is_correct"] == 1)
        total_questions = len(exercise["questions"])
        percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        
        st.markdown(
            f'<div class="result-summary">Resultado: {correct_count}/{total_questions} respuestas correctas ({percentage:.1f}%)</div>',
            unsafe_allow_html=True
        )


def format_dialog(dialog_text):
    """
    Formatea el diálogo para que cada intervención aparezca en una nueva línea
    """
    import re
    
    # Dividir el texto en segmentos basados en los patrones "Nombre:"
    pattern = r'([A-Za-z]+):\s*'
    
    # Encontrar todas las posiciones donde aparece un nombre seguido de dos puntos
    matches = list(re.finditer(pattern, dialog_text))
    
    if not matches:
        return dialog_text
    
    formatted_parts = []
    last_end = 0
    
    # Procesar cada coincidencia
    for i, match in enumerate(matches):
        # Si no es la primera coincidencia, añadir el texto entre la coincidencia anterior y esta
        if i > 0:
            # Obtener el texto entre la coincidencia anterior y esta
            text = dialog_text[last_end:match.start()]
            formatted_parts.append(text)
            # Agregar un salto de línea para separar las intervenciones
            formatted_parts.append("<br><br>")
        
        # Añadir el nombre en negrita
        name = match.group(1)
        formatted_parts.append(f"<strong>{name}:</strong> ")
        
        # Actualizar la posición final
        last_end = match.end()
    
    # Añadir el texto restante después de la última coincidencia
    if last_end < len(dialog_text):
        formatted_parts.append(dialog_text[last_end:])
    
    # Unir todas las partes
    return "".join(formatted_parts)

# Función para la página de generación de ejercicios
def generate_exercise_page():
    st.markdown('<h2>Genera un nuevo ejercicio</h2>', unsafe_allow_html=True)
    
    # Formulario para generar ejercicio
    with st.form("generate_exercise_form"):
        language = st.selectbox(
            "Idioma",
            ["Inglés", "Español", "Francés", "Alemán", "Italiano"]
        )
        
        difficulty = st.selectbox(
            "Nivel de dificultad",
            ["Fácil", "Intermedio", "Difícil"]
        )
        
        scenario = st.selectbox(
            "Escenario",
            ["Restaurante", "Oficina", "Viaje", "Compras", "Hotel", "Entrevista", "Reunión Casual"]
        )
        
        num_questions = st.slider("Número de preguntas", min_value=2, max_value=10, value=5)
        
        submit_button = st.form_submit_button("Generar ejercicio")
        
        if submit_button:
            with st.spinner("Generando ejercicio..."):
                exercise_id = generate_exercise(language, difficulty, scenario, num_questions)
                if exercise_id:
                    st.success("¡Ejercicio generado correctamente!")
                    st.session_state.selected_exercise = exercise_id
                    st.experimental_rerun()

# Función principal de la aplicación
def main():
    st.markdown('<h1 class="main-header">🎧 Listening Practice App</h1>', unsafe_allow_html=True)
    
    # Barra lateral
    st.sidebar.title("Navegación")
    
    # Botones de navegación
    page = st.sidebar.radio("Ir a:", ["Ejercicios disponibles", "Generar ejercicio"])
    
    if page == "Ejercicios disponibles":
        st.markdown("## Ejercicios de Listening Disponibles")
        
        # Obtener ejercicios
        with st.spinner("Cargando ejercicios..."):
            exercises = get_all_exercises()
        
        if not exercises:
            st.info("No hay ejercicios disponibles. ¡Genera uno nuevo!")
        else:
            # Crear un selectbox con los ejercicios disponibles
            exercise_options = [f"{ex['title']} ({ex['language']}, {ex['difficulty']})" for ex in exercises]
            exercise_map = {f"{ex['title']} ({ex['language']}, {ex['difficulty']})": ex['id'] for ex in exercises}
            
            # Seleccionar ejercicio
            selected_option = st.selectbox(
                "Selecciona un ejercicio:",
                exercise_options,
                index=0 if "selected_exercise" not in st.session_state else 
                      next((i for i, ex in enumerate(exercises) if ex['id'] == st.session_state.selected_exercise), 0)
            )
            
            selected_id = exercise_map[selected_option]
            
            # Guardar el ID seleccionado en la sesión
            st.session_state.selected_exercise = selected_id
            
            # Obtener detalles del ejercicio seleccionado
            with st.spinner("Cargando ejercicio..."):
                exercise = get_exercise_by_id(selected_id)
            
            if exercise:
                display_exercise(exercise)
    else:
        generate_exercise_page()
    
    # Pie de página
    st.sidebar.markdown("---")
    st.sidebar.info("Desarrollado para práctica de listening")

if __name__ == "__main__":
    main()