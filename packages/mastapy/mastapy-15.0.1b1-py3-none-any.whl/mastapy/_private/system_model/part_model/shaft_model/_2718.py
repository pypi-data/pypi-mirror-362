"""WindageLossCalculationParametersForEndOfSection"""

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

_WINDAGE_LOSS_CALCULATION_PARAMETERS_FOR_END_OF_SECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ShaftModel",
    "WindageLossCalculationParametersForEndOfSection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.shaft_model import _2716

    Self = TypeVar("Self", bound="WindageLossCalculationParametersForEndOfSection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WindageLossCalculationParametersForEndOfSection._Cast_WindageLossCalculationParametersForEndOfSection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WindageLossCalculationParametersForEndOfSection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WindageLossCalculationParametersForEndOfSection:
    """Special nested class for casting WindageLossCalculationParametersForEndOfSection to subclasses."""

    __parent__: "WindageLossCalculationParametersForEndOfSection"

    @property
    def windage_loss_calculation_parameters_for_end_of_section(
        self: "CastSelf",
    ) -> "WindageLossCalculationParametersForEndOfSection":
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
class WindageLossCalculationParametersForEndOfSection(_0.APIBase):
    """WindageLossCalculationParametersForEndOfSection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WINDAGE_LOSS_CALCULATION_PARAMETERS_FOR_END_OF_SECTION

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
    def inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

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
    ) -> "_Cast_WindageLossCalculationParametersForEndOfSection":
        """Cast to another type.

        Returns:
            _Cast_WindageLossCalculationParametersForEndOfSection
        """
        return _Cast_WindageLossCalculationParametersForEndOfSection(self)
