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
import numpy as np
from gh_twilight.repo import GHRepositoryWeeksum

class TSDatasetGenerateError(Exception):
    """Could not create the analysis dataset."""

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
        data (tuple): A tuple containing the weekly commits (x) and the total commits by the author
            specified in the repository (y).
    """
    x_data = create_raw_matrix(raw)
    y_data = np.array([x.total for x in raw])
    return x_data, y_data
