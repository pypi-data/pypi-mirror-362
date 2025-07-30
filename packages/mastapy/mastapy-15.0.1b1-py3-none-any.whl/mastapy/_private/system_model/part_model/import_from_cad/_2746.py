"""ShaftFromCADAuto"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.import_from_cad import _2731

_SHAFT_FROM_CAD_AUTO = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "ShaftFromCADAuto"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.shafts import _31, _35

    Self = TypeVar("Self", bound="ShaftFromCADAuto")
    CastSelf = TypeVar("CastSelf", bound="ShaftFromCADAuto._Cast_ShaftFromCADAuto")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftFromCADAuto",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftFromCADAuto:
    """Special nested class for casting ShaftFromCADAuto to subclasses."""

    __parent__: "ShaftFromCADAuto"

    @property
    def component_from_cad_base(self: "CastSelf") -> "_2731.ComponentFromCADBase":
        return self.__parent__._cast(_2731.ComponentFromCADBase)

    @property
    def shaft_from_cad_auto(self: "CastSelf") -> "ShaftFromCADAuto":
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
class ShaftFromCADAuto(_2731.ComponentFromCADBase):
    """ShaftFromCADAuto

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_FROM_CAD_AUTO

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def create_assembly(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CreateAssembly")

        if temp is None:
            return False

        return temp

    @create_assembly.setter
    @exception_bridge
    @enforce_parameter_types
    def create_assembly(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "CreateAssembly", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def shaft_profile_type(self: "Self") -> "_35.ShaftProfileType":
        """mastapy.shafts.ShaftProfileType"""
        temp = pythonnet_property_get(self.wrapped, "ShaftProfileType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Shafts.ShaftProfileType")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.shafts._35", "ShaftProfileType"
        )(value)

    @shaft_profile_type.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_profile_type(self: "Self", value: "_35.ShaftProfileType") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Shafts.ShaftProfileType")
        pythonnet_property_set(self.wrapped, "ShaftProfileType", value)

    @property
    @exception_bridge
    def shaft_information(self: "Self") -> "_31.ShaftProfileFromImport":
        """mastapy.shafts.ShaftProfileFromImport

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftInformation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftFromCADAuto":
        """Cast to another type.

        Returns:
            _Cast_ShaftFromCADAuto
        """
        return _Cast_ShaftFromCADAuto(self)
