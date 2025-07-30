"""ToothFlankFractureAnalysisContactPoint"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.cylindrical.iso6336 import _616

_TOOTH_FLANK_FRACTURE_ANALYSIS_CONTACT_POINT = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336",
    "ToothFlankFractureAnalysisContactPoint",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ToothFlankFractureAnalysisContactPoint")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ToothFlankFractureAnalysisContactPoint._Cast_ToothFlankFractureAnalysisContactPoint",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothFlankFractureAnalysisContactPoint",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ToothFlankFractureAnalysisContactPoint:
    """Special nested class for casting ToothFlankFractureAnalysisContactPoint to subclasses."""

    __parent__: "ToothFlankFractureAnalysisContactPoint"

    @property
    def tooth_flank_fracture_analysis_contact_point_common(
        self: "CastSelf",
    ) -> "_616.ToothFlankFractureAnalysisContactPointCommon":
        return self.__parent__._cast(_616.ToothFlankFractureAnalysisContactPointCommon)

    @property
    def tooth_flank_fracture_analysis_contact_point(
        self: "CastSelf",
    ) -> "ToothFlankFractureAnalysisContactPoint":
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
class ToothFlankFractureAnalysisContactPoint(
    _616.ToothFlankFractureAnalysisContactPointCommon
):
    """ToothFlankFractureAnalysisContactPoint

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TOOTH_FLANK_FRACTURE_ANALYSIS_CONTACT_POINT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def half_of_hertzian_contact_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HalfOfHertzianContactWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HertzianContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def local_normal_radius_of_relative_curvature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LocalNormalRadiusOfRelativeCurvature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ToothFlankFractureAnalysisContactPoint":
        """Cast to another type.

        Returns:
            _Cast_ToothFlankFractureAnalysisContactPoint
        """
        return _Cast_ToothFlankFractureAnalysisContactPoint(self)
