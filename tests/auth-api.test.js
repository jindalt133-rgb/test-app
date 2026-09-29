import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { after, before, beforeEach, describe, test } from 'node:test';
import jwt from 'jsonwebtoken';

process.env.JWT_SECRET = 'test-secret-that-is-at-least-32-characters-long';
process.env.JWT_EXPIRES_IN = '1h';

const { default: app } = await import('../src/app.js');
const { userRepository } = await import('../src/repositories/user.repository.js');
let server;
let baseUrl;

before(async () => {
  server = createServer(app);
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
  const address = server.address();
  if (!address || typeof address === 'string') throw new Error('Unable to determine test server address');
  baseUrl = `http://127.0.0.1:${address.port}`;
});

after(() => new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve())));
beforeEach(() => userRepository.clear());

async function request(path, options = {}) {
  const response = await fetch(`${baseUrl}${path}`, { ...options, headers: { 'content-type': 'application/json', ...(options.headers ?? {}) } });
  const text = await response.text();
  return { response, body: text ? JSON.parse(text) : null, text };
}
const signup = (email = 'user@example.com', password = 'secure-password') => request('/api/auth/signup', { method: 'POST', body: JSON.stringify({ email, password }) });
const login = (email = 'user@example.com', password = 'secure-password') => request('/api/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) });

describe('authentication API', () => {
  test('registers a user', async () => { const { response, body } = await signup(); assert.equal(response.status, 201); assert.deepEqual(body, { message: 'User registered successfully' }); });
  test('normalizes email and logs in', async () => { await signup('  User@Example.COM  '); const { response, body } = await login('USER@example.com'); assert.equal(response.status, 200); assert.equal(body.tokenType, 'Bearer'); assert.equal(body.expiresIn, '1h'); });
  test('rejects duplicate email', async () => { await signup(); const { response, body } = await signup(); assert.equal(response.status, 409); assert.deepEqual(body, { error: 'Email address is already registered' }); });
  test('validates missing and malformed credentials', async () => { for (const payload of [{ password: 'secure-password' }, { email: 'user@example.com' }, { email: 'bad', password: 'secure-password' }, { email: 'user@example.com', password: 'short' }]) { const { response } = await request('/api/auth/signup', { method: 'POST', body: JSON.stringify(payload) }); assert.equal(response.status, 400); } });
  test('returns and verifies a JWT', async () => { await signup(); const { body } = await login(); const decoded = jwt.verify(body.accessToken, process.env.JWT_SECRET); assert.equal(decoded.email, 'user@example.com'); assert.equal(typeof decoded.sub, 'string'); });
  test('uses generic invalid credentials errors', async () => { await signup(); const wrong = await login('user@example.com', 'wrong-password'); const unknown = await login('unknown@example.com'); assert.equal(wrong.response.status, 401); assert.deepEqual(wrong.body, unknown.body); });
  test('handles malformed JSON and unknown routes', async () => { const malformed = await request('/api/auth/signup', { method: 'POST', body: '{"email":' }); assert.equal(malformed.response.status, 400); const missing = await request('/api/auth/unknown', { method: 'GET' }); assert.equal(missing.response.status, 404); });
});
