"""AbstractLinearConnectionProperties"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

_ABSTRACT_LINEAR_CONNECTION_PROPERTIES = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "AbstractLinearConnectionProperties"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis import _75, _76

    Self = TypeVar("Self", bound="AbstractLinearConnectionProperties")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractLinearConnectionProperties._Cast_AbstractLinearConnectionProperties",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractLinearConnectionProperties",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractLinearConnectionProperties:
    """Special nested class for casting AbstractLinearConnectionProperties to subclasses."""

    __parent__: "AbstractLinearConnectionProperties"

    @property
    def linear_damping_connection_properties(
        self: "CastSelf",
    ) -> "_75.LinearDampingConnectionProperties":
        from mastapy._private.nodal_analysis import _75

        return self.__parent__._cast(_75.LinearDampingConnectionProperties)

    @property
    def linear_stiffness_properties(
        self: "CastSelf",
    ) -> "_76.LinearStiffnessProperties":
        from mastapy._private.nodal_analysis import _76

        return self.__parent__._cast(_76.LinearStiffnessProperties)

    @property
    def abstract_linear_connection_properties(
        self: "CastSelf",
    ) -> "AbstractLinearConnectionProperties":
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
class AbstractLinearConnectionProperties(_0.APIBase):
    """AbstractLinearConnectionProperties

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_LINEAR_CONNECTION_PROPERTIES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractLinearConnectionProperties":
        """Cast to another type.

        Returns:
            _Cast_AbstractLinearConnectionProperties
        """
        return _Cast_AbstractLinearConnectionProperties(self)
