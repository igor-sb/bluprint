![logo](docs/source/images/bluprint_logo.png)

# Bluprint

Bluprint is a command line utility for organizing exploratory data science projects using this type of directory structure:

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

File paths are stored in *data.yaml*, relative to the *demo/data* directory:

```yaml
emailed:
  - messy: 'emailed/messy.xlsx'
user:
  - processed: 'user_processed.csv'
```

Bluprint also installs the entire directory as an editable Python package (like [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)), which means Python source code can be easily imported into notebooks.

Here's an example of how *process.ipynb* could look:

```py
from bluprint_conf import load_data_yaml
from demo.common_code import process_data
import pandas as pd

data = load_data_yaml() # default arg: conf/data.yaml
print(data)
#> {
#>   'emailed': {
#>     'messy': '/path/to/demo/data/emailed/messy.xlsx'
#>   },
#>   'user': {
#> 	   'processed': '/path/to/demo/data/user_processed.csv'
#>   }
#> }

messy_df = pd.read_xlsx(data.emailed.messy)

processed_df = process_data(messy_df)

processed_df.to_csv(data.user.processed)
```

For a demonstration of a shareable project see
[https://github.com/igor-sb/bluprint-demo/](https://github.com/igor-sb/bluprint-demo/).

## Bluprint project features

* Configuration, data and common code can be consistenly imported without hunting down relative paths or copy/pasting absolute paths across the code.

* [load_data_yaml()](https://igor-sb.github.io/bluprint-conf/html/reference.html#bluprint_conf.config.load_data_yaml) automatically parses relative paths while leaving absolute paths and URIs untouched.

* Yaml configurations are loaded as [OmegaConf](https://omegaconf.readthedocs.io/) dictionaries, which supports many useful features such as [variable interpolation](https://omegaconf.readthedocs.io/en/2.3_branch/usage.html#variable-interpolation) and [merging multiple yaml files](https://omegaconf.readthedocs.io/en/2.3_branch/usage.html#merging-configurations) into a single configuration.

* Bluprint projects can be shared without needing bluprint! [Bluprint_conf](https://github.com/igor-sb/bluprint-conf/) is a separate lightweight Python package (basically OmegaConf wrapper with path inference) automatically added as a project dependency.

* Support for both Jupyter and RMarkdown notebooks.

* Bluprint projects are reproducible thanks to PDM pinning versions of all dependecies in a *pdm.lock* file and {renv} doing the same with R packages.

* Support for simple workflows.

## Examples

See a [demo project](https://github.com/igor-sb/bluprint-demo/) as an example.

## Installation

Install [pipx](https://github.com/pypa/pipx) and [PDM](https://pdm-project.org/latest/). Then run:

```sh
pipx install bluprint
```

---

Bluprint is released under [MIT license](LICENSE).
