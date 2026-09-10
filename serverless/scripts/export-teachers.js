import { execFile } from 'node:child_process';
import { mkdir, readFile, writeFile, appendFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { promisify } from 'node:util';

const curl = promisify(execFile);
const endpoint = 'https://sc.gstu.by/api/schedules/autocomplete';
const slugAlphabet = [...'abcdefghijklmnopqrstuvwxyz0123456789-_'];
const output = resolve(process.argv[2] || 'backups/sc-teachers-20260910');
const networkInterface = process.argv[3] || 'en0';
const queries = new Map();
const teachers = new Map();
const exactSlugs = new Map();

async function request(url) {
  const { stdout } = await curl('/usr/bin/curl', [
    '--interface', networkInterface, '--noproxy', '*',
    '--connect-timeout', '5', '--max-time', '20', '--silent', '--show-error',
    '--retry', '3', '--retry-max-time', '90',
    '--write-out', '\n%{http_code}', url,
  ], { maxBuffer: 4 * 1024 * 1024 });
  const separator = stdout.lastIndexOf('\n');
  const status = Number(stdout.slice(separator + 1));
  const body = JSON.parse(stdout.slice(0, separator));
  if (status !== 200 && status !== 404) throw new Error(`HTTP ${status}: ${body.message || 'request failed'}`);
  await new Promise(done => setTimeout(done, 150));
  return { status, body };
}

function collectTeacher(teacher) {
  if (typeof teacher.slug !== 'string' || !/^[a-z0-9_-]+$/.test(teacher.slug)
      || typeof teacher.fullName !== 'string' || !teacher.fullName.trim()) {
    throw new Error('Teacher without a supported slug or full name');
  }
  const previous = teachers.get(teacher.slug);
  if (previous && previous.fullName !== teacher.fullName) {
    throw new Error(`Name changed while exporting: ${teacher.slug}`);
  }
  teachers.set(teacher.slug, teacher);
}

function collect(query, data) {
  if (!Array.isArray(data.teachers) || typeof data.hasMore !== 'boolean') {
    throw new Error(`Unexpected response for ${JSON.stringify(query)}`);
  }
  for (const teacher of data.teachers) collectTeacher(teacher);
  queries.set(query, data);
}

async function search(query) {
  if (queries.has(query)) return queries.get(query);
  const { status, body } = await request(`${endpoint}?q=${encodeURIComponent(query)}`);
  if (status !== 200 || body.success !== true) throw new Error(`Search failed: ${JSON.stringify(query)}`);
  collect(query, body.data);
  await appendFile(`${output}/queries.jsonl`, `${JSON.stringify({ query, ...body.data })}\n`, { mode: 0o600 });
  if (queries.size % 25 === 0) console.log(`Queries: ${queries.size}; unique teachers: ${teachers.size}; query: ${query}`);
  return body.data;
}

async function readExactSlug(slug) {
  if (teachers.has(slug) || exactSlugs.has(slug)) return;
  const { status, body } = await request(`https://sc.gstu.by/api/schedules/teacher/${encodeURIComponent(slug)}`);
  let teacher = null;
  if (status === 200) {
    const entity = body.data?.entity;
    if (body.success !== true || entity?.slug !== slug) throw new Error(`Unexpected exact slug response: ${slug}`);
    teacher = {
      slug, fullName: entity.fullName, firstName: entity.firstName,
      lastName: entity.lastName, middleName: entity.middleName, shortName: entity.shortName,
      position: { name: entity.position, shortName: entity.positionShort },
      degree: { name: entity.degree, shortName: entity.degreeShort },
      cafedra: { name: entity.cafedra, shortName: entity.cafedraShort, slug: entity.cafedraSlug },
      faculty: { name: entity.faculty, shortName: entity.facultyShort, slug: entity.facultySlug },
    };
    collectTeacher(teacher);
  }
  exactSlugs.set(slug, teacher);
  await appendFile(`${output}/exact-slugs.jsonl`, `${JSON.stringify({ slug, teacher })}\n`, { mode: 0o600 });
}

function truncated(data) {
  return data.teachers.length >= 10 && data.hasMore;
}

async function save(stage, coverage = null) {
  const rows = [...teachers.values()].sort((a, b) => a.fullName.localeCompare(b.fullName, 'ru') || a.slug.localeCompare(b.slug));
  await writeFile(`${output}/teachers.json`, JSON.stringify({
    source: endpoint, exported_at: new Date().toISOString(), stage,
    query_count: queries.size, count: rows.length,
    completeness: coverage
      ? 'All reachable public-search slug prefixes in the checked alphabet; administrative total and hidden records are not available.'
      : 'Incomplete export; resume using the same output directory.',
    coverage, teachers: rows,
  }, null, 2) + '\n', { mode: 0o600 });
  await writeFile(`${output}/teachers.txt`, rows.map(row => row.fullName).join('\n') + '\n', { mode: 0o600 });
  console.log(`Saved ${rows.length} teachers (${stage})`);
}

async function main() {
  await mkdir(output, { recursive: true, mode: 0o700 });
  try {
    const cache = await readFile(`${output}/queries.jsonl`, 'utf8');
    for (const line of cache.split('\n').filter(Boolean)) {
      const { query, ...data } = JSON.parse(line);
      collect(query, data);
    }
  } catch (error) { if (error.code !== 'ENOENT') throw error; }
  try {
    const cache = await readFile(`${output}/exact-slugs.jsonl`, 'utf8');
    for (const line of cache.split('\n').filter(Boolean)) {
      const { slug, teacher } = JSON.parse(line);
      exactSlugs.set(slug, teacher);
      if (teacher && !teachers.has(slug)) collectTeacher(teacher);
    }
  } catch (error) { if (error.code !== 'ENOENT') throw error; }

  // Latin queries select slug prefixes, avoiding ambiguous Cyrillic name prefixes.
  const pending = [...slugAlphabet];
  const checked = [];
  const expanded = [];
  for (let offset = 0; offset < pending.length; offset++) {
    const prefix = pending[offset];
    // The search treats an unescaped underscore as a SQL LIKE wildcard.
    const data = await search(prefix.replaceAll('_', '\\_'));
    if (data.teachers.some(t => !t.slug.startsWith(prefix))) {
      throw new Error(`Search no longer matches slug prefixes: ${prefix}`);
    }
    checked.push(prefix);
    if (truncated(data)) {
      // A complete slug can itself prefix other slugs; do not lose that record.
      await readExactSlug(prefix);
      expanded.push(prefix);
      pending.push(...slugAlphabet.map(letter => prefix + letter));
    }
  }
  await save('complete public slug-prefix scan', {
    alphabet: slugAlphabet.join(''), checked_prefixes: checked,
    expanded_prefixes: expanded, unresolved_prefixes: [],
    exact_slug_checks: exactSlugs.size,
  });
}

main().catch(async error => {
  console.error(error.message);
  if (queries.size) await save('interrupted');
  process.exitCode = 1;
});
