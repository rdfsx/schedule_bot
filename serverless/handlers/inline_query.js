import { api } from 'sdk';
import { ensureUser } from 'lib/users';
import { listTeachers, ratingSummaries } from 'lib/db';
import { searchTeachers } from 'lib/search';
import { cardView, summary } from 'lib/views';

export default async function (query) {
  if (!query.from || query.from.is_bot) return;
  await ensureUser(query.from);
  const offset = /^\d{1,8}$/.test(query.offset ?? '') ? Number(query.offset) : 0;
  const matches = searchTeachers(await listTeachers(), query.query);
  const page = matches.slice(offset, offset + 20);
  const stats = new Map((await ratingSummaries(page.map(t => t.id), query.from.id)).map(r => [r.teacher_id, r]));
  const results = page.map(t => {
    const teacher = { ...t, ...(stats.get(t.id) ?? { count: 0, own_rate: null, own_created_at: null }) };
    const view = cardView(teacher, query.from.id);
    return { type: 'article', id: String(t.id), title: t.full_name, description: summary(teacher),
      input_message_content: { message_text: view.text, parse_mode: view.parse_mode }, reply_markup: view.reply_markup };
  });
  if (!results.length && !offset) results.push({ type: 'article', id: 'not-found',
    title: 'Преподаватель не найден', description: 'Попробуйте другую фамилию или инициалы.',
    input_message_content: { message_text: 'Преподаватель не найден' } });
  await api.answerInlineQuery({ inline_query_id: query.id, results, cache_time: 0,
    is_personal: true, next_offset: offset + 20 < matches.length ? String(offset + 20) : '' });
}
