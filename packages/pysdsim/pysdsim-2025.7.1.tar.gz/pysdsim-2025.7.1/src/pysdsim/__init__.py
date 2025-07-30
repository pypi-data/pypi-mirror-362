from .core import Simulator
import importlib.metadata


__author__ = "Morteza Khazaei <morteza.khazaei@usherbrooke.ca>"
try:
    __version__ = importlib.metadata.version("pysdsim")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"