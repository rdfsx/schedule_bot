import { db } from 'sdk';
import message from 'lib/message-handler';
import inline from 'handlers/inline_query';
import callback from 'handlers/callback_query';
import { addUser, setRating, deleteRating, teacherCard } from 'lib/db';
import { ensureUser } from 'lib/users';
import { calls, options, reset } from 'lib/test-api';
import importer from 'lib/import-handler';

export default async function () {
  let assertions = 0;
  function check(ok, label) {
    assertions++;
    if (!ok) throw new Error(label);
  }
  async function rejects(fn, label) {
    let rejected = false;
    try { await fn(); } catch { rejected = true; }
    check(rejected, label);
  }
  const user = id => ({ id, first_name: 'Иван <тест>', username: 'tester' });
  const msg = (text, id = 1) => ({ from: user(id), chat: { id, type: 'private' }, message_id: 10, text });
  const call = (data, id = 1) => ({ id: `call-${assertions}`, from: user(id), data,
    message: { chat: { id, type: 'private' }, message_id: 11, date: 1 } });

  await db.run("INSERT INTO teachers (id, full_name) VALUES (1, 'Иванов Иван Иванович'), (2, 'Семёнов Пётр Ильич')");
  check((await db.all('PRAGMA index_list(teacher_rating)')).some(i => i.name.endsWith('rating_teacher_idx')), 'Teacher rating index exists');
  await addUser(1);
  reset();
  await message(msg('/start'));
  check(calls.filter(c => c.method === 'sendMessage').length === 1, 'Imported user must not notify admin');
  check(calls[0].text.includes('sc.gstu.by'), 'Start shows schedule link');
  check(calls[0].reply_markup.inline_keyboard[0][0].text === 'Преподаватели', 'Button is attached in the initial send');
  check(calls.at(-1).reply_markup.inline_keyboard[0][0].switch_inline_query_current_chat === '', 'No #p');

  reset();
  await message({ ...msg('Иванов'), via_bot: { id: 986323431, is_bot: true } });
  check(calls.length === 0, 'Chosen inline result does not trigger a second response');

  reset();
  await message(msg('ПТ'));
  check(calls.length === 3 && calls[0].text === '.' && calls[0].reply_markup.remove_keyboard === true,
    'Legacy schedule button removes reply keyboard');
  check(calls[1].method === 'deleteMessage' && calls[1].message_id === 1,
    'Keyboard-removal placeholder is deleted');
  check(calls[2].text.includes('sc.gstu.by'), 'Home follows legacy keyboard cleanup');

  reset(); options.photo = true;
  await Promise.all([ensureUser(user(2)), ensureUser(user(2))]);
  check(calls.filter(c => c.method === 'sendPhoto').length === 1, 'Concurrent registration notifies once');
  check(calls.find(c => c.method === 'sendPhoto').caption.includes('&lt;тест&gt;'), 'Escape profile HTML');
  reset();
  await message(msg('/start', 2));
  check(!calls.some(c => c.chat_id === 343726189), 'Repeated start does not notify');
  reset(); options.photoError = true;
  await ensureUser({ id: 3, first_name: 'Без username' });
  check(calls.some(c => c.method === 'sendMessage' && c.text.includes('tg://user?id=3')), 'Missing photo falls back to text');
  check(!calls.at(-1).text.includes('undefined'), 'Missing username omitted');
  reset(); options.photo = true; options.sendPhotoError = true;
  await ensureUser(user(4));
  check(calls.some(c => c.method === 'sendMessage'), 'Failed photo falls back to text');
  reset(); options.adminError = true;
  await message(msg('/start', 5));
  check(calls.some(c => c.chat_id === 5 && c.method === 'sendMessage'), 'Admin failure does not block bot');

  reset();
  await Promise.all([setRating(1, 1, 5), setRating(1, 1, 5), setRating(1, 2, 3)]);
  let card = await teacherCard(1, 1);
  check(card.count === 2 && card.average === 4 && card.own_rate === 5, 'Concurrent votes and duplicate delivery');
  await setRating(9999, 1, 5);
  await setRating(1, 9999, 5);
  await setRating(1, 3, 6);
  check((await teacherCard(1, 1)).count === 2, 'Invalid vote and missing parents rejected');
  await rejects(() => db.run('INSERT INTO teacher_rating (user_id, teacher_id, rate) VALUES (3, 1, 6)'), 'Rate CHECK');
  await rejects(() => db.run('INSERT INTO teacher_rating (user_id, teacher_id, rate) VALUES (3, 1, 2.5)'), 'Integer CHECK');
  await rejects(() => db.run('INSERT INTO teacher_rating (user_id, teacher_id, rate) VALUES (1, 1, 4)'), 'Composite primary key');

  await callback(call('teacher:1:1:1'));
  check((await teacherCard(1, 1)).own_rate === 5, 'Legacy vote button does not overwrite');
  await callback(call('delete:1:1', 2));
  check((await teacherCard(1, 1)).own_rate === 5, 'Cannot delete someone else’s vote');
  await callback(call('delete:1:1'));
  check((await teacherCard(1, 1)).own_rate === null, 'Legacy deletion works');
  await callback(call('teacher:1:1:2'));
  card = await teacherCard(1, 1);
  check(card.count === 2 && card.average === 2.5, 'Rate after removal');
  await deleteRating(1, 1, '2000-01-01T00:00:00.000Z');
  check((await teacherCard(1, 1)).own_rate === 2, 'Stale deletion does not remove current vote');
  const deletion = calls.filter(c => c.method === 'editMessageText').at(-1).reply_markup.inline_keyboard[0][0].callback_data;
  await callback(call(deletion));
  await callback(call(deletion));
  check((await teacherCard(1, 1)).count === 1, 'New removal and repeated removal');
  reset();
  await callback(call('teacher:1:1:9'));
  check(calls.at(-1).method === 'answerCallbackQuery', 'Invalid callback is answered');
  await callback(call('show:9999'));
  check(calls.at(-1).text.includes('не найден'), 'Unknown teacher callback');
  await callback({ ...call('show:1'), message: undefined, inline_message_id: 'inline' });
  check(calls.at(-1).method === 'editMessageText' && calls.at(-1).inline_message_id === 'inline', 'Inline card is editable');
  await callback({ ...call('show:1'), message: undefined });
  check(calls.at(-1).text.includes('заново'), 'Inaccessible callback handled');
  await callback(call('schedule:1:this_week'));
  check(calls.at(-1).text.includes('sc.gstu.by'), 'Old schedule button shows home');

  reset();
  await message(msg('Иванов'));
  check(calls.at(-1).text.includes('<b>Иванов') && !calls.at(-1).text.includes('sc.gstu.by'), 'Surname opens card');
  await message(msg('Ивнаов'));
  check(calls.at(-1).reply_markup.inline_keyboard[0][0].callback_data === 'show:1', 'Typo asks for selection');
  await message(msg(undefined));
  check(calls.at(-1).text.includes('sc.gstu.by'), 'Media fallback');
  await message(msg('привет'));
  check(calls.at(-1).text.includes('sc.gstu.by'), 'Unrelated message fallback');
  reset();
  await inline({ id: 'q', from: user(6), query: '#p Семенов', offset: '' });
  check(calls.some(c => c.chat_id === 343726189), 'First inline query notifies');
  check(calls.at(-1).results[0].id === '2', 'Legacy #p and ё normalization');
  check(calls.at(-1).results[0].input_message_content.message_text.includes('<b>Семёнов') &&
    calls.at(-1).results[0].reply_markup.inline_keyboard[0].length === 5, 'Inline result sends the complete card');
  reset();
  await callback({ ...call('teacher:6:2:5', 6), message: undefined, inline_message_id: 'chosen-inline' });
  check(calls.at(-1).method === 'editMessageText' && calls.at(-1).inline_message_id === 'chosen-inline',
    'Voting edits the chosen inline result');
  reset();
  await inline({ id: 'q', from: user(6), query: 'ЫЫЫЫЫ', offset: '' });
  check(calls.at(-1).results[0].id === 'not-found', 'Inline no results');
  await callback(call('show:1', 7));
  check(calls.some(c => c.chat_id === 343726189 && c.text?.includes('id=7')), 'First callback notifies');

  for (let i = 10; i < 35; i++) await db.run('INSERT INTO teachers (id, full_name) VALUES (:id, :name)', {
    ':id': i, ':name': `Иванов Тестовый ${String.fromCharCode(1040 + i)}`,
  });
  reset();
  await inline({ id: 'q', from: user(1), query: '', offset: '' });
  check(calls.at(-1).results.length === 20 && calls.at(-1).next_offset === '20', 'Inline first page');
  const first = calls.at(-1).results.map(r => r.id);
  await inline({ id: 'q', from: user(1), query: '', offset: '20' });
  check(calls.at(-1).results.length === 7 && calls.at(-1).results.every(r => !first.includes(r.id)), 'Inline next page no duplicates');
  await message(msg('Иванов'));
  check(calls.at(-1).reply_markup.inline_keyboard.length === 12, 'Namesakes require paginated choice');
  const pagination = call('page:1');
  pagination.message.reply_to_message = { text: 'Иванов' };
  await callback(pagination);
  check(calls.at(-1).text.includes('(2/3)'), 'Message pagination');
  reset(); options.editError = { code: 400, description: 'Bad Request: message is not modified' };
  await callback(call('show:1'));
  check(true, 'Unchanged edit is harmless');
  reset();

  const importedUser = { id: 100, created_at: '2021-09-04T12:12:42.123456+00:00', updated_at: null };
  await importer({ action: 'import', table: 'users', rows: [importedUser] });
  await importer({ action: 'import', table: 'users', rows: [importedUser] });
  check((await db.get('SELECT COUNT(*) AS n FROM users WHERE id = 100')).n === 1, 'Repeated import no duplicates');
  check((await db.get('SELECT created_at FROM users WHERE id = 100')).created_at === importedUser.created_at, 'Preserve microseconds');
  await rejects(() => importer({ action: 'import', table: 'users', rows: [{ ...importedUser, updated_at: '2026-01-01' }] }), 'Conflict does not overwrite');
  await rejects(() => importer({ action: 'import', table: 'teacher_rating', rows: [{ user_id: 100, teacher_id: 9999, rate: 1 }] }), 'Import rejects orphan');
  await rejects(() => importer({ action: 'import', table: 'users', rows: [] }, { update: {} }), 'No import through Telegram updates');
  await ensureUser(user(100));
  check(!calls.length, 'Imported users do not notify');

  const nextUser = { id: 101, created_at: null, updated_at: null };
  await rejects(() => importer({ action: 'import', table: 'users', rows: [nextUser,
    { ...importedUser, updated_at: '2026-01-01' }] }), 'Interrupted batch reports conflict');
  await importer({ action: 'import', table: 'users', rows: [nextUser, importedUser] });
  check((await db.get('SELECT COUNT(*) AS n FROM users WHERE id IN (100, 101)')).n === 2, 'Resume partially completed batch');
  const importedTeacher = { id: 200, full_name: 'Новый Преподаватель Тестовый', created_at: importedUser.created_at, updated_at: null };
  await importer({ action: 'import', table: 'teachers', rows: [importedTeacher] });
  const importedVotes = [
    { user_id: 100, teacher_id: 200, rate: 5, link: 'old-link', created_at: importedUser.created_at, updated_at: null },
    { user_id: 101, teacher_id: 200, rate: 3, link: null, created_at: null, updated_at: null },
  ];
  await importer({ action: 'import', table: 'teacher_rating', rows: importedVotes });
  await importer({ action: 'import', table: 'teacher_rating', rows: importedVotes });
  const exportedVotes = await importer({ action: 'read', table: 'teacher_rating', offset: 0 });
  for (const vote of importedVotes) {
    const exported = exportedVotes.find(r => r.user_id === vote.user_id && r.teacher_id === vote.teacher_id);
    check(exported && Object.keys(vote).every(key => exported[key] === vote[key]), 'Every imported vote field round-trips');
  }
  const importedCard = await teacherCard(200, 100);
  check(importedCard.count === 2 && importedCard.average === 4, 'Imported aggregates match votes');
  return { assertions };
}
