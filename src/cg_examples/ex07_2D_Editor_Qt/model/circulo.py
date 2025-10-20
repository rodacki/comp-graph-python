# import math
# from OpenGL.GL import (
#     GL_LINE_LOOP,
#     GL_ENABLE_BIT,
#     GL_LINE_STIPPLE,
#     glBegin,
#     glEnd,
#     glVertex2f,
#     glPushAttrib,
#     glLineStipple,
#     glEnable,
#     glPopAttrib
# )

# class Circulo:
#     def __init__(self, xc = 0.0, yc = 0.0, raio = 0.0):
#         self._xc = xc
#         self._yc = yc
#         self._raio = raio

#     @property
#     def xc(self):
#         return self._xc
    
#     @xc.setter
#     def xc(self, novoxc):
#         self._xc = novoxc

#     @property
#     def yc(self):
#         return self._yc
    
#     @yc.setter
#     def yc(self, novoyc):
#         self._yc = novoyc

#     @property
#     def raio(self):
#         return self._raio
    
#     @raio.setter
#     def raio(self, novoraio):
#         self._raio = novoraio

#     def draw(self):
#         glBegin(GL_LINE_LOOP)
#         for i in range(24):
#             x = self.xc + self._raio * math.cos(i*2*math.pi/24)
#             y = self.yc + self._raio * math.sin(i*2*math.pi/24)
#             glVertex2f(x, y)
#         glEnd()


#     def drawOpen(self):
#         glPushAttrib(GL_ENABLE_BIT)
#         # glPushAttrib is done to return everything to normal after drawing
#         glLineStipple(3, 0xAAAA)  # [1]
#         glEnable(GL_LINE_STIPPLE)
#         glBegin(GL_LINE_LOOP)
#         for i in range(24):
#             x = self.xc + self._raio * math.cos(i*2*math.pi/24)
#             y = self.yc + self._raio * math.sin(i*2*math.pi/24)
#             glVertex2f(x, y)
#         glEnd()
#         glPopAttrib()
    
#     def __str__(self):
#         mensagem = "Circulo - xc: {:.2f} yc: {:.2f} raio: {:.2f}".format(self.xc, self.yc, self.raio)
#         return mensagem


from dataclasses import dataclass
import math
from OpenGL.GL import (
    GL_LINE_LOOP,
    glBegin,
    glEnd,
    glVertex2f,
    glPushAttrib,
    glPopAttrib,
    GL_ENABLE_BIT,
    glEnable,
    glLineStipple,
    glColor3f,
    glLineWidth,
    GL_LINE_STIPPLE,
)

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

    def hit_test(self, context, xw: float, yw: float) -> bool:
        from ..view.draw_utils import px_to_world
        tol_world = px_to_world(context)
        d1 = abs(math.hypot(xw - self.xc, yw - self.yc) - self.raio)
        border = d1 <= tol_world
        inside = ((xw - self.xc)**2 + (yw - self.yc)**2) <=  self.raio**2

        return border or inside