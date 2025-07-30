"""GearSetStaticLoadCaseGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
    _5967,
)

_GEAR_SET_STATIC_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups",
    "GearSetStaticLoadCaseGroup",
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
        _5963,
        _5964,
        _5965,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7759,
        _7761,
        _7764,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2534
    from mastapy._private.system_model.part_model.gears import _2767, _2769

    Self = TypeVar("Self", bound="GearSetStaticLoadCaseGroup")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetStaticLoadCaseGroup._Cast_GearSetStaticLoadCaseGroup"
    )

TGearSet = TypeVar("TGearSet", bound="_2769.GearSet")
TGear = TypeVar("TGear", bound="_2767.Gear")
TGearStaticLoad = TypeVar("TGearStaticLoad", bound="_7759.GearLoadCase")
TGearMesh = TypeVar("TGearMesh", bound="_2534.GearMesh")
TGearMeshStaticLoad = TypeVar("TGearMeshStaticLoad", bound="_7761.GearMeshLoadCase")
TGearSetStaticLoad = TypeVar("TGearSetStaticLoad", bound="_7764.GearSetLoadCase")

__docformat__ = "restructuredtext en"
__all__ = ("GearSetStaticLoadCaseGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetStaticLoadCaseGroup:
    """Special nested class for casting GearSetStaticLoadCaseGroup to subclasses."""

    __parent__: "GearSetStaticLoadCaseGroup"

    @property
    def part_static_load_case_group(
        self: "CastSelf",
    ) -> "_5967.PartStaticLoadCaseGroup":
        return self.__parent__._cast(_5967.PartStaticLoadCaseGroup)

    @property
    def design_entity_static_load_case_group(
        self: "CastSelf",
    ) -> "_5965.DesignEntityStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
            _5965,
        )

        return self.__parent__._cast(_5965.DesignEntityStaticLoadCaseGroup)

    @property
    def gear_set_static_load_case_group(
        self: "CastSelf",
    ) -> "GearSetStaticLoadCaseGroup":
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
class GearSetStaticLoadCaseGroup(
    _5967.PartStaticLoadCaseGroup,
    Generic[
        TGearSet,
        TGear,
        TGearStaticLoad,
        TGearMesh,
        TGearMeshStaticLoad,
        TGearSetStaticLoad,
    ],
):
    """GearSetStaticLoadCaseGroup

    This is a mastapy class.

    Generic Types:
        TGearSet
        TGear
        TGearStaticLoad
        TGearMesh
        TGearMeshStaticLoad
        TGearSetStaticLoad
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_STATIC_LOAD_CASE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def part(self: "Self") -> "TGearSet":
        """TGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Part")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_set(self: "Self") -> "TGearSet":
        """TGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def part_load_cases(self: "Self") -> "List[TGearSetStaticLoad]":
        """List[TGearSetStaticLoad]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_set_load_cases(self: "Self") -> "List[TGearSetStaticLoad]":
        """List[TGearSetStaticLoad]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gears_load_cases(
        self: "Self",
    ) -> "List[_5963.ComponentStaticLoadCaseGroup[TGear, TGearStaticLoad]]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups.ComponentStaticLoadCaseGroup[TGear, TGearStaticLoad]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshes_load_cases(
        self: "Self",
    ) -> "List[_5964.ConnectionStaticLoadCaseGroup[TGearMesh, TGearMeshStaticLoad]]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups.ConnectionStaticLoadCaseGroup[TGearMesh, TGearMeshStaticLoad]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetStaticLoadCaseGroup":
        """Cast to another type.

        Returns:
            _Cast_GearSetStaticLoadCaseGroup
        """
        return _Cast_GearSetStaticLoadCaseGroup(self)
