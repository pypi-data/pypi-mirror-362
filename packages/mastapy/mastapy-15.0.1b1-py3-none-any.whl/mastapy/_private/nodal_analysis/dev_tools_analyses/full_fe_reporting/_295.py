"""ElementPropertiesBeam"""

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
from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import _302

_ELEMENT_PROPERTIES_BEAM = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "ElementPropertiesBeam",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.fe_tools.vis_tools_global.vis_tools_global_enums import _1355
    from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
        _294,
    )

    Self = TypeVar("Self", bound="ElementPropertiesBeam")
    CastSelf = TypeVar(
        "CastSelf", bound="ElementPropertiesBeam._Cast_ElementPropertiesBeam"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementPropertiesBeam",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementPropertiesBeam:
    """Special nested class for casting ElementPropertiesBeam to subclasses."""

    __parent__: "ElementPropertiesBeam"

    @property
    def element_properties_with_material(
        self: "CastSelf",
    ) -> "_302.ElementPropertiesWithMaterial":
        return self.__parent__._cast(_302.ElementPropertiesWithMaterial)

    @property
    def element_properties_base(self: "CastSelf") -> "_294.ElementPropertiesBase":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _294,
        )

        return self.__parent__._cast(_294.ElementPropertiesBase)

    @property
    def element_properties_beam(self: "CastSelf") -> "ElementPropertiesBeam":
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
class ElementPropertiesBeam(_302.ElementPropertiesWithMaterial):
    """ElementPropertiesBeam

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_PROPERTIES_BEAM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def section_dimensions(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SectionDimensions")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def section_type(self: "Self") -> "_1355.BeamSectionType":
        """mastapy.fe_tools.vis_tools_global.vis_tools_global_enums.BeamSectionType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SectionType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.FETools.VisToolsGlobal.VisToolsGlobalEnums.BeamSectionType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.fe_tools.vis_tools_global.vis_tools_global_enums._1355",
            "BeamSectionType",
        )(value)

    @property
    def cast_to(self: "Self") -> "_Cast_ElementPropertiesBeam":
        """Cast to another type.

        Returns:
            _Cast_ElementPropertiesBeam
        """
        return _Cast_ElementPropertiesBeam(self)
