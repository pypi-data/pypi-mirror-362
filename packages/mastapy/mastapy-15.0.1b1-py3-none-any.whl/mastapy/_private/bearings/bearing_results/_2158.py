"""LoadedConceptClearanceBearingResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results import _2163

_LOADED_CONCEPT_CLEARANCE_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedConceptClearanceBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2078
    from mastapy._private.bearings.bearing_results import _2155, _2157, _2159

    Self = TypeVar("Self", bound="LoadedConceptClearanceBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedConceptClearanceBearingResults._Cast_LoadedConceptClearanceBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedConceptClearanceBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedConceptClearanceBearingResults:
    """Special nested class for casting LoadedConceptClearanceBearingResults to subclasses."""

    __parent__: "LoadedConceptClearanceBearingResults"

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2163.LoadedNonLinearBearingResults":
        return self.__parent__._cast(_2163.LoadedNonLinearBearingResults)

    @property
    def loaded_bearing_results(self: "CastSelf") -> "_2155.LoadedBearingResults":
        from mastapy._private.bearings.bearing_results import _2155

        return self.__parent__._cast(_2155.LoadedBearingResults)

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "_2078.BearingLoadCaseResultsLightweight":
        from mastapy._private.bearings import _2078

        return self.__parent__._cast(_2078.BearingLoadCaseResultsLightweight)

    @property
    def loaded_concept_axial_clearance_bearing_results(
        self: "CastSelf",
    ) -> "_2157.LoadedConceptAxialClearanceBearingResults":
        from mastapy._private.bearings.bearing_results import _2157

        return self.__parent__._cast(_2157.LoadedConceptAxialClearanceBearingResults)

    @property
    def loaded_concept_radial_clearance_bearing_results(
        self: "CastSelf",
    ) -> "_2159.LoadedConceptRadialClearanceBearingResults":
        from mastapy._private.bearings.bearing_results import _2159

        return self.__parent__._cast(_2159.LoadedConceptRadialClearanceBearingResults)

    @property
    def loaded_concept_clearance_bearing_results(
        self: "CastSelf",
    ) -> "LoadedConceptClearanceBearingResults":
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
class LoadedConceptClearanceBearingResults(_2163.LoadedNonLinearBearingResults):
    """LoadedConceptClearanceBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_CONCEPT_CLEARANCE_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def is_in_contact(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsInContact")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def relative_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedConceptClearanceBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedConceptClearanceBearingResults
        """
        return _Cast_LoadedConceptClearanceBearingResults(self)
