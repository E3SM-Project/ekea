#!/usr/bin/bash

# Step 1: Clone E3SM: https://github.com/E3SM-Project/E3SM.git
#         and checkout "ykim/crusher/ekea" branch for testing

# Step 2: Change E3SMDIR and CASEBASE for your testing
E3SMDIR=/autofs/nccs-svm1_home1/grnydawn/repos/github/E3SM
CASEBASE=/gpfs/alpine/cli133/proj-shared/grnydawn/e3sm_scratch/crusher_gnu_ekeatest

# Step 3: Create a case. In this example CMPASO-NYF compset, T62_oQU120 grid,
#         and gnu compiler is used on Crusher system
CASEDIR=${CASEBASE}/ne4_oQU240.F2010
CALLSITEFILE=${E3SMDIR}/components/eam/src/physics/clubb/mixing_length.F90
OUTDIR=${CASEDIR}/ekea

# Step 4: Run ekea ocn command. Note: remove --no-batch to use batch system
ekea eam $CASEDIR $CALLSITEFILE -o $OUTDIR --no-batch
