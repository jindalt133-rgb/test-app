import { login, signup } from '../services/auth.service.js';

export async function signupController(request, response) {
  const result = await signup(request.body);

  response.status(201).json(result);
}

export async function loginController(request, response) {
  const result = await login(request.body);

  response.status(200).json(result);
}
