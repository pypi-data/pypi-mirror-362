"""GearMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.connections_and_sockets import _2502

_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "GearMesh"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs import _1053
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets import _2493
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2520,
        _2522,
        _2524,
        _2526,
        _2528,
        _2530,
        _2532,
        _2536,
        _2539,
        _2540,
        _2541,
        _2544,
        _2546,
        _2548,
        _2550,
        _2552,
    )

    Self = TypeVar("Self", bound="GearMesh")
    CastSelf = TypeVar("CastSelf", bound="GearMesh._Cast_GearMesh")


__docformat__ = "restructuredtext en"
__all__ = ("GearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMesh:
    """Special nested class for casting GearMesh to subclasses."""

    __parent__: "GearMesh"

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2502.InterMountableComponentConnection":
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
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2520.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2520

        return self.__parent__._cast(_2520.AGMAGleasonConicalGearMesh)

    @property
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2522.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2522

        return self.__parent__._cast(_2522.BevelDifferentialGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2524.BevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2524

        return self.__parent__._cast(_2524.BevelGearMesh)

    @property
    def concept_gear_mesh(self: "CastSelf") -> "_2526.ConceptGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2526

        return self.__parent__._cast(_2526.ConceptGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2528.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2528

        return self.__parent__._cast(_2528.ConicalGearMesh)

    @property
    def cylindrical_gear_mesh(self: "CastSelf") -> "_2530.CylindricalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2530

        return self.__parent__._cast(_2530.CylindricalGearMesh)

    @property
    def face_gear_mesh(self: "CastSelf") -> "_2532.FaceGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2532

        return self.__parent__._cast(_2532.FaceGearMesh)

    @property
    def hypoid_gear_mesh(self: "CastSelf") -> "_2536.HypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2536

        return self.__parent__._cast(_2536.HypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2539.KlingelnbergCycloPalloidConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2539

        return self.__parent__._cast(_2539.KlingelnbergCycloPalloidConicalGearMesh)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "CastSelf",
    ) -> "_2540.KlingelnbergCycloPalloidHypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2540

        return self.__parent__._cast(_2540.KlingelnbergCycloPalloidHypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "CastSelf",
    ) -> "_2541.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2541

        return self.__parent__._cast(_2541.KlingelnbergCycloPalloidSpiralBevelGearMesh)

    @property
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "_2544.SpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2544

        return self.__parent__._cast(_2544.SpiralBevelGearMesh)

    @property
    def straight_bevel_diff_gear_mesh(
        self: "CastSelf",
    ) -> "_2546.StraightBevelDiffGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2546

        return self.__parent__._cast(_2546.StraightBevelDiffGearMesh)

    @property
    def straight_bevel_gear_mesh(self: "CastSelf") -> "_2548.StraightBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2548

        return self.__parent__._cast(_2548.StraightBevelGearMesh)

    @property
    def worm_gear_mesh(self: "CastSelf") -> "_2550.WormGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2550

        return self.__parent__._cast(_2550.WormGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2552.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2552

        return self.__parent__._cast(_2552.ZerolBevelGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "GearMesh":
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
class GearMesh(_2502.InterMountableComponentConnection):
    """GearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def mesh_efficiency(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MeshEfficiency")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @mesh_efficiency.setter
    @exception_bridge
    @enforce_parameter_types
    def mesh_efficiency(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MeshEfficiency", value)

    @property
    @exception_bridge
    def use_specified_mesh_stiffness(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseSpecifiedMeshStiffness")

        if temp is None:
            return False

        return temp

    @use_specified_mesh_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def use_specified_mesh_stiffness(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseSpecifiedMeshStiffness",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def user_specified_mesh_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedMeshStiffness")

        if temp is None:
            return 0.0

        return temp

    @user_specified_mesh_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def user_specified_mesh_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UserSpecifiedMeshStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def active_gear_mesh_design(self: "Self") -> "_1053.GearMeshDesign":
        """mastapy.gears.gear_designs.GearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearMesh":
        """Cast to another type.

        Returns:
            _Cast_GearMesh
        """
        return _Cast_GearMesh(self)
