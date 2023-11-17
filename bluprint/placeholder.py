"""Placeholder file contents for new projects."""

import yaml
import inspect


def add_one(x: int) -> int:
	return x + 1


def create_readme_md(project_name: str) -> None:
    with open(f'{project_name}/README.md', 'w') as readme:
        readme.write(f'#{project_name}\n Description.')


def create_example_module(
    project_name: str,
    python_file: str,
) -> None:
    with open(f'{project_name}/{project_name}/{python_file}', 'w') as py:
        py.write(inspect.getsource(add_one))


def create_config_yaml(contents: dict, file: str) -> None:
    yaml_contents = {
        'raw_table': 'data/raw/table1.csv',
        'transformed_table': 'data/transformed/table2.csv',
    }
    with open(file, 'w') as yaml_file:
        yaml.dump(contents, yaml_file, default_flow_style=False)