#!/bin/bash

set -e

# Created 2021-09-20 16:06:17

E3SMDIR="/ccs/home/grnydawn/repos/github/E3SM"
OUTDIR="/gpfs/alpine/cli133/scratch/grnydawn/e3sm_scratch/ekea"
COMPSET="F2010"
GRID="ne4pg2_oQU480"
MACHINE="crusher"
COMPILER="gnu"
PROJECT="cli133"
CASEID="simple"
CASEDIR="${OUTDIR}/${COMPSET}_${GRID}_${COMPILER}_${MACHINE}_${CASEID}"

${E3SMDIR}/cime/scripts/create_newcase \
    --case "${CASEDIR}" \
    --compset ${COMPSET} \
    --res ${GRID}\
    --machine ${MACHINE}\
    --compiler ${COMPILER} \
    --project ${PROJECT}

cd "${CASEDIR}"

./case.setup
