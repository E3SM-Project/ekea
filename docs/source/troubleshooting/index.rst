.. _commands-trouble:


=============================
Troubleshootings
=============================

The execution of ekea consists of several consecutive steps.

.. image:: ../_static/ekea-steps.png

After completion, some steps produce intermittent outputs as shown above.

The basic approach to resolve issues during kernel extraction is to identify which step went wrong by locating those intermittent outputs.

ekea checks if those intermittent outputs exist. If so, ekea skip the steps required to generate the outputs. For some reason, if you do not want to skip those steps, just remove the output files.

Checking compile.json
============================

"compile.json" is one of the output files that **ekea** generates to save E3SM compilation information. In the Json file, following information is saved per every source file that is compiled during E3SM build.

* path to the source file
* include directories
* macro definitions
* openmp compiler flag
* other compiler flags
* path to the backup of the source file

If you can see the "compile.json" file in the kernel output directory, that means that **ekea** drives the compilation of E3SM and collected the information successfully.

If there is not "compile.json" in the directory, you may want to check following items:

* case directory and target source file path in ekea command line
* kernel marking in the target source file
* The E3SM case itself should not have an issue of building

Checking model.json
============================

"model.ini" is one of the output files that **ekea** generates to save the elapsed time of running the specified kernel code. In the Ini file, following information is saved per every execution of the kernel code.

* start clock and stop clock of the kernel code
* MPI rank, OpenMP thread id, and the order of invocation

This timing information is analyzed by ekea internally and generates a set of triplets with MPI rank, OpenMP thread id, and the order of invocation that maximally represents the timing characteristics of the original E3SM execution.

Following list explains causes of failure and corresponding possible fixes if there is not "compile.json" in the directory.

* ekea could not generate instrumented source files for timing generation.
   - check the etime subdirectory at the output directory. If you can see one Makefile and one or more source files, that indicates that ekea generated instrumented source files.
* ekea could not generate raw timing data
   - ekea compiles E3SM with the instrumented source file(s). Users can manually generate the raw timing data by running "make recover; make" in the etime subdirectory. You may check the E3SM log files for what went wrong.
   - If raw timing data generated successfully, you can see many subdirectories under model subdirectory with many files whose name is just a number and contains raw timing data. If you can see the files but not model.ini, then try to run ekea again



Checking kernel and data
============================

"kernel" subdirectory at the output directory contains all kernel files, data files, and one Makefile. If kernel extraction is successful, you can build and run the kernel by running "make build; make run".

In many kernel extraction cases, the most challenging part is to generate data files. the names of data files are "<kernel_name>.<mpi rank>.<openmp thread number>.<invocation order>". 

ekea generates instrumented source files to generate data files and build & run E3SM with the instrumented files. You may manually build & run E3SM with the instrumented file by running "make recover; make run" iin "state" subdirectory. You may want to the E3SM log files if you see some error message during the E3SM build & run.

