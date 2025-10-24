from OpenGL.GL import (
    GL_LINE_LOOP,
    GL_LINE_STRIP,
    glBegin,
    glEnd,
    glVertex2f,
)


class Poligono:
    def __init__(self):
        self.__pontos = []

    @property
    def pontos(self):
        return self.__pontos

    @property
    def lastPoint(self):
        if len(self.__pontos) > 0:
            return self.__pontos[-1]
        else:
            return None

    def addPonto(self, ponto):
        self.__pontos.append(ponto)

    def draw(self):
        glBegin(GL_LINE_LOOP)
        for ponto in self.__pontos:
            glVertex2f(ponto.x, ponto.y)
        glEnd()

    def drawOpen(self):
        glBegin(GL_LINE_STRIP)
        for ponto in self.__pontos:
            glVertex2f(ponto.x, ponto.y)
        glEnd()
