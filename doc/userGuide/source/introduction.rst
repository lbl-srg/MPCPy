Introduction
============

General
-------

MPCPy is a python package that facilitates the testing and implementation of occupant-integrated model predictive control (MPC) for building systems.  The package focuses on the use of data-driven, simplified physical or statistical models to predict building performance and optimize control.  Four main modules contain object classes to import data, interact with real or emulated systems, estimate and validate data-driven models, and optimize control inputs:

- ``exodata`` classes collect external data and process it for use within MPCPy.  This includes data for weather, internal loads, control signals, grid signals, model parameters, optimization constraints, and miscellaneous inputs.
- ``system`` classes represent real or emulated systems to be controlled, collecting measurements from and providing control inputs to the systems.  For example, these include detailed simulations or real data collected for zone thermal response, HVAC performance, or ground-truth occupancy.
- ``models`` classes represent system models for MPC, managing model simulation, estimation, and validation.  For example, these could represent an RC zone thermal response model, simplified HVAC equipment performance models, or occupancy models.
- ``optimization`` classes formulate and solve the MPC optimization problems using ``models`` objects.

Three other modules provide additional, mainly internal, functionality to MPCPy:

- ``variables`` and ``units`` classes together maintain the association of static or timeseries data with units.
- ``utility`` classes provide functionality needed across modules and for interactions with external components.

.. figure:: images/SoftwareArchitecture.png
    :scale: 60 %
    
    Software architecture diagram for MPCPy.  Note that a user interface has not been developed.


Third-Party Software
--------------------
While MPCPy provides an integration platform, it relies on free, open-source, third-party software packages for model implementation, simulators, parameter estimation algorithms, and optimization solvers.  This includes python packages for scripting and data manipulation as well as other more comprehensive software packages for specific purposes.  In particular, modeling and optimization for physical systems rely heavily on the Modelica language specification (https://www.modelica.org/) and FMI standard (http://fmi-standard.org/) in order to leverage model library and tool development on these standards occurring elsewhere within the building and other industries.  Two examples of these third-party tools are:

- **JModelica.org** (http://jmodelica.org/) is used for simulation of FMUs, compiling FMUs from Modelica models, parameter estimation of Modelica models, and control optimization using Modelica models.
- **EstimationPy** (http://lbl-srg.github.io/EstimationPy/) is used for implementing the Unscented Kalman Filter for parameter estimation of FMU models.

Contributing
------------
Research has shown that MPC can address emerging control challenges faced by buildings.  However, there exists no standard practice or methods for implementing MPC in buildings.  Implementation is defined here as model structure, complexity, and training methods, data resolution and amount, optimization problem structure and algorithm, and transfer of optimal control solution to real building control.  In fact, different applications likely require different implementations.  Therefore, the aim is for MPCPy to be flexible enough to accommodate different and new approaches to MPC in buildings.  

If you are interested in contributing to this project, please contact the developers and visit the development site at https://github.com/lbl-srg/MPCPy.

Cite
----
To cite MPCPy, please use:

Blum, D. H. and Wetter, M. “MPCPy: An Open-Source Software Platform for Model Predictive Control in Buildings.” Proceedings of the 15th Conference of International Building Performance Simulation, Aug 7 – 9, 2017. San Francisco, CA, Accepted.

