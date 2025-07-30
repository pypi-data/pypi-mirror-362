"""ElementPropertiesRigid"""

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
from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import _294

_ELEMENT_PROPERTIES_RIGID = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "ElementPropertiesRigid",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
        _306,
    )

    Self = TypeVar("Self", bound="ElementPropertiesRigid")
    CastSelf = TypeVar(
        "CastSelf", bound="ElementPropertiesRigid._Cast_ElementPropertiesRigid"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementPropertiesRigid",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementPropertiesRigid:
    """Special nested class for casting ElementPropertiesRigid to subclasses."""

    __parent__: "ElementPropertiesRigid"

    @property
    def element_properties_base(self: "CastSelf") -> "_294.ElementPropertiesBase":
        return self.__parent__._cast(_294.ElementPropertiesBase)

    @property
    def element_properties_rigid(self: "CastSelf") -> "ElementPropertiesRigid":
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
class ElementPropertiesRigid(_294.ElementPropertiesBase):
    """ElementPropertiesRigid

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_PROPERTIES_RIGID

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_degree_of_freedom_inputs(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfDegreeOfFreedomInputs")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def degrees_of_freedom_list(
        self: "Self",
    ) -> "List[_306.RigidElementNodeDegreesOfFreedom]":
        """List[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.RigidElementNodeDegreesOfFreedom]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DegreesOfFreedomList")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ElementPropertiesRigid":
        """Cast to another type.

        Returns:
            _Cast_ElementPropertiesRigid
        """
        return _Cast_ElementPropertiesRigid(self)
