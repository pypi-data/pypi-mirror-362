"""ReplacedShaftSelectionHelper"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_REPLACED_SHAFT_SELECTION_HELPER = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "ReplacedShaftSelectionHelper"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.shaft_model import _2714

    Self = TypeVar("Self", bound="ReplacedShaftSelectionHelper")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ReplacedShaftSelectionHelper._Cast_ReplacedShaftSelectionHelper",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ReplacedShaftSelectionHelper",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ReplacedShaftSelectionHelper:
    """Special nested class for casting ReplacedShaftSelectionHelper to subclasses."""

    __parent__: "ReplacedShaftSelectionHelper"

    @property
    def replaced_shaft_selection_helper(
        self: "CastSelf",
    ) -> "ReplacedShaftSelectionHelper":
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
class ReplacedShaftSelectionHelper(_0.APIBase):
    """ReplacedShaftSelectionHelper

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _REPLACED_SHAFT_SELECTION_HELPER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def is_replaced_by_fe(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsReplacedByFE")

        if temp is None:
            return False

        return temp

    @is_replaced_by_fe.setter
    @exception_bridge
    @enforce_parameter_types
    def is_replaced_by_fe(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsReplacedByFE", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def shaft(self: "Self") -> "_2714.Shaft":
        """mastapy.system_model.part_model.shaft_model.Shaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shaft")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ReplacedShaftSelectionHelper":
        """Cast to another type.

        Returns:
            _Cast_ReplacedShaftSelectionHelper
        """
        return _Cast_ReplacedShaftSelectionHelper(self)
