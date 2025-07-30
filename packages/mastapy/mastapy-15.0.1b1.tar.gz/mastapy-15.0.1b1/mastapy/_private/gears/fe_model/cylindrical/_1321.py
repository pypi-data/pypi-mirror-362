"""CylindricalGearFEModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.fe_model import _1317

_CYLINDRICAL_GEAR_FE_MODEL = python_net_import(
    "SMT.MastaAPI.Gears.FEModel.Cylindrical", "CylindricalGearFEModel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1335, _1338, _1341

    Self = TypeVar("Self", bound="CylindricalGearFEModel")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearFEModel._Cast_CylindricalGearFEModel"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearFEModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearFEModel:
    """Special nested class for casting CylindricalGearFEModel to subclasses."""

    __parent__: "CylindricalGearFEModel"

    @property
    def gear_fe_model(self: "CastSelf") -> "_1317.GearFEModel":
        return self.__parent__._cast(_1317.GearFEModel)

    @property
    def gear_implementation_detail(
        self: "CastSelf",
    ) -> "_1341.GearImplementationDetail":
        from mastapy._private.gears.analysis import _1341

        return self.__parent__._cast(_1341.GearImplementationDetail)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1338.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1338

        return self.__parent__._cast(_1338.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def cylindrical_gear_fe_model(self: "CastSelf") -> "CylindricalGearFEModel":
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
class CylindricalGearFEModel(_1317.GearFEModel):
    """CylindricalGearFEModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_FE_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def thickness_for_analyses(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "ThicknessForAnalyses")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @thickness_for_analyses.setter
    @exception_bridge
    @enforce_parameter_types
    def thickness_for_analyses(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ThicknessForAnalyses", value)

    @property
    @exception_bridge
    def use_specified_web(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseSpecifiedWeb")

        if temp is None:
            return False

        return temp

    @use_specified_web.setter
    @exception_bridge
    @enforce_parameter_types
    def use_specified_web(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UseSpecifiedWeb", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearFEModel":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearFEModel
        """
        return _Cast_CylindricalGearFEModel(self)
