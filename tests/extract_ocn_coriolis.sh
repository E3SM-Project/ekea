#!/usr/bin/bash

CASEDIR=/gpfs/alpine/cli133/proj-shared/grnydawn/e3sm_scratch/crusher_gnu_ekeatest/T62_oQU120.CMPASO-NYF
CALLSITEFILE=/autofs/nccs-svm1_home1/grnydawn/repos/github/E3SM/components/mpas-ocean/src/shared/mpas_ocn_vel_hadv_coriolis.F
OUTDIR=${CASEDIR}/ekea

ekea ocn $CASEDIR $CALLSITEFILE -o $OUTDIR --no-batch
