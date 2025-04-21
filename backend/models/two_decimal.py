from pydantic import GetCoreSchemaHandler, RootModel, Field, field_validator, field_serializer
from pydantic_core import core_schema
from decimal import Decimal as PyDecimal, ROUND_HALF_DOWN, ROUND_FLOOR
from typing import Any

class TwoDecimal(RootModel[PyDecimal]):
    @field_validator('root', mode='before')
    @classmethod
    def quantize(cls, v: Any) -> PyDecimal:
        d = PyDecimal(v)
        return d.quantize(PyDecimal('0.01'), rounding=ROUND_HALF_DOWN)

    @field_serializer('root')
    @classmethod
    def serialize_root(cls, v: PyDecimal) -> str:
        return str(v)

    def __repr__(self):
        return f"{self.root}"
    
    def __str__(self):
        return f"{self.root}"
    
    def __getstate__(self):
        return {'root': str(self.root)}

    # Arithmetic Operators
    def __add__(self, other: "TwoDecimal"):
        return TwoDecimal(self.root + other.root)

    def __sub__(self, other: "TwoDecimal"):
        return TwoDecimal(self.root - other.root)

    def __mul__(self, other: "TwoDecimal"):
        return TwoDecimal(self.root * other.root)

    def __truediv__(self, other: "TwoDecimal"):
        return TwoDecimal(self.root / other.root)
    
    # Floored Division to Whole Number
    def floored_div(self, other: "TwoDecimal"):
        return TwoDecimal(self.root // other.root)  # Floor division using //

    # Comparison Operators
    def __eq__(self, other: "TwoDecimal"):
        return self.root == other.root

    def __ne__(self, other: "TwoDecimal"):
        return self.root != other.root

    def __lt__(self, other: "TwoDecimal"):
        return self.root < other.root

    def __le__(self, other: "TwoDecimal"):
        return self.root <= other.root

    def __gt__(self, other: "TwoDecimal"):
        return self.root > other.root

    def __ge__(self, other: "TwoDecimal"):
        return self.root >= other.root