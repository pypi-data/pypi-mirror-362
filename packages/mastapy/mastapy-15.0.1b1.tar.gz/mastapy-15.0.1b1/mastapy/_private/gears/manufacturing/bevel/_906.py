"""PinionConcave"""

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

_PINION_CONCAVE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "PinionConcave"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.bevel import _909
    from mastapy._private.gears.manufacturing.bevel.basic_machine_settings import _926

    Self = TypeVar("Self", bound="PinionConcave")
    CastSelf = TypeVar("CastSelf", bound="PinionConcave._Cast_PinionConcave")


__docformat__ = "restructuredtext en"
__all__ = ("PinionConcave",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PinionConcave:
    """Special nested class for casting PinionConcave to subclasses."""

    __parent__: "PinionConcave"

    @property
    def pinion_concave(self: "CastSelf") -> "PinionConcave":
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
class PinionConcave(_0.APIBase):
    """PinionConcave

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PINION_CONCAVE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def pinion_concave_ob_configuration(
        self: "Self",
    ) -> "_926.BasicConicalGearMachineSettingsGenerated":
        """mastapy.gears.manufacturing.bevel.basic_machine_settings.BasicConicalGearMachineSettingsGenerated

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionConcaveOBConfiguration")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pinion_cutter_parameters_concave(
        self: "Self",
    ) -> "_909.PinionFinishMachineSettings":
        """mastapy.gears.manufacturing.bevel.PinionFinishMachineSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionCutterParametersConcave")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PinionConcave":
        """Cast to another type.

        Returns:
            _Cast_PinionConcave
        """
        return _Cast_PinionConcave(self)
