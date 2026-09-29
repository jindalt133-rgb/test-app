import { z } from 'zod';
const credentials = z.object({
  email: z.string({ required_error: 'Email is required' }).trim().email('Email must be a valid email address').transform((email) => email.toLowerCase()),
  password: z.string({ required_error: 'Password is required' }).min(8, 'Password must be at least 8 characters long')
}).strict();
export const signupSchema = credentials;
export const loginSchema = credentials;
