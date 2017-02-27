## Run Unit Tests
The script runUnitTests.py runs the unit tests of MPCPy.  By default, all of the unit tests are run.  An optional argument -s [module.class] will run only the specified unit tests module or class.

To run all unit tests from command-line, use the command (shown from the parent directory):

    .. code-block:: text
    
	   > python bin/runUnitTests

To run only unit tests in the module test_models from command-line, use the command (shown from the parent directory):

    .. code-block:: text

	   > python bin/runUnitTests -s test_models

To run only unit tests in the class Estimate_Jmo from the module test_models from the command-line, use the command (shown from the parent directory):

    .. code-block:: text

    	> python bin/runUnitTests -s test_models.Estimate_Jmo
