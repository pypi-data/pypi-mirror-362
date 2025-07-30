"""VirtualPlungeShaverOutputs"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving import _754

_VIRTUAL_PLUNGE_SHAVER_OUTPUTS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving",
    "VirtualPlungeShaverOutputs",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutters import _818

    Self = TypeVar("Self", bound="VirtualPlungeShaverOutputs")
    CastSelf = TypeVar(
        "CastSelf", bound="VirtualPlungeShaverOutputs._Cast_VirtualPlungeShaverOutputs"
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualPlungeShaverOutputs",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualPlungeShaverOutputs:
    """Special nested class for casting VirtualPlungeShaverOutputs to subclasses."""

    __parent__: "VirtualPlungeShaverOutputs"

    @property
    def plunge_shaver_outputs(self: "CastSelf") -> "_754.PlungeShaverOutputs":
        return self.__parent__._cast(_754.PlungeShaverOutputs)

    @property
    def virtual_plunge_shaver_outputs(self: "CastSelf") -> "VirtualPlungeShaverOutputs":
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
class VirtualPlungeShaverOutputs(_754.PlungeShaverOutputs):
    """VirtualPlungeShaverOutputs

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_PLUNGE_SHAVER_OUTPUTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def lead_modification_on_conjugate_shaver_chart_left_flank(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LeadModificationOnConjugateShaverChartLeftFlank"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def lead_modification_on_conjugate_shaver_chart_right_flank(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LeadModificationOnConjugateShaverChartRightFlank"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def shaver(self: "Self") -> "_818.CylindricalGearShaver":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearShaver

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shaver")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualPlungeShaverOutputs":
        """Cast to another type.

        Returns:
            _Cast_VirtualPlungeShaverOutputs
        """
        return _Cast_VirtualPlungeShaverOutputs(self)
