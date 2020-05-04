#
# Configurations
# GitHub Machine Learning Project
# (C) 2020 Marquis Kurt
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""The sparkle submodule contains the utilities necessary for handling Sparkle configurations
    for use with the main program."""
import logging
import toml
from gh_twilight.analysis import TSDataModel

class TSConfigurationError(Exception):
    """Could not load, parse, or read the configuration requested."""

class TSConfiguration:
    """The class representation of sparkle.toml.

    The Sparkle configuration contains important information such as the GitHub API token to use,
        what repositories to scan, and other configurations that are necessary for Twilight to
        work correctly.

    Attributes:
        study_repos (list): The list of repos to use as modeling data.
        git_name (str): The name of the Git author to filter for, if any.
        prediction_method (str): The method for making predictions.
        inputs (list): The list of inputs to predict values for.
    """

    study_repos = []
    models = []

    prediction_method = ""
    inputs = []

    git_name = ""
    __api_token = ""

    def __init__(self, path: str):
        """Create a configuration from the given TOML file path.

        Args:
            path (str): The file path to the sparkle.toml to read from.
        """
        with open(path, 'r') as sparkle_reader:
            sparkle_toml = toml.loads(sparkle_reader.read())

            if "config" not in sparkle_toml:
                raise TSConfigurationError("Config field is missing or corrupted.")

            s_dict = sparkle_toml["config"]

            if "account" not in s_dict:
                raise TSConfigurationError("Account data is missing from config.")
            self.__api_token = s_dict["account"]["token"]
            self.git_name = s_dict["account"]["git_name"]

            if "activities" not in s_dict:
                raise TSConfigurationError("Activity data missing from config.")
            self.study_repos = s_dict["activities"]["repos"]

            self.models = []
            for model in s_dict["activities"]["models"]:
                if model == "neural" and TSDataModel.NEURAL not in self.models:
                    self.models.append(TSDataModel.NEURAL)
                elif model == "linear" and TSDataModel.LINEAR not in self.models:
                    self.models.append(TSDataModel.LINEAR)
                elif model == "forest" and TSDataModel.FOREST not in self.models:
                    self.models.append(TSDataModel.FOREST)
                else:
                    raise TSConfigurationError("Invalid model configuration: %s." % (model))


            if "predictions" not in s_dict:
                raise TSConfigurationError("Prediction data missing from config.")

            self.prediction_method = s_dict["predictions"]["method"]
            self.inputs = s_dict["predictions"]["inputs"]

            logging.info("Loaded Sparkle configuration from %s.", path)

    def get_token(self) -> str:
        """Grab the personal access token from the configuration.

        Returns:
            api_token (str): The personal access token used for the analysis.
        """
        return self.__api_token

def create_sparkle_data():
    """Interactively create sparkle.toml."""
    sparkle = {
        "config": {
            "account": {
                "git_name": "",
                "token": ""
            },
            "activities": {
                "models": [],
                "repos": []
            },
            "predictions": {
                "method": "best",
                "inputs": [
                    {
                        "name": "example_org/example_repo",
                        "commits": [0, 0, 0, 0, 0, 0, 0]
                    }
                ]
            }
        }
    }
    sparkle["config"]["account"]["git_name"] = input("Enter your name in git.config: ")

    # Get the GitHub token.
    print("To log into GitHub, you will need to generate a personal access token from GitHub.")
    print("Go to https://github.com/settings/tokens/new?scopes=repo to create a token and then"
          + " copy the token below.")
    print("If you want to skip this step, press Enter or Return now.\n")
    sparkle["config"]["account"]["token"] = input("Enter your GitHub personal access token: ")

    # Get the models.
    print("\nWhat kinds of models do you want to use when analyzing your data?")
    print("Valid options are: \"linear\", \"forest\", and \"neural\".")
    print("To use multiple models, separate the models with a comma (no spaces).")
    sparkle["config"]["activities"]["models"] = input("Enter your models here: ").split(",")

    # Get the method for prediction.
    print("How do you want to predict your data?")
    print("Options are: forest, neural, linear, and best (uses model with highest accuracy).")
    sparkle["config"]["predictions"]["method"] = input("Enter your prediction method here: ")
    with open("sparkle.toml", "w+") as sparkle_writer:
        sparkle_writer.write(toml.dumps(sparkle))
        logging.info("Written Sparkle file to sparkle.toml.")
