import pydantic
from typing import Dict

class InconsistentDeductionException(Exception):
    '''exception raised when deduction values do not add up to total deduction between end values'''

    def __init__(self, evu: float, ev: float, deductions: Dict) -> None:
        self.evu = evu
        self.ev = ev
        self.deductions = deductions
        self.message = f"Inconsistent deductions: {evu} deduced to {ev} with deduction values {deductions}"
        super().__init__(self.message)


class InvalidCurrencyTag(Exception):
    '''exception raised when currency tag is not 3 characters long'''

    def __init__(self, tag: str) -> None:
        self.message = f"Currency tag {tag} is not 3 characters long"
        super().__init__(self.message)


class Transaction(pydantic.BaseModel):
    '''immutable class containing transaction info, including all deduction sources and values
    contains error checking for deductions and currency tags'''
    class Config:
        frozen = True

    index: int
    c1: str
    c2: str
    start_val: float
    end_val: float
    raw_end_val: float = -1
    deductions: Dict = {}

    def __init__(self, **kwargs):
        '''if no raw value is given, default it to the end value'''
        if "raw_end_val" not in kwargs:
            kwargs["raw_end_val"] = kwargs["end_val"]
        super().__init__(**kwargs)

    @pydantic.root_validator()
    @classmethod
    def check_deductions(cls, kwargs):
        '''check to ensure that all deductions are accounted for in the deductions field, and that:
        1) end val is not different from raw end val without any deduction argument
        2) the sum of the deductions add up to the total deduction'''
        if "raw_end_val" not in kwargs:
            return kwargs

        if "deductions" not in kwargs:  # if there are no deductions, make sure that end val was not changed
            if kwargs["raw_end_val"] != kwargs["end_val"]:
                raise InconsistentDeductionException(
                    kwargs["raw_end_val"], kwargs["end_val"], {})
            else:
                return kwargs

        if abs(kwargs["raw_end_val"] - kwargs["end_val"] - sum(kwargs["deductions"].values())) > 0.00000000001:
            raise InconsistentDeductionException(
                kwargs["raw_end_val"], kwargs["end_val"], kwargs["deductions"])

        return kwargs

    @pydantic.validator("c1", "c2")
    @classmethod
    def check_currency_tag(cls, tag):
        '''validates tags to be 3 characters long'''
        if len(tag) != 3:
            raise InvalidCurrencyTag(tag)
        return tag
