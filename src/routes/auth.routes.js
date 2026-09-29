import { Router } from 'express';
import { login, signup } from '../controllers/auth.controller.js';
import { validate } from '../middleware/validation.js';
import { loginSchema, signupSchema } from '../validators/auth.validators.js';

const router = Router();
router.post('/signup', validate(signupSchema), signup);
router.post('/login', validate(loginSchema), login);
export default router;
