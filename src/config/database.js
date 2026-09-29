import pg from 'pg';
import { config } from './config.js';
const { Pool } = pg;
export const pool = new Pool({ connectionString: config.databaseUrl, max: 10, idleTimeoutMillis: 30000, connectionTimeoutMillis: 5000, ssl: config.nodeEnv === 'production' ? { rejectUnauthorized: false } : undefined });
export async function initializeDatabase() { await pool.query(`CREATE TABLE IF NOT EXISTS users (id BIGSERIAL PRIMARY KEY, email VARCHAR(320) NOT NULL UNIQUE, password_hash TEXT NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW())`); }
