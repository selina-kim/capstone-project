-- Built-in reference decks seeded at database initialization.
-- Requires the following CSV files alongside this script in database/init/:
--   chinese_mando_vocab_beginner.csv
--   korean_vocab_beginner.csv
--   french_vocab_beginner.csv
-- Each CSV is two columns (word, translation), no header row.

INSERT INTO Users (u_id, email, display_name, timezone)
VALUES ('system', 'system@languine.app', 'Languine', 'UTC')
ON CONFLICT (u_id) DO NOTHING;

INSERT INTO Decks (u_id, deck_name, word_lang, trans_lang, description, is_public)
VALUES
    ('system', 'Mandarin Chinese Beginner', 'Chinese (Mandarin)', 'English', 'Essential beginner vocabulary for Mandarin Chinese', true),
    ('system', 'Korean Beginner',           'Korean',             'English', 'Essential beginner vocabulary for Korean',           true),
    ('system', 'French Beginner',           'French',             'English', 'Essential beginner vocabulary for French',           true)
ON CONFLICT (u_id, deck_name) DO NOTHING;

-- ── Mandarin Chinese ──────────────────────────────────────────────────────────
CREATE TEMP TABLE tmp_cards (word text, translation text);

COPY tmp_cards FROM '/docker-entrypoint-initdb.d/chinese_mando_vocab_beginner.csv'
    WITH (FORMAT csv);

INSERT INTO Cards (d_id, word, translation)
SELECT deck.d_id, t.word, t.translation
FROM tmp_cards t
CROSS JOIN (
    SELECT d_id FROM Decks WHERE u_id = 'system' AND deck_name = 'Mandarin Chinese Beginner'
) AS deck;

DROP TABLE tmp_cards;

-- ── Korean ────────────────────────────────────────────────────────────────────
CREATE TEMP TABLE tmp_cards (word text, translation text);

COPY tmp_cards FROM '/docker-entrypoint-initdb.d/korean_vocab_beginner.csv'
    WITH (FORMAT csv);

INSERT INTO Cards (d_id, word, translation)
SELECT deck.d_id, t.word, t.translation
FROM tmp_cards t
CROSS JOIN (
    SELECT d_id FROM Decks WHERE u_id = 'system' AND deck_name = 'Korean Beginner'
) AS deck;

DROP TABLE tmp_cards;

-- ── French ────────────────────────────────────────────────────────────────────
CREATE TEMP TABLE tmp_cards (word text, translation text);

COPY tmp_cards FROM '/docker-entrypoint-initdb.d/french_vocab_beginner.csv'
    WITH (FORMAT csv);

INSERT INTO Cards (d_id, word, translation)
SELECT deck.d_id, t.word, t.translation
FROM tmp_cards t
CROSS JOIN (
    SELECT d_id FROM Decks WHERE u_id = 'system' AND deck_name = 'French Beginner'
) AS deck;

DROP TABLE tmp_cards;
