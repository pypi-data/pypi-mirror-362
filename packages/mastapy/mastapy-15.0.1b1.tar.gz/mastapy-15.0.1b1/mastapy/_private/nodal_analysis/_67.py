"""FEModalFrequencyComparison"""

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

_FE_MODAL_FREQUENCY_COMPARISON = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "FEModalFrequencyComparison"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FEModalFrequencyComparison")
    CastSelf = TypeVar(
        "CastSelf", bound="FEModalFrequencyComparison._Cast_FEModalFrequencyComparison"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEModalFrequencyComparison",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEModalFrequencyComparison:
    """Special nested class for casting FEModalFrequencyComparison to subclasses."""

    __parent__: "FEModalFrequencyComparison"

    @property
    def fe_modal_frequency_comparison(self: "CastSelf") -> "FEModalFrequencyComparison":
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
class FEModalFrequencyComparison(_0.APIBase):
    """FEModalFrequencyComparison

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_MODAL_FREQUENCY_COMPARISON

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def difference_in_frequencies(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DifferenceInFrequencies")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def full_model_frequency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullModelFrequency")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mode(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mode")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def percentage_error(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PercentageError")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reduced_model_frequency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReducedModelFrequency")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_FEModalFrequencyComparison":
        """Cast to another type.

        Returns:
            _Cast_FEModalFrequencyComparison
        """
        return _Cast_FEModalFrequencyComparison(self)
