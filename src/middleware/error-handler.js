export function notFoundHandler(req, res) {
  res.status(404).json({ error: 'Route not found' });
}

export function errorHandler(error, req, res, next) {
  if (res.headersSent) return next(error);
  if (error instanceof SyntaxError && error.status === 400 && 'body' in error) {
    return res.status(400).json({ error: 'Malformed JSON request body' });
  }
  const statusCode = Number.isInteger(error.statusCode) && error.statusCode >= 400 ? error.statusCode : 500;
  if (statusCode >= 500) {
    console.error(error);
    return res.status(500).json({ error: 'Internal server error' });
  }
  return res.status(statusCode).json({ error: error.message });
}
