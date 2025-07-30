"""ElementDetailsForFEModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_ELEMENT_DETAILS_FOR_FE_MODEL = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "ElementDetailsForFEModel",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="ElementDetailsForFEModel")
    CastSelf = TypeVar(
        "CastSelf", bound="ElementDetailsForFEModel._Cast_ElementDetailsForFEModel"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementDetailsForFEModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementDetailsForFEModel:
    """Special nested class for casting ElementDetailsForFEModel to subclasses."""

    __parent__: "ElementDetailsForFEModel"

    @property
    def element_details_for_fe_model(self: "CastSelf") -> "ElementDetailsForFEModel":
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
class ElementDetailsForFEModel(_0.APIBase):
    """ElementDetailsForFEModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_DETAILS_FOR_FE_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def element_areas(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementAreas")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def element_ids_with_negative_jacobian(self: "Self") -> "List[int]":
        """List[int]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementIdsWithNegativeJacobian")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, int)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def element_ids_with_negative_size(self: "Self") -> "List[int]":
        """List[int]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementIdsWithNegativeSize")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, int)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def element_ids_with_no_material(self: "Self") -> "List[int]":
        """List[int]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementIdsWithNoMaterial")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, int)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def element_volumes(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementVolumes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def external_ids(self: "Self") -> "List[int]":
        """List[int]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExternalIDs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, int)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def node_ids_for_elements(self: "Self") -> "List[List[int]]":
        """List[List[int]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeIDsForElements")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list_of_lists(temp, int)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def total_element_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalElementArea")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_element_volume(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalElementVolume")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ElementDetailsForFEModel":
        """Cast to another type.

        Returns:
            _Cast_ElementDetailsForFEModel
        """
        return _Cast_ElementDetailsForFEModel(self)
