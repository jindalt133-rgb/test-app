import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { pool } from './pool.js';

const currentDirectory = path.dirname(fileURLToPath(import.meta.url));
const migrationPath = path.resolve(
  currentDirectory,
  '../../migrations/001_create_users.sql'
);

try {
  const migrationSql = await readFile(migrationPath, 'utf8');
  await pool.query(migrationSql);
  console.log('Database migration completed successfully.');
} catch (error) {
  console.error('Database migration failed:', error.message);
  process.exitCode = 1;
} finally {
  await pool.end();
}
