# from OpenGL.GL import (
#     GL_LINE_LOOP,
#     GL_LINE_STRIP,
#     glBegin,
#     glEnd,
#     glVertex2f,
# )

# class Poligono:
#     def __init__(self):
#         self.__pontos = []

#     @property
#     def pontos(self):
#         return self.__pontos
    
#     @property
#     def  lastPoint(self):
#         if len(self.__pontos) > 0:
#             return self.__pontos[-1]
#         else:
#             return None
    
#     def addPonto(self, ponto):
#         self.__pontos.append(ponto)
        
#     def draw(self):
#         glBegin(GL_LINE_LOOP)
#         for ponto in self.__pontos:
#             glVertex2f(ponto.x, ponto.y)
#         glEnd()

#     def drawOpen(self):
#         glBegin(GL_LINE_STRIP)
#         for ponto in self.__pontos:
#             glVertex2f(ponto.x, ponto.y)
#         glEnd()

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, TYPE_CHECKING
from ..utils.floatcmp import Tol, ae, ale, agt, age, ane
from OpenGL.GL import (
    GL_LINE_LOOP,
    GL_LINE_STRIP,
    GL_ENABLE_BIT,
    GL_LINE_STIPPLE,
    glBegin,
    glEnd,
    glVertex2f,
    glColor3f,
    glLineWidth,
    glPushAttrib,
    glLineStipple,
    glEnable,
    glPopAttrib,
)

# Importa sua classe Ponto, que deve ter atributos x e y (float)
from .ponto import Ponto
if TYPE_CHECKING:
    from ..state.context import Context


@dataclass
class Poligono:
    """Representa um polígono composto por pontos no plano."""
    pontos: List[Ponto] = field(default_factory=list)
    selected: bool = False  # flag para objeto selecionado pelo usuário

    @property
    def lastPoint(self) -> Optional[Ponto]:
        """Retorna o último ponto do polígono, se existir."""
        return self.pontos[-1] if self.pontos else None

    def addPonto(self, ponto: Ponto) -> None:
        """Adiciona um novo ponto ao polígono."""
        self.pontos.append(ponto)

    # def draw(self) -> None:
    #     """Desenha o polígono fechado."""
    #     glBegin(GL_LINE_LOOP)
    #     for ponto in self.pontos:
    #         glVertex2f(ponto.x, ponto.y)
    #     glEnd()

    def bounding_box(self) -> Tuple[Ponto, Ponto]:
        xs = [p.x for p in self.pontos]
        ys = [p.y for p in self.pontos]
        p1 = Ponto(min(xs), min(ys))
        p2 = Ponto(max(xs), max(ys))
        return p1, p2
    


    def draw_b_box(self):
        p1, p2 = self.bounding_box()
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(10, 0xAAAA)
        glEnable(GL_LINE_STIPPLE)
        glBegin(GL_LINE_LOOP)
        glVertex2f(p1.x, p1.y)
        glVertex2f(p2.x, p1.y)
        glVertex2f(p2.x, p2.y)
        glVertex2f(p1.x, p2.y)
        glEnd()
        glPopAttrib()


    def draw(self, open_strip: bool = False):
            # estilo
            if self.selected:
                self.draw_b_box()
                glColor3f(1.0, 0.6, 0.0)
                glLineWidth(3.0)
            else:
                glColor3f(1.0, 1.0, 1.0)
                glLineWidth(1.0)

            mode = GL_LINE_STRIP if open_strip else GL_LINE_LOOP
            glBegin(mode)
            for p in self.pontos:
                glVertex2f(p.x, p.y)
            glEnd()
            glLineWidth(1.0)


    def drawOpen(self) -> None:
        """Desenha o polígono parcialmente (ainda não fechado)."""
        glBegin(GL_LINE_STRIP)
        for ponto in self.pontos:
            glVertex2f(ponto.x, ponto.y)
        glEnd()

    def hit_test(self, context: Context, xw: float, yw: float) -> bool:
        from ..view.draw_utils import px_to_world
        tol_world = px_to_world(context, context.global_vars.selection_tolerance_px)
        #print("Tolerancia =", tol_world)
        tol = Tol.abs_only(tol_world) # criando objeto para comparacao de floats
        x_sel = xw
        y_sel = yw
        n_int = 0
        n = len(self.pontos)
        for i in range(n):
            p1 = self.pontos[i]
            p2 = self.pontos[(i+1)%n]
            #print(f"Lado {i}={(i+1)%n}")
            if ane(p1.y, p2.y, tol): # lado não horizontal
                t_int = (y_sel - p1.y)/(p2.y-p1.y)
                x_int = p1.x + t_int*(p2.x-p1.x)
                y_int = y_sel
                #print(f"x_sel = {x_sel:.2f}, y_sel = {y_sel:.2f}, x_int = {x_int:.2f}, y_int = {y_int:.2f}, t_int = {t_int:.2f}")
                if ae(x_int, x_sel, tol) and t_int>=0.0 and t_int<=1.0:
                    #print("Clicou sobre um lado, PARE")
                    return True
                elif agt(x_int, x_sel, tol) and agt(y_int, min(p1.y, p2.y), tol) and ale(y_int, max(p1.y, p2.y), tol):
                    n_int += 1
            elif ae(y_sel, p1.y, tol) and age(x_sel, min(p1.x, p2.x), tol) and ale(x_sel, max(p1.x, p2.x), tol):
                #print("Clicou lado horizontal: PARE")
                return True

        #print(f"N_int = {n_int}")
        return (n_int % 2) != 0

        