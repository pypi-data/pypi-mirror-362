"""CylindricalSetManufacturingConfig"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1351

_CYLINDRICAL_SET_MANUFACTURING_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical", "CylindricalSetManufacturingConfig"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1337, _1346
    from mastapy._private.gears.manufacturing.cylindrical import _715, _725

    Self = TypeVar("Self", bound="CylindricalSetManufacturingConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalSetManufacturingConfig._Cast_CylindricalSetManufacturingConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalSetManufacturingConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalSetManufacturingConfig:
    """Special nested class for casting CylindricalSetManufacturingConfig to subclasses."""

    __parent__: "CylindricalSetManufacturingConfig"

    @property
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "_1351.GearSetImplementationDetail":
        return self.__parent__._cast(_1351.GearSetImplementationDetail)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1346.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1346

        return self.__parent__._cast(_1346.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1337.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1337

        return self.__parent__._cast(_1337.AbstractGearSetAnalysis)

    @property
    def cylindrical_set_manufacturing_config(
        self: "CastSelf",
    ) -> "CylindricalSetManufacturingConfig":
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
class CylindricalSetManufacturingConfig(_1351.GearSetImplementationDetail):
    """CylindricalSetManufacturingConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_SET_MANUFACTURING_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cylindrical_gear_manufacturing_configurations(
        self: "Self",
    ) -> "List[_715.CylindricalGearManufacturingConfig]":
        """List[mastapy.gears.manufacturing.cylindrical.CylindricalGearManufacturingConfig]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearManufacturingConfigurations"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cylindrical_mesh_manufacturing_configurations(
        self: "Self",
    ) -> "List[_725.CylindricalMeshManufacturingConfig]":
        """List[mastapy.gears.manufacturing.cylindrical.CylindricalMeshManufacturingConfig]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalMeshManufacturingConfigurations"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def duplicate(self: "Self") -> "CylindricalSetManufacturingConfig":
        """mastapy.gears.manufacturing.cylindrical.CylindricalSetManufacturingConfig"""
        method_result = pythonnet_method_call(self.wrapped, "Duplicate")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalSetManufacturingConfig":
        """Cast to another type.

        Returns:
            _Cast_CylindricalSetManufacturingConfig
        """
        return _Cast_CylindricalSetManufacturingConfig(self)
