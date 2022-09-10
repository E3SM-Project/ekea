#!/usr/bin/bash

CASEDIR=/ccs/home/grnydawn/prjcli133/e3sm_scratch/crusher/F2010_ne4pg2_oQU480_gnu_crusher_
CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/eam/src/physics/rrtmg/radlw.F90
OUTDIR=${CASEDIR}/ekea

ekea eam $CASEDIR $CALLSITEFILE -o $OUTDIR
