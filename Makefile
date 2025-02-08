fmt:
	ruff format src
	toml-sort pyproject.toml


check:
	ruff check src --fix --unsafe-fixes
	mypy src


lint:
	make fmt
	make check