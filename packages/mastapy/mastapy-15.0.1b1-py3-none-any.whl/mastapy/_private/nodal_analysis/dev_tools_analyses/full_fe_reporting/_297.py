"""ElementPropertiesMass"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import _294

_ELEMENT_PROPERTIES_MASS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "ElementPropertiesMass",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1701

    Self = TypeVar("Self", bound="ElementPropertiesMass")
    CastSelf = TypeVar(
        "CastSelf", bound="ElementPropertiesMass._Cast_ElementPropertiesMass"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementPropertiesMass",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementPropertiesMass:
    """Special nested class for casting ElementPropertiesMass to subclasses."""

    __parent__: "ElementPropertiesMass"

    @property
    def element_properties_base(self: "CastSelf") -> "_294.ElementPropertiesBase":
        return self.__parent__._cast(_294.ElementPropertiesBase)

    @property
    def element_properties_mass(self: "CastSelf") -> "ElementPropertiesMass":
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
class ElementPropertiesMass(_294.ElementPropertiesBase):
    """ElementPropertiesMass

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_PROPERTIES_MASS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def inertia(self: "Self") -> "_1701.InertiaTensor":
        """mastapy.math_utility.InertiaTensor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Inertia")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mass(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ElementPropertiesMass":
        """Cast to another type.

        Returns:
            _Cast_ElementPropertiesMass
        """
        return _Cast_ElementPropertiesMass(self)
