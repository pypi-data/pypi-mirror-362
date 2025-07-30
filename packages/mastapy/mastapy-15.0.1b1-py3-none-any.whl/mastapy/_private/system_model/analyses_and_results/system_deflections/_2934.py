"""BearingDynamicElementContactPropertyWrapper"""

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

_BEARING_DYNAMIC_ELEMENT_CONTACT_PROPERTY_WRAPPER = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "BearingDynamicElementContactPropertyWrapper",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2937,
    )

    Self = TypeVar("Self", bound="BearingDynamicElementContactPropertyWrapper")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BearingDynamicElementContactPropertyWrapper._Cast_BearingDynamicElementContactPropertyWrapper",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingDynamicElementContactPropertyWrapper",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingDynamicElementContactPropertyWrapper:
    """Special nested class for casting BearingDynamicElementContactPropertyWrapper to subclasses."""

    __parent__: "BearingDynamicElementContactPropertyWrapper"

    @property
    def bearing_dynamic_element_contact_property_wrapper(
        self: "CastSelf",
    ) -> "BearingDynamicElementContactPropertyWrapper":
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
class BearingDynamicElementContactPropertyWrapper(_0.APIBase):
    """BearingDynamicElementContactPropertyWrapper

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_DYNAMIC_ELEMENT_CONTACT_PROPERTY_WRAPPER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def contact_results(
        self: "Self",
    ) -> "List[_2937.BearingDynamicResultsPropertyWrapper]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BearingDynamicResultsPropertyWrapper]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BearingDynamicElementContactPropertyWrapper":
        """Cast to another type.

        Returns:
            _Cast_BearingDynamicElementContactPropertyWrapper
        """
        return _Cast_BearingDynamicElementContactPropertyWrapper(self)
