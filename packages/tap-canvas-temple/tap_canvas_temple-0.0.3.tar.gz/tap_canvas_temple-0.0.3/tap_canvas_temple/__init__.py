from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # local editable install, etc.
    __version__ = "0.0.0"