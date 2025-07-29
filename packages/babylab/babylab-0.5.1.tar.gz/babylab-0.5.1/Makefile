test:
	uv run pytest -v -p no:cacheprovider --exitfirst --benchmark-time-unit="s" --benchmark-autosave

cov:
	uv run pytest --cov=babylab

lint:
	uv run pylint $(git ls-files '*.py')
