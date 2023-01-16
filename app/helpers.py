class CircularCounter:

    def __init__(self, start, cycle_len, value=None):
        if not isinstance(start, int):
            raise ValueError("start must be int")
        if not isinstance(cycle_len, int) or cycle_len <= 0:
            raise ValueError("cycle_len must be a positive integer")
        if value is not None:
            if not isinstance(value, int) or not (start <= value < start+cycle_len):
                raise ValueError("value must be integer in range [start, start+cycle_len)")

        self.start = start
        self.cycle_len = cycle_len
        self._value = value if value is not None else start

    @property
    def value(self):
        return self._value

    def increment(self):
        self._value += 1
        if self._value == self.start + self.cycle_len:
            self._value = self.start



