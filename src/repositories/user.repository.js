import { pool } from '../db/pool.js';

export async function findUserByEmail(email) {
  const result = await pool.query(
    `
      SELECT id, email, password_hash, created_at, updated_at
      FROM users
      WHERE email = $1
      LIMIT 1
    `,
    [email]
  );

  return result.rows[0] ?? null;
}

export async function createUser({ id, email, passwordHash }) {
  const result = await pool.query(
    `
      INSERT INTO users (id, email, password_hash)
      VALUES ($1, $2, $3)
      RETURNING id, email, created_at, updated_at
    `,
    [id, email, passwordHash]
  );

  return result.rows[0];
}
