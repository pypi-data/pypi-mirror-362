"""RelativeValuesSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

_RELATIVE_VALUES_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "RelativeValuesSpecification"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.gear_designs.cylindrical import _1103
    from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
        _1202,
    )

    Self = TypeVar("Self", bound="RelativeValuesSpecification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RelativeValuesSpecification._Cast_RelativeValuesSpecification",
    )

T = TypeVar("T", bound="RelativeValuesSpecification")

__docformat__ = "restructuredtext en"
__all__ = ("RelativeValuesSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RelativeValuesSpecification:
    """Special nested class for casting RelativeValuesSpecification to subclasses."""

    __parent__: "RelativeValuesSpecification"

    @property
    def backlash_specification(self: "CastSelf") -> "_1103.BacklashSpecification":
        from mastapy._private.gears.gear_designs.cylindrical import _1103

        return self.__parent__._cast(_1103.BacklashSpecification)

    @property
    def finish_stock_specification(
        self: "CastSelf",
    ) -> "_1202.FinishStockSpecification":
        from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
            _1202,
        )

        return self.__parent__._cast(_1202.FinishStockSpecification)

    @property
    def relative_values_specification(
        self: "CastSelf",
    ) -> "RelativeValuesSpecification":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class RelativeValuesSpecification(_0.APIBase, Generic[T]):
    """RelativeValuesSpecification

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _RELATIVE_VALUES_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RelativeValuesSpecification":
        """Cast to another type.

        Returns:
            _Cast_RelativeValuesSpecification
        """
        return _Cast_RelativeValuesSpecification(self)
