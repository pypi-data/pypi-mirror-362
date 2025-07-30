"""FEEntityGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_FE_ENTITY_GROUP = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "FEEntityGroup"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.nodal_analysis.component_mode_synthesis import (
        _310,
        _311,
        _313,
    )
    from mastapy._private.nodal_analysis.dev_tools_analyses import (
        _264,
        _265,
        _266,
        _268,
        _286,
    )

    Self = TypeVar("Self", bound="FEEntityGroup")
    CastSelf = TypeVar("CastSelf", bound="FEEntityGroup._Cast_FEEntityGroup")

T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("FEEntityGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEEntityGroup:
    """Special nested class for casting FEEntityGroup to subclasses."""

    __parent__: "FEEntityGroup"

    @property
    def element_edge_group(self: "CastSelf") -> "_264.ElementEdgeGroup":
        from mastapy._private.nodal_analysis.dev_tools_analyses import _264

        return self.__parent__._cast(_264.ElementEdgeGroup)

    @property
    def element_face_group(self: "CastSelf") -> "_265.ElementFaceGroup":
        from mastapy._private.nodal_analysis.dev_tools_analyses import _265

        return self.__parent__._cast(_265.ElementFaceGroup)

    @property
    def element_group(self: "CastSelf") -> "_266.ElementGroup":
        from mastapy._private.nodal_analysis.dev_tools_analyses import _266

        return self.__parent__._cast(_266.ElementGroup)

    @property
    def fe_entity_group_integer(self: "CastSelf") -> "_268.FEEntityGroupInteger":
        from mastapy._private.nodal_analysis.dev_tools_analyses import _268

        return self.__parent__._cast(_268.FEEntityGroupInteger)

    @property
    def node_group(self: "CastSelf") -> "_286.NodeGroup":
        from mastapy._private.nodal_analysis.dev_tools_analyses import _286

        return self.__parent__._cast(_286.NodeGroup)

    @property
    def cms_element_face_group(self: "CastSelf") -> "_310.CMSElementFaceGroup":
        from mastapy._private.nodal_analysis.component_mode_synthesis import _310

        return self.__parent__._cast(_310.CMSElementFaceGroup)

    @property
    def cms_element_face_group_of_all_free_faces(
        self: "CastSelf",
    ) -> "_311.CMSElementFaceGroupOfAllFreeFaces":
        from mastapy._private.nodal_analysis.component_mode_synthesis import _311

        return self.__parent__._cast(_311.CMSElementFaceGroupOfAllFreeFaces)

    @property
    def cms_node_group(self: "CastSelf") -> "_313.CMSNodeGroup":
        from mastapy._private.nodal_analysis.component_mode_synthesis import _313

        return self.__parent__._cast(_313.CMSNodeGroup)

    @property
    def fe_entity_group(self: "CastSelf") -> "FEEntityGroup":
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
class FEEntityGroup(_0.APIBase, Generic[T]):
    """FEEntityGroup

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _FE_ENTITY_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def number_of_items(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfItems")

        if temp is None:
            return 0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_FEEntityGroup":
        """Cast to another type.

        Returns:
            _Cast_FEEntityGroup
        """
        return _Cast_FEEntityGroup(self)
