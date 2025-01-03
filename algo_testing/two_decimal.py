from decimal import Decimal, ROUND_HALF_UP, ROUND_FLOOR

class TwoDecimal:
    def __init__(self, value):
        self.value = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Arithmetic operator overloads
    def __add__(self, other):
        if isinstance(other, TwoDecimal):
            return TwoDecimal(self.value + other.value)
        elif isinstance(other, (int, float, Decimal)):
            return TwoDecimal(self.value + Decimal(other).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, TwoDecimal):
            return TwoDecimal(self.value - other.value)
        elif isinstance(other, (int, float, Decimal)):
            return TwoDecimal(self.value - Decimal(other).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, TwoDecimal):
            return TwoDecimal(self.value * other.value)
        elif isinstance(other, (int, float, Decimal)):
            return TwoDecimal(self.value * Decimal(other).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, TwoDecimal):
            return TwoDecimal(self.value / other.value)
        elif isinstance(other, (int, float, Decimal)):
            return TwoDecimal(self.value / Decimal(other).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        return NotImplemented

    # Comparison methods
    def __eq__(self, other):
        # Check if 'other' is a number (int, float, or Decimal)
        if isinstance(other, TwoDecimal):
            return self.value == other.value
        elif isinstance(other, (float, int, Decimal)):
            return self.value == Decimal(other).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return False

    def __lt__(self, other):
        if isinstance(other, TwoDecimal):
            return self.value < other.value
        elif isinstance(other, (float, int, Decimal)):
            return self.value < Decimal(other).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return False

    def __le__(self, other):
        if isinstance(other, TwoDecimal):
            return self.value <= other.value
        elif isinstance(other, (float, int, Decimal)):
            return self.value <= Decimal(other).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return False

    def __gt__(self, other):
        if isinstance(other, TwoDecimal):
            return self.value > other.value
        elif isinstance(other, (float, int, Decimal)):
            return self.value > Decimal(other).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return False

    def __ge__(self, other):
        if isinstance(other, TwoDecimal):
            return self.value >= other.value
        elif isinstance(other, (float, int, Decimal)):
            return self.value >= Decimal(other).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return False

    def __ne__(self, other):
        if isinstance(other, TwoDecimal):
            return self.value != other.value
        elif isinstance(other, (float, int, Decimal)):
            return self.value != Decimal(other).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return False
    
    def __str__(self):
        return str(self.value)
    
    def floor(self):
        # Use the Decimal method `to_integral_value()` with the ROUND_FLOOR option to floor the value
        return TwoDecimal(self.value.to_integral_value(rounding=ROUND_FLOOR))
    
    # Method to round and return the value
    def two_decimal(self, val):
        return Decimal(val).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)