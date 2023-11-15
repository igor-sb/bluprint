# Project Bluprint

## Motivation

Bluprint solves problems encounted in data science exploratory work:

1. Setup a template for data science exploratory projects
1. Using YAML-based config files
1. Move and immediately use Python code outside of Jupyter Notebooks
1. Run notebooks as a workflow

## v1

Run a notebook in CI/CD:

```
poetry run jupyter nbconvert --execute --to notebook --inplace test.ipynb
```

We can create an alias for this, e.g.:

```
bluprint run notebook test
```

Run a pipeline of notebooks (pipeline name should match yaml definition):

```
```


Usage idea:

```
bluprint create {project_name} {python_version} (optional)
```

`pyenv latest 3` gives the last Python version in stdout.


would create this folder and file structure:

```
project
├── conf
│   ├── config.yaml
│   └── workflow.yaml
├── notebooks
│   └── example.ipynb
├── project
│   └── module_example.py
├── .gitignore
├── pyproject.toml
└── README.md

```

Steps for creating a new project `bluprint create {project_name}`:

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
* Add notebook execution to .github/workflows:

Adding features on top of the base blueprint:

* 

### Workflows

Usage: `bluprint run workflow a_and_b`

YAML definition in workflows.yaml:

```
a_and_b:
  - preprocess
  - summarize
  - plot
```
