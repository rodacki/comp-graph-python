# arquivo para definicao de variaveis globais do projeto
from dataclasses import dataclass, field
from typing import Any

from ..model.modelo import Modelo


# ----------------------------------------------------- #
#  Global variables                                     #
# ----------------------------------------------------- #
@dataclass
class GlobalDefinitions:
    contents: list[Any] = field(default_factory=list)
    selected: list[Any] = field(default_factory=list)  # objetos selecionados
    should_exit: bool = False
    left: float = -500.0
    right: float = 500.0
    bottom: float = -500.0
    top: float = 500.0
    w: int = 500
    h: int = 500
    wind: Any | None = None
    poligono: Any | None = None
    circulo: Any | None = None
    modelo: Modelo = field(default_factory=Modelo)
    selection_tolerance_px: int = 3  # tolerância de *hit test* em px
    handle_size_px: int = 20  # lado do “quadradinho” em px
    handle_size_world: float | None = None  # cache: tamanho em coordenadas de mundo
