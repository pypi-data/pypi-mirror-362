"""Module for list with selected item typing and logic."""

from typing import TYPE_CHECKING, Generic, TypeVar

from mastapy._private._internal.mixins import ListWithSelectedItemMixin
from mastapy._private._internal.utility import qualname

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Sequence, Tuple, Type, Union

    from mastapy import APIBase

    Self_ListWithSelectedItemMeta = TypeVar(
        "Self_ListWithSelectedItemMeta", bound="_ListWithSelectedItemMeta"
    )
    Self_ListWithSelectedItem = TypeVar(
        "Self_ListWithSelectedItem", bound="ListWithSelectedItem"
    )
    Self_ListWithSelectedItemBase = TypeVar(
        "Self_ListWithSelectedItemBase", bound="_ListWithSelectedItemBase"
    )

    Self_Int = TypeVar("Self_Int", bound="ListWithSelectedItem.Int")
    Self_Float = TypeVar("Self_Float", bound="ListWithSelectedItem.Float")
    Self_Complex = TypeVar("Self_Complex", bound="ListWithSelectedItem.Complex")
    Self_Str = TypeVar("Self_Str", bound="ListWithSelectedItem.Str")
    Self_Bool = TypeVar("Self_Bool", bound="ListWithSelectedItem.Bool")

T = TypeVar("T")

__all__ = ("ListWithSelectedItem",)


def _mutate_mastapy_class(
    cls: "Type[Any]", value: "Any", items: "Optional[Sequence[Any]]" = None
) -> "Any":
    class_ = value.__class__
    class_name = qualname(class_)
    class_bases = class_, _ListWithSelectedItemBase
    class_dict = dict(class_.__dict__)

    def _init(
        self: "Self_ListWithSelectedItemBase",
        value: "Any",
        items: "Optional[Sequence[Any]]",
    ):
        if isinstance(value, ListWithSelectedItemMixin):
            value = value.selected_value

        class_.__init__(self, value.wrapped)
        _ListWithSelectedItemBase.__init__(self, value, items)

    class_dict["__init__"] = _init

    mutated_class = type(class_name, class_bases, class_dict)
    return mutated_class(value, items)


class _ListWithSelectedItemMeta(type):
    def __init__(
        self: "Any",
        name: str,
        bases: "Tuple[type]",
        dict_: "Dict[str, Any]",
    ) -> None:
        if not len(bases):
            return

        from mastapy import APIBase

        if not issubclass(self, APIBase):
            raise Exception(
                "Cannot create a custom ListWithSelectedItem type using a non-API type."
            ) from None

        self.__new__ = _mutate_mastapy_class


class _ListWithSelectedItemBase(Generic[T], ListWithSelectedItemMixin):
    def __init__(
        self: "Self_ListWithSelectedItemBase",
        value: T,
        items: "Optional[Sequence[T]]" = None,
    ) -> None:
        object.__setattr__(self, "__value__", value)

        if items is None:
            items = []

        items = list(items)

        if value not in items:
            items.append(value)

        object.__setattr__(self, "__items__", items)

    @property
    def available_values(self: "Self_ListWithSelectedItemBase") -> "List[T]":
        """All available values in the list.

        Returns:
            list[T]
        """
        return self.__items__

    @property
    def selected_value(self: "Self_ListWithSelectedItemBase") -> "T":
        """The currently selected value in the list.

        Returns:
            T
        """
        return self.__value__


class ListWithSelectedItemInstantiationError(Exception):
    """Exception raised if the list with selected item fails to instantiate."""


class ListWithSelectedItem(metaclass=_ListWithSelectedItemMeta):
    """List with selected item type.

    Note:
        This should only be used as a type. Attempts to instantiate this class will
        result in an error.

    Examples:
        Use this as a return type in scripted properties. Values will be automatically
        converted to a list with selected item.

            >>> from mastapy import masta_property, ListWithSelectedItem
            >>> @masta_property(...)
            >>> def my_property(...) -> ListWithSelectedItem:
            >>>     return 5.0

        If you want type hints, you can either use a premade type:

            >>> @my_property.setter
            >>> def my_property(..., value: ListWithSelectedItem.Float) -> None:
            >>>     ...

        Or you can create your own type.

            >>> class ListWithSelectedItemDatum(Datum, ListWithSelectedItem):
            >>>     pass
            >>>
            >>> @my_property.setter
            >>> def my_property(..., value: ListWithSelectedItemDatum) -> None:
            >>>     ...
    """

    def __init__(self: "Self_ListWithSelectedItem") -> None:
        raise ListWithSelectedItemInstantiationError(
            "This class must only be used for type hinting and cannot be instantiated. "
            "See the examples in the class documentation for how to use this correctly."
        ) from None

    @property
    def available_values(self: "Self_ListWithSelectedItem") -> "List[APIBase]":
        """All available values in the list.

        Returns:
            list[APIBase]
        """
        return self.__items__

    @property
    def selected_value(self: "Self_ListWithSelectedItem") -> "APIBase":
        """The currently selected value in the list.

        Returns:
            APIBase
        """
        return self.__value__

    class Int(int, _ListWithSelectedItemBase[int]):
        """A premade type for ListWithSelectedItem integers.

        Example:
            >>> from mastapy import masta_property, ListWithSelectedItem
            >>> @masta_property(...)
            >>> def my_property(...) -> ListWithSelectedItem.Int:
            >>>     return 5
        """

        def __new__(
            cls: "Type[ListWithSelectedItem.Int]",
            value: int,
            items: "Optional[Sequence[int]]" = None,
        ) -> int:
            try:
                return int.__new__(cls, value)
            except ValueError:
                raise ListWithSelectedItemInstantiationError(
                    "This object must be instantiated with int values."
                ) from None

        def __init__(
            self: "Self_Int", value: int, items: "Optional[Sequence[int]]" = None
        ) -> None:
            try:
                if items is not None:
                    items = list(map(int, items))

                _ListWithSelectedItemBase.__init__(self, int(value), items)
            except ValueError:
                raise ListWithSelectedItemInstantiationError(
                    "This object must be instantiated with int values."
                ) from None

    class Float(float, _ListWithSelectedItemBase[float]):
        """A premade type for ListWithSelectedItem floats.

        Example:
            >>> from mastapy import masta_property, ListWithSelectedItem
            >>> @masta_property(...)
            >>> def my_property(...) -> ListWithSelectedItem.Float:
            >>>     return 5.0
        """

        def __new__(
            cls: "Type[ListWithSelectedItem.Float]",
            value: float,
            items: "Optional[Sequence[float]]" = None,
        ) -> float:
            try:
                return float.__new__(cls, value)
            except ValueError:
                raise ListWithSelectedItemInstantiationError(
                    "This object must be instantiated with float values."
                ) from None

        def __init__(
            self: "Self_Float", value: float, items: "Optional[Sequence[float]]" = None
        ) -> None:
            try:
                if items is not None:
                    items = list(map(float, items))

                _ListWithSelectedItemBase.__init__(self, float(value), items)
            except ValueError:
                raise ListWithSelectedItemInstantiationError(
                    "This object must be instantiated with float values."
                ) from None

    class Complex(complex, _ListWithSelectedItemBase[complex]):
        """A premade type for ListWithSelectedItem complex numbers.

        Example:
            >>> from mastapy import masta_property, ListWithSelectedItem
            >>> @masta_property(...)
            >>> def my_property(...) -> ListWithSelectedItem.Complex:
            >>>     return complex(2.0, 3.0)
        """

        def __new__(
            cls: "Type[ListWithSelectedItem.Complex]",
            value: complex,
            items: "Optional[Sequence[complex]]" = None,
        ) -> complex:
            try:
                return complex.__new__(cls, value.real, value.imag)
            except AttributeError:
                raise Exception(
                    "This object must be instantiated with complex values."
                ) from None

        def __init__(
            self: "Self_Complex",
            value: complex,
            items: "Optional[Sequence[complex]]" = None,
        ) -> None:
            try:
                value = complex(value.real, value.imag)

                if items is not None:
                    items = [complex(x.real, x.imag) for x in items]
            except AttributeError:
                raise Exception(
                    "This object must be instantiated with complex values."
                ) from None

            _ListWithSelectedItemBase.__init__(self, complex(value), items)

    class Str(str, _ListWithSelectedItemBase[str]):
        """A premade type for ListWithSelectedItem strings.

        Example:
            >>> from mastapy import masta_property, ListWithSelectedItem
            >>> @masta_property(...)
            >>> def my_property(...) -> ListWithSelectedItem.Str:
            >>>     return "Hello world!"
        """

        def __new__(
            cls: "Type[ListWithSelectedItem.Str]",
            value: str,
            items: "Optional[Sequence[str]]" = None,
        ) -> str:
            try:
                return str.__new__(cls, value)
            except ValueError:
                raise ListWithSelectedItemInstantiationError(
                    "This object must be instantiated with str values."
                ) from None

        def __init__(
            self: "Self_Str",
            value: str,
            items: "Optional[Sequence[str]]" = None,
        ) -> None:
            try:
                if items is not None:
                    items = list(map(str, items))

                _ListWithSelectedItemBase.__init__(self, str(value), items)
            except ValueError:
                raise ListWithSelectedItemInstantiationError(
                    "This object must be instantiated with str values."
                ) from None

    class Bool(_ListWithSelectedItemBase[bool]):
        """A premade type for ListWithSelectedItem bools.

        Example:
            >>> from mastapy import masta_property, ListWithSelectedItem
            >>> @masta_property(...)
            >>> def my_property(...) -> ListWithSelectedItem.Bool:
            >>>     return True
        """

        def __init__(
            self: "Self_Bool",
            value: bool,
            items: "Optional[Sequence[bool]]" = None,
        ) -> None:
            try:
                if items is not None:
                    items = list(map(bool, items))

                _ListWithSelectedItemBase.__init__(self, bool(value), items)
            except ValueError:
                raise ListWithSelectedItemInstantiationError(
                    "This object must be instantiated with bool values."
                ) from None

        def __bool__(self: "Self_Bool") -> bool:
            """Override of the bool magic method.

            Returns:
                bool
            """
            return self.selected_value

        def __str__(self: "Self_Bool") -> str:
            """Override of the str magic method.

            Returns:
                str
            """
            return str(self.selected_value)

        def __repr__(self: "Self_Bool") -> str:
            """Override of the repr magic method.

            Returns:
                str
            """
            return str(self.selected_value)


if TYPE_CHECKING:
    ExpectedType = Union[Type[ListWithSelectedItem], Type[ListWithSelectedItemMixin]]


class ListWithSelectedItemPromotionException(Exception):
    """Exception raised if a type cannot be promoted to a list with selected item."""


def promote_to_list_with_selected_item(
    value: "T",
    items: "Sequence[T]" = [],
    expected_type: "ExpectedType" = ListWithSelectedItem,
) -> "Optional[ListWithSelectedItemMixin]":
    """Automatically promote a value to a ListWithSelectedItem type if possible.

    Note:
        This returns None if the promotion fails.

    Args:
        value (T): The value to promote.
        items (Sequence[T]): Available values to promote.
        expected_type (type[ListWithSelectedItem] | type[ListWithSelectedItemMixin]):
            The expected type to promote the value to.

    Returns:
        ListWithSelectedItemMixin | None
    """
    from mastapy._private._internal.sentinels import ListWithSelectedItem_None

    if (
        value is None
        or isinstance(value, ListWithSelectedItem_None)
        or isinstance(value, ListWithSelectedItemMixin)
    ):
        return value

    if expected_type is ListWithSelectedItem:
        if isinstance(value, int):
            return ListWithSelectedItem.Int(value, items)
        elif isinstance(value, float):
            return ListWithSelectedItem.Float(value, items)
        elif isinstance(value, complex):
            return ListWithSelectedItem.Complex(value, items)
        elif isinstance(value, str):
            return ListWithSelectedItem.Str(value, items)
        elif isinstance(value, bool):
            return ListWithSelectedItem.Bool(value, items)
        else:
            from mastapy import APIBase

            if isinstance(value, APIBase):
                return _mutate_mastapy_class(expected_type, value, items)

    if not isinstance(value, ListWithSelectedItemMixin) and (
        isinstance(value, bool)
        and expected_type is ListWithSelectedItem.Bool
        or issubclass(expected_type, value.__class__)
    ):
        return expected_type(value, items)

    raise ListWithSelectedItemPromotionException(
        f"Failed to promote type {type(value)} to a {qualname(expected_type)}."
    ) from None
