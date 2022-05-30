# `util_python` - General Python Utility Repository

This repository is meant to contain general tools and utilities that are reliable and can be used in many software projects.

You can add this repo as a submodule to your project, or fork it in case you wish to make changes.

## Current Utilities:
- `repeated_timer.py`: Perform iterations at a specified frequency with accurate timing (nanosecond accuracy) in a separate thread (this timer will not be affected by any other processes you have running)
- `axis.py`: Elegant definition to x, y and z axis
- `units.py`: Ability to add assign physical units to your values in code, perform unit conversions clearly without miscalculations.
- `force.py` & `moment.py`: Ability to define forces and moments/torques in projects and perform calculations onto them (with units).

## Installing Dependencies
This repo requires the installation of the following packages:
- [`numpy`](https://pypi.org/project/numpy/)
- [`pint`](https://pypi.org/project/Pint/)

To install these dependencies, enter this command in a terminal when inside this folder:
``` bash
python -m pip install -r requirements.txt
```

## Todos
- [ ] `force.py` & `moment.py`: Should make `Moment` a derived class of `Force` to prevent duplicate code.
