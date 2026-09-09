import { api } from 'sdk';
import { ensureUser } from 'lib/users';
import { listTeachers, teacherCard } from 'lib/db';
import { searchTeachers, stripPrefix } from 'lib/search';
import { sendHome, cardView, resultsView } from 'lib/views';

const legacyButtons = new Set([
  'пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс',
  'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье',
  'сегодня', 'сейчас', 'завтра', 'ещё', 'еще',
]);

async function clearLegacyKeyboard(chatId) {
  const placeholder = await api.sendMessage({ chat_id: chatId, text: '.', reply_markup: { remove_keyboard: true } });
  await api.deleteMessage({ chat_id: chatId, message_id: placeholder.message_id });
  return sendHome(chatId);
}

export default async function (message) {
  if (!message.from || message.from.is_bot || !message.chat || message.via_bot) return;
  await ensureUser(message.from);
  if (legacyButtons.has(message.text?.trim().toLowerCase())) return clearLegacyKeyboard(message.chat.id);
  const text = stripPrefix(message.text);
  if (!text || text.startsWith('/') || text.length > 100) return sendHome(message.chat.id);
  const results = searchTeachers(await listTeachers(), text);
  if (!results.length) return sendHome(message.chat.id);
  const exact = results.filter(t => t.exact);
  const view = exact.length === 1
    ? cardView(await teacherCard(exact[0].id, message.from.id), message.from.id)
    : resultsView(results);
  await api.sendMessage({ chat_id: message.chat.id, ...view,
    reply_parameters: { message_id: message.message_id } });
}
