import sys
from .core import parla

if not sys.platform.startswith("win"):
    raise ImportError(
        "rsd_tts è compatibile solo con Windows 10/11. "
        "Verifica di avere un voice pack italiano installato."
    )

__version__ = "0.1.0"
__all__ = ['parla']


