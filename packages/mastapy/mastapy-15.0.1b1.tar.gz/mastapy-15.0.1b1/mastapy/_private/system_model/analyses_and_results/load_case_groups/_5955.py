"""GenericClutchEngagementStatus"""

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

_GENERIC_CLUTCH_ENGAGEMENT_STATUS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups",
    "GenericClutchEngagementStatus",
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5951,
        _5952,
    )

    Self = TypeVar("Self", bound="GenericClutchEngagementStatus")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GenericClutchEngagementStatus._Cast_GenericClutchEngagementStatus",
    )

T = TypeVar("T", bound="_2414.DesignEntity")

__docformat__ = "restructuredtext en"
__all__ = ("GenericClutchEngagementStatus",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GenericClutchEngagementStatus:
    """Special nested class for casting GenericClutchEngagementStatus to subclasses."""

    __parent__: "GenericClutchEngagementStatus"

    @property
    def clutch_engagement_status(self: "CastSelf") -> "_5951.ClutchEngagementStatus":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5951,
        )

        return self.__parent__._cast(_5951.ClutchEngagementStatus)

    @property
    def concept_synchro_gear_engagement_status(
        self: "CastSelf",
    ) -> "_5952.ConceptSynchroGearEngagementStatus":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5952,
        )

        return self.__parent__._cast(_5952.ConceptSynchroGearEngagementStatus)

    @property
    def generic_clutch_engagement_status(
        self: "CastSelf",
    ) -> "GenericClutchEngagementStatus":
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
class GenericClutchEngagementStatus(_0.APIBase, Generic[T]):
    """GenericClutchEngagementStatus

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _GENERIC_CLUTCH_ENGAGEMENT_STATUS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def is_engaged(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsEngaged")

        if temp is None:
            return False

        return temp

    @is_engaged.setter
    @exception_bridge
    @enforce_parameter_types
    def is_engaged(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsEngaged", bool(value) if value is not None else False
        )

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
    def unique_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UniqueName")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_GenericClutchEngagementStatus":
        """Cast to another type.

        Returns:
            _Cast_GenericClutchEngagementStatus
        """
        return _Cast_GenericClutchEngagementStatus(self)
