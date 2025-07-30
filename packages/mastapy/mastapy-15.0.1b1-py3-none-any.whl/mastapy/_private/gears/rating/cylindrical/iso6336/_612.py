"""ISO6336MeanStressInfluenceFactor"""

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

_ISO6336_MEAN_STRESS_INFLUENCE_FACTOR = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336", "ISO6336MeanStressInfluenceFactor"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _412

    Self = TypeVar("Self", bound="ISO6336MeanStressInfluenceFactor")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO6336MeanStressInfluenceFactor._Cast_ISO6336MeanStressInfluenceFactor",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO6336MeanStressInfluenceFactor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO6336MeanStressInfluenceFactor:
    """Special nested class for casting ISO6336MeanStressInfluenceFactor to subclasses."""

    __parent__: "ISO6336MeanStressInfluenceFactor"

    @property
    def iso6336_mean_stress_influence_factor(
        self: "CastSelf",
    ) -> "ISO6336MeanStressInfluenceFactor":
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
class ISO6336MeanStressInfluenceFactor(_0.APIBase):
    """ISO6336MeanStressInfluenceFactor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO6336_MEAN_STRESS_INFLUENCE_FACTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def higher_loaded_flank(self: "Self") -> "_412.CylindricalFlanks":
        """mastapy.gears.CylindricalFlanks

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HigherLoadedFlank")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.CylindricalFlanks")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._412", "CylindricalFlanks"
        )(value)

    @property
    @exception_bridge
    def load_per_unit_face_width_of_the_higher_loaded_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LoadPerUnitFaceWidthOfTheHigherLoadedFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_per_unit_face_width_of_the_lower_loaded_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LoadPerUnitFaceWidthOfTheLowerLoadedFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_stress_ratio_for_reference_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanStressRatioForReferenceStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_stress_ratio_for_static_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanStressRatioForStaticStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_influence_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressInfluenceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_influence_factor_for_reference_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressInfluenceFactorForReferenceStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO6336MeanStressInfluenceFactor":
        """Cast to another type.

        Returns:
            _Cast_ISO6336MeanStressInfluenceFactor
        """
        return _Cast_ISO6336MeanStressInfluenceFactor(self)
