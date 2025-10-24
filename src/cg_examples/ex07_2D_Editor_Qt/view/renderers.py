# view/renderers.py
from OpenGL.GL import (
    GL_ENABLE_BIT,
    GL_LINE_LOOP,
    GL_LINE_STIPPLE,
    GL_LINE_STRIP,
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


def draw_circle(circle, dashed: bool = False, color=(1, 1, 1), width: float = 1.0):
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


def draw_polygon(poly, open_strip=False, color=(1, 1, 1), width: float = 1.0):
    glColor3f(*color)
    glLineWidth(width)
    mode = GL_LINE_STRIP if open_strip else GL_LINE_LOOP
    glBegin(mode)
    for p in poly.pontos:
        glVertex2f(p.x, p.y)
    glEnd()
    glLineWidth(1.0)
