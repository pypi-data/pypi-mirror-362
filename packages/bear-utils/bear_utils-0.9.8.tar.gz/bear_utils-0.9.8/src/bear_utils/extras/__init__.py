"""A module for various utilities in Bear Utils extras."""

from singleton_base import SingletonBase

from ._tools import ClipboardManager, ascii_header, clear_clipboard, copy_to_clipboard, paste_from_clipboard
from ._zapper import zap, zap_as, zap_as_multi, zap_get, zap_multi
from .platform_utils import OS, get_platform, is_linux, is_macos, is_windows
from .wrappers.add_methods import add_comparison_methods

__all__ = [
    "OS",
    "ClipboardManager",
    "SingletonBase",
    "add_comparison_methods",
    "ascii_header",
    "clear_clipboard",
    "copy_to_clipboard",
    "get_platform",
    "is_linux",
    "is_macos",
    "is_windows",
    "paste_from_clipboard",
    "zap",
    "zap_as",
    "zap_as_multi",
    "zap_get",
    "zap_multi",
]
