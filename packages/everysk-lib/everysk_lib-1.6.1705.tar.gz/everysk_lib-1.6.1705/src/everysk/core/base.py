###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from copy import deepcopy
from inspect import isroutine
from types import GenericAlias, UnionType
from typing import Any, Self

from everysk.core.exceptions import DefaultError, FieldValueError, RequiredError

CLASS_KEY: str = '__class_path__'


class SimpleField:
    ## Private attributes
    _required_empty_values: tuple = (None, Undefined, '', [], {}, set(), frozenset())

    ## Public attributes
    # We set these attributes to Undefined so they can be set later and the field can
    # be initialized properly if it is set to be readonly, required, or has a default value None.
    attr_type: type | UnionType = Undefined
    attr_name: str = Undefined
    choices: set = Undefined
    default: Any = Undefined
    readonly: bool = Undefined
    required: bool = Undefined
    required_lazy: bool = Undefined
    empty_is_none: bool = Undefined

    ## Private methods
    def __init__(
        self,
        default: Any = None,
        *,
        choices: set | None = None,
        readonly: bool = False,
        required: bool = False,
        **kwargs,
    ) -> None:
        required_lazy = kwargs.pop('required_lazy', False)
        if required and required_lazy:
            raise FieldValueError("Required and required_lazy can't be both True.")

        # Set additional attributes from kwargs first because
        # they can change the value of the other attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.choices = set(choices) if choices else set()
        self.empty_is_none = kwargs.pop('empty_is_none', False)
        self.readonly = readonly
        self.required = required
        self.required_lazy = required_lazy

        # We use a function to clean the default value so we must set it after the other attributes
        self.default = self._clean_default(default)

        # We need to validate the default value if it is set
        # on init we do not validate by required because it can be set to Undefined or None
        if self.default is not None and self.default is not Undefined:
            self.validate(self.default)

        if readonly and (self.default is Undefined or self.default is None):
            raise RequiredError('If field is readonly, then default value is required.')

    def __eq__(self, value: object) -> bool:
        if isinstance(value, type(self)):
            # If the object is of the same type, we compare the attributes
            return self.__dict__ == value.__dict__

        return False

    def __getattr__(self, name: str) -> Any:
        # https://pythonhint.com/post/2118347356810295/avoid-pylint-warning-e1101-instance-of-has-no-member-for-class-with-dynamic-attributes
        if not isinstance(self.attr_type, UnionType):
            return getattr(self.attr_type, name)

        # We try to get the attribute from the ones that are in the tuple
        for attr_type in getattr(self.attr_type, '__args__', []):
            try:
                return getattr(attr_type, name)
            except AttributeError:
                pass

        # If no attribute was found we raise the error
        msg = f"type object '{self.attr_type}' has no attribute '{name}'."
        raise AttributeError(msg)

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)

    def __setattr__(self, name: str, value: Any) -> None:
        # If the field is readonly, we could not change its values
        if self.readonly:
            old_value = getattr(self, name, Undefined)
            if old_value is not Undefined and old_value != value:
                self._raise_readonly_error()

        return super().__setattr__(name, value)

    def __str__(self) -> str:
        return str(self.default)

    def __repr__(self) -> str:
        cls = type(self)
        return cls.__name__

    def _clean_default(self, value: Any) -> Any:
        value = self.clean_value(value)

        if isinstance(value, (list, dict)) and not value:
            # For default values they can't be empty [] or {} - because this can cause
            # some issues with class attributes where these type can aggregate values.
            raise DefaultError('Default value cannot be a list or a dict.')

        return value

    ## Validation methods
    def _validate_attr_type(self, value: Any) -> None:  # pylint: disable=inconsistent-return-statements
        # We always accept these 3
        if value is None or value is Undefined or self.attr_type is Any:
            return

        # If attr_type is string, we check if the class name matches
        if isinstance(self.attr_type, str) and type(value).__name__ == self.attr_type:
            return

        # For subscriptable types like List, Dict, Tuple, etc.
        # We need to check if the value is a instance of the origin type
        # We not check the content of the list, dict, tuple, etc
        if isinstance(self.attr_type, GenericAlias):
            attr_type = self.attr_type.__origin__
        else:
            attr_type = self.attr_type

        if isinstance(value, attr_type):
            return

        self._raise_attr_type_error()

    def _validate_choices(self, value: Any) -> None:
        if value not in self.choices:
            self._raise_choices_error(value)

    def _validate_readonly(self, value: Any) -> None:
        # This is necessary to be able to at least assign the default value to the field
        if value != self.default:
            self._raise_readonly_error()

    def _validate_required(self, value: Any) -> None:
        if value in self._required_empty_values:
            self._raise_required_error()

    ## Raise methods
    def _raise_attr_type_error(self) -> None:
        msg = f'Key {self.attr_name} must be {self.attr_type}.'
        raise FieldValueError(msg)

    def _raise_choices_error(self, value: Any) -> None:
        msg = f"The value '{value}' for field '{self.attr_name}' must be in this list {self.choices}."
        raise FieldValueError(msg)

    def _raise_readonly_error(self) -> None:
        msg = f"The field '{self.attr_name}' value cannot be changed."
        raise FieldValueError(msg)

    def _raise_required_error(self) -> None:
        msg = f'The {self.attr_name} attribute is required.'
        raise RequiredError(msg)

    ## Public methods
    def clean_value(self, value: Any) -> Any:
        if self.empty_is_none and value == '':
            return None

        return value

    def validate(self, value: Any) -> None:
        # Required validation is always first to ensure that the field is not empty
        if not self.required_lazy and self.required:
            self._validate_required(value)

        # Run the other validations
        self._validate_attr_type(value)
        if self.choices:
            self._validate_choices(value)

        if self.readonly:
            self._validate_readonly(value)


class MetaSimpleObject(type):
    def __new__(mcs, name: str, bases: tuple, attrs: dict) -> Self:
        # Compute all attributes from the class and its bases
        attributes = {}
        # Bases are only the classes that are directly inherited from
        for cls in bases:
            # They have already been processed and have their attributes set
            attributes.update(getattr(cls, '_attributes', None) or {})

        # Add the attributes from the current class
        # We get all fields from the class annotations
        annotations = attrs.get('__annotations__', {})
        for key, value in annotations.items():
            # All annotations are types, so we need to create a SimpleField for each one
            field = SimpleField(attr_type=value, default=attrs.get(key), attr_name=key)
            # After the field is created, we need to set it in the class if it is not already set
            if key not in attrs:
                attrs[key] = field.default

            attributes[key] = field

        # We need to add the attributes that are not in the annotations
        for key in attrs.keys() - annotations.keys():
            # We need to discard python builtins and class methods/properties
            if not key.startswith('__') and not isroutine(value) and not isinstance(value, property):
                value = attrs.get(key, Undefined)
                # If the value is not a SimpleField, we create a new one
                if not isinstance(value, SimpleField):
                    value = SimpleField(attr_type=type(value), default=value, attr_name=key)
                else:
                    # If the value is a SimpleField, we need to set the attr_name
                    value.attr_name = key

                # And update the value in the attributes dictionary
                attrs[key] = value.default

                # We set the field in the attributes dictionary
                attributes[key] = value

        # Add the attributes as an attribute to the class
        attrs['_attributes'] = attributes

        return super().__new__(mcs, name, bases, attrs)

    def __setattr__(cls, name: str, value: Any) -> None:
        # if the attribute exists in the _attributes dictionary, we need to validate it
        if name in cls._attributes:
            # First we need to clean the value
            value = cls._attributes[name].clean_value(value)
            # Then we validate the value
            cls._attributes[name].validate(value)

        return super().__setattr__(name, value)


class SimpleObject(dict, metaclass=MetaSimpleObject):
    ## Private attributes
    # The _attributes is set by the metaclass when the class is created we put it here
    # to be able to access it in the instance methods and for autocomplete works.
    _attributes: dict[str, SimpleField]
    _errors: dict[str, Exception] = None
    _invalid_key_names: frozenset[str] = frozenset([])
    _need_validation: bool = True
    _silent: bool = False
    _to_dict_exclude_keys: frozenset[str] = frozenset([])
    _to_dict_key_mapping: dict[str, str] = None

    ## Init methods
    def __before_init__(self, **kwargs) -> dict:
        return kwargs

    def __init_attributes__(self) -> None:
        # Initialize attributes that are not part of the dictionary
        if self._errors is None:
            self._errors = {}

        if self._to_dict_key_mapping is None:
            self._to_dict_key_mapping = {}

    def __init_kwargs__(self, **kwargs) -> None:
        # Get all default keys from the class attributes
        # Remove the keys that are already in kwargs
        # and remove the keys that are already set in the instance
        keys = self._attributes.keys() - kwargs.keys() - self.__dict__.keys()
        kwargs.update({key: getattr(self, key, None) for key in keys})
        return kwargs

    def __init__(self, *args, **kwargs) -> None:
        # Transform args and kwargs into a dictionary to better handle them
        kwargs = dict(*args, **kwargs)
        self._silent = kwargs.pop('silent', kwargs.pop('_silent', False))

        # Call the before_init method to allow subclasses to modify kwargs
        try:
            self.__init_attributes__()
            kwargs = self.__init_kwargs__(**kwargs)
            kwargs = self.__before_init__(**kwargs)
        except Exception as error:  # pylint: disable=broad-exception-caught
            if not self._silent:
                raise error
            self._errors['before_init'] = deepcopy(error)

        # Validate the keys in kwargs
        try:
            # Remove all private keys from kwargs
            private_keys = {k for k in kwargs if self._is_invalid_key(k)}
            for key in private_keys:
                setattr(self, key, kwargs.pop(key))

            # We need to check if the values are valid before setting them
            kwargs = {k: self._clean_and_validate_value(k, v) for k, v in kwargs.items()}

            # Initialize the dictionary with the remaining keys
            super().__init__(**kwargs)

        except Exception as error:  # pylint: disable=broad-exception-caught
            if not self._silent:
                raise error
            self._errors['init'] = deepcopy(error)

        # Call the after_init method to allow subclasses to perform additional initialization
        try:
            self.__after_init__()
        except Exception as error:  # pylint: disable=broad-exception-caught
            if not self._silent:
                raise error
            self._errors['after_init'] = deepcopy(error)

    def __after_init__(self) -> None:
        pass

    ## Internal methods
    def __delattr__(self, name: str) -> None:
        if name in self:
            del self[name]
        else:
            super().__delattr__(name)

    def __getattribute__(self, name):
        # This is to keep the values only accessible through the dictionary
        if name in self:
            return self[name]

        return super().__getattribute__(name)

    def __getitem__(self, key: str) -> Any:
        if self._is_invalid_key(key):
            raise KeyError(f"Invalid key: '{key}'.")

        return super().__getitem__(key)

    def __setattr__(self, name: str, value: Any) -> None:
        # Not valid keys are set directly on the instance
        if self._is_invalid_key(name):
            value = self._clean_and_validate_value(name, value)
            super().__setattr__(name, value)
        else:
            # Public keys are set in the dictionary
            self[name] = value

    def __setitem__(self, key, value):
        if self._is_invalid_key(key):
            raise KeyError(f"Invalid key: '{key}'.")

        value = self._clean_and_validate_value(key, value)
        return super().__setitem__(key, value)

    ## Private methods
    def _clean_and_validate_value(self, key: str, value: Any) -> Any:
        if key in self._attributes:
            # First we clean the value
            value = self._attributes[key].clean_value(value)

            # Then we validate the value if needed
            if self._need_validation:
                self._attributes[key].validate(value)

        return value

    def _is_invalid_key(self, key: str) -> bool:
        return key.startswith('_') or key in self._invalid_key_names

    @classmethod
    def _get_full_doted_class_path(cls) -> str:
        return f'{cls.__module__}.{cls.__name__}'

    ## Public methods
    def copy(self) -> Self:
        return deepcopy(self)

    def fromkeys(self, keys: list, default: Any = None) -> dict:
        cls = type(self)
        return cls({key: self.get(key, getattr(self, key, default)) for key in keys})

    def get_full_doted_class_path(self) -> str:
        cls = type(self)
        return cls._get_full_doted_class_path()  # pylint: disable=protected-access

    def to_dict(self, add_class_path: bool = False, recursion: bool = False) -> dict:
        dct = {}
        for key, value in self.items():
            if key in self._to_dict_exclude_keys:
                continue

            if recursion and isinstance(value, SimpleObject):
                value = value.to_dict(add_class_path=add_class_path, recursion=recursion)

            func = getattr(self, f'_process_{key}', None)
            if callable(func):
                value = func(value)

            mapped_key = self._to_dict_key_mapping.get(key, key)
            dct[mapped_key] = value

        if add_class_path:
            dct[CLASS_KEY] = self.get_full_doted_class_path()

        return dct

    def update(self, *args, **kwargs):
        dct = dict(*args, **kwargs)
        has_invalid_keys = [key for key in dct if self._is_invalid_key(key)]
        if has_invalid_keys:
            raise KeyError(f'Invalid keys: {", ".join(has_invalid_keys)}.')

        super().update(*args, **kwargs)

    def validate_required_fields(self) -> None:
        for key, field in self._attributes.items():
            if getattr(field, 'required_lazy', False):
                field._validate_required(getattr(self, key, Undefined))  # pylint: disable=protected-access
