FILE_PATH = $(shell pwd)/code_examples/narcissic_number.py

test:
	pytest

reduce: $(FILE_PATH)
	python main.py --file_path $(FILE_PATH)

format:
	black pygolf
	black test
	isort pygolf/**/*.py
	isort test/**/*.py
