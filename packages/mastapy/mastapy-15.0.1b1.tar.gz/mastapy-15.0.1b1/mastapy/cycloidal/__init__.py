"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.cycloidal._1636 import ContactSpecification
    from mastapy._private.cycloidal._1637 import CrowningSpecificationMethod
    from mastapy._private.cycloidal._1638 import CycloidalAssemblyDesign
    from mastapy._private.cycloidal._1639 import CycloidalDiscDesign
    from mastapy._private.cycloidal._1640 import CycloidalDiscDesignExporter
    from mastapy._private.cycloidal._1641 import CycloidalDiscMaterial
    from mastapy._private.cycloidal._1642 import CycloidalDiscMaterialDatabase
    from mastapy._private.cycloidal._1643 import CycloidalDiscModificationsSpecification
    from mastapy._private.cycloidal._1644 import DirectionOfMeasuredModifications
    from mastapy._private.cycloidal._1645 import GeometryToExport
    from mastapy._private.cycloidal._1646 import NamedDiscPhase
    from mastapy._private.cycloidal._1647 import RingPinsDesign
    from mastapy._private.cycloidal._1648 import RingPinsMaterial
    from mastapy._private.cycloidal._1649 import RingPinsMaterialDatabase
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.cycloidal._1636": ["ContactSpecification"],
        "_private.cycloidal._1637": ["CrowningSpecificationMethod"],
        "_private.cycloidal._1638": ["CycloidalAssemblyDesign"],
        "_private.cycloidal._1639": ["CycloidalDiscDesign"],
        "_private.cycloidal._1640": ["CycloidalDiscDesignExporter"],
        "_private.cycloidal._1641": ["CycloidalDiscMaterial"],
        "_private.cycloidal._1642": ["CycloidalDiscMaterialDatabase"],
        "_private.cycloidal._1643": ["CycloidalDiscModificationsSpecification"],
        "_private.cycloidal._1644": ["DirectionOfMeasuredModifications"],
        "_private.cycloidal._1645": ["GeometryToExport"],
        "_private.cycloidal._1646": ["NamedDiscPhase"],
        "_private.cycloidal._1647": ["RingPinsDesign"],
        "_private.cycloidal._1648": ["RingPinsMaterial"],
        "_private.cycloidal._1649": ["RingPinsMaterialDatabase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ContactSpecification",
    "CrowningSpecificationMethod",
    "CycloidalAssemblyDesign",
    "CycloidalDiscDesign",
    "CycloidalDiscDesignExporter",
    "CycloidalDiscMaterial",
    "CycloidalDiscMaterialDatabase",
    "CycloidalDiscModificationsSpecification",
    "DirectionOfMeasuredModifications",
    "GeometryToExport",
    "NamedDiscPhase",
    "RingPinsDesign",
    "RingPinsMaterial",
    "RingPinsMaterialDatabase",
)
