def generate_sql_seed(words, group_name):
    """
    Generate a SQL seed file content for the given words and group,
    compatible with the provided database schema.
    """
    # Mapeo de nombres de grupo a su ID en la base de datos (según tu esquema)
    GROUP_MAPPING = {
        "Basic Greetings": 1,
        "Numbers and Counting": 2,
        "Colors and Shapes": 3,
        "Family Members": 4,
        "Food and Drinks": 5,
        "Daily Activities": 6,
        "Weather and Seasons": 7,
        "Professions": 8,
        "Travel and Transportation": 9,
        "House and Furniture": 10
    }
    
    group_id = GROUP_MAPPING.get(group_name, None)
    if group_id:
        group_identifier = str(group_id)
    else:
        # Si no se encuentra, se usa una subconsulta (esto es menos ideal)
        group_identifier = f"(SELECT id FROM groups WHERE name = '{group_name}')"
    
    sql_lines = []
    
    # Para cada palabra, generar INSERT OR IGNORE en la tabla words y luego en word_groups.
    for word in words:
        # Escapar comillas simples en los valores
        english = word['english'].replace("'", "''")
        spanish = word['spanish'].replace("'", "''")
        pronunciation = word['pronunciation'].replace("'", "''")
        parts = word['parts'].replace("'", "''")
        
        # Insertar la palabra en words (sin el campo id, que se autogenera)
        sql_lines.append(f"""INSERT OR IGNORE INTO words (english, spanish, pronunciation, parts, correct_count, wrong_count)
VALUES ('{english}', '{spanish}', '{pronunciation}', '{parts}', 0, 0);""")
        
        # Insertar la relación en word_groups usando un subquery para obtener el id de la palabra
        sql_lines.append(f"""INSERT OR IGNORE INTO word_groups (word_id, group_id)
VALUES ((SELECT id FROM words WHERE english = '{english}'), {group_identifier});""")
    
    # Actualizar el contador de palabras en el grupo
    sql_lines.append(f"""UPDATE groups
SET words_count = (SELECT COUNT(*) FROM word_groups WHERE group_id = {group_identifier})
WHERE id = {group_identifier};""")
    
    return "\n".join(sql_lines)
