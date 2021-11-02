from abc import ABC, abstractmethod
from typing import Tuple

class DeductionException(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)

class Deduction(ABC):
    '''abstract class representing deductions'''    
    @abstractmethod
    def deduct(self, val: float) -> Tuple[float, float]:
        '''abstract method calculate a deduction given a certain value. returns a tuple (output value, amount removed)'''
        pass

class FlatDeduction(Deduction):
    '''class to deduct a flat amount from all input values'''
    def __init__(self, amount: float) -> None:
        '''constructor'''
        self.amount = amount
        super().__init__()
    
    def deduct(self, val: float) -> Tuple[float, float]:
        '''deducts self.amount from val. raises DeductionException if result is negative'''
        to_return = (val-self.amount, self.amount)
        if to_return[0] < 0:
            raise DeductionException(f"deducting {self.amount} from {val} gives negative value")
        
        return to_return

class PercentDeduction(Deduction):
    '''class to deduct a percentage amount from all input values'''
    def __init__(self, percent: float) -> None:
        '''constructor. raises exception if percent is greater than 1'''
        if percent > 1:
            raise DeductionException(f"deduction with percent {percent} is greater than 1")

        self.percent = percent
        super().__init__()
    
    def deduct(self, val: float) -> Tuple[float, float]:
        '''deducts self.percent * val from val.'''
        return (val - val * self.percent, val * self.percent)


