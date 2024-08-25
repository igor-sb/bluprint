UV_RUN := uv run
FOLDERS= src
PROJ= src
NC=\033[0m # No Color

.PHONY: install autolint lint lint-flake8 shell precommit uv-precommit \
		install-dev test test-update-snapshots report-coverage docs lint-mypy \
		build publish

test:
		${UV_RUN} coverage erase
		${UV_RUN} coverage run --branch -m pytest tests ${PROJ} \
				--junitxml=junit/test-results.xml -v

test-update-snapshots:
		${UV_RUN} coverage run --branch -m pytest --snapshot-update tests/workflow src

install: install-dev
		${UV_RUN} sync

lint:
		make autolint
		make lint-ruff
		make lint-mypy

install-dev:
		cp tools/pre-commit .git/hooks
		chmod +x .git/hooks/pre-commit

autolint:
		@${UV_RUN} autopep8 -r -i ${FOLDERS}
		@${UV_RUN} unify -r -i ${FOLDERS}
		@${UV_RUN} isort ${FOLDERS}

lint-flake8:
		@echo "\n${BLUE}Running flake8...${NC}\n"
		@${UV_RUN} flake8 .

lint-ruff:
		@echo "\n${BLUE}Running ruff...${NC}\n"
		@${UV_RUN} ruff check

lint-mypy:
		@echo "\n${BLUE}Running mypy...${NC}\n"
		${UV_RUN} mypy --show-error-codes ${PROJ}

precommit: uv-precommit lint

uv-precommit:
		${UV_RUN} pre-commit run --all-files

report-coverage:
		${UV_RUN} coverage report
		${UV_RUN} coverage html
		${UV_RUN} coverage xml

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
	@rm -rf dist; uvx --from build pyproject-build --installer uv

publish:
	@uvx twine upload dist/*