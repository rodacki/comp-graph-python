# view/renderers.py
"""Primitivas de renderização imediata usadas pelo editor 2D.

As funções deste módulo encapsulam desenho OpenGL (pipeline fixa) para
círculos, polígonos e segmentos auxiliares, reduzindo duplicação na camada View.
"""

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


def draw_circle(
    circle: Circulo,
    dashed: bool = False,
    color: tuple[float, float, float] = (1, 1, 1),
    width: float = 1.0,
) -> None:
    """Desenha círculo aproximado por polilinha.

    Args:
        circle: Entidade de círculo com centro e raio.
        dashed: Quando `True`, ativa estilo tracejado.
        color: Cor RGB em faixa [0, 1].
        width: Espessura da linha.

    Returns:
        None: Emite vértices no pipeline OpenGL imediato.
    """
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


def draw_polygon(
    poly: Poligono,
    open_strip: bool = False,
    color: tuple[float, float, float] = (1, 1, 1),
    width: float = 1.0,
) -> None:
    """Desenha polígono aberto ou fechado.

    Args:
        poly: Entidade de polígono com lista de vértices.
        open_strip: `True` para polilinha aberta, `False` para loop fechado.
        color: Cor RGB em faixa [0, 1].
        width: Espessura da linha.

    Returns:
        None: Emite vértices no pipeline OpenGL imediato.
    """
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
    """Desenha um segmento entre dois pontos.

    Args:
        x0: Coordenada X do ponto inicial.
        y0: Coordenada Y do ponto inicial.
        x1: Coordenada X do ponto final.
        y1: Coordenada Y do ponto final.
        dashed: Quando `True`, ativa estilo tracejado.
        color: Cor RGB em faixa [0, 1].
        width: Espessura da linha.

    Returns:
        None: Emite vértices no pipeline OpenGL imediato.
    """
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
