#
# Data Analysis
# GitHub Machine Learning Project
# (C) 2020 Marquis Kurt
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

"""The analysis submodule contains the utilities and functions necessary for analyzing repository
    data."""
from enum import IntEnum
import logging
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import pyplot as plt
from gh_twilight.repo import GHRepositoryWeeksum

class TSDataModel(IntEnum):
    """An enumeration for the type of data model to analyze with.

    Enumerations:
        LINEAR: Used for the linear regression model.
        NEURAL: Used for a neural network with two layers and ten nodes per layer with an alpha of
            0.1.
        FOREST: Used for the random forest regression model.
    """
    LINEAR = 0
    NEURAL = 1
    FOREST = 2

class TSDatasetGenerateError(Exception):
    """Could not create the analysis dataset."""

class TSDataAnalysisError(Exception):
    """Could not analyze the dataset."""

def create_raw_matrix(raw_dataset: list) -> np.ndarray:
    """Convert a list of GHRepositoryWeeksum objects to a proper numpy array for analysis.

    Arguments:
        raw_dataset (list): The list of GHRepositoryWeeksum objects to convert

    Returns:
        matrix (ndarray): A numpy array that contains all of the weekday commit numbers for every
            repository in the list.
    """
    repository: GHRepositoryWeeksum
    matr = None
    for repository in raw_dataset:
        repo_array = np.array(repository.weeksum.to_list())
        matr = np.vstack([matr, repo_array]) if matr is not None else repo_array

    if matr is None:
        matr = np.empty((1, 1))
    return matr

def create_dataset(raw: list) -> tuple:
    """Create a dataset used for numpy analysis from a repository dataset list.

    Arguments:
        raw (list): The list of GHRepositoryWeeksum objects to create a dataset for

    Returns:
        data (dict): A dictionary containing the dataset, as well as targets and features.
    """
    dataset = {
        "targets": [x.name for x in raw],
        "features": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "data": (create_raw_matrix(raw), np.array([x.abstotal for x in raw]))
    }
    return dataset

def analyze_dataset(dataset: dict, model: TSDataModel):
    """Analyze a given dataset using a model.

    The analysis utility will split the data to training and testing data with an 80/20 split and
        selects an appropriate model to predict the total project commit values. The utility will
        also make a graph plot saved to where this function is called from.

    Arguments:
        dataset (tuple): A dictionary that represents the repository dataset to use for analysis.
        model (TSDataModel): The data model type to use.
    """
    X, y = dataset["data"] #pylint:disable=invalid-name
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0) #pylint:disable=invalid-name
    logging.info("Dataset split to training and test sets. Sizes: %s (train), %s (test)",
                 X_train.shape[0],
                 X_test.shape[0])

    if model == TSDataModel.LINEAR:
        logging.info("Linear model selected. Creating a regression model...")
        a_model = LinearRegression()
    elif model == TSDataModel.NEURAL:
        logging.info("Neural network model selected. Creating a regression model...")
        a_model = MLPRegressor(solver="lbfgs",
                               alpha=0.001,
                               hidden_layer_sizes=(10, 2),
                               max_iter=5000,
                               random_state=None)
    elif model == TSDataModel.FOREST:
        logging.info("Random forest model selected. Creating a regression model...")
        a_model = RandomForestRegressor(random_state=None)
    else:
        raise TSDataAnalysisError("Invalid model selected: %s." % (model))

    a_model.fit(X_train, y_train)
    logging.info("Model fitted to training data.")
    logging.info("Applying testing data...")
    predictions = a_model.predict(X_test)
    logging.info("Predicted total commits from testing data: %s.", predictions)

    data_mse = mean_squared_error(y_test, predictions)
    logging.info("Model predicted test data with a MSE of %s. ", data_mse)

    data_r2_score = r2_score(y_test, predictions)
    if data_r2_score < 0.7:
        logging.log(logging.WARN, "Model accuracy is less than 75 percent;" #pylint:disable=logging-not-lazy
                    + " the current model scores with %s percent accuracy.",
                    round(data_r2_score * 100, 2))
    else:
        logging.info("Model predicted test data with a R2 score of %s percent.",
                     round(data_r2_score * 100, 2))

    logging.info("Creating a regression plot...")
    labels = [x.split("/")[1] for x in dataset["targets"][(-1 * X_test.shape[0]):]]
    try:
        plt.scatter(np.arange(X_test.shape[0]), y_test, color="black")
        plt.plot(np.arange(X_test.shape[0]), predictions)
        plt.ylabel("Total project commits")
        plt.xlabel("Projects")
        plt.xticks(np.arange(X_test.shape[0]),
                   labels,
                   rotation=90)
        plt.tight_layout()
        plt.rcParams.update({
            'font.size': 10
        })
        plt.savefig("sparkle_analytics_%s.png" % (model.name))
        plt.clf()
        logging.info("Saved figure to sparkle_analytics_%s.png", model.name)
    except Exception as error:
        logging.error("Couldn't generate regression plot: %s", error)
