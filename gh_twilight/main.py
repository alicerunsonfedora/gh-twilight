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
import csv
import sys
import logging
import json
from argparse import ArgumentParser
from gh_twilight.data import GithubMLDataCollector
from gh_twilight.repo import GHRepositoryWeeksum
from gh_twilight.sparkle import TSConfiguration, create_sparkle_data

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

def sparkle_args():
    """Create the argument parser for Twilight."""
    sarg = ArgumentParser("Analyze your growth as a software developer on GitHub!")
    sarg.add_argument("--config",
                      nargs=1,
                      help="The path to the configuration file to read from.")
    sarg.add_argument("--csv",
                      action="store_true",
                      help="Create a CSV file that contains the dataset.")
    sarg.add_argument("--json",
                      action="store_true",
                      help="Create a JSON file that contains the dataset.")
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

    if not options.config:
        sparkle_args().print_help()
        return

    config = TSConfiguration(options.config[0])

    # Initialize the collector
    gh_collector = GithubMLDataCollector(config.get_token())

    # Get the dataset and go through every repo in the list to get its data.
    dataset = []
    if not config.study_repos:
        logging.log(logging.WARN, "Repository list is empty.")

    for repo in config.study_repos:
        dataset.append(gh_collector.get_weeksum(repo, by_author=config.git_name))

    if options.json:
        logging.info("Writing JSON dataset to dataset.json...")
        with open("dataset.json", "w+") as json_file:
            json_file.write(json.dumps([x.to_dict() for x in dataset], indent=4))

    if options.csv:
        logging.info("Writing CSV dataset to results.csv...")
        with open("dataset.csv", "w+") as csv_file_writer:
            csv_data_writer = csv.writer(csv_file_writer,
                                         delimiter=",",
                                         quotechar="|",
                                         quoting=csv.QUOTE_MINIMAL)
            csv_data_writer.writerow([
                "Repository",
                "Git Commit Author",
                "Total Commits",
                "Total Commits by Author",
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday"
            ])

            data: GHRepositoryWeeksum
            for data in dataset:
                csv_data_writer.writerow([
                    data.name,
                    data.author,
                    data.abstotal,
                    data.total,
                    data.weeksum.sunday(),
                    data.weeksum.monday(),
                    data.weeksum.tuesday(),
                    data.weeksum.wednesday(),
                    data.weeksum.thursday(),
                    data.weeksum.friday(),
                    data.weeksum.saturday()
                ])

if __name__ == "__main__":
    main()
