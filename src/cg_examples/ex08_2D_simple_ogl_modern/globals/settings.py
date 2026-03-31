"""Configurações e estado global mínimo do ex08."""

from dataclasses import dataclass

from ..model.modelo import Modelo
from ..model.ponto import Ponto


@dataclass
class GlobalDefinitions:
    """Estado global compartilhado entre contexto, estado e view.

    Attributes:
        modelo: Repositório principal com os segmentos criados.
        ponto_pendente: Primeiro ponto aguardando o segundo clique para formar um segmento.
        ponto_cursor: Posição atual do cursor em NDC para preview do próximo segmento.
        line_color: Cor RGB usada para desenhar segmentos.
        preview_color: Cor RGB usada para preview do segmento temporário.
        clear_color: Cor RGBA de fundo da cena.
        line_width: Espessura das linhas em pixels (1.0 em core profile no macOS).
    """

    modelo: Modelo
    ponto_pendente: Ponto | None = None
    ponto_cursor: Ponto | None = None
    line_color: tuple[float, float, float] = (0.95, 0.95, 0.95)
    preview_color: tuple[float, float, float] = (0.1, 0.95, 0.3)
    clear_color: tuple[float, float, float, float] = (0.08, 0.1, 0.14, 1.0)
    line_width: float = 1.0
