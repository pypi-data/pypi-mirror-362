"""Module for type enforcement methods."""

from __future__ import annotations

import contextlib
import functools
import inspect
import platform
import typing
import warnings
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, ForwardRef, Union

if TYPE_CHECKING:
    from typing import (
        Any,
        Callable,
        Dict,
        Iterable,
        List,
        Optional,
        Type,
        TypeVar,
    )

    T = TypeVar("T")
    DecoratorMethod = Callable[..., T]

from packaging.specifiers import SpecifierSet
from packaging.version import Version

try:
    import typeguard
except ImportError:
    typeguard = None

from .constructor_map import _get_mastapy_type_from_module_code
from .exceptions import CastException, TypeCheckException
from .utility import qualname

_typeguard_warning_raised = False


class TypeCheckingDisabledWarning(UserWarning):
    """Warning raised if the type checking is disabled."""


class CallableType(Enum):
    """Type of callable."""

    METHOD = auto()
    PROPERTY = auto()


@dataclass(frozen=True)
class InvalidArgument:
    """Dataclass for holding invalid argument information.

    Args:
        name (str): Name of the invalid argument.
        received_type (Type): Received type of the argument.
        expected_type (Iterable[Type]): Type the argument was expected to be.
    """

    name: str
    received_type: "Type"
    expected_types: "Iterable[Type]"

    @property
    def formatted_expected_type(self) -> str:
        """Get the expected type for printing.

        Returns:
            str
        """
        expected_types = list(self.expected_types)

        def formatted_name(type_: "Type") -> str:
            module = getattr(type_, "__module__", None)

            if module == "typing":
                try:
                    origin = typing.get_origin(type_)

                    if origin is None:
                        return str(type_)
                except AttributeError:
                    return str(type_)

                original_name = f"{type_.__module__}.{qualname(type_)}"
                new_name = qualname(origin)
                return str(type_).replace(original_name, new_name, 1)

            return qualname(type_)

        if len(expected_types) == 1:
            return formatted_name(expected_types[0])
        else:
            last = formatted_name(expected_types[-1])
            types = map(formatted_name, expected_types[:-1])
            return f"{', '.join(types)} or {last}"

    @property
    def formatted_types(self) -> str:
        """Get the types formatted for printing.

        Returns:
            str
        """
        received_type = qualname(self.received_type)
        expected_type = self.formatted_expected_type

        return f"(Received: {received_type}; Expected: {expected_type})"

    def __str__(self) -> str:
        """__str__ overload.

        Returns:
            str
        """
        return f"{self.name} {self.formatted_types}"


@functools.lru_cache(maxsize=None)
def _try_evaluate_mastapy_type(input: str) -> "Union[Type, str]":
    try:
        module_name, _ = input.strip("'").rsplit(".")
        return _get_mastapy_type_from_module_code(module_name)
    except (ValueError, CastException):
        return input


def _evaluate_forward_ref(input: "ForwardRef") -> "Type":
    with contextlib.suppress(TypeError):
        return input._evaluate(
            globals(), locals(), type_params=None, recursive_guard=frozenset()
        )

    with contextlib.suppress(TypeError):
        return input._evaluate(globals(), locals(), recursive_guard=frozenset())

    with contextlib.suppress(TypeError):
        return input._evaluate(globals(), locals(), frozenset())

    with contextlib.suppress(TypeError):
        return input._evaluate(globals(), locals())


def _try_evaluate_forward_ref(input: str) -> "Union[Type, str]":
    try:
        return _evaluate_forward_ref(ForwardRef(input))
    except NameError:
        return _try_evaluate_mastapy_type(input)


def _get_callable_type(func: "DecoratorMethod") -> CallableType:
    module = inspect.getmodule(func)
    qualified_name = qualname(func)
    class_name = qualified_name.split(".<locals>", 1)[0].rsplit(".", 1)[0]
    cls = getattr(module, class_name, None)

    if cls is None:
        return CallableType.METHOD

    method = getattr(cls, func.__name__, None)

    if method is None:
        return CallableType.METHOD

    is_property = isinstance(method, property)
    return CallableType.PROPERTY if is_property else CallableType.METHOD


def _check_invalid_typing(
    name: str, value: "Any", type_: "Union[Type, str]"
) -> "Optional[InvalidArgument]":
    if isinstance(type_, str):
        return

    from .implicit.overridable import Overridable_bool

    if isinstance(value, bool) and type_ == Overridable_bool:
        return

    try:
        typeguard.check_type(
            value, type_, forward_ref_policy=typeguard.ForwardRefPolicy.IGNORE
        )
    except typeguard.TypeCheckError:
        with contextlib.suppress(AttributeError):
            is_union = typing.get_origin(type_) == Union

            if is_union:
                args = typing.get_args(type_)
                return InvalidArgument(name, type(value), args)

        return InvalidArgument(name, type(value), (type_,))


def _get_annotations(func: "DecoratorMethod") -> "Dict[str, Union[Type, str]]":
    try:
        annotations = typing.get_type_hints(func)
        annotations.pop("return", None)
        return annotations
    except NameError:
        signature = inspect.signature(func)
        parameters = dict(signature.parameters)

        return {
            key: _try_evaluate_forward_ref(value.annotation)
            for key, value in parameters.items()
        }


def enforce_parameter_types(func):
    """Decorate method and enforce the types of all arguments.

    Note:
        This decorator operates lazily and only enforces if a type error or
        value error occurs. That way we can attempt to internally convert
        arguments to the correct type first.
    """

    @functools.wraps(func)
    def wrapper_enforce_parameter_types(*args: "Any", **kwargs: "Any") -> "T":
        global _typeguard_warning_raised

        try:
            return func(*args, **kwargs)
        except (TypeError, ValueError):
            if typeguard is None:
                if _typeguard_warning_raised:
                    raise

                python_version = Version(platform.python_version())
                message = (
                    "The type checking has been disabled because the "
                    "typeguard package could not be found."
                )

                if python_version in SpecifierSet("<3.7.4"):
                    message += (
                        " Mastapy does not support type checking in "
                        "versions of Python less than 3.7.4. Consider "
                        "updating Python to enable this feature."
                    )

                warnings.warn(message, TypeCheckingDisabledWarning, stacklevel=2)
                _typeguard_warning_raised = True
                raise

            callable_type = _get_callable_type(func)
            annotations = _get_annotations(func)

            if annotations.pop("self", None) is not None:
                args = args[1:]

            num_args = len(args)
            invalid_args: "List[InvalidArgument]" = []

            for i, (name, type_) in enumerate(annotations.items()):
                if i >= num_args:
                    break

                result = _check_invalid_typing(name, args[i], type_)
                if result is not None:
                    invalid_args.append(result)

            for name, value in kwargs.items():
                type_ = annotations.get(name, None)

                if type_ is None:
                    continue

                result = _check_invalid_typing(name, value, type_)
                if result is not None:
                    invalid_args.append(result)

            if not any(invalid_args):
                raise

            if callable_type == CallableType.METHOD:
                formatted_args = "\n".join(map(str, invalid_args))
                message = (
                    f"Attempted to call a mastapy method using arguments "
                    "with unexpected types. The following arguments "
                    f"were invalid:\n{formatted_args}"
                )
            else:
                message = (
                    "Attempted to set a mastapy property with a value of an "
                    f"unexpected type {invalid_args[0].formatted_types}"
                )

            raise TypeCheckException(message) from None

    return wrapper_enforce_parameter_types
