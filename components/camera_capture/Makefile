# === GLOBAL VARIABLES ======================================================
PROJECT_SRC=camera_capture
DOCKER_COMPOSE_APP=camera-capture
TEST_COVERAGE_PERCENTAGE=100

# === COMMANDS ==============================================================
# Installs the Python dependencies
install:
	pip install -r requirements.txt

# Installs the dev Python dependencies
install-dev: install
	echo "Installing DEV dependencies"
	pip install -e ".[dev]"

# Lints the code
lint:
	flake8 $(PROJECT_SRC)/
	flake8 tests/
	black --check $(PROJECT_SRC)/
	black --check tests/
	isort --check-only .
	mypy $(PROJECT_SRC) --ignore-missing-imports

# Formats the code (when possible) to the lint standards
format:
	black $(PROJECT_SRC)/
	black tests/
	isort .

# Runs the Unit tests
unit:
	python -m pytest tests/unit/ -v

# Runs the component tests
component:
	python -m pytest tests/component/ -v

# Tests coverage check and reports
coverage:
	coverage run -m pytest tests -v
	coverage report --fail-under=$(TEST_COVERAGE_PERCENTAGE)

# Tests CI coverage report (for external tools)
coverage-report: coverage
	coverage report --fail-under=$(TEST_COVERAGE_PERCENTAGE)
	coverage html -d build/coverage
	coverage xml -o build/coverage.xml

# Summaries LOC
pygount-summary:
	echo "pygount - tests/"
	pygount --suffix=py,yml --format=summary tests/
	echo ""
	echo "pygount - $(PROJECT_SRC)/"
	pygount --suffix=py,yml --format=summary $(PROJECT_SRC)/
	echo ""

# Runs all the QA tooling
qa: lint unit component coverage pygount-summary

# Locks the dependency file (from setup.py)
freeze:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile --no-annotate --no-emit-index-url --output-file requirements.txt setup.py --cache-dir /tmp/pip-compile-cache

# Upgrades the dependencies lock file
freeze-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile --no-annotate --no-emit-index-url --output-file requirements.txt --upgrade setup.py --cache-dir /tmp/pip-compile-cache

# Builds the development container
docker:
	docker-compose build --pull

# Gets a shell inside the development container (note: You can sudo this)
docker-shell:
	docker-compose run --user="`id -u`" --rm $(DOCKER_COMPOSE_APP) bash

# Alias for docker-shell
shell:
	make docker-shell
