dopptx:
	python src/presentpy/writer/slides.py dopptx .

unpptx:
	python src/presentpy/writer/slides.py unpptx .

clean-all:
	rm -rf *.pptx
	rm -rf *.odp
	rm -rf *_odp

fmt:
	black .
	isort .

lint:
	black --check .
	isort --check .
