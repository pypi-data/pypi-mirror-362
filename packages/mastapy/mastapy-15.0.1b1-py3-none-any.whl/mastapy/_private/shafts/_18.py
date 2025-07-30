"""ShaftAxialTorsionalComponentValues"""

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
)

_SHAFT_AXIAL_TORSIONAL_COMPONENT_VALUES = python_net_import(
    "SMT.MastaAPI.Shafts", "ShaftAxialTorsionalComponentValues"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.shafts import _16, _17

    Self = TypeVar("Self", bound="ShaftAxialTorsionalComponentValues")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftAxialTorsionalComponentValues._Cast_ShaftAxialTorsionalComponentValues",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftAxialTorsionalComponentValues",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftAxialTorsionalComponentValues:
    """Special nested class for casting ShaftAxialTorsionalComponentValues to subclasses."""

    __parent__: "ShaftAxialTorsionalComponentValues"

    @property
    def shaft_axial_bending_torsional_component_values(
        self: "CastSelf",
    ) -> "_16.ShaftAxialBendingTorsionalComponentValues":
        from mastapy._private.shafts import _16

        return self.__parent__._cast(_16.ShaftAxialBendingTorsionalComponentValues)

    @property
    def shaft_axial_bending_x_bending_y_torsional_component_values(
        self: "CastSelf",
    ) -> "_17.ShaftAxialBendingXBendingYTorsionalComponentValues":
        from mastapy._private.shafts import _17

        return self.__parent__._cast(
            _17.ShaftAxialBendingXBendingYTorsionalComponentValues
        )

    @property
    def shaft_axial_torsional_component_values(
        self: "CastSelf",
    ) -> "ShaftAxialTorsionalComponentValues":
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
class ShaftAxialTorsionalComponentValues(_0.APIBase):
    """ShaftAxialTorsionalComponentValues

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_AXIAL_TORSIONAL_COMPONENT_VALUES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Axial")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torsional(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Torsional")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftAxialTorsionalComponentValues":
        """Cast to another type.

        Returns:
            _Cast_ShaftAxialTorsionalComponentValues
        """
        return _Cast_ShaftAxialTorsionalComponentValues(self)
