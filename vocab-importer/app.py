import streamlit as st
import pandas as pd
import json
from services.llm import generate_vocabulary
from services.validator import validate_word, validate_group
from services.sql_generator import generate_sql_seed

def create_sidebar():
    st.sidebar.title("Configuration")
    category = st.sidebar.selectbox(
        "Select Category",
        [
         "Basic Greetings",
         "Numbers and Counting",
         "Colors and Shapes",
         "Family Members",
         "Food and Drinks",
         "Daily Activities",
         "Weather and Seasons",
         "Professions",
         "Travel and Transportation",
         "House and Furniture"
        ]
    )
    word_count = st.sidebar.slider("Number of Words", 1, 10, 5)
    return category, word_count

def create_generation_form(category, word_count):
    st.header("Generate Vocabulary")
    
    if st.button("Generate Words"):
        with st.spinner("Generating vocabulary..."):
            words = generate_vocabulary(category, word_count)
            
            if words:
                # Create group
                group = {
                    "id": 1,  # En una aplicación real, el ID se genera automáticamente
                    "name": category,
                    "wordsCount": len(words)
                }
                
                # Agregar IDs y valores de conteo a cada palabra
                for i, word in enumerate(words):
                    word['id'] = i + 1
                    word['correctCount'] = 0
                    word['wrongCount'] = 0
                
                # Guardar en el session_state
                st.session_state['current_words'] = words
                st.session_state['current_group'] = group
                
                # Mostrar vista previa y botones de descarga
                show_preview(words, group)

def show_preview(words, group):
    st.subheader("Preview")
    
    # Convertir la lista de palabras a DataFrame y resetear el índice para no mostrar la columna extra
    df = pd.DataFrame(words).reset_index(drop=True)
    edited_df = st.data_editor(df, key="data_editor")
    
    # Mostrar botones de descarga en dos columnas
    col1, col2 = st.columns(2)
    
    with col1:
        # Exportar a JSON: armar el objeto que incluye "words" y "group"
        export_data = {
            "words": edited_df.to_dict('records'),
            "group": group
        }
        json_str = json.dumps(export_data, indent=2)
        st.download_button(
            "Download JSON",
            json_str,
            file_name="vocabulary.json",
            mime="application/json"
        )
    
    with col2:
        # Exportar a SQL Seed: generar el contenido SQL usando la función ya implementada
        sql_content = generate_sql_seed(edited_df.to_dict('records'), group['name'])
        st.download_button(
            "Download SQL Seed",
            sql_content,
            file_name="vocab_seed.sql",
            mime="text/plain"
        )

def main():
    st.title("Vocab Importer Tool")
    
    # Inicializar el session_state
    if 'current_words' not in st.session_state:
        st.session_state['current_words'] = None
    if 'current_group' not in st.session_state:
        st.session_state['current_group'] = None
    
    # Sidebar
    category, word_count = create_sidebar()
    
    # Contenido principal: pestañas para generar e importar
    tab1, tab2 = st.tabs(["Generate", "Import"])
    
    with tab1:
        create_generation_form(category, word_count)
    
    with tab2:
        st.header("Import JSON")
        uploaded_file = st.file_uploader("Choose a JSON file")
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                st.json(data)
            except json.JSONDecodeError:
                st.error("Invalid JSON file")

if __name__ == "__main__":
    main()
