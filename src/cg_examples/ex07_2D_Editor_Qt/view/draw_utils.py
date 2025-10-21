from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..state.context import Context 

import numpy as np

from OpenGL.GL import (
    GL_PROJECTION, GL_MODELVIEW, GL_LINES, GL_VIEWPORT,
    glMatrixMode, glLoadIdentity, glOrtho,
    glBegin, glEnd, glVertex2f, glColor3f, glGetIntegerv, 
)

# ----------------------------------------------------- #
# Inicialização de projeção/matriz (sem mexer no viewport)
# ----------------------------------------------------- #
def init(context: "Context") -> None:
    gv = context.global_vars
    left, right, bottom, top = gv.left, gv.right, gv.bottom, gv.top
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Protege contra largura/altura zero
    if right == left:
        right = left + 1.0
    if top == bottom:
        top = bottom + 1.0
    glOrtho(left, right, bottom, top, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# ----------------------------------------------------- #
# Funcao axis: desenha eixos x e y                      #
# ----------------------------------------------------- #
def axis(context: "Context"):
    gv = context.global_vars
    left, right, top, bottom = gv.left, gv.right, gv.top, gv.bottom

    larg = right - left
    alt = top - bottom

    xc = (right + left)/2
    yc = (top + bottom)/2

    x1 = (xc - larg/2) * 0.8
    x2 = (xc + larg/2) * 0.8
    y1 = (yc - alt/2) * 0.8
    y2 = (yc + alt/2) * 0.8

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES); glVertex2f(x1, yc); glVertex2f(x2, yc); glEnd()

    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES); glVertex2f(xc, y1); glVertex2f(xc, y2); glEnd()

# ----------------------------------------------------- #
# Projecao inversa de coordenadas                       #
# ----------------------------------------------------- #
# def getWorldCoords(context, x, y):
#     """
#     Transforms screen coordinates (x, y) to OpenGL world coordinates.

#     Args:
#         x (int): The x screen coordinate.
#         y (int): The y screen coordinate.

#     Returns:
#         tuple: A tuple containing the x and y world coordinates.

#     Raises:
#         ValueError: If the input screen coordinates are not within the viewport.

#     This function calculates the world coordinates corresponding to the provided screen coordinates (x, y) by performing the following steps:

#     1. Retrieves the current modelview and projection matrices, and the viewport dimensions using OpenGL calls.
#     2. Inverts the projection and modelview matrices.
#     3. Converts the screen coordinates to normalized device coordinates (NDC) in the range [-1, 1] for both x and y axes.
#     4. Constructs a 4D NDC vector with z and w components set to 0 and 1, respectively.
#     5. Transforms the NDC vector to clip space by multiplying with the inverse projection matrix.
#     6. Transforms the clip space vector to world space by multiplying with the inverse modelview matrix.
#     7. Extracts the x and y components of the transformed world space vector and returns them as a tuple.

#     Note that this function assumes the depth is always 0 and only returns the x and y world coordinates. If you need all three world coordinates (x, y, z), you can modify the function to extract them accordingly.

#     **Error Handling:**

#     The function raises a `ValueError` if the provided screen coordinates are not within the viewport bounds.

#     **Example Usage:**

#     ```python
#     x, y = 100, 200
#     world_x, world_y = getWorldCoords(x, y)
#     print(f"World coordinates: ({world_x:.2f}, {world_y:.2f})")
#     ```
           
#     # Reference: Karsten Lehn, Merijam Gotzes, Frank Klawonn. 
#     # Introduction to Computer Graphics Using OpenGL and Java, 3. Ed.
#     # Springer, ISBN 978-3-031-28134-1
#     # págs. 171 e 416
#      """
def getWorldCoords(context: "Context", x: int, y: int)-> tuple[float, float] :
    gv = context.global_vars
    xl, xr, yb, yt = gv.left, gv.right, gv.bottom, gv.top
    zn = 1.0
    zf = -1.0
    # matriz de projeção
    P = [
        [2 / (xr - xl), 0.0, 0.0, -(xr + xl) / (xr - xl)],
        [0.0, 2 / (yt - yb), 0.0, -(yt + yb) / (yt - yb)],
        [0.0, 0.0, -2 / (zf - zn), -(zf + zn) / (zf - zn)],
        [0.0, 0.0, 0.0, 1.0],
    ]
    invP = np.linalg.inv(np.array(P))

    # 💡 Compensar o fator de escala Retina
    ratio = context.global_vars.h / glGetIntegerv(GL_VIEWPORT)[3]
    x *= ratio
    y *= ratio

    viewport = glGetIntegerv(GL_VIEWPORT)
    ywin = viewport[3] - y
    xndc = (2 * (x - viewport[0])) / viewport[2] - 1
    yndc = (2 * (ywin - viewport[1])) / viewport[3] - 1

    vndc = np.array([xndc, yndc, 0, 1])
    world = np.matmul(invP, vndc)

    return float(world[0]), float(world[1])

def px_to_world(context: "Context", px: float, axis: str = "avg") -> float:
    """
    Converte N pixels (Qt, lógicos) para unidades de mundo.
    axis: "x", "y" ou "avg" (média aritmética de x/y).
    """
    gv = context.global_vars
    left, right, bottom, top = gv.left, gv.right, gv.bottom, gv.top
    
    _, _, vw, vh = glGetIntegerv(GL_VIEWPORT)   # em *pixels físicos*
    if vw == 0 or vh == 0:
        return 0.0

    # Fator Retina (mesmo usado em getWorldCoords)
    ratio = gv.h / vh          # lógicos → físicos

    sx = (right - left) / vw    # mundo por pixel físico (eixo X)
    sy = (top - bottom) / vh    # mundo por pixel físico (eixo Y)

    if axis == "x":
        return px * ratio * sx
    if axis == "y":
        return px * ratio * sy
    # média: boa para testes isotrópicos (círculo, distância ponto-segmento)
    return px * ratio * 0.5 * (sx + sy)