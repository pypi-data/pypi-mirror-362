"""ElementPropertiesShell"""

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

_ELEMENT_PROPERTIES_SHELL = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "ElementPropertiesShell",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.fe_tools.vis_tools_global.vis_tools_global_enums import _1358
    from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
        _294,
    )

    Self = TypeVar("Self", bound="ElementPropertiesShell")
    CastSelf = TypeVar(
        "CastSelf", bound="ElementPropertiesShell._Cast_ElementPropertiesShell"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementPropertiesShell",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementPropertiesShell:
    """Special nested class for casting ElementPropertiesShell to subclasses."""

    __parent__: "ElementPropertiesShell"

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
    def element_properties_shell(self: "CastSelf") -> "ElementPropertiesShell":
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
class ElementPropertiesShell(_302.ElementPropertiesWithMaterial):
    """ElementPropertiesShell

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_PROPERTIES_SHELL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def effective_shear_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveShearRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def layer_thicknesses(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LayerThicknesses")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def number_of_layers(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfLayers")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Thickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wall_type(self: "Self") -> "_1358.ElementPropertiesShellWallType":
        """mastapy.fe_tools.vis_tools_global.vis_tools_global_enums.ElementPropertiesShellWallType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WallType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.FETools.VisToolsGlobal.VisToolsGlobalEnums.ElementPropertiesShellWallType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.fe_tools.vis_tools_global.vis_tools_global_enums._1358",
            "ElementPropertiesShellWallType",
        )(value)

    @property
    def cast_to(self: "Self") -> "_Cast_ElementPropertiesShell":
        """Cast to another type.

        Returns:
            _Cast_ElementPropertiesShell
        """
        return _Cast_ElementPropertiesShell(self)
