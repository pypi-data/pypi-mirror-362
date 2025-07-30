"""CMSNodeGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis.dev_tools_analyses import _286

_CMS_NODE_GROUP = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis", "CMSNodeGroup"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.dev_tools_analyses import _267, _268

    Self = TypeVar("Self", bound="CMSNodeGroup")
    CastSelf = TypeVar("CastSelf", bound="CMSNodeGroup._Cast_CMSNodeGroup")


__docformat__ = "restructuredtext en"
__all__ = ("CMSNodeGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CMSNodeGroup:
    """Special nested class for casting CMSNodeGroup to subclasses."""

    __parent__: "CMSNodeGroup"

    @property
    def node_group(self: "CastSelf") -> "_286.NodeGroup":
        return self.__parent__._cast(_286.NodeGroup)

    @property
    def fe_entity_group_integer(self: "CastSelf") -> "_268.FEEntityGroupInteger":
        from mastapy._private.nodal_analysis.dev_tools_analyses import _268

        return self.__parent__._cast(_268.FEEntityGroupInteger)

    @property
    def fe_entity_group(self: "CastSelf") -> "_267.FEEntityGroup":
        from mastapy._private.nodal_analysis.dev_tools_analyses import _267

        return self.__parent__._cast(_267.FEEntityGroup)

    @property
    def cms_node_group(self: "CastSelf") -> "CMSNodeGroup":
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
class CMSNodeGroup(_286.NodeGroup):
    """CMSNodeGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CMS_NODE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def show_nvh_results_at_these_nodes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowNVHResultsAtTheseNodes")

        if temp is None:
            return False

        return temp

    @show_nvh_results_at_these_nodes.setter
    @exception_bridge
    @enforce_parameter_types
    def show_nvh_results_at_these_nodes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowNVHResultsAtTheseNodes",
            bool(value) if value is not None else False,
        )

    @exception_bridge
    def create_element_face_group(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateElementFaceGroup")

    @property
    def cast_to(self: "Self") -> "_Cast_CMSNodeGroup":
        """Cast to another type.

        Returns:
            _Cast_CMSNodeGroup
        """
        return _Cast_CMSNodeGroup(self)
