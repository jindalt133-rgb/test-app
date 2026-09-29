# User Authentication Microservice

A Node.js 20+ REST microservice providing user signup and login with PostgreSQL persistence, bcrypt password hashing, and JWT authentication.

## API

- `POST /api/auth/signup` creates a user and returns a JWT.
- `POST /api/auth/login` authenticates a user and returns a JWT.
- `GET /health` returns `{ "status": "ok" }`.

Email is trimmed and normalized to lowercase. Passwords require at least eight characters, are hashed before persistence, and are never returned. Duplicate emails return 409; invalid credentials return 401.

## Configuration

Copy `.env.example` to `.env`. `DATABASE_URL` and `JWT_SECRET` are required.

```bash
npm install
npm start
```

Run integration tests with a reachable PostgreSQL database:

```bash
DATABASE_URL="postgresql://username:password@localhost:5432/authentication" npm test
```

The service automatically initializes the `users` table and uses parameterized SQL queries. Tests were statically validated but not executed by the generation step.
