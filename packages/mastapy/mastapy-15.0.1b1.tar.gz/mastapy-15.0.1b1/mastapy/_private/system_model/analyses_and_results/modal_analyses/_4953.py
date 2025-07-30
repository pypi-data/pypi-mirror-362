"""ShaftModalAnalysisMode"""

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
from mastapy._private._math.vector_3d import Vector3D

_SHAFT_MODAL_ANALYSIS_MODE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "ShaftModalAnalysisMode",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="ShaftModalAnalysisMode")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftModalAnalysisMode._Cast_ShaftModalAnalysisMode"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftModalAnalysisMode",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftModalAnalysisMode:
    """Special nested class for casting ShaftModalAnalysisMode to subclasses."""

    __parent__: "ShaftModalAnalysisMode"

    @property
    def shaft_modal_analysis_mode(self: "CastSelf") -> "ShaftModalAnalysisMode":
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
class ShaftModalAnalysisMode(_0.APIBase):
    """ShaftModalAnalysisMode

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_MODAL_ANALYSIS_MODE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angular_displacement(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularDisplacement")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def linear_displacement(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearDisplacement")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftModalAnalysisMode":
        """Cast to another type.

        Returns:
            _Cast_ShaftModalAnalysisMode
        """
        return _Cast_ShaftModalAnalysisMode(self)
