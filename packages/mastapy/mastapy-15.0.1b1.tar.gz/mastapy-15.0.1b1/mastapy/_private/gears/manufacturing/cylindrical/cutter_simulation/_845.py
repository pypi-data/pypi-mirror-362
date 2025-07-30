"""ManufacturingProcessControls"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_MANUFACTURING_PROCESS_CONTROLS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "ManufacturingProcessControls",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ManufacturingProcessControls")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ManufacturingProcessControls._Cast_ManufacturingProcessControls",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ManufacturingProcessControls",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ManufacturingProcessControls:
    """Special nested class for casting ManufacturingProcessControls to subclasses."""

    __parent__: "ManufacturingProcessControls"

    @property
    def manufacturing_process_controls(
        self: "CastSelf",
    ) -> "ManufacturingProcessControls":
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
class ManufacturingProcessControls(_0.APIBase):
    """ManufacturingProcessControls

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MANUFACTURING_PROCESS_CONTROLS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def tooth_thickness_specification_compliance_checked(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ToothThicknessSpecificationComplianceChecked"
        )

        if temp is None:
            return False

        return temp

    @tooth_thickness_specification_compliance_checked.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_thickness_specification_compliance_checked(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToothThicknessSpecificationComplianceChecked",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ManufacturingProcessControls":
        """Cast to another type.

        Returns:
            _Cast_ManufacturingProcessControls
        """
        return _Cast_ManufacturingProcessControls(self)
