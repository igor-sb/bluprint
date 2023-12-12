PDM_RUN := pdm run
FOLDERS= src
PROJ= src
NC=\033[0m # No Color

.PHONY: install autolint lint lint-flake8 shell precommit poetry-precommit \
		install-dev test report-coverage docs lint-mypy

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

precommit: poetry-precommit lint

poetry-precommit:
		${PDM_RUN} pre-commit run --all-files

report-coverage:
		${PDM_RUN} coverage report
		${PDM_RUN} coverage html
		${PDM_RUN} coverage xml

docs:
	@echo "\n${BLUE}Preparing Sphinx documentation...${NC}\n"
	@cd docs; make html; make prepare-gh-pages

clean-docs:
	@cd docs; rm -rf build; rm -rf html