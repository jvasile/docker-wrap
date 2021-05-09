SOURCE:=$(shell find src -name '*.py')
BUILD:=${subst src,build/lib,$(SOURCE)}

all: build

build: ${BUILD}

build/lib/%: src/% setup.py
	python3 -m build
	touch ${BUILD}

upload: ${BUILD}
	twine upload --skip-existing dist/*

clean:
	rm -rf build

.PHONY: build clean
