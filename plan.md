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
