# An example of structure for FastAPI application


## Project uses:
* Poetry - a tool for dependency management and packaging (pip analogue)
* Ruff - a Python linter
* Mypy - a static type checker for Python
```
make check - check your project
make fmt - format your project
make lint - check & format your project
```


###
## How to run a project
```
git clone ...
cd fastapi-example
```
```
pip install poetry==2.0.1
poetry install
```
```
python src/main.py
```

###
## Migrations
```
aerich migrate [--name custom_name]     - make migrations
aerich upgrade                          - apply migrations
aerich downgrade [-h]                   - downgrade the migration
```

###
## Available paths
```
/api/auth/
/api/registration/

/api/upload/
/api/download/
/api/test/
```
