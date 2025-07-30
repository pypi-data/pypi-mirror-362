"""RealMatrix"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.math_utility import _1698

_REAL_MATRIX = python_net_import("SMT.MastaAPI.MathUtility", "RealMatrix")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1693, _1708, _1710, _1715, _1719

    Self = TypeVar("Self", bound="RealMatrix")
    CastSelf = TypeVar("CastSelf", bound="RealMatrix._Cast_RealMatrix")


__docformat__ = "restructuredtext en"
__all__ = ("RealMatrix",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RealMatrix:
    """Special nested class for casting RealMatrix to subclasses."""

    __parent__: "RealMatrix"

    @property
    def generic_matrix(self: "CastSelf") -> "_1698.GenericMatrix":
        pass

        return self.__parent__._cast(_1698.GenericMatrix)

    @property
    def euler_parameters(self: "CastSelf") -> "_1693.EulerParameters":
        from mastapy._private.math_utility import _1693

        return self.__parent__._cast(_1693.EulerParameters)

    @property
    def quaternion(self: "CastSelf") -> "_1708.Quaternion":
        from mastapy._private.math_utility import _1708

        return self.__parent__._cast(_1708.Quaternion)

    @property
    def real_vector(self: "CastSelf") -> "_1710.RealVector":
        from mastapy._private.math_utility import _1710

        return self.__parent__._cast(_1710.RealVector)

    @property
    def square_matrix(self: "CastSelf") -> "_1715.SquareMatrix":
        from mastapy._private.math_utility import _1715

        return self.__parent__._cast(_1715.SquareMatrix)

    @property
    def vector_6d(self: "CastSelf") -> "_1719.Vector6D":
        from mastapy._private.math_utility import _1719

        return self.__parent__._cast(_1719.Vector6D)

    @property
    def real_matrix(self: "CastSelf") -> "RealMatrix":
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
class RealMatrix(_1698.GenericMatrix[float, "RealMatrix"]):
    """RealMatrix

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _REAL_MATRIX

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    @enforce_parameter_types
    def get_column_at(self: "Self", index: "int") -> "List[float]":
        """List[float]

        Args:
            index (int)
        """
        index = int(index)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(self.wrapped, "GetColumnAt", index if index else 0),
            float,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_row_at(self: "Self", index: "int") -> "List[float]":
        """List[float]

        Args:
            index (int)
        """
        index = int(index)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(self.wrapped, "GetRowAt", index if index else 0),
            float,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RealMatrix":
        """Cast to another type.

        Returns:
            _Cast_RealMatrix
        """
        return _Cast_RealMatrix(self)
