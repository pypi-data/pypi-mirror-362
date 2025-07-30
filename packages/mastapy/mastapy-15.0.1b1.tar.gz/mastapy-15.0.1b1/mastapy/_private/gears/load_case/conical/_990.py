"""ConicalMeshLoadCase"""

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
from mastapy._private.gears.load_case import _978

_CONICAL_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.Gears.LoadCase.Conical", "ConicalMeshLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1336, _1342
    from mastapy._private.gears.gear_designs.conical import _1270, _1280
    from mastapy._private.gears.load_case.bevel import _995

    Self = TypeVar("Self", bound="ConicalMeshLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalMeshLoadCase._Cast_ConicalMeshLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshLoadCase:
    """Special nested class for casting ConicalMeshLoadCase to subclasses."""

    __parent__: "ConicalMeshLoadCase"

    @property
    def mesh_load_case(self: "CastSelf") -> "_978.MeshLoadCase":
        return self.__parent__._cast(_978.MeshLoadCase)

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
    def bevel_mesh_load_case(self: "CastSelf") -> "_995.BevelMeshLoadCase":
        from mastapy._private.gears.load_case.bevel import _995

        return self.__parent__._cast(_995.BevelMeshLoadCase)

    @property
    def conical_mesh_load_case(self: "CastSelf") -> "ConicalMeshLoadCase":
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
class ConicalMeshLoadCase(_978.MeshLoadCase):
    """ConicalMeshLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESH_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def active_flank(self: "Self") -> "_1270.ActiveConicalFlank":
        """mastapy.gears.gear_designs.conical.ActiveConicalFlank

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveFlank")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Conical.ActiveConicalFlank"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.conical._1270", "ActiveConicalFlank"
        )(value)

    @property
    @exception_bridge
    def include_mesh_node_misalignments_in_default_report(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "IncludeMeshNodeMisalignmentsInDefaultReport"
        )

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def use_user_specified_misalignments_in_tca(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseUserSpecifiedMisalignmentsInTCA"
        )

        if temp is None:
            return False

        return temp

    @use_user_specified_misalignments_in_tca.setter
    @exception_bridge
    @enforce_parameter_types
    def use_user_specified_misalignments_in_tca(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseUserSpecifiedMisalignmentsInTCA",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def mesh_node_misalignments_pinion(
        self: "Self",
    ) -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshNodeMisalignmentsPinion")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_node_misalignments_total(self: "Self") -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshNodeMisalignmentsTotal")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_node_misalignments_wheel(self: "Self") -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshNodeMisalignmentsWheel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignments_pinion(self: "Self") -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentsPinion")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignments_total(self: "Self") -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentsTotal")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignments_wheel(self: "Self") -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentsWheel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_pinion(
        self: "Self",
    ) -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodePinion",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_total(
        self: "Self",
    ) -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeTotal",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_wheel(
        self: "Self",
    ) -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeWheel",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def user_specified_misalignments(self: "Self") -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedMisalignments")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshLoadCase":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshLoadCase
        """
        return _Cast_ConicalMeshLoadCase(self)
