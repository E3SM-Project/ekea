.. _ekea-output:

************************************
ekea output files and directories
************************************

ekea creates several directories and generates files in the directories during kernel extraction . The next section explains the generated files in the kernel subdirectory. And the following sections explains all other directories and files other than the kernel directory.

Files in kernel directory
--------------------------------------------------------

Kernel source files
************************

Files whose extension is f90. The entry of the program is in "kernel_driver.f90"

Kernel binary data files
************************

Files whose name ends with ###.###.### where # represents one or more digit numbers (example: mpas_ocn_coriolis.0.0.1). Each of these files is a set of one kernel invocation.

Makefile file
************************

This is an auto-generated makefile to compile and run this kernel. This file makes it easy to build and run the kernel. The useful Makefile targets are built to build the kernel and run to run the kernel.


kgen_statefile.lst
************************

This file contains a name of kernel data files to be used for kernel execution. One file name is allowed per each line. This file is generated from running the kernel for the first time.


Directories and files in ekea output directory
--------------------------------------------------------

kernel directory
************************

Explained in the above section

compile.json file
************************

This JSON file contains compilation information of E3SM: compiler used, compiler options, MACROS defined, and temporary backup of dynamically generated files.

model.json file
************************

This JSON file contains kernel timing measurement information: kernel region wall-time per MPI rank, OpenMP thread, and invocation order.


backup directory
************************

This directory contains all the E3SM source files compiled during E3SM compilation. These backed-up files can be used in the case that the files are dynamically generated and deleted before completion of compilation.

etime directory
************************

This directory contains instrumented source files for kernel wall-time generation.

model directory
************************

This directory contains kernel timing raw measurements.


state directory
************************

This directory contains instrumented source files for kernel data generation.

