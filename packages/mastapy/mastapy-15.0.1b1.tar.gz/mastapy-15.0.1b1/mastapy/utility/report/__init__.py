"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.report._1937 import AdHocCustomTable
    from mastapy._private.utility.report._1938 import AxisSettings
    from mastapy._private.utility.report._1939 import BlankRow
    from mastapy._private.utility.report._1940 import CadPageOrientation
    from mastapy._private.utility.report._1941 import CadPageSize
    from mastapy._private.utility.report._1942 import CadTableBorderType
    from mastapy._private.utility.report._1943 import ChartDefinition
    from mastapy._private.utility.report._1944 import SMTChartPointShape
    from mastapy._private.utility.report._1945 import CustomChart
    from mastapy._private.utility.report._1946 import CustomDrawing
    from mastapy._private.utility.report._1947 import CustomGraphic
    from mastapy._private.utility.report._1948 import CustomImage
    from mastapy._private.utility.report._1949 import CustomReport
    from mastapy._private.utility.report._1950 import CustomReportCadDrawing
    from mastapy._private.utility.report._1951 import CustomReportChart
    from mastapy._private.utility.report._1952 import CustomReportChartItem
    from mastapy._private.utility.report._1953 import CustomReportColumn
    from mastapy._private.utility.report._1954 import CustomReportColumns
    from mastapy._private.utility.report._1955 import CustomReportDefinitionItem
    from mastapy._private.utility.report._1956 import CustomReportHorizontalLine
    from mastapy._private.utility.report._1957 import CustomReportHtmlItem
    from mastapy._private.utility.report._1958 import CustomReportItem
    from mastapy._private.utility.report._1959 import CustomReportItemContainer
    from mastapy._private.utility.report._1960 import (
        CustomReportItemContainerCollection,
    )
    from mastapy._private.utility.report._1961 import (
        CustomReportItemContainerCollectionBase,
    )
    from mastapy._private.utility.report._1962 import (
        CustomReportItemContainerCollectionItem,
    )
    from mastapy._private.utility.report._1963 import CustomReportKey
    from mastapy._private.utility.report._1964 import CustomReportMultiPropertyItem
    from mastapy._private.utility.report._1965 import CustomReportMultiPropertyItemBase
    from mastapy._private.utility.report._1966 import CustomReportNameableItem
    from mastapy._private.utility.report._1967 import CustomReportNamedItem
    from mastapy._private.utility.report._1968 import CustomReportPropertyItem
    from mastapy._private.utility.report._1969 import CustomReportStatusItem
    from mastapy._private.utility.report._1970 import CustomReportTab
    from mastapy._private.utility.report._1971 import CustomReportTabs
    from mastapy._private.utility.report._1972 import CustomReportText
    from mastapy._private.utility.report._1973 import CustomRow
    from mastapy._private.utility.report._1974 import CustomSubReport
    from mastapy._private.utility.report._1975 import CustomTable
    from mastapy._private.utility.report._1976 import DefinitionBooleanCheckOptions
    from mastapy._private.utility.report._1977 import DynamicCustomReportItem
    from mastapy._private.utility.report._1978 import FontStyle
    from mastapy._private.utility.report._1979 import FontWeight
    from mastapy._private.utility.report._1980 import HeadingSize
    from mastapy._private.utility.report._1981 import SimpleChartDefinition
    from mastapy._private.utility.report._1982 import UserTextRow
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.report._1937": ["AdHocCustomTable"],
        "_private.utility.report._1938": ["AxisSettings"],
        "_private.utility.report._1939": ["BlankRow"],
        "_private.utility.report._1940": ["CadPageOrientation"],
        "_private.utility.report._1941": ["CadPageSize"],
        "_private.utility.report._1942": ["CadTableBorderType"],
        "_private.utility.report._1943": ["ChartDefinition"],
        "_private.utility.report._1944": ["SMTChartPointShape"],
        "_private.utility.report._1945": ["CustomChart"],
        "_private.utility.report._1946": ["CustomDrawing"],
        "_private.utility.report._1947": ["CustomGraphic"],
        "_private.utility.report._1948": ["CustomImage"],
        "_private.utility.report._1949": ["CustomReport"],
        "_private.utility.report._1950": ["CustomReportCadDrawing"],
        "_private.utility.report._1951": ["CustomReportChart"],
        "_private.utility.report._1952": ["CustomReportChartItem"],
        "_private.utility.report._1953": ["CustomReportColumn"],
        "_private.utility.report._1954": ["CustomReportColumns"],
        "_private.utility.report._1955": ["CustomReportDefinitionItem"],
        "_private.utility.report._1956": ["CustomReportHorizontalLine"],
        "_private.utility.report._1957": ["CustomReportHtmlItem"],
        "_private.utility.report._1958": ["CustomReportItem"],
        "_private.utility.report._1959": ["CustomReportItemContainer"],
        "_private.utility.report._1960": ["CustomReportItemContainerCollection"],
        "_private.utility.report._1961": ["CustomReportItemContainerCollectionBase"],
        "_private.utility.report._1962": ["CustomReportItemContainerCollectionItem"],
        "_private.utility.report._1963": ["CustomReportKey"],
        "_private.utility.report._1964": ["CustomReportMultiPropertyItem"],
        "_private.utility.report._1965": ["CustomReportMultiPropertyItemBase"],
        "_private.utility.report._1966": ["CustomReportNameableItem"],
        "_private.utility.report._1967": ["CustomReportNamedItem"],
        "_private.utility.report._1968": ["CustomReportPropertyItem"],
        "_private.utility.report._1969": ["CustomReportStatusItem"],
        "_private.utility.report._1970": ["CustomReportTab"],
        "_private.utility.report._1971": ["CustomReportTabs"],
        "_private.utility.report._1972": ["CustomReportText"],
        "_private.utility.report._1973": ["CustomRow"],
        "_private.utility.report._1974": ["CustomSubReport"],
        "_private.utility.report._1975": ["CustomTable"],
        "_private.utility.report._1976": ["DefinitionBooleanCheckOptions"],
        "_private.utility.report._1977": ["DynamicCustomReportItem"],
        "_private.utility.report._1978": ["FontStyle"],
        "_private.utility.report._1979": ["FontWeight"],
        "_private.utility.report._1980": ["HeadingSize"],
        "_private.utility.report._1981": ["SimpleChartDefinition"],
        "_private.utility.report._1982": ["UserTextRow"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AdHocCustomTable",
    "AxisSettings",
    "BlankRow",
    "CadPageOrientation",
    "CadPageSize",
    "CadTableBorderType",
    "ChartDefinition",
    "SMTChartPointShape",
    "CustomChart",
    "CustomDrawing",
    "CustomGraphic",
    "CustomImage",
    "CustomReport",
    "CustomReportCadDrawing",
    "CustomReportChart",
    "CustomReportChartItem",
    "CustomReportColumn",
    "CustomReportColumns",
    "CustomReportDefinitionItem",
    "CustomReportHorizontalLine",
    "CustomReportHtmlItem",
    "CustomReportItem",
    "CustomReportItemContainer",
    "CustomReportItemContainerCollection",
    "CustomReportItemContainerCollectionBase",
    "CustomReportItemContainerCollectionItem",
    "CustomReportKey",
    "CustomReportMultiPropertyItem",
    "CustomReportMultiPropertyItemBase",
    "CustomReportNameableItem",
    "CustomReportNamedItem",
    "CustomReportPropertyItem",
    "CustomReportStatusItem",
    "CustomReportTab",
    "CustomReportTabs",
    "CustomReportText",
    "CustomRow",
    "CustomSubReport",
    "CustomTable",
    "DefinitionBooleanCheckOptions",
    "DynamicCustomReportItem",
    "FontStyle",
    "FontWeight",
    "HeadingSize",
    "SimpleChartDefinition",
    "UserTextRow",
)
