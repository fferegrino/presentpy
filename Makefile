build:
	python utils/dotpptx.py dopptx src/presentpy/slide_templates --delete-original
	poetry build

reset-templates:
	python utils/dotpptx.py unpptx src/presentpy/slide_templates

fmt:
	black .
	isort .
	ruff --fix .

lint:
	black --check .
	isort --check .
	ruff .
