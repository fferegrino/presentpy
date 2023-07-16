build:
	python utils/dotpptx.py dopptx src/presentpy/slide_templates --delete-original
	poetry build

reset-templates:
	python utils/dotpptx.py unpptx src/presentpy/slide_templates

fmt:
	black .
	isort .

lint:
	black --check .
	isort --check .

docs-serve:
	mkdocs serve

release-patch:
	bumpversion patch

release-minor:
	bumpversion minor

release-major:
	bumpversion major
