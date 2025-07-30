"""SingleExcitationDetails"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_SINGLE_EXCITATION_DETAILS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses",
    "SingleExcitationDetails",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.acoustic_analyses import (
        _7671,
        _7672,
    )

    Self = TypeVar("Self", bound="SingleExcitationDetails")
    CastSelf = TypeVar(
        "CastSelf", bound="SingleExcitationDetails._Cast_SingleExcitationDetails"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SingleExcitationDetails",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SingleExcitationDetails:
    """Special nested class for casting SingleExcitationDetails to subclasses."""

    __parent__: "SingleExcitationDetails"

    @property
    def single_harmonic_excitation_analysis_detail(
        self: "CastSelf",
    ) -> "_7671.SingleHarmonicExcitationAnalysisDetail":
        from mastapy._private.system_model.analyses_and_results.acoustic_analyses import (
            _7671,
        )

        return self.__parent__._cast(_7671.SingleHarmonicExcitationAnalysisDetail)

    @property
    def unit_force_excitation_analysis_detail(
        self: "CastSelf",
    ) -> "_7672.UnitForceExcitationAnalysisDetail":
        from mastapy._private.system_model.analyses_and_results.acoustic_analyses import (
            _7672,
        )

        return self.__parent__._cast(_7672.UnitForceExcitationAnalysisDetail)

    @property
    def single_excitation_details(self: "CastSelf") -> "SingleExcitationDetails":
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
class SingleExcitationDetails(_0.APIBase):
    """SingleExcitationDetails

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SINGLE_EXCITATION_DETAILS

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
    def number_of_frequencies(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfFrequencies")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_frequencies_to_calculate(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfFrequenciesToCalculate")

        if temp is None:
            return 0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SingleExcitationDetails":
        """Cast to another type.

        Returns:
            _Cast_SingleExcitationDetails
        """
        return _Cast_SingleExcitationDetails(self)
