"""AdditionalAccelerationOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.utility import _1779

_ADDITIONAL_ACCELERATION_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AdditionalAccelerationOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AdditionalAccelerationOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AdditionalAccelerationOptions._Cast_AdditionalAccelerationOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AdditionalAccelerationOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AdditionalAccelerationOptions:
    """Special nested class for casting AdditionalAccelerationOptions to subclasses."""

    __parent__: "AdditionalAccelerationOptions"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def additional_acceleration_options(
        self: "CastSelf",
    ) -> "AdditionalAccelerationOptions":
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
class AdditionalAccelerationOptions(
    _1779.IndependentReportablePropertiesBase["AdditionalAccelerationOptions"]
):
    """AdditionalAccelerationOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ADDITIONAL_ACCELERATION_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def include_additional_acceleration(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeAdditionalAcceleration")

        if temp is None:
            return False

        return temp

    @include_additional_acceleration.setter
    @exception_bridge
    @enforce_parameter_types
    def include_additional_acceleration(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeAdditionalAcceleration",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def magnitude(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Magnitude")

        if temp is None:
            return 0.0

        return temp

    @magnitude.setter
    @exception_bridge
    @enforce_parameter_types
    def magnitude(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Magnitude", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def specify_direction_and_magnitude(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyDirectionAndMagnitude")

        if temp is None:
            return False

        return temp

    @specify_direction_and_magnitude.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_direction_and_magnitude(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyDirectionAndMagnitude",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def acceleration_vector(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "AccelerationVector")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @acceleration_vector.setter
    @exception_bridge
    @enforce_parameter_types
    def acceleration_vector(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "AccelerationVector", value)

    @property
    @exception_bridge
    def orientation(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "Orientation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @orientation.setter
    @exception_bridge
    @enforce_parameter_types
    def orientation(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "Orientation", value)

    @property
    def cast_to(self: "Self") -> "_Cast_AdditionalAccelerationOptions":
        """Cast to another type.

        Returns:
            _Cast_AdditionalAccelerationOptions
        """
        return _Cast_AdditionalAccelerationOptions(self)
