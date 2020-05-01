#
# Data Collector
# GitHub Machine Learning Project
# (C) 2020 Marquis Kurt
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""The data submodule contains the utilities and classes needed to gather data from GitHub."""
import datetime
import logging
from github import Github, Repository, PaginatedList
from gh_twilight.repo import GHRepositoryWeeksum


class GithubMLDataCollector:
    """The base class that represents the data structure for the machine learning data.

     Attributes:
        client (Github): The GitHub client with the requested token login.
    """

    def __init__(self, token: str):
        """Construct a GitHub machine learning structure.

        Arguments:
            token: The access token to sign in to GitHub with.
        """
        self.client = Github(token)
        logging.info("Authentcated with GitHub.")

    def get_weeksum(self, of_repository: str, **kwargs) -> GHRepositoryWeeksum:
        """Get the weekly commits of a given repository.

        Arguments:
            of_repository (str): The repository name to get the commit data for.

        Kwargs:
            by_author (str): The name of the Git commit author to filter by.

        Returns:
            data (GHRepositoryWeeksum): The data structure containing the name, total commit count,
                and the sum of commits in all weeks in a given repository by a given Git commit
                author (or by all authors).
        """
        logging.info("Gathering repository data for %s...", of_repository)
        name = of_repository
        current_repo: Repository = self.client.get_repo(of_repository)
        repo_commits: PaginatedList = current_repo.get_commits()
        t_count = repo_commits.totalCount
        abs_count = repo_commits.totalCount

        week = [0, 0, 0, 0, 0, 0, 0]
        for commit in repo_commits:
            date: datetime.datetime = commit.commit.committer.date
            if "by_author" in kwargs and commit.commit.committer.name != kwargs["by_author"]:
                continue
            week[date.weekday()] += 1

        if "by_author" in kwargs and kwargs["by_author"]:
            t_count = sum(week)
        data = GHRepositoryWeeksum(name,
                                   kwargs["by_author"] if "by_author" in kwargs else "all",
                                   t_count,
                                   abs_count,
                                   week)
        return data
