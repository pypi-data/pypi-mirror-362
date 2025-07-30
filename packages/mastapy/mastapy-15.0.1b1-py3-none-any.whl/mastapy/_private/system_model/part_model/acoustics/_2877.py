"""MeshedResultSphere"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.acoustics import _2878, _2883

_MESHED_RESULT_SPHERE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Acoustics", "MeshedResultSphere"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.acoustics import _2879

    Self = TypeVar("Self", bound="MeshedResultSphere")
    CastSelf = TypeVar("CastSelf", bound="MeshedResultSphere._Cast_MeshedResultSphere")


__docformat__ = "restructuredtext en"
__all__ = ("MeshedResultSphere",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeshedResultSphere:
    """Special nested class for casting MeshedResultSphere to subclasses."""

    __parent__: "MeshedResultSphere"

    @property
    def meshed_result_surface(self: "CastSelf") -> "_2878.MeshedResultSurface":
        return self.__parent__._cast(_2878.MeshedResultSurface)

    @property
    def meshed_result_surface_base(self: "CastSelf") -> "_2879.MeshedResultSurfaceBase":
        from mastapy._private.system_model.part_model.acoustics import _2879

        return self.__parent__._cast(_2879.MeshedResultSurfaceBase)

    @property
    def meshed_result_sphere(self: "CastSelf") -> "MeshedResultSphere":
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
class MeshedResultSphere(_2878.MeshedResultSurface[_2883.ResultSphereOptions]):
    """MeshedResultSphere

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MESHED_RESULT_SPHERE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MeshedResultSphere":
        """Cast to another type.

        Returns:
            _Cast_MeshedResultSphere
        """
        return _Cast_MeshedResultSphere(self)
