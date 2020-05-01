#
# Main Entry Point
# GitHub Machine Learning Project
# (C) 2020 Marquis Kurt
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

import os
from src.data import GithubMLDataCollector

def main():
    # Get the list of repos that I want to sample here.
    repos = [
        "UnscriptedVN/game",
        "Sayo-nika/Frontend",
        "hyperspacedev/hyperspace",
        "hyperspacedev/hyperspace-classic",
        "projectalicedev/aliceos",
        "projectalicedev/the-angel-returns",
        "alicerunsonfedora/portal-jam",
        "alicerunsonfedora/ocellusscript",
        "alicerunsonfedora/pacman-enrichment-center",
        "alicerunsonfedora/imagenes",
        "alicerunsonfedora/camino",
        "alicerunsonfedora/alcayde-redemption-class",
        "TerminaGame/mac",
        "TerminaGame/base",
    ]

    # Exit out of the function if we don't have the GitHub token set.
    if "GH_TOKEN" not in os.environ:
        print("Missing GH_TOKEN key in environment. Aborting.")
        return

    # Initialize the collector
    gh = GithubMLDataCollector(os.environ["GH_TOKEN"])

    # Get the dataset and go through every repo in the list to get its data.
    dataset = []
    for repo in repos:
        print("Processing " + repo)
        dataset.append(gh.get_weeksum(repo, by_author="Marquis Kurt").to_dict())

if __name__ == "__main__":
    main()