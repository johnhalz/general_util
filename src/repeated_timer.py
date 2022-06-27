from threading import Timer
from time import perf_counter
import logging

class RepeatedTimer:
    def __init__(self, number_of_executions, interval, function, *args, **kwargs) -> None:
        self._timer = None
        self.interval = interval    # Interval in seconds
        self.function = function

        if number_of_executions is None:
            self.current_exec_number = -1
        else:
            self.current_exec_number = 0
            self.number_of_executions = number_of_executions
        
        self.args = args
        self.kwargs = kwargs
        self._is_running = False
        self.next_call = perf_counter()
        
        logging.debug(f"RepeatedTimer - Starting repeated process: {function} @ {1.0/interval} Hz")
        if self.current_exec_number == 0:
            logging.debug(f"RepeatedTimer - Set number of executions: {self.number_of_executions}")

        self.start()

    def _run(self):
        self._is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

        # Only increment execution number if a total number of executions have been specified
        if not self.current_exec_number == -1:
            self.current_exec_number += 1
            logging.debug(f"RepeatedTimer - Completed Process {self.current_exec_number}/{self.number_of_executions}")

    def start(self):
        if not self._is_running:
            self.next_call += self.interval
            self._timer = Timer(self.next_call - perf_counter(), self._run)
            self._timer.start()
            self._is_running = True

    def stop(self):
        logging.debug(f"RepeatedTimer - Stopping repeated process: {self.function} @ {1.0/self.interval} Hz")
        self._timer.cancel()
        self._is_running = False
