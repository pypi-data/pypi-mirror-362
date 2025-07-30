"""NewtonRaphsonDegreeOfFreedomError"""

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

_NEWTON_RAPHSON_DEGREE_OF_FREEDOM_ERROR = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.SystemSolvers", "NewtonRaphsonDegreeOfFreedomError"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="NewtonRaphsonDegreeOfFreedomError")
    CastSelf = TypeVar(
        "CastSelf",
        bound="NewtonRaphsonDegreeOfFreedomError._Cast_NewtonRaphsonDegreeOfFreedomError",
    )


__docformat__ = "restructuredtext en"
__all__ = ("NewtonRaphsonDegreeOfFreedomError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NewtonRaphsonDegreeOfFreedomError:
    """Special nested class for casting NewtonRaphsonDegreeOfFreedomError to subclasses."""

    __parent__: "NewtonRaphsonDegreeOfFreedomError"

    @property
    def newton_raphson_degree_of_freedom_error(
        self: "CastSelf",
    ) -> "NewtonRaphsonDegreeOfFreedomError":
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
class NewtonRaphsonDegreeOfFreedomError(_0.APIBase):
    """NewtonRaphsonDegreeOfFreedomError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NEWTON_RAPHSON_DEGREE_OF_FREEDOM_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def degree_of_freedom(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DegreeOfFreedom")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def residual(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Residual")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scaled_residual(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScaledResidual")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_NewtonRaphsonDegreeOfFreedomError":
        """Cast to another type.

        Returns:
            _Cast_NewtonRaphsonDegreeOfFreedomError
        """
        return _Cast_NewtonRaphsonDegreeOfFreedomError(self)
