#!/bin/bash

CASEDIR=/gpfs/alpine/cli115/proj-shared/grnydawn/e3sm_scratch/ERS_Ld5.T62_oQU120.CMPASO-NYF.summit_pgi.20210706_140224_pvykcp
#CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_gm.F
#CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_diagnostics.F
CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/mode_forward/mpas_ocn_time_integration_split.F
OUTDIR=/ccs/home/grnydawn/scrcli115/kernels/ocn/varlist
ekea varwhere $CASEDIR $CALLSITEFILE -o $OUTDIR
