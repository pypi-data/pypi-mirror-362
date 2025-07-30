"""ConstantLine"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_CONSTANT_LINE = python_net_import("SMT.MastaAPI.UtilityGUI.Charts", "ConstantLine")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility_gui.charts import _2061, _2067

    Self = TypeVar("Self", bound="ConstantLine")
    CastSelf = TypeVar("CastSelf", bound="ConstantLine._Cast_ConstantLine")


__docformat__ = "restructuredtext en"
__all__ = ("ConstantLine",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConstantLine:
    """Special nested class for casting ConstantLine to subclasses."""

    __parent__: "ConstantLine"

    @property
    def mode_constant_line(self: "CastSelf") -> "_2061.ModeConstantLine":
        from mastapy._private.utility_gui.charts import _2061

        return self.__parent__._cast(_2061.ModeConstantLine)

    @property
    def constant_line(self: "CastSelf") -> "ConstantLine":
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
class ConstantLine(_0.APIBase):
    """ConstantLine

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONSTANT_LINE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axis(self: "Self") -> "_2067.SMTAxis":
        """mastapy.utility_gui.charts.SMTAxis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Axis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.UtilityGUI.Charts.SMTAxis")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility_gui.charts._2067", "SMTAxis"
        )(value)

    @property
    @exception_bridge
    def end(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "End")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def label(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Label")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def start(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Start")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Value")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ConstantLine":
        """Cast to another type.

        Returns:
            _Cast_ConstantLine
        """
        return _Cast_ConstantLine(self)
