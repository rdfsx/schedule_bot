CREATE TABLE users (id INTEGER PRIMARY KEY, created_at TEXT, updated_at TEXT);
CREATE TABLE teachers (id INTEGER PRIMARY KEY, full_name TEXT NOT NULL, created_at TEXT, updated_at TEXT);
CREATE TABLE teacher_rating (
  user_id INTEGER NOT NULL, teacher_id INTEGER NOT NULL, rate INTEGER NOT NULL, link TEXT,
  created_at TEXT, updated_at TEXT,
  PRIMARY KEY (user_id, teacher_id),
  CONSTRAINT rating_1_to_5 CHECK (typeof(rate) = 'integer' AND rate BETWEEN 1 AND 5)
);
CREATE INDEX rating_teacher_idx ON teacher_rating(teacher_id);
