import math

from OpenGL.GL import (
    GL_ENABLE_BIT,
    GL_LINE_LOOP,
    GL_LINE_STIPPLE,
    glBegin,
    glEnable,
    glEnd,
    glLineStipple,
    glPopAttrib,
    glPushAttrib,
    glVertex2f,
)


class Circulo:
    def __init__(self, xc=0.0, yc=0.0, raio=0.0):
        self._xc = xc
        self._yc = yc
        self._raio = raio

    @property
    def xc(self):
        return self._xc

    @xc.setter
    def xc(self, novoxc):
        self._xc = novoxc

    @property
    def yc(self):
        return self._yc

    @yc.setter
    def yc(self, novoyc):
        self._yc = novoyc

    @property
    def raio(self):
        return self._raio

    @raio.setter
    def raio(self, novoraio):
        self._raio = novoraio

    def draw(self):
        glBegin(GL_LINE_LOOP)
        for i in range(24):
            x = self.xc + self._raio * math.cos(i * 2 * math.pi / 24)
            y = self.yc + self._raio * math.sin(i * 2 * math.pi / 24)
            glVertex2f(x, y)
        glEnd()

    def drawOpen(self):
        glPushAttrib(GL_ENABLE_BIT)
        # glPushAttrib is done to return everything to normal after drawing
        glLineStipple(3, 0xAAAA)  # [1]
        glEnable(GL_LINE_STIPPLE)
        glBegin(GL_LINE_LOOP)
        for i in range(24):
            x = self.xc + self._raio * math.cos(i * 2 * math.pi / 24)
            y = self.yc + self._raio * math.sin(i * 2 * math.pi / 24)
            glVertex2f(x, y)
        glEnd()
        glPopAttrib()

    def __str__(self):
        mensagem = f"Circulo - xc: {self.xc:.2f} yc: {self.yc:.2f} raio: {self.raio:.2f}"
        return mensagem
