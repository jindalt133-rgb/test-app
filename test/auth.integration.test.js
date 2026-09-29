import test, { before, after } from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';

let app;
let pool;
let server;
let baseUrl;
const emails = new Set();
const runId = `${Date.now()}-${Math.random().toString(16).slice(2)}`;

function emailFor(name) {
  const email = `qa-${runId}-${name}@example.com`;
  emails.add(email);
  return email;
}

function requestJson(method, path, body) {
  return new Promise((resolve, reject) => {
    const payload = body === undefined ? undefined : JSON.stringify(body);
    const request = http.request(`${baseUrl}${path}`, {
      method,
      headers: payload ? {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      } : {}
    }, (response) => {
      let raw = '';
      response.setEncoding('utf8');
      response.on('data', (chunk) => { raw += chunk; });
      response.on('end', () => resolve({
        status: response.statusCode,
        headers: response.headers,
        body: raw ? JSON.parse(raw) : null
      }));
    });
    request.on('error', reject);
    if (payload) request.write(payload);
    request.end();
  });
}

function assertError(response, status, code) {
  assert.equal(response.status, status);
  assert.deepEqual(response.body.error.code, code);
}

before(async () => {
  if (!process.env.DATABASE_URL || !process.env.JWT_SECRET || process.env.JWT_SECRET.length < 32) {
    throw new Error('DATABASE_URL and a 32-character JWT_SECRET are required');
  }
  ({ app } = await import('../src/app.js'));
  ({ pool } = await import('../src/db/pool.js'));
  server = await new Promise((resolve, reject) => {
    const instance = app.listen(0, '127.0.0.1', () => resolve(instance));
    instance.on('error', reject);
  });
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});

after(async () => {
  if (emails.size) await pool.query('DELETE FROM users WHERE email = ANY($1::text[])', [[...emails]]);
  await new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
  await pool.end();
});

test('GET /health returns a liveness response', async () => {
  const response = await requestJson('GET', '/health');
  assert.equal(response.status, 200);
  assert.deepEqual(response.body, { status: 'ok' });
});

test('signup creates a user and login authenticates it', async () => {
  const email = emailFor('auth');
  const password = 'correct-horse-battery';
  const signup = await requestJson('POST', '/api/auth/signup', { email, password });
  assert.equal(signup.status, 201);
  assert.equal(signup.body.user.email, email);
  assert.equal(typeof signup.body.token, 'string');
  const login = await requestJson('POST', '/api/auth/login', { email, password });
  assert.equal(login.status, 200);
  assert.equal(login.body.user.id, signup.body.user.id);
});

test('signup normalizes email and rejects duplicate users', async () => {
  const email = emailFor('normalized');
  const first = await requestJson('POST', '/api/auth/signup', { email: `  ${email.toUpperCase()}  `, password: 'valid-password' });
  assert.equal(first.status, 201);
  assert.equal(first.body.user.email, email);
  const duplicate = await requestJson('POST', '/api/auth/signup', { email, password: 'valid-password' });
  assertError(duplicate, 409, 'EMAIL_ALREADY_REGISTERED');
});

test('validation and generic authentication errors are consistent', async () => {
  assertError(await requestJson('POST', '/api/auth/signup', {}), 400, 'INVALID_REQUEST');
  assertError(await requestJson('POST', '/api/auth/signup', { email: 'invalid', password: 'valid-password' }), 400, 'INVALID_EMAIL');
  assertError(await requestJson('POST', '/api/auth/signup', { email: emailFor('short'), password: 'short' }), 400, 'INVALID_PASSWORD');
  assertError(await requestJson('POST', '/api/auth/login', { email: emailFor('unknown'), password: 'valid-password' }), 401, 'INVALID_CREDENTIALS');
  assertError(await requestJson('GET', '/missing'), 404, 'NOT_FOUND');
});
