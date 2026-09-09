-- Run with psql -X -qAt -v ON_ERROR_STOP=1 -f export.sql > ratings.json
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY;
SET LOCAL TIME ZONE 'UTC';
SELECT json_build_object(
  'format', 1,
  'exported_at', now(),
  'users', COALESCE((SELECT json_agg(u ORDER BY u.id) FROM users u), '[]'::json),
  'teachers', COALESCE((SELECT json_agg(t ORDER BY t.id) FROM teachers t), '[]'::json),
  'teacher_rating', COALESCE((SELECT json_agg(r ORDER BY r.user_id, r.teacher_id) FROM teacher_rating r), '[]'::json)
);
COMMIT;
