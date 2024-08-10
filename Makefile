dopptx:
	python src/presentpy/writer/slides.py dopptx .

unpptx:
	python src/presentpy/writer/slides.py unpptx .

clean-all:
	rm -rf *.pptx
	rm -rf *.odp
	rm -rf *_odp

reset-test:
	presentpy tests/files/test.ipynb --theme default --output test.odp --keep-intermediate --prettify
	cp -r test_odp/ tests/outputs/test_odp
	rm -rf test_odp

fmt:
	black .
	isort .

lint:
	black --check .
	isort --check .
