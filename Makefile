POETRY_RUN := pdm run
FOLDERS= bluprint
PROJ= bluprint
NC=\033[0m # No Color

.PHONY: install autolint lint lint-flake8 shell precommit poetry-precommit \
		install-dev test report-coverage docs

test:
		${POETRY_RUN} coverage erase
		${POETRY_RUN} coverage run --branch -m pytest tests src/${PROJ} \
				--junitxml=junit/test-results.xml -v

install: install-dev
		poetry install

lint:
		make autolint
		make lint-flake8
		make lint-mypy

install-dev:
		cp tools/pre-commit .git/hooks
		chmod +x .git/hooks/pre-commit

autolint:
		@${POETRY_RUN} autopep8 -r -i src/${FOLDERS}
		@${POETRY_RUN} unify -r -i src/${FOLDERS}
		@${POETRY_RUN} isort src/${FOLDERS}

lint-flake8:
		@echo "\n${BLUE}Running flake8...${NC}\n"
		@${POETRY_RUN} flake8 .

lint-mypy:
		@echo "\n${BLUE}Running mypy...${NC}\n"
		${POETRY_RUN} mypy --show-error-codes -p ${PROJ}

shell:
		poetry shell

precommit: poetry-precommit lint

poetry-precommit:
		${POETRY_RUN} pre-commit run --all-files

report-coverage:
		${POETRY_RUN} coverage report
		${POETRY_RUN} coverage html
		${POETRY_RUN} coverage xml

docs:
	@echo "\n${BLUE}Preparing Sphinx documentation...${NC}\n"
	@cd docs; make html; make prepare-gh-pages

clean-docs:
	@cd docs; rm -rf build; rm -rf html