import { login, signup } from '../services/authService.js';
export async function signupController(request, response) { const result = await signup({ email: request.body.email, password: request.body.password }); return response.status(201).json({ message: 'User registered successfully', ...result }); }
export async function loginController(request, response) { const result = await login({ email: request.body.email, password: request.body.password }); return response.status(200).json({ message: 'Login successful', ...result }); }
