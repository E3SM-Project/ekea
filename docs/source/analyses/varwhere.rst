..  -*- coding: utf-8 -*-

==================================
ekea Kernel Variable Analysis App
==================================

This tool generates variable and function(subroutine) call cross-reference information and puts them in the source code so that user can easily see where variables are defined and being used. This analysis information is particularly useful if the user wants to restructure code for various purposes including GPU porting.

Cross-reference information includes.

* module variables used in functions
* caller sites for functions
* local variables used in the kernel block
* module variables used within the kernel block
* code locations where module variables are referenced

Installation
==============

This app is a default app in ekea. Once ekea is installed, this app will be available.


Usage
============

::

        >>> mkdir ocn_varwhere
        >>> cd ocn_varwhere
        >>> ekea varwhere ${HOME}/scratch/mycase ${HOME}/scratch/E3SM/components/mpas-source/src/core_ocean/mode_forward/mpas_ocn_time_integration_split.F

  
Outputs
============

Once completed successfully, “kernel” directory will be created in the output directory with source files annotated with cross reference information.

::

        !"config_use_redi_surface_layer_tapering" is referenced from namepath of "ocn_gm:ocn_gm_compute_bolus_velocity" near original &
        !line (169, 170)
        !"config_use_redi_surface_layer_tapering" is referenced from namepath of "ocn_gm:ocn_gm_compute_bolus_velocity" near original &
        !line (487, 487)
        logical, pointer :: config_use_Redi_surface_layer_tapering
