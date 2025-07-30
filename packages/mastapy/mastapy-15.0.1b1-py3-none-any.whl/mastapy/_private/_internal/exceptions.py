"""Module for custom exceptions."""

from __future__ import annotations


class MastapyException(Exception):
    """Base of all custom mastapy exceptions."""


class MastaInitException(MastapyException):
    """Exception raised when there is an issue with initialising mastapy."""


class MastaPropertyException(MastapyException):
    """Exception raised when there is an issue with a defined MASTA property."""


class MastaPropertyTypeException(MastapyException):
    """Exception raised when there is an issue with the type of a MASTA property."""


class CastException(MastapyException):
    """Exception raised when using the cast method on APIBase."""


class MastapyImportException(MastapyException):
    """Custom exception for errors on import."""


class MastapyVersionException(MastapyException):
    """Custom exception for version errors."""


class ApiAccessException(MastapyException):
    """Exception raised when there is a problem accessing the API."""


class InvalidatedPropertyException(MastapyException):
    """Exception raised when a property is invalidated."""


class ReadOnlyPropertyException(MastapyException):
    """Exception raised when a property is read-only."""


class LicensingException(MastapyException):
    """Exception raised when there are general licensing issues."""


class ScriptingNotLicensedException(LicensingException):
    """Exception raised when scripting has not been licensed."""


class AnalysisException(MastapyException):
    """Exception raised when there is a problem with the analysis."""


class VectorException(MastapyException):
    """Exception raised for errors occurring in the Vector classes."""


class MatrixException(VectorException):
    """Exception raised for errors occurring in the Matrix classes."""


class TypeCheckException(TypeError):
    """Error raised when type checking detects an issue."""


class AssemblyLoadError(Exception):
    """Exception raised if there is a problem loading an assembly."""


class UnavailableMethodError(Exception):
    """Exception raised if a method is unavailable in the currently loaded API."""
