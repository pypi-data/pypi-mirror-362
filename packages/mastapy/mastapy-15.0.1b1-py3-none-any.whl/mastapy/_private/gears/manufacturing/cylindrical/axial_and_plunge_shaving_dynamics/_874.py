"""ShavingDynamicsViewModelBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical import _731

_SHAVING_DYNAMICS_VIEW_MODEL_BASE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics",
    "ShavingDynamicsViewModelBase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
        _857,
        _863,
        _873,
    )

    Self = TypeVar("Self", bound="ShavingDynamicsViewModelBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShavingDynamicsViewModelBase._Cast_ShavingDynamicsViewModelBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShavingDynamicsViewModelBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShavingDynamicsViewModelBase:
    """Special nested class for casting ShavingDynamicsViewModelBase to subclasses."""

    __parent__: "ShavingDynamicsViewModelBase"

    @property
    def gear_manufacturing_configuration_view_model(
        self: "CastSelf",
    ) -> "_731.GearManufacturingConfigurationViewModel":
        return self.__parent__._cast(_731.GearManufacturingConfigurationViewModel)

    @property
    def conventional_shaving_dynamics_view_model(
        self: "CastSelf",
    ) -> "_857.ConventionalShavingDynamicsViewModel":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _857,
        )

        return self.__parent__._cast(_857.ConventionalShavingDynamicsViewModel)

    @property
    def plunge_shaving_dynamics_view_model(
        self: "CastSelf",
    ) -> "_863.PlungeShavingDynamicsViewModel":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _863,
        )

        return self.__parent__._cast(_863.PlungeShavingDynamicsViewModel)

    @property
    def shaving_dynamics_view_model(
        self: "CastSelf",
    ) -> "_873.ShavingDynamicsViewModel":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _873,
        )

        return self.__parent__._cast(_873.ShavingDynamicsViewModel)

    @property
    def shaving_dynamics_view_model_base(
        self: "CastSelf",
    ) -> "ShavingDynamicsViewModelBase":
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
class ShavingDynamicsViewModelBase(_731.GearManufacturingConfigurationViewModel):
    """ShavingDynamicsViewModelBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAVING_DYNAMICS_VIEW_MODEL_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ShavingDynamicsViewModelBase":
        """Cast to another type.

        Returns:
            _Cast_ShavingDynamicsViewModelBase
        """
        return _Cast_ShavingDynamicsViewModelBase(self)
