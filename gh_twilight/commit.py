#
# Commit Week
# GitHub Machine Learning Project
# (C) 2020 Marquis Kurt
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
"""The commit submodule contains the data structure for a week in commits."""
class GHCommitWeek:
    """The class representation of a week's worth commits in Github."""

    def __init__(self, days):
        """Construct a commit week.

        Arguments:
            days (list): A list containing integer values that correspond to how many commits were pushed on each day of
                the week.
        """
        if len(days) != 7:
            raise ValueError("List is required to have seven values. Got %s instead." % (len(days)))
        self._days = days

    def sunday(self) -> int:
        """Get the number of commits on Sunday.

        Returns:
            commits (int): The number of commits on Sunday.
        """
        return self._days[0]

    def monday(self) -> int:
        """Get the number of commits on Monday.

        Returns:
            commits (int): The number of commits on Monday.
        """
        return self._days[1]

    def tuesday(self) -> int:
        """Get the number of commits on Tuesday.

        Returns:
            commits (int): The number of commits on Tuesday.
        """
        return self._days[2]

    def wednesday(self) -> int:
        """Get the number of commits on Wednesday.

        Returns:
            commits (int): The number of commits on Wednesday.
        """
        return self._days[3]

    def thursday(self) -> int:
        """Get the number of commits on Thursday.

        Returns:
            commits (int): The number of commits on Thursday.
        """
        return self._days[4]

    def friday(self) -> int:
        """Get the number of commits on Friday.

        Returns:
            commits (int): The number of commits on Friday.
        """
        return self._days[5]

    def saturday(self) -> int:
        """Get the number of commits on Saturday.

        Returns:
            commits (int): The number of commits on Saturday.
        """
        return self._days[6]

    def average(self) -> int:
        """Get the average number of commits in this week.

        Returns:
            average (int): The average number of commits in this week.
        """
        return sum(self._days) / len(self._days)

    def to_list(self):
        """Get the week as a list of numbers.

        Returns:
            commits (list): A list of integers for the commits in the week.
        """
        return self._days