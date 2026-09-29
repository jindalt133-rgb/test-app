import { Router } from 'express';
import { loginController, signupController } from '../controllers/authController.js';
import { validateCredentials } from '../middleware/validation.js';
const authRouter = Router();
authRouter.post('/signup', validateCredentials, signupController);
authRouter.post('/login', validateCredentials, loginController);
export default authRouter;
