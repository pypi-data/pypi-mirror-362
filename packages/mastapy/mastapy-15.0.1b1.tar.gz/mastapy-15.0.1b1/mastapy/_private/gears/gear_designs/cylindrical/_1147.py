"""CylindricalMeshAngularBacklash"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical import _1150

_CYLINDRICAL_MESH_ANGULAR_BACKLASH = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalMeshAngularBacklash"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs.cylindrical import _1179, _1196

    Self = TypeVar("Self", bound="CylindricalMeshAngularBacklash")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalMeshAngularBacklash._Cast_CylindricalMeshAngularBacklash",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalMeshAngularBacklash",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalMeshAngularBacklash:
    """Special nested class for casting CylindricalMeshAngularBacklash to subclasses."""

    __parent__: "CylindricalMeshAngularBacklash"

    @property
    def cylindrical_mesh_linear_backlash_specification(
        self: "CastSelf",
    ) -> "_1150.CylindricalMeshLinearBacklashSpecification":
        return self.__parent__._cast(_1150.CylindricalMeshLinearBacklashSpecification)

    @property
    def toleranced_value_specification(
        self: "CastSelf",
    ) -> "_1196.TolerancedValueSpecification":
        pass

        from mastapy._private.gears.gear_designs.cylindrical import _1196

        return self.__parent__._cast(_1196.TolerancedValueSpecification)

    @property
    def relative_measurement_view_model(
        self: "CastSelf",
    ) -> "_1179.RelativeMeasurementViewModel":
        pass

        from mastapy._private.gears.gear_designs.cylindrical import _1179

        return self.__parent__._cast(_1179.RelativeMeasurementViewModel)

    @property
    def cylindrical_mesh_angular_backlash(
        self: "CastSelf",
    ) -> "CylindricalMeshAngularBacklash":
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
class CylindricalMeshAngularBacklash(_1150.CylindricalMeshLinearBacklashSpecification):
    """CylindricalMeshAngularBacklash

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_MESH_ANGULAR_BACKLASH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def average_mean(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AverageMean")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @average_mean.setter
    @exception_bridge
    @enforce_parameter_types
    def average_mean(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AverageMean", value)

    @property
    @exception_bridge
    def maximum(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Maximum")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Maximum", value)

    @property
    @exception_bridge
    def minimum(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Minimum")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Minimum", value)

    @property
    @exception_bridge
    def spread(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Spread")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @spread.setter
    @exception_bridge
    @enforce_parameter_types
    def spread(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Spread", value)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalMeshAngularBacklash":
        """Cast to another type.

        Returns:
            _Cast_CylindricalMeshAngularBacklash
        """
        return _Cast_CylindricalMeshAngularBacklash(self)
