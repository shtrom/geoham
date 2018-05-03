VENV=.venv/geoham
PYTHON=python3

define activate
. $(VENV)/bin/activate
endef

all: dist

dist: install-dev
	$(call activate); \
		$(PYTHON) setup.py sdist; \
		$(PYTHON) setup.py bdist

install-dev: venv-install

venv: $(VENV)
$(VENV):
	virtualenv $@ -p$(PYTHON)

venv-install: venv
	$(call activate); \
		pip install -e .

clean: clean-venv
real-clean: clean-dist clean

clean-build:
	rm -rf build
clean-dist:
	rm -rf dist
clean-venv:
	rm -rf $(VENV)

.PHONY: all dist \
	install-dev \
	venv venv-install \
	clean real-clean \
	clean-build clean-dist clean-venv
