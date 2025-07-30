"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility_gui.charts._2055 import BubbleChartDefinition
    from mastapy._private.utility_gui.charts._2056 import ConstantLine
    from mastapy._private.utility_gui.charts._2057 import CustomLineChart
    from mastapy._private.utility_gui.charts._2058 import CustomTableAndChart
    from mastapy._private.utility_gui.charts._2059 import LegacyChartMathChartDefinition
    from mastapy._private.utility_gui.charts._2060 import MatrixVisualisationDefinition
    from mastapy._private.utility_gui.charts._2061 import ModeConstantLine
    from mastapy._private.utility_gui.charts._2062 import NDChartDefinition
    from mastapy._private.utility_gui.charts._2063 import (
        ParallelCoordinatesChartDefinition,
    )
    from mastapy._private.utility_gui.charts._2064 import PointsForSurface
    from mastapy._private.utility_gui.charts._2065 import ScatterChartDefinition
    from mastapy._private.utility_gui.charts._2066 import Series2D
    from mastapy._private.utility_gui.charts._2067 import SMTAxis
    from mastapy._private.utility_gui.charts._2068 import ThreeDChartDefinition
    from mastapy._private.utility_gui.charts._2069 import ThreeDVectorChartDefinition
    from mastapy._private.utility_gui.charts._2070 import TwoDChartDefinition
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility_gui.charts._2055": ["BubbleChartDefinition"],
        "_private.utility_gui.charts._2056": ["ConstantLine"],
        "_private.utility_gui.charts._2057": ["CustomLineChart"],
        "_private.utility_gui.charts._2058": ["CustomTableAndChart"],
        "_private.utility_gui.charts._2059": ["LegacyChartMathChartDefinition"],
        "_private.utility_gui.charts._2060": ["MatrixVisualisationDefinition"],
        "_private.utility_gui.charts._2061": ["ModeConstantLine"],
        "_private.utility_gui.charts._2062": ["NDChartDefinition"],
        "_private.utility_gui.charts._2063": ["ParallelCoordinatesChartDefinition"],
        "_private.utility_gui.charts._2064": ["PointsForSurface"],
        "_private.utility_gui.charts._2065": ["ScatterChartDefinition"],
        "_private.utility_gui.charts._2066": ["Series2D"],
        "_private.utility_gui.charts._2067": ["SMTAxis"],
        "_private.utility_gui.charts._2068": ["ThreeDChartDefinition"],
        "_private.utility_gui.charts._2069": ["ThreeDVectorChartDefinition"],
        "_private.utility_gui.charts._2070": ["TwoDChartDefinition"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BubbleChartDefinition",
    "ConstantLine",
    "CustomLineChart",
    "CustomTableAndChart",
    "LegacyChartMathChartDefinition",
    "MatrixVisualisationDefinition",
    "ModeConstantLine",
    "NDChartDefinition",
    "ParallelCoordinatesChartDefinition",
    "PointsForSurface",
    "ScatterChartDefinition",
    "Series2D",
    "SMTAxis",
    "ThreeDChartDefinition",
    "ThreeDVectorChartDefinition",
    "TwoDChartDefinition",
)
