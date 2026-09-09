import { api } from 'sdk';
import { ensureUser } from 'lib/users';
import { validId, listTeachers, teacherCard, setRating, deleteRating } from 'lib/db';
import { searchTeachers } from 'lib/search';
import { cardView, resultsView, editView, homeText, homeKeyboard } from 'lib/views';

export default async function (call) {
  if (!call.from || call.from.is_bot) return;
  await ensureUser(call.from);
  const answer = text => api.answerCallbackQuery({ callback_query_id: call.id, ...(text ? { text } : {}) });
  if ((!call.message?.chat || call.message.date === 0) && !call.inline_message_id) {
    return answer('Откройте карточку заново в чате с ботом.');
  }
  const parts = String(call.data ?? '').split(':');
  const action = parts[0];
  if (action === 'page') {
    if (!call.message?.chat) return answer('Отправьте фамилию ещё раз.');
    const query = call.message.reply_to_message?.text;
    if (!query || !/^\d{1,6}$/.test(parts[1] ?? '')) return answer('Отправьте фамилию ещё раз.');
    await answer();
    return editView(call.message, resultsView(searchTeachers(await listTeachers(), query), Number(parts[1])));
  }
  if (!['show', 'teacher', 'delete', 'remove'].includes(action)) {
    await answer();
    return editView(call.message, { text: homeText, link_preview_options: { is_disabled: true }, reply_markup: homeKeyboard }, call.inline_message_id);
  }
  const teacherId = Number(parts[action === 'show' ? 1 : 2]);
  const owner = action === 'show' ? call.from.id : Number(parts[1]);
  const rate = Number(parts[3]);
  if (!validId(teacherId) || owner !== call.from.id ||
      (action === 'teacher' && (parts.length !== 4 || !Number.isInteger(rate) || rate < 1 || rate > 5)) ||
      (action === 'delete' && parts.length !== 3) || (action === 'show' && parts.length !== 2) ||
      (action === 'remove' && !parts.slice(3).join(':'))) {
    return answer('Откройте свою карточку преподавателя заново.');
  }
  if (action === 'teacher') await setRating(teacherId, call.from.id, rate);
  if (action === 'delete' || action === 'remove') await deleteRating(teacherId, call.from.id,
    action === 'remove' ? parts.slice(3).join(':') : undefined);
  const teacher = await teacherCard(teacherId, call.from.id);
  if (!teacher) return answer('Преподаватель не найден.');
  await answer(action === 'show' ? undefined : 'Голос учтён.');
  return editView(call.message, cardView(teacher, call.from.id), call.inline_message_id);
}
