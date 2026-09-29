export function errorHandler(error, request, response, next) {
  if (response.headersSent) {
    return next(error);
  }

  if (error instanceof SyntaxError && error.status === 400 && 'body' in error) {
    return response.status(400).json({
      error: {
        code: 'INVALID_JSON',
        message: 'Request body contains invalid JSON'
      }
    });
  }

  const status = Number.isInteger(error.status) ? error.status : 500;
  const code = error.code || 'INTERNAL_SERVER_ERROR';
  const message =
    status >= 500
      ? 'An unexpected server error occurred'
      : error.message;

  if (status >= 500) {
    console.error(error);
  }

  return response.status(status).json({
    error: {
      code,
      message
    }
  });
}
