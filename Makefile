SRC_DIR = ulm
DOCS_DIR = docs

.PHONY: all help init devinit mininit check test \
	docs html readme requirements clean

all: help

help:
	@echo "Help"
	@echo "----"
	@echo
	@echo "  init - install recommended dependencies in virtualenv"
	@echo "  devinit - install full dependencies in virtualenv"
	@echo "  mininit - install min versions of dependencies in virtualenv"
	@echo "  check - run static checkers"
	@echo "  test - run tests"
	@echo "  docs - generate documentation with Sphinx"
	@echo "  readme - (re)generate README"
	@echo "  requirements - (re)generate pinned and minimum requirements"
	@echo "  clean - remove generated files"

init:
	@[ -n "$$VIRTUAL_ENV" ] || { echo "No virtualenv!"; exit 1; }
	@echo "Installing base dependencies"
	pip install -r requirements/base.txt

devinit:
	@[ -n "$$VIRTUAL_ENV" ] || { echo "No virtualenv!"; exit 1; }
	@echo "Installing full dependencies for development and testing"
	pip install -r requirements/local.txt

mininit: reqminvers.txt
	@[ -n "$$VIRTUAL_ENV" ] || { echo "No virtualenv!"; exit 1; }
	@echo "Installing minimum versions of dependencies"
	pip install -r reqminvers.txt

check:
	-flake8 $(SRC_DIR) *.py
	pylint --rcfile=pylint $(SRC_DIR) *.py

test:
	@TESTER=`which py.test nosetests | sed 1q`;			\
	 [ -n "$$TESTER" ] && $$TESTER $(SRC_DIR) ||			\
	 { echo py.test or nose required for testing 1>&2; exit 1; }

docs html:
	@# The following creates the HTML docs.
	make -C $(DOCS_DIR) html

readme: README.rst

README_DOCS:=intro overview $(DOCS_DIR)/install $(DOCS_DIR)/deploy
README_DOCS:=$(addsuffix .rst,$(README_DOCS))
README.rst: $(README_DOCS)
	cat $^ > $@

clean:
	@if git clean -ndX | grep .; then				\
	   printf 'Remove these files? (y/N) '; read ANS;		\
	   case $$ANS in [yY]*) git clean -fdX;; *) exit 1;; esac	\
	 fi

# Perform forced build using -W for the (.PHONY) requirements target
requirements:
	$(MAKE) -W $(REQFILE) reqminvers.txt requirements.txt

REQS=.reqs
REQFILE=requirements/production.txt

requirements.txt: $(REQFILE) requirements/base.txt # by inclusion
	@# Due to TLS 1.0 and 1.1 deprecation, pip 20 is required;
	@# see ttps://stackoverflow.com/questions/49768770 and/or run
	@# curl https://bootstrap.pypa.io/pip/2.7/get-pip.py | sudo python2
	@set -e;							\
	pip2 download -d $(REQS) -r $(REQFILE);				\
	: trap removes partial/empty target on failure;			\
	trap 'if [ "$$?" != 0 ]; then rm -f $@; fi' 0;			\
	(cd $(REQS) && ls *.tar* *.whl | sort | sed -e 's/-\([0-9]\)/==\1/' \
	-e 's/\.tar.*$$//' -e 's/-py2\.py3-none-any\.whl$$//' -e 's/_/-/g') >$@

reqminvers.txt: requirements/*.txt
	@if grep -q '>[0-9]' $^; then				\
	   echo "Use '>=' not '>' for requirements"; exit 1;	\
	 fi
	@echo "creating $@"
	@cat $^ | sed -n '/^.[^ ].*=/{s/>=/==/;s/<[^,]*,*//;s/,*$$//;p;}' >$@
