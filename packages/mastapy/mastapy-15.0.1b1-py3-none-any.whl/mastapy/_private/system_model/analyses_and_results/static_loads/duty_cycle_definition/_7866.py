"""LoadCaseNameOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility_gui import _2050

_LOAD_CASE_NAME_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition",
    "LoadCaseNameOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LoadCaseNameOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadCaseNameOptions._Cast_LoadCaseNameOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadCaseNameOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadCaseNameOptions:
    """Special nested class for casting LoadCaseNameOptions to subclasses."""

    __parent__: "LoadCaseNameOptions"

    @property
    def column_input_options(self: "CastSelf") -> "_2050.ColumnInputOptions":
        return self.__parent__._cast(_2050.ColumnInputOptions)

    @property
    def load_case_name_options(self: "CastSelf") -> "LoadCaseNameOptions":
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
class LoadCaseNameOptions(_2050.ColumnInputOptions):
    """LoadCaseNameOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOAD_CASE_NAME_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadCaseNameOptions":
        """Cast to another type.

        Returns:
            _Cast_LoadCaseNameOptions
        """
        return _Cast_LoadCaseNameOptions(self)
