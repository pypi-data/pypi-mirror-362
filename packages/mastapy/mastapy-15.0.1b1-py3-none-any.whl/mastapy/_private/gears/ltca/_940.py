"""GearFilletNodeStressResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_GEAR_FILLET_NODE_STRESS_RESULTS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearFilletNodeStressResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.ltca import _928, _931

    Self = TypeVar("Self", bound="GearFilletNodeStressResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearFilletNodeStressResults._Cast_GearFilletNodeStressResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearFilletNodeStressResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearFilletNodeStressResults:
    """Special nested class for casting GearFilletNodeStressResults to subclasses."""

    __parent__: "GearFilletNodeStressResults"

    @property
    def conical_gear_fillet_stress_results(
        self: "CastSelf",
    ) -> "_928.ConicalGearFilletStressResults":
        from mastapy._private.gears.ltca import _928

        return self.__parent__._cast(_928.ConicalGearFilletStressResults)

    @property
    def cylindrical_gear_fillet_node_stress_results(
        self: "CastSelf",
    ) -> "_931.CylindricalGearFilletNodeStressResults":
        from mastapy._private.gears.ltca import _931

        return self.__parent__._cast(_931.CylindricalGearFilletNodeStressResults)

    @property
    def gear_fillet_node_stress_results(
        self: "CastSelf",
    ) -> "GearFilletNodeStressResults":
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
class GearFilletNodeStressResults(_0.APIBase):
    """GearFilletNodeStressResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_FILLET_NODE_STRESS_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fillet_column_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FilletColumnIndex")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def fillet_row_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FilletRowIndex")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def first_principal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FirstPrincipalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_tensile_principal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumTensilePrincipalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def second_principal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SecondPrincipalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_intensity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressIntensity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def third_principal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThirdPrincipalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def von_mises_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VonMisesStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def x_component(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XComponent")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def xy_shear_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XYShearStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def xz_shear_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XZShearStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def y_component(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YComponent")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def yz_shear_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YZShearStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def z_component(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZComponent")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_GearFilletNodeStressResults":
        """Cast to another type.

        Returns:
            _Cast_GearFilletNodeStressResults
        """
        return _Cast_GearFilletNodeStressResults(self)
