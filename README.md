![logo](docs/source/images/bluprint_logo.png)

# Bluprint

Bluprint is a command line utility for organizing and streamlining exploratory data science projects in a cookiecutter style, e.g.:

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

Easily import shared code **in any notebook or script** in the project:

```py
from demo.common_code import process_data
```

## Separate configuration from code

All data paths are listed relative to the *demo/data* directory in *data.yaml*:

```yaml
emailed:
	- messy: 'emailed/messy.xlsx'
user:
	- processed: 'user_processed.csv'
```

YAML configurations are parsed and handled using [OmegaConf]() that supports many additional features such as [variable interpolation]().

## File paths automatically handled

Organize or nest notebooks however you want, file paths are inferred automatically, e.g. *process.ipynb*:

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


There are other tools that support creating projects, such as
[RStudio's Projects](https://r4ds.hadley.nz/workflow-scripts.html) and
[Cookiecutter](https://drivendata.github.io/cookiecutter-data-science/), but 



