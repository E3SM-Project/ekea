.. _kernel-extract:

==========================
Extracting a E3SM kernel
==========================

Following sections explain how to extract a kernel from MPAS Ocean model using **ekea**. The same method can be used to extract a kernel from EAM model.

Step 0. create a E3SM case
----------------------------

Before preceeding, please make sure that you have cloned E3SM repository on the system where you run ekea.

Once you have E3SM repository on your system, tries to checkout an ekea tutorial branch on E3SM github.

.. code-block:: bash

        >>> git checkout ykim/crusher/ekea

The example on this branch is tested on a system (Crusher of Oak Ridge National Laboratory) and most of explanations here should be applicable to other systems too.

The E3SM case used in this example is as following:

.. code-block:: bash

        E3SM="/my/E3SM"
        OUTROOT="my/outdir"
        RES="T62_oQU120"
        COMPSET="CMPASO-NYF"
        CASEDIR="${OUTROOT}/${RES}.${COMPSET}"
        ACCOUNT="myaccount"
        MACHINE="mymachine"
        COMPILER="gnu"

        ${E3SM}/cime/scripts/create_newcase \
                --case "${CASEDIR}" \
                --res ${RES} \
                --compset ${COMPSET}  \
                --machine ${MACINE} \
                --compiler {COMPILER} \
                --project ${ACCOUNT} \
                --output-root "${OUTROOT}"


Step 1. mark the kernel region with ekea directives in source file
----------------------------------------------------------------------------

Next thing to extract a kernel is to specify ekea kernel region in a E3SM source file. In this example, we selected "${E3SM}/components/mpas-ocean/src/shared/mpas_ocn_vel_hadv_coriolis.F". If you checked out "ykim/crusher/ekea" branch, there already exist the directives in the source file as shown below:



#### mpas_ocn_vel_hadv_coriolis.F#####

.. code-block:: fortran

        module ocn_vel_hadv_coriolis

        ...

        subroutine ocn_vel_hadv_coriolis_tend(normRelVortEdge, &
              normPlanetVortEdge, &
              layerThickEdgeFlux, normalVelocity, &
              kineticEnergyCell, tend, err)

        ...   

        !*** allocate and transfer temporary arrays

        allocate(tmpVorticity(nVertLevels,nEdgesAll), &
                               qArr(nVertLevels,nEdgesAll))

        !!!!!!!! begin ekea kernel region !!!!!
        !$kgen begin_callsite mpas_ocn_coriolis
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        !$acc enter data create(tmpVorticity, qArr)

        #ifndef MPAS_OPENACC
              !$omp parallel
        #endif
              if (usePlanetVorticity) then

        ...

                 do k = kmin, kmax
                    tend(k,iEdge) = tend(k,iEdge) + &
                                edgeMask(k,iEdge)* (qArr(k,iEdge) - &
                                   (kineticEnergyCell(k,cell2) &
                                  - kineticEnergyCell(k,cell1))*invLength)
                 end do
              end do
        #ifndef MPAS_OPENACC
              !$omp end do
              !$omp end parallel
        #endif

        !!!!!!!! end ekea kernel region !!!!!
        !$kgen end_callsite mpas_ocn_coriolis
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        !$acc exit data delete(tmpVorticity, qArr)
        deallocate(qArr,tmpVorticity)

        call mpas_timer_stop("coriolis")

        end subroutine ocn_vel_hadv_coriolis_tend

        ...

        end module ocn_vel_hadv_coriolis

The essential lines for kernel extraction in the above example are the lines starts with "!$kgen". The two directives should be in the same block level. For example, the following cases are **NOT** allowed:

* "begin_callsite" is located outside of a DO Fortran block while "end_callsite" is inside of the Do block.
* "begin_callsite" is located inside of a subroutine while "end_callsite" is inside of another subroutine.

Step 2. run ekea
--------------------

Once you specified ekea kernel region with "begin_callsite" and "end_callsite" directives, you can run ekea command to extract a kernel as shown below:

.. code-block:: bash

        >>> ekea ocn 
                ${CASEDIR} \
                ${E3SM}/components/mpas-ocean/src/shared/mpas_ocn_vel_hadv_coriolis.F
                -o ${CASEDIR}/ekea \
                --no-batch

"-o" option specifies the directory path for ekea to generate output files.
"--no-batch" allows to use an interactive node instead of submitting a job to a job scheduler"

Step 3. check screen output messages during kernel extraction
---------------------------------------------------------------

Kernel extraction on ekea goes through multiple stages.

* ekea starts
* collecting E3SM case information
* collecting compiler flags used for compiling E3SM source files
* analyzing E3SM source codes.
* generating kernel timing data
* generating a suite of kernel files.
* generating binary data to drive execution of the extracted kernel.
* ekea ends

When an error occurs during ekea kernel extraction, it is helpful to know which stage ekea stops. For details of ekea screen messages, please see :ref:`ekea-message`.


Step 4. check extracted kernel source files and data files
---------------------------------------------------------------

Once completed kernel extraction successfully, kernel directory will be created in the output directory with source files, data files, and a Makefile. Please see :ref:`ekea-output` for the details of output files.

The following shows the files generated in kernel subdirector of this example.

.. code-block:: bash

        >> ls -l ${CASEDIR}/ekea/kernel

        kernel_driver.f90
        kgen_statefile.lst
        kgen_utils.f90
        Makefile
        mpas_derived_types.f90
        mpas_kind_types.f90
        mpas_ocn_config.f90
        mpas_ocn_mesh.f90
        mpas_ocn_vel_hadv_coriolis.f90
        mpas_ocn_coriolis.0.0.1
        mpas_ocn_coriolis.11.0.1
        ...
 
In addition to the files copied from E3SM source files, there exists several other files:

* kernel_driver.f90   : has Fortran "PROGRAM" statement
* kgen_utils.f90      : has kgen utility functions
* Makefile            : has convinient make targets for build and run the extracted kernel
* mpas_ocn_coriolis.* : binary data files generated from running E3SM
* kgen_statefile.lst  : will be generated when you run the kernel the first time.
                        Each line has a path to a binary data file to be used.

Step 4. compiling and running a kernel
---------------------------------------------------------------

To compile the kernel, go to kernel subdirectory and run make command as shown below:

.. code-block:: bash

        >>> make

        /opt/cray/pe/gcc/11.2.0/bin/../snos/bin/gfortran -march=znver3 -mcmodel=medium -fconvert=big-endian -ffree-line-length-none -ffixed-line-length-none -fallow-argument-mismatch -O -O2 -c -o kgen_utils.o kgen_utils.f90
        /opt/cray/pe/gcc/11.2.0/bin/../snos/bin/gfortran -march=znver3 -mcmodel=medium -fconvert=big-endian -ffree-line-length-none -ffixed-line-length-none -fallow-argument-mismatch -O -O2 -c -o kgen_utils.o kgen_utils.f90
        /opt/cray/pe/gcc/11.2.0/bin/../snos/bin/gfortran -march=znver3 -mcmodel=medium -fconvert=big-endian -ffree-line-length-none -ffixed-line-length-none -fallow-argument-mismatch -O -O2 -c -o mpas_kind_types.o mpas_kind_types.f90
        /opt/cray/pe/gcc/11.2.0/bin/../snos/bin/gfortran -march=znver3 -mcmodel=medium -fconvert=big-endian -ffree-line-length-none -ffixed-line-length-none -fallow-argument-mismatch -O -O2 -c -o mpas_derived_types.o mpas_derived_types.f90
        /opt/cray/pe/gcc/11.2.0/bin/../snos/bin/gfortran -march=znver3 -mcmodel=medium -fconvert=big-endian -ffree-line-length-none -ffixed-line-length-none -fallow-argument-mismatch -O -O2 -c -o mpas_ocn_mesh.o mpas_ocn_mesh.f90
        /opt/cray/pe/gcc/11.2.0/bin/../snos/bin/gfortran -march=znver3 -mcmodel=medium -fconvert=big-endian -ffree-line-length-none -ffixed-line-length-none -fallow-argument-mismatch -O -O2 -c -o mpas_ocn_config.o mpas_ocn_config.f90
        /opt/cray/pe/gcc/11.2.0/bin/../snos/bin/gfortran -march=znver3 -mcmodel=medium -fconvert=big-endian -ffree-line-length-none -ffixed-line-length-none -fallow-argument-mismatch -O -O2 -c -o mpas_ocn_vel_hadv_coriolis.o mpas_ocn_vel_hadv_coriolis.f90
        /opt/cray/pe/gcc/11.2.0/bin/../snos/bin/gfortran -march=znver3 -mcmodel=medium -fconvert=big-endian -ffree-line-length-none -ffixed-line-length-none -fallow-argument-mismatch -O -O2 -c -o kernel_driver.o kernel_driver.f90
        /opt/cray/pe/gcc/11.2.0/bin/../snos/bin/gfortran -march=znver3 -mcmodel=medium -fconvert=big-endian -ffree-line-length-none -ffixed-line-length-none -fallow-argument-mismatch -O -O2 -o kernel.exe mpas_ocn_vel_hadv_coriolis.o mpas_ocn_mesh.o mpas_ocn_config.o mpas_derived_types.o mpas_kind_types.o kernel_driver.o kgen_utils.o

To improve reproducibility, Makefile uses the same compiler flags used to compile the E3SM source files during E3SM compilation.


To run the kernel, run following make command:

.. code-block:: bash

        >>> make run

        /opt/cray/pe/gcc/11.2.0/bin/../snos/bin/gfortran -march=znver3 -mcmodel=medium -fconvert=big-endian -ffree-line-length-none -ffixed-line-length-none -fallow-argument-mismatch -O -O2 -o kernel.exe mpas_ocn_vel_hadv_coriolis.o mpas_ocn_mesh.o mpas_ocn_config.o mpas_derived_types.o mpas_kind_types.o kernel_driver.o kgen_utils.o
        ./kernel.exe

        ***************** Verification against 'mpas_ocn_coriolis.45.0.1' *****************

        Number of output variables:           14
        Number of identical variables:           13
        Number of non-identical variables within tolerance:            1
        Number of non-identical variables out of tolerance:            0
        Tolerance:    1.0000000000000000E-014

        Verification PASSED with mpas_ocn_coriolis.45.0.1

        mpas_ocn_coriolis : Time per call (usec):    1322.9690000000001

        ...

        ****************************************************
            kernel execution summary: mpas_ocn_coriolis
        ****************************************************
            Total number of verification cases  :    40
            Number of verification-passed cases :    40

            kernel: mpas_ocn_coriolis: PASSED verification

            number of processes  1

            Average call time (usec):  0.120E+04
            Minimum call time (usec):  0.824E+03
            Maximum call time (usec):  0.143E+04
        ****************************************************

Running the extracted kernel displays verfication and timing information of the execution. Please see :ref:`kernel-output` for details.


Step 5. using the kernel
---------------------------------------------------------------

The extracted kernel is a stand-alone software that can be compiled and run without using MPI nor batch system. Therefore, at this point, it is upto users to decide what to do with the extracted kernel.

If you want to modify source code of the kernel, it is generally good idea to start looking at the call site file that you specified in ekea command line, "mpas_ocn_vel_hadv_coriolis.f90" in this example.
