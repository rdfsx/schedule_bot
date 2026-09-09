import { api } from 'sdk';
import { adminId } from 'lib/config';
import { addUser } from 'lib/db';
import { escapeHtml } from 'lib/views';

export async function ensureUser(user) {
  if (!user || user.is_bot || !await addUser(user.id) || !adminId) return;
  const name = [user.first_name, user.last_name].filter(Boolean).join(' ') || String(user.id);
  const text = ['#new_user', `Имя: ${escapeHtml(name)}`,
    `ID: <a href="tg://user?id=${user.id}">${user.id}</a>`,
    ...(user.username ? [`Username: @${escapeHtml(user.username)}`] : [])].join('\n');
  try {
    let photo;
    try {
      const result = await api.getUserProfilePhotos({ user_id: user.id, limit: 1 });
      photo = result.photos?.[0]?.at(-1)?.file_id;
    } catch { /* Fall back to text if the photo is unavailable. */ }
    if (photo) {
      try {
        await api.sendPhoto({ chat_id: adminId, photo, caption: text, parse_mode: 'HTML' });
        return;
      } catch { /* Try text if Telegram cannot send this photo. */ }
    }
    await api.sendMessage({ chat_id: adminId, text, parse_mode: 'HTML' });
  } catch (error) {
    console.warn('New-user notification failed', error.code ?? 'network');
  }
}
