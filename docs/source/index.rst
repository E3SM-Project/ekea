.. _index:

.. ekea documentation master file, created by
   sphinx-quickstart on Wed Mar 10 14:45:17 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. only:: html

    :Release: |release|
    :Date: |today|

===================================================
ekea: E3SM Kernel Extraction and Analysis
===================================================

**ekea** automates the process of kernel extraction from a large Fortran applicatin. Especially, it is customized for E3SM so that, in many kernel extraction cases from E3SM, user only needs to specify E3SM case directory and region for kernel extraction.

In additiion, user can easily extend **ekea** to create a new E3SM analysis software tools(ekea-app). Several examples of ekea-app are included in this distribution too.

**ekea** is a Python module and command-line tool. It can be downloaded using the Python package manager (pip).

.. code-block:: bash

        >>> pip install ekea

The usage of ekea could be as simple as a shell command shown below.

.. code-block:: bash

        >>> ekea ocn $CASEDIR $CALLSITEFILE

, where $CASEDIR is a directory path to E3SM case directory and $CALLSITEFILE is a file path to a E3SM source file containing **ekea** kernel region directives(See :ref:`intro` for more details). "ocn" subcommand is used to extract a kernel from Ocean model.

In addition to kernel source files, **ekea** also generates input data to drive the kernel execution and out-type data to verify the correctness of the execution. With combined the extracted kernel code and generated data, user can perform various software engineering tasks such as performance optimization, GPU porting, simulation validation, debugging, unit testing, and more without depending on the whole E3SM as well as the batch system.

As of this version, **ekea** supports MPAS Ocean model and EAM model.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro 
   command
   extract
   message 
   kernel 
   output 
   analyses/index
   develop/index
   troubleshooting/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
