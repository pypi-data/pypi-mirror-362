

from pathlib import Path
from typing import Final

BUILDTOOLS_DIR:Final[Path] = Path(__file__).parent.parent
SCRIPTS_DIR: Final[Path] = BUILDTOOLS_DIR / 'scripts'
