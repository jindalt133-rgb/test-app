import dotenv from 'dotenv';

dotenv.config();

function parsePort(value) {
  const port = Number.parseInt(value ?? '3000', 10);

  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw new Error('PORT must be an integer between 1 and 65535');
  }

  return port;
}

const jwtSecret = process.env.JWT_SECRET?.trim();

if (!jwtSecret) {
  throw new Error(
    'JWT_SECRET is required. Configure it in the environment before starting the service.'
  );
}

if (jwtSecret.length < 32) {
  throw new Error('JWT_SECRET must contain at least 32 characters');
}

export const config = Object.freeze({
  port: parsePort(process.env.PORT),
  jwtSecret,
  jwtExpiresIn: process.env.JWT_EXPIRES_IN?.trim() || '1h'
});
