import test from 'node:test';
import assert from 'node:assert/strict';
import { runtime } from './runtime.js';

test('real SQL and all three handlers', async () => {
  const app = await runtime();
  try { assert.ok((await app.run()).assertions >= 40); }
  finally { app.close(); }
});
