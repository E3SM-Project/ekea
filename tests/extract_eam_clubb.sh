#!/usr/bin/bash

CASEDIR=/gpfs/alpine/cli133/proj-shared/grnydawn/e3sm_scratch/crusher_gnu_ekeatest/ne4_oQU240.F2010
CALLSITEFILE=/autofs/nccs-svm1_home1/grnydawn/repos/github/E3SM/components/eam/src/physics/clubb/mixing_length.F90
OUTDIR=${CASEDIR}/ekea

ekea eam $CASEDIR $CALLSITEFILE -o $OUTDIR --no-batch
