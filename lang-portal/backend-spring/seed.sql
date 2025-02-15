-- Populate study_activities table
INSERT INTO study_activities (id, name, url)
VALUES (
        1,
        'Flashcards',
        'https://learning-portal.com/flashcards'
    ),
    (
        2,
        'Multiple Choice Quiz',
        'https://learning-portal.com/quiz'
    ),
    (
        3,
        'Writing Practice',
        'https://learning-portal.com/writing'
    ),
    (
        4,
        'Listening Exercise',
        'https://learning-portal.com/listening'
    ),
    (
        5,
        'Speaking Practice',
        'https://learning-portal.com/speaking'
    );
-- Populate groups table with different categories
INSERT INTO groups (id, name, words_count)
VALUES (1, 'Basic Greetings', 0),
    (2, 'Numbers and Counting', 0),
    (3, 'Colors and Shapes', 0),
    (4, 'Family Members', 0),
    (5, 'Food and Drinks', 0),
    (6, 'Daily Activities', 0),
    (7, 'Weather and Seasons', 0),
    (8, 'Professions', 0),
    (9, 'Travel and Transportation', 0),
    (10, 'House and Furniture', 0);
-- Populate words table
INSERT INTO words (
        id,
        english,
        spanish,
        pronunciation,
        parts,
        correct_count,
        wrong_count
    )
VALUES -- Basic Greetings
    (
        1,
        'Hello',
        'Hola',
        'həˈləʊ',
        '{"type": "greeting", "usage": "formal/informal"}',
        0,
        0
    ),
    (
        2,
        'Good morning',
        'Buenos días',
        'ɡʊd ˈmɔːnɪŋ',
        '{"type": "greeting", "usage": "formal", "time": "morning"}',
        0,
        0
    ),
    (
        3,
        'Good afternoon',
        'Buenas tardes',
        'ɡʊd ɑːftəˈnuːn',
        '{"type": "greeting", "usage": "formal", "time": "afternoon"}',
        0,
        0
    ),
    (
        4,
        'Goodbye',
        'Adiós',
        'ɡʊdˈbaɪ',
        '{"type": "farewell", "usage": "formal/informal"}',
        0,
        0
    ),
    (
        5,
        'See you later',
        'Hasta luego',
        'siː juː ˈleɪtə',
        '{"type": "farewell", "usage": "informal"}',
        0,
        0
    ),
    -- Numbers
    (
        6,
        'One',
        'Uno',
        'wʌn',
        '{"type": "number", "category": "cardinal"}',
        0,
        0
    ),
    (
        7,
        'Two',
        'Dos',
        'tuː',
        '{"type": "number", "category": "cardinal"}',
        0,
        0
    ),
    (
        8,
        'Three',
        'Tres',
        'θriː',
        '{"type": "number", "category": "cardinal"}',
        0,
        0
    ),
    (
        9,
        'Four',
        'Cuatro',
        'fɔː',
        '{"type": "number", "category": "cardinal"}',
        0,
        0
    ),
    (
        10,
        'Five',
        'Cinco',
        'faɪv',
        '{"type": "number", "category": "cardinal"}',
        0,
        0
    ),
    -- Colors
    (
        11,
        'Red',
        'Rojo',
        'red',
        '{"type": "color", "category": "primary"}',
        0,
        0
    ),
    (
        12,
        'Blue',
        'Azul',
        'bluː',
        '{"type": "color", "category": "primary"}',
        0,
        0
    ),
    (
        13,
        'Yellow',
        'Amarillo',
        'ˈjeləʊ',
        '{"type": "color", "category": "primary"}',
        0,
        0
    ),
    (
        14,
        'Green',
        'Verde',
        'ɡriːn',
        '{"type": "color", "category": "secondary"}',
        0,
        0
    ),
    (
        15,
        'Purple',
        'Morado',
        'ˈpɜːpl',
        '{"type": "color", "category": "secondary"}',
        0,
        0
    ),
    -- Family Members
    (
        16,
        'Mother',
        'Madre',
        'ˈmʌðə',
        '{"type": "family", "relationship": "parent"}',
        0,
        0
    ),
    (
        17,
        'Father',
        'Padre',
        'ˈfɑːðə',
        '{"type": "family", "relationship": "parent"}',
        0,
        0
    ),
    (
        18,
        'Sister',
        'Hermana',
        'ˈsɪstə',
        '{"type": "family", "relationship": "sibling"}',
        0,
        0
    ),
    (
        19,
        'Brother',
        'Hermano',
        'ˈbrʌðə',
        '{"type": "family", "relationship": "sibling"}',
        0,
        0
    ),
    (
        20,
        'Grandmother',
        'Abuela',
        'ˈɡranmʌðə',
        '{"type": "family", "relationship": "grandparent"}',
        0,
        0
    ),
    -- Food and Drinks
    (
        21,
        'Water',
        'Agua',
        'ˈwɔːtə',
        '{"type": "drink", "category": "beverage"}',
        0,
        0
    ),
    (
        22,
        'Bread',
        'Pan',
        'bred',
        '{"type": "food", "category": "bakery"}',
        0,
        0
    ),
    (
        23,
        'Apple',
        'Manzana',
        'ˈapl',
        '{"type": "food", "category": "fruit"}',
        0,
        0
    ),
    (
        24,
        'Chicken',
        'Pollo',
        'ˈtʃɪkɪn',
        '{"type": "food", "category": "meat"}',
        0,
        0
    ),
    (
        25,
        'Rice',
        'Arroz',
        'raɪs',
        '{"type": "food", "category": "grain"}',
        0,
        0
    );
-- Populate word_groups table
-- Basic Greetings
INSERT INTO word_groups (word_id, group_id)
VALUES (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    -- Numbers
    (6, 2),
    (7, 2),
    (8, 2),
    (9, 2),
    (10, 2),
    -- Colors
    (11, 3),
    (12, 3),
    (13, 3),
    (14, 3),
    (15, 3),
    -- Family Members
    (16, 4),
    (17, 4),
    (18, 4),
    (19, 4),
    (20, 4),
    -- Food and Drinks
    (21, 5),
    (22, 5),
    (23, 5),
    (24, 5),
    (25, 5);
-- Update words_count in groups
UPDATE groups
SET words_count = 5
WHERE id IN (1, 2, 3, 4, 5);
-- Create some sample study sessions
INSERT INTO study_sessions (id, group_id, study_activity_id, created_at)
VALUES (1, 1, 1, datetime('now', '-7 days')),
    (2, 2, 2, datetime('now', '-6 days')),
    (3, 3, 1, datetime('now', '-5 days')),
    (4, 4, 3, datetime('now', '-4 days')),
    (5, 5, 4, datetime('now', '-3 days'));
-- Add some sample word reviews
INSERT INTO word_review_items (word_id, study_session_id, correct, created_at)
VALUES -- Session 1 reviews (Greetings)
    (1, 1, true, datetime('now', '-7 days')),
    (2, 1, true, datetime('now', '-7 days')),
    (3, 1, false, datetime('now', '-7 days')),
    (4, 1, true, datetime('now', '-7 days')),
    (5, 1, false, datetime('now', '-7 days')),
    -- Session 2 reviews (Numbers)
    (6, 2, true, datetime('now', '-6 days')),
    (7, 2, true, datetime('now', '-6 days')),
    (8, 2, true, datetime('now', '-6 days')),
    (9, 2, false, datetime('now', '-6 days')),
    (10, 2, true, datetime('now', '-6 days'));
-- Update correct_count and wrong_count in words table
UPDATE words
SET correct_count = (
        SELECT COUNT(*)
        FROM word_review_items
        WHERE word_review_items.word_id = words.id
            AND correct = true
    );
UPDATE words
SET wrong_count = (
        SELECT COUNT(*)
        FROM word_review_items
        WHERE word_review_items.word_id = words.id
            AND correct = false
    );