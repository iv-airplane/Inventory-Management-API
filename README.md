# Inventory Management API

An async CRUD (Create, Read, Update, Delete) API for managing inventory items in an e-commerce
website, built with FastAPI, SQLAlchemy (async), and Pydantic.

## Written Spec

Develop an application that allows administrators to manage the product catalog.

The application shall:

* Allow administrator to create an item
* List all items in a catalog
* Retrieve a single item from a catalog
* Mark item as in-stock
* Delete an item from a catalog

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

| Variable       | Default                        | Description                   |
|----------------|--------------------------------|-------------------------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./app.db` | SQLAlchemy async database URL |

Works out of the box with no config needed.

## API

All endpoints are prefixed with `/items`.

| Method | Path                  | Description                               |
|--------|-----------------------|-------------------------------------------|
| POST   | `/items`              | Create an item                            |
| GET    | `/items`              | List all items                            |
| GET    | `/items/{id}`         | Get a single item (404 if missing)        |
| PATCH  | `/items/{id}/restock` | Mark an item as in stock (404 if missing) |
| DELETE | `/items/{id}`         | Delete an item (404 if missing)           |

## Project structure

```
app/
  main.py        # FastAPI app instance, lifespan, router registration
  core/           # config and database engine/session setup
  models/         # SQLAlchemy ORM models
  schemas/        # Pydantic request/response schemas
  crud/           # database access functions
  api/            # route handlers (APIRouters)
tests/            # pytest suite (in-memory async SQLite via dependency overrides)
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
