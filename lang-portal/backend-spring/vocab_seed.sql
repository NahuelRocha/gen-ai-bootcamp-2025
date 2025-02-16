INSERT OR IGNORE INTO words (english, spanish, pronunciation, parts, correct_count, wrong_count)
VALUES ('Doctor', 'Médico', '/dəˈsaɪtər/', '{"type": "profession", "category": "medical"}', 0, 0);
INSERT OR IGNORE INTO word_groups (word_id, group_id)
VALUES ((SELECT id FROM words WHERE english = 'Doctor'), 8);
INSERT OR IGNORE INTO words (english, spanish, pronunciation, parts, correct_count, wrong_count)
VALUES ('Teacher', 'Profesor', '/ˈtiːtər/', '{"type": "profession", "category": "educational"}', 0, 0);
INSERT OR IGNORE INTO word_groups (word_id, group_id)
VALUES ((SELECT id FROM words WHERE english = 'Teacher'), 8);
INSERT OR IGNORE INTO words (english, spanish, pronunciation, parts, correct_count, wrong_count)
VALUES ('Engineer', 'Ingeniero', '/ɪnˈdʒiːnər/', '{"type": "profession", "category": "technical"}', 0, 0);
INSERT OR IGNORE INTO word_groups (word_id, group_id)
VALUES ((SELECT id FROM words WHERE english = 'Engineer'), 8);
UPDATE groups
SET words_count = (SELECT COUNT(*) FROM word_groups WHERE group_id = 8)
WHERE id = 8;