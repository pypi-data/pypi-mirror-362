"""InformationForContactAtPointAlongFaceWidth"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_INFORMATION_FOR_CONTACT_AT_POINT_ALONG_FACE_WIDTH = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "InformationForContactAtPointAlongFaceWidth",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="InformationForContactAtPointAlongFaceWidth")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InformationForContactAtPointAlongFaceWidth._Cast_InformationForContactAtPointAlongFaceWidth",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InformationForContactAtPointAlongFaceWidth",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InformationForContactAtPointAlongFaceWidth:
    """Special nested class for casting InformationForContactAtPointAlongFaceWidth to subclasses."""

    __parent__: "InformationForContactAtPointAlongFaceWidth"

    @property
    def information_for_contact_at_point_along_face_width(
        self: "CastSelf",
    ) -> "InformationForContactAtPointAlongFaceWidth":
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
class InformationForContactAtPointAlongFaceWidth(_0.APIBase):
    """InformationForContactAtPointAlongFaceWidth

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INFORMATION_FOR_CONTACT_AT_POINT_ALONG_FACE_WIDTH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def force_per_unit_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForcePerUnitLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_per_unit_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessPerUnitLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_penetration(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfacePenetration")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_InformationForContactAtPointAlongFaceWidth":
        """Cast to another type.

        Returns:
            _Cast_InformationForContactAtPointAlongFaceWidth
        """
        return _Cast_InformationForContactAtPointAlongFaceWidth(self)
