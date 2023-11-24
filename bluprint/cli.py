"""Command-line interface for bluprint."""

import fire


class Bluprint(object):
    """Bluprint sub-commands used by CLI."""

    def create(self, project_name: str):
        """Create a new directory with a bluprint project."""
        print(f'Creating a new project {project_name}.')  # noqa: WPS421

    def init(self):
        """Initialize a bluprint project in existing directory."""
        print('Initializing project.')  # noqa: WPS421

    def workflow(self, workflow_yaml: str = 'conf/workflows.yaml'):
        """Run notebook workflows."""
        print('Running notebook workflows.')  # noqa: WPS421

    def config_from_dir(self, parse_dir: str):
        """Automatically create config.yaml from a dir with data files."""
        print('Generating config.')  # noqa: WPS421


def main():
    fire.Fire(Bluprint)


if __name__ == '__main__':
    main()
