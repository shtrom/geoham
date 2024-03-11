PYTHON=python3
VENV=.venv/geoham
VENV_PYTHON=${VENV}/bin/${PYTHON}
VENV_PIP=${VENV}/bin/pip
VENV_JUPYTER=${VENV}/bin/jupyter-notebook
VENV_PYTEST=${VENV}/bin/pytest

all: dist

run: ${VENV_JUPYTER}
	${VENV_JUPYTER}

test: ${VENV_PYTEST}
	${VENV_PYTEST} --doctest-modules

dist: ${VENV}
	${VENV_PYTHON} setup.py sdist
	${VENV_PYTHON} setup.py bdist

venv: ${VENV}
${VENV}: ${VENV_PYTHON}
	$(info Enter Virtualenv with \n\n\t. $(VENV)/bin/activate)
${VENV_PYTHON} ${VENV_PIP} \
	${VENV_JUPYTER}\
	:
	$(PYTHON) -m venv ${VENV}
	${VENV_PIP} install -e .
${VENV_PYTEST}: ${VENV_PIP}
	${VENV_PIP} install -e .[tests]

clean: clean-venv clean-pycache
real-clean: clean-build clean-data clean-dist clean-test clean
	rm -rf *.egg-info/

clean-build:
	rm -rf build
clean-data:
	rm -rf *.csv
clean-dist:
	rm -rf dist
clean-pycache:
	find . -type f -path '*/__pycache__/*' -exec rm {} \;
	find . -type d -name __pycache__ -exec rmdir {} +
clean-test:
	rm -rf .eggs
clean-venv:
	rm -rf $(VENV)

.PHONY: all dist \
	venv \
	clean real-clean \
	clean-build clean-dist clean-venv
