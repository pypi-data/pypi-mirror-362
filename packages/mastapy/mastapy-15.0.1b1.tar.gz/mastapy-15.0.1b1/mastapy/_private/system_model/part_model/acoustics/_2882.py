"""ResultPlaneOptions"""

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
from mastapy._private.system_model.part_model.acoustics import _2885

_RESULT_PLANE_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Acoustics", "ResultPlaneOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1676

    Self = TypeVar("Self", bound="ResultPlaneOptions")
    CastSelf = TypeVar("CastSelf", bound="ResultPlaneOptions._Cast_ResultPlaneOptions")


__docformat__ = "restructuredtext en"
__all__ = ("ResultPlaneOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResultPlaneOptions:
    """Special nested class for casting ResultPlaneOptions to subclasses."""

    __parent__: "ResultPlaneOptions"

    @property
    def result_surface_options(self: "CastSelf") -> "_2885.ResultSurfaceOptions":
        return self.__parent__._cast(_2885.ResultSurfaceOptions)

    @property
    def result_plane_options(self: "CastSelf") -> "ResultPlaneOptions":
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
class ResultPlaneOptions(_2885.ResultSurfaceOptions):
    """ResultPlaneOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RESULT_PLANE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axis_for_plane_normal(self: "Self") -> "_1676.Axis":
        """mastapy.math_utility.Axis"""
        temp = pythonnet_property_get(self.wrapped, "AxisForPlaneNormal")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.MathUtility.Axis")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1676", "Axis"
        )(value)

    @axis_for_plane_normal.setter
    @exception_bridge
    @enforce_parameter_types
    def axis_for_plane_normal(self: "Self", value: "_1676.Axis") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.MathUtility.Axis")
        pythonnet_property_set(self.wrapped, "AxisForPlaneNormal", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ResultPlaneOptions":
        """Cast to another type.

        Returns:
            _Cast_ResultPlaneOptions
        """
        return _Cast_ResultPlaneOptions(self)
