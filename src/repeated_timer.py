from threading import Timer
from time import perf_counter
import logging

class RepeatedTimer:
    def __init__(self, interval, function, *args, **kwargs) -> None:
        self._timer = None
        self.interval = interval    # Interval in seconds
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self._is_running = False
        self.next_call = perf_counter()
        logging.debug(f"Starting repeated process: {function} @ {1.0/interval} Hz...")
        self.start()

    def _run(self):
        self._is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self._is_running:
            self.next_call += self.interval
            self._timer = Timer(self.next_call - perf_counter(), self._run)
            self._timer.start()
            self._is_running = True

    def stop(self):
        logging.debug(f"Stopping repeated process: {self.function} @ {1.0/self.interval} Hz...")
        self._timer.cancel()
        self._is_running = False
