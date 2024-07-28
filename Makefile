dopptx:
	python slides.py dopptx .

unpptx:
	python slides.py unpptx .

fmt:
	black .
	isort .

lint:
	black --check .
	isort --check .
