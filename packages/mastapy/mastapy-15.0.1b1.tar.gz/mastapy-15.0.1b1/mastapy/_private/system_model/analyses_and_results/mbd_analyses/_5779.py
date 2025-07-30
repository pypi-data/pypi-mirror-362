"""SplineDampingOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.math_utility.hertzian_contact import _1757

_SPLINE_DAMPING_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses", "SplineDampingOptions"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="SplineDampingOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="SplineDampingOptions._Cast_SplineDampingOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SplineDampingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SplineDampingOptions:
    """Special nested class for casting SplineDampingOptions to subclasses."""

    __parent__: "SplineDampingOptions"

    @property
    def spline_damping_options(self: "CastSelf") -> "SplineDampingOptions":
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
class SplineDampingOptions(_0.APIBase):
    """SplineDampingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPLINE_DAMPING_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_damping_model(
        self: "Self",
    ) -> "overridable.Overridable_ContactDampingModel":
        """Overridable[mastapy.math_utility.hertzian_contact.ContactDampingModel]"""
        temp = pythonnet_property_get(self.wrapped, "ContactDampingModel")

        if temp is None:
            return None

        value = overridable.Overridable_ContactDampingModel.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @contact_damping_model.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_damping_model(
        self: "Self",
        value: "Union[_1757.ContactDampingModel, Tuple[_1757.ContactDampingModel, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_ContactDampingModel.wrapper_type()
        enclosed_type = overridable.Overridable_ContactDampingModel.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ContactDampingModel", value)

    @property
    @exception_bridge
    def damping_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DampingFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @damping_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def damping_factor(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DampingFactor", value)

    @property
    @exception_bridge
    def penetration_for_max_damping(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PenetrationForMaxDamping")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @penetration_for_max_damping.setter
    @exception_bridge
    @enforce_parameter_types
    def penetration_for_max_damping(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PenetrationForMaxDamping", value)

    @property
    @exception_bridge
    def rayleigh_damping_beta(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RayleighDampingBeta")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @rayleigh_damping_beta.setter
    @exception_bridge
    @enforce_parameter_types
    def rayleigh_damping_beta(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RayleighDampingBeta", value)

    @property
    def cast_to(self: "Self") -> "_Cast_SplineDampingOptions":
        """Cast to another type.

        Returns:
            _Cast_SplineDampingOptions
        """
        return _Cast_SplineDampingOptions(self)
