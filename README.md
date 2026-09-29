# Authentication Microservice

A Node.js REST microservice that provides user signup and login functionality. The service validates credentials, securely hashes passwords, and returns JSON Web Tokens for authenticated users.

## Features

- `POST /api/auth/signup` creates a user and returns a JWT.
- `POST /api/auth/login` authenticates a user and returns a JWT.
- `GET /health` provides a liveness check.
- Bcrypt password hashing and parameterized PostgreSQL queries.
- Email normalization and validation, password boundary validation, consistent JSON errors, and graceful shutdown.

## Technology Stack

- Node.js 20+, ECMAScript modules, Express, npm
- PostgreSQL 14+
- bcryptjs for password hashing
- jsonwebtoken for access tokens
- dotenv for environment configuration

## Project Structure

```text
.
├── .env.example
├── .gitignore
├── migrations/001_create_users.sql
├── package.json
├── README.md
├── src/
│   ├── app.js
│   ├── server.js
│   ├── config/environment.js
│   ├── controllers/auth.controller.js
│   ├── db/migrate.js
│   ├── db/pool.js
│   ├── middleware/async-handler.js
│   ├── middleware/error-handler.js
│   ├── middleware/not-found.js
│   ├── repositories/user.repository.js
│   ├── routes/auth.routes.js
│   └── services/auth.service.js
└── test/auth.integration.test.js
```

## Installation and Configuration

Prerequisites: Node.js 20+, npm, and PostgreSQL 14+.

```bash
npm install
cp .env.example .env
npm run db:migrate
npm start
```

Required environment variables are `DATABASE_URL` and `JWT_SECRET` (at least 32 characters). Optional variables are `PORT` (default `3000`), `JWT_EXPIRES_IN` (default `1h`), and `BCRYPT_SALT_ROUNDS` (8–15, default `12`). Never commit `.env` or real secrets.

## API

Signup and login accept JSON such as:

```json
{"email":"user@example.com","password":"strong-password"}
```

Successful responses contain a public `{ "user": { "id", "email" }, "token" }` object. Emails are trimmed and lowercased; passwords must be 8–128 characters and are never returned or stored in plaintext. Authentication failures return the generic `INVALID_CREDENTIALS` error. API errors use `{ "error": { "code", "message" } }`.

The migration creates a `users` table with UUID IDs, unique normalized emails, bcrypt password hashes, and timestamps. Run `npm run db:migrate` before using signup or login.

## Testing

The integration suite uses Node's built-in `node:test` framework and requires a configured PostgreSQL database and applied migration:

```bash
npm run db:migrate && npm test
```

The approved test suite covers health checks, signup and login success/failure paths, duplicate emails, email normalization, JWT claims, bcrypt hashing, validation boundaries, malformed JSON, and unknown routes. Runtime tests were statically validated but were not executed in the generation environment.

## Security

JWT secrets are environment-only, SQL queries are parameterized, password hashes are excluded from responses, and unexpected errors do not expose internal details. Production deployments should use HTTPS, rate limiting, and centralized logging.

## Original User Story

> Build a user authentication microservice with login and signup REST API endpoints in Node.js.
