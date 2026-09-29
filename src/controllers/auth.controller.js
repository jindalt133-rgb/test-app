import * as authService from '../services/auth.service.js';

export const signup = async (req, res, next) => { try { res.status(201).json(await authService.signup(req.body)); } catch (error) { next(error); } };

export const login = async (req, res, next) => { try { res.status(200).json(await authService.login(req.body)); } catch (error) { next(error); } };
