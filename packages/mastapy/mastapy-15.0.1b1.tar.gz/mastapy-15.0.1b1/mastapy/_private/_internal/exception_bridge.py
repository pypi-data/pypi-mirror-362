"""Module for converting .NET exceptions to mastapy-friendly ones."""

import functools
from typing import TYPE_CHECKING

from .exceptions import (
    AnalysisException,
    ApiAccessException,
    InvalidatedPropertyException,
    LicensingException,
    MastapyException,
    ReadOnlyPropertyException,
    ScriptingNotLicensedException,
)
from .python_net import python_net_import

if TYPE_CHECKING:
    from typing import Any, TypeVar

    T = TypeVar("T")

_API_ACCESS_EXCEPTION = python_net_import("SMT.MastaAPI", "APIAccessException")
_INVALIDATED_PROPERTY_EXCEPTION = python_net_import(
    "SMT.MastaAPIUtility.Exceptions", "InvalidatedPropertyException"
)
_READ_ONLY_PROPERTY_EXCEPTION = python_net_import(
    "SMT.MastaAPIUtility.Exceptions", "ReadOnlyPropertyException"
)
_SCRIPTING_NOT_LICENSED_EXCEPTION = python_net_import(
    "SMT.MastaAPIUtility.Exceptions", "ScriptingNotLicensedException"
)


def exception_bridge(func):
    """Decorate method and convert .NET exceptions to mastapy exceptions."""

    @functools.wraps(func)
    def wrapper_exception_bridge(*args: "Any", **kwargs: "Any") -> "T":
        try:
            return func(*args, **kwargs)
        except _API_ACCESS_EXCEPTION as e:
            raise ApiAccessException(e.Message) from None
        except _INVALIDATED_PROPERTY_EXCEPTION as e:
            raise InvalidatedPropertyException(e.Message) from None
        except _READ_ONLY_PROPERTY_EXCEPTION as e:
            raise ReadOnlyPropertyException(e.Message) from None
        except _SCRIPTING_NOT_LICENSED_EXCEPTION as e:
            raise ScriptingNotLicensedException(e.Message) from None
        except Exception as e:
            dotnet_type_method = getattr(e, "GetType", None)

            if dotnet_type_method is None:
                raise

            dotnet_exception_name = dotnet_type_method().Name
            message = getattr(e, "Message")

            if dotnet_exception_name == "AnalysisException":
                raise AnalysisException(message) from None
            elif dotnet_exception_name == "LicensingException":
                raise LicensingException(message) from None

            raise MastapyException(message) from None

    return wrapper_exception_bridge
