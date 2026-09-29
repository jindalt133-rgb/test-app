import { login, signup } from '../services/auth.service.js';

export async function signupController(req, res) {
  return res.status(201).json(await signup(req.body));
}

export async function loginController(req, res) {
  return res.status(200).json(await login(req.body));
}
