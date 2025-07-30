"""PinionConvex"""

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
)

_PINION_CONVEX = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "PinionConvex"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.bevel import _909
    from mastapy._private.gears.manufacturing.bevel.basic_machine_settings import _926

    Self = TypeVar("Self", bound="PinionConvex")
    CastSelf = TypeVar("CastSelf", bound="PinionConvex._Cast_PinionConvex")


__docformat__ = "restructuredtext en"
__all__ = ("PinionConvex",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PinionConvex:
    """Special nested class for casting PinionConvex to subclasses."""

    __parent__: "PinionConvex"

    @property
    def pinion_convex(self: "CastSelf") -> "PinionConvex":
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
class PinionConvex(_0.APIBase):
    """PinionConvex

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PINION_CONVEX

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def pinion_convex_ib_configuration(
        self: "Self",
    ) -> "_926.BasicConicalGearMachineSettingsGenerated":
        """mastapy.gears.manufacturing.bevel.basic_machine_settings.BasicConicalGearMachineSettingsGenerated

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionConvexIBConfiguration")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pinion_cutter_parameters_convex(
        self: "Self",
    ) -> "_909.PinionFinishMachineSettings":
        """mastapy.gears.manufacturing.bevel.PinionFinishMachineSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionCutterParametersConvex")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PinionConvex":
        """Cast to another type.

        Returns:
            _Cast_PinionConvex
        """
        return _Cast_PinionConvex(self)
