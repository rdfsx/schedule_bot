export function normalize(text) {
  return String(text ?? '').normalize('NFKC').toLowerCase().replace(/ё/g, 'е')
    .replace(/[^а-яa-z]+/g, ' ').trim().replace(/\s+/g, ' ');
}

export function stripPrefix(text) {
  return String(text ?? '').replace(/^\s*#p\s*/i, '').trim();
}

function correctLayout(text) {
  const en = "qwertyuiop[]asdfghjkl;'zxcvbnm,.`";
  const ru = 'йцукенгшщзхъфывапролджэячсмитьбюё';
  return [...text.toLowerCase()].map(c => en.includes(c) ? ru[en.indexOf(c)] : c).join('');
}

export function distance(a, b) {
  const d = Array.from({ length: a.length + 1 }, () => Array(b.length + 1).fill(0));
  for (let i = 0; i <= a.length; i++) d[i][0] = i;
  for (let j = 0; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] !== b[j - 1]));
      if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) {
        d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
      }
    }
  }
  return d[a.length][b.length];
}

function scoreName(name, query) {
  if (name === query) return 0;
  const words = name.split(' ');
  if (words[0] === query) return 1;
  const tokens = query.split(' ');
  if (tokens.length > words.length || tokens.every(t => t.length === 1)) return Infinity;
  // Each query token matches a different part of the name, including «И. И. Иванов».
  function match(index, used, cost) {
    if (index === tokens.length) return cost;
    const token = tokens[index];
    let best = Infinity;
    for (let j = 0; j < words.length; j++) {
      if (used.includes(j)) continue;
      let penalty = words[j].startsWith(token) ? 0 : Infinity;
      const threshold = token.length >= 8 ? 2 : token.length >= 4 ? 1 : 0;
      if (penalty && threshold && Math.abs(token.length - words[j].length) <= threshold) {
        const errors = distance(token, words[j]);
        if (errors <= threshold) penalty = 10 + errors;
      }
      if (Number.isFinite(penalty)) best = Math.min(best, match(index + 1, [...used, j], cost + penalty));
    }
    return best;
  }
  return 2 + match(0, [], 0);
}

export function searchTeachers(teachers, input) {
  const raw = stripPrefix(input);
  if (raw.length > 100) return [];
  const query = normalize(raw);
  if (raw && !query) return [];
  const corrected = /[a-z]/i.test(raw) ? normalize(correctLayout(raw)) : query;
  return teachers.map(teacher => {
    const name = normalize(teacher.full_name);
    const direct = query ? scoreName(name, query) : 0;
    const layout = corrected && corrected !== query ? scoreName(name, corrected) : Infinity;
    return { ...teacher, score: Math.min(direct, layout + 0.25), exact: Boolean(query) && Math.min(direct, layout) <= 1 };
  }).filter(t => Number.isFinite(t.score))
    .sort((a, b) => a.score - b.score || a.full_name.localeCompare(b.full_name, 'ru') || a.id - b.id);
}
