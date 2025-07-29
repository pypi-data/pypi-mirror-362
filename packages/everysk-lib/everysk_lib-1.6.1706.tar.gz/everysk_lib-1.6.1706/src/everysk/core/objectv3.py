###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from types import UnionType
from typing import Any

from everysk.core.exceptions import FieldValueError, RequiredError


class Field:
    ## Private attributes
    _empty_values: frozenset[Any] = frozenset({None, Undefined, '', (), [], {}})
    _always_valid: frozenset[Any] = frozenset({None, Undefined, callable})

    ## Public attributes
    attr_name: str = None
    attr_type: type | UnionType = None
    choices: set[Any] = None
    default: Any = None
    max_value: Any = None
    min_value: Any = None
    readonly: bool = False
    required: bool = False
    required_lazy: bool = False
    empty_is_none: bool = False

    ## Internal methods
    def __init__(self, default: Any = None, *, readonly: bool = False, required: bool = False, **kwargs) -> None:
        if required and kwargs.get('required_lazy'):
            msg = f"{self.attr_name} -> required and required_lazy can't be both True."
            raise FieldValueError(msg)
        self.required = required

        if readonly and default in self._empty_values:
            msg = f'{self.attr_name} -> is readonly then default value is required.'
            raise RequiredError(msg)
        self.readonly = readonly

        # Set all other attributes if they exist in the class
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                msg = f'{self.attr_name} -> invalid attribute: {key}'
                raise FieldValueError(msg)

        # We store the default value already cleaned
        self.default = self.clean_value(default)

    def __get__(self, obj: object, cls: type) -> Any:
        # We will use this var to store the correct place to get the attr_name value
        dct = {}
        # If it is a dict we get it directly
        if isinstance(obj, dict):
            dct = obj
        else:
            # All python objects have the __dict__ attribute except for builtins
            dct = getattr(obj, '__dict__', {})

        # If the value is not in the dict we try to get it from the class
        # We need to use getattr here to raise AttributeError if we can't find the attribute
        value = dct.get(self.attr_name, getattr(cls, self.attr_name))

        if callable(value):
            return value()

        return value

    def __set__(self, obj: object, value: Any) -> None:

    ## Public methods
    def clean_value(self, value: Any) -> Any:
        return value

    def validate(self, value: Any) -> None:
        if self.readonly and value != self.default:
            # This is necessary to be able to at least assign the default value to the field
            msg = f"The field '{self.attr_name}' value cannot be changed."
            raise FieldValueError(msg)

        if self.required and value in self._empty_values:
            msg = f'The {self.attr_name} attribute is required.'
            raise RequiredError(msg)
