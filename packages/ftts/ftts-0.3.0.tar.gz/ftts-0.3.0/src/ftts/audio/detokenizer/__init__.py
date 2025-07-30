from ...utils import _LazyModule
from typing import TYPE_CHECKING

_import_structure = {
    "spark_detokenizer": ["SparkDeTokenizer"],
    "snac_detokenizer": ["SnacDeTokenizer"],
}
if TYPE_CHECKING:
    from .spark_detokenizer import SparkDeTokenizer
    from .snac_detokenizer import SnacDeTokenizer

else:
    import sys

    sys.modules[__name__] = _LazyModule(
        __name__,
        globals()["__file__"],
        _import_structure,
        module_spec=__spec__,
    )
