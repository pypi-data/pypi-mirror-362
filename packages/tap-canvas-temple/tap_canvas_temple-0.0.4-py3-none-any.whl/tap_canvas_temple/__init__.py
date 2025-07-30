from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("tap-canvas-temple")
except PackageNotFoundError:  # local editable install, etc.
    __version__ = "0.0.0"