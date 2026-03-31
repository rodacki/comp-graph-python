"""Definição de segmento de reta 2D."""

from dataclasses import dataclass

from .ponto import Ponto


@dataclass
class Segmento:
    """Representa um segmento de reta entre dois pontos.

    Attributes:
        p1: Ponto inicial do segmento.
        p2: Ponto final do segmento.
    """

    p1: Ponto
    p2: Ponto
