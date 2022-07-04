from sys import path
from os.path import dirname, join, abspath
path.insert(0, abspath(join(dirname(__file__), '..')))

from src.time_string import TimeString

input_time = "-1"

print(TimeString.to_seconds(input_time))
print(TimeString.get_current_time())