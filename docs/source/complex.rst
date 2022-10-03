.. _kernel-complex:

*************************************
Extracting complex kernels
*************************************

To extract complex kernels, you may need to do extra-works in addition to the tasks explained at :ref:`kernel-extract`.

First of all, it would be useful to understand the limitations of current ekea kernel extraction capabilities.

Limitations on kernel extraction
--------------------------------------

* Not all Fortran standards are supported. We are working on adding more Fortran standard support.
* Fortran pointers are sometimes broken when loading data into variables
* Kernel can not contain the codes having side-effects such as input from network and/or file.
* Complex data structure such as cyclic linked list and complex derived types sometimes break ekea analysis

In case that you can not extract a kernel due to above issues, please consider a different region of kernel for extraction that can avoid them.

.. _exclude_ini:

Excluding unnecessary codes from kernel region
------------------------------------------------

One effective way to enhance the ability of kernel extraction is to exclude non-essential codes from kernel extraction.

To use this feature, users need to add an ekea "--exclude-ini" option.

.. code-block:: bash

        ekea ... --exclude-ini /my/exclude/ini/file.ini

For example, there are many E3SM subroutines that include timing measurement routines such as "mpas_timer_start" or "t_startf". In many cases, it is not essential to include those code lines in the extracted kernels. By excluding those subroutine calls from kernel extraction, users can reduce the complexity of source code analyses and kernel generation from ekea tasks. In addition, sometimes it is essential to entirely exclude a Fortran module such as pio module which eventually will read data from the file system.

For the purpose of code exclusion, ekea provides users a way to specify that information in an INI-format file.


.. code-block:: ini

        [namepath]
        pio = skip_module
        :mpas_log_open =
        mixing_length:compute_mixing_length:t_startf =
        parameters_tunable::initvars =


As of this version, only one section of "[namepath]" is available in this file. 

All "namepaths" specified under "[namepath]" section will be excluded from ekea analysis and kernel generation.

":" in namepaths works as either a separator or any names.

Exclusion action comes after the equal sign in the namepath line. If no execution action is specified, its default action is simply to ignore the namepath.

After equal sign of the "pio" line, the "skip_module" is an action for ekea to skin the "pio" module. "skip_module" action order ekea skip any lines that contain the module name of "pio". By doing this, ekea skips any Fortran USE statements that contain "pio" module name.

":mpas_log_open" tells ekea to skip the Fortran statements that contains "mpas_log_open". Namepath is organized as a hierarchy from module name through subroutine(function) name to a name in execution statements. For example, if a module "A" has a subroutine "B", and the subroutine "B" has a Fortran statement having "C" variable, then we can select the "C" by specifying namepath as "A:B:C".  In case of ":mpas_log_open", because there exists ":" as the first characters, it selects all statements having "mpas_log_open" in any subroutine in any modules in a source file. The ":" acts as if it is "*" in "ls" linux command.

"mixing_length:compute_mixing_length:t_startf" tells ekea to exclude the name of "t_startf" in the "compute_mixing_length" subroutine of the "mixing_length" module.

"parameters_tunable::initvars" tells ekea to exclude the name of "initvars" in the module "parameters_tunable".

.. _include_ini:

Including artifacts manually
------------------------------------------------

The other way to improve kernel extraction capability is to manually add what ekea needs.

To use this feature, user needs to use "--include-ini" ekea option.

.. code-block:: bash

        ekea ... --include-ini /my/include/ini/file.ini

Following examples show various information that is given to ekea through the INI-format file.

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

Under the "[macro]" section, users can add multiple macro definitions that will be used to compile any source files in the generated kernel.


Under the "[import]" section, users can add a library when linking the generated kernel. There are three types of import including "shared_library", "static_library", and "object" file.

Under the "[include]" section, users can add multiple include paths that will be used to compile any source files in the generated kernel.
