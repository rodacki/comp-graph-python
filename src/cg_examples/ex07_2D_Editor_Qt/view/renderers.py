# view/renderers.py


from OpenGL.GL import (
    GL_ENABLE_BIT,
    GL_LINE_LOOP,
    GL_LINE_STIPPLE,
    GL_LINE_STRIP,
    GL_LINES,
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

from ..model.circulo import Circulo
from ..model.poligono import Poligono


def draw_circle(circle: Circulo, dashed: bool = False, color=(1, 1, 1), width: float = 1.0):
    glColor3f(*color)
    glLineWidth(width)
    if dashed:
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(10, 0xAAAA)
        glEnable(GL_LINE_STIPPLE)

    glBegin(GL_LINE_LOOP)
    for x, y in circle.sample_polyline():
        glVertex2f(x, y)
    glEnd()

    if dashed:
        glPopAttrib()
    glLineWidth(1.0)


def draw_polygon(poly: Poligono, open_strip=False, color=(1, 1, 1), width: float = 1.0):
    glColor3f(*color)
    glLineWidth(width)
    mode = GL_LINE_STRIP if open_strip else GL_LINE_LOOP
    glBegin(mode)
    for p in poly.pontos:
        glVertex2f(p.x, p.y)
    glEnd()
    glLineWidth(1.0)


def draw_segment(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    *,
    dashed: bool = False,
    color=(1.0, 1.0, 1.0),
    width: float = 1.0,
) -> None:
    """Desenha um segmento entre dois pontos; opcionalmente tracejado."""
    glColor3f(*color)
    glLineWidth(width)

    if dashed:
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(10, 0xAAAA)
        glEnable(GL_LINE_STIPPLE)

    glBegin(GL_LINES)
    glVertex2f(x0, y0)
    glVertex2f(x1, y1)
    glEnd()

    if dashed:
        glPopAttrib()
    glLineWidth(1.0)
