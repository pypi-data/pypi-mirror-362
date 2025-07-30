"""ConnectionStaticLoadCaseGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
    _5965,
)

_CONNECTION_STATIC_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups",
    "ConnectionStaticLoadCaseGroup",
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.system_model.analyses_and_results.static_loads import _7718
    from mastapy._private.system_model.connections_and_sockets import _2493

    Self = TypeVar("Self", bound="ConnectionStaticLoadCaseGroup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionStaticLoadCaseGroup._Cast_ConnectionStaticLoadCaseGroup",
    )

TConnection = TypeVar("TConnection", bound="_2493.Connection")
TConnectionStaticLoad = TypeVar(
    "TConnectionStaticLoad", bound="_7718.ConnectionLoadCase"
)

__docformat__ = "restructuredtext en"
__all__ = ("ConnectionStaticLoadCaseGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionStaticLoadCaseGroup:
    """Special nested class for casting ConnectionStaticLoadCaseGroup to subclasses."""

    __parent__: "ConnectionStaticLoadCaseGroup"

    @property
    def design_entity_static_load_case_group(
        self: "CastSelf",
    ) -> "_5965.DesignEntityStaticLoadCaseGroup":
        return self.__parent__._cast(_5965.DesignEntityStaticLoadCaseGroup)

    @property
    def connection_static_load_case_group(
        self: "CastSelf",
    ) -> "ConnectionStaticLoadCaseGroup":
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
class ConnectionStaticLoadCaseGroup(
    _5965.DesignEntityStaticLoadCaseGroup, Generic[TConnection, TConnectionStaticLoad]
):
    """ConnectionStaticLoadCaseGroup

    This is a mastapy class.

    Generic Types:
        TConnection
        TConnectionStaticLoad
    """

    TYPE: ClassVar["Type"] = _CONNECTION_STATIC_LOAD_CASE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection(self: "Self") -> "TConnection":
        """TConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Connection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_load_cases(self: "Self") -> "List[TConnectionStaticLoad]":
        """List[TConnectionStaticLoad]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionStaticLoadCaseGroup":
        """Cast to another type.

        Returns:
            _Cast_ConnectionStaticLoadCaseGroup
        """
        return _Cast_ConnectionStaticLoadCaseGroup(self)
