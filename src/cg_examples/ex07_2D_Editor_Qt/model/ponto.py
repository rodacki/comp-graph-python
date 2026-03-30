"""Definição de ponto 2D usado pelas primitivas geométricas."""

from dataclasses import dataclass


@dataclass
class Ponto:
    """Representa um ponto 2D no plano cartesiano."""

    x: float = 0.0
    y: float = 0.0

    def __str__(self) -> str:
        """Retorna representação textual compacta do ponto.

        Returns:
            str: Coordenadas no formato `(x, y)` com duas casas decimais.
        """
        return f"({self.x:.2f}, {self.y:.2f})"
