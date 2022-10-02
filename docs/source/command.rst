.. _ekea-command:

==========================
ekea command-line syntax
==========================

Following shows ekea eam command line syntax.

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
          --no-batch            Do not submit jobs to batch system, run locally

<Example> ::
        >>> ekea mpasocn \
            /path/to/my/case \
            $E3SM/components/mpas-ocean/src/shared/mpas_ocn_vel_hadv_coriolis.F \
            -o /path/to/output

As of this version, there exist two subcommands of "ocn" and "eam" for MPAS Ocean Model and E3SM Atmospheric Model each.

-o, --outdir OUTDIR
-------------------------

With this option specified with OUTDIR path, all of ekea outputs will be created under the path.

-m, --mpidir MPIDIR
-------------------------

This option specifies the root of MPI directory used for building E3SM executable. This option may be used in case that user gets an ekea error related to not finding MPI parameters.

--no-batch
-------------------------

This option add "--no-batch" option to "case.submit" command allowing building and running E3SM on an interactive node, insteads of submitting a job to a job scheduler.
