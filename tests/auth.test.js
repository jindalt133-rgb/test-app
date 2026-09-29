import { beforeEach, describe, expect, it, vi } from 'vitest';
import request from 'supertest';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
const mocks = vi.hoisted(() => ({ findUserByEmail: vi.fn(), createUser: vi.fn(), disconnect: vi.fn() }));
vi.hoisted(() => { process.env.NODE_ENV = 'test'; process.env.DATABASE_URL = 'postgresql://test:test@localhost:5432/auth_service_test'; process.env.JWT_SECRET = 'test-jwt-secret-that-is-at-least-32-characters-long'; process.env.JWT_EXPIRES_IN = '1h'; });
vi.mock('../src/repositories/user.repository.js', () => ({ prisma: { $disconnect: mocks.disconnect }, findUserByEmail: mocks.findUserByEmail, createUser: mocks.createUser }));
const { default: app } = await import('../src/app.js');
const { env } = await import('../src/config/env.js');
const email = 'user@example.com'; const password = 'correct-password';
beforeEach(() => { vi.clearAllMocks(); mocks.findUserByEmail.mockResolvedValue(null); mocks.createUser.mockImplementation(async ({ email, passwordHash }) => ({ id: 'user-123', email, passwordHash })); });
describe('authentication service', () => {
  it('reports health and security headers', async () => { const response = await request(app).get('/health'); expect(response.status).toBe(200); expect(response.body).toEqual({ status: 'ok' }); expect(response.headers['x-content-type-options']).toBe('nosniff'); });
  it('signs up with normalized email, hash, and JWT', async () => { const response = await request(app).post('/api/auth/signup').send({ email: ' USER@EXAMPLE.COM ', password }); expect(response.status).toBe(201); expect(response.body.user).toEqual({ id: 'user-123', email }); expect(jwt.verify(response.body.token, env.JWT_SECRET)).toMatchObject({ sub: 'user-123', email }); const args = mocks.createUser.mock.calls[0][0]; expect(await bcrypt.compare(password, args.passwordHash)).toBe(true); });
  it('rejects duplicate signup and bad login', async () => { mocks.findUserByEmail.mockResolvedValue({ id: 'user-123', email, passwordHash: await bcrypt.hash(password, 4) }); const duplicate = await request(app).post('/api/auth/signup').send({ email, password }); expect(duplicate.status).toBe(409); const login = await request(app).post('/api/auth/login').send({ email, password: 'incorrect-password' }); expect(login.status).toBe(401); });
  it('authenticates valid login and rejects invalid input', async () => { mocks.findUserByEmail.mockResolvedValue({ id: 'user-123', email, passwordHash: await bcrypt.hash(password, 4) }); const login = await request(app).post('/api/auth/login').send({ email, password }); expect(login.status).toBe(200); const invalid = await request(app).post('/api/auth/signup').send({ email, password: 'short', role: 'admin' }); expect(invalid.status).toBe(400); });
});
