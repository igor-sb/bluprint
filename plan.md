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
├── .venv/
├── conf/
│   ├── config.yaml
│   ├── data.yaml
│   └── workflow.yaml
├── notebooks/
│   └── example.ipynb
├── project/
│   └── module_example.py
├── .gitignore
├── pyproject.toml
└── README.md

```

- data.yaml: file paths / locations
	- once loaded into `data`, access full paths using `data.group.raw` which
	  uses OmegaConf OmegaDict
- config.yaml: config other than paths, e.g. random seeds

- workflow.yaml: list of notebooks to run in sequence




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
* Add notebook execution to .github/workflows:

Adding features on top of the base blueprint:

* 

### Workflows

Usage: `bluprint run workflow a_and_b`

YAML definition in workflows.yaml:

```sh
a_and_b:
  - preprocess
  - summarize
  - plot
```

Use `poetry` to orchestrate jobs behind the scenes.
For each notebook create a function/method that calculates hash of the python
cells only.
Use caching with this hash to see if notebooks need to be re-run. 



Deprecated code:

```sh
def load_workflow_yaml(
    config_file: str = 'workflows.yaml',
    config_dir: str = 'conf',
    notebook_dir: str = 'notebooks',
) -> DictConfig:
    conf = load_config_yaml(config_file, config_dir)
    notebook_path = str(importlib.resources.files(notebook_dir).joinpath(''))
    for workflow_name, notebooks in conf.items():
        conf[workflow_name] = [
            str(Path(notebook_path) / notebook) for notebook in notebooks
        ]
    return conf


# CHECK IF SUB_CONFIG IS A RELATIVE PATH
# Don't append prefix if it's an absolute path, or URI
def add_prefix_to_nested_config(
    conf: DictConfig | ListConfig,
    prefix: str | PosixPath,
) -> DictConfig | ListConfig:
    config = deepcopy(conf)            
    if isinstance(config, ListConfig):
        for index, sub_config in enumerate(config):
            if isinstance(sub_config, DictConfig | ListConfig):
                config[index] = add_prefix_to_nested_config(sub_config, prefix)
            else:
                config[index] = f'{prefix}{sub_config}'

    elif isinstance(config, DictConfig):
        for key, sub_config in conf.items():
            if isinstance(sub_config, DictConfig | ListConfig):
                config[key] = add_prefix_to_nested_config(sub_config, prefix)
            else:
                config[key] = f'{prefix}{sub_config}'
    return config



def add_prefix_to_nested_config2(
    conf: DictConfig | ListConfig,
    prefix: str | PosixPath,
) -> DictConfig | ListConfig:
    config = conf
    def process_sub_config(sub_config: Any, key: Any):
        if isinstance(sub_config, DictConfig | ListConfig):
            config[key] = add_prefix_to_nested_config2(sub_config, prefix)         
        
    if isinstance(config, ListConfig):
        for index, sub_config in enumerate(config):
            if isinstance(sub_config, DictConfig | ListConfig):
                config[index] = add_prefix_to_nested_config(sub_config, prefix)
            else:
                config[index] = f'{prefix}{sub_config}'

    elif isinstance(config, DictConfig):
        for key, sub_config in conf.items():
            if isinstance(sub_config, DictConfig | ListConfig):
                config[key] = add_prefix_to_nested_config(sub_config, prefix)
            else:
                config[key] = f'{prefix}{sub_config}'
    return config
```