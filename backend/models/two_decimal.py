from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from decimal import Decimal as PyDecimal, ROUND_DOWN, ROUND_FLOOR

class TwoDecimal:
    def __init__(self, value: str | float | int):
        self.value = PyDecimal(value).quantize(PyDecimal("0.01"), rounding=ROUND_DOWN)

    def __repr__(self):
        return f"{self.value}"
    
    def __str__(self):
        return f"{self.value}"
    
    def __getstate__(self):
        return {'value': str(self.value)}

    # Arithmetic Operators
    def __add__(self, other: "TwoDecimal"):
        return TwoDecimal(self.value + other.value)

    def __sub__(self, other: "TwoDecimal"):
        return TwoDecimal(self.value - other.value)

    def __mul__(self, other: "TwoDecimal"):
        return TwoDecimal(self.value * other.value)

    def __truediv__(self, other: "TwoDecimal"):
        return TwoDecimal(self.value / other.value)
    
    # Floored Division to Whole Number
    def floored_div(self, other: "TwoDecimal"):
        return TwoDecimal(self.value // other.value)  # Floor division using //

    # Comparison Operators
    def __eq__(self, other: "TwoDecimal"):
        return self.value == other.value

    def __ne__(self, other: "TwoDecimal"):
        return self.value != other.value

    def __lt__(self, other: "TwoDecimal"):
        return self.value < other.value

    def __le__(self, other: "TwoDecimal"):
        return self.value <= other.value

    def __gt__(self, other: "TwoDecimal"):
        return self.value > other.value

    def __ge__(self, other: "TwoDecimal"):
        return self.value >= other.value
    
     # Pydantic support: Define how Pydantic should handle TwoDecimal
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, value):
        if isinstance(value, cls):
            return value
        return cls(value)  # Convert int/float/str to TwoDecimal automatically