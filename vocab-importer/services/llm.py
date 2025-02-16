import json
import re
import requests

def extract_all_top_level_json_objects(text):
    """
    Extracts all top-level (non-nested) JSON objects from the text.
    Traverses the text and counts the braces to determine when an object is closed.
    Returns a list of strings with each JSON object.
    """
    objects = []
    start_index = None
    brace_count = 0
    in_string = False
    escape = False

    for i, char in enumerate(text):
        if char == '"' and not escape:
            in_string = not in_string
        if in_string:
            if char == '\\' and not escape:
                escape = True
            else:
                escape = False
            continue

        if char == '{':
            if brace_count == 0:
                start_index = i
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0 and start_index is not None:
                # Se ha completado un objeto JSON de nivel superior.
                objects.append(text[start_index:i+1])
                start_index = None

    return objects

def generate_vocabulary(category, word_count):
    PROMPT_TEMPLATE = """
    Generate {word_count} words for category '{category}' in English with Spanish translations.
    Follow these STRICT requirements:
    1. Only return the requested JSON. Do not include any greetings, explanations, or extra text.
    2. Do not repeat any existing common words.
    3. Ensure all IPA pronunciations are accurate and correspond to the generated English word.
    4. The 'parts' JSON must follow the exact format and categories shown in the examples below.
    5. Do NOT include an "id" field; the database will generate it automatically.
    
    Examples for different categories:
    - For "Basic Greetings": {{"type": "greeting", "usage": "formal/informal"}}
    - For "Numbers and Counting": {{"type": "number", "category": "cardinal"}}
    - For "Colors and Shapes": {{"type": "color", "category": "primary/secondary"}}
    - For "Family Members": {{"type": "family", "relationship": "parent/sibling/grandparent"}}
    - For "Food and Drinks": {{"type": "food/drink", "category": "meat/fruit/beverage/grain"}}
    
    **Output format MUST be exactly a JSON array with objects that have only the following keys:**
    "english", "spanish", "pronunciation", "parts", "correctCount", "wrongCount"
    
    For example:
    ```json
    [
        {{
            "english": "Hello",
            "spanish": "Hola",
            "pronunciation": "/həˈloʊ/",
            "parts": "{{\\"type\\": \\"greeting\\", \\"usage\\": \\"formal/informal\\"}}",
            "correctCount": 0,
            "wrongCount": 0
        }},
        ...
    ]
    ```
    Generate {word_count} words appropriate for the {category} category.
    """

    prompt = PROMPT_TEMPLATE.format(word_count=word_count, category=category)

    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            "model": "llama2:7b",
            "prompt": prompt,
            "stream": False
        })

        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")

        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "").strip()

            # Extraer el bloque entre el primer "{" y el último "}".
            start = response_text.find('{')
            end = response_text.rfind('}')
            if start == -1 or end == -1:
                print("Error: No se encontró bloque JSON en la respuesta.")
                return None
            json_block = response_text[start:end+1]

            # Dividir el bloque en partes. Asumimos que los objetos se separan con "}," seguido de salto de línea.
            parts = re.split(r'\},\s*\n', json_block)
            objects = []
            for i, part in enumerate(parts):
                part = part.strip()
                # Si no termina con "}" y no es el último, agregarla.
                if i < len(parts) - 1 and not part.endswith('}'):
                    part += '}'
                # Validar que la cadena empiece con "{" y termine con "}"
                if part.startswith('{') and part.endswith('}'):
                    try:
                        obj = json.loads(part)
                        objects.append(obj)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON object: {e}")
                else:
                    print(f"Ignorado fragmento no válido: {part[:50]}...")
            if not objects:
                print("Error: No se pudo parsear ningún objeto JSON.")
                return None
            print(f"Words generated: {objects}")
            return objects
        else:
            print(f"Error in API request: {response.status_code}")
    except Exception as e:
        print(f"Error during request: {str(e)}")

    return None