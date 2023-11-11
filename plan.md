# Project Bluprint

## v1

Folder structure:

- notebooks
- src

.gitignore
pyproject.toml
poetry.lock
Makefile
LICENSE
README.md

Run a notebook in CI/CD:

```
poetry run jupyter nbconvert --execute --to notebook --inplace test.ipynb
```


Usage idea:

```
bluprint create {project_name} {python_version} (optional)
```

`pyenv latest 3` gives the last Python version in stdout.


would create this folder and file structure:

```
project
├── .github
│   └── workflows
│       └── notebooks.yaml
├── conf
│   └── config.yaml
├── notebooks
│   └── example.ipynb
├── src
│   └── module_example.py
├── pyproject.toml
├── README.md
└── Makefile
```

Steps:

* Check path for executables:
	- `poetry`
	- `git`
	- `gh`

* Create folder structure: `mkdir -p`:
	- `{project_name}/.github/workflows`
	- `{project_name}/conf`
	- `{project_name}/notebooks`
	- `{project_name}/src`
	Use `os.makedirs()`` from Python

* Run `poetry config --local virtualenvs.in-project true`
* Run `poetry init --name={package_name} --python={python_version} --no-interaction --directory={directory}`
* Create simple template `conf/config.yaml`
* Create simple example notebook `notebooks/example.ipynb`
* Create `src/module_example.py`
* Create `README.md` with `#{project_name}\n Description placeholder.`
* Makefile not really needed in v1?




## v2

In second version, implement these CI/CD:

* test: run all ipynb files within notebooks and all subfolders using workflows
* lint
	- lint `src/**/*.py` using flake8 (autopep8, unify, isort)
    - lint `notebooks/**/*.py` using nbqa (isort, flake8)

Makefile should implement: