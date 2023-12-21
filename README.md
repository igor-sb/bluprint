![logo](docs/source/images/bluprint_logo.png)

# Bluprint

Bluprint is a command line utility for organizing exploratory data science projects. Bluprint creates projects in this type of directory structure:

```
demo
├── conf
│   └── data.yaml
├── data
│   ├── emailed
│   │   └── messy.xlsx
│   └── user_processed.csv
├── notebooks
│   ├── pre
│   │   └── process.ipynb
│   └── final_report.ipynb
└── demo
    └── common_code.py
```

## Import shared code

Easily import shared code in notebook or script **anywhere** in the project:

```py
from demo.common_code import process_data
```

No more hunting down the relative paths, deleting and copy/pasting absolute paths to files, scripts, etc. It just works. 🙌

## Separate configuration from code

All data paths are listed relative to the *demo/data* directory in *data.yaml*:

```yaml
emailed:
  - messy: 'emailed/messy.xlsx'
user:
  - processed: 'user_processed.csv'
```

Relative paths in *config/data.yaml* will be automatically parsed by [load_data_yaml()](https://igor-sb.github.io/bluprint-conf/html/reference.html#bluprint_conf.config.load_data_yaml). Absolute paths and URIs are auto-detected and are left untouched, so your project can access data from anywhere.

Yaml configurations are loaded as [OmegaConf](https://omegaconf.readthedocs.io/) dictionaries, which supports many useful features such as [variable interpolation](https://omegaconf.readthedocs.io/en/2.3_branch/usage.html#variable-interpolation) and [merging multiple yaml files](https://omegaconf.readthedocs.io/en/2.3_branch/usage.html#merging-configurations) into a single configuration. This can help you organize complex project configuration across multiple files without repeating main paths.

## Create portable notebooks

Organize or nest notebooks however you want, file paths of data, config and Python files are inferred automatically. For example, *process.ipynb*:

```py
# py cell 1
from bluprint_conf import load_data_yaml
from common_code import process_data
import pandas as pd

data = load_data_yaml() # default arg: conf/data.yaml

# py cell 2
messy_df = pd.read_xlsx(data.emailed.messy)

# py cell 3
processed_df = process_data(messy_df)

# py cell 4
processed_df.to_csv(data.user.processed)
```

## Run notebook workflows

Workflow feature is inspired by [Databricks Workflows](https://docs.databricks.com/en/workflows/index.html) and can be used to run integration tests on your notebooks to make sure they execute without errors.

To run workflows simply create a *conf/workflows.yaml* file that specifies the order in which notebooks will run:

```yaml
my_workflow:
  - pre/process.ipynb
  - final_report.ipynb
```

and then run:

```sh
bluprint workflow my_workflow
```

## Sharing reproducible projects

Bluprint uses [PDM](https://pdm-project.org) to pin all Python project dependencies and [renv](https://rstudio.github.io/renv/articles/renv.html) to pin all R dependencies. Bluprint projects can be shared on Github and installed and used without needing bluprint! [Bluprint_conf](https://igor-sb.github.io/bluprint-conf/html/index.html) is a separate lightweight Python package that wraps OmegaConf which is automatically added as a project dependency.

See a shared [demo project](https://github.com/igor-sb/bluprint-demo/) as an example.


## Support for RMarkdown notebooks

Once the Bluprint project is created, you can access yaml configuration and data paths using through [reticulate]() R package and just use RStudio as usual.



# Alternatives

There are other tools that support creating data science projects, such as
[RStudio's Projects](https://r4ds.hadley.nz/workflow-scripts.html) and
[Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/). They were both big inspiration behind Bluprint. 

Cookiecutter Data Science also instals a project directory as an editable Python package and suggests using a very similar project structure. However, I felt that data and configuration handling part is a big missing feature and I prefer to use poetry or PDM to manage Python dependencies. 

RStudio Project system sets up current working directory to the project root so R scripts work similar to Bluprint project (but not RMarkdown notebooks).However I haven't found anything close to OmegaConf to deal with yaml configurations in R.




---

Bluprint is released under [MIT license](LICENSE).