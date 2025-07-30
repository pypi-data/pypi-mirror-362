"""GearSetOptimiser"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_INT_32 = python_net_import("System", "Int32")
_BOOLEAN = python_net_import("System", "Boolean")
_TASK_PROGRESS = python_net_import("SMT.MastaAPIUtility", "TaskProgress")
_GEAR_SET_OPTIMISER = python_net_import("SMT.MastaAPI.Gears", "GearSetOptimiser")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private import _7901
    from mastapy._private.gears import _420
    from mastapy._private.gears.gear_designs.cylindrical import _1140

    Self = TypeVar("Self", bound="GearSetOptimiser")
    CastSelf = TypeVar("CastSelf", bound="GearSetOptimiser._Cast_GearSetOptimiser")


__docformat__ = "restructuredtext en"
__all__ = ("GearSetOptimiser",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetOptimiser:
    """Special nested class for casting GearSetOptimiser to subclasses."""

    __parent__: "GearSetOptimiser"

    @property
    def cylindrical_gear_set_macro_geometry_optimiser(
        self: "CastSelf",
    ) -> "_1140.CylindricalGearSetMacroGeometryOptimiser":
        from mastapy._private.gears.gear_designs.cylindrical import _1140

        return self.__parent__._cast(_1140.CylindricalGearSetMacroGeometryOptimiser)

    @property
    def gear_set_optimiser(self: "CastSelf") -> "GearSetOptimiser":
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
class GearSetOptimiser(_0.APIBase):
    """GearSetOptimiser

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_OPTIMISER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialRatioRatingForNVH")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bending_safety_factor_for_worst_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingSafetyFactorForWorstGear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_safety_factor_for_worst_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactSafetyFactorForWorstGear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def crack_initiation_safety_factor_for_worst_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CrackInitiationSafetyFactorForWorstGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_fracture_safety_factor_for_worst_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FatigueFractureSafetyFactorForWorstGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def micropitting_safety_factor_for_worst_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingSafetyFactorForWorstGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permanent_deformation_safety_factor_for_worst_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermanentDeformationSafetyFactorForWorstGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_safety_factor_flash_temperature_method_for_worst_gear(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingSafetyFactorFlashTemperatureMethodForWorstGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_safety_factor_integral_method_for_worst_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingSafetyFactorIntegralMethodForWorstGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def static_bending_safety_factor_for_worst_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StaticBendingSafetyFactorForWorstGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def static_contact_safety_factor_for_worst_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StaticContactSafetyFactorForWorstGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_and_axial_contact_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseAndAxialContactRatioRatingForNVH"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseRatioRatingForNVH")

        if temp is None:
            return 0.0

        return temp

    @exception_bridge
    def dispose(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Dispose")

    @exception_bridge
    @enforce_parameter_types
    def perform_strength_optimisation_with_progress(
        self: "Self",
        number_of_results: "int",
        progress: "_7901.TaskProgress",
        use_current_design_as_starting_point: "bool" = False,
    ) -> "_420.GearSetOptimisationResults":
        """mastapy.gears.GearSetOptimisationResults

        Args:
            number_of_results (int)
            progress (mastapy.TaskProgress)
            use_current_design_as_starting_point (bool, optional)
        """
        number_of_results = int(number_of_results)
        use_current_design_as_starting_point = bool(
            use_current_design_as_starting_point
        )
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "PerformStrengthOptimisation",
            [_INT_32, _TASK_PROGRESS, _BOOLEAN],
            number_of_results if number_of_results else 0,
            progress.wrapped if progress else None,
            use_current_design_as_starting_point
            if use_current_design_as_starting_point
            else False,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def perform_strength_optimisation(
        self: "Self",
        number_of_results: "int",
        use_current_design_as_starting_point: "bool" = False,
    ) -> "_420.GearSetOptimisationResults":
        """mastapy.gears.GearSetOptimisationResults

        Args:
            number_of_results (int)
            use_current_design_as_starting_point (bool, optional)
        """
        number_of_results = int(number_of_results)
        use_current_design_as_starting_point = bool(
            use_current_design_as_starting_point
        )
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "PerformStrengthOptimisation",
            [_INT_32, _BOOLEAN],
            number_of_results if number_of_results else 0,
            use_current_design_as_starting_point
            if use_current_design_as_starting_point
            else False,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def __enter__(self: "Self") -> None:
        return self

    def __exit__(
        self: "Self", exception_type: "Any", exception_value: "Any", traceback: "Any"
    ) -> None:
        self.dispose()

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetOptimiser":
        """Cast to another type.

        Returns:
            _Cast_GearSetOptimiser
        """
        return _Cast_GearSetOptimiser(self)
