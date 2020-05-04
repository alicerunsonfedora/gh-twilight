#
# Repository Information
# GitHub Machine Learning Project
# (C) 2020 Marquis Kurt
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

"""The repo submodule contains the data structure for a repository for analysis."""
from gh_twilight.commit import GHCommitWeek

class GHRepositoryWeeksum:
    """A class representation of a repository with commit counts.

    Attributes:
        name (str): The name of the repository.
        author (str): The Git author that made the commits in weeksum.
        total (int): The total number of commits made by the Git author to the repository.
        abstotal (int): The total nomber of commits to the repository.
        weeksum (GHCommitWeek): The data structure that represents the commit week.
    """

    def __init__(self, name: str, author: str, total: int, abstotal: int, weeksum: list):
        """Initialize a GHRepositoryWeeksum data structure.

        Args:
            name (str): The name of the repository.
            author (str): The Git author that made the commits in weeksum.
            total (int): The total number of commits made by the Git author to the repository.
            abstotal (int): The total nomber of commits to the repository.
            weeksum (list): The list of integers that represent the commit week.
        """
        self.name = name
        self.author = author
        self.total = total
        self.abstotal = abstotal
        self.weeksum = GHCommitWeek(weeksum)

    def __str__(self):
        return """Name: %s
Filtered by author: %s
Total project commits: %s
Total commits by author: %s
Total commits per weekday:
    Sunday: %s
    Monday: %s
    Tuesday: %s
    Wednesday: %s
    Thursday: %s
    Friday: %s
    Saturday: %s""" % (self.name,
                       self.author,
                       self.abstotal,
                       self.total,
                       self.weeksum.sunday(),
                       self.weeksum.monday(),
                       self.weeksum.tuesday(),
                       self.weeksum.wednesday(),
                       self.weeksum.thursday(),
                       self.weeksum.friday(),
                       self.weeksum.saturday())

    def to_dict(self) -> dict:
        """Get a serialized dictionary of the repo data.

        Returns:
            data (dict): A dictionary containing the repository data.
        """
        return {
            "name": self.name,
            "total_count": self.total,
            "absolute_total_count": self.abstotal,
            "weeksum": {
                "author": self.author,
                "week": self.weeksum.to_list()
            }
        }
