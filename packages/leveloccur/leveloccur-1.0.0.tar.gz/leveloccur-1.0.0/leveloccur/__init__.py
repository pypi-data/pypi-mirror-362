def probability_of_occurrence(item, array):
    """Returns the probability of occurrence of a value in an iterable object."""
    return array.count(item) / len(array)

class Level:
    """Returns one of the strings below depends on the occurrence of a value in an iterable object,
    or the ratio of a number to another number.
    - x > 1: returns 'Excess'
    - x = 1: returns 'Full'
    - 1 > x > 0.9: returns 'Very high'
    - 0.9 ≥ x > 0.8: returns 'High'
    - 0.8 ≥ x > 0.7: returns 'Pretty high'
    - 0.7 ≥ x > 0.6: returns 'Medium-high'
    - 0.6 ≥ x > 0.5: returns 'Medium'
    - x = 0.5: returns 'Exactly half'
    - 0.5 > x > 0.4: returns 'Medium-low'
    - 0.4 ≥ x > 0.3: returns 'Pretty low'
    - 0.3 ≥ x > 0.2: returns 'Low'
    - 0.2 ≥ x > 0.1: returns 'Very low'
    - 0.1 ≥ x > 0: returns 'Extremely low'
    - x = 0: returns 'Exactly zero'
    - x < 0: returns 'Negative'
    
    For example:
    - The `'shackles'` string has 6 values, two of them are `'s'`. The probability of occurrence of `'s'` is 2/8 = 0.25 =>
    returns `Low`
    - Ratio of 3 to 6 is 3/6 = 0.5 => returns `Exactly half`"""
    def __init__(self, part, total):
        self.part = part
        self.total = total
        try: self.x = self.part / self.total
        except TypeError: self.x = probability_of_occurrence(self.part, self.total)
    def __str__(self):
        if self.x > 1: return 'Excess'
        elif self.x == 1: return 'Full'
        elif self.x > 0.9: return 'Very high'
        elif self.x > 0.8: return 'High'
        elif self.x > 0.7: return 'Pretty high'
        elif self.x > 0.6: return 'Medium-high'
        elif self.x > 0.5: return 'Medium'
        elif self.x == 0.5: return 'Exactly half'
        elif self.x > 0.4: return 'Medium-low'
        elif self.x > 0.3: return 'Pretty low'
        elif self.x > 0.2: return 'Low'
        elif self.x > 0.1: return 'Very low'
        elif self.x > 0: return 'Extremely low'
        elif self.x == 0: return 'Exactly zero'
        else: return 'Negative'
    def __bool__(self):
        if self.x == 0: return False
        else: return True