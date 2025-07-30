"""conversion.

This module is for converting between Pythonnet representations and mastapy
representations. Should only be used internally.
"""

from __future__ import annotations

from collections import OrderedDict
from datetime import datetime
from io import BytesIO
from typing import TYPE_CHECKING

from numpy import ndarray
from packaging.version import Version

if TYPE_CHECKING:
    from enum import Enum
    from typing import (
        Any,
        Callable,
        Dict,
        Iterable,
        List,
        Optional,
        Sequence,
        Tuple,
        Type,
        Union,
    )

    from mastapy import APIBase
    from mastapy._private._internal.mixins import ListWithSelectedItemMixin

from PIL import Image

from mastapy._private._internal import constructor, core
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import python_net_import
from mastapy._private._internal.tuple_with_name import TupleWithName
from mastapy._private._math.color import Color
from mastapy._private._math.matrix_4x4 import Matrix4x4
from mastapy._private._math.vector_2d import Vector2D
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private._math.vector_4d import Vector4D

_SYSTEM = python_net_import("System")
_IO = python_net_import("System.IO")
_IMAGE = python_net_import("System.Drawing.Image")
_COLOR = python_net_import("System.Drawing", "Color")
_LIST = python_net_import("System.Collections.Generic", "List")
_DICTIONARY = python_net_import("System.Collections.Generic", "Dictionary")
_VECTOR2D = python_net_import("SMT.MastaAPI.MathUtility", "Vector2D")
_VECTOR3D = python_net_import("SMT.MastaAPI.MathUtility", "Vector3D")
_COMPLEX = python_net_import("System.Numerics", "Complex")
_SMT_BITMAP = python_net_import("SMT.MastaAPIUtility.Scripting", "SMTBitmap")
_SMT_LWSI = python_net_import("SMT.MastaAPI.Utility.Property", "ListWithSelectedItem")
_SMT_RANGE = python_net_import("SMT.MastaAPI.MathUtility", "Range")
_SMT_INTEGER_RANGE = python_net_import("SMT.MastaAPI.Utility", "IntegerRange")


class ConversionException(Exception):
    """Exception raised when conversion fails."""


def pn_to_mp_objects_in_iterable(iterable_of_objects: "Iterable[Any]", wrapper=None):
    """Wrap up all Pythonnet objects returned in an iterable in mastapy types.

    Args:
        iterable_of_objects: Iterable of Pythonnet objects
        wrapper: the wrapping mastapy type

    Returns:
        Iterable[wrapper]
    """
    if wrapper is None:

        def create_object(x, type_):
            if type_ is None:
                return x

            evaluated_type = type_()
            return constructor.new(evaluated_type.Namespace, evaluated_type.Name)(x)

        types = ((x, getattr(x, "GetType", None)) for x in iterable_of_objects)
        return (create_object(x, type_) for x, type_ in types)
    elif wrapper in (Vector2D, Vector3D, Vector4D):
        return (wrapper.wrap(x) for x in iterable_of_objects)
    else:
        return iter(map(wrapper, iterable_of_objects))


def pn_to_mp_objects_in_list(list_of_objects: "List[Any]", wrapper=None):
    """Wrap up all Pythonnet objects returned in a list in mastapy types.

    Args:
        list_of_objects: List of Pythonnet objects
        wrapper: the wrapping mastapy type

    Returns:
        List[wrapper]
    """
    if wrapper:
        return list(pn_to_mp_objects_in_iterable(list_of_objects, wrapper))
    else:
        return list(pn_to_mp_objects_in_iterable(list_of_objects))


def pn_to_mp_objects_in_iterable_of_iterables(
    iterable_of_objects: "Iterable[Any]", wrapper=None
):
    """Wrap up all Pythonnet objects returned in an iterable of iterables.

    Args:
        iterable_of_objects: Iterable of iterables of Pythonnet objects
        wrapper: the wrapping mastapy type

    Returns:
        Iterable[Iterable[wrapper]]
    """
    for iterable in iterable_of_objects:
        if wrapper:
            yield from pn_to_mp_objects_in_iterable(iterable, wrapper)
        else:
            yield from pn_to_mp_objects_in_iterable(iterable)


def pn_to_mp_objects_in_list_of_lists(list_of_objects: "List[Any]", wrapper=None):
    """Wrap up all Pythonnet objects returned in a list of lists.

    Args:
        list_of_objects: List of lists of Pythonnet objects
        wrapper: the wrapping mastapy type

    Returns:
        List[List[wrapper]]
    """
    if wrapper:
        return [pn_to_mp_objects_in_list(x, wrapper) for x in list_of_objects]
    else:
        return [pn_to_mp_objects_in_list(x) for x in list_of_objects]


def mp_to_pn_objects_in_list(list_of_objects: "List[Any]") -> "List[Any]":
    """Unwrap all mastapy objects to a list of pythonnet objects.

    Args:
        list_of_objects: List of mastapy objects

    Returns:
        List[x._TYPE]
    """
    return [x.wrapped for x in list_of_objects]


def mp_to_pn_objects_in_dotnet_list(list_of_objects: "List[Any]") -> "Any":
    """Convert a list of mastapy/python objects to a .NET list

    Args:
        list_of_objects: List of mastapy objects

    Returns:
        _LIST[x._TYPE]
    """
    if not any(list_of_objects):
        return []

    list_of_objects = list(list_of_objects)
    first_object = list_of_objects[0]
    api_object = getattr(first_object, "wrapped", None)

    conversion_method: "Optional[Callable]" = None

    if api_object is None:
        if isinstance(first_object, int):
            dotnet_type = _SYSTEM.Int32
        elif isinstance(first_object, float):
            dotnet_type = _SYSTEM.Double
        elif isinstance(first_object, complex):
            dotnet_type = _COMPLEX
            conversion_method = mp_to_pn_complex
        elif isinstance(first_object, str):
            dotnet_type = _SYSTEM.String
        elif isinstance(first_object, bool):
            dotnet_type = _SYSTEM.Boolean
        else:
            message = f"Cannot convert type {type(first_object)} to a .NET type."
            raise Exception(message) from None

        new_list = _LIST[dotnet_type]()
    else:
        new_list = _LIST[type(api_object)]()

    for obj in list_of_objects:
        converted_value = getattr(obj, "wrapped", obj)

        if conversion_method is not None:
            converted_value = conversion_method(converted_value)

        new_list.Add(converted_value)

    return new_list


def pn_to_mp_complex(pn_complex: "Any") -> complex:
    """Convert Masta API complex types to Python complex types.

    Args:
        pn_complex: Masta API complex object

    Returns:
        complex
    """
    return complex(pn_complex.Real, pn_complex.Imaginary)


def mp_to_pn_complex(mp_complex: complex) -> "Any":
    """Convert python complex types to Masta API complex types.

    Args:
        mp_complex: Python complex object

    Returns:
        .NET Complex
    """
    return _COMPLEX(mp_complex.real, mp_complex.imag)


def pn_to_mp_complex_list(pn_complex_list: "Any") -> "List[complex]":
    """Convert Masta API complex types in a list to Python complex types in a list.

    Args:
        pn_complex: List of Masta API complex objects

    Returns:
        List[complex]
    """
    return [pn_to_mp_complex(x) for x in pn_complex_list]


def pn_to_mp_enum(pn_enum: "Any", enum_type: "Type") -> int:
    """Convert .NET enum to int.

    Args:
        pn_enum: .NET enum
        enum_type: Type of the enum to wrap the int in

    Returns:
        int
    """
    if core.using_pythonnet3():
        if isinstance(enum_type, str):
            namespace, _, name = enum_type.rpartition(".")
            enum_type = constructor.new(namespace, name)

        return enum_type(int(pn_enum))
    else:
        return int(pn_enum)


def mp_to_pn_enum(mp_enum: "Enum", enum_type: "Type") -> "Any":
    """Convert Python enum to .NET enum.

    Args:
        mp_enum: Python enum
        enum_type: Type of the enum to wrap the int in

    Returns:
        Enum
    """
    if core.using_pythonnet3():
        if isinstance(enum_type, str):
            namespace, _, name = enum_type.rpartition(".")
            enum_type = python_net_import(namespace, name)

        try:
            return enum_type(mp_enum.value if mp_enum else 0)
        except AttributeError:
            return enum_type(int(mp_enum))
    else:
        try:
            return mp_enum.value if mp_enum else 0
        except AttributeError:
            return int(mp_enum)


def pn_to_mp_vector2d(pn_vector2d: "Any") -> Vector2D:
    """Convert .NET Vector2D and friends to a mastapy Vector2D.

    Args:
        pn_vector2d: .NET Vector2D (or similar)

    Returns:
        Vector2D
    """
    return Vector2D.wrap(pn_vector2d)


def mp_to_pn_vector2d(mp_vector2d: "Tuple[float, ...]"):
    """Convert Python tuple to .NET Vector2D.

    Args:
        mp_vector2d: tuple

    Returns:
        .NET Vector2D
    """
    if not hasattr(mp_vector2d, "__iter__") or len(mp_vector2d) != 2:
        raise ConversionException(
            (
                "Failed to convert object to a Vector2D. "
                "Make sure that the object is iterable and contains exactly 2 "
                "components."
            )
        )

    return _VECTOR2D(mp_vector2d[0], mp_vector2d[1])


def pn_to_mp_vector3d(pn_vector3d: "Any") -> Vector3D:
    """Convert .NET Vector3D and friends to a mastapy Vector3D.

    Args:
        pn_vector3d: .NET Vector3D (or similar)

    Returns:
        Vector3D
    """
    return Vector3D.wrap(pn_vector3d)


def mp_to_pn_vector3d(mp_vector3d: "Tuple[float, ...]") -> "Any":
    """Convert. Python tuple to .NET Vector3D.

    Args:
        mp_vector3d: tuple

    Returns:
        .NET Vector3D
    """
    if not hasattr(mp_vector3d, "__iter__") or len(mp_vector3d) != 3:
        raise ConversionException(
            (
                "Failed to convert object to a Vector3D. "
                "Make sure that the object is iterable and contains exactly 3 "
                "components."
            )
        )

    return _VECTOR3D(mp_vector3d[0], mp_vector3d[1], mp_vector3d[2])


def pn_to_mp_color(pn_color: "Any") -> Color:
    """Convert .NET Color to a mastapy Color.

    Args:
        pn_color: .NET Color

    Returns:
        Color
    """
    return Color.wrap(pn_color)


def mp_to_pn_color(mp_color: "Tuple[int, ...]"):
    """Convert Python tuple to .NET Color.

    Args:
        mp_color: tuple

    Returns:
        .NET Color
    """
    num_components = len(mp_color)

    if not hasattr(mp_color, "__iter__") or num_components < 3 or num_components > 4:
        raise ConversionException(
            (
                "Failed to convert object to a Color. "
                "Make sure that the object is iterable and contains exactly 3 or 4"
                " components."
            )
        )

    if num_components < 4:
        mp_color = *mp_color, 255

    r, g, b, a = mp_color

    return _COLOR.FromArgb(a, r, g, b)


def pn_to_mp_matrix4x4(pn_matrix4x4: "Any") -> Matrix4x4:
    """Convert .NET TransformMatrix3D to a Matrix4x4.

    Args:
        pn_matrix4x4: .NET TransformMatrix3D

    Returns:
        Matrix4x4
    """
    return Matrix4x4.wrap(pn_matrix4x4)


def mp_to_pn_matrix4x4(mp_matrix4x4: Matrix4x4) -> "Any":
    """Convert Matrix4x4 to a .NET TransformMatrix3D.

    Args:
        mp_matrix4x4: Matrix4x4

    Returns:
        TransformMatrix3D
    """
    message = (
        "Can only pass in Matrix4x4 that was first obtained from "
        "Masta. You cannot pass in a Matrix4x4 you have constructed "
        "yourself."
    )

    try:
        if not mp_matrix4x4.wrapped:
            raise ConversionException(message)

        return mp_matrix4x4.wrapped
    except AttributeError:
        raise ConversionException(message)


def pn_to_mp_tuple_with_name(
    pn_tuple_with_name: "Any", conversion_methods=None
) -> TupleWithName:
    """Convert .NET NamedTuple to Python TupleWithName.

    Args:
        pn_tuple_with_name: .NET NamedTuple
        conversion_methods (optional): conversion methods for items in tuple

    Returns:
        TupleWithName
    """
    attrs = filter(
        None,
        map(lambda x: getattr(pn_tuple_with_name, "Item" + str(x), None), range(1, 8)),
    )
    converted = (
        map(lambda x: x[1](x[0]) if x[1] else x[0], zip(attrs, conversion_methods))
        if conversion_methods
        else attrs
    )
    return TupleWithName(*tuple(converted), name=pn_tuple_with_name.Name)


def pn_to_mp_datetime(pn_datetime: "Any") -> datetime:
    """Convert .NET System.DateTime struct to python datetime object.

    Args:
        pn_datetime: .NET System.DateTime struct

    Returns:
        datetime
    """
    if not pn_datetime:
        return datetime.max

    year = pn_datetime.Year
    month = pn_datetime.Month
    day = pn_datetime.Day
    hour = pn_datetime.Hour
    minute = pn_datetime.Minute
    second = pn_datetime.Second
    microsecond = pn_datetime.Millisecond * 1000

    return datetime(year, month, day, hour, minute, second, microsecond)


def pn_to_mp_image(pn_bytes: "Any") -> Image.Image:
    """Convert .NET System.Byte[] to a PIL image.

    Args:
        pn_bytes: .NET System.Byte[]

    Returns:
        Image.Image
    """
    if not pn_bytes:
        return None

    byte_data = bytes(pn_bytes)
    byte_stream = BytesIO(byte_data)
    image = Image.open(byte_stream)

    return image


def mp_to_pn_image(mp_image: Image.Image) -> "Any":
    """Convert PIL image to a .NET System.Drawing.Image.

    Args:
        mp_image (Image.Image): PIL image

    Returns:
        .NET System.Drawing.Image
    """
    if not mp_image:
        return None

    byte_stream = BytesIO()
    mp_image.save(byte_stream, format=mp_image.format)
    byte_data = byte_stream.getvalue()

    memory_stream = _IO.MemoryStream(byte_data)
    return _IMAGE.FromStream(memory_stream)


def pn_to_mp_smt_bitmap(pn_image: "Any") -> Image.Image:
    """Convert .NET SMTBitmap to a PIL image.

    Args:
        pn_image: .NET SMTBitmap

    Returns:
        Image.Image
    """
    if not pn_image:
        return None

    return pn_to_mp_image(pn_image.ToBytes())


def mp_to_pn_smt_bitmap(mp_image: Image.Image) -> "Any":
    """Convert PIL image to a .NET SMTBitmap.

    Args:
        mp_image (Image.Image): PIL image

    Returns:
        .NET SMTBitmap
    """
    if not mp_image:
        return None

    return _SMT_BITMAP(mp_to_pn_image(mp_image))


def mp_to_pn_smt_list_with_selected_item(
    api_object: "APIBase",
    mp_lwsi: "ListWithSelectedItemMixin",
    generic_type: "Optional[Type]" = None,
) -> "Any":
    """Convert a mastapy ListWithSelectedItem to a .NET ListWithSelectedItem.

    Args:
        api_object (APIBase): API object necessary to convert the LWSI.
        mp_lwsi (ListWithSelectedItemMixin): List with selected item.
        generic_type (Type | None, optional): Generic type of the API object. Default
            is derived from mp_lwsi.

    Returns:
        .NET ListWithSelectedItem
    """
    from mastapy._private._internal.sentinels import ListWithSelectedItem_None

    if mp_lwsi is None or isinstance(mp_lwsi, ListWithSelectedItem_None):
        return None

    value = getattr(mp_lwsi.selected_value, "wrapped", mp_lwsi.selected_value)
    items = mp_to_pn_objects_in_dotnet_list(mp_lwsi.available_values)

    if generic_type is None:
        generic_type = type(value)

    return api_object.wrapped.ToListWithSelectedItem[generic_type](value, items)


def pn_to_mp_smt_list_with_selected_item(pn_lwsi: "Any") -> "ListWithSelectedItemMixin":
    if pn_lwsi is None:
        return None

    value = pn_lwsi.SelectedValue
    items = pn_to_mp_objects_in_list(pn_lwsi.AvailableValues)

    return promote_to_list_with_selected_item(value, items)


def pn_to_mp_version(pn_version: "Any") -> Version:
    """Convert .NET Version to Python Version.

    Args:
        pn_version: .NET Version

    Returns:
        packaging.version.Version
    """
    if not pn_version:
        return None

    return Version(pn_version.ToString())


def mp_to_pn_version(mp_version: Version) -> "Any":
    """Convert Python Version to .NET Version.

    Args:
        mp_version: Python Version

    Returns:
        System.Version
    """
    if not mp_version:
        return None

    return _SYSTEM.Version(str(mp_version))


def pn_to_mp_dict(pn_dict: "Any") -> "Dict[Any, Any]":
    """Convert a .NET dictionary to a python dictionary.

    Note:
        We assume that the key is a basic Python type.

    Args:
        pn_dict : .NET dictionary

    Returns:
        Dict[TKey, TValue]
    """
    if not pn_dict:
        return dict()

    return {kvp.Key: kvp.Value for kvp in pn_dict}


def mp_to_pn_dict_float(mp_dict: "Dict[str, float]") -> "Any":
    """Convert a python dictionary to a .NET dictionary.

    Args:
        mp_dict : python dictionary

    Returns:
        .NET dictionary
    """
    if not isinstance(mp_dict, dict):
        raise ConversionException(
            "Invalid argument provided. Argument must be a dictionary."
        )

    new_dict = _DICTIONARY[_SYSTEM.String, _SYSTEM.Double]()
    for key, value in mp_dict.items():
        if not isinstance(key, str):
            raise ConversionException(
                "Invalid argument provided. Dictionary keys must be str."
            )

        if not isinstance(value, float):
            raise ConversionException(
                "Invalid argument provided. Dictionary values must be float."
            )

        new_dict.Add(key, value)
    return new_dict


def pn_to_mp_objects_in_list_in_ordered_dict(
    dict_of_objects: "Any", wrapper=None
) -> OrderedDict:
    """Wrap up all Pythonnet objects returned in a list in a dictionary.

    Note:
        We assume that the key is a basic Python type.

    Args:
        dict_of_objects: Dictionary of lists of objects.
            e.g. {float : [PYTHON_NET_OBJECT, ...], ...}
        wrapper: the wrapping mastapy type

    Returns:
        OrderedDict[TKey, List[wrapper]]
    """
    if wrapper:
        return OrderedDict(
            (kv.Key, [wrapper(obj) for obj in kv.Value]) for kv in dict_of_objects
        )
    else:
        return OrderedDict((kv.Key, kv.Value) for kv in dict_of_objects)


def pn_to_mp_objects_in_list_in_dict(
    dict_of_objects: "Any", wrapper=None
) -> "Dict[Any, Any]":
    """Wrap up all Pythonnet objects returned in a list in a dictionary.

    Note:
        We assume that the key is a basic Python type.

    Args:
        dict_of_objects: Dictionary of lists of objects.
            e.g. {float: [PYTHON_NET_OBJECT, ...], ...}
        wrapper: the wrapping mastapy type

    Returns:
        Dict[TKey, List[wrapper]]
    """
    if wrapper:
        return {kv.Key: [wrapper(obj) for obj in kv.Value] for kv in dict_of_objects}
    else:
        return {kv.Key: kv.Value for kv in dict_of_objects}


def _pn_to_mp_tuple_append(values: "List[Any]", other: "Any", attr: str) -> bool:
    try:
        values.append(getattr(other, attr))
    except AttributeError:
        return False

    return True


def pn_to_mp_tuple(pn_tuple: "Any"):
    """Convert a .NET tuple to a Python tuple.

    Args:
        pn_tuple (System.Tuple[...]): .NET tuple

    Returns:
        Tuple[...]
    """
    values = []
    i = 1

    while _pn_to_mp_tuple_append(values, pn_tuple, "Item{}".format(i)):
        i += 1

    return tuple(values)


def mp_to_pn_tuple(mp_tuple: "Tuple[Any, ...]"):
    """Convert a Python tuple to a .NET tuple.

    Args:
        mp_tuple (Tuple[Any, ...]): Python tuple

    Returns:
        System.Tuple[...]
    """
    if mp_tuple is None or not any(mp_tuple):
        raise ConversionException("Invalid argument provided. Was expecting a tuple")

    return _SYSTEM.Tuple.Create(*mp_tuple)


def pn_to_mp_bytes(pn_list: "Any") -> bytes:
    """Convert a .NET byte array to a bytes object.

    Args:
        pn_list (System.Array[System.Byte]): 1D Array of bytes

    Returns:
        bytes
    """
    return bytes([int(x) for x in pn_list])


def to_list_any(mp_list: "Iterable[Any]") -> "List[Any]":
    """Convert an iterable of anything to a list of anything.

    Args:
        mp_list (Iterable[Any]): iterable of anything

    Returns:
        List[Any]
    """
    return list(mp_list)


def mp_to_pn_array_float(mp_list: "Union[ndarray, Sequence[float]]") -> "List[float]":
    """Convert a list of floats to a 1D array.

    Args:
        mp_list (Union[ndarray, Sequence[float]]): Sequence of floats

    Returns:
        List[float]
    """
    if mp_list is None or not any(mp_list):
        return []

    if isinstance(mp_list, ndarray):
        if len(mp_list.shape) > 1:
            raise ConversionException(
                (
                    "Invalid argument provided. Argument must be a 1D array of "
                    "float values."
                )
            )

    return list(mp_list)


def mp_to_pn_list_float(
    mp_list: "Union[ndarray, Sequence[float]]",
) -> "Any":
    """Convert a list of floats to a 1D list.

    Args:
        mp_list (List[float]): List of floats

    Returns:
        System.Collections.Generic.List[System.Double]
    """
    if isinstance(mp_list, ndarray):
        if len(mp_list.shape) > 1:
            raise ConversionException(
                (
                    "Invalid argument provided. Argument must be a 1D array of "
                    "float values."
                )
            )

    new_list = _LIST[_SYSTEM.Double]()
    for x in mp_list:
        new_list.Add(x)
    return new_list


def mp_to_pn_list_string(
    mp_list: "Union[ndarray, Sequence[str]]",
):
    """Convert a list of strings to a 1D list.

    Args:
        mp_list (List[str]): List of strings

    Returns:
        System.Collections.Generic.List[System.String]
    """
    if isinstance(mp_list, ndarray):
        if len(mp_list.shape) > 1:
            raise ConversionException(
                (
                    "Invalid argument provided. Argument must be a 1D array of "
                    "string values."
                )
            )

    new_list = _LIST[_SYSTEM.String]()
    for x in mp_list:
        new_list.Add(x)
    return new_list


def pn_to_mp_list_float_2d(
    pn_list: "Any",
) -> "List[List[float]]":
    """Convert a 2D Array of Doubles to a list of lists of floats.

    Args:
        pn_list (System.Array[System.Double]): 2D Array

    Returns:
        List[List[float]]
    """
    length0 = pn_list.GetLength(0)
    length1 = pn_list.GetLength(1)

    return [[pn_list.GetValue(y, x) for x in range(length1)] for y in range(length0)]


def mp_to_pn_list_float_2d(
    mp_list: "List[List[float]]",
) -> "Any":
    """Convert a list of lists of floats to a 2D array.

    Args:
        mp_list (List[List[float]]): List of lists of floats

    Returns:
        System.Array[System.Double]: i.e. System.Double[,]
    """
    if mp_list is None or not hasattr(mp_list, "__iter__"):
        return _SYSTEM.Array.CreateInstance(_SYSTEM.Double, 0, 0)

    length0 = len(mp_list)

    if not hasattr(mp_list, "__getitem__"):
        mp_list = list(mp_list)

    if not length0:
        return _SYSTEM.Array.CreateInstance(_SYSTEM.Double, 0, 0)

    if not hasattr(mp_list[0], "__iter__"):
        raise ConversionException(
            "Invalid argument provided. Argument is not a list of lists."
        )

    length1 = len(mp_list[0])

    pn_list = _SYSTEM.Array.CreateInstance(_SYSTEM.Double, length0, length1)
    for i, y in enumerate(mp_list):
        if not hasattr(y, "__iter__") or len(y) != length1:
            raise ConversionException(
                (
                    "Invalid argument provided. Argument must be a "
                    "2d array (i.e. [[1.0, 0.0], [0.0, 1.0]])"
                )
            )
        for j, x in enumerate(y):
            pn_list.SetValue(float(x), i, j)
    return pn_list


def pn_to_mp_range(
    value: "Any",
) -> "Union[Tuple[float, float], Tuple[int, int]]":
    """Convert an API Range or IntegerRange to a tuple.

    Args:
        value (Any)

    Returns:
        Tuple[float, float] | Tuple[int, int]
    """
    return (value.Min, value.Max)


def mp_to_pn_range(
    value: "Iterable[float]",
) -> "Any":
    """Convert a tuple to an API Range.

    Args:
        value (Iterable[float])

    Returns:
        _SMT_RANGE
    """
    if value is None or not hasattr(value, "__iter__"):
        return _SMT_RANGE(0.0, 0.0)

    if len(value) != 2:
        raise ConversionException(
            "Invalid argument provided. Argument must be an iterable with exactly two "
            "values."
        ) from None

    v = tuple(value)
    return _SMT_RANGE(v[0], v[1])


def mp_to_pn_integer_range(value: "Iterable[int]") -> "Any":
    """Convert a tuple to an API IntegerRange.

    Args:
        value (Iterable[int])

    Returns:
        _SMT_INTEGER_RANGE
    """
    if value is None or not hasattr(value, "__iter__"):
        return _SMT_INTEGER_RANGE(0, 0)

    if len(value) != 2:
        raise ConversionException(
            "Invalid argument provided. Argument must be an iterable with exactly two "
            "values."
        ) from None

    v = tuple(value)
    return _SMT_INTEGER_RANGE(v[0], v[1])
