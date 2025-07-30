"""LinearBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_designs import _2340

_LINEAR_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns", "LinearBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2080, _2085

    Self = TypeVar("Self", bound="LinearBearing")
    CastSelf = TypeVar("CastSelf", bound="LinearBearing._Cast_LinearBearing")


__docformat__ = "restructuredtext en"
__all__ = ("LinearBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LinearBearing:
    """Special nested class for casting LinearBearing to subclasses."""

    __parent__: "LinearBearing"

    @property
    def bearing_design(self: "CastSelf") -> "_2340.BearingDesign":
        return self.__parent__._cast(_2340.BearingDesign)

    @property
    def linear_bearing(self: "CastSelf") -> "LinearBearing":
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
class LinearBearing(_2340.BearingDesign):
    """LinearBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LINEAR_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialStiffness")

        if temp is None:
            return 0.0

        return temp

    @axial_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AxialStiffness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def bore(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Bore")

        if temp is None:
            return 0.0

        return temp

    @bore.setter
    @exception_bridge
    @enforce_parameter_types
    def bore(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Bore", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def model(self: "Self") -> "_2080.BearingModel":
        """mastapy.bearings.BearingModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Model")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bearings.BearingModel")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2080", "BearingModel"
        )(value)

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def radial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialStiffness")

        if temp is None:
            return 0.0

        return temp

    @radial_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialStiffness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def stiffness_options(self: "Self") -> "_2085.BearingStiffnessMatrixOption":
        """mastapy.bearings.BearingStiffnessMatrixOption"""
        temp = pythonnet_property_get(self.wrapped, "StiffnessOptions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingStiffnessMatrixOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2085", "BearingStiffnessMatrixOption"
        )(value)

    @stiffness_options.setter
    @exception_bridge
    @enforce_parameter_types
    def stiffness_options(
        self: "Self", value: "_2085.BearingStiffnessMatrixOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingStiffnessMatrixOption"
        )
        pythonnet_property_set(self.wrapped, "StiffnessOptions", value)

    @property
    @exception_bridge
    def tilt_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TiltStiffness")

        if temp is None:
            return 0.0

        return temp

    @tilt_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TiltStiffness", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_LinearBearing":
        """Cast to another type.

        Returns:
            _Cast_LinearBearing
        """
        return _Cast_LinearBearing(self)
