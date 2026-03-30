"""Utilitários de projeção e conversão de coordenadas para a View.

Este módulo concentra rotinas auxiliares de desenho e conversão entre:
- coordenadas do widget Qt (pixels lógicos),
- pixels físicos do framebuffer OpenGL,
- coordenadas de mundo do editor.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..state.context import Context

from OpenGL.GL import (
    GL_LINES,
    GL_MODELVIEW,
    GL_PROJECTION,
    glBegin,
    glColor3f,
    glEnd,
    glLoadIdentity,
    glMatrixMode,
    glOrtho,
    glVertex2f,
)


def init(context: Context) -> None:
    """Inicializa matriz de projeção ortográfica e modelview.

    Args:
        context: Contexto com limites de janela em coordenadas de mundo.

    Returns:
        None: Atualiza o estado OpenGL da matriz corrente.
    """
    gv = context.global_vars
    left, right, bottom, top = gv.left, gv.right, gv.bottom, gv.top
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if right == left:
        right = left + 1.0
    if top == bottom:
        top = bottom + 1.0

    glOrtho(left, right, bottom, top, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def axis(context: Context) -> None:
    """Desenha eixos X (vermelho) e Y (verde) no centro da janela.

    Args:
        context: Contexto com limites de janela em coordenadas de mundo.

    Returns:
        None: Emite segmentos de linha no pipeline OpenGL imediato.
    """
    gv = context.global_vars
    left, right, top, bottom = gv.left, gv.right, gv.top, gv.bottom

    larg = right - left
    alt = top - bottom

    xc = (right + left) / 2
    yc = (top + bottom) / 2

    x1 = (xc - larg / 2) * 0.8
    x2 = (xc + larg / 2) * 0.8
    y1 = (yc - alt / 2) * 0.8
    y2 = (yc + alt / 2) * 0.8

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(x1, yc)
    glVertex2f(x2, yc)
    glEnd()

    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(xc, y1)
    glVertex2f(xc, y2)
    glEnd()


def get_world_coords(context: Context, x: int, y: int) -> tuple[float, float]:
    """Converte coordenadas de tela (Qt) para coordenadas de mundo.

    Args:
        context: Contexto com limites da janela e métricas de framebuffer.
        x: Coordenada X em pixels lógicos do evento Qt.
        y: Coordenada Y em pixels lógicos do evento Qt.

    Returns:
        tuple[float, float]: Ponto `(xw, yw)` em coordenadas de mundo.
    """
    gv = context.global_vars
    xl, xr, yb, yt = gv.left, gv.right, gv.bottom, gv.top
    ratio = gv.device_pixel_ratio or 1.0
    width = gv.w or 1
    height = gv.h or 1

    x_phys = x * ratio
    y_phys = y * ratio
    ywin = height - y_phys

    world_x = xl + (x_phys / width) * (xr - xl)
    world_y = yb + (ywin / height) * (yt - yb)
    return float(world_x), float(world_y)


def px_to_world(context: Context, px: float, axis: str = "avg") -> float:
    """Converte distância em pixels lógicos para distância em mundo.

    Args:
        context: Contexto com limites da janela e métricas do framebuffer.
        px: Distância em pixels lógicos (Qt).
        axis: Eixo de referência:
            - `"x"`: usa escala horizontal;
            - `"y"`: usa escala vertical;
            - `"avg"`: média das duas escalas (padrão).

    Returns:
        float: Distância equivalente em coordenadas de mundo.
    """
    gv = context.global_vars
    left, right, bottom, top = gv.left, gv.right, gv.bottom, gv.top
    vw = gv.w or 0
    vh = gv.h or 0
    if vw == 0 or vh == 0:
        return 0.0

    ratio = gv.device_pixel_ratio or 1.0

    sx = (right - left) / vw
    sy = (top - bottom) / vh

    if axis == "x":
        return px * ratio * sx
    if axis == "y":
        return px * ratio * sy
    return px * ratio * 0.5 * (sx + sy)
