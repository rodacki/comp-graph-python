from __future__ import annotations
from dataclasses import dataclass
import math
from typing import TYPE_CHECKING
from OpenGL.GL import (
    GL_LINE_LOOP, GL_ENABLE_BIT, GL_LINE_STIPPLE,
    glBegin, glEnd, glVertex2f, glPushAttrib, glPopAttrib,
    glEnable, glLineStipple, glColor3f, glLineWidth,
)

if TYPE_CHECKING:
    from ..state.context import Context  # só para type hints, não roda em runtime

@dataclass
class Circulo:
    """Representa um círculo desenhado no plano 2D."""
    xc: float = 0.0
    yc: float = 0.0
    raio: float = 0.0
    segmentos: int = 48  # número de segmentos para aproximar o círculo
    selected: bool = False  # flag para objeto selecionado pelo usuário

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

    def drawOpen(self):
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

    def hit_test(self, context: "Context", xw: float, yw: float) -> bool:
        from ..view.draw_utils import px_to_world
        tol_world = px_to_world(context, context.global_vars.selection_tolerance_px)
        d1 = abs(math.hypot(xw - self.xc, yw - self.yc) - self.raio)
        border = d1 <= tol_world
        inside = ((xw - self.xc)**2 + (yw - self.yc)**2) <=  self.raio**2

        return border or inside