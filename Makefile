fmt:
	poetry run ruff format src
	poetry run toml-sort pyproject.toml


check:
	poetry run ruff check src --fix --unsafe-fixes
	poetry run mypy src


lint:
	make fmt
	make check