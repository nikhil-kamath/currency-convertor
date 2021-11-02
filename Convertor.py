from typing import Dict
from forex_python.converter import CurrencyRates
from Deduction import Deduction, FlatDeduction, PercentDeduction
from Transaction import Transaction

class Convertor:
    '''convertor class to keep a deduction dictionary and keep track of all transactions it is used for'''
    def __init__(self, deductions: Dict[str, Deduction] = {}) -> None:
        self.deductions = deductions
        self.receipt = []
        self.c = CurrencyRates()

    def convert(self, c1: str, c2: str, val: float) -> float:
        '''convert val from c1 to c2 using stored deductions and current conversion data from forex-python'''
        conversion_rate = self.c.get_rate(c1, c2)
        initial_conversion = val * conversion_rate
        converted = initial_conversion
        transaction_data = {'index': len(self.receipt), 'start_val': val, 'c1': c1, 'c2': c2, 'raw_end_val': initial_conversion}
        deductions = {}
        for source, d in self.deductions.items():
            converted, removed = d.deduct(converted)
            deductions[source] = removed
        
        transaction_data['deductions'] = deductions
        transaction_data['end_val'] = converted
        t = Transaction(**transaction_data)
        self.receipt.append(t)
        return converted

def main() -> None:
    '''main method'''
    c1 = Convertor({'flat percent': PercentDeduction(.1), 'flat amount': FlatDeduction(10)})
    c2 = Convertor({"flat amount": FlatDeduction(10), "flat percent": PercentDeduction(.1)})
    output = c1.convert('USD', 'INR', 2)
    output2 = c2.convert('USD', 'INR', 2)
    print(output)
    print(output2)
    print(c1.receipt)
    print(c2.receipt)


if __name__ == "__main__":
    main()

