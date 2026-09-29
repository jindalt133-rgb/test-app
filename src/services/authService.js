import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { config } from '../config/config.js';
import { createUser, findUserByEmail } from '../repositories/userRepository.js';
export class AppError extends Error { constructor(status, code, message, details) { super(message); this.name = 'AppError'; this.status = status; this.code = code; this.details = details; } }
const normalize = (email) => email.trim().toLowerCase();
const publicUser = (user) => ({ id: String(user.id), email: user.email });
const token = (user) => jwt.sign({ sub: String(user.id), email: user.email }, config.jwtSecret, { expiresIn: config.jwtExpiresIn });
export async function signup({ email, password }) { const normalizedEmail = normalize(email); if (await findUserByEmail(normalizedEmail)) throw new AppError(409, 'EMAIL_ALREADY_REGISTERED', 'An account already exists for this email address'); const passwordHash = await bcrypt.hash(password, config.bcryptSaltRounds); try { const user = await createUser({ email: normalizedEmail, passwordHash }); return { token: token(user), user: publicUser(user) }; } catch (error) { if (error.code === '23505') throw new AppError(409, 'EMAIL_ALREADY_REGISTERED', 'An account already exists for this email address'); throw error; } }
export async function login({ email, password }) { const user = await findUserByEmail(normalize(email)); if (!user || !(await bcrypt.compare(password, user.password_hash))) throw new AppError(401, 'INVALID_CREDENTIALS', 'Invalid email or password'); return { token: token(user), user: publicUser(user) }; }
