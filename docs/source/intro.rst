===============
Getting-started
===============

To use ekea, ekea should be installed on the system where E3SM case directory and E3SM source files exist.

-------------
Installation
-------------

The easiest way to install ekea is to use the pip python package manager. 

        >>> pip install ekea

You can install ekea from github code repository if you want to try the latest version.

        >>> git clone https://github.com/grnydawn/ekea.git
        >>> cd ekea
        >>> python setup.py install

Once installed, you can test the installation by running the following command.

        >>> ekea --version
        ekea 0.1.0

------------
Requirements
------------

- Linux OS
- Python 3.5+ or Python 2.7
- Make building tool(make)
- C Preprocessor(cpp)
- System Call Tracer(strace)

-------------------------
E3SM Kernel Extraction
-------------------------

Once ekea is installed correctly and a E3SM case is created successfully, you can extract a kernel as explained below.

The syntax of ekea command is following:

        >>> ekea <mpasocn|eam> $CASEDIR $CALLSITEFILE

, where $CASEDIR is a directory path to E3SM case directory and $CALLSITEFILE is a file path to a E3SM source file containing ekea kernel region directives(explained below).
As of this version, there exist two subcommands of mpasocn and eam for MPAS Ocean Model and E3SM Atmospheric Model each. Please see _command for details about the sub-commands.

ekea kernel region in source code is defined by a pair of "begin_callsite" and "end_callsite" directives. The kernel region is where to be extracted. Following example shows a ekea kernel region that encompasses a DO loop.

::

        !$kgen begin_callsite vecadd
        DO i=1
                C(i) = A(i) + B(i)
        END DO
        !$kgen  end_callsite

Please see _directives for details about using ekea directives.
