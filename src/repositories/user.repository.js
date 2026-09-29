import { randomUUID } from 'node:crypto';

export class UserRepository {
  #usersByEmail = new Map();
  findByEmail(email) { return this.#usersByEmail.get(email) ?? null; }
  create({ email, passwordHash }) {
    if (this.#usersByEmail.has(email)) { const error = new Error('A user with this email already exists'); error.code = 'USER_ALREADY_EXISTS'; throw error; }
    const user = { id: randomUUID(), email, passwordHash, createdAt: new Date().toISOString() };
    this.#usersByEmail.set(email, user);
    return user;
  }
  clear() { this.#usersByEmail.clear(); }
}
export const userRepository = new UserRepository();
