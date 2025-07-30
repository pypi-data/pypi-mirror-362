"""LTCASettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
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

_LTCA_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "LTCASettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1169

    Self = TypeVar("Self", bound="LTCASettings")
    CastSelf = TypeVar("CastSelf", bound="LTCASettings._Cast_LTCASettings")


__docformat__ = "restructuredtext en"
__all__ = ("LTCASettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LTCASettings:
    """Special nested class for casting LTCASettings to subclasses."""

    __parent__: "LTCASettings"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def ltca_settings(self: "CastSelf") -> "LTCASettings":
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
class LTCASettings(_1779.IndependentReportablePropertiesBase["LTCASettings"]):
    """LTCASettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LTCA_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def face_utilization_load_cutoff_parameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "FaceUtilizationLoadCutoffParameter"
        )

        if temp is None:
            return 0.0

        return temp

    @face_utilization_load_cutoff_parameter.setter
    @exception_bridge
    @enforce_parameter_types
    def face_utilization_load_cutoff_parameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FaceUtilizationLoadCutoffParameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def include_extended_tip_contact(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeExtendedTipContact")

        if temp is None:
            return False

        return temp

    @include_extended_tip_contact.setter
    @exception_bridge
    @enforce_parameter_types
    def include_extended_tip_contact(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeExtendedTipContact",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def load_case_modifiable_settings(
        self: "Self",
    ) -> "_1169.LTCALoadCaseModifiableSettings":
        """mastapy.gears.gear_designs.cylindrical.LTCALoadCaseModifiableSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCaseModifiableSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LTCASettings":
        """Cast to another type.

        Returns:
            _Cast_LTCASettings
        """
        return _Cast_LTCASettings(self)
