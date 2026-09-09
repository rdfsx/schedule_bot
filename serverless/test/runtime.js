import { DatabaseSync } from 'node:sqlite';
import { readFile } from 'node:fs/promises';
import { SourceTextModule, SyntheticModule, createContext } from 'node:vm';
import { sources } from '../scripts/cloud.js';

export async function runtime() {
  const sqlite = new DatabaseSync(':memory:');
  sqlite.exec(await readFile(new URL('./schema.sql', import.meta.url), 'utf8'));
  const db = {
    async all(sql, params = {}) { return sqlite.prepare(sql).all(params); },
    async get(sql, params = {}) { return sqlite.prepare(sql).get(params) ?? null; },
    async run(sql, params = {}) {
      const stmt = sqlite.prepare(sql);
      if (/\bRETURNING\b/i.test(sql)) return { rows: stmt.all(params) };
      const result = stmt.run(params);
      return { rows: [], rowsAffected: result.changes };
    },
  };
  const modules = await sources();
  modules['lib/config'] = 'export const adminId = 343726189;';
  modules['lib/message-handler'] = modules['handlers/message'];
  for (const [name, filename] of Object.entries({
    'lib/test-api': './api.js', 'lib/scenarios': './scenarios.js',
    'lib/import-handler': '../scripts/import-handler.js', 'lib/transfer-data': '../scripts/transfer-data.js',
  })) modules[name] = await readFile(new URL(filename, import.meta.url), 'utf8');
  const context = createContext({ console });
  const loaded = new Map();
  function get(name) {
    if (loaded.has(name)) return loaded.get(name);
    if (!modules[name]) throw new Error(`Unknown module: ${name}`);
    const module = new SourceTextModule(modules[name], { context, identifier: name });
    loaded.set(name, module);
    return module;
  }
  const fakeApi = get('lib/test-api');
  await fakeApi.link(get);
  await fakeApi.evaluate();
  const sdk = new SyntheticModule(['db', 'api'], function () {
    this.setExport('db', db); this.setExport('api', fakeApi.namespace.api);
  }, { context });
  loaded.set('sdk', sdk);
  return {
    async run() {
      const module = get('lib/scenarios');
      await module.link(get);
      await module.evaluate();
      return module.namespace.default();
    },
    close() { sqlite.close(); },
  };
}
