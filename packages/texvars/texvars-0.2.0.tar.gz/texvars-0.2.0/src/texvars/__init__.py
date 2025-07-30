from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

try:
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


from .main import TexVarsGenerator, get_latex_value_cmd

__all__ = [
    "TexVarsGenerator",
    "get_latex_value_cmd"
    ]
