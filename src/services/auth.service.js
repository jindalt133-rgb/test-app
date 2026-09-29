import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { env } from '../config/env.js';
import { createUser, findUserByEmail } from '../repositories/user.repository.js';

const PASSWORD_HASH_ROUNDS = 12;

const createServiceError = (message, statusCode, code) => { const error = new Error(message); error.statusCode = statusCode; error.code = code; return error; };

const toPublicUser = (user) => ({ id: user.id, email: user.email });
const createToken = (user) => jwt.sign({ sub: user.id, email: user.email }, env.JWT_SECRET, { expiresIn: env.JWT_EXPIRES_IN });

function validateCredentials(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) {
    throw new ApplicationError(
      400,
      'INVALID_REQUEST',
      'Request body must be a JSON object'
    );
  }

  const { email, password } = input;

  if (typeof email !== 'string' || typeof password !== 'string') {
    throw new ApplicationError(
      400,
      'INVALID_REQUEST',
      'Email and password are required'
    );
  }

  const normalizedEmail = normalizeEmail(email);

  if (
    normalizedEmail.length === 0 ||
    normalizedEmail.length > 320 ||
    !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalizedEmail)
  ) {
    throw new ApplicationError(
      400,
      'INVALID_EMAIL',
      'A valid email address is required'
    );
  }

  if (password.length < 8 || password.length > 128) {
    throw new ApplicationError(
      400,
      'INVALID_PASSWORD',
      'Password must be between 8 and 128 characters'
    );
  }

  return {
    email: normalizedEmail,
    password
  };
}

function toPublicUser(user) {
  return {
    id: user.id,
    email: user.email
  };
}

function createAccessToken(user) {
  return jwt.sign(
    {
      sub: user.id,
      email: user.email
    },
    config.jwtSecret,
    {
      expiresIn: config.jwtExpiresIn
    }
  );
}

export const signup = async ({ email, password }) => {
  const existingUser = await findUserByEmail(email);

  if (existingUser) throw createServiceError('An account already exists for this email address', 409, 'EMAIL_ALREADY_REGISTERED');

  const passwordHash = await bcrypt.hash(password, PASSWORD_HASH_ROUNDS);

  let user;

  try {
    user = await createUser({ email, passwordHash });
  } catch (error) {
    if (error.code === '23505') {
      throw createServiceError('An account already exists for this email address', 409, 'EMAIL_ALREADY_REGISTERED');
    }

    throw error;
  }

  return { user: toPublicUser(user), token: createToken(user) };
};

export const login = async ({ email, password }) => {
  const user = await findUserByEmail(email);
  const passwordMatches = user && await bcrypt.compare(password, user.passwordHash);

  if (!passwordMatches) {
    throw createServiceError('Invalid email or password', 401, 'INVALID_CREDENTIALS');
  }

  return { user: toPublicUser(user), token: createToken(user) };
};
