"""ShaftComplexShape"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D

_SHAFT_COMPLEX_SHAPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.RotorDynamics", "ShaftComplexShape"
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.system_model.analyses_and_results.rotor_dynamics import (
        _4289,
        _4290,
        _4291,
        _4292,
    )
    from mastapy._private.utility.units_and_measurements import _1797

    Self = TypeVar("Self", bound="ShaftComplexShape")
    CastSelf = TypeVar("CastSelf", bound="ShaftComplexShape._Cast_ShaftComplexShape")

TLinearMeasurement = TypeVar("TLinearMeasurement", bound="_1797.MeasurementBase")
TAngularMeasurement = TypeVar("TAngularMeasurement", bound="_1797.MeasurementBase")

__docformat__ = "restructuredtext en"
__all__ = ("ShaftComplexShape",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftComplexShape:
    """Special nested class for casting ShaftComplexShape to subclasses."""

    __parent__: "ShaftComplexShape"

    @property
    def shaft_forced_complex_shape(self: "CastSelf") -> "_4289.ShaftForcedComplexShape":
        from mastapy._private.system_model.analyses_and_results.rotor_dynamics import (
            _4289,
        )

        return self.__parent__._cast(_4289.ShaftForcedComplexShape)

    @property
    def shaft_modal_complex_shape(self: "CastSelf") -> "_4290.ShaftModalComplexShape":
        from mastapy._private.system_model.analyses_and_results.rotor_dynamics import (
            _4290,
        )

        return self.__parent__._cast(_4290.ShaftModalComplexShape)

    @property
    def shaft_modal_complex_shape_at_speeds(
        self: "CastSelf",
    ) -> "_4291.ShaftModalComplexShapeAtSpeeds":
        from mastapy._private.system_model.analyses_and_results.rotor_dynamics import (
            _4291,
        )

        return self.__parent__._cast(_4291.ShaftModalComplexShapeAtSpeeds)

    @property
    def shaft_modal_complex_shape_at_stiffness(
        self: "CastSelf",
    ) -> "_4292.ShaftModalComplexShapeAtStiffness":
        from mastapy._private.system_model.analyses_and_results.rotor_dynamics import (
            _4292,
        )

        return self.__parent__._cast(_4292.ShaftModalComplexShapeAtStiffness)

    @property
    def shaft_complex_shape(self: "CastSelf") -> "ShaftComplexShape":
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
class ShaftComplexShape(_0.APIBase, Generic[TLinearMeasurement, TAngularMeasurement]):
    """ShaftComplexShape

    This is a mastapy class.

    Generic Types:
        TLinearMeasurement
        TAngularMeasurement
    """

    TYPE: ClassVar["Type"] = _SHAFT_COMPLEX_SHAPE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angular_imaginary(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularImaginary")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def angular_magnitude(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularMagnitude")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def angular_phase(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularPhase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def angular_real(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularReal")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def linear_imaginary(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearImaginary")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def linear_magnitude(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearMagnitude")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def linear_phase(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearPhase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def linear_real(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearReal")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftComplexShape":
        """Cast to another type.

        Returns:
            _Cast_ShaftComplexShape
        """
        return _Cast_ShaftComplexShape(self)
