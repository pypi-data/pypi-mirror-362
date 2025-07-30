"""RollingBearingFromCAD"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.import_from_cad import _2733

_ROLLING_BEARING_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "RollingBearingFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import (
        _2730,
        _2731,
        _2740,
    )

    Self = TypeVar("Self", bound="RollingBearingFromCAD")
    CastSelf = TypeVar(
        "CastSelf", bound="RollingBearingFromCAD._Cast_RollingBearingFromCAD"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollingBearingFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollingBearingFromCAD:
    """Special nested class for casting RollingBearingFromCAD to subclasses."""

    __parent__: "RollingBearingFromCAD"

    @property
    def connector_from_cad(self: "CastSelf") -> "_2733.ConnectorFromCAD":
        return self.__parent__._cast(_2733.ConnectorFromCAD)

    @property
    def mountable_component_from_cad(
        self: "CastSelf",
    ) -> "_2740.MountableComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2740

        return self.__parent__._cast(_2740.MountableComponentFromCAD)

    @property
    def component_from_cad(self: "CastSelf") -> "_2730.ComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2730

        return self.__parent__._cast(_2730.ComponentFromCAD)

    @property
    def component_from_cad_base(self: "CastSelf") -> "_2731.ComponentFromCADBase":
        from mastapy._private.system_model.part_model.import_from_cad import _2731

        return self.__parent__._cast(_2731.ComponentFromCADBase)

    @property
    def rolling_bearing_from_cad(self: "CastSelf") -> "RollingBearingFromCAD":
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
class RollingBearingFromCAD(_2733.ConnectorFromCAD):
    """RollingBearingFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLING_BEARING_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bore(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Bore")

        if temp is None:
            return 0.0

        return temp

    @bore.setter
    @exception_bridge
    @enforce_parameter_types
    def bore(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Bore", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RollingBearingFromCAD":
        """Cast to another type.

        Returns:
            _Cast_RollingBearingFromCAD
        """
        return _Cast_RollingBearingFromCAD(self)
