export const calls = [];
export const options = {};
export function reset() {
  calls.length = 0;
  for (const key of Object.keys(options)) delete options[key];
}
export const api = new Proxy({}, {
  get(_target, method) {
    return async params => {
      calls.push({ method, ...params });
      if (method === 'getUserProfilePhotos') {
        if (options.photoError) throw { code: 400 };
        return { photos: options.photo ? [[{ file_id: 'small' }, { file_id: 'large' }]] : [] };
      }
      if (method === 'sendPhoto' && options.sendPhotoError) throw { code: 400 };
      if ((method === 'sendPhoto' || method === 'sendMessage') && params.chat_id === 343726189 && options.adminError) throw { code: 403 };
      if (method === 'editMessageText' && options.editError) throw options.editError;
      return { message_id: calls.length, chat: { id: params?.chat_id } };
    };
  },
});
