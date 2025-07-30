"""This module holds utility classes and methods to be used internally by mastapy.

These should not be accessed by package users.
"""

from __future__ import annotations

import contextlib
import inspect
import re
from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from re import Pattern
    from typing import Any, Type, TypeVar

    Self_StrEnum = TypeVar("Self_StrEnum", "StrEnum")

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        """Polyfill for Python 3.11+ StrEnum."""

        def __str__(self: "Self_StrEnum") -> str:
            """Override of the str magic method.

            Returns:
                str
            """
            return str(self.value)


class Setter:
    """Decorator class for setter-only properties.

    By using this instead of @property and @func.setter for setter-only properties,
    we remove some minor overheads.

    Args:
        func: the function to be decorated.
        doc (str, optional): documentation for the setter.


    Attributes:
        func: the decorated function.
    """

    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__

    def __set__(self, obj, value):
        """Override of the set magic method."""
        return self.func(obj, value)


__SYSTEM_DRAWING_COMMON = {
    "FxResources.System.Drawing.Common.SR",
    "System.LocalAppContextSwitches",
    "System.SR",
    "System.Drawing.Bitmap",
    "System.Drawing.BitmapSelector",
    "System.Drawing.BitmapSuffixInSameAssemblyAttribute",
    "System.Drawing.BitmapSuffixInSatelliteAssemblyAttribute",
    "System.Drawing.Brush",
    "System.Drawing.Brushes",
    "System.Drawing.BufferedGraphics",
    "System.Drawing.BufferedGraphicsContext",
    "System.Drawing.BufferedGraphicsManager",
    "System.Drawing.CharacterRange",
    "System.Drawing.ClientUtils",
    "System.Drawing.ContentAlignment",
    "System.Drawing.CopyPixelOperation",
    "System.Drawing.DrawingCom",
    "System.Drawing.Font",
    "System.Drawing.FontConverter",
    "System.Drawing.FontFamily",
    "System.Drawing.FontStyle",
    "System.Drawing.Graphics",
    "System.Drawing.GraphicsContext",
    "System.Drawing.GraphicsUnit",
    "System.Drawing.Icon",
    "System.Drawing.IconConverter",
    "System.Drawing.IDeviceContext",
    "System.Drawing.Image",
    "System.Drawing.ImageAnimator",
    "System.Drawing.ImageConverter",
    "System.Drawing.ImageFormatConverter",
    "System.Drawing.ImageType",
    "System.Drawing.NativeMethods",
    "System.Drawing.NumericsExtensions",
    "System.Drawing.Pen",
    "System.Drawing.Pens",
    "System.Drawing.PrintPreviewGraphics",
    "System.Drawing.Region",
    "System.Drawing.RotateFlipType",
    "System.Drawing.SafeNativeMethods",
    "System.Drawing.ScreenDC",
    "System.Drawing.SolidBrush",
    "System.Drawing.SRDescriptionAttribute",
    "System.Drawing.StockIconId",
    "System.Drawing.StockIconOptions",
    "System.Drawing.StringAlignment",
    "System.Drawing.StringDigitSubstitute",
    "System.Drawing.StringFormat",
    "System.Drawing.StringFormatFlags",
    "System.Drawing.StringTrimming",
    "System.Drawing.StringUnit",
    "System.Drawing.SystemBrushes",
    "System.Drawing.SystemFonts",
    "System.Drawing.SystemIcons",
    "System.Drawing.SystemPens",
    "System.Drawing.TextureBrush",
    "System.Drawing.ToolboxBitmapAttribute",
    "System.Drawing.Design.CategoryNameCollection",
    "System.Drawing.Drawing2D.AdjustableArrowCap",
    "System.Drawing.Drawing2D.Blend",
    "System.Drawing.Drawing2D.BrushType",
    "System.Drawing.Drawing2D.ColorBlend",
    "System.Drawing.Drawing2D.CombineMode",
    "System.Drawing.Drawing2D.CompositingMode",
    "System.Drawing.Drawing2D.CompositingQuality",
    "System.Drawing.Drawing2D.CoordinateSpace",
    "System.Drawing.Drawing2D.CustomLineCap",
    "System.Drawing.Drawing2D.CustomLineCapType",
    "System.Drawing.Drawing2D.DashCap",
    "System.Drawing.Drawing2D.DashStyle",
    "System.Drawing.Drawing2D.FillMode",
    "System.Drawing.Drawing2D.FlushIntention",
    "System.Drawing.Drawing2D.GraphicsContainer",
    "System.Drawing.Drawing2D.GraphicsPath",
    "System.Drawing.Drawing2D.GraphicsPathIterator",
    "System.Drawing.Drawing2D.GraphicsState",
    "System.Drawing.Drawing2D.HatchBrush",
    "System.Drawing.Drawing2D.HatchStyle",
    "System.Drawing.Drawing2D.InterpolationMode",
    "System.Drawing.Drawing2D.LinearGradientBrush",
    "System.Drawing.Drawing2D.LinearGradientMode",
    "System.Drawing.Drawing2D.LineCap",
    "System.Drawing.Drawing2D.LineJoin",
    "System.Drawing.Drawing2D.Matrix",
    "System.Drawing.Drawing2D.MatrixOrder",
    "System.Drawing.Drawing2D.PathData",
    "System.Drawing.Drawing2D.PathGradientBrush",
    "System.Drawing.Drawing2D.PathPointType",
    "System.Drawing.Drawing2D.PenAlignment",
    "System.Drawing.Drawing2D.PenType",
    "System.Drawing.Drawing2D.PixelOffsetMode",
    "System.Drawing.Drawing2D.QualityMode",
    "System.Drawing.Drawing2D.RegionData",
    "System.Drawing.Drawing2D.SafeCustomLineCapHandle",
    "System.Drawing.Drawing2D.SmoothingMode",
    "System.Drawing.Drawing2D.WarpMode",
    "System.Drawing.Drawing2D.WrapMode",
    "System.Drawing.Imaging.BitmapData",
    "System.Drawing.Imaging.CachedBitmap",
    "System.Drawing.Imaging.ColorAdjustType",
    "System.Drawing.Imaging.ColorChannelFlag",
    "System.Drawing.Imaging.ColorMap",
    "System.Drawing.Imaging.ColorMapType",
    "System.Drawing.Imaging.ColorMatrix",
    "System.Drawing.Imaging.ColorMatrixFlag",
    "System.Drawing.Imaging.ColorMode",
    "System.Drawing.Imaging.ColorPalette",
    "System.Drawing.Imaging.EmfPlusFlags",
    "System.Drawing.Imaging.EmfPlusRecordType",
    "System.Drawing.Imaging.EmfType",
    "System.Drawing.Imaging.Encoder",
    "System.Drawing.Imaging.EncoderParameter",
    "System.Drawing.Imaging.EncoderParameterNative",
    "System.Drawing.Imaging.EncoderParameters",
    "System.Drawing.Imaging.EncoderParametersNative",
    "System.Drawing.Imaging.EncoderParameterValueType",
    "System.Drawing.Imaging.EncoderValue",
    "System.Drawing.Imaging.FrameDimension",
    "System.Drawing.Imaging.ImageAttributes",
    "System.Drawing.Imaging.ImageCodecFlags",
    "System.Drawing.Imaging.ImageCodecInfo",
    "System.Drawing.Imaging.ImageCodecInfoPrivate",
    "System.Drawing.Imaging.ImageFlags",
    "System.Drawing.Imaging.ImageFormat",
    "System.Drawing.Imaging.ImageLockMode",
    "System.Drawing.Imaging.Metafile",
    "System.Drawing.Imaging.MetafileFrameUnit",
    "System.Drawing.Imaging.MetafileHeader",
    "System.Drawing.Imaging.MetafileHeaderEmf",
    "System.Drawing.Imaging.MetafileHeaderWmf",
    "System.Drawing.Imaging.MetafileType",
    "System.Drawing.Imaging.MetaHeader",
    "System.Drawing.Imaging.PaletteFlags",
    "System.Drawing.Imaging.PixelFormat",
    "System.Drawing.Imaging.PlayRecordCallback",
    "System.Drawing.Imaging.PropertyItem",
    "System.Drawing.Imaging.PropertyItemInternal",
    "System.Drawing.Imaging.WmfMetaHeader",
    "System.Drawing.Imaging.WmfPlaceableFileHeader",
    "System.Drawing.Internal.ApplyGraphicsProperties",
    "System.Drawing.Internal.DbgUtil",
    "System.Drawing.Internal.DeviceContext",
    "System.Drawing.Internal.DeviceContexts",
    "System.Drawing.Internal.DeviceContextType",
    "System.Drawing.Internal.GpPathData",
    "System.Drawing.Internal.GPStream",
    "System.Drawing.Internal.ISystemColorTracker",
    "System.Drawing.Internal.SystemColorTracker",
    "System.Drawing.Internal.WindowsGraphics",
    "System.Drawing.Internal.WindowsRegion",
    "System.Drawing.Interop.LOGFONT",
    "System.Drawing.Printing.Duplex",
    "System.Drawing.Printing.InvalidPrinterException",
    "System.Drawing.Printing.Margins",
    "System.Drawing.Printing.MarginsConverter",
    "System.Drawing.Printing.ModeField",
    "System.Drawing.Printing.PageSettings",
    "System.Drawing.Printing.PaperKind",
    "System.Drawing.Printing.PaperSize",
    "System.Drawing.Printing.PaperSource",
    "System.Drawing.Printing.PaperSourceKind",
    "System.Drawing.Printing.PreviewPageInfo",
    "System.Drawing.Printing.PreviewPrintController",
    "System.Drawing.Printing.PrintAction",
    "System.Drawing.Printing.PrintController",
    "System.Drawing.Printing.PrintDocument",
    "System.Drawing.Printing.PrinterResolution",
    "System.Drawing.Printing.PrinterResolutionKind",
    "System.Drawing.Printing.PrinterSettings",
    "System.Drawing.Printing.PrinterUnit",
    "System.Drawing.Printing.PrinterUnitConvert",
    "System.Drawing.Printing.PrintEventArgs",
    "System.Drawing.Printing.PrintEventHandler",
    "System.Drawing.Printing.PrintPageEventArgs",
    "System.Drawing.Printing.PrintPageEventHandler",
    "System.Drawing.Printing.PrintRange",
    "System.Drawing.Printing.QueryPageSettingsEventArgs",
    "System.Drawing.Printing.QueryPageSettingsEventHandler",
    "System.Drawing.Printing.StandardPrintController",
    "System.Drawing.Printing.TriState",
    "System.Drawing.Text.FontCollection",
    "System.Drawing.Text.GenericFontFamilies",
    "System.Drawing.Text.HotkeyPrefix",
    "System.Drawing.Text.InstalledFontCollection",
    "System.Drawing.Text.PrivateFontCollection",
    "System.Drawing.Text.TextRenderingHint",
    "System.Runtime.InteropServices.Marshalling.HandleRefMarshaller",
    "System.Text.ValueStringBuilder",
    "System.Windows.Forms.DpiHelper",
}


def is_system_drawing_common_module(module_name: str) -> bool:
    """Check whether the module is part of System.Drawing.Common.

    Args:
        module_name (str): Module to check.

    Returns:
        bool
    """
    return module_name in __SYSTEM_DRAWING_COMMON


def qualname(input: "Any") -> str:
    """Safely get the qualified name of an object.

    Args:
        input (Any): Object.

    Returns:
        str
    """

    with contextlib.suppress(AttributeError):
        return input.__qualname__

    with contextlib.suppress(AttributeError):
        return input.__name__

    return str(input)


@lru_cache(maxsize=None)
def _get_snake_case_regex() -> "Pattern[str]":
    return re.compile(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))")


def snake(input: str) -> str:
    """Convert a string to snake case.

    Args:
        input (str): Input string to convert.

    Returns:
        str
    """
    reg = _get_snake_case_regex()
    return reg.sub(r"_\1", input).lower()


def camel_spaced(input: str) -> str:
    """Convert a string to spaced camel case.

    Args:
        input (str): Input string to convert.

    Returns:
        str
    """
    return " ".join(x.capitalize() for x in input.replace(" ", "_").split("_"))


def camel(input: str) -> str:
    """Convert a string to camel case.

    Args:
        input (str): Input string to convert.

    Returns:
        str
    """
    return "".join(x.capitalize() for x in input.replace(" ", "_").split("_"))


def camel_lower(input: str) -> str:
    """Convert a string to lower camel case.

    Args:
        input (str): Input string to convert.

    Returns:
        str
    """
    result = camel(input)
    return result[0].lower() + result[1:]


@lru_cache(maxsize=None)
def _get_punctuation_table():
    import string

    return str.maketrans(dict.fromkeys(string.punctuation))


def strip_punctuation(input: str) -> str:
    """Strip punctuation from a string.

    Args:
        input (str): Input string to strip of punctuation.

    Returns:
        str
    """
    return input.translate(_get_punctuation_table())


__issubclass = issubclass


def issubclass(value: "Any", type_: "Type[Any]") -> bool:
    """Check if a value is a subclass of another type.

    This differs to the built in issubclass method by first confirming
    whether the value is even a class.

    Args:
        value (Any): Value to check.
        type_ (Type[Any]): Type to compare against.

    Returns:
        bool
    """
    return inspect.isclass(value) and __issubclass(value, type_)
