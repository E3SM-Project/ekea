#!/usr/bin/env bash

CASEDIR=/gpfs/alpine/cli133/scratch/grnydawn/e3sm_scratch/ekeatest2 
#CALLSITE=/ccs/home/grnydawn/scrcli133/repos/github/E3SM.pr/components/mpas-ocean/src/mode_forward/mpas_ocn_time_integration_split.F
CALLSITE=/ccs/home/grnydawn/scrcli133/repos/github/E3SM/components/eam/src/physics/cam/micro_mg_cam.F90

#ekea mpasocn $CASEDIR  $CALLSITE -o $CASEDIR/kernel
ekea eam $CASEDIR  $CALLSITE -o $CASEDIR/kernel
