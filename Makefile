#!/usr/bin/env make

#
# Makefile
#

default: pep doc test

githook:
	git config core.hooksPath .githooks

pep:
	yapf --style '{based_on_style: pep8; indent_width: 4}' -i get_vat_eu/*.py tests/*.py
	flake8 --ignore=F401,E501,W503,W504,W605,E125 get_vat_eu/*.py tests/*.py

doc:
	$(MAKE) -C docs html

install:
	pip3 install .

test:
	python3 setup.py test

uninstall:
	pip3 uninstall get_vat_eu

clean:
	rm -rf build dist *.egg-info tests/benchmark-results

.PHONY: default pep doc install test uninstall dist upload clean
