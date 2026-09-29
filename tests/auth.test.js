const test = require('node:test');
const assert = require('node:assert/strict');
const { AuthService } = require('../src/services/auth.service');

test('signup validates, normalizes email, and hashes password', async () => {
  const users = new Map();
  const service = new AuthService({
    userRepository: { async findByEmail(email) { return users.get(email) || null; }, async create(user) { users.set(user.email, { id: 1, email: user.email, password_hash: user.passwordHash }); } },
    jwtSecret: 'test-secret-with-at-least-16-chars', jwtExpiresIn: '1h'
  });
  assert.deepEqual(await service.signup({ email: ' User@Example.com ', password: 'strong-password' }), { message: 'User created successfully' });
  assert.ok(users.has('user@example.com'));
});

test('invalid credentials are rejected', async () => {
  const service = new AuthService({ userRepository: { findByEmail: async () => null }, jwtSecret: 'test-secret-with-at-least-16-chars', jwtExpiresIn: '1h' });
  await assert.rejects(() => service.login({ email: 'bad', password: 'short' }), { statusCode: 400 });
});
