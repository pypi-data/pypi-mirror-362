"""ToothFlankFractureAnalysisRowN1457"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.cylindrical.iso6336 import _618

_TOOTH_FLANK_FRACTURE_ANALYSIS_ROW_N1457 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336",
    "ToothFlankFractureAnalysisRowN1457",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.cylindrical.iso6336 import _620

    Self = TypeVar("Self", bound="ToothFlankFractureAnalysisRowN1457")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ToothFlankFractureAnalysisRowN1457._Cast_ToothFlankFractureAnalysisRowN1457",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothFlankFractureAnalysisRowN1457",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ToothFlankFractureAnalysisRowN1457:
    """Special nested class for casting ToothFlankFractureAnalysisRowN1457 to subclasses."""

    __parent__: "ToothFlankFractureAnalysisRowN1457"

    @property
    def tooth_flank_fracture_analysis_contact_point_n1457(
        self: "CastSelf",
    ) -> "_618.ToothFlankFractureAnalysisContactPointN1457":
        return self.__parent__._cast(_618.ToothFlankFractureAnalysisContactPointN1457)

    @property
    def tooth_flank_fracture_analysis_row_n1457(
        self: "CastSelf",
    ) -> "ToothFlankFractureAnalysisRowN1457":
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
class ToothFlankFractureAnalysisRowN1457(
    _618.ToothFlankFractureAnalysisContactPointN1457
):
    """ToothFlankFractureAnalysisRowN1457

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TOOTH_FLANK_FRACTURE_ANALYSIS_ROW_N1457

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_fatigue_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumFatigueDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def analysis_point_with_maximum_fatigue_damage(
        self: "Self",
    ) -> "_620.ToothFlankFractureAnalysisPointN1457":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisPointN1457

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AnalysisPointWithMaximumFatigueDamage"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def watch_points(self: "Self") -> "List[_620.ToothFlankFractureAnalysisPointN1457]":
        """List[mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisPointN1457]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WatchPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ToothFlankFractureAnalysisRowN1457":
        """Cast to another type.

        Returns:
            _Cast_ToothFlankFractureAnalysisRowN1457
        """
        return _Cast_ToothFlankFractureAnalysisRowN1457(self)
