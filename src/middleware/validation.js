export const validate = (schema) => (req, _res, next) => {
  const result = schema.safeParse(req.body);
  if (!result.success) {
    const error = new Error('Request validation failed');
    error.statusCode = 400;
    error.code = 'VALIDATION_ERROR';
    error.details = result.error.issues.map((issue) => ({ field: issue.path.join('.') || 'body', message: issue.message }));
    return next(error);
  }
  req.body = result.data;
  return next();
};
