"""A Simple wrapper around StringIO to make things easier."""

from io import BytesIO, StringIO
from typing import Any, cast


class BaseIOWrapper[T: StringIO | BytesIO]:
    """A Base wrapper around IO objects to make things easier."""

    def __init__(self, io_obj: T | Any) -> None:
        """Initialize the IOWrapper with a IO Object object."""
        if not isinstance(io_obj, (StringIO | BytesIO)):
            raise TypeError("io_obj must be an instance of StringIO or BytesIO")
        self._value: T = cast("T", io_obj)
        self._cached_value = None

    def _reset_io(self) -> None:
        """Reset the current a IO Object."""
        self._value.truncate(0)
        self._value.seek(0)
        self._cached_value = None


class StringIOWrapper(BaseIOWrapper[StringIO]):
    """A Simple wrapper around StringIO to make things easier."""

    def __init__(self, **kwargs) -> None:
        """Initialize the IOWrapper with a a IO Object object."""
        super().__init__(StringIO(**kwargs))
        self._cached_value: str = ""

    def _reset_io(self) -> None:
        """Reset the current a IO Object."""
        self._value.truncate(0)
        self._value.seek(0)
        self._cached_value = ""

    def write(self, *values: str) -> None:
        """Write values to the a IO Object object."""
        for value in values:
            self._value.write(value)

    def getvalue(self) -> str:
        """Get the string value from the a IO Object object."""
        self._cached_value = self._value.getvalue()
        return self._cached_value
