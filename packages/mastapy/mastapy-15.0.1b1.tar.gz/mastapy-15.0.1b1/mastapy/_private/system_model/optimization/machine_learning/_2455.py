"""CylindricalGearFlankOptimisationParameters"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.utility.databases import _2028

_CYLINDRICAL_GEAR_FLANK_OPTIMISATION_PARAMETERS = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization.MachineLearning",
    "CylindricalGearFlankOptimisationParameters",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.optimization.machine_learning import _2454

    Self = TypeVar("Self", bound="CylindricalGearFlankOptimisationParameters")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearFlankOptimisationParameters._Cast_CylindricalGearFlankOptimisationParameters",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearFlankOptimisationParameters",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearFlankOptimisationParameters:
    """Special nested class for casting CylindricalGearFlankOptimisationParameters to subclasses."""

    __parent__: "CylindricalGearFlankOptimisationParameters"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def cylindrical_gear_flank_optimisation_parameters(
        self: "CastSelf",
    ) -> "CylindricalGearFlankOptimisationParameters":
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
class CylindricalGearFlankOptimisationParameters(_2028.NamedDatabaseItem):
    """CylindricalGearFlankOptimisationParameters

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_FLANK_OPTIMISATION_PARAMETERS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_parameters(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfParameters")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def optimization_properties(
        self: "Self",
    ) -> "List[_2454.CylindricalGearFlankOptimisationParameter]":
        """List[mastapy.system_model.optimization.machine_learning.CylindricalGearFlankOptimisationParameter]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OptimizationProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearFlankOptimisationParameters":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearFlankOptimisationParameters
        """
        return _Cast_CylindricalGearFlankOptimisationParameters(self)
