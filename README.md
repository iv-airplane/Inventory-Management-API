# Inventory Management API

An async CRUD (Create, Read, Update, Delete) API for managing inventory items in an e-commerce
website, built with FastAPI, SQLAlchemy (async), SQLite, and Pydantic. Users register and log in
with JWT bearer tokens, and role-based access control (RBAC) limits catalog changes to admins.

## Written Spec

Develop an application that allows administrators to manage the product catalog and users to view the catalog.

The application shall:

* Allow administrator to create an item
* List all items in a catalog
* Retrieve a single item from a catalog
* Mark item as in-stock
* Delete an item from a catalog
* Users to view an item

Please see the table for allowed actions per user below

| Action                        | Required role      |
|-------------------------------|--------------------|
| GET /items                    | any logged-in user |
| GET /items/{id}               | any logged-in user |
| POST /items (create an item)  | admin              |
| PATCH /items/{id}/restock     | admin              |
| DELETE /items/{id}            | admin              |

## Requirements

- Python >= 3.14
- Package manager: [uv](https://docs.astral.sh/uv/) (recommended) or `pip`

## Setup

Install uv: https://docs.astral.sh/uv/getting-started/installation/#standalone-installer

```bash
uv sync
```

Or with pip:

```bash
pip install -r requirements.txt
```

## Running the app

```bash
uv run uvicorn app.main:app --reload
```

Interactive API docs are available at `http://127.0.0.1:8000/docs`.

## Configuration

| Variable                      | Default                             | Description                          |
|-------------------------------|-------------------------------------|--------------------------------------|
| `DATABASE_URL`                | `sqlite+aiosqlite:///./app.db`      | SQLAlchemy async database URL        |
| `SECRET_KEY`                  | `dev-secret-key-change-in-production` | Key used to sign JWTs              |
| `ALGORITHM`                   | `HS256`                             | JWT signing algorithm                |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30`                                | How long a login token stays valid   |

Works out of the box with no config needed. Set a real `SECRET_KEY` before any non-local use.

## Authentication

1. `POST /auth/register` with an email and password to create a user.
2. `POST /auth/login` (form fields `username` = your email, and `password`) to receive a JWT.
3. Send it on later requests as `Authorization: Bearer <token>`.

In the Swagger docs at `/docs`, click **Authorize** and enter your email and password; Swagger
handles the token for you. Passwords are hashed with bcrypt. Missing or invalid tokens return
401, and a valid user without the required role gets 403.

> Note: `role` is currently accepted at registration so admins can be created for testing. This
> lets anyone self-register as an admin, so replace it with a seeded admin or an admin-only
> promotion endpoint before real use.

## API

| Method | Path                  | Required role | Description                               |
|--------|-----------------------|---------------|-------------------------------------------|
| POST   | `/auth/register`      | none          | Register a user (409 if email exists)     |
| POST   | `/auth/login`         | none          | Log in and receive a JWT (401 if invalid) |
| POST   | `/items`              | admin         | Create an item                            |
| GET    | `/items`              | any user      | List all items                            |
| GET    | `/items/{id}`         | any user      | Get a single item (404 if missing)        |
| PATCH  | `/items/{id}/restock` | admin         | Mark an item as in stock (404 if missing) |
| DELETE | `/items/{id}`         | admin         | Delete an item (404 if missing)           |

## Project structure

```
app/
  main.py        # FastAPI app instance, lifespan, router registration
  core/           # config, database engine/session setup, JWT and role checks (security.py)
  models/         # SQLAlchemy ORM models (Item, User, Role)
  schemas/        # Pydantic request/response schemas
  crud/           # database access functions
  api/            # route handlers (APIRouters)
tests/            # pytest suite for items, auth, and role permissions (in-memory async SQLite via dependency overrides)
```

## Testing

```bash
uv run pytest
```

Tests use an in-memory SQLite database per test, injected via FastAPI's `dependency_overrides` (see
`tests/conftest.py`).

Advantages of this testing approach:

- **Fast** — no disk I/O, no cleanup.
- **Isolated** — every test starts with a clean slate, no leftover data.
