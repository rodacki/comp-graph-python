# arquivo para definicao de variaveis globais do projeto
from dataclasses import dataclass, field
from typing import Any, List, Optional
from ..model.modelo import Modelo

# ----------------------------------------------------- #
#  Global variables                                     #
# ----------------------------------------------------- #
@dataclass
class GlobalDefinitions():
    contents: List[Any] = field(default_factory=list)
    selected: List[Any] = field(default_factory=list)  # objetos selecionados
    should_exit: bool = False
    left: float = -500.0
    right: float = 500.0
    bottom: float = -500.0
    top: float = 500.0
    w: int = 500
    h: int = 500
    wind: Optional[Any] = None
    poligono: Optional[Any] = None
    circulo: Optional[Any] = None
    modelo: Modelo = field(default_factory=Modelo)
    selection_tolerance_px: int = 3           # tolerância de *hit test* em px
    handle_size_px: int = 20                  # lado do “quadradinho” em px
    handle_size_world: Optional[float] = None # cache: tamanho em coordenadas de mundo
