from django.test import TestCase
from django.core.exceptions import ValidationError

from app.fields import CircularCounterField
from app.helpers import CircularCounter
from app.models import State


class FieldTestCase(TestCase):
    def test_from_db_value_with_valid_data(self):
        data = "1:3:2"
        c = CircularCounterField().from_db_value(data, expression=None, connection=None)
        self.assertIsInstance(c, CircularCounter)
        self.assertEqual(c.start, 1)
        self.assertEqual(c.cycle_len, 3)
        self.assertEqual(c.value, 2)

    def test_from_db_value_with_negative_start_and_valid_data(self):
        data = "-2:3:0"
        c = CircularCounterField().from_db_value(data, expression=None, connection=None)
        self.assertIsInstance(c, CircularCounter)
        self.assertEqual(c.start, -2)
        self.assertEqual(c.cycle_len, 3)
        self.assertEqual(c.value, 0)

    def test_from_db_value_with_non_integer_start(self):
        data = "abc:3:2"
        with self.assertRaises(ValidationError):
            CircularCounterField().from_db_value(data, expression=None, connection=None)

    def test_from_db_value_with_non_integer_cycle_len(self):
        data = "1:x:2"
        with self.assertRaises(ValidationError):
            CircularCounterField().from_db_value(data, expression=None, connection=None)

    def test_from_db_value_with_non_positive_cycle_len(self):
        data = "1:-2:1"
        with self.assertRaises(ValidationError):
            CircularCounterField().from_db_value(data, expression=None, connection=None)

    def test_from_db_value_with_non_integer_value(self):
        data = "1:3:z"
        with self.assertRaises(ValidationError):
            CircularCounterField().from_db_value(data, expression=None, connection=None)

    def test_from_db_value_with_value_below_range(self):
        data = "1:3:0"
        with self.assertRaises(ValidationError):
            CircularCounterField().from_db_value(data, expression=None, connection=None)

    def test_from_db_value_with_value_above_range(self):
        data = "1:3:4"
        with self.assertRaises(ValidationError):
            CircularCounterField().from_db_value(data, expression=None, connection=None)

    def test_prep_value(self):
        c = CircularCounter(start=1, cycle_len=3)
        c.increment()
        serialized = CircularCounterField().get_prep_value(c)
        self.assertEqual(serialized, "1:3:2")



class WithModelTestCase(TestCase):
    def test_refresh_from_db(self):
        c = CircularCounter(start=1, cycle_len=2)
        c.increment()
        s = State.objects.create(counter=c)
        s.refresh_from_db(fields=['counter'])
        self.assertIsInstance(s.counter, CircularCounter)
        self.assertEqual(s.counter.start, 1)
        self.assertEqual(s.counter.cycle_len, 2)
        self.assertEqual(s.counter.value, 2)

    def test_refresh_from_db_manipulate_refresh_again(self):
        c = CircularCounter(start=-1, cycle_len=3)
        c.increment()

        s = State.objects.create(counter=c)
        s.refresh_from_db(fields=['counter'])
        self.assertIsInstance(s.counter, CircularCounter)
        self.assertEqual(s.counter.start, -1)
        self.assertEqual(s.counter.cycle_len, 3)
        self.assertEqual(s.counter.value, 0)

        s.counter.increment()
        s.counter.increment()
        s.save()

        s.refresh_from_db(fields=['counter'])
        self.assertIsInstance(s.counter, CircularCounter)
        self.assertEqual(s.counter.start, -1)
        self.assertEqual(s.counter.cycle_len, 3)
        self.assertEqual(s.counter.value, -1)



