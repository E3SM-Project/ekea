#!/usr/bin/bash

# Step 1: Clone E3SM: https://github.com/E3SM-Project/E3SM.git
#         and checkout "ykim/crusher/ekea" branch for testing

# Step 2: Change E3SMDIR and CASEBASE for your testing
E3SMDIR=/autofs/nccs-svm1_home1/grnydawn/repos/github/E3SM
CASEBASE=/gpfs/alpine/cli133/proj-shared/grnydawn/e3sm_scratch/crusher_gnu_ekeatest

# Step 3: Create a case. In this example CMPASO-NYF compset, T62_oQU120 grid,
#         and gnu compiler is used on Crusher system
CASEDIR=${CASEBASE}/T62_oQU120.CMPASO-NYF
CALLSITEFILE=${E3SMDIR}/components/mpas-ocean/src/shared/mpas_ocn_gm.F
OUTDIR=${CASEDIR}/ekea_gm

# Step 4: Run ekea ocn command. Note: remove --no-batch to use batch system
ekea ocn $CASEDIR $CALLSITEFILE -o $OUTDIR --no-batch --include-ini /ccs/home/grnydawn/repos/github/ekea/tests/include_gm.ini
