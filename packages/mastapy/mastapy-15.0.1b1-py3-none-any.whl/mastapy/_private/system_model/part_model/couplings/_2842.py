"""SplineHalfManufacturingError"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
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
from mastapy._private.system_model.part_model.couplings import _2832

_SPLINE_HALF_MANUFACTURING_ERROR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SplineHalfManufacturingError"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="SplineHalfManufacturingError")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SplineHalfManufacturingError._Cast_SplineHalfManufacturingError",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SplineHalfManufacturingError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SplineHalfManufacturingError:
    """Special nested class for casting SplineHalfManufacturingError to subclasses."""

    __parent__: "SplineHalfManufacturingError"

    @property
    def rigid_connector_settings(self: "CastSelf") -> "_2832.RigidConnectorSettings":
        return self.__parent__._cast(_2832.RigidConnectorSettings)

    @property
    def spline_half_manufacturing_error(
        self: "CastSelf",
    ) -> "SplineHalfManufacturingError":
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
class SplineHalfManufacturingError(_2832.RigidConnectorSettings):
    """SplineHalfManufacturingError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPLINE_HALF_MANUFACTURING_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def misalignment_error_x(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MisalignmentErrorX")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @misalignment_error_x.setter
    @exception_bridge
    @enforce_parameter_types
    def misalignment_error_x(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MisalignmentErrorX", value)

    @property
    @exception_bridge
    def misalignment_error_y(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MisalignmentErrorY")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @misalignment_error_y.setter
    @exception_bridge
    @enforce_parameter_types
    def misalignment_error_y(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MisalignmentErrorY", value)

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def run_out_error_x(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RunOutErrorX")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @run_out_error_x.setter
    @exception_bridge
    @enforce_parameter_types
    def run_out_error_x(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RunOutErrorX", value)

    @property
    @exception_bridge
    def run_out_error_y(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RunOutErrorY")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @run_out_error_y.setter
    @exception_bridge
    @enforce_parameter_types
    def run_out_error_y(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RunOutErrorY", value)

    @property
    def cast_to(self: "Self") -> "_Cast_SplineHalfManufacturingError":
        """Cast to another type.

        Returns:
            _Cast_SplineHalfManufacturingError
        """
        return _Cast_SplineHalfManufacturingError(self)
