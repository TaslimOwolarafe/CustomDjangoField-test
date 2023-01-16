## Environment:
- Python version: 3.7
- Django version: 3.0.6

## Read-Only Files:
- app/tests.py
- app/helpers.py
- app/models.py
- manage.py

## Requirements:


In this challenge, your task is to implement a custom model field called `CircularCounterField` as a field to hold the provided `CircularCounter` class.

A circular counter is an object that stores a value that is initially set to the given start value and can be incremented. After a given number of increments from the starting value (let's call this number `cycle_len`), the value is reset to the starting value. For example, if `start=1` and `cycle_len=2`, then the initial value is 1. After the first increment, the value becomes 2. After the second increment, the value is reset to the start value, i.e. 1. Then, after the third increment, the value becomes 2, and after the fourth increment, it again becomes 1, and so on.



`CircularCounter` class is a very simple class to store the state of a circular counter:

```python
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
```

The `CircularCounterField` must be implemented according to the following requirements:

1. Must behave like a valid field that can be used in a model. In particular, it must implement the `from_db_value()`, `to_python()`, and `get_prep_value()` methods of `django.db.models.Field`. The placeholders for these methods are provided.

2. Serializes a `CircularCounter` instance to a string of the format `"<start>:<cycle_len>:<value>"`, where `<start>`, `<cycle_len>`, and `<value>` are attributes of the counter being serialized. For instance, if the counter has `start=1`, `cycle_len=3`, and `value=2`, then it must be serialized to the string `"1:3:2"`.

3. Restores a `CircularCounter` instance from a serialized string. In case the object cannot be created from the serialized value (e.g., due to invalid parameters), it raises `django.core.exceptions.ValidationError`.

## Example Usage:

```python
>>> from app.models import State
>>> from app.helpers import CircularCounter

>>> counter = CircularCounter(start=1, cycle_len=2)
>>> counter.value
1
>>> state = State.objects.create(counter=counter)
>>> state.refresh_from_db()
>>> state.counter.value
1
>>> state.counter.increment()
>>> state.counter.value
2
>>> state.counter.increment()
>>> state.counter.value
1
>>> another_counter = CircularCounter(start=2, cycle_len=1)
>>> state.counter = another_counter
>>> state.counter.value
2
>>> state.save()
>>> state.counter.increment()
>>> state.counter.value
2
>>> state.counter.increment()
>>> state.counter.value

```

## Commands

+ run:
```source env1/bin/activate; pip3 install -r requirements.txt; python3 manage.py makemigrations && python3 manage.py migrate --run-syncdb && python3 manage.py runserver 0.0.0.0:8000```

+  install:
```bash python_install.sh;source env1/bin/activate; pip3 install -r requirements.txt;```

+ test:
```rm -rf unit.xml;source env1/bin/activate; python3 manage.py test```
