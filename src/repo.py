#
# Repository Information
# GitHub Machine Learning Project
# (C) 2020 Marquis Kurt
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from src.commit import GHCommitWeek

class GHRepositoryWeeksum:
    def __init__(self, name, author, total, abstotal, weeksum):
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

    def to_dict(self):
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