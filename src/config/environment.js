import 'dotenv/config';

function parsePort(value) {
  const port = Number(value || 3000);

  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw new Error('PORT must be an integer between 1 and 65535');
  }

  return port;
}

function parseSaltRounds(value) {
  const rounds = Number(value || 12);

  if (!Number.isInteger(rounds) || rounds < 8 || rounds > 15) {
    throw new Error('BCRYPT_SALT_ROUNDS must be an integer between 8 and 15');
  }

  return rounds;
}

const databaseUrl = process.env.DATABASE_URL;
const jwtSecret = process.env.JWT_SECRET;

if (!databaseUrl) {
  throw new Error('DATABASE_URL is required');
}

if (!jwtSecret || jwtSecret.length < 32) {
  throw new Error('JWT_SECRET is required and must be at least 32 characters long');
}

export const config = Object.freeze({
  port: parsePort(process.env.PORT),
  databaseUrl,
  jwtSecret,
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || '1h',
  bcryptSaltRounds: parseSaltRounds(process.env.BCRYPT_SALT_ROUNDS)
});
