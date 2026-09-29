import { app } from './app.js';
import { config } from './config/config.js';
import { initializeDatabase, pool } from './config/database.js';
let server;
async function startServer() { await initializeDatabase(); server = app.listen(config.port, () => console.log(`Authentication service listening on port ${config.port}`)); }
async function shutdown(signal) { console.log(`${signal} received; shutting down`); if (server) server.close(async () => { await pool.end(); process.exit(0); }); else { await pool.end(); process.exit(0); } }
process.on('SIGINT', () => void shutdown('SIGINT'));
process.on('SIGTERM', () => void shutdown('SIGTERM'));
startServer().catch(async (error) => { console.error('Unable to start authentication service', error); await pool.end(); process.exit(1); });
