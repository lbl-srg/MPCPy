<center> MPCPy v0.1
==============================
<center> Users Guide
------------------------------


Introduction
------------------------------
MPCPy facilitates the testing and implementation of Model Predictive Control (MPC) for building systems.  The software package focuses on the use of data-driven simplified physical or statistical models to predict building performance and optimize control.  Four main modules contain object classes to import data, interact with a real or emulated system, estimate and validate data-driven models, and optimize control inputs.  Three other modules contain classes to help track units and provide additional, mainly internal, functionality to MPCPy.

1. **ExoData** classes collect external data and process it for use within MPCPy.
2. **System** classes represent real or emulated systems to be controlled, collecting measurements from and providing control inputs to the systems.
3. **Models** classes represent system models for MPC, managing model simulation, estimation, and validation.
4. **Optimization** classes formulate and solve the MPC optimization problems using Models objects.
5. **Variable** and **Unit** classes together maintain the association of static or timeseries data with units.
6. **Utility** classes provide functionality needed across modules and for interactions with external components.


Getting Started
------------------------------
To get started, include the MPCPy directory on the PYTHONPATH environmental variable.  To quickly test that it is installed correctly, run the Units module unit tests:

    > python bin/runUnitTests -s test_units




Section 1: ExoData
------------------------------
Section 2: Systems
------------------------------
Section 3: Models
------------------------------
Section 4: Optimization
------------------------------
Section 5: Occupants
------------------------------
Section 6: Variables and Units
------------------------------
Section 7: Utility
------------------------------
