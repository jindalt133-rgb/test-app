const { Pool } = require('pg');

function createDatabasePool(config) {
  const pool = new Pool({ connectionString: config.databaseUrl, max: 10, idleTimeoutMillis: 30000, connectionTimeoutMillis: 5000 });
  pool.on('error', (error) => console.error('Unexpected PostgreSQL pool error:', error.message));
  return pool;
}

module.exports = { createDatabasePool };
