test:
	pytest

format:
	black pygolf
	black test
	isort pygolf/**/*.py
	isort test/**/*.py
