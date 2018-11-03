VENV=.venv/geoham
PYTHON=python3

define activate
. $(VENV)/bin/activate
endef
define deactivate
deactivate || true
endef

all: dist

test: $(VENV)
	$(call activate); \
		pip install -r requirements-dev.txt; \
		pytest --doctest-modules

dist: $(VENV)
	$(call activate); \
		$(PYTHON) setup.py sdist; \
		$(PYTHON) setup.py bdist

venv: $(VENV)
	@echo -e "*** Enter Virtualenv with \n\n\t. $(VENV)/bin/activate\n"
$(VENV):
	$(call deactivate); \
	virtualenv $@ -p$(PYTHON)
	$(call activate); \
		pip install -r requirements.txt; \
		pip install -e .

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
	venv venv-install \
	clean real-clean \
	clean-build clean-dist clean-venv
