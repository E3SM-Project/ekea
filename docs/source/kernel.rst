.. _kernel-output:

*************************************
Kernel execution output on screen
*************************************

Kernel execution verification and timing measurements are built-in in all ekea kernels.

During kernel extraction, ekea generates one or more binary data files in the kernel subdirectory. The extracted kernel reads those data files at runtime and loads it to proper variables, and checks if the extracted kernel produces the same contents of the variables compared to the data generated from the original E3SM execution.

In the following example, "mpas_ocn_coriolis.45.0.1" binary data file is read and the verification results is shown. Among variables used in the kernel, 14 variables are marked as out type. Therefore the content of the 14 variables are verified after execution by the kernel. In the following example, among 14 out-type variables, 13 variables are bit-for-bit the same while one variable is different within 1.0E14 tolerance. Because none of out-type variables is out of tolerance, the test is PASSED. Next the kernel displays the elapsed time measurement of the kernel execution.

Users can modify the tolerance and the amount of information to display by changing values in the source files that contain theekea kernel region. For example, in "mpas_ocn_vel_hadv_coriolis.f90" in this example, User can change values in the following code.

.. code-block:: fortran

        CALL kgen_init_verify(tolerance=1.D-14, minvalue=1.D-14, verboseLevel=1)

"minvalue" is to set the minimum distinguishable value. "verboseLevel" sets the amount of information to display. Higher value will display more information on screen upto 3.

::

        ***************** Verification against 'mpas_ocn_coriolis.45.0.1' *****************

        Number of output variables:           14
        Number of identical variables:           13
        Number of non-identical variables within tolerance:            1
        Number of non-identical variables out of tolerance:            0
        Tolerance:    1.0000000000000000E-014

        Verification PASSED with mpas_ocn_coriolis.45.0.1

        mpas_ocn_coriolis : Time per call (usec):    1322.9690000000001

        ...

        ****************************************************
            kernel execution summary: mpas_ocn_coriolis
        ****************************************************
            Total number of verification cases  :    40
            Number of verification-passed cases :    40

            kernel: mpas_ocn_coriolis: PASSED verification

            number of processes  1

            Average call time (usec):  0.120E+04
            Minimum call time (usec):  0.824E+03
            Maximum call time (usec):  0.143E+04
        ****************************************************


At the end of kernel execution, the kernel displays the summary of kernel execution. In this example, it shows that 40 binary data files are used to verification and all of them are passed. The elapsed time statistics are shown below with average, minimum, and maximum elapsed times.

