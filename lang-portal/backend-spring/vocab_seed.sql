INSERT OR IGNORE INTO words (english, spanish, pronunciation, parts, correct_count, wrong_count)
VALUES ('Passport', 'Pasaporte', '/pəˈspôrt/', '{"type": "document", "usage": "official"}', 0, 0);
INSERT OR IGNORE INTO word_groups (word_id, group_id)
VALUES ((SELECT id FROM words WHERE english = 'Passport'), 9);
INSERT OR IGNORE INTO words (english, spanish, pronunciation, parts, correct_count, wrong_count)
VALUES ('Bus', 'autobus', '/ˈbʌs/', '{"type": "vehicle", "usage": "public transportation"}', 0, 0);
INSERT OR IGNORE INTO word_groups (word_id, group_id)
VALUES ((SELECT id FROM words WHERE english = 'Bus'), 9);
INSERT OR IGNORE INTO words (english, spanish, pronunciation, parts, correct_count, wrong_count)
VALUES ('Ticket', 'billete', '/ˈtɪkət/', '{"type": "document", "usage": "travel"}', 0, 0);
INSERT OR IGNORE INTO word_groups (word_id, group_id)
VALUES ((SELECT id FROM words WHERE english = 'Ticket'), 9);
INSERT OR IGNORE INTO words (english, spanish, pronunciation, parts, correct_count, wrong_count)
VALUES ('Luggage', 'maletas', '/ˈlʌɡədʒ/', '{"type": "item", "usage": "travel"}', 0, 0);
INSERT OR IGNORE INTO word_groups (word_id, group_id)
VALUES ((SELECT id FROM words WHERE english = 'Luggage'), 9);
INSERT OR IGNORE INTO words (english, spanish, pronunciation, parts, correct_count, wrong_count)
VALUES ('Train', 'tren', '/ˈtreɪn/', '{"type": "vehicle", "usage": "public transportation"}', 0, 0);
INSERT OR IGNORE INTO word_groups (word_id, group_id)
VALUES ((SELECT id FROM words WHERE english = 'Train'), 9);
INSERT OR IGNORE INTO words (english, spanish, pronunciation, parts, correct_count, wrong_count)
VALUES ('Ferry', 'barco', '/ˈfɛri/', '{"type": "vehicle", "usage": "water transportation"}', 0, 0);
INSERT OR IGNORE INTO word_groups (word_id, group_id)
VALUES ((SELECT id FROM words WHERE english = 'Ferry'), 9);
UPDATE groups
SET words_count = (SELECT COUNT(*) FROM word_groups WHERE group_id = 9)
WHERE id = 9;