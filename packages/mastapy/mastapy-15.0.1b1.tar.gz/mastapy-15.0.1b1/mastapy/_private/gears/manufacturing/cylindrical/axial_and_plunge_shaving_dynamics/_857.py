"""ConventionalShavingDynamicsViewModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _854,
    _873,
)

_CONVENTIONAL_SHAVING_DYNAMICS_VIEW_MODEL = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics",
    "ConventionalShavingDynamicsViewModel",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical import _731
    from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
        _874,
    )

    Self = TypeVar("Self", bound="ConventionalShavingDynamicsViewModel")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConventionalShavingDynamicsViewModel._Cast_ConventionalShavingDynamicsViewModel",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConventionalShavingDynamicsViewModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConventionalShavingDynamicsViewModel:
    """Special nested class for casting ConventionalShavingDynamicsViewModel to subclasses."""

    __parent__: "ConventionalShavingDynamicsViewModel"

    @property
    def shaving_dynamics_view_model(
        self: "CastSelf",
    ) -> "_873.ShavingDynamicsViewModel":
        return self.__parent__._cast(_873.ShavingDynamicsViewModel)

    @property
    def shaving_dynamics_view_model_base(
        self: "CastSelf",
    ) -> "_874.ShavingDynamicsViewModelBase":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _874,
        )

        return self.__parent__._cast(_874.ShavingDynamicsViewModelBase)

    @property
    def gear_manufacturing_configuration_view_model(
        self: "CastSelf",
    ) -> "_731.GearManufacturingConfigurationViewModel":
        from mastapy._private.gears.manufacturing.cylindrical import _731

        return self.__parent__._cast(_731.GearManufacturingConfigurationViewModel)

    @property
    def conventional_shaving_dynamics_view_model(
        self: "CastSelf",
    ) -> "ConventionalShavingDynamicsViewModel":
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
class ConventionalShavingDynamicsViewModel(
    _873.ShavingDynamicsViewModel[_854.ConventionalShavingDynamics]
):
    """ConventionalShavingDynamicsViewModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONVENTIONAL_SHAVING_DYNAMICS_VIEW_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConventionalShavingDynamicsViewModel":
        """Cast to another type.

        Returns:
            _Cast_ConventionalShavingDynamicsViewModel
        """
        return _Cast_ConventionalShavingDynamicsViewModel(self)
