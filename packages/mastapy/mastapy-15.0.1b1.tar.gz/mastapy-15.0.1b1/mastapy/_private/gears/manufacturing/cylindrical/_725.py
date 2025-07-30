"""CylindricalMeshManufacturingConfig"""

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
from mastapy._private.gears.analysis import _1345

_CYLINDRICAL_MESH_MANUFACTURING_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical", "CylindricalMeshManufacturingConfig"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1336, _1342
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
        _834,
        _837,
        _838,
    )

    Self = TypeVar("Self", bound="CylindricalMeshManufacturingConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalMeshManufacturingConfig._Cast_CylindricalMeshManufacturingConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalMeshManufacturingConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalMeshManufacturingConfig:
    """Special nested class for casting CylindricalMeshManufacturingConfig to subclasses."""

    __parent__: "CylindricalMeshManufacturingConfig"

    @property
    def gear_mesh_implementation_detail(
        self: "CastSelf",
    ) -> "_1345.GearMeshImplementationDetail":
        return self.__parent__._cast(_1345.GearMeshImplementationDetail)

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1342.GearMeshDesignAnalysis":
        from mastapy._private.gears.analysis import _1342

        return self.__parent__._cast(_1342.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def cylindrical_mesh_manufacturing_config(
        self: "CastSelf",
    ) -> "CylindricalMeshManufacturingConfig":
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
class CylindricalMeshManufacturingConfig(_1345.GearMeshImplementationDetail):
    """CylindricalMeshManufacturingConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_MESH_MANUFACTURING_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gear_a_as_manufactured(self: "Self") -> "List[_834.CutterSimulationCalc]":
        """List[mastapy.gears.manufacturing.cylindrical.cutter_simulation.CutterSimulationCalc]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearAAsManufactured")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_b_as_manufactured(self: "Self") -> "List[_834.CutterSimulationCalc]":
        """List[mastapy.gears.manufacturing.cylindrical.cutter_simulation.CutterSimulationCalc]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBAsManufactured")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshed_gear_a_as_manufactured(
        self: "Self",
    ) -> "List[_837.CylindricalManufacturedRealGearInMesh]":
        """List[mastapy.gears.manufacturing.cylindrical.cutter_simulation.CylindricalManufacturedRealGearInMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshedGearAAsManufactured")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshed_gear_a_as_manufactured_virtual(
        self: "Self",
    ) -> "List[_838.CylindricalManufacturedVirtualGearInMesh]":
        """List[mastapy.gears.manufacturing.cylindrical.cutter_simulation.CylindricalManufacturedVirtualGearInMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshedGearAAsManufacturedVirtual")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshed_gear_b_as_manufactured(
        self: "Self",
    ) -> "List[_837.CylindricalManufacturedRealGearInMesh]":
        """List[mastapy.gears.manufacturing.cylindrical.cutter_simulation.CylindricalManufacturedRealGearInMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshedGearBAsManufactured")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshed_gear_b_as_manufactured_virtual(
        self: "Self",
    ) -> "List[_838.CylindricalManufacturedVirtualGearInMesh]":
        """List[mastapy.gears.manufacturing.cylindrical.cutter_simulation.CylindricalManufacturedVirtualGearInMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshedGearBAsManufacturedVirtual")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalMeshManufacturingConfig":
        """Cast to another type.

        Returns:
            _Cast_CylindricalMeshManufacturingConfig
        """
        return _Cast_CylindricalMeshManufacturingConfig(self)
