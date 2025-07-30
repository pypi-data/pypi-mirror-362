[![Test (uv)](https://github.com/mipwise/mwcommons/actions/workflows/tests.yaml/badge.svg)](https://github.com/mipwise/mwcommons/actions/workflows/tests.yaml)

**A utility package to enhance workflows in projects using TicDat.**

The `mwcommons` library is designed to streamline development and improve usability for optimization and machine 
learning projects that rely on [TicDat](https://pypi.org/project/ticdat/). This shared utility package offers specialized tools, helper functions, 
and custom exceptions, enabling faster development and consistent workflows.


### Common Maintenance Tasks

- **Installing dependencies**:
  - For fresh environments or setting up the project for the first time.
    - Install uv using pip or pipx. The last one is more recommended to its global isolation property.
      - `pipx install uv`
  - Create virtual environment using uv.
    - `uv venv`
    - If you need to create the venv based on a specific python you can use:
      - `uv venv --python python3.11`
  - Install dependencies using uv.
    - `uv sync`

- **Add dependencies**:
  - `uv add <package-name>`

- **Removing dependencies**:
  - `uv remove <package-name>`
  
- **Updating version of the project**: 
  - Change the version into the pyproject.toml.
  - It uses semantic versioning: '<patch/minor/major>`
  
- **Running tests**: 
  - python -m unittest discover test_mw_utils

- **Maintaining a changelog**: 
  - Update `CHANGELOG.md` with each release  

- **Tagging the release**: 
  - `git tag v<new-version>` 

- **Building the package**: 
  - This will create a `dist` directory with the built package.
  - `uv build`

- **Publishing to PyPI**: 
  - `uv publish --repository pypi`,
  - or `twine upload dist/*`.
