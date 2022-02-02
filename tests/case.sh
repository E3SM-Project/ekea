#!/bin/bash
  
set -e

# Created 2021-09-20 16:06:17

CASEDIR="/gpfs/alpine/cli133/scratch/grnydawn/e3sm_scratch/ekeatest2"

/gpfs/alpine/cli133/scratch/grnydawn/repos/github/E3SM/cime/scripts/create_newcase --case "${CASEDIR}" --compset F1850 --res ne4_ne4 --machine spock --compiler gnu --project cli133

cd "${CASEDIR}"

./case.setup
