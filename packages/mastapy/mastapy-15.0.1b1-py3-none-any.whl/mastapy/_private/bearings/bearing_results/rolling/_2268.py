"""MaximumStaticContactStress"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2270

_MAXIMUM_STATIC_CONTACT_STRESS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "MaximumStaticContactStress"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MaximumStaticContactStress")
    CastSelf = TypeVar(
        "CastSelf", bound="MaximumStaticContactStress._Cast_MaximumStaticContactStress"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MaximumStaticContactStress",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MaximumStaticContactStress:
    """Special nested class for casting MaximumStaticContactStress to subclasses."""

    __parent__: "MaximumStaticContactStress"

    @property
    def maximum_static_contact_stress_results_abstract(
        self: "CastSelf",
    ) -> "_2270.MaximumStaticContactStressResultsAbstract":
        return self.__parent__._cast(_2270.MaximumStaticContactStressResultsAbstract)

    @property
    def maximum_static_contact_stress(self: "CastSelf") -> "MaximumStaticContactStress":
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
class MaximumStaticContactStress(_2270.MaximumStaticContactStressResultsAbstract):
    """MaximumStaticContactStress

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MAXIMUM_STATIC_CONTACT_STRESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MaximumStaticContactStress":
        """Cast to another type.

        Returns:
            _Cast_MaximumStaticContactStress
        """
        return _Cast_MaximumStaticContactStress(self)
