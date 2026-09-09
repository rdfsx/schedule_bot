import { readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { accessToken, run } from './cloud.js';
import { columns, rowKey, validateExport, sameRow } from './transfer-data.js';

const importBatchSize = 500;
const readPageSize = 2000;

export async function transferSources() {
  return {
    'handlers/message': await readFile(new URL('./import-handler.js', import.meta.url), 'utf8'),
    'lib/transfer-data': await readFile(new URL('./transfer-data.js', import.meta.url), 'utf8'),
  };
}

async function cloudRun(token, modules, args) {
  for (;;) {
    try {
      return await run(token, modules, args);
    } catch (error) {
      const retry = /Too many requests: retry after (\d+)/i.exec(error.message);
      if (!retry) throw error;
      const seconds = Number(retry[1]) + 1;
      console.log(`Rate limited; retrying in ${seconds}s`);
      await new Promise(resolve => setTimeout(resolve, seconds * 1000));
    }
  }
}

async function main() {
  const [action, filename] = process.argv.slice(2);
  if (!['import', 'verify', 'backup'].includes(action) || !filename) throw new Error('Usage: node scripts/transfer.js import|verify|backup FILE.json');
  const token = await accessToken();
  const modules = await transferSources();
  const expected = action === 'backup' ? null : validateExport(JSON.parse(await readFile(filename, 'utf8')));
  if (action === 'import') {
    for (const table of Object.keys(columns)) {
      for (let offset = 0; offset < expected[table].length; offset += importBatchSize) {
        await cloudRun(token, modules, { action: 'import', table, rows: expected[table].slice(offset, offset + importBatchSize) });
      }
      console.log(`Imported and checked ${table}: ${expected[table].length}`);
    }
  }
  const actual = { format: 1, exported_at: new Date().toISOString() };
  for (const table of Object.keys(columns)) {
    actual[table] = [];
    for (let offset = 0; ; offset += readPageSize) {
      const page = await cloudRun(token, modules, { action: 'read', table, offset });
      if (!Array.isArray(page)) throw new Error('Unexpected export response');
      actual[table].push(...page);
      if (page.length < readPageSize) break;
    }
    if (expected) {
      const found = new Map(actual[table].map(row => [rowKey(table, row), row]));
      if (actual[table].length !== expected[table].length) throw new Error(`${table}: row count differs`);
      for (const row of expected[table]) {
        const existing = found.get(rowKey(table, row));
        if (!existing || !sameRow(table, row, existing)) throw new Error(`${table}: row differs (${rowKey(table, row)})`);
      }
      console.log(`Verified every field in ${table}: ${actual[table].length}`);
    }
  }
  validateExport(actual);
  if (action === 'backup') {
    await writeFile(filename, JSON.stringify(actual), { flag: 'wx', mode: 0o600 });
    console.log('Backup saved. For a consistent snapshot, pause writes before running backup.');
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch(error => { console.error(error.message); process.exitCode = 1; });
}
