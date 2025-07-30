"""LTCALoadCaseModifiableSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1779

_LTCA_LOAD_CASE_MODIFIABLE_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "LTCALoadCaseModifiableSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LTCALoadCaseModifiableSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LTCALoadCaseModifiableSettings._Cast_LTCALoadCaseModifiableSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LTCALoadCaseModifiableSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LTCALoadCaseModifiableSettings:
    """Special nested class for casting LTCALoadCaseModifiableSettings to subclasses."""

    __parent__: "LTCALoadCaseModifiableSettings"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def ltca_load_case_modifiable_settings(
        self: "CastSelf",
    ) -> "LTCALoadCaseModifiableSettings":
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
class LTCALoadCaseModifiableSettings(
    _1779.IndependentReportablePropertiesBase["LTCALoadCaseModifiableSettings"]
):
    """LTCALoadCaseModifiableSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LTCA_LOAD_CASE_MODIFIABLE_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def apply_application_and_dynamic_factor(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ApplyApplicationAndDynamicFactor")

        if temp is None:
            return False

        return temp

    @apply_application_and_dynamic_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def apply_application_and_dynamic_factor(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ApplyApplicationAndDynamicFactor",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_change_in_contact_point_due_to_micro_geometry(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeChangeInContactPointDueToMicroGeometry"
        )

        if temp is None:
            return False

        return temp

    @include_change_in_contact_point_due_to_micro_geometry.setter
    @exception_bridge
    @enforce_parameter_types
    def include_change_in_contact_point_due_to_micro_geometry(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeChangeInContactPointDueToMicroGeometry",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_jacobian_advanced_ltca_solver(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseJacobianAdvancedLTCASolver")

        if temp is None:
            return False

        return temp

    @use_jacobian_advanced_ltca_solver.setter
    @exception_bridge
    @enforce_parameter_types
    def use_jacobian_advanced_ltca_solver(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseJacobianAdvancedLTCASolver",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_LTCALoadCaseModifiableSettings":
        """Cast to another type.

        Returns:
            _Cast_LTCALoadCaseModifiableSettings
        """
        return _Cast_LTCALoadCaseModifiableSettings(self)
