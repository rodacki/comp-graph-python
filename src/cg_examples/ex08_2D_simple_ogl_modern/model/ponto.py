"""Definição de ponto 2D em coordenadas NDC.

NDC (Normalized Device Coordinates) usam o intervalo [-1, 1] nos eixos X e Y.
"""

from dataclasses import dataclass


@dataclass
class Ponto:
    """Representa um ponto 2D em NDC.

    Attributes:
        x: Coordenada horizontal em NDC.
        y: Coordenada vertical em NDC.
    """

    x: float
    y: float
