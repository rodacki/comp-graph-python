# arquivo para definicao de variaveis globais do projeto
"""Configurações e variáveis globais compartilhadas pelo editor.

O objetivo desta estrutura é centralizar estado de interface e parâmetros
globais usados por múltiplos estados e pela camada de renderização.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from ..model.modelo import Modelo

if TYPE_CHECKING:
    from ..model.ponto import Ponto


# ----------------------------------------------------- #
#  Global variables                                     #
# ----------------------------------------------------- #
@dataclass
class GlobalDefinitions:
    """Container de estado global do editor 2D.

    Attributes:
        contents: Lista genérica para dados auxiliares legados.
        selected: Objetos atualmente selecionados.
        should_exit: Flag auxiliar de encerramento.
        left/right/bottom/top: Limites da janela em coordenadas de mundo.
        w/h: Dimensões do viewport em pixels físicos.
        device_pixel_ratio: Fator de escala HiDPI do monitor.
        wind: Referência opcional para janela principal (legado).
        poligono: Polígono temporário em construção.
        circulo: Círculo temporário em construção.
        modelo: Repositório principal das primitivas da cena.
        selection_tolerance_px: Tolerância de hit-test em pixels lógicos.
        handle_size_px: Tamanho visual das alças (handlers) em pixels lógicos.
        handle_size_world: Cache do tamanho das alças em coordenadas de mundo.
        rotation_snap_degrees: Passo angular (em graus) para snap durante rotação.
    """

    contents: list[Any] = field(default_factory=list)
    selected: list[object] = field(default_factory=list)  # objetos selecionados
    should_exit: bool = False
    left: float = -500.0
    right: float = 500.0
    bottom: float = -500.0
    top: float = 500.0
    w: int = 500
    h: int = 500
    device_pixel_ratio: float = 1.0
    wind: Any | None = None
    poligono: Any | None = None
    circulo: Any | None = None
    modelo: Modelo = field(default_factory=Modelo)
    selection_tolerance_px: int = 3  # tolerância de *hit test* em px
    handle_size_px: int = 20  # lado do “quadradinho” em px
    handle_size_world: float | None = None  # cache: tamanho em coordenadas de mundo
    rotation_snap_degrees: float = 15.0
    pivot: Ponto | None = None
