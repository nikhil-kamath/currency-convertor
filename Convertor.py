from typing import Dict
from forex_python.converter import CurrencyRates
from Transaction import Transaction

class Convertor:
    '''convertor class to keep a tax dictionary with *percentages* and keep track of all transactions it is used for'''
    def __init__(self, tax: Dict = {}) -> None:
        self.tax = tax
        self.receipt = []
        self.c = CurrencyRates()

    def convert(self, c1: str, c2: str, val: float) -> float:
        '''convert val from c1 to c2 using stored constant tax rates and current conversion data from forex-python'''
        conversion_rate = self.c.get_rate(c1, c2)
        initial_conversion = val * conversion_rate
        converted = initial_conversion
        transaction_data = {'index': len(self.receipt), 'start_val': val, 'c1': c1, 'c2': c2, 'end_val_untaxed': initial_conversion}
        taxes = {}
        for source, percent in self.tax.items():
            deduction = initial_conversion * percent
            converted -= deduction
            taxes[source] = deduction
        
        transaction_data['tax'] = taxes
        transaction_data['end_val'] = converted
        t = Transaction(**transaction_data)
        self.receipt.append(t)
        return converted




def main() -> None:
    '''main method'''
    c1 = Convertor({'flat percent': .1})
    output = c1.convert('USD', 'INR', 2)
    print(output)
    print(c1.receipt)


if __name__ == "__main__":
    main()

