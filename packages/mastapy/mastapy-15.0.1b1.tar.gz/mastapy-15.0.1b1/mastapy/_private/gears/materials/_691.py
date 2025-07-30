"""InstantaneousCoefficientOfFrictionCalculator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.materials import _681

_INSTANTANEOUS_COEFFICIENT_OF_FRICTION_CALCULATOR = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "InstantaneousCoefficientOfFrictionCalculator"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.materials import _675, _687, _697, _703, _704, _710
    from mastapy._private.gears.rating.cylindrical import _549

    Self = TypeVar("Self", bound="InstantaneousCoefficientOfFrictionCalculator")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InstantaneousCoefficientOfFrictionCalculator._Cast_InstantaneousCoefficientOfFrictionCalculator",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InstantaneousCoefficientOfFrictionCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InstantaneousCoefficientOfFrictionCalculator:
    """Special nested class for casting InstantaneousCoefficientOfFrictionCalculator to subclasses."""

    __parent__: "InstantaneousCoefficientOfFrictionCalculator"

    @property
    def coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_681.CoefficientOfFrictionCalculator":
        return self.__parent__._cast(_681.CoefficientOfFrictionCalculator)

    @property
    def benedict_and_kelley_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_675.BenedictAndKelleyCoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _675

        return self.__parent__._cast(
            _675.BenedictAndKelleyCoefficientOfFrictionCalculator
        )

    @property
    def drozdov_and_gavrikov_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_687.DrozdovAndGavrikovCoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _687

        return self.__parent__._cast(
            _687.DrozdovAndGavrikovCoefficientOfFrictionCalculator
        )

    @property
    def isotc60_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_697.ISOTC60CoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _697

        return self.__parent__._cast(_697.ISOTC60CoefficientOfFrictionCalculator)

    @property
    def misharin_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_703.MisharinCoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _703

        return self.__parent__._cast(_703.MisharinCoefficientOfFrictionCalculator)

    @property
    def o_donoghue_and_cameron_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_704.ODonoghueAndCameronCoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _704

        return self.__parent__._cast(
            _704.ODonoghueAndCameronCoefficientOfFrictionCalculator
        )

    @property
    def script_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_710.ScriptCoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _710

        return self.__parent__._cast(_710.ScriptCoefficientOfFrictionCalculator)

    @property
    def instantaneous_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "InstantaneousCoefficientOfFrictionCalculator":
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
class InstantaneousCoefficientOfFrictionCalculator(
    _681.CoefficientOfFrictionCalculator
):
    """InstantaneousCoefficientOfFrictionCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INSTANTANEOUS_COEFFICIENT_OF_FRICTION_CALCULATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cylindrical_gear_mesh_rating(self: "Self") -> "_549.CylindricalGearMeshRating":
        """mastapy.gears.rating.cylindrical.CylindricalGearMeshRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearMeshRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_InstantaneousCoefficientOfFrictionCalculator":
        """Cast to another type.

        Returns:
            _Cast_InstantaneousCoefficientOfFrictionCalculator
        """
        return _Cast_InstantaneousCoefficientOfFrictionCalculator(self)
