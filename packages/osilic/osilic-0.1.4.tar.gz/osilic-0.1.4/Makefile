.PHONY: changelog build install clean

changelog:
	git log --pretty=format:'- %h %s (%an, %ad)' --date=short > CHANGELOG.md

build:
	uv build

install:
	pip install -e .

clean:
	rm -rf build dist *.egg-info
