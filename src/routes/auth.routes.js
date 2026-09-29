import { Router } from 'express';
import { loginController, signupController } from '../controllers/auth.controller.js';
import { asyncHandler } from '../middleware/async-handler.js';

const router = Router();

router.post('/signup', asyncHandler(signupController));
router.post('/login', asyncHandler(loginController));

export default router;
