import { randomUUID } from 'node:crypto';

class UserRepository {
  constructor(databasePool) { this.databasePool = databasePool; }
  async findByEmail(email) { const result = await this.databasePool.query('SELECT id, email, password_hash FROM users WHERE email = $1 LIMIT 1', [email]); return result.rows[0] || null; }
  async create({ email, passwordHash }) { const result = await this.databasePool.query('INSERT INTO users (email, password_hash) VALUES ($1, $2) RETURNING id, email', [email, passwordHash]); return result.rows[0]; }
}
module.exports = { UserRepository };
