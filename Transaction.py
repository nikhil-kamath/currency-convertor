import pydantic
from typing import Dict

class InconsistentTaxException(Exception):
    '''exception raised when tax values do not add up to total deduction between end values'''

    def __init__(self, evu: float, ev: float, tax: Dict) -> None:
        self.evu = evu
        self.ev = ev
        self.tax = tax
        self.message = f"Inconsistent taxation: {evu} taxed to {ev} with tax values {tax}"
        super().__init__(self.message)


class InvalidCurrencyTag(Exception):
    '''exception raised when currency tag is not 3 characters long'''

    def __init__(self, tag: str) -> None:
        self.message = f"Currency tag {tag} is not 3 characters long"
        super().__init__(self.message)


class Transaction(pydantic.BaseModel):
    '''immutable class containing transaction info, including all tax sources as monetary values (not percentages)
    contains error checking for tax and currency tags'''
    class Config:
        frozen = True

    index: int
    c1: str
    c2: str
    start_val: float
    end_val: float
    end_val_untaxed: float = -1
    tax: Dict = {}

    def __init__(self, **kwargs):
        '''if no untaxed value is given, default it to the end value'''
        if "end_val_untaxed" not in kwargs:
            kwargs["end_val_untaxed"] = kwargs["end_val"]
        super().__init__(**kwargs)

    @pydantic.root_validator()
    @classmethod
    def check_tax(cls, kwargs):
        '''check to ensure that all deductions are accounted for in the tax field, and that:
        1) end val is not different from end val untaxed without any tax argument
        2) the sum of the taxes add up to the total deduction'''
        if "end_val_untaxed" not in kwargs:
            return kwargs

        if "tax" not in kwargs:  # if there is no tax, make sure that end val was not changed
            if kwargs["end_val_untaxed"] != kwargs["end_val"]:
                raise InconsistentTaxException(
                    kwargs["end_val_untaxed"], kwargs["end_val"], {})
            else:
                return kwargs

        if abs(kwargs["end_val_untaxed"] - kwargs["end_val"] - sum(kwargs["tax"].values())) > 0.00000000001:
            raise InconsistentTaxException(
                kwargs["end_val_untaxed"], kwargs["end_val"], kwargs["tax"])

        return kwargs

    @pydantic.validator("c1", "c2")
    @classmethod
    def check_currency_tag(cls, tag):
        '''validates tags to be 3 characters long'''
        if len(tag) != 3:
            raise InvalidCurrencyTag(tag)
        return tag
