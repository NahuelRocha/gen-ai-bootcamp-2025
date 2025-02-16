import json

def export_to_json(words, group):
    # Asegurarse de que 'parts' sea un string JSON válido
    for word in words:
        if isinstance(word['parts'], dict):
            word['parts'] = json.dumps(word['parts'])
    export_data = {
        "words": words,
        "group": group
    }
    return json.dumps(export_data, indent=2)
