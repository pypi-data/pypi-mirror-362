"""RelativeMeasurementViewModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

_RELATIVE_MEASUREMENT_VIEW_MODEL = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "RelativeMeasurementViewModel"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.gear_designs.cylindrical import _1147, _1150, _1196
    from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
        _1204,
        _1205,
    )

    Self = TypeVar("Self", bound="RelativeMeasurementViewModel")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RelativeMeasurementViewModel._Cast_RelativeMeasurementViewModel",
    )

T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("RelativeMeasurementViewModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RelativeMeasurementViewModel:
    """Special nested class for casting RelativeMeasurementViewModel to subclasses."""

    __parent__: "RelativeMeasurementViewModel"

    @property
    def cylindrical_mesh_angular_backlash(
        self: "CastSelf",
    ) -> "_1147.CylindricalMeshAngularBacklash":
        from mastapy._private.gears.gear_designs.cylindrical import _1147

        return self.__parent__._cast(_1147.CylindricalMeshAngularBacklash)

    @property
    def cylindrical_mesh_linear_backlash_specification(
        self: "CastSelf",
    ) -> "_1150.CylindricalMeshLinearBacklashSpecification":
        from mastapy._private.gears.gear_designs.cylindrical import _1150

        return self.__parent__._cast(_1150.CylindricalMeshLinearBacklashSpecification)

    @property
    def toleranced_value_specification(
        self: "CastSelf",
    ) -> "_1196.TolerancedValueSpecification":
        from mastapy._private.gears.gear_designs.cylindrical import _1196

        return self.__parent__._cast(_1196.TolerancedValueSpecification)

    @property
    def nominal_value_specification(
        self: "CastSelf",
    ) -> "_1204.NominalValueSpecification":
        from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
            _1204,
        )

        return self.__parent__._cast(_1204.NominalValueSpecification)

    @property
    def no_value_specification(self: "CastSelf") -> "_1205.NoValueSpecification":
        from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
            _1205,
        )

        return self.__parent__._cast(_1205.NoValueSpecification)

    @property
    def relative_measurement_view_model(
        self: "CastSelf",
    ) -> "RelativeMeasurementViewModel":
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
class RelativeMeasurementViewModel(_0.APIBase, Generic[T]):
    """RelativeMeasurementViewModel

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _RELATIVE_MEASUREMENT_VIEW_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RelativeMeasurementViewModel":
        """Cast to another type.

        Returns:
            _Cast_RelativeMeasurementViewModel
        """
        return _Cast_RelativeMeasurementViewModel(self)
