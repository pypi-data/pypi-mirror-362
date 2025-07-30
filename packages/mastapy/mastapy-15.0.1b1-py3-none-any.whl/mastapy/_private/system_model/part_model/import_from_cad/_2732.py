"""ConceptBearingFromCAD"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.import_from_cad import _2733

_CONCEPT_BEARING_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "ConceptBearingFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import (
        _2730,
        _2731,
        _2740,
    )

    Self = TypeVar("Self", bound="ConceptBearingFromCAD")
    CastSelf = TypeVar(
        "CastSelf", bound="ConceptBearingFromCAD._Cast_ConceptBearingFromCAD"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptBearingFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptBearingFromCAD:
    """Special nested class for casting ConceptBearingFromCAD to subclasses."""

    __parent__: "ConceptBearingFromCAD"

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
    def concept_bearing_from_cad(self: "CastSelf") -> "ConceptBearingFromCAD":
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
class ConceptBearingFromCAD(_2733.ConnectorFromCAD):
    """ConceptBearingFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_BEARING_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptBearingFromCAD":
        """Cast to another type.

        Returns:
            _Cast_ConceptBearingFromCAD
        """
        return _Cast_ConceptBearingFromCAD(self)
