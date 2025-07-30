"""BearingStiffnessMatrixReporter"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_BEARING_STIFFNESS_MATRIX_REPORTER = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "BearingStiffnessMatrixReporter"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2171

    Self = TypeVar("Self", bound="BearingStiffnessMatrixReporter")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BearingStiffnessMatrixReporter._Cast_BearingStiffnessMatrixReporter",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingStiffnessMatrixReporter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingStiffnessMatrixReporter:
    """Special nested class for casting BearingStiffnessMatrixReporter to subclasses."""

    __parent__: "BearingStiffnessMatrixReporter"

    @property
    def bearing_stiffness_matrix_reporter(
        self: "CastSelf",
    ) -> "BearingStiffnessMatrixReporter":
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
class BearingStiffnessMatrixReporter(_0.APIBase):
    """BearingStiffnessMatrixReporter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_STIFFNESS_MATRIX_REPORTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_radial_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumRadialStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_tilt_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumTiltStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_radial_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumRadialStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_tilt_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumTiltStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def radial_stiffness_variation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialStiffnessVariation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_xx(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessXX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_xy(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessXY")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_xz(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessXZ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_x_theta_x(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessXThetaX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_x_theta_y(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessXThetaY")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_x_theta_z(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessXThetaZ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_yx(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessYX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_yy(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessYY")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_yz(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessYZ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_y_theta_x(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessYThetaX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_y_theta_y(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessYThetaY")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_y_theta_z(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessYThetaZ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_zx(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessZX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_zy(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessZY")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_zz(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessZZ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_z_theta_x(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessZThetaX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_z_theta_y(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessZThetaY")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_z_theta_z(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessZThetaZ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_xx(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaXX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_xy(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaXY")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_xz(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaXZ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_x_theta_x(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaXThetaX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_x_theta_y(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaXThetaY")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_x_theta_z(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaXThetaZ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_yx(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaYX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_yy(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaYY")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_yz(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaYZ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_y_theta_x(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaYThetaX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_y_theta_y(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaYThetaY")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_y_theta_z(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaYThetaZ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_zx(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaZX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_zy(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaZY")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_zz(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaZZ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_z_theta_x(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaZThetaX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_z_theta_y(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaZThetaY")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_theta_z_theta_z(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessThetaZThetaZ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tilt_stiffness_variation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TiltStiffnessVariation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torsional_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorsionalStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rows(self: "Self") -> "List[_2171.StiffnessRow]":
        """List[mastapy.bearings.bearing_results.StiffnessRow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rows")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BearingStiffnessMatrixReporter":
        """Cast to another type.

        Returns:
            _Cast_BearingStiffnessMatrixReporter
        """
        return _Cast_BearingStiffnessMatrixReporter(self)
