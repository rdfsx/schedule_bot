import test from 'node:test';
import assert from 'node:assert/strict';
import { validateExport } from '../scripts/transfer-data.js';

const fixture = () => ({ format: 1, users: [{ id: 4503599627370000, group_id: 42 }],
  teachers: [{ id: 11, full_name: 'Иванов Иван Иванович', count: 1, rating: 5 }],
  teacher_rating: [{ user_id: 4503599627370000, teacher_id: 11, rate: 5, link: 'old-link' }] });

test('preserves Telegram IDs and links, archives unused fields in source', () => {
  const original = fixture();
  const projected = validateExport(original);
  assert.equal(projected.users[0].id, 4503599627370000);
  assert.equal(projected.teacher_rating[0].link, 'old-link');
  assert.equal(original.users[0].group_id, 42);
});

test('stops on duplicates, orphans, invalid ratings and inconsistent counters', () => {
  const duplicate = fixture(); duplicate.users.push(duplicate.users[0]);
  assert.throws(() => validateExport(duplicate), /duplicate/);
  const orphan = fixture(); orphan.users = [];
  assert.throws(() => validateExport(orphan), /Orphan/);
  const mismatch = fixture(); mismatch.teachers[0].rating = 4;
  assert.throws(() => validateExport(mismatch), /counters/);
  const invalid = fixture(); invalid.teacher_rating[0].rate = 0;
  assert.throws(() => validateExport(invalid), /rate/);
  const unsafe = fixture(); unsafe.users[0].id = Number.MAX_SAFE_INTEGER + 1;
  assert.throws(() => validateExport(unsafe), /ID/);
});
