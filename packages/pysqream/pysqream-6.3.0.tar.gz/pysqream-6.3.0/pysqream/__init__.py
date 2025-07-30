from pysqream.pysqream import connect

try:
    # Py 3.8+
    from importlib.metadata import version
except ImportError:
    # Older Python + setuptools
    from pkg_resources import get_distribution as version
__version__ = version(__name__)

__all__ = ["connect"]
