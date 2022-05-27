from .units import ureg

import numpy as np
import logging


class Force:
    def __init__(self, vector=None):
        self._expected_input_size = 3
        if vector is None:
            self._value = np.zeros(self._expected_input_size) * ureg.newton
        else:
            if np.size(vector) == self._expected_input_size:
                self._value = vector
            else:
                logging.error(f"Incorrect input vector size (input size {np.size(vector)}, required size {self._expected_input_size})")

    def x(self):
        return self._value[0]

    def y(self):
        return self._value[1]

    def z(self):
        return self._value[2]

    # Return L2 norm of force vector
    def norm(self):
        return np.linalg.norm(self._value.magnitude) * self._value.units

    # Return numpy vector of value
    def vector(self):
        return self._value

    # Log the current value in the cli
    def log(self, name: str = None):
        if name is None:
            logging.info(f"Force: {self._value}")
        else:
            logging.info(f"{name}: {self._value}")

    # Ability to print(Force)
    def __repr__(self) -> str:
        return f"{self._value}"
