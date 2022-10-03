.. _kernel-complex:

*************************************
Extracting complex kernels
*************************************

To extract complex kernels, you may need to do extra-works in addition to the tasks explained at :ref:`kernel-extract`.

First of all, you need to understand the limitations of current ekea kernel extraction capabilities.

Limitations on kernel extraction
--------------------------------------

* Not all Fortran standard are supported. We are working on adding more Fortran standard support.
* Fortran pointers are sometimes broken when loading data into variables
* Kernel can not contain the codes having side-effects such as input from network and/or file.
* Complex data structure such as cyclic linked list and complex derived types sometimes break ekea analysis

In case that you can not extract a kernel due to above issues, please consider differnt region of kernel for extraction that can avoid them.

Excluding unnecessary codes from kernel region
------------------------------------------------

One effective way to enhance the ability of kernel extraction is to exclude non-essential codes from kernel extraction.

To use this feature, user needs to add an ekea "--exclude-ini" option.

.. code-block:: bash

        ekea ... --exclude-ini /my/exclude/ini/file.ini

For example, there are many E3SM subroutines that include timing measurement routines such as "mpas_timer_start" or "t_startf". In many cases, it is not essential to include those code lines in the extracted kernels. By excluding those subroutine calls from kernel extraction, user can reduce the complexity of source code analyses and kernel generation from ekea tasks. In addition, sometimes it is essential to entirely exclude a Fortran module such as pio module which eventually will read data from file system.

For the purpuse of code exclusion, ekea provides users a way to specify those information in a INI-format file.


.. code-block:: ini

        [namepath]
        pio = skip_module
        :mpas_log_open =
        parameters_tunable::initvars =


As of this version, only one section of "[namepath]" is available in this file. 


Including artifacts manually
------------------------------------------------

The other way to improve kernel extraction capability is to manually add what ekea needs.

To use this feature, user needs to use "--include-ini" ekea option.

.. code-block:: bash

        ekea ... --include-ini /my/include/ini/file.ini

Following example show various information that is given to ekea through INI-format file.

.. code-block:: ini

        [macro]
        NUM_VARS = 2

        [import]
        /my/shared/library.so = shared_library
        /my/static/library.a = static_library
        /my/object.o = object

        [include]
        /my/include/file1.h =
        /my/include/file2.inc =

        [compiler]
        /my/include/file1.h =
        /my/include/file2.inc =

        [/my/source/file1.f90]
        include = /my/include/file1.h:/my/include/file2.h
        compiler = /my/gfortran
        compiler_options = -O1
        NUM_VARS = 2

        [/my/source/file2.f90]
        compiler_options = -O2

