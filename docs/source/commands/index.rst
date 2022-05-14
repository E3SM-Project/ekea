.. _commands-index:

==========================
Extracting a E3SM kernel
==========================

User can run the following ekea shell command to extract a E3SM kernel::

        usage: ekea <mpasocn|eam> [-h] [--version] [-o OUTDIR] casedir callsitefile

        casedir
        directory path to E3SM case directory

        callsitefile
        file path to the source file that contains ekea callsite directives

        [-o OUTDIR]
        directory path in that kernel output files and data will be created

        [-h]
        print help message


<Example> ::
        >>> ekea mpasocn \
            /path/to/my/case \
            $E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_diagnostics.F \
            -o /path/to/output

As of this version, there exist two subcommands of mpasocn and eam for MPAS Ocean Model and E3SM Atmospheric Model each.


.. toctree::
    :maxdepth: 2

    mpasocn
    eam
