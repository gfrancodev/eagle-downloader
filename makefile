# Eagle Downloader - Makefile
# This Makefile automates common tasks for the Eagle Downloader project.

# Variables
PYTHON = python3
VENV_DIR = venv

# Detect Operating System
ifeq ($(OS),Windows_NT)
    OS_NAME = Windows
    PIP = $(VENV_DIR)\Scripts\pip.exe
    PYTHON_BIN = $(VENV_DIR)\Scripts\python.exe
    ACTIVATE = $(VENV_DIR)\Scripts\activate
    RM = del /Q /S
    ECHO = @echo
    SLASH = \\
else
    OS_NAME = Unix
    PIP = $(VENV_DIR)/bin/pip
    PYTHON_BIN = $(VENV_DIR)/bin/python
    ACTIVATE = source $(VENV_DIR)/bin/activate
    RM = rm -rf
    ECHO = @echo
    SLASH = /
endif

# Tools
LINT_TOOL = $(PYTHON_BIN) -m flake8
FORMAT_TOOL = $(PYTHON_BIN) -m black
TEST_TOOL = $(PYTHON_BIN) -m pytest
COVERAGE_TOOL = $(PYTHON_BIN) -m coverage
PYINSTALLER = $(PYTHON_BIN) -m PyInstaller

# Directories
SRC_DIR = .  # Source code directory
TESTS_DIR = tests

.PHONY: help venv install lint format test test-coverage build clean error

## ----------------------------------------
## Helper Functions
## ----------------------------------------

# Function to print error messages
error:
	$(ECHO) "Error: $(MESSAGE)"
	exit 1

## ----------------------------------------
## Targets
## ----------------------------------------

help:
	@echo "Eagle Downloader - Available commands:"
	@echo "  make venv             Create a virtual environment with Python 3.11.10"
	@echo "  make install          Install dependencies in the virtual environment"
	@echo "  make lint             Run linting on the code"
	@echo "  make format           Format the code"
	@echo "  make test             Run tests without coverage"
	@echo "  make test-coverage    Run tests with coverage and display the percentage"
	@echo "  make build            Build executables for different platforms"
	@echo "  make clean            Remove the virtual environment and temporary files"

venv:
	@echo "Creating virtual environment with Python 3.11.10..."
	$(PYTHON) -m venv $(VENV_DIR) || make error MESSAGE="Failed to create virtual environment."
	@echo "Virtual environment created in '$(VENV_DIR)'"

install: venv
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip setuptools wheel || make error MESSAGE="Failed to upgrade pip/setuptools/wheel."
	$(PIP) install -r requirements.txt || make error MESSAGE="Failed to install dependencies."
	@echo "Dependencies installed."

lint:
	$(PIP) install flake8 || make error MESSAGE="Failed to install flake8."
	$(LINT_TOOL) $(SRC_DIR) || make error MESSAGE="Linting failed."

format:
	$(PIP) install black || make error MESSAGE="Failed to install black."
	$(FORMAT_TOOL) $(SRC_DIR) || make error MESSAGE="Code formatting failed."

test:
	$(PIP) install pytest || make error MESSAGE="Failed to install pytest."
	$(TEST_TOOL) $(TESTS_DIR) || make error MESSAGE="Tests failed."

test-coverage:
	$(PIP) install coverage pytest || make error MESSAGE="Failed to install coverage or pytest."
	$(COVERAGE_TOOL) run -m $(TEST_TOOL) $(TESTS_DIR) || make error MESSAGE="Tests with coverage failed."
	$(COVERAGE_TOOL) report -m || make error MESSAGE="Coverage report generation failed."
	$(COVERAGE_TOOL) xml -o coverage.xml || make error MESSAGE="Coverage XML generation failed."
	$(COVERAGE_TOOL) report | grep "TOTAL" | awk '{print $$4}' > coverage.txt || make error MESSAGE="Extracting coverage percentage failed."
	@echo "Test coverage: $(shell cat coverage.txt)%"

build:
	@echo "Building executable..."
	$(PYINSTALLER) --onefile --name eagle main.py || make error MESSAGE="Build failed."
	@echo "Executable built successfully in 'dist/' directory."

clean:
	@echo "Removing virtual environment and temporary files..."
	$(RM) $(VENV_DIR) || make error MESSAGE="Failed to remove virtual environment."
	$(RM) __pycache__/
	$(RM) $(TESTS_DIR)/__pycache__/
	$(RM) .pytest_cache/
	$(RM) .coverage
	$(RM) coverage.xml
	$(RM) coverage.txt
	$(RM) dist/
	$(RM) build/
	$(RM) *.spec
	$(RM) htmlcov/
	$(RM) .mypy_cache/
	$(RM) *.pyc
	$(RM) *.pyo
	$(RM) *.coverage
	@echo "Cleanup completed."
