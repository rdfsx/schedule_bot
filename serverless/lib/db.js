import { db } from 'sdk';

export function validId(value) {
  return Number.isSafeInteger(value) && value > 0;
}

export async function addUser(id) {
  if (!validId(id)) return false;
  const result = await db.run(`INSERT INTO users (id, created_at, updated_at)
    VALUES (:id, :now, :now) ON CONFLICT(id) DO NOTHING RETURNING id`,
  { ':id': id, ':now': new Date().toISOString() });
  return result.rows.length > 0;
}

export async function listTeachers() {
  return db.all('SELECT id, full_name FROM teachers ORDER BY id');
}

export async function teacherCard(id, userId) {
  return db.get(`SELECT t.id, t.full_name,
      COUNT(r.rate) AS count, AVG(r.rate) AS average,
      MAX(CASE WHEN r.user_id = :user THEN r.rate END) AS own_rate,
      MAX(CASE WHEN r.user_id = :user THEN r.created_at END) AS own_created_at
    FROM teachers t LEFT JOIN teacher_rating r ON r.teacher_id = t.id
    WHERE t.id = :id GROUP BY t.id, t.full_name`, { ':id': id, ':user': userId });
}

export async function ratingSummaries(ids, userId) {
  if (!ids.length) return [];
  const idsByParameter = Object.fromEntries(ids.map((id, i) => [`:id${i}`, id]));
  return db.all(`SELECT teacher_id, COUNT(*) AS count, AVG(rate) AS average,
      MAX(CASE WHEN user_id = :user THEN rate END) AS own_rate,
      MAX(CASE WHEN user_id = :user THEN created_at END) AS own_created_at
    FROM teacher_rating WHERE teacher_id IN (${Object.keys(idsByParameter).join(',')})
    GROUP BY teacher_id`, { ':user': userId, ...idsByParameter });
}

export async function setRating(teacherId, userId, rate) {
  if (!validId(teacherId) || !validId(userId) || !Number.isInteger(rate) || rate < 1 || rate > 5) return;
  // One statement checks both parents and inserts. Retries do not overwrite a vote.
  await db.run(`INSERT INTO teacher_rating (user_id, teacher_id, rate, created_at, updated_at)
    SELECT :user, :teacher, :rate, :now, :now
    WHERE EXISTS (SELECT 1 FROM users WHERE id = :user)
      AND EXISTS (SELECT 1 FROM teachers WHERE id = :teacher)
    ON CONFLICT(user_id, teacher_id) DO NOTHING`, {
    ':user': userId, ':teacher': teacherId, ':rate': rate, ':now': new Date().toISOString(),
  });
}

export async function deleteRating(teacherId, userId, createdAt) {
  // New buttons bind deletion to the displayed vote, not a later replacement.
  await db.run(`DELETE FROM teacher_rating WHERE user_id = :user AND teacher_id = :teacher
    AND (:created IS NULL OR created_at IS :created)`, {
    ':user': userId, ':teacher': teacherId, ':created': createdAt ?? null,
  });
}
