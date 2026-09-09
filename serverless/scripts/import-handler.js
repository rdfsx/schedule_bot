// Only sent to `tgcloud run`; this file is outside the deployable directories.
import { db } from 'sdk';
import { columns, keys, validateRows, projectRow, sameRow, rowKey } from 'lib/transfer-data';

export default async function (input, ctx) {
  if (ctx?.update) throw new Error('Migration must not be invoked by a Telegram update');
  const { table, action } = input;
  if (!Object.hasOwn(columns, table)) throw new Error('Unknown table');
  if (action === 'read') {
    if (!Number.isSafeInteger(input.offset) || input.offset < 0) throw new Error('Invalid offset');
    return db.all(`SELECT ${columns[table].join(',')} FROM ${table}
      ORDER BY ${keys[table].join(',')} LIMIT 2000 OFFSET :offset`, { ':offset': input.offset });
  }
  if (action !== 'import' || !Array.isArray(input.rows) || input.rows.length > 500) throw new Error('Invalid import batch');
  validateRows(table, input.rows);
  for (const original of input.rows) {
    const row = projectRow(table, original);
    const params = Object.fromEntries(columns[table].map(key => [`:${key}`, row[key]]));
    const parentCheck = table === 'teacher_rating'
      ? 'WHERE EXISTS (SELECT 1 FROM users WHERE id = :user_id) AND EXISTS (SELECT 1 FROM teachers WHERE id = :teacher_id)'
      : 'WHERE 1';
    await db.run(`INSERT INTO ${table} (${columns[table].join(',')})
      SELECT ${Object.keys(params).join(',')} ${parentCheck}
      ON CONFLICT(${keys[table].join(',')}) DO NOTHING`, params);
    const keyParams = Object.fromEntries(keys[table].map(key => [`:${key}`, row[key]]));
    const existing = await db.get(`SELECT * FROM ${table} WHERE ${keys[table].map(key => `${key} = :${key}`).join(' AND ')}`, keyParams);
    if (!existing || !sameRow(table, row, existing)) throw new Error(`Import conflict in ${table}: ${rowKey(table, row)}`);
  }
  return { checked: input.rows.length };
}
