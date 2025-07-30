"""ResultSphereOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.acoustics import _2885

_RESULT_SPHERE_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Acoustics", "ResultSphereOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ResultSphereOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="ResultSphereOptions._Cast_ResultSphereOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResultSphereOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResultSphereOptions:
    """Special nested class for casting ResultSphereOptions to subclasses."""

    __parent__: "ResultSphereOptions"

    @property
    def result_surface_options(self: "CastSelf") -> "_2885.ResultSurfaceOptions":
        return self.__parent__._cast(_2885.ResultSurfaceOptions)

    @property
    def result_sphere_options(self: "CastSelf") -> "ResultSphereOptions":
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
class ResultSphereOptions(_2885.ResultSurfaceOptions):
    """ResultSphereOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RESULT_SPHERE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ResultSphereOptions":
        """Cast to another type.

        Returns:
            _Cast_ResultSphereOptions
        """
        return _Cast_ResultSphereOptions(self)
