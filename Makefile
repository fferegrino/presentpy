dopptx:
	python src/presentpy/writer/slides.py dopptx .

unpptx:
	python src/presentpy/writer/slides.py unpptx .

fmt:
	black .
	isort .

lint:
	black --check .
	isort --check .
