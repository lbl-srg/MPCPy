Getting Started
===============

To get started with MPCPy, first follow the installation instructions below.  Then, checkout the introductory tutorial to get a feel for the workflow of MPCPy.  You can always consult the user guide for more information.

Installation Instructions For Linux (Ubuntu 16.04 LTS)
------------------------------------------------------

1. Install Python packages:

    - MPCPy uses Python 2.7.

    - using pip, install the following packages:

	    matplotlib >= 2.0.2

	    numpy >= 1.13.1

	    pandas >= 0.20.3

	    python-dateutil >= 2.6.1

	    pytz >= 2017.2

	    scikit-learn >= 0.18.2

	    sphinx >= 1.6.3

	    numpydoc >= 0.7.0

	    tzwhere **==** 2.3

        modestpy **==** 0.0.7

2. Install libgeos-dev with command:

	.. code-block:: text

	    > sudo apt-get install libgeos-dev

3. Install JModelica 2.0 (for Modelica compiling, optimization, and fmu simulation)

4. Create JModelica environmental variables

    - add the following lines to your bashrc script and replace the "..." with the JModelica install directory:

        ::

            export JMODELICA_HOME=".../JModelica"
            export IPOPT_HOME=".../Ipopt-3.12.4-inst"
            export SUNDIALS_HOME="$JMODELICA_HOME/ThirdParty/Sundials"
            export SEPARATE_PROCESS_JVM="/usr/lib/jvm/java-8-openjdk-amd64/"
            export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/"

5. Create the MODELICAPATH environmental variable

    - add the following lines to your bashrc script (assumes 4. above sets JMODELICA_HOME): 

        ::

            export MODELICAPATH="$JMODELICA_HOME/ThirdParty/MSL"

6. Download or Clone EstimationPy-KA

    - go to https://github.com/krzysztofarendt/EstimationPy-KA and clone or download repository into a directory (let's call it ``.../EstimationPy-KA``).

7. Download or Clone MPCPy

    - go to https://github.com/lbl-srg/MPCPy and clone or download repository into a directory (let's call it ``.../MPCPy``).

8. Edit PYTHONPATH environmental variable

    - add the following lines to your bashrc script (assumes 4. above sets JMODELICA_HOME) and replace the "..." with the appropriate directory:
        
        ::
        
            export PYTHONPATH=$PYTHONPATH:"$JMODELICA_HOME/Python"
            export PYTHONPATH=$PYTHONPATH:"$JMODELICA_HOME/Python/pymodelica"
            export PYTHONPATH=$PYTHONPATH:".../EstimationPy-KA"
            export PYTHONPATH=$PYTHONPATH:".../MPCPy"

9. Test the installation

    - Run the introductory tutorial example.  From the command-line, use the commands:

	.. code-block:: text

	    > cd doc/userGuide/tutorial
	    > python introductory.py

10. Optional, for developers only

    - to pass all unit tests, the `Modelica Buildings Library <http://simulationresearch.lbl.gov/modelica/>`_ must also be on the MODELICAPATH.  Download the library and add the appropriate directory path to the MODELICAPATH variable.

    - to generate the user guide pdf, latex must be installed.  Use the following commands to install texlive and latexmk:

    	.. code-block:: text

	    > sudo apt-get install texlive
	    > sudo apt-get install texlive-formats-extra
	    > sudo apt-get install latexmk
	

Introductory Tutorial
---------------------

.. automodule:: doc.userGuide.tutorial.introductory


Run Unit Tests
--------------
The script bin/runUnitTests.py runs the unit tests of MPCPy.  By default, all of the unit tests are run.  An optional argument -s [module.class] will run only the specified unit tests module or class.

To run all unit tests from command-line, use the command:

    .. code-block:: text

    	> python bin/runUnitTests

To run only unit tests in the module test_models from command-line, use the command:

    .. code-block:: text

	> python bin/runUnitTests -s test_models

To run only unit tests in the class SimpleRC from the module test_models from the command-line, use the command:

    .. code-block:: text

	> python bin/runUnitTests -s test_models.SimpleRC

