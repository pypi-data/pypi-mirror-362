from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("carey_mcp_video")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.1"

from .server import mcp