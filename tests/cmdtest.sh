#!/bin/bash

#CASEDIR=/gpfs/alpine/cli115/proj-shared/grnydawn/e3sm_scratch/ERS_Ld5.T62_oQU120.CMPASO-NYF.summit_pgi.20210125_094617_kmwz7r
#CASEDIR=/gpfs/alpine/cli115/proj-shared/grnydawn/e3sm_scratch/ERS_Ld5.T62_oQU120.CMPASO-NYF.summit_pgi.20210429_162740_1b4b5n
CASEDIR=/gpfs/alpine/cli133/proj-shared/grnydawn/e3sm_tests/crusher_gnu/SMS_R_Ld5.ne4_ne4.FSCM5A97.crusher_gnu.eam-scm.20220130_203636_8yrdon
##CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_diagnostics.F
#CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_diagnostics.F
#ekgen_3 success CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/mode_forward/mpas_ocn_time_integration_split.F
#CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-ocean/src/mode_forward/mpas_ocn_time_integration_split.F
CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/eam/src/physics/cam/micro_mg_cam.F90
#CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/mode_forward/mpas_ocn_time_integration_split.F
#ekgen_4 no model CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_high_freq_thickness_hmix_del2.F
#ekgen_5 success CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_surface_bulk_forcing.F
#ekgen_6 success CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_vel_hadv_coriolis.F
#ekgen_7 success CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_vel_vadv.F
#ekgen_8 no model CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_tidal_potential_forcing.F
#ekgen_9 error allocation? CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_vel_pressure_grad.F
#ekgen_10 no model CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_vel_hmix_del2.F
#ekgen_12 success CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_thick_hadv.F
#ekgen_13 derived type failure pooling CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_surface_bulk_forcing.F
#ekgen_14 no model CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_tracer_ecosys.F
#ekgen_15 no model CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_tracer_DMS.F
#ekgen_16 no model CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_tracer_MacroMolecules.F
#CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_tracer_surface_flux_to_tend.F
#OUTDIR=/ccs/home/grnydawn/scratch/kernels/ocn/ekgen_2
#OUTDIR=/ccs/home/grnydawn/scrcli115/kernels/ocn/ekgen_release

OUTDIR=/ccs/home/grnydawn/prjcli133/kernels/eam/mixedprectest

ekea mpasocn $CASEDIR $CALLSITEFILE -o $OUTDIR
