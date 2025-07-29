#!/usr/bin/env python
###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

import sys

from DIRAC.Core.Base.Script import Script


@Script()
def main():
    Script.parseCommandLine()

    import DIRAC

    transIDs = []
    if len(sys.argv) < 2:
        print("Usage: dirac-transformation-clean transID [transID] [transID]")
        DIRAC.exit(1)
    else:
        try:
            transIDs = [int(arg) for arg in sys.argv[1:]]
        except Exception:
            print("Invalid list of transformations")
            DIRAC.exit(1)

    from LHCbDIRAC.TransformationSystem.Agent.TransformationCleaningAgent import TransformationCleaningAgent

    agent = TransformationCleaningAgent(
        "Transformation/TransformationCleaningAgent",
        "Transformation/TransformationCleaningAgent",
        "dirac-transformation-clean",
    )
    agent.initialize()

    for transID in transIDs:
        agent.cleanTransformation(transID)


if __name__ == "__main__":
    main()
