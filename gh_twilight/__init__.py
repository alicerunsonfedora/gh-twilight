#
# Project Twilight Module
# GitHub Machine Learning Project
# (C) 2020 Marquis Kurt
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""
Project Twilight is a machine learning experiment for my DMC345 (Intro to Machine Learning)
    course that tries to predict a Git repository's size by reading a list of numbers that
    represent commits in a week. This tool makes use of SciKit Learn, matplotlib, and NumPy to
    handle data manipulation and analysis and PyGithub to fetch data from GitHub.

## Installation

### Install via PyPI (TBD)
Run `pip install gh-twilight` to install the tool to your Python environment.

### Build from source

#### Requirements
- Python 3.7 or higher
- Poetry package manager

Clone the repository and run `poetry install` in the project root to set up the environment and
    install dependencies.

## Creating a configuration file

To create the config file that Project Twilight uses, run `gh-twilight --generate` in your
    terminal. The configuration utility will help you set up some details about what models you
    want to use for training, your GitHub access token, and how you want to predict your data.

## Running the utility

### Configuration arguments
- `--config CONFIG`: The path to the configuration file to use.
`--generate`: Runs the interactive configuration utility.

### Analysis and prediction arguments
- `--plot`: Creates plot graphs of predicted and testing data from training the network.
- `--predict`: Run predictions on the data provided in the configuration file.

### Extra arguments
- `--log-file LOG_FILE`: The path to where you want the logs to be store. Omitting this argument
    will disable logging.
- `--csv`: Exports the raw dataset to a CSV file before analysis.
- `--json`: Exports the raw dataset to a JSON file before analysis.

## Sparkle configuration file
The configuration file (in TOML syntax) contains important information on how to collect data, what
    data to collect, and how to run analysis and predictions. There are three important keys in the
    configuration file:

- `config.account`: Includes GitHub personal token and Git username.
- `config.activities`: Includes what repository to use as training data and what models to use.
- `config.predictions`: Includes what model to use to make predictions and inputs to predict.

### Account information
The `config.account` section includes the following keys:

- `git_name`: The Git username that made the commits to the repository
- `token`: The GitHub personal token with the `repo` permission.

### Activity configuration
The `config.activities` section includes the following keys:

- `models`: A list of strings containing what models to use. Valid options are `forest`, `neural`,
    and `linear`.
- `repos`: A list of strings containing the repositories on GitHub to use as training data.

### Prediction configuration
The `config.predictions` section includes the following keys:

- `method`: The model to use to make predictions. Valid options are `forest`, `neural`, `linear`,
    and `best`.
    - Using `best` will automatically determine the best model to use by using the model with the
        highest R2 accuracy score.
- `inputs`: A list of dictionaries that contain the input values to predict. The dictionary should
    have the following keys:
    - `name`: The name of the repository. This does _not_ need to point to a real repository on
        GitHub.
    - `commits`: A list containing seven integers that represent how many commits are made on the
        weekdays if all weeks are combined. For example, if a user make two commits to a repository
        every day for two weeks, the commits list should be `[4, 4, 4, 4, 4, 4, 4]`.

---

An example configuration may look like the following:
```toml
[config.account]
git_name = "Twilight Sparkle"
token = "githash"

[config.activities]
models = [ "forest", "linear" ]
repos = [ "equestria/friendship.equ", "equestria/governance" ]

[config.predictions]
method = "best"
inputs = [{ name = "equestria/journal", commits = [1, 13, 9, 8, 7, 12, 8] }]
```

## License
Project Twilight is free and open-source software licensed under the Mozilla Public License, v2.0.
"""
from .analysis import *
from .cli import *
from .commit import *
from .data import *
from .repo import *
from .sparkle import *

__version__ = '0.1.0'
