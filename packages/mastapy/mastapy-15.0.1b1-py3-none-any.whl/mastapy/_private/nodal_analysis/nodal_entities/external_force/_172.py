"""ExternalForceLineContactEntity"""

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
from mastapy._private.nodal_analysis.nodal_entities.external_force import _171

_EXTERNAL_FORCE_LINE_CONTACT_ENTITY = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities.ExternalForce",
    "ExternalForceLineContactEntity",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _153, _155

    Self = TypeVar("Self", bound="ExternalForceLineContactEntity")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ExternalForceLineContactEntity._Cast_ExternalForceLineContactEntity",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExternalForceLineContactEntity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExternalForceLineContactEntity:
    """Special nested class for casting ExternalForceLineContactEntity to subclasses."""

    __parent__: "ExternalForceLineContactEntity"

    @property
    def external_force_entity(self: "CastSelf") -> "_171.ExternalForceEntity":
        return self.__parent__._cast(_171.ExternalForceEntity)

    @property
    def nodal_component(self: "CastSelf") -> "_153.NodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _153

        return self.__parent__._cast(_153.NodalComponent)

    @property
    def nodal_entity(self: "CastSelf") -> "_155.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.NodalEntity)

    @property
    def external_force_line_contact_entity(
        self: "CastSelf",
    ) -> "ExternalForceLineContactEntity":
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
class ExternalForceLineContactEntity(_171.ExternalForceEntity):
    """ExternalForceLineContactEntity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EXTERNAL_FORCE_LINE_CONTACT_ENTITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def force_normal_per_tooth_a(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceNormalPerToothA")

        if temp is None:
            return None

        value = conversion.to_list_any(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def force_normal_per_tooth_b(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceNormalPerToothB")

        if temp is None:
            return None

        value = conversion.to_list_any(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def interference_normal_maximum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InterferenceNormalMaximum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def interference_normal_mean(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InterferenceNormalMean")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def misalignment_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def moment_about_mesh_centre(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MomentAboutMeshCentre")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_contact_lines(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfContactLines")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_loaded_contact_lines(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfLoadedContactLines")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_deflection_normal_mean(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeDeflectionNormalMean")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_normal(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessNormal")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_tilt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessTilt")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def strain_energy(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrainEnergy")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def velocity_normal_mean(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VelocityNormalMean")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def velocity_normal_at_maximum_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "VelocityNormalAtMaximumInterference"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ExternalForceLineContactEntity":
        """Cast to another type.

        Returns:
            _Cast_ExternalForceLineContactEntity
        """
        return _Cast_ExternalForceLineContactEntity(self)
