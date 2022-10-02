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


Welcome to the E3SM Kernel Extraction and Analysis (**ekea**).

**ekea** is a kernel extraction and analysis tool customized for the Energy Exascale Earth System Model (E3SM). **ekea** is a Python module and command-line tool that can be downloaded using the Python package manager (pip). With **ekea**, a user can extract a part of E3SM code and make the extracted code(kernel) compilable independently from the E3SM.

The usage of ekea could be as simple as a shell command shown below.

.. code-block:: bash

        >>> ekea mpasocn $CASEDIR $CALLSITEFILE

, where $CASEDIR is a directory path to E3SM case directory and $CALLSITEFILE is a file path to a E3SM source file containing **ekea** kernel region directives(See :ref:`intro` for more details).

In addition to kernel source files, **ekea** also generates input data to drive the kernel execution and out-type data to verify the correctness of the execution. With combined the extracted kernel code and generated data, user can perform various software engineering tasks such as performance optimization, GPU porting, simulation validation, debugging, unit testing, and more without depending on the whole E3SM as well as the batch system.

As of this version, **ekea** supports MPAS Ocean model and EAM model.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro 
   extract
   troubleshooting/index
   usage 
   analyses/index
   develop/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
