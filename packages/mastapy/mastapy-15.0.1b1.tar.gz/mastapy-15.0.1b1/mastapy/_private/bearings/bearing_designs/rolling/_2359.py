"""CylindricalRollerBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
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
from mastapy._private.bearings.bearing_designs.rolling import _2371

_CYLINDRICAL_ROLLER_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "CylindricalRollerBearing"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_designs import _2340, _2341, _2344
    from mastapy._private.bearings.bearing_designs.rolling import _2370, _2372, _2375
    from mastapy._private.bearings.bearing_results import _2148

    Self = TypeVar("Self", bound="CylindricalRollerBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalRollerBearing._Cast_CylindricalRollerBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalRollerBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalRollerBearing:
    """Special nested class for casting CylindricalRollerBearing to subclasses."""

    __parent__: "CylindricalRollerBearing"

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2371.NonBarrelRollerBearing":
        return self.__parent__._cast(_2371.NonBarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2372.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2372

        return self.__parent__._cast(_2372.RollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2375.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2375

        return self.__parent__._cast(_2375.RollingBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2341.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2341

        return self.__parent__._cast(_2341.DetailedBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2344.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2344

        return self.__parent__._cast(_2344.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2340.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2340

        return self.__parent__._cast(_2340.BearingDesign)

    @property
    def needle_roller_bearing(self: "CastSelf") -> "_2370.NeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2370

        return self.__parent__._cast(_2370.NeedleRollerBearing)

    @property
    def cylindrical_roller_bearing(self: "CastSelf") -> "CylindricalRollerBearing":
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
class CylindricalRollerBearing(_2371.NonBarrelRollerBearing):
    """CylindricalRollerBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_ROLLER_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allowable_axial_load_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AllowableAxialLoadFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @allowable_axial_load_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def allowable_axial_load_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AllowableAxialLoadFactor", value)

    @property
    @exception_bridge
    def capacity_lubrication_factor_for_permissible_axial_load_grease(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "CapacityLubricationFactorForPermissibleAxialLoadGrease"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @capacity_lubrication_factor_for_permissible_axial_load_grease.setter
    @exception_bridge
    @enforce_parameter_types
    def capacity_lubrication_factor_for_permissible_axial_load_grease(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped,
            "CapacityLubricationFactorForPermissibleAxialLoadGrease",
            value,
        )

    @property
    @exception_bridge
    def capacity_lubrication_factor_for_permissible_axial_load_oil(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "CapacityLubricationFactorForPermissibleAxialLoadOil"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @capacity_lubrication_factor_for_permissible_axial_load_oil.setter
    @exception_bridge
    @enforce_parameter_types
    def capacity_lubrication_factor_for_permissible_axial_load_oil(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "CapacityLubricationFactorForPermissibleAxialLoadOil", value
        )

    @property
    @exception_bridge
    def diameter_exponent_factor_for_permissible_axial_load(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DiameterExponentFactorForPermissibleAxialLoad"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diameter_exponent_factor_for_permissible_axial_load.setter
    @exception_bridge
    @enforce_parameter_types
    def diameter_exponent_factor_for_permissible_axial_load(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DiameterExponentFactorForPermissibleAxialLoad", value
        )

    @property
    @exception_bridge
    def diameter_scaling_factor_for_permissible_axial_load(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DiameterScalingFactorForPermissibleAxialLoad"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diameter_scaling_factor_for_permissible_axial_load.setter
    @exception_bridge
    @enforce_parameter_types
    def diameter_scaling_factor_for_permissible_axial_load(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DiameterScalingFactorForPermissibleAxialLoad", value
        )

    @property
    @exception_bridge
    def permissible_axial_load_default_calculation_method(
        self: "Self",
    ) -> "_2148.CylindricalRollerMaxAxialLoadMethod":
        """mastapy.bearings.bearing_results.CylindricalRollerMaxAxialLoadMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAxialLoadDefaultCalculationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Bearings.BearingResults.CylindricalRollerMaxAxialLoadMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_results._2148",
            "CylindricalRollerMaxAxialLoadMethod",
        )(value)

    @permissible_axial_load_default_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def permissible_axial_load_default_calculation_method(
        self: "Self", value: "_2148.CylindricalRollerMaxAxialLoadMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Bearings.BearingResults.CylindricalRollerMaxAxialLoadMethod",
        )
        pythonnet_property_set(
            self.wrapped, "PermissibleAxialLoadDefaultCalculationMethod", value
        )

    @property
    @exception_bridge
    def permissible_axial_load_dimension_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAxialLoadDimensionFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @permissible_axial_load_dimension_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def permissible_axial_load_dimension_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "PermissibleAxialLoadDimensionFactor", value
        )

    @property
    @exception_bridge
    def permissible_axial_load_internal_dimension_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAxialLoadInternalDimensionFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @permissible_axial_load_internal_dimension_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def permissible_axial_load_internal_dimension_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "PermissibleAxialLoadInternalDimensionFactor", value
        )

    @property
    @exception_bridge
    def radial_load_lubrication_factor_for_permissible_axial_load_grease(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "RadialLoadLubricationFactorForPermissibleAxialLoadGrease"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @radial_load_lubrication_factor_for_permissible_axial_load_grease.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_load_lubrication_factor_for_permissible_axial_load_grease(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped,
            "RadialLoadLubricationFactorForPermissibleAxialLoadGrease",
            value,
        )

    @property
    @exception_bridge
    def radial_load_lubrication_factor_for_permissible_axial_load_oil(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "RadialLoadLubricationFactorForPermissibleAxialLoadOil"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @radial_load_lubrication_factor_for_permissible_axial_load_oil.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_load_lubrication_factor_for_permissible_axial_load_oil(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "RadialLoadLubricationFactorForPermissibleAxialLoadOil", value
        )

    @property
    @exception_bridge
    def reference_rotation_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReferenceRotationSpeed")

        if temp is None:
            return 0.0

        return temp

    @reference_rotation_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def reference_rotation_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReferenceRotationSpeed",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalRollerBearing":
        """Cast to another type.

        Returns:
            _Cast_CylindricalRollerBearing
        """
        return _Cast_CylindricalRollerBearing(self)
