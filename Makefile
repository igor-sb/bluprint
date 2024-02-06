PDM_RUN := pdm run
FOLDERS= src
PROJ= src
NC=\033[0m # No Color

.PHONY: install autolint lint lint-flake8 shell precommit pdm-precommit \
		install-dev test report-coverage docs lint-mypy build

test:
		${PDM_RUN} coverage erase
		${PDM_RUN} coverage run --branch -m pytest tests ${PROJ} \
				--junitxml=junit/test-results.xml -v

install: install-dev
		pdm install

lint:
		make autolint
		make lint-flake8
		make lint-mypy

install-dev:
		cp tools/pre-commit .git/hooks
		chmod +x .git/hooks/pre-commit

autolint:
		@${PDM_RUN} autopep8 -r -i ${FOLDERS}
		@${PDM_RUN} unify -r -i ${FOLDERS}
		@${PDM_RUN} isort ${FOLDERS}

lint-flake8:
		@echo "\n${BLUE}Running flake8...${NC}\n"
		@${PDM_RUN} flake8 .

lint-mypy:
		@echo "\n${BLUE}Running mypy...${NC}\n"
		${PDM_RUN} mypy --show-error-codes ${PROJ}

precommit: pdm-precommit lint

pdm-precommit:
		${PDM_RUN} pre-commit run --all-files

report-coverage:
		${PDM_RUN} coverage report
		${PDM_RUN} coverage html
		${PDM_RUN} coverage xml

docs:
	@echo "\n${BLUE}Preparing Sphinx documentation...${NC}\n"
	@cd docs; rm -rf build; make html; make prepare-gh-pages

clean-docs:
	@cd docs; rm -rf build; rm -rf html

clean:
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf bluprint.egg-info
	rm -rf build
	rm -rf dist
	rm -rf htmlcov
	rm -rf junit
	rm -rf src/bluprint/__pycache__
	rm -rf src/bluprint/create/__pycache__
	rm -rf src/bluprint/bluprint.egg-info
	rm -rf tests/__pycache__

build:
	@rm -rf build; pdm build
