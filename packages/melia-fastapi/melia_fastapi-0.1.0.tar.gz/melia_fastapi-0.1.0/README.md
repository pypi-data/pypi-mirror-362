# Melia

### Tree

fastapi-starter/
  ├── app/
  │   ├── __init__.py
  │   ├── main.py                     # FastAPI app instance
  │   ├── core/
  │   │   ├── __init__.py
  │   │   ├── config.py              # Settings & config
  │   │   ├── database.py            # Database setup
  │   │   └── security.py            # Auth & security
  │   ├── api/
  │   │   ├── __init__.py
  │   │   ├── deps.py                # Dependencies
  │   │   └── endpoints/
  │   │       ├── __init__.py
  │   │       ├── auth.py            # Auth endpoints
  │   │       └── users.py           # User endpoints
  │   ├── models/
  │   │   ├── __init__.py
  │   │   └── user.py                # Database models
  │   └── schemas/
  │       ├── __init__.py
  │       └── user.py                # Pydantic schemas
  ├── tests/
  │   ├── __init__.py
  │   └── test_main.py
  ├── .env.example
  ├── .gitignore
  ├── Dockerfile
  ├── pyproject.toml
  ├── docker-compose.yml
  ├── melia.yml                      # Melia configuration
  └── README.md
