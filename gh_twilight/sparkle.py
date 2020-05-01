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
    """

    study_repos = []
    git_name = ""
    __api_token = ""

    def __init__(self, path: str):
        """Create a configuration from the given TOML file path.

        Arguments:
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
                "repos": []
            }
        }
    }
    sparkle["config"]["account"]["git_name"] = input("Enter your name in git.config: ")
    print("To log into GitHub, you will need to generate a personal access token from GitHub.")
    print("Go to https://github.com/settings/tokens/new?scopes=repo to create a token and then"
          + " copy the token below.")
    print("If you want to skip this step, press Enter or Return now.\n")
    sparkle["config"]["account"]["token"] = input("Enter your GitHub personal access token: ")
    with open("sparkle.toml", "w+") as sparkle_writer:
        sparkle_writer.write(toml.dumps(sparkle))
        logging.info("Written Sparkle file to sparkle.toml.")
