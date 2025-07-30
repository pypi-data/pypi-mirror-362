"""RotorInternalLayerSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ROTOR_INTERNAL_LAYER_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "RotorInternalLayerSpecification"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines import _1416, _1448, _1449

    Self = TypeVar("Self", bound="RotorInternalLayerSpecification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RotorInternalLayerSpecification._Cast_RotorInternalLayerSpecification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RotorInternalLayerSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RotorInternalLayerSpecification:
    """Special nested class for casting RotorInternalLayerSpecification to subclasses."""

    __parent__: "RotorInternalLayerSpecification"

    @property
    def u_shaped_layer_specification(
        self: "CastSelf",
    ) -> "_1448.UShapedLayerSpecification":
        from mastapy._private.electric_machines import _1448

        return self.__parent__._cast(_1448.UShapedLayerSpecification)

    @property
    def v_shaped_magnet_layer_specification(
        self: "CastSelf",
    ) -> "_1449.VShapedMagnetLayerSpecification":
        from mastapy._private.electric_machines import _1449

        return self.__parent__._cast(_1449.VShapedMagnetLayerSpecification)

    @property
    def rotor_internal_layer_specification(
        self: "CastSelf",
    ) -> "RotorInternalLayerSpecification":
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
class RotorInternalLayerSpecification(_0.APIBase):
    """RotorInternalLayerSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROTOR_INTERNAL_LAYER_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bridge_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BridgeThickness")

        if temp is None:
            return 0.0

        return temp

    @bridge_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def bridge_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BridgeThickness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def central_bridge_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CentralBridgeThickness")

        if temp is None:
            return 0.0

        return temp

    @central_bridge_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def central_bridge_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CentralBridgeThickness",
            float(value) if value is not None else 0.0,
        )

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
    def magnets(self: "Self") -> "_1416.MagnetForLayer":
        """mastapy.electric_machines.MagnetForLayer

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Magnets")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_RotorInternalLayerSpecification":
        """Cast to another type.

        Returns:
            _Cast_RotorInternalLayerSpecification
        """
        return _Cast_RotorInternalLayerSpecification(self)
