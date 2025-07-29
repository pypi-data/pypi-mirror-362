from .sob_pomes import DB_ID, DB_TABLE, PySob

__all__ = [
    "DB_ID", "DB_TABLE", "PySob"
]

from importlib.metadata import version
__version__: str = version("pypomes_core")
__version_info__: tuple = tuple(int(i) for i in __version__.split(".") if i.isdigit())
