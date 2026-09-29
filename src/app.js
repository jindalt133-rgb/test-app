import express from 'express';
import authRoutes from './routes/auth.routes.js';
import { errorHandler, notFoundHandler } from './middleware/error-handler.js';

const app = express();
app.disable('x-powered-by');
app.use(express.json({ limit: '10kb' }));
app.use('/api/auth', authRoutes);
app.use(notFoundHandler);
app.use(errorHandler);
export default app;
