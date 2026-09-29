# Authentication Microservice

Node.js/Express REST microservice for email/password signup and login with bcrypt, JWT, PostgreSQL, Prisma, Zod, and Helmet.

## Endpoints

- `GET /health` returns `{ "status": "ok" }`.
- `POST /api/auth/signup` creates an account and returns a JWT (`201`); duplicate emails return `409`.
- `POST /api/auth/login` authenticates credentials and returns a JWT (`200`); invalid credentials return `401`.

Emails are trimmed and normalized to lowercase. Passwords must contain at least eight characters, are stored only as bcrypt hashes, and are never returned.

## Setup

Requires Node.js 20+, npm, and PostgreSQL 14+.

```bash
npm install
cp .env.example .env
npm run db:generate
npm run db:migrate
npm run dev
```

Run the mocked Vitest/Supertest suite with `npm test`; no live database is required.

Configuration: `DATABASE_URL` and a `JWT_SECRET` of at least 32 characters are required. `PORT` defaults to `3000`; `JWT_EXPIRES_IN` defaults to `1h`.

## Overview

This service exposes authentication endpoints for creating user accounts and authenticating existing users. Passwords are securely hashed before persistence, and successful logins return a JSON Web Token (JWT).

## Features

- User signup and login endpoints
- Password hashing using `bcryptjs`
- JWT-based authentication responses
- PostgreSQL-backed user persistence
- Environment-based configuration
- JSON REST API

## Technology Stack

- **Runtime:** Node.js 20 or later
- **Framework:** Express
- **Database:** PostgreSQL
- **Password Hashing:** bcryptjs
- **Authentication Token:** JSON Web Token
- **Configuration:** dotenv

## Project Structure

```text
.
├── package.json
├── .env.example
├── README.md
├── tests/auth.test.js
└── src/
    ├── server.js
    ├── app.js
    ├── config/environment.js
    ├── routes/auth.routes.js
    ├── controllers/auth.controller.js
    ├── services/auth.service.js
    ├── repositories/user.repository.js
    ├── middleware/error-handler.js
    └── database/
        ├── client.js
        └── migrations/001_create_users.sql
```

## REST API

`GET /health` returns `{ "status": "ok" }`.

`POST /api/auth/signup` accepts an email and password and returns `201 Created` with `{ "message": "User created successfully" }`.

`POST /api/auth/login` accepts an email and password and returns a `200 OK` response containing a JWT, `Bearer` token type, and configured expiration.

Passwords are never returned in API responses. Invalid input returns `400`, duplicate email signup returns `409`, and invalid login credentials return `401`.

## Installation

Prerequisites: Node.js 20+, npm, and PostgreSQL 14+.

```bash
npm install
cp .env.example .env
```

Apply `src/database/migrations/001_create_users.sql` before using the service. Required environment variables are `DATABASE_URL` and `JWT_SECRET` (at least 16 characters). `PORT` defaults to `3000`; `JWT_EXPIRES_IN` defaults to `1h`.

```bash
npm start
```

For development:

```bash
npm run dev
```

## Testing

Run `npm test`. The generated suite uses Node's built-in test runner and an in-memory repository to test the HTTP contract without requiring PostgreSQL.

## Security

- Store only password hashes, never plaintext passwords.
- Use a strong, randomly generated `JWT_SECRET`.
- Use HTTPS in deployed environments.
- Keep secrets outside source control.

## Original User Story

> Build a user authentication microservice with login and signup REST API endpoints in Node.js.
