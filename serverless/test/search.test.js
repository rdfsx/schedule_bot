import test from 'node:test';
import assert from 'node:assert/strict';
import { searchTeachers, normalize, distance } from '../lib/search.js';

const teachers = ['Иванов Иван Иванович', 'Иванов Пётр Ильич', 'Иванова Анна Сергеевна',
  'Семёнов Пётр Ильич', 'Петров-Сидоров Алексей Иванович', 'Александров Александр Александрович']
  .map((full_name, i) => ({ id: i + 1, full_name }));

test('exact names, namesakes, prefixes and initials', () => {
  assert.deepEqual(searchTeachers(teachers, 'ИВАНОВ').slice(0, 2).map(t => t.id), [1, 2]);
  assert.equal(searchTeachers(teachers, 'Иванов Иван Иванович')[0].id, 1);
  assert.equal(searchTeachers(teachers, 'И. И. Иванов')[0].id, 1);
  assert.equal(searchTeachers(teachers, 'Иванов П.И.')[0].id, 2);
  assert.equal(searchTeachers(teachers, 'Петров-Сидоров А.')[0].id, 5);
  assert.equal(searchTeachers(teachers, 'Семен')[0].id, 4);
  assert.equal(normalize('  СЕМЁНОВ  П.И. '), 'семенов п и');
});

test('layout, transpositions, typos and relevance', () => {
  assert.equal(searchTeachers(teachers, 'bdfyjd')[0].id, 1);
  assert.equal(searchTeachers(teachers, 'Ивнаов')[0].id, 1);
  assert.equal(searchTeachers(teachers, 'Ивнаов')[0].exact, false);
  assert.equal(searchTeachers(teachers, 'Алекснадрво')[0].id, 6);
  assert.equal(distance('ивнаов', 'иванов'), 1);
  assert.equal(searchTeachers(teachers, 'ёёёёёёёё').length, 0);
  assert.equal(searchTeachers(teachers, 'Ивн').length, 0);
  assert.equal(searchTeachers(teachers, 'И. И.').length, 0);
});

test('empty queries, legacy prefix, punctuation and limits', () => {
  assert.equal(searchTeachers(teachers, '').length, teachers.length);
  assert.equal(searchTeachers(teachers, '#p Семенов')[0].id, 4);
  assert.equal(searchTeachers(teachers, '#p ').length, teachers.length);
  assert.equal(searchTeachers(teachers, '%%%').length, 0);
  assert.equal(searchTeachers(teachers, 'я'.repeat(101)).length, 0);
});
