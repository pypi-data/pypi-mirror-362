# usage: make {command}
# example: make lint
lint:
	@echo "Lint project"
	uv run ruff format . --check
	uv run ruff check --select I .
	uv run ruff check
	uv run mypy . --explicit-package-bases

fix:
	@echo "Fix project"
	uv run ruff format .
	uv run ruff check --select I --fix .
	uv run ruff check . --fix

test:
	@echo "Run tests"
	uv run pytest tests/ -v

build:
	@echo "Build package"
	uv run python -m build

clean:
	@echo "Clean build artifacts"
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/

publish-test:
	@echo "Publish to TestPyPI"
	uv run twine upload --repository testpypi dist/*

publish:
	@echo "Publish to PyPI"
	uv run twine upload dist/*

check-build:
	@echo "Check package"
	uv run twine check dist/*
