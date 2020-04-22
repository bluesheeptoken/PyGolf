check: test check-lint mypy check-examples

test:
	pytest

check-lint:
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude code_example/
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics  --exclude code_example/,scripts/shorten_code.py
	black . --check --exclude code_example/ --line-length=127
	isort --check

mypy:
	mypy pygolf

check-examples:
	python3 scripts/shorten_code.py --check

lint:
	black . --exclude code_example/ --line-length=127
	isort

generate-examples:
	python scripts/shorten_code.py --generate
