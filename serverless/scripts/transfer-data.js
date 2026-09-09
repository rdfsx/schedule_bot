// Pure validation shared by local migration tools and the temporary cloud runner.
export const columns = {
  users: ['id', 'created_at', 'updated_at'],
  teachers: ['id', 'full_name', 'created_at', 'updated_at'],
  teacher_rating: ['user_id', 'teacher_id', 'rate', 'link', 'created_at', 'updated_at'],
};
export const keys = { users: ['id'], teachers: ['id'], teacher_rating: ['user_id', 'teacher_id'] };
export const rowKey = (table, row) => keys[table].map(key => row[key]).join(':');

export function projectRow(table, row) {
  return Object.fromEntries(columns[table].map(key => [key, row[key] ?? null]));
}

export function validateRows(table, rows) {
  if (!Object.hasOwn(columns, table) || !Array.isArray(rows)) throw new Error('Unknown table or invalid rows');
  const seen = new Set();
  for (const row of rows) {
    if (!row || keys[table].some(key => !Number.isSafeInteger(row[key]) || row[key] <= 0)) throw new Error(`${table}: invalid ID`);
    const key = rowKey(table, row);
    if (seen.has(key)) throw new Error(`${table}: duplicate ${key}`);
    seen.add(key);
    for (const field of ['created_at', 'updated_at']) {
      if (row[field] != null && (typeof row[field] !== 'string' || !Number.isFinite(Date.parse(row[field])))) {
        throw new Error(`${table} ${key}: invalid ${field}`);
      }
    }
    if (table === 'teachers' && (typeof row.full_name !== 'string' || !row.full_name.trim())) throw new Error(`teachers ${key}: empty name`);
    if (table === 'teacher_rating') {
      if (!Number.isInteger(row.rate) || row.rate < 1 || row.rate > 5) throw new Error(`teacher_rating ${key}: invalid rate`);
      if (row.link != null && typeof row.link !== 'string') throw new Error(`teacher_rating ${key}: invalid link`);
    }
  }
}

export function validateExport(data) {
  if (data?.format !== 1) throw new Error('Unsupported export format');
  for (const table of Object.keys(columns)) validateRows(table, data[table]);
  const users = new Set(data.users.map(u => u.id));
  const teachers = new Map(data.teachers.map(t => [t.id, { count: 0, sum: 0 }]));
  for (const row of data.teacher_rating) {
    if (!users.has(row.user_id) || !teachers.has(row.teacher_id)) throw new Error(`Orphan vote ${rowKey('teacher_rating', row)}`);
    const total = teachers.get(row.teacher_id);
    total.count++;
    total.sum += row.rate;
  }
  for (const teacher of data.teachers) {
    const total = teachers.get(teacher.id);
    // PostgreSQL exports carry the original counters; Serverless backups do not.
    if (Object.hasOwn(teacher, 'count') && teacher.count !== total.count ||
        Object.hasOwn(teacher, 'rating') && teacher.rating !== total.sum) {
      throw new Error(`Teacher ${teacher.id}: legacy counters disagree with individual votes`);
    }
  }
  return Object.fromEntries(Object.keys(columns).map(table => [table, data[table].map(row => projectRow(table, row))]));
}

export function sameRow(table, a, b) {
  return columns[table].every(key => (a[key] ?? null) === (b[key] ?? null));
}
