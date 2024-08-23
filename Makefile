dopptx:
	python src/presentpy/writer/slides.py dopptx .

unpptx:
	python src/presentpy/writer/slides.py unpptx .

clean-all:
	rm -rf *.pptx
	rm -rf *.odp
	rm -rf *_odp
	find . -name ".DS_Store" -delete

reset-test:
	presentpy tests/files/test.ipynb --theme default --output test.odp --keep-intermediate --prettify
	cp -r test_odp/ tests/outputs/test_odp
	rm -rf test_odp

docs-serve:
	mkdocs serve

fmt:
	black .
	ruff check --fix .
	python utils/format_xml.py src/presentpy/templates/odp

lint:
	black --check .
	ruff check .
	python utils/format_xml.py src/presentpy/templates/odp --check

patch:
	bump-my-version bump patch

minor:
	bump-my-version bump minor

major:
	bump-my-version bump major
