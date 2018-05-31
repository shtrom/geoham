VENV=.venv/geoham
PYTHON=python3

define activate
. $(VENV)/bin/activate
endef

all: dist

test:
	$(call activate); \
		pip install pytest; \
		pytest --doctest-modules

dist: venv-install
	$(call activate); \
		$(PYTHON) setup.py sdist; \
		$(PYTHON) setup.py bdist

venv: $(VENV)
$(VENV):
	virtualenv $@ -p$(PYTHON)

venv-install: venv
	$(call activate); \
		pip install -e .
	@echo "Enter Virtualenv with '. $(VENV)/bin/activate'"

clean: clean-venv
real-clean: clean-data clean-dist clean
	rm -rf *.egg-info/

clean-build:
	rm -rf build
clean-dist:
	rm -rf dist
clean-venv:
	rm -rf $(VENV)
clean-data:
	rm -rf *.csv

.PHONY: all dist \
	venv venv-install \
	clean real-clean \
	clean-build clean-dist clean-venv
