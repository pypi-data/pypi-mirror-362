"""RotorSetDataInputFileOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility_gui import _2051

_ROTOR_SET_DATA_INPUT_FILE_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet",
    "RotorSetDataInputFileOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RotorSetDataInputFileOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RotorSetDataInputFileOptions._Cast_RotorSetDataInputFileOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RotorSetDataInputFileOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RotorSetDataInputFileOptions:
    """Special nested class for casting RotorSetDataInputFileOptions to subclasses."""

    __parent__: "RotorSetDataInputFileOptions"

    @property
    def data_input_file_options(self: "CastSelf") -> "_2051.DataInputFileOptions":
        return self.__parent__._cast(_2051.DataInputFileOptions)

    @property
    def rotor_set_data_input_file_options(
        self: "CastSelf",
    ) -> "RotorSetDataInputFileOptions":
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
class RotorSetDataInputFileOptions(_2051.DataInputFileOptions):
    """RotorSetDataInputFileOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROTOR_SET_DATA_INPUT_FILE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RotorSetDataInputFileOptions":
        """Cast to another type.

        Returns:
            _Cast_RotorSetDataInputFileOptions
        """
        return _Cast_RotorSetDataInputFileOptions(self)
