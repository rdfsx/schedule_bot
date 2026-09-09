import { api } from 'sdk';

export const homeText = 'Расписание занятий теперь смотрите на https://sc.gstu.by\n\n'
  + 'Преподаватели — по кнопке ниже, либо отправьте фамилию в чат.';
export const searchButton = { text: 'Преподаватели', switch_inline_query_current_chat: '' };
export const homeKeyboard = { inline_keyboard: [[searchButton]] };
export const escapeHtml = text => String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

export async function sendHome(chatId) {
  return api.sendMessage({ chat_id: chatId, text: homeText,
    link_preview_options: { is_disabled: true }, reply_markup: homeKeyboard });
}

export function summary(teacher) {
  return teacher.count ? `${Number(teacher.average).toFixed(1)}/5 · голосов: ${teacher.count}` : 'Пока нет голосов. Вы можете быть первым!';
}

export function cardView(teacher, userId) {
  const text = [`<b>${escapeHtml(teacher.full_name)}</b>`,
    ...(teacher.own_rate == null ? [] : [`Вы поставили ${teacher.own_rate}`]), summary(teacher)].join('\n\n');
  let deletion = `remove:${userId}:${teacher.id}:${teacher.own_created_at ?? ''}`;
  if (deletion.length > 64 || !teacher.own_created_at) deletion = `delete:${userId}:${teacher.id}`;
  const votes = teacher.own_rate == null
    ? [1, 2, 3, 4, 5].map(rate => ({ text: String(rate), callback_data: `teacher:${userId}:${teacher.id}:${rate}` }))
    : [{ text: 'Удалить/изменить голос', callback_data: deletion }];
  return { text, parse_mode: 'HTML', reply_markup: { inline_keyboard: [votes, [searchButton]] } };
}

export function resultsView(results, page = 0) {
  const lastPage = Math.max(0, Math.ceil(results.length / 10) - 1);
  page = Math.min(Math.max(0, page), lastPage);
  const rows = results.slice(page * 10, page * 10 + 10).map(t => [{ text: t.full_name, callback_data: `show:${t.id}` }]);
  const navigation = [];
  if (page > 0) navigation.push({ text: '←', callback_data: `page:${page - 1}` });
  if (page < lastPage) navigation.push({ text: '→', callback_data: `page:${page + 1}` });
  if (navigation.length) rows.push(navigation);
  rows.push([searchButton]);
  return { text: results.length ? `Выберите преподавателя (${page + 1}/${lastPage + 1}):` : 'Преподаватель не найден. Попробуйте другую фамилию.',
    reply_markup: { inline_keyboard: rows } };
}

export async function editView(message, view, inlineMessageId) {
  try {
    const target = inlineMessageId
      ? { inline_message_id: inlineMessageId }
      : { chat_id: message.chat.id, message_id: message.message_id };
    await api.editMessageText({ ...target, ...view });
  } catch (error) {
    if (error.code === 400 && /message is not modified/i.test(error.description ?? '')) return;
    throw error;
  }
}
