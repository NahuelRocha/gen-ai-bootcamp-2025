import streamlit as st
from difflib import SequenceMatcher
from transformers import pipeline
from PIL import Image

# Configuración del pipeline de traducción (de español a inglés)
translator = pipeline("translation_es_to_en", model="Helsinki-NLP/opus-mt-es-en")

# Función para generar una frase sencilla a partir de las palabras clave.
def generate_sentence(keywords):
    words = keywords.strip().split()
    if not words:
        return "Por favor, ingresa al menos una palabra."
    # Si hay 1 palabra:
    if len(words) == 1:
        return f"Ayer, el {words[0]} fue muy especial."
    # Si hay 2 palabras:
    elif len(words) == 2:
        return f"Ayer, el {words[0]} se mostró {words[1]}."
    # Si hay 3 o más palabras, se usan las tres primeras
    else:
        # Suponiendo que la primera es un sustantivo, la segunda un adjetivo y la tercera un lugar.
        return f"Ayer, el {words[0]} se mostró {words[1]} en la {words[2]}."

# Función para evaluar la traducción del usuario comparándola con una traducción de referencia.
def evaluate_translation(spanish_sentence, user_translation):
    # Generamos la traducción de referencia
    ref_translation = translator(spanish_sentence)[0]['translation_text']
    # Calculamos la similitud entre la traducción de referencia y la del usuario.
    ratio = SequenceMatcher(None, ref_translation.lower(), user_translation.lower()).ratio()
    # Asignamos una calificación en función de la similitud.
    if ratio > 0.85:
        grade = "A"
    elif ratio > 0.5:
        grade = "B"
    else:
        grade = "C"
    return ref_translation, grade, ratio

# Interfaz de usuario con Streamlit
st.title("Ejercicio de Práctica de Escritura - Aprende Inglés")

# Sección 1: Generador de Frases
st.subheader("Generador de Frases")
keywords_input = st.text_input("Ingresa 2 o 3 palabras (ej. 'perro feliz plaza')")
if st.button("Generar frase"):
    sentence = generate_sentence(keywords_input)
    st.write("**Frase generada:**")
    st.write(sentence)
    st.session_state.generated_sentence = sentence  # Guardamos la frase en la sesión

# Sección 2: Evaluación de la Traducción
st.subheader("Evalúa tu traducción")
if "generated_sentence" in st.session_state:
    st.write("**Frase a traducir:**")
    st.write(st.session_state.generated_sentence)
    user_translation = st.text_input("Escribe la traducción al inglés de la frase anterior")
    if st.button("Evaluar traducción"):
        ref_trans, grade, ratio = evaluate_translation(st.session_state.generated_sentence, user_translation)
        st.write("**Traducción de referencia:**")
        st.write(ref_trans)
        st.write(f"**Calificación:** {grade} (Similitud: {ratio:.2f})")
else:
    st.write("Primero genera una frase para poder evaluarla.")

# Sección 3: Carga de Imagen (Opcional)
st.subheader("Cargar Imagen (Opcional)")
uploaded_file = st.file_uploader("Sube una imagen (png, jpg, jpeg)", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_column_width=True)
    # Opcional: Si deseas extraer texto de la imagen usando OCR,
    # puedes descomentar las siguientes líneas y asegurarte de tener instalado pytesseract y Tesseract-OCR.
    """
    import pytesseract
    ocr_text = pytesseract.image_to_string(image, lang="spa")
    st.write("**Texto extraído:**")
    st.write(ocr_text)
    """

# Sección 4: Cierre
st.write("¡Gracias por usar el Ejercicio de Práctica de Escritura! Esperamos que aprendas inglés con nosotros.")