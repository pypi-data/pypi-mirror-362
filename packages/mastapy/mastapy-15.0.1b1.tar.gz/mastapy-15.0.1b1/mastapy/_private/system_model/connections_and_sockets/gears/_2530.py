"""CylindricalGearMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.connections_and_sockets.gears import _2534

_CYLINDRICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "CylindricalGearMesh"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1128
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets import _2493, _2502
    from mastapy._private.system_model.part_model.gears import _2762, _2763

    Self = TypeVar("Self", bound="CylindricalGearMesh")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearMesh._Cast_CylindricalGearMesh"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMesh:
    """Special nested class for casting CylindricalGearMesh to subclasses."""

    __parent__: "CylindricalGearMesh"

    @property
    def gear_mesh(self: "CastSelf") -> "_2534.GearMesh":
        return self.__parent__._cast(_2534.GearMesh)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2502.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2502

        return self.__parent__._cast(_2502.InterMountableComponentConnection)

    @property
    def connection(self: "CastSelf") -> "_2493.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2493

        return self.__parent__._cast(_2493.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def cylindrical_gear_mesh(self: "CastSelf") -> "CylindricalGearMesh":
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
class CylindricalGearMesh(_2534.GearMesh):
    """CylindricalGearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def centre_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CentreDistance")

        if temp is None:
            return 0.0

        return temp

    @centre_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def centre_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CentreDistance", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def centre_distance_range(self: "Self") -> "Tuple[float, float]":
        """Tuple[float, float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CentreDistanceRange")

        if temp is None:
            return None

        value = conversion.pn_to_mp_range(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def centre_distance_with_normal_module_adjustment_by_scaling_entire_model(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "CentreDistanceWithNormalModuleAdjustmentByScalingEntireModel"
        )

        if temp is None:
            return 0.0

        return temp

    @centre_distance_with_normal_module_adjustment_by_scaling_entire_model.setter
    @exception_bridge
    @enforce_parameter_types
    def centre_distance_with_normal_module_adjustment_by_scaling_entire_model(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CentreDistanceWithNormalModuleAdjustmentByScalingEntireModel",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def is_centre_distance_ready_to_change(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsCentreDistanceReadyToChange")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def active_gear_mesh_design(self: "Self") -> "_1128.CylindricalGearMeshDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_mesh_design(self: "Self") -> "_1128.CylindricalGearMeshDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_set(self: "Self") -> "_2763.CylindricalGearSet":
        """mastapy.system_model.part_model.gears.CylindricalGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gears(self: "Self") -> "List[_2762.CylindricalGear]":
        """List[mastapy.system_model.part_model.gears.CylindricalGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMesh":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMesh
        """
        return _Cast_CylindricalGearMesh(self)
