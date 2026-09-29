import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { config } from '../config/environment.js';
import { userRepository } from '../repositories/user.repository.js';

const BCRYPT_ROUNDS = 12;
const DUMMY_PASSWORD_HASH = '$2b$12$C6UzMDM.H6dfI/f/IKcEe.1aJ9V7Z7YQ8Jw7b4h5x6z7A8B9C0D1e';

export class ApplicationError extends Error {
  constructor(status, code, message) {
    super(message);
    this.name = 'ApplicationError';
    this.status = status;
    this.code = code;
  }
}

function normalizeEmail(email) {
  return email.trim().toLowerCase();
}

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

export async function signup(input) {
  const { email, password } = validateCredentials(input);
  const existingUser = userRepository.findByEmail(email);

  if (existingUser) {
    throw new ApplicationError(
      409,
      'EMAIL_ALREADY_REGISTERED',
      'An account with this email already exists'
    );
  }

  const passwordHash = await bcrypt.hash(password, BCRYPT_ROUNDS);

  let user;

  try {
    user = userRepository.create({ email, passwordHash });
  } catch (error) {
    if (error.code === '23505') {
      throw new ApplicationError(
        409,
        'EMAIL_ALREADY_REGISTERED',
        'An account with this email already exists'
      );
    }

    throw error;
  }

  return {
    user: toPublicUser(user),
    token: createAccessToken(user)
  };
}

export async function login(input) {
  const { email, password } = validateCredentials(input);
  const user = userRepository.findByEmail(email);

  if (!user) {
    throw new ApplicationError(
      401,
      'INVALID_CREDENTIALS',
      'Invalid email or password'
    );
  }

  const passwordMatches = await bcrypt.compare(password, user.passwordHash);

  if (!passwordMatches) {
    throw new ApplicationError(
      401,
      'INVALID_CREDENTIALS',
      'Invalid email or password'
    );
  }

  return {
    user: toPublicUser(user),
    token: createAccessToken(user)
  };
}
