"""SystemDeflectionOptions"""

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
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7878
from mastapy._private.system_model.analyses_and_results.static_loads import _7674

_SYSTEM_DEFLECTION_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "SystemDeflectionOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SystemDeflectionOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="SystemDeflectionOptions._Cast_SystemDeflectionOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SystemDeflectionOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SystemDeflectionOptions:
    """Special nested class for casting SystemDeflectionOptions to subclasses."""

    __parent__: "SystemDeflectionOptions"

    @property
    def abstract_analysis_options(self: "CastSelf") -> "_7878.AbstractAnalysisOptions":
        return self.__parent__._cast(_7878.AbstractAnalysisOptions)

    @property
    def system_deflection_options(self: "CastSelf") -> "SystemDeflectionOptions":
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
class SystemDeflectionOptions(_7878.AbstractAnalysisOptions[_7674.StaticLoadCase]):
    """SystemDeflectionOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYSTEM_DEFLECTION_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def ground_shaft_if_rigid_body_rotation_is_large(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "GroundShaftIfRigidBodyRotationIsLarge"
        )

        if temp is None:
            return False

        return temp

    @ground_shaft_if_rigid_body_rotation_is_large.setter
    @exception_bridge
    @enforce_parameter_types
    def ground_shaft_if_rigid_body_rotation_is_large(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "GroundShaftIfRigidBodyRotationIsLarge",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def maximum_number_of_unstable_rigid_body_rotation_iterations(
        self: "Self",
    ) -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumNumberOfUnstableRigidBodyRotationIterations"
        )

        if temp is None:
            return 0

        return temp

    @maximum_number_of_unstable_rigid_body_rotation_iterations.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_unstable_rigid_body_rotation_iterations(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumNumberOfUnstableRigidBodyRotationIterations",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def maximum_rigid_body_rotation_change_in_system_deflection(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumRigidBodyRotationChangeInSystemDeflection"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_rigid_body_rotation_change_in_system_deflection.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_rigid_body_rotation_change_in_system_deflection(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumRigidBodyRotationChangeInSystemDeflection",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SystemDeflectionOptions":
        """Cast to another type.

        Returns:
            _Cast_SystemDeflectionOptions
        """
        return _Cast_SystemDeflectionOptions(self)
