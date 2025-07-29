PYTHON ?= python3
PIP    ?= pip3

MODULE_NAME  ?= $(notdir $(PWD))
MODULE_SPATH ?= $(subst -,_,$(MODULE_NAME))

PYTMPDIR ?= var/lib/python

REQUIERD_MODULES = build twine

TWINE ?= $(PYTMPDIR)/bin/twine
BUILD ?= $(PYTMPDIR)/build
TOML ?= $(PYTMPDIR)/toml

MOD_TEST_DIR_SRC  ?= var/tmp/test_src
MOD_TEST_DIR_DIST ?= var/tmp/test_dist

MOD_DEPENDENCIES := $(shell env PYTHONPATH=$(PYTMPDIR):$(PYTHONPATH) $(PYTHON) -c "import sys,toml;[sys.stdout.write(i) for i in toml.load('pyproject.toml').get('project')['dependencies']]")

MOD_VERSION := $(shell env PYTHONPATH=$(PYTMPDIR):$(PYTHONPATH) $(PYTHON) -c "import sys,toml;sys.stdout.write(toml.load('pyproject.toml').get('project')['version'])")

MOD_TEST_OPT = '-h'

.PHONY: info clean sdist test_src test_dist test_upload upload clean distclean

info:
	@echo 'Module name         : '$(MODULE_NAME)
	@echo 'Module short path   : '$(MODULE_SPATH)
	@echo 'Module VERSION      : '$(MOD_VERSION)
	@echo 'Module dependencies : '$(MOD_DEPENDENCIES)

$(TWINE): 
	env PYTHONPATH=$(PYTMPDIR):$(PYTHONPATH) $(PIP) install --target $(PYTMPDIR) $(notdir $@)

$(BUILD): 
	env PYTHONPATH=$(PYTMPDIR):$(PYTHONPATH) $(PIP) install --target $(PYTMPDIR) $(notdir $@)

$(TOML):
	env PYTHONPATH=$(PYTMPDIR):$(PYTHONPATH) $(PIP) install --target $(PYTMPDIR) $(notdir $@)

sdist:
	env PYTHONPATH=$(PYTMPDIR):$(PYTHONPATH) $(PYTHON) -m build 

test_src: $(MOD_TEST_DIR_SRC)
	env PYTHONPATH=$(MOD_TEST_DIR_SRC):$(PYTHONPATH) $(PIP) install --target $(MOD_TEST_DIR_SRC) $(notdir $(MOD_DEPENDENCIES))
	env PYTHONPATH=$(MOD_TEST_DIR_SRC):$(PYTHONPATH) $(PIP) install --target $(MOD_TEST_DIR_SRC) $(PWD)
	env PYTHONPATH=$(MOD_TEST_DIR_SRC):$(PYTHONPATH) $(MOD_TEST_DIR_SRC)/bin/$(MODULE_SPATH) $(MOD_TEST_OPT)

test_dist: $(MOD_TEST_DIR_DIST) dist/$(MODULE_SPATH)-$(MOD_VERSION).tar.gz
#env PYTHONPATH=$(MOD_TEST_DIR_DIST):$(PYTHONPATH) $(PIP) install --target $(MOD_TEST_DIR_DIST) $(notdir $(MOD_DEPENDENCIES))
	env PYTHONPATH=$(MOD_TEST_DIR_DIST):$(PYTHONPATH) $(PIP) install --target $(MOD_TEST_DIR_DIST) dist/$(MODULE_SPATH)-$(MOD_VERSION).tar.gz
	env PYTHONPATH=$(MOD_TEST_DIR_DIST):$(PYTHONPATH) $(MOD_TEST_DIR_DIST)/bin/$(MODULE_SPATH) $(MOD_TEST_OPT)

dist/$(MODULE_SPATH)-$(MOD_VERSION).tar.gz: sdist

$(MOD_TEST_DIR_SRC):
	mkdir -p $(MOD_TEST_DIR_SRC)

$(MOD_TEST_DIR_DIST):
	mkdir -p $(MOD_TEST_DIR_DIST)

test_upload: $(TWINE) sdist
	env PYTHONPATH=$(PYTMPDIR):$(PYTHONPATH) $(TWINE) upload --verbose --repository pypitest dist/*

upload: $(TWINE) sdist
	env PYTHONPATH=$(PYTMPDIR):$(PYTHONPATH) $(TWINE) upload --verbose dist/*

clean: 
	rm -rf src/$(MODULE_SPATH)/*~ \
           src/$(MODULE_SPATH)/__pycache__ \
           src/$(MODULE_SPATH)/share/data/*~ \
           dist/* build/* var/lib/python/* *~ test/*~ 

distclean: clean
	rm -rf $(MODULE_SPATH).egg-info \
           dist build lib var

