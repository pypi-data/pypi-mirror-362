import importlib.metadata

# get version from pyproject.toml
try:
    __version__ = importlib.metadata.version("psychopy-legacy")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.dev"