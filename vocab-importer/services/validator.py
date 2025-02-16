def validate_word(word):
    errors = []
    required_fields = ['english', 'spanish', 'pronunciation', 'parts']
    
    for field in required_fields:
        if field not in word or not word[field]:
            errors.append(f"Missing {field}")
    
    # Validar que 'parts' sea un string JSON válido
    try:
        json.loads(word['parts'])  # Verifica si 'parts' es un JSON válido
    except json.JSONDecodeError:
        errors.append("Parts must be a valid JSON string")
    
    return len(errors) == 0, errors

def validate_group(group, words):
    errors = []
    if not group.get('name'):
        errors.append("Group name is required")
    
    group['wordsCount'] = len(words)
    return len(errors) == 0, errors