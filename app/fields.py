from django.db import models
from django.core.exceptions import ValidationError

from app.helpers import CircularCounter


# finish the implementation of CircularCounterField

class CircularCounterField(models.Field):
    def db_type(self, connection):
        return 'char(25)'

    description = "Field to store CircularCounter instances"

    def from_db_value(self, value, expression, connection):
        pass

    def to_python(self, value):
        pass

    def get_prep_value(self, value, *args, **kwargs):
        pass


