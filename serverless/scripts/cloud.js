import { readFile, readdir, writeFile } from 'node:fs/promises';
import { parseEnv } from 'node:util';
import { fileURLToPath } from 'node:url';
import { runFunction, getFiles, getWebhook, applyMigration } from '../node_modules/@tgcloud/cli/src/api/endpoints.js';

// Never enable credential/request debug output in migration or test scripts.
process.env.TGCLOUD_DEBUG = '0';

export const root = fileURLToPath(new URL('../', import.meta.url));
export { getFiles, getWebhook, applyMigration };

export async function environment() {
  let file = {};
  try { file = parseEnv(await readFile(new URL('../../.env', import.meta.url), 'utf8')); }
  catch (error) { if (error.code !== 'ENOENT') throw error; }
  return { ...file, ...process.env };
}

export async function accessToken() {
  const env = await environment();
  const token = env.TGCLOUD_TOKEN || env.SERVERLESS_ACCESS_TOKEN;
  if (!/^app\d+:[A-Za-z0-9_-]+$/.test(token ?? '')) throw new Error('Set SERVERLESS_ACCESS_TOKEN in the root .env');
  return token;
}

export async function configure() {
  const env = await environment();
  const admin = Number(env.ADMIN_ID);
  if (!Number.isSafeInteger(admin) || admin <= 0) throw new Error('Set ADMIN_ID in the root .env');
  await writeFile(new URL('../lib/config.js', import.meta.url), `// Generated from ADMIN_ID; no access token is deployed.\nexport const adminId = ${admin};\n`);
}

export async function sources() {
  const result = { schema: await readFile(new URL('../schema.js', import.meta.url), 'utf8') };
  for (const dir of ['lib', 'handlers']) {
    for (const file of await readdir(`${root}${dir}`)) {
      if (file.endsWith('.js') && !file.endsWith('.example.js')) {
        result[`${dir}/${file.slice(0, -3)}`] = await readFile(`${root}${dir}/${file}`, 'utf8');
      }
    }
  }
  return result;
}

// Same official CLI implementation as `tgcloud run`, with JSON kept out of shell arguments.
export async function run(token, modules, args = {}, ctx = {}) {
  const response = await runFunction(token, 'handlers/message', modules, args, ctx);
  return response.result;
}
