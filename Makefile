# Common commands for the BIИ practical cycle repository.
# Windows users: run `make` from Git Bash / WSL, or execute the commands directly.

PY ?= python

.PHONY: help install reproduce reproduce-preliminary reproduce-pr1 test clean

help:
	@echo "Available commands:"
	@echo "  make install                - Install dependencies"
	@echo "  make reproduce              - Reproduce preliminary + PR1 results"
	@echo "  make reproduce-preliminary  - Reproduce the frozen baseline metric M(0)"
	@echo "  make reproduce-pr1          - Reproduce PR1 data-quality metrics"
	@echo "  make test                   - Run smoke tests"
	@echo "  make clean                  - Remove caches and temporary files"

install:
	$(PY) -m pip install -r requirements.txt

reproduce: reproduce-preliminary reproduce-pr1

reproduce-preliminary:
	$(PY) scripts/reproduce_preliminary.py

reproduce-pr1:
	$(PY) scripts/reproduce_pr1.py

test:
	$(PY) -m pytest tests/ -v

clean:
	$(PY) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__') if p.is_dir()]; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('.ipynb_checkpoints') if p.is_dir()]"
