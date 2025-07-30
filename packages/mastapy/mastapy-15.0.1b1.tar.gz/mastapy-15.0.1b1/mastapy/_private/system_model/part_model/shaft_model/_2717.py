"""WindageLossCalculationParametersForCurvedSurfaceOfSection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_WINDAGE_LOSS_CALCULATION_PARAMETERS_FOR_CURVED_SURFACE_OF_SECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ShaftModel",
    "WindageLossCalculationParametersForCurvedSurfaceOfSection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.gears import _2762, _2767
    from mastapy._private.system_model.part_model.shaft_model import _2716

    Self = TypeVar(
        "Self", bound="WindageLossCalculationParametersForCurvedSurfaceOfSection"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="WindageLossCalculationParametersForCurvedSurfaceOfSection._Cast_WindageLossCalculationParametersForCurvedSurfaceOfSection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WindageLossCalculationParametersForCurvedSurfaceOfSection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WindageLossCalculationParametersForCurvedSurfaceOfSection:
    """Special nested class for casting WindageLossCalculationParametersForCurvedSurfaceOfSection to subclasses."""

    __parent__: "WindageLossCalculationParametersForCurvedSurfaceOfSection"

    @property
    def windage_loss_calculation_parameters_for_curved_surface_of_section(
        self: "CastSelf",
    ) -> "WindageLossCalculationParametersForCurvedSurfaceOfSection":
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
class WindageLossCalculationParametersForCurvedSurfaceOfSection(_0.APIBase):
    """WindageLossCalculationParametersForCurvedSurfaceOfSection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _WINDAGE_LOSS_CALCULATION_PARAMETERS_FOR_CURVED_SURFACE_OF_SECTION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angular_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def is_surface_underside_of_a_webbed_gear(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsSurfaceUndersideOfAWebbedGear")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def is_toothed_surface_of_cylindrical_gear(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsToothedSurfaceOfCylindricalGear")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def is_toothed_surface_of_gear(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsToothedSurfaceOfGear")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def mean_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def roughness_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughnessFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def section_length_along_axis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SectionLengthAlongAxis")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def section_length_along_surface(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SectionLengthAlongSurface")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cylindrical_gear(self: "Self") -> "_2762.CylindricalGear":
        """mastapy.system_model.part_model.gears.CylindricalGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear(self: "Self") -> "_2767.Gear":
        """mastapy.system_model.part_model.gears.Gear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def oil_parameters(self: "Self") -> "_2716.WindageLossCalculationOilParameters":
        """mastapy.system_model.part_model.shaft_model.WindageLossCalculationOilParameters

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilParameters")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_WindageLossCalculationParametersForCurvedSurfaceOfSection":
        """Cast to another type.

        Returns:
            _Cast_WindageLossCalculationParametersForCurvedSurfaceOfSection
        """
        return _Cast_WindageLossCalculationParametersForCurvedSurfaceOfSection(self)
