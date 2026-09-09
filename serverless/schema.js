import { table, integer, text, primaryKey, index, check, sql } from 'sdk/db';

export const users = table('users', {
  id: integer('id').primaryKey(),
  createdAt: text('created_at'),
  updatedAt: text('updated_at'),
});

export const teachers = table('teachers', {
  id: integer('id').primaryKey(),
  fullName: text('full_name').notNull(),
  createdAt: text('created_at'),
  updatedAt: text('updated_at'),
});

export const ratings = table('teacher_rating', {
  userId: integer('user_id').notNull(),
  teacherId: integer('teacher_id').notNull(),
  rate: integer('rate').notNull(),
  link: text('link'),
  createdAt: text('created_at'),
  updatedAt: text('updated_at'),
}, (t) => ({
  pk: primaryKey({ columns: [t.userId, t.teacherId] }),
  teacherIndex: index('rating_teacher_idx').on(t.teacherId),
  validRate: check('rating_1_to_5', sql`typeof(${t.rate}) = 'integer' AND ${t.rate} BETWEEN 1 AND 5`),
}));
