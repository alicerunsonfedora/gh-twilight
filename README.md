# Project Twilight

Predict a repository's size based on a contributor's commit history.

## What is it?

Twilight is a project that aims to predict how many commits there are on projects you've contributed to by using machine learning models from SciKit Learn. Twilight makes use of tools like PyGithub and numpy to analyze repository datasets.

## Getting started

### Install via PyPI (TBD)

To install the project via PyPI, run `pip install gh-twilight`.

### Build from source

#### Requirements

- Python 3.7+
- Poetry package manager

#### Instructions
After cloning the repository, run `poetry install` in the root of the project, followed by `poetry build`.

### Configuring the project

In your terminal, run `gh-twilight --generate` to open the interactive Sparkle configuration generator. Alternatively, you can make a config TOML file like below:

```toml
[config.account]
token = "githubhash"
git_name = "Twilight Sparkle"

[config.activities]
models = ["forest", "neural"]
repos = [
    "equestria/friendship",
    "equestria/governance",
]
```

### Running the tool

Run `gh-twilight --config <pathToConfigFile>` to run the analysis tool. Graphs will be produced where the tool is run from.

#### Arguments

- `--config CONFIG`: The path to the Sparkle configuration file to read from and analyze.
- `--generate`: Run the interactive config generator.
- `--csv`: Export the raw repository dataset as a CSV file.
- `--json`: Export the raw repository dataset as a JSON file.