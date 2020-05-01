#
# Main Entry Point
# GitHub Machine Learning Project
# (C) 2020 Marquis Kurt
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

"""The main module contains the utilities necessary to handle the command-line logic for the
    tool."""
import sys
import logging
from argparse import ArgumentParser
from gh_twilight.data import GithubMLDataCollector
from gh_twilight.sparkle import TSConfiguration, create_sparkle_data

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

def sparkle_args():
    """Create the argument parser for Twilight."""
    sarg = ArgumentParser("Analyze your growth as a software developer on GitHub!")
    sarg.add_argument("--config",
                      nargs=1,
                      help="The path to the configuration file to read from.")
    sarg.add_argument("--generate",
                      action="store_true",
                      help="Generate a new Sparkle configuration.")
    return sarg

def main(**kwargs):
    """Run the main program.

    Arguments:
        **kwargs (dict): Arbitrary keyword arguments.

    Keyword Arguments:
        args (list): The list of arguments to pass to the program.
    """
    args = kwargs["args"] if "args" in kwargs else sys.argv[1:]
    options = sparkle_args().parse_args(args)

    if options.generate:
        logging.info("Generate option detected. Generating new sparkle.toml...")
        try:
            create_sparkle_data()
        except KeyboardInterrupt:
            logging.info("Generation tool aborted by user.")
        return

    if options.config:
        config = TSConfiguration(options.config[0])

        # Initialize the collector
        gh_collector = GithubMLDataCollector(config.get_token())

        # Get the dataset and go through every repo in the list to get its data.
        dataset = []
        if not config.study_repos:
            logging.log(logging.WARN, "Repository list is empty.")

        for repo in config.study_repos:
            dataset.append(gh_collector.get_weeksum(repo, by_author=config.git_name).to_dict())

if __name__ == "__main__":
    main()
