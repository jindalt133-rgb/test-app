import { app } from './app.js';
import { config } from './config/environment.js';
import { pool } from './db/pool.js';

const server = app.listen(config.port, () => {
  console.log(`Authentication service listening on port ${config.port}`);
});

function shutdown(signal) {
  console.log(`${signal} received. Shutting down gracefully.`);

  server.close(async (serverError) => {
    if (serverError) {
      console.error('HTTP server shutdown failed:', serverError.message);
      process.exitCode = 1;
    }

    try {
      await pool.end();
    } catch (databaseError) {
      console.error('Database pool shutdown failed:', databaseError.message);
      process.exitCode = 1;
    }
  });
}

process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));
