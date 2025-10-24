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
        return (
            f"Circulo(xc={self.xc:.2f}, yc={self.yc:.2f}, "
            f"raio={self.raio:.2f}, selected={self.selected})"
        )

    def __repr__(self) -> str:
        return str(self)

    def sample_polyline(self, n: int | None = None) -> list[tuple[float, float]]:
        """Retorna pontos (x,y) para desenhar o círculo como polilinha."""
        n = n or self.segmentos
        pts = []
        for i in range(n):
            a = 2 * math.pi * i / n
            pts.append((self.xc + self.raio * math.cos(a), self.yc + self.raio * math.sin(a)))
        return pts

    def hit_test(self, xw: float, yw: float, tol_world: float) -> bool:
        d1 = abs(math.hypot(xw - self.xc, yw - self.yc) - self.raio)
        border = d1 <= tol_world
        inside = ((xw - self.xc) ** 2 + (yw - self.yc) ** 2) <= self.raio**2
        return border or inside
