from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from OpenGL.GL import (
    GL_ENABLE_BIT,
    GL_LINE_LOOP,
    GL_LINE_STIPPLE,
    glBegin,
    glColor3f,
    glEnable,
    glEnd,
    glLineStipple,
    glLineWidth,
    glPopAttrib,
    glPushAttrib,
    glVertex2f,
)

if TYPE_CHECKING:
    pass  # só para type hints, não roda em runtime


@dataclass
class Circulo:
    """Representa um círculo desenhado no plano 2D."""

    xc: float = 0.0
    yc: float = 0.0
    raio: float = 0.0
    segmentos: int = 48  # número de segmentos para aproximar o círculo
    selected: bool = False  # flag para objeto selecionado pelo usuário

    def sample_polyline(self, n: int | None = None) -> list[tuple[float, float]]:
        """Retorna pontos (x,y) para desenhar o círculo como polilinha."""
        n = n or self.segmentos
        pts = []
        for i in range(n):
            a = 2 * math.pi * i / n
            pts.append((self.xc + self.raio * math.cos(a), self.yc + self.raio * math.sin(a)))
        return pts

    def draw(self):
        """Desenha o círculo completo."""
        # estilo
        if self.selected:
            glColor3f(0.2, 1.0, 0.2)
            glLineWidth(3.0)
        else:
            glColor3f(1.0, 1.0, 1.0)
            glLineWidth(1.0)

        glBegin(GL_LINE_LOOP)
        for i in range(self.segmentos):
            angle = 2 * math.pi * i / self.segmentos
            x = self.xc + self.raio * math.cos(angle)
            y = self.yc + self.raio * math.sin(angle)
            glVertex2f(x, y)
        glEnd()
        glLineWidth(1.0)

    def draw_open(self):
        """Desenha o círculo com linha tracejada (modo temporário)."""
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(10, 0xAAAA)
        glEnable(GL_LINE_STIPPLE)
        glBegin(GL_LINE_LOOP)
        for i in range(self.segmentos):
            angle = 2 * math.pi * i / self.segmentos
            x = self.xc + self.raio * math.cos(angle)
            y = self.yc + self.raio * math.sin(angle)
            glVertex2f(x, y)
        glEnd()
        glPopAttrib()

    def hit_test(self, xw: float, yw: float, tol_world: float) -> bool:
        d1 = abs(math.hypot(xw - self.xc, yw - self.yc) - self.raio)
        border = d1 <= tol_world
        inside = ((xw - self.xc) ** 2 + (yw - self.yc) ** 2) <= self.raio**2
        return border or inside
