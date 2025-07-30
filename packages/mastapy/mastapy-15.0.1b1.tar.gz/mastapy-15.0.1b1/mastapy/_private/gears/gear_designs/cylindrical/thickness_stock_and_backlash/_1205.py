"""NoValueSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical import _1196

_NO_VALUE_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ThicknessStockAndBacklash",
    "NoValueSpecification",
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.gear_designs.cylindrical import _1179

    Self = TypeVar("Self", bound="NoValueSpecification")
    CastSelf = TypeVar(
        "CastSelf", bound="NoValueSpecification._Cast_NoValueSpecification"
    )

T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("NoValueSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NoValueSpecification:
    """Special nested class for casting NoValueSpecification to subclasses."""

    __parent__: "NoValueSpecification"

    @property
    def toleranced_value_specification(
        self: "CastSelf",
    ) -> "_1196.TolerancedValueSpecification":
        return self.__parent__._cast(_1196.TolerancedValueSpecification)

    @property
    def relative_measurement_view_model(
        self: "CastSelf",
    ) -> "_1179.RelativeMeasurementViewModel":
        from mastapy._private.gears.gear_designs.cylindrical import _1179

        return self.__parent__._cast(_1179.RelativeMeasurementViewModel)

    @property
    def no_value_specification(self: "CastSelf") -> "NoValueSpecification":
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
class NoValueSpecification(_1196.TolerancedValueSpecification[T]):
    """NoValueSpecification

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _NO_VALUE_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NoValueSpecification":
        """Cast to another type.

        Returns:
            _Cast_NoValueSpecification
        """
        return _Cast_NoValueSpecification(self)
