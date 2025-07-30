"""ToothFlankFractureAnalysisContactPointN1457"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_2d import Vector2D

_TOOTH_FLANK_FRACTURE_ANALYSIS_CONTACT_POINT_N1457 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336",
    "ToothFlankFractureAnalysisContactPointN1457",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1135
    from mastapy._private.gears.rating.cylindrical.iso6336 import _621

    Self = TypeVar("Self", bound="ToothFlankFractureAnalysisContactPointN1457")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ToothFlankFractureAnalysisContactPointN1457._Cast_ToothFlankFractureAnalysisContactPointN1457",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothFlankFractureAnalysisContactPointN1457",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ToothFlankFractureAnalysisContactPointN1457:
    """Special nested class for casting ToothFlankFractureAnalysisContactPointN1457 to subclasses."""

    __parent__: "ToothFlankFractureAnalysisContactPointN1457"

    @property
    def tooth_flank_fracture_analysis_row_n1457(
        self: "CastSelf",
    ) -> "_621.ToothFlankFractureAnalysisRowN1457":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _621

        return self.__parent__._cast(_621.ToothFlankFractureAnalysisRowN1457)

    @property
    def tooth_flank_fracture_analysis_contact_point_n1457(
        self: "CastSelf",
    ) -> "ToothFlankFractureAnalysisContactPointN1457":
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
class ToothFlankFractureAnalysisContactPointN1457(_0.APIBase):
    """ToothFlankFractureAnalysisContactPointN1457

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TOOTH_FLANK_FRACTURE_ANALYSIS_CONTACT_POINT_N1457

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
    def mean_coefficient_of_friction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanCoefficientOfFriction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def coordinates(self: "Self") -> "Vector2D":
        """Vector2D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Coordinates")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def position_on_profile(self: "Self") -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PositionOnProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ToothFlankFractureAnalysisContactPointN1457":
        """Cast to another type.

        Returns:
            _Cast_ToothFlankFractureAnalysisContactPointN1457
        """
        return _Cast_ToothFlankFractureAnalysisContactPointN1457(self)
