#!/usr/bin/bash

CASEDIR=/ccs/home/grnydawn/workbench/E3SM/case
CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/cam/src/physics/cam/micro_mg_cam.F90
#OUTDIR=/ccs/home/grnydawn/scratch/kernels/eam/ekgen_eam1
OUTDIR=/gpfs/alpine/cli115/proj-shared/grnydawn/e3sm_scratch/ekgen_eam1

ekea eam $CASEDIR $CALLSITEFILE -o $OUTDIR
