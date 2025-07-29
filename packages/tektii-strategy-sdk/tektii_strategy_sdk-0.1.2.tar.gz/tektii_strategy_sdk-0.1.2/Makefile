# Makefile for tektii-strategy-sdk

.PHONY: help proto clean test test-watch lint format format-safe format-check install dev-install setup setup-dev proto-deps check quick-check security docstring-check install-check-deps run-example validate-example requirements release

# Default target
help:
	@echo "Available targets:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  setup         - Complete setup for first-time users"
	@echo "  setup-dev     - Setup development environment"
	@echo "  install       - Install the package"
	@echo "  dev-install   - Install with development dependencies"
	@echo "  proto-deps    - Install protobuf dependencies"
	@echo "  install-check-deps - Install all code quality dependencies"
	@echo ""
	@echo "Code Generation:"
	@echo "  proto         - Generate Python code from proto files"
	@echo ""
	@echo "Code Quality & Formatting:"
	@echo "  check         - Run ALL quality checks (recommended before commit)"
	@echo "  format        - Auto-fix code formatting and style issues"
	@echo "  lint          - Run linters (flake8, mypy)"
	@echo "  test          - Run tests with coverage"
	@echo "  security      - Run security checks with bandit"
	@echo "  docstring-check - Check docstring conventions"
	@echo ""
	@echo "Development:"
	@echo "  run-example   - Run example strategy"
	@echo "  validate-example - Validate example strategy"
	@echo "  test-watch    - Run tests in watch mode"
	@echo "  clean         - Clean generated files and caches"
	@echo ""
	@echo "Release:"
	@echo "  requirements  - Generate requirements files"
	@echo "  release       - Create release artifacts"

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(PYTHON) -m pip

# Proto compilation
PROTO_DIR := proto
PROTO_OUT := tektii_sdk/proto
PROTO_FILES := $(wildcard $(PROTO_DIR)/*.proto)

proto:
	@echo Pulling latest proto file...
	@$(PYTHON) proto/pull_proto.py
	@echo "Generating Python code from proto file..."
	@echo "Checking for grpc_tools..."
	@$(PYTHON) -c "import grpc_tools" 2>/dev/null || (echo "Error: grpcio-tools not installed. Run 'make proto-deps' first." && exit 1)
	@echo "Generating Python code from proto files..."
	@mkdir -p $(PROTO_OUT)
	@$(PYTHON) -m grpc_tools.protoc \
		-I$(PROTO_DIR) \
		--python_out=$(PROTO_OUT) \
		--grpc_python_out=$(PROTO_OUT) \
		$(PROTO_FILES)
	@# Fix imports in generated files - handle both macOS and Linux sed
	@if [ "$$(uname)" = "Darwin" ]; then \
		sed -i '' 's/import strategy_pb2/from . import strategy_pb2/' $(PROTO_OUT)/*_grpc.py 2>/dev/null || true; \
	else \
		sed -i 's/import strategy_pb2/from . import strategy_pb2/' $(PROTO_OUT)/*_grpc.py 2>/dev/null || true; \
	fi
	@touch $(PROTO_OUT)/__init__.py
	@echo "Proto generation complete!"

proto-deps:
	@echo "Installing protobuf dependencies..."
	@$(PIP) install grpcio-tools mypy-protobuf

# Clean
clean:
	@echo "Cleaning..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name ".coverage" -delete
	@rm -rf build/ dist/ *.egg-info/
	@rm -f $(PROTO_OUT)/*_pb2.py $(PROTO_OUT)/*_pb2_grpc.py $(PROTO_OUT)/*_pb2.pyi
	@echo "Clean complete!"

# Testing
test:
	@echo "Running tests..."
	@$(PYTHON) -m pytest tests/ -v --cov=tektii_sdk --cov-report=term-missing

test-watch:
	@echo "Running tests in watch mode..."
	@$(PYTHON) -m pytest tests/ -v --watch

# Linting with all flake8 plugins
lint:
	@echo "Installing flake8 plugins..."
	@$(PIP) install flake8-docstrings flake8-bugbear flake8-comprehensions flake8-simplify >/dev/null 2>&1 || true

	@echo "Running flake8..."
	@flake8 tektii_sdk/ tests/ \
		--max-line-length=150 \
		--extend-ignore=E203,W503 \
		--exclude=*_pb2*.py

	@echo "Running mypy..."
	@mypy tektii_sdk/ \
		--ignore-missing-imports \
		--exclude="proto/.*_pb2.*"

	@echo "Linting complete!"

# Security check with bandit
security:
	@echo "Installing bandit..."
	@$(PIP) install bandit >/dev/null 2>&1 || true

	@echo "Running security checks with bandit..."
	@bandit -r tektii_sdk -ll --exclude="tests/*" -f custom 2>/dev/null || bandit -r tektii_sdk -ll --exclude="tests/*"
	@echo "Security check complete!"

# Docstring checking with pydocstyle
docstring-check:
	@echo "Installing pydocstyle..."
	@$(PIP) install pydocstyle >/dev/null 2>&1 || true

	@echo "Checking docstrings..."
	@pydocstyle tektii_sdk \
		--convention=google \
		--match='(?!.*_pb2).*\.py' \
		--match-dir='(?!proto).*'
	@echo "Docstring check complete!"

# Formatting and auto-fixing
format:
	@echo "Installing formatting tools..."
	@$(PIP) install black isort autoflake pyupgrade docformatter >/dev/null 2>&1 || true

	@echo "Removing trailing whitespace..."
	@find tektii_sdk tests examples -name "*.py" -type f -exec sed -i.bak 's/[[:space:]]*$//' {} \; -exec rm {}.bak \; 2>/dev/null || true

	@echo "Fixing missing final newlines..."
	@find tektii_sdk tests examples -name "*.py" -type f -exec bash -c 'test -n "$(tail -c 1 "{}")" && echo >> "{}"' \; 2>/dev/null || true

	@echo "Fixing line endings to LF..."
	@find tektii_sdk tests examples -name "*.py" -type f -exec dos2unix {} \; 2>/dev/null || \
		find tektii_sdk tests examples -name "*.py" -type f -exec sed -i.bak 's/\r$//' {} \; -exec rm {}.bak \; 2>/dev/null || true

	@echo "Running autoflake to remove unused imports and variables..."
	@autoflake --in-place --recursive --remove-all-unused-imports --remove-unused-variables \
		--exclude="*_pb2*.py,__pycache__" \
		tektii_sdk/ tests/ examples/

	@echo "Running pyupgrade for Python syntax modernization..."
	@find tektii_sdk tests examples -name "*.py" -type f \
		! -path "*/proto/*_pb2*.py" \
		-exec pyupgrade --py38-plus {} \; 2>/dev/null || true

	@echo "Running isort..."
	@isort tektii_sdk/ tests/ examples/ \
		--profile=black \
		--line-length=150 \
		--skip-glob="**/proto/*_pb2*.py"

	@echo "Running black..."
	@black tektii_sdk/ tests/ examples/ \
		--line-length=150 \
		--exclude="proto/.*_pb2.*"

	@echo "Running docformatter..."
	@docformatter --in-place --recursive \
		--wrap-summaries=150 \
		--wrap-descriptions=150 \
		--exclude="*_pb2*.py" \
		tektii_sdk/ || true

	@echo "Formatting complete!"

# Installation
install: proto
	@echo "Installing package..."
	@$(PIP) install .

# Quick setup for first-time users
setup:
	@echo "Setting up tektii-strategy-sdk..."
	@$(PIP) install .
	@make proto-deps
	@make proto
	@$(PIP) install -e .
	@echo "Setup complete! Run 'make test' to verify installation."

# Comprehensive check, matching what pre-commit does
check:
	pre-commit run --all-files

# Validate example strategy
validate-example:
	@echo "Validating example strategy..."
	@$(PYTHON) -m tektii_sdk.cli validate examples/simple_ma_strategy.py SimpleMAStrategy

# Generate requirements from setup.py
requirements:
	@$(PIP)-compile setup.py --extra=dev -o requirements-dev.txt
	@$(PIP)-compile setup.py -o requirements.txt

# Create a new release
release: clean proto check
	@echo "Creating release..."
	@$(PYTHON) setup.py sdist bdist_wheel
	@echo "Release artifacts created in dist/"
	@echo "Run 'twine upload dist/*' to upload to PyPI"

# Install all quality check dependencies
install-check-deps:
	@echo "Installing all quality check dependencies..."
	@$(PIP) install flake8 flake8-docstrings flake8-bugbear flake8-comprehensions flake8-simplify
	@$(PIP) install mypy types-protobuf types-python-dateutil
	@$(PIP) install bandit pydocstyle
	@$(PIP) install black isort autoflake pyupgrade docformatter
	@echo "All check dependencies installed!"
