"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bolts._1650 import AxialLoadType
    from mastapy._private.bolts._1651 import BoltedJointMaterial
    from mastapy._private.bolts._1652 import BoltedJointMaterialDatabase
    from mastapy._private.bolts._1653 import BoltGeometry
    from mastapy._private.bolts._1654 import BoltGeometryDatabase
    from mastapy._private.bolts._1655 import BoltMaterial
    from mastapy._private.bolts._1656 import BoltMaterialDatabase
    from mastapy._private.bolts._1657 import BoltSection
    from mastapy._private.bolts._1658 import BoltShankType
    from mastapy._private.bolts._1659 import BoltTypes
    from mastapy._private.bolts._1660 import ClampedSection
    from mastapy._private.bolts._1661 import ClampedSectionMaterialDatabase
    from mastapy._private.bolts._1662 import DetailedBoltDesign
    from mastapy._private.bolts._1663 import DetailedBoltedJointDesign
    from mastapy._private.bolts._1664 import HeadCapTypes
    from mastapy._private.bolts._1665 import JointGeometries
    from mastapy._private.bolts._1666 import JointTypes
    from mastapy._private.bolts._1667 import LoadedBolt
    from mastapy._private.bolts._1668 import RolledBeforeOrAfterHeatTreatment
    from mastapy._private.bolts._1669 import StandardSizes
    from mastapy._private.bolts._1670 import StrengthGrades
    from mastapy._private.bolts._1671 import ThreadTypes
    from mastapy._private.bolts._1672 import TighteningTechniques
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bolts._1650": ["AxialLoadType"],
        "_private.bolts._1651": ["BoltedJointMaterial"],
        "_private.bolts._1652": ["BoltedJointMaterialDatabase"],
        "_private.bolts._1653": ["BoltGeometry"],
        "_private.bolts._1654": ["BoltGeometryDatabase"],
        "_private.bolts._1655": ["BoltMaterial"],
        "_private.bolts._1656": ["BoltMaterialDatabase"],
        "_private.bolts._1657": ["BoltSection"],
        "_private.bolts._1658": ["BoltShankType"],
        "_private.bolts._1659": ["BoltTypes"],
        "_private.bolts._1660": ["ClampedSection"],
        "_private.bolts._1661": ["ClampedSectionMaterialDatabase"],
        "_private.bolts._1662": ["DetailedBoltDesign"],
        "_private.bolts._1663": ["DetailedBoltedJointDesign"],
        "_private.bolts._1664": ["HeadCapTypes"],
        "_private.bolts._1665": ["JointGeometries"],
        "_private.bolts._1666": ["JointTypes"],
        "_private.bolts._1667": ["LoadedBolt"],
        "_private.bolts._1668": ["RolledBeforeOrAfterHeatTreatment"],
        "_private.bolts._1669": ["StandardSizes"],
        "_private.bolts._1670": ["StrengthGrades"],
        "_private.bolts._1671": ["ThreadTypes"],
        "_private.bolts._1672": ["TighteningTechniques"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AxialLoadType",
    "BoltedJointMaterial",
    "BoltedJointMaterialDatabase",
    "BoltGeometry",
    "BoltGeometryDatabase",
    "BoltMaterial",
    "BoltMaterialDatabase",
    "BoltSection",
    "BoltShankType",
    "BoltTypes",
    "ClampedSection",
    "ClampedSectionMaterialDatabase",
    "DetailedBoltDesign",
    "DetailedBoltedJointDesign",
    "HeadCapTypes",
    "JointGeometries",
    "JointTypes",
    "LoadedBolt",
    "RolledBeforeOrAfterHeatTreatment",
    "StandardSizes",
    "StrengthGrades",
    "ThreadTypes",
    "TighteningTechniques",
)
