import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { randomBytes } from 'node:crypto';
import { accessToken, sources, run, getFiles, getWebhook, applyMigration } from './cloud.js';
import { changeId } from '../node_modules/@tgcloud/cli/src/core/db-changes.js';

const token = await accessToken();
const prefix = `test_${randomBytes(6).toString('hex')}_`;
const tables = ['users', 'teachers', 'teacher_rating'];
const beforeFiles = await getFiles(token);
const beforeWebhook = await getWebhook(token);
const modules = await sources();
modules['lib/config'] = 'export const adminId = 343726189;';
modules['lib/message-handler'] = modules['handlers/message'];
for (const [name, filename] of Object.entries({
  'lib/test-api': '../test/api.js', 'lib/scenarios': '../test/scenarios.js',
  'lib/import-handler': './import-handler.js', 'lib/transfer-data': './transfer-data.js',
})) modules[name] = await readFile(new URL(filename, import.meta.url), 'utf8');
modules['handlers/message'] = "export { default } from 'lib/scenarios';";
for (const name of Object.keys(modules)) modules[name] = modules[name].replaceAll("from 'sdk'", "from 'lib/test-sdk'");
modules['lib/test-sdk'] = `
  import { db as real } from 'sdk';
  export { api } from 'lib/test-api';
  const rewrite = sql => sql.replace(/\\b(users|teachers|teacher_rating)\\b/g, name => ${JSON.stringify(prefix)} + name);
  export const db = {
    run: (sql, params = {}) => real.run(rewrite(sql), params),
    get: (sql, params = {}) => real.get(rewrite(sql), params),
    all: (sql, params = {}) => real.all(rewrite(sql), params),
  };
`;
const schema = modules.schema.replace(/'(users|teachers|teacher_rating|rating_teacher_idx|rating_1_to_5)'/g,
  (_match, name) => `'${prefix}${name}'`);
let report;
try {
  const preview = await applyMigration(token, { schema, dry_run: true });
  const changes = preview.db_changes ?? [];
  const creates = changes.filter(c => tables.map(t => prefix + t).includes(c.table) && ['create_table', 'create_index'].includes(c.kind));
  assert.equal(creates.filter(c => c.kind === 'create_table').length, 3, 'Schema must create exactly three isolated tables');
  console.log(`Validated schema; creating ${creates.length} test objects (${prefix}).`);
  await applyMigration(token, { schema, apply: creates.map(changeId) });
  report = await run(token, modules);
  assert.ok(report?.assertions >= 40, 'Cloud scenarios did not complete');
  console.log(`Cloud handlers, SQLite and import: ${report.assertions} assertions passed.`);
} finally {
  await run(token, { 'handlers/message': `import { db } from 'sdk';
    export default async function () {
      ${tables.toReversed().map(t => `await db.run('DROP TABLE IF EXISTS ${prefix}${t}');`).join('\n')}
      return db.all("SELECT name FROM sqlite_master WHERE name LIKE '${prefix}%'");
    }` }).then(remaining => assert.equal(remaining.length, 0, 'Test objects remain'));
  const afterFiles = await getFiles(token);
  const afterWebhook = await getWebhook(token);
  assert.deepEqual(afterFiles, beforeFiles, 'Deployment state changed during tests');
  assert.equal(afterWebhook.url, beforeWebhook.url, 'Webhook changed during tests');
  assert.deepEqual(afterWebhook.allowed_updates, beforeWebhook.allowed_updates, 'Allowed updates changed');
  console.log('Test tables removed; deployed code and webhook unchanged.');
}
