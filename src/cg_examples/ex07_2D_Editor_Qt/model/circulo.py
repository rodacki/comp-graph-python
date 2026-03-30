"""Entidade geométrica de círculo usada pelo editor 2D."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Circulo:
    """Representa um círculo desenhado no plano 2D."""

    xc: float = 0.0
    yc: float = 0.0
    raio: float = 0.0
    segmentos: int = 48  # número de segmentos para aproximar o círculo
    selected: bool = False  # flag para objeto selecionado pelo usuário

    def __str__(self) -> str:
        """Representação legível para logs e depuração.

        Returns:
            str: Descrição textual com centro, raio e estado de seleção.
        """
        return (
            f"Circulo(xc={self.xc:.2f}, yc={self.yc:.2f}, "
            f"raio={self.raio:.2f}, selected={self.selected})"
        )

    def __repr__(self) -> str:
        """Representação oficial da instância em debugging.

        Returns:
            str: Mesmo conteúdo de `__str__`.
        """
        return str(self)

    def sample_polyline(self, n: int | None = None) -> list[tuple[float, float]]:
        """Amostra pontos da circunferência para desenho em polilinha.

        Args:
            n: Quantidade de amostras; quando `None`, usa `self.segmentos`.

        Returns:
            list[tuple[float, float]]: Lista de pontos `(x, y)` na circunferência.
        """
        n = n or self.segmentos
        pts = []
        for i in range(n):
            a = 2 * math.pi * i / n
            pts.append((self.xc + self.raio * math.cos(a), self.yc + self.raio * math.sin(a)))
        return pts

    def hit_test(self, xw: float, yw: float, tol_world: float) -> bool:
        """Testa se ponto de consulta toca borda ou interior do círculo.

        Args:
            xw: Coordenada X do ponto consultado em mundo.
            yw: Coordenada Y do ponto consultado em mundo.
            tol_world: Tolerância em unidades de mundo para seleção de borda.

        Returns:
            bool: `True` quando ponto está na borda (com tolerância) ou dentro.
        """
        d1 = abs(math.hypot(xw - self.xc, yw - self.yc) - self.raio)
        border = d1 <= tol_world
        inside = ((xw - self.xc) ** 2 + (yw - self.yc) ** 2) <= self.raio**2
        return border or inside

    def translate(self, dx: float, dy: float) -> None:
        """Move o círculo por um deslocamento (dx, dy) no mundo."""
        self.xc += dx
        self.yc += dy
