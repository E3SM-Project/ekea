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


Welcome to the E3SM Kernel Extraction and Analysis (ekea).

ekea is a kernel extraction and analysis tool customized for the Energy Exascale Earth System Model (E3SM). The ekea is a Python module and command-line tool that can be downloaded using the Python package manager (pip). With ekea, a user can extract a part of E3SM code and make the extracted code(kernel) compilable independently from the E3SM. The ekea also generates input data to drive the kernel execution and out-type data to verify the correctness of the execution. With combined the extracted kernel code and generated data, user can perform various software engineering tasks such as performance optimization, GPU porting, simulation validation, debugging, unit testing, and more without depending on the E3SM as well as the system.

As of this version, the ekea supports MPAS Ocean and EAM component models.

The ekea is an E3SM-specialized version of a more generic Kernel Extraction and Analysis Framework explained in the next section.


Kernel extraction and analysis framework
-------------------------------------------------

The automated kernel extraction is based on static analysis of an application source code. When a user provides the ekea with a range of code for extraction, it parses the code to Abstract Syntax Tree (AST) and see if all code statements required to compile the part of code exist within the AST. If yes, it stops the analysis and converts the collected ASTs to source code. If not, it reads another source file based on information found in the Fortran USE statement, and tries to find all statements that make the range of code compilable until all the information is collected.

In practice, kernel extraction should deal with the complexity and variability of each application. For example, there are subtle differences between applications in terms of building system, Fortran standard used, complexity of the code, dynamic code generation among others, which makes it hard for one version of a kernel extractor to support all the applications. For these reasons, a framework for kernel extraction is developed as a core function and each variant of the framework supports a specific application.


In the following section, the benefits of using a kernel are explained.


Kernel-based software engineering approach
------------------------------------------------

A kernel is a small software that represents a certain characteristic of a larger application. It can be compiled and run generally without using external libraries on a single computing node. Due to its simple usage, it can greatly improve productivity of various software engineering tasks such as performance optimization, debugging, porting, verification, and so on.

In addition, a kernel could be an efficient vehcle for enhancing communication between collaborators possibly from various disciplines. For example, a kernel that contains a compiler bug is useful not only for reporting the bug but also for producing and fixing the bug by the compiler engineer.

While a kernel is useful for many software engineering tasks, it is generally a hard to create one. Mere copying and pasting an interesting block of code generally does not produce compilable software. In manual kernel extraction, it is common to scan through all source files to find required statements such as variable declaration and importing other modules. Furthermore, preparing state data for driving the execution of a generated kernel is generally harder task. For example, if a structured variable contains a pointer variable in another structured variable, the user should manually copy those variables, aka, deep copying.

Fortunately, most of kernel extraction task from large Fortran application can be automated through static analysis, which is a core function of ekea.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro 
   kernel 
   commands/index
   usage 
   examples/index
   developer/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
