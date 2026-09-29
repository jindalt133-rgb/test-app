import app from './app.js';
import { config } from './config/environment.js';

const server = app.listen(config.port, () => {
  console.log(`Authentication Microservice listening on port ${config.port}`);
});

function shutdown(signal) {
  console.log(`${signal} received. Shutting down gracefully.`);

  server.close((serverError) => {
    if (serverError) {
      console.error('HTTP server shutdown failed:', serverError.message);
      process.exitCode = 1;
    }

    process.exit(0);
  });
}

process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));
