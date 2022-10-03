.. _intro:

===============
Getting-started
===============

To use ekea, **ekea** needs to be installed on the system where E3SM case directory and E3SM source files exist.

-------------
Installation
-------------

The easiest way to install **ekea** is to use the pip python package manager. 

.. code-block:: bash

        >>> pip install ekea

You can install **ekea** from the github code repository if you want to try the latest version.

.. code-block:: bash

        >>> git clone https://github.com/grnydawn/ekea.git
        >>> cd ekea
        >>> python setup.py install

Once installed, you can test the installation by running the following command.

.. code-block:: bash

        >>> ekea --version
        ekea 1.1.2

------------
Requirements
------------

- Linux OS
- Python 3.5+
- Make building tool(make)
- C Preprocessor(cpp)
- System Call Tracer(strace)

-------------------------
E3SM Kernel Extraction
-------------------------

Once **ekea** is installed correctly and a E3SM case is created successfully, you can extract a kernel as explained below.

The syntax of **ekea** command for simple usage is following:

.. code-block:: bash

        >>> ekea <ocn|eam> $CASEDIR $CALLSITEFILE

, where $CASEDIR is a directory path to E3SM case directory and $CALLSITEFILE is a file path to a E3SM source file containing **ekea** kernel region directives(explained below).

Next to the "ekea" command, the user chooses one of two subcommands(**ocn** or **eam**) for MPAS Ocean Model and E3SM Atmospheric Model each.

Kernel region directives
-------------------------

As shown below, a pair of "begin_callsite" and "end_callsite" directives defines an ekea kernel region in source code. The kernel region is where to be extracted as a kernel. Following example shows an **ekea** kernel region that encompasses a DO loop.

.. code-block:: fortran

        ! file path : /my/E3SM/components/eam/src/file.F90

        !$kgen begin_callsite vecadd
        DO i=1
            C(i) = A(i) + B(i)
        END DO
        !$kgen  end_callsite

Kernel extraction command
-------------------------

Assuming that the E3SM case directory is "/e3smcases/mycase" and the above ekea kernel region directives are specified in "/my/E3SM/components/eam/src/file.F90" under EAM source directory, the full ekea command is below:

.. code-block:: bash

        >>> ekea eam /e3smcases/mycase /my/E3SM/components/eam/src/file.F90


For the more complex kernel extraction cases, please see :ref:`kernel-extract`.
