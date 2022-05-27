from .axis import Axis
from .units import ureg

import logging
from math import pi
import numpy as np


class Block:
    def __init__(self, vector = None):
        self._expected_input_size = 3
        if vector is None:
            self._dims = np.zeros(self._expected_input_size) * ureg.newton
        else:
            if np.size(vector) == self._expected_input_size:
                self._dims = vector
            else:
                logging.error(f"Incorrect input vector size (input size {np.size(vector)}, required size {self._expected_input_size})")

    def x(self):
        return self._dims[0]

    def y(self):
        return self._dims[1]

    def z(self):
        return self._dims[2]

    def volume(self):
        return self._dims[0] * self._dims[1] * self._dims[2]

    def cross_section_area(self, axis: Axis):
        if axis is Axis.x:
            return self.y() * self.z()
        elif axis is Axis.y:
            return self.x() * self.z()
        elif axis is Axis.z:
            return self.x() * self.y()

    def inertia(self, axis: Axis):
        if axis is Axis.x:
            return (self.x() * self.y()**3)/12.0
        elif axis is Axis.y:
            return (self.y() * self.x()**3)/12.0
        elif axis is Axis.z:
            return 0.0 * ureg.m**4

    # Log the current value in the cli
    def log(self, name: str = None):
        if name is None:
            logging.info(f"Block dimensions: {self._dims}")
        else:
            logging.info(f"{name} dimensions: {self._dims}")

class Cylinder:
    def __init__(self, diameter = None, height = None, axis: Axis = None):
        if diameter is None:
            self._diameter = 0.0 * ureg.m
        else:
            self._diameter = diameter
            
        if height is None:
            self._height = 0.0 * ureg.m
        else:
            self._height = height

        if axis is None:
            self._axis = Axis.z
        else:
            self._axis = axis

    def height(self):
        return self._height

    def diameter(self):
        return self._diameter

    def x(self):
        if self._axis is Axis.x:
            return self.height()
        else:
            return self.diameter()

    def y(self):
        if self._axis is Axis.y:
            return self.height()
        else:
            return self.diameter()

    def z(self):
        if self._axis is Axis.z:
            return self.height()
        else:
            return self.diameter()

    def radius(self):
        return self._diameter/2.0

    def volume(self):
        return self._height * self.cross_section_area(self._axis)

    def cross_section_area(self, axis: Axis):
        if axis != self._axis:
            return 0.0 * ureg.m**2
        else:
            return pi * (self._diameter**2/4.0)

    def inertia(self, axis: Axis):
        if axis != self._axis:
            return 0.0 * ureg.m**4
        else:
            return pi * self._diameter**4/64.0

    # Log the current value in the cli
    def log(self, name: str = None):
        if name is None:
            logging.info(f"Cylinder: Diameter: {self._diameter}, Height: {self._height}, Axis: {self._axis}")
        else:
            logging.info(f"{name}: Diameter: {self._diameter}, Height: {self._height}, Axis: {self._axis}")