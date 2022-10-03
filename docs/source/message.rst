.. _ekea-message:

*************************************
ekea screen messages
*************************************

During kernel extraction, ekea displays important messages on the terminal screen. The messages show what ekea is currently working on during one of the following stages:

* ekea starts
* collecting E3SM case information
* collecting compiler flags used for compiling E3SM source files
* analyzing E3SM source codes.
* generating kernel timing data
* generating a suite of kernel files.
* generating binary data to drive execution of the extracted kernel.
* ekea ends


ekea screen messages
******************************************************************************

This section introduces the details of screen output messages.

::

        ==== Kernel extraction is started. (ocn) ====
        Displays information collected from E3SM test case

        ==== Collecting compiler flags (cd /.../T62_oQU120.CMPASO-NYF; ./case.build) ====
        In this stage, ekea collects compiler options used to compile E3SM source files
        Displays the status message of collecting compiler options and informative messages about the task 
        ==== Analyzing source codes ====
        In this stage, ekea analyze source codes based on source codes used during compilation.

        ==== Generating timing raw data ====
        In this stage, ekea instrument source code to generate kernel elapsed time.
        With the instrumentation, ekea rebuild and run E3SM.

        ==== Collecting timing data ====
        In this stage, ekea selects MPI ranks, OpenMP threads (if used), and the invocation orders to maximize the representativeness in the extracted kernel
        Displays histogram information of measured kernel elapsed time.

        ==== Generating kernel files (/.../T62_oQU120.CMPASO-NYF/ekea/kernel) ====
        In this stage, ekea generate kernel files.
        Displays a list of kernel files

        ==== Generating state data files (/.../T62_oQU120.CMPASO-NYF/ekea/kernel) ====
        ekea instrument E3SM source files to generate binary data files.
        With the instrumentation, ekea rebuild and run E3SM.

        ==== Kernel extraction is finished. (ocn) ====


An example screen messages
******************************************************************************

This section captures the screen messages from extracting a kernel from mpas_ocn_vel_hadv_coriolis.f90.

::

        ==== Kernel extraction is started. (ocn) ====
        [Case directory] = /.../T62_oQU120.CMPASO-NYF
        [Callsite file] = /.../T62_oQU120.CMPASO-NYF/bld/cmake-bld/core_ocean/shared/mpas_ocn_vel_hadv_coriolis.f90
        [Output directory] = /.../T62_oQU120.CMPASO-NYF/ekea
        [Batch system] = slurm
        [MPI directory] = /opt/cray/pe/mpich/8.1.16/ofi/crayclang/10.0
        ==== Collecting compiler flags (cd /.../T62_oQU120.CMPASO-NYF; ./case.build) ====
        [Source backup directory] = /.../T62_oQU120.CMPASO-NYF/ekea/backup/src
        [Info] processed 100 source files
        [Info] processed 200 source files
        [Info] processed 300 source files
        [Info] /.../T62_oQU120.CMPASO-NYF/shr_infnan_mod.F90 is not saved in backup directory.
        [Info] /.../T62_oQU120.CMPASO-NYF/shr_infnan_mod.F90 is not saved in backup directory.
        [Info] processed 400 source files
        [Info] /.../T62_oQU120.CMPASO-NYF/shr_assert_mod.F90 is not saved in backup directory.
        [Info] /.../T62_oQU120.CMPASO-NYF/shr_frz_mod.F90 is not saved in backup directory.
        [Info] /.../T62_oQU120.CMPASO-NYF/shr_frz_mod.F90 is not saved in backup directory.
        [Info] /.../T62_oQU120.CMPASO-NYF/shr_assert_mod.F90 is not saved in backup directory.
        [Info] processed 500 source files
        [Info] processed 600 source files
        [Info] processed 700 source files
        [Info] processed 800 source files
        [Info] processed 900 source files
        [Info] processed 1000 source files
        [Info] processed 1100 source files
        [Info] processed 1200 source files
        [Info] processed 1300 source files
        [Info] processed 1400 source files
        [Info] processed 1500 source files
        [Info] processed 1600 source files
        [Info] processed 1700 source files
        [Info] processed total 1730 source files
        [Output JOSN file] = /.../T62_oQU120.CMPASO-NYF/ekea/compile.json
        ==== Analyzing source codes ====
        WARNING: '/.../T62_oQU120.CMPASO-NYF/shr_infnan_mod.F90' does not exist. It may cause failure of KGen analysis.
        WARNING: '/.../T62_oQU120.CMPASO-NYF/shr_assert_mod.F90' does not exist. It may cause failure of KGen analysis.
        WARNING: '/.../T62_oQU120.CMPASO-NYF/shr_frz_mod.F90' does not exist. It may cause failure of KGen analysis.
        ==== Generating timing raw data ====
        [timing instrumentation directory] = /.../T62_oQU120.CMPASO-NYF/ekea/etime
        [timing output directory] = /.../T62_oQU120.CMPASO-NYF/ekea/model
        ==== Collecting timing data ====
        From bin # 0 [ 0.001548 (sec) ~ 0.007651 (sec) ] 90.437894 % of 30464
                invocation triple: 46:0:1
                invocation triple: 34:0:1
                invocation triple: 29:0:1
                invocation triple: 28:0:1
                invocation triple: 18:0:1
                invocation triple: 5:0:1
                invocation triple: 1:0:1
                invocation triple: 0:0:1
                invocation triple: 56:0:1
                invocation triple: 42:0:1
                invocation triple: 23:0:1
                invocation triple: 45:0:1
                invocation triple: 24:0:1
                invocation triple: 3:0:1
                invocation triple: 36:0:1
                invocation triple: 55:0:1
                invocation triple: 10:0:1
                invocation triple: 50:0:1
                invocation triple: 26:0:1
                invocation triple: 41:0:1
                invocation triple: 61:0:1
                invocation triple: 58:0:1
                invocation triple: 51:0:1
                invocation triple: 40:0:1
                invocation triple: 27:0:1
                invocation triple: 6:0:1
                invocation triple: 37:0:1
                invocation triple: 8:0:1
                invocation triple: 38:0:1
                invocation triple: 48:0:1
                invocation triple: 63:0:1
                invocation triple: 9:0:1
                invocation triple: 4:0:1
                invocation triple: 49:0:1
                invocation triple: 12:0:1
                invocation triple: 22:0:1
        From bin # 1 [ 0.007651 (sec) ~ 0.013755 (sec) ] 9.401261 % of 30464
                invocation triple: 7:0:2
                invocation triple: 52:0:2
                invocation triple: 37:0:2
                invocation triple: 13:0:2
        From bin # 2 [ 0.013755 (sec) ~ 0.019858 (sec) ] 0.065651 % of 30464
        From bin # 3 [ 0.019858 (sec) ~ 0.025961 (sec) ] 0.036108 % of 30464
        From bin # 4 [ 0.025961 (sec) ~ 0.032065 (sec) ] 0.013130 % of 30464
        From bin # 5 [ 0.032065 (sec) ~ 0.038168 (sec) ] 0.019695 % of 30464
        From bin # 6 [ 0.038168 (sec) ~ 0.044272 (sec) ] 0.009848 % of 30464
        From bin # 7 [ 0.044272 (sec) ~ 0.050375 (sec) ] 0.006565 % of 30464
        From bin # 8 [ 0.050375 (sec) ~ 0.056478 (sec) ] 0.006565 % of 30464
        From bin # 9 [ 0.056478 (sec) ~ ] 0.003283 % of 30464
        Number of bins: 10
        Minimun elapsed time: 0.001548
        Maximum elapsed time: 0.062582
        ==== Generating kernel files (/.../T62_oQU120.CMPASO-NYF/ekea/kernel) ====
        mpas_ocn_vel_hadv_coriolis.f90
        mpas_ocn_mesh.f90
        mpas_ocn_config.f90
        mpas_derived_types.f90
        mpas_kind_types.f90
        kernel_driver.f90
        kgen_utils.f90
        Makefile
        ==== Generating state data files (/.../T62_oQU120.CMPASO-NYF/ekea/kernel) ====
        ==== Kernel extraction is finished. (ocn) ====

