# FastAPI project structure

```
src/
├── api/
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── auth.py      # routers only
│   │   ├── doctors.py
│   │   └── patients.py
│   ├── v2/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── doctors.py
│   │   ├── users.py
│   │   └── patients.py
│   └── __init__.py
├── core/               # business logic (version-agnostic)
│   ├── auth/
│   │   ├── service.py
│   │   ├── models.py
│   │   ├── constants.py
│   │   ├── config.py       # local configs, e.g. env vars
│   │   ├── dependencies.py
│   │   └── exceptions.py # module specific exceptions, e.g. PostNotFound, InvalidUserData
│   ├── doctors/
│   ├── patients/
│   ├── users/
│   └── notifications/
├── schemas/           # pydantic models for request/response validation
│   ├── v1/
│   │   ├── auth.py
│   │   ├── patients.py
│   │   └── doctors.py
│   └── v2/
│       ├── auth.py
│       ├── doctors.py
│       ├── patients.py
│       └── users.py
├── tests/             # tests
├── config.py          # global configuration settings
├── database.py
└── main.py
```

1. Store all domain directories inside src folder
   1. src/ - highest level of an app, contains common models, configs, and constants, etc.
   2. src/main.py - root of the project, which inits the FastAPI app
2. When package requires services or dependencies or constants from other packages - import them with an explicit module name
