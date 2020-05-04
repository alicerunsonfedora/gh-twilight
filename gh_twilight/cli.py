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
from random import shuffle
from gh_twilight.data import GithubMLDataCollector
from gh_twilight.repo import GHRepositoryWeeksum
from gh_twilight.sparkle import TSConfiguration, TSConfigurationError, create_sparkle_data
from gh_twilight.analysis import create_dataset, analyze_dataset, TSDataAnalysisResult

def sparkle_args() -> ArgumentParser:
    """Create the argument parser for Twilight."""
    sarg = ArgumentParser("Predict a repository's size based on a contributor's commit history.")
    sarg.add_argument("--config",
                      nargs=1,
                      help="The path to the configuration file to read from.")
    sarg.add_argument("--log-file",
                      nargs=1,
                      help="The path to where a log file should be created.")
    sarg.add_argument("--csv",
                      action="store_true",
                      help="Create a CSV file that contains the dataset.")
    sarg.add_argument("--json",
                      action="store_true",
                      help="Create a JSON file that contains the dataset.")
    sarg.add_argument("--plot",
                      action="store_true",
                      help="Generate plot graphs from the analysis.")
    sarg.add_argument("--predict",
                      action="store_true",
                      help="Predict the project size for the given inputs in the config file.")
    sarg.add_argument("--generate",
                      action="store_true",
                      help="Generate a new Sparkle configuration.")
    return sarg

def generate_csv(raw_dataset: list):
    """Write a CSV file containing the raw dataset information.

    Args:
        raw_dataset (list): The list containing the repository information.
    """
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
        for data in raw_dataset:
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

def main(**kwargs):
    """Run the main program.

    Args:
        **kwargs (dict): Arbitrary keyword arguments.

    Kwargs:
        args (list): The list of arguments to pass to the program.
    """

    # Get the arguments needed for this program to function.
    args = kwargs["args"] if "args" in kwargs else sys.argv[1:]
    options = sparkle_args().parse_args(args)

    # Configure the logger and re-route logging data if requested.
    logging.basicConfig(format='[%(levelname)s] %(message)s',
                        level=logging.INFO,
                        filename=options.log_file[0] if options.log_file else None)

    # If the user has requested to generate a Sparkle configuration, run the interactive tool
    # and exit the program after.
    if options.generate:
        logging.info("Generate option detected. Generating new sparkle.toml...")
        try:
            create_sparkle_data()
        except KeyboardInterrupt:
            logging.info("Generation tool aborted by user.")
        return

    # If no configuration file has been supplied, display the help message and exit here.
    if not options.config:
        sparkle_args().print_help()
        return

    # Load the configuration file and create the GitHub data collector.
    print("🛠  Reading configuration...")
    try:
        config = TSConfiguration(options.config[0])
    except TSConfigurationError as err:
        logging.error("Configuration failed to load: %s", err)
        return

    if "config" not in vars():
        return

    gh_collector = GithubMLDataCollector(config.get_token())
    raw_dataset = []

    if not config.study_repos:
        logging.log(logging.WARN, "Repository list is empty.")

    # Collect the repository data for every repository listed in the config.
    print("🌎 Collecting data from GitHub...")
    shuffle(config.study_repos)
    for repo in config.study_repos:
        raw_dataset.append(gh_collector.get_weeksum(repo, by_author=config.git_name))
    print("Collected data for %s repositories." % (len(config.study_repos)))

    if options.json or options.csv:
        print("📥 Exporting raw dataset...")

    # Write a JSON file containing the raw data if requested.
    if options.json:
        logging.info("Writing JSON dataset to dataset.json...")
        with open("dataset.json", "w+") as json_file:
            json_file.write(json.dumps([x.to_dict() for x in raw_dataset], indent=4))

    # Write a CSV file containing the raw data if requested.
    if options.csv:
        logging.info("Writing CSV dataset to results.csv...")
        generate_csv(raw_dataset)

    # Create the dataset from the raw repository data.
    true_dataset = create_dataset(raw_dataset)

    print("🔍 Preparing network models...")
    logging.info("Running analysis on dataset...")
    analyses = [analyze_dataset(dataset=true_dataset, model=model) for model in config.models]

    # If predictions are enabled, run the predictions on the inputs in the config.
    if options.predict:
        print("📖 Making predictions...")
        logging.info("Predicting values in config...")
        sort_by_accuracy = lambda a: a.get_accuracy()
        matches_method = lambda x: x.model_type.name.lower() == config.prediction_method

        if config.prediction_method == "best":
            model = max(analyses, key=sort_by_accuracy)
            logging.info("Determined that %s is best model.", model.model_type.name.lower())
        else:
            model = [x for x in analyses if matches_method(x)][0]

        pred_input: dict
        for pred_input in config.inputs:
            logging.info("Predicting commit count for %s with weeksum %s...",
                         pred_input["name"],
                         pred_input["commits"])
            count = model.predict(pred_input["commits"])
            logging.info("Predicted value of %s.", count)
            print("Predicted that %s will have %s commits in total."
                  % (pred_input["name"], int(count)))

    # Create plot images if plot is passed as an argument.
    if options.plot:
        result: TSDataAnalysisResult
        for result in analyses:
            logging.info("Creating a plot for results using %s model.",
                         result.model_type.name.lower())
            try:
                result.plot()
                logging.info("Plot saved to sparkle_analytics_%s.png.", result.model_type.name)
            except Exception as err:    #pylint:disable=broad-except
                logging.error("Failed to plot data: %s", err)

# Main loop.
if __name__ == "__main__":
    main()
