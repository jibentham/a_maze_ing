PYTHON      = .venv/bin/python3
PIP         = .venv/bin/pip
MAIN        = main.py
NAME        = mazegen
VERSION     = 1.0.0
TARBALL     = $(NAME)-$(VERSION).tar.gz
INSTALL_DIR = $(NAME)-$(VERSION)
SOURCES     = main.py Makefile \
              maze/ algorithms/ rendering/ runner/ config/

run:
	@if [ -f $(TARBALL) ]; then \
		mkdir -p $(INSTALL_DIR); \
		tar -xzvf $(TARBALL) -C $(INSTALL_DIR); \
		cd $(INSTALL_DIR) && $(PYTHON) $(MAIN); \
	else \
		$(PYTHON) $(MAIN); \
	fi

install:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy
	@echo "Virtual environment created. Run 'make run' to start."

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -f output.txt

fclean: clean
	rm -f $(TARBALL)
	rm -rf .venv
	rm -rf $(INSTALL_DIR)

package: clean
	tar -czvf $(TARBALL) $(SOURCES)

lint:
	.venv/bin/flake8 .
	.venv/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	.venv/bin/flake8 .
	.venv/bin/mypy . --strict

.PHONY: run install debug clean fclean package lint lint-strict
