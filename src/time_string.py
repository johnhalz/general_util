import datetime

class TimeString:
    # Meant for short durations. If you write 14:15:12.44 will convert to seconds
    @staticmethod
    def to_seconds(time_string: str) -> float:
        c_split_time = time_string.split(':')

        if '.' in c_split_time[-1]:
            d_split_time = c_split_time[-1].split('.')
            c_split_time[-1] = d_split_time[0]
        else:
            d_split_time = ['0']

        if '-' in c_split_time[0]:
            negative = True
        else:
            negative = False

        r_c_split_time = list(reversed(c_split_time))

        seconds = sum(x * int(t) for x, t in zip([1, 60, 3600], r_c_split_time)) + abs(float('.' + d_split_time[-1]))

        return seconds, negative

    @staticmethod
    def get_current_time() -> str:
        return datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
