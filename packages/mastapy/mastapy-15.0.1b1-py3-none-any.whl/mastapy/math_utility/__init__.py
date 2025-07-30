"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility._1674 import AcousticWeighting
    from mastapy._private.math_utility._1675 import AlignmentAxis
    from mastapy._private.math_utility._1676 import Axis
    from mastapy._private.math_utility._1677 import CirclesOnAxis
    from mastapy._private.math_utility._1678 import ComplexMatrix
    from mastapy._private.math_utility._1679 import ComplexPartDisplayOption
    from mastapy._private.math_utility._1680 import ComplexVector
    from mastapy._private.math_utility._1681 import ComplexVector3D
    from mastapy._private.math_utility._1682 import ComplexVector6D
    from mastapy._private.math_utility._1683 import CoordinateSystem3D
    from mastapy._private.math_utility._1684 import CoordinateSystemEditor
    from mastapy._private.math_utility._1685 import CoordinateSystemForRotation
    from mastapy._private.math_utility._1686 import CoordinateSystemForRotationOrigin
    from mastapy._private.math_utility._1687 import DataPrecision
    from mastapy._private.math_utility._1688 import DegreeOfFreedom
    from mastapy._private.math_utility._1689 import DynamicsResponseScalarResult
    from mastapy._private.math_utility._1690 import DynamicsResponseScaling
    from mastapy._private.math_utility._1691 import Eigenmode
    from mastapy._private.math_utility._1692 import Eigenmodes
    from mastapy._private.math_utility._1693 import EulerParameters
    from mastapy._private.math_utility._1694 import ExtrapolationOptions
    from mastapy._private.math_utility._1695 import FacetedBody
    from mastapy._private.math_utility._1696 import FacetedSurface
    from mastapy._private.math_utility._1697 import FourierSeries
    from mastapy._private.math_utility._1698 import GenericMatrix
    from mastapy._private.math_utility._1699 import GriddedSurface
    from mastapy._private.math_utility._1700 import HarmonicValue
    from mastapy._private.math_utility._1701 import InertiaTensor
    from mastapy._private.math_utility._1702 import MassProperties
    from mastapy._private.math_utility._1703 import MaxMinMean
    from mastapy._private.math_utility._1704 import ComplexMagnitudeMethod
    from mastapy._private.math_utility._1705 import MultipleFourierSeriesInterpolator
    from mastapy._private.math_utility._1706 import Named2DLocation
    from mastapy._private.math_utility._1707 import PIDControlUpdateMethod
    from mastapy._private.math_utility._1708 import Quaternion
    from mastapy._private.math_utility._1709 import RealMatrix
    from mastapy._private.math_utility._1710 import RealVector
    from mastapy._private.math_utility._1711 import ResultOptionsFor3DVector
    from mastapy._private.math_utility._1712 import RotationAxis
    from mastapy._private.math_utility._1713 import RoundedOrder
    from mastapy._private.math_utility._1714 import SinCurve
    from mastapy._private.math_utility._1715 import SquareMatrix
    from mastapy._private.math_utility._1716 import StressPoint
    from mastapy._private.math_utility._1717 import TranslationRotation
    from mastapy._private.math_utility._1718 import Vector2DListAccessor
    from mastapy._private.math_utility._1719 import Vector6D
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility._1674": ["AcousticWeighting"],
        "_private.math_utility._1675": ["AlignmentAxis"],
        "_private.math_utility._1676": ["Axis"],
        "_private.math_utility._1677": ["CirclesOnAxis"],
        "_private.math_utility._1678": ["ComplexMatrix"],
        "_private.math_utility._1679": ["ComplexPartDisplayOption"],
        "_private.math_utility._1680": ["ComplexVector"],
        "_private.math_utility._1681": ["ComplexVector3D"],
        "_private.math_utility._1682": ["ComplexVector6D"],
        "_private.math_utility._1683": ["CoordinateSystem3D"],
        "_private.math_utility._1684": ["CoordinateSystemEditor"],
        "_private.math_utility._1685": ["CoordinateSystemForRotation"],
        "_private.math_utility._1686": ["CoordinateSystemForRotationOrigin"],
        "_private.math_utility._1687": ["DataPrecision"],
        "_private.math_utility._1688": ["DegreeOfFreedom"],
        "_private.math_utility._1689": ["DynamicsResponseScalarResult"],
        "_private.math_utility._1690": ["DynamicsResponseScaling"],
        "_private.math_utility._1691": ["Eigenmode"],
        "_private.math_utility._1692": ["Eigenmodes"],
        "_private.math_utility._1693": ["EulerParameters"],
        "_private.math_utility._1694": ["ExtrapolationOptions"],
        "_private.math_utility._1695": ["FacetedBody"],
        "_private.math_utility._1696": ["FacetedSurface"],
        "_private.math_utility._1697": ["FourierSeries"],
        "_private.math_utility._1698": ["GenericMatrix"],
        "_private.math_utility._1699": ["GriddedSurface"],
        "_private.math_utility._1700": ["HarmonicValue"],
        "_private.math_utility._1701": ["InertiaTensor"],
        "_private.math_utility._1702": ["MassProperties"],
        "_private.math_utility._1703": ["MaxMinMean"],
        "_private.math_utility._1704": ["ComplexMagnitudeMethod"],
        "_private.math_utility._1705": ["MultipleFourierSeriesInterpolator"],
        "_private.math_utility._1706": ["Named2DLocation"],
        "_private.math_utility._1707": ["PIDControlUpdateMethod"],
        "_private.math_utility._1708": ["Quaternion"],
        "_private.math_utility._1709": ["RealMatrix"],
        "_private.math_utility._1710": ["RealVector"],
        "_private.math_utility._1711": ["ResultOptionsFor3DVector"],
        "_private.math_utility._1712": ["RotationAxis"],
        "_private.math_utility._1713": ["RoundedOrder"],
        "_private.math_utility._1714": ["SinCurve"],
        "_private.math_utility._1715": ["SquareMatrix"],
        "_private.math_utility._1716": ["StressPoint"],
        "_private.math_utility._1717": ["TranslationRotation"],
        "_private.math_utility._1718": ["Vector2DListAccessor"],
        "_private.math_utility._1719": ["Vector6D"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AcousticWeighting",
    "AlignmentAxis",
    "Axis",
    "CirclesOnAxis",
    "ComplexMatrix",
    "ComplexPartDisplayOption",
    "ComplexVector",
    "ComplexVector3D",
    "ComplexVector6D",
    "CoordinateSystem3D",
    "CoordinateSystemEditor",
    "CoordinateSystemForRotation",
    "CoordinateSystemForRotationOrigin",
    "DataPrecision",
    "DegreeOfFreedom",
    "DynamicsResponseScalarResult",
    "DynamicsResponseScaling",
    "Eigenmode",
    "Eigenmodes",
    "EulerParameters",
    "ExtrapolationOptions",
    "FacetedBody",
    "FacetedSurface",
    "FourierSeries",
    "GenericMatrix",
    "GriddedSurface",
    "HarmonicValue",
    "InertiaTensor",
    "MassProperties",
    "MaxMinMean",
    "ComplexMagnitudeMethod",
    "MultipleFourierSeriesInterpolator",
    "Named2DLocation",
    "PIDControlUpdateMethod",
    "Quaternion",
    "RealMatrix",
    "RealVector",
    "ResultOptionsFor3DVector",
    "RotationAxis",
    "RoundedOrder",
    "SinCurve",
    "SquareMatrix",
    "StressPoint",
    "TranslationRotation",
    "Vector2DListAccessor",
    "Vector6D",
)
