TESTPYPI=testpypi

# Specifying phony targets
.PHONY: init test build package dist-test dist dist-clean

init: ;

test: init
	python setup.py nosetests

build:
	python setup.py build

package:
	python setup.py sdist
	python setup.py bdist_wheel

dist: package
	twine upload dist/*

dist-test: package
	twine upload --repository ${TESTPYPI} dist/*

dist-clean:
	rm -rf dist/ build/ *.egg-info
