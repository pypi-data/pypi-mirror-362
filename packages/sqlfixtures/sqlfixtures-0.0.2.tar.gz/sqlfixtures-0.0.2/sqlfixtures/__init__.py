from .insertable import Insertable
from .insertable import Generated
from .insertable import apply_to_fixture
from .insertable import SELF
from .insertable import PARENT
from .sqlfixture import SQLFixture

__version__ = "0.0.2"
__all__ = [
    "Insertable",
    "Generated",
    "SQLFixture",
    "apply_to_fixture",
    "SELF",
    "PARENT",
]
