"""ShavingDynamicsConfiguration"""

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
from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _854,
    _858,
)

_SHAVING_DYNAMICS_CONFIGURATION = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics",
    "ShavingDynamicsConfiguration",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
        _869,
    )

    Self = TypeVar("Self", bound="ShavingDynamicsConfiguration")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShavingDynamicsConfiguration._Cast_ShavingDynamicsConfiguration",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShavingDynamicsConfiguration",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShavingDynamicsConfiguration:
    """Special nested class for casting ShavingDynamicsConfiguration to subclasses."""

    __parent__: "ShavingDynamicsConfiguration"

    @property
    def shaving_dynamics_configuration(
        self: "CastSelf",
    ) -> "ShavingDynamicsConfiguration":
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
class ShavingDynamicsConfiguration(_0.APIBase):
    """ShavingDynamicsConfiguration

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAVING_DYNAMICS_CONFIGURATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def conventional_shaving_dynamics(
        self: "Self",
    ) -> "_869.ShavingDynamicsCalculation[_854.ConventionalShavingDynamics]":
        """mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.ShavingDynamicsCalculation[mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.ConventionalShavingDynamics]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConventionalShavingDynamics")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _854.ConventionalShavingDynamics
        ](temp)

    @property
    @exception_bridge
    def plunge_shaving_dynamics(
        self: "Self",
    ) -> "_869.ShavingDynamicsCalculation[_858.PlungeShaverDynamics]":
        """mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.ShavingDynamicsCalculation[mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.PlungeShaverDynamics]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlungeShavingDynamics")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_858.PlungeShaverDynamics](
            temp
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ShavingDynamicsConfiguration":
        """Cast to another type.

        Returns:
            _Cast_ShavingDynamicsConfiguration
        """
        return _Cast_ShavingDynamicsConfiguration(self)
