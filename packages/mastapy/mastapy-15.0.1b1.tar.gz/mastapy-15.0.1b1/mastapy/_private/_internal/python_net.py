"""python_net.

Utility module for importing python net modules.
"""

from __future__ import annotations

import os
import warnings
from typing import TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.exceptions import (
    AssemblyLoadError,
    UnavailableMethodError,
)

if TYPE_CHECKING:
    from typing import Any, Callable, Optional, Sequence, Type

    from mastapy._private._internal.core import EnvironmentSummary


utility_dll = None
FileNotFoundException = None
FileLoadException = None
__verify_system_drawing_common_modules = False


def initialise_python_net_importing(
    environment_summary: "EnvironmentSummary", utility_dll_path: str
) -> None:
    """Initialise the Python.NET importing.

    By providing the path to the MASTA API Utility assembly, we can ensure
    we are importing from the correct assembly.

    Args:
        environment_summary (EnvironmentSummary): Current environment.
        utility_dll_path (str): Path to the MASTA API Utility assembly.
    """
    global utility_dll, __verify_system_drawing_common_modules

    if not os.path.exists(utility_dll_path):
        raise FileNotFoundError("Failed to find the MASTA API Utility assembly.")

    utility_dll = utility_dll_path
    __verify_system_drawing_common_modules = (
        environment_summary.is_valid_linux_configuration
    )


def python_net_add_reference(path: str) -> "Any":
    """Add a reference to a .NET assembly and return the assembly.

    Args:
        path (str): Path to the assembly.

    Returns:
        Any
    """
    global FileNotFoundException, FileLoadException
    import clr

    if FileNotFoundException is None or FileLoadException is None:
        FileNotFoundException = python_net_import("System.IO", "FileNotFoundException")
        FileLoadException = python_net_import("System.IO", "FileLoadException")

    try:
        return clr.AddReference(path)
    except (FileNotFoundException, FileLoadException) as e:
        message = (
            f'Failed to load the assembly "{path}" or one of its '
            "dependencies. If you are on Windows and using a portable "
            "version of MASTA it is possible that files are being "
            "blocked. If you are distributing a portable version of "
            "MASTA locally from one computer to another, ensure that "
            "it is distributed as a single archive file (such as "
            ".zip) and unpacked on the target computer.\n\n"
            f"{e.Message}"
        )
        raise AssemblyLoadError(message) from None


def _verify_imports_can_be_resolved() -> None:
    """Verify that the import system works correctly.

    While it is unlikely, there are rare instances when assemblies can be loaded but
    importing fails. This situation produces confusing errors, so this method is
    designed to report something slightly more readable.

    We only do verification if a Python.NET import error occurs to avoid performance
    costs in working applications.
    """
    module_name = "SMT"
    module = __import__(module_name)

    if "MastaAPI" not in dir(module):
        raise ImportError(
            "Failed to load internal MastaAPI dependencies. This is likely due to a "
            'conflicting module on the path. Ensure there is no folder called "SMT" in '
            "the same directory as the script you are attempting to run."
        ) from None


def python_net_import(module: str, class_name: "Optional[str]" = None) -> "Any":
    """Dynamically import a Python.NET module.

    Args:
        module (str): Module path
        class_name (str, optional): class name

    Returns:
        Any
    """
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            path = list(filter(None, module.split(".")))
            m = __import__(path[0])

            for p in path[1:]:
                m = getattr(m, p)

            if class_name:
                m = getattr(m, class_name)
    except ImportError:
        raise ImportError(
            "Mastapy has not been initialised. You must call `mastapy.init(...)` with "
            "the path to your MASTA directory as the only argument before importing "
            "anything else."
        ) from None
    except Exception:
        _verify_imports_can_be_resolved()

        if (
            __verify_system_drawing_common_modules
            and utility.is_system_drawing_common_module(module)
        ):
            return None

        raise ImportError(f"Failed to load {class_name} from {module}.") from None

    return m


def pythonnet_method_call(
    caller: "Any",
    method_name: str,
    *args: "Any",
) -> "Any":
    """Call a Python.NET method safely.

    It is possible that a method available for the .NET Framework API is not available
    on .NET 6+. As we cannot possibly know whether someone is using one or the other,
    we can wrap Python.NET method calls and report missing methods with a useful error
    message.

    Args:
        caller (Any): Object to find the method on.
        method_name (str): Name of the Python.NET method to be called.
        *args (Any): Method arguments.

    Returns:
        Any
    """
    try:
        found_method: "Optional[Callable[..., Any]]" = getattr(caller, method_name)
        return found_method(*args)
    except AttributeError:
        snake_name = utility.snake(method_name)
        raise UnavailableMethodError(
            f'The method "{snake_name}" is not available in .NET 6+ APIs.'
        ) from None


def pythonnet_method_call_generic(
    caller: "Any",
    method_name: str,
    generic_arg: "Any",
    *args: "Any",
) -> "Any":
    """Call a Python.NET generic method safely.

    It is possible that a method available for the .NET Framework API is not available
    on .NET 6+. As we cannot possibly know whether someone is using one or the other,
    we can wrap Python.NET method calls and report missing methods with a useful error
    message.

    Args:
        caller (Any): Object to find the method on.
        method_name (str): Name of the Python.NET method to be called.
        generic_arg (Any): Generic argument.
        *args (Any): Method arguments.

    Returns:
        Any
    """
    try:
        found_method: "Optional[Callable[..., Any]]" = getattr(caller, method_name)
        return found_method[generic_arg](*args)
    except AttributeError:
        snake_name = utility.snake(method_name)
        raise UnavailableMethodError(
            f'The method "{snake_name}" is not available in .NET 6+ APIs.'
        ) from None


def pythonnet_method_call_overload(
    caller: "Any",
    method_name: str,
    overload_types: "Sequence[Type]",
    *args: "Any",
) -> "Any":
    """Call a Python.NET generic method safely.

    It is possible that a method available for the .NET Framework API is not available
    on .NET 6+. As we cannot possibly know whether someone is using one or the other,
    we can wrap Python.NET method calls and report missing methods with a useful error
    message.

    Args:
        caller (Any): Object to find the method on.
        method_name (str): Name of the Python.NET method to be called.
        overload_types (Sequence[Type]): Types used to select the overload.
        *args (Any): Method arguments.

    Returns:
        Any
    """
    try:
        found_method: "Optional[Callable[..., Any]]" = getattr(caller, method_name)
        try:
            return found_method.Overloads.__getitem__(*overload_types)(*args)
        except TypeError:
            return found_method(*args)
    except AttributeError:
        snake_name = utility.snake(method_name)
        raise UnavailableMethodError(
            f'The method "{snake_name}" is not available in .NET 6+ APIs.'
        ) from None


def pythonnet_property_get(
    caller: "Any",
    property_name: str,
) -> "Any":
    """Get a Python.NET property safely.

    It is possible that a property available for the .NET framework API is not available
    on .NET 6+. As we cannot possibly know whether someone is using one or the other,
    we can wrap Python.NET property calls and report missing properties with a useful
    error message.

    Args:
        caller (Any): Object to find the method on.
        property_name (str): Name of the Python.NET method to be called.

    Returns:
        Any
    """
    try:
        return getattr(caller, property_name)
    except AttributeError:
        snake_name = utility.snake(property_name)
        raise UnavailableMethodError(
            f'The property "{snake_name}" is not available in .NET 6+ APIs.'
        ) from None


def pythonnet_property_get_with_method(
    caller: "Any",
    property_name: str,
    method_name: str,
) -> "Any":
    """Get a Python.NET property safely.

    It is possible that a property available for the .NET framework API is not available
    on .NET 6+. As we cannot possibly know whether someone is using one or the other,
    we can wrap Python.NET property calls and report missing properties with a useful
    error message.

    Args:
        caller (Any): Object to find the method on.
        property_name (str): Name of the Python.NET method to be called.
        method_name (str): Method used to actually get the property.

    Returns:
        Any
    """
    try:
        found_property: "Any" = getattr(caller, property_name)
        return getattr(found_property, method_name)
    except AttributeError:
        snake_name = utility.snake(property_name)
        raise UnavailableMethodError(
            f'The property "{snake_name}" is not available in .NET 6+ APIs.'
        ) from None


def pythonnet_property_set(caller: "Any", property_name: str, value: "Any") -> None:
    """Set a Python.NET property safely.

    It is possible that a property available for the .NET framework API is not available
    on .NET 6+. As we cannot possibly know whether someone is using one or the other,
    we can wrap Python.NET property calls and report missing properties with a useful
    error message.

    Args:
        caller (Any): Object to find the method on.
        property_name (str): Name of the Python.NET method to be called.
        value (Any): Value to set the property to.
    """
    try:
        setattr(caller, property_name, value)
    except AttributeError:
        snake_name = utility.snake(property_name)
        raise UnavailableMethodError(
            f'The property "{snake_name}" is not available in .NET 6+ APIs.'
        ) from None


def pythonnet_property_set_with_method(
    caller: "Any", property_name: str, method_name: str, value: "Any"
) -> None:
    """Set a Python.NET property safely.

    It is possible that a property available for the .NET framework API is not available
    on .NET 6+. As we cannot possibly know whether someone is using one or the other,
    we can wrap Python.NET property calls and report missing properties with a useful
    error message.

    Args:
        caller (Any): Object to find the method on.
        property_name (str): Name of the Python.NET method to be called.
        method_name (str): Method used to actually set the property.
        value (Any): Value to set the property to.
    """
    try:
        found_property: "Any" = getattr(caller, property_name)
        found_method: "Callable[[Any], None]" = getattr(found_property, method_name)
        found_method(value)
    except AttributeError:
        snake_name = utility.snake(property_name)
        raise UnavailableMethodError(
            f'The property "{snake_name}" is not available in .NET 6+ APIs.'
        ) from None
