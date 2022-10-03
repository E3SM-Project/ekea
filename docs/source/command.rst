.. _ekea-command:

==========================
ekea command-line syntax
==========================

Following shows the ekea command line syntax.

::

        usage: ekea <ocn|eam> [-h] [--version] [-o OUTDIR] [-m MPIDIR] [--no-batch]
                              casedir callsitefile

        positional arguments:
          casedir               E3SM case directory
          callsitefile          ekea callsite Fortran source file

        optional arguments:
          -h, --help            show this help message and exit
          --version             show program's version number and exit
          -o, --outdir OUTDIR   output directory
          -m, --mpidir MPIDIR   MPI root directory
          -e, --exclude-ini EXCLUDE_INI
                                information to be excluded for analysis
          -i, --include-ini INCLUDE_INI
                                information to be included for analysis
          --no-batch            Do not submit jobs to batch system, run locally

<Example> ::
        >>> ekea ocn \
            /path/to/my/case \
            $E3SM/components/mpas-ocean/src/shared/mpas_ocn_vel_hadv_coriolis.F \
            -o /path/to/output

As of this version, there exist two subcommands of "ocn" and "eam" for MPAS Ocean Model and E3SM Atmospheric Model each.

-o, --outdir OUTDIR
-------------------------

With this option specified with OUTDIR path, all of ekea outputs will be created under the path.

-m, --mpidir MPIDIR
-------------------------

This option specifies the root of the MPI directory used for building the E3SM executable. This option may be used in case that user gets an ekea error related to not finding MPI parameters.

-e, --exclude-ini EXCLUDE_INI
-------------------------------

This is a INI-format file that specifies a list of names that should be excluded during ekea source file analysis. Please see :ref:`exclude_ini` for details.

-i, --include-ini INCLUDE_INI
-------------------------------

This is a INI-format file that specifies several pieces of information for ekea to include during source file analysis. Please see :ref:`include_ini` for details.

--no-batch
-------------------------

This option adds the "--no-batch" option to the "case.submit" command allowing building and running E3SM on an interactive node, insteads of submitting a job to a job scheduler.
