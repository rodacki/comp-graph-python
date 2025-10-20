
from OpenGL.GL import (
    GL_PROJECTION,
    GL_MODELVIEW,
    GL_LINES,
    GL_VIEWPORT,
    glViewport,
    glMatrixMode,
    glLoadIdentity,
    glOrtho,
    glBegin,
    glEnd,
    glVertex2f,
    glColor3f,
    glGetIntegerv,
    
)

import numpy as np


# ----------------------------------------------------- #
# Funcao axis: inicializacao do OpenGL                      #
# ----------------------------------------------------- #
def init(context):
    right = context.global_vars.right
    left = context.global_vars.left
    bottom = context.global_vars.bottom
    top = context.global_vars.top

    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(left, right, bottom, top, -1.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# ----------------------------------------------------- #
# Funcao axis: desenha eixos x e y                      #
# ----------------------------------------------------- #
def axis(context):
    #from globals.settings import left, right, top, bottom
    left = context.global_vars.left
    right = context.global_vars.right
    top = context.global_vars.top
    bottom = context.global_vars.bottom

    larg = right - left
    xc = (right + left)/2
    x1 = (xc - larg/2) * 0.8
    x2 = (xc + larg/2) * 0.8
    alt = top - bottom
    yc = (top + bottom)/2
    y1 = (yc - alt/2) * 0.8
    y2 = (yc + alt/2) * 0.8
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
    
#     viewport = glGetIntegerv(GL_VIEWPORT)
#     print("Viewport:", viewport)
#     # coordenadas do volume de visualização
#     xr = context.global_vars.right
#     xl = context.global_vars.left
#     yt = context.global_vars.top
#     yb = context.global_vars.bottom
#     zn = 1.0
#     zf = -1.0
    
#     # matriz de projeçao (window + NDC)
#     P =[
#         [2/(xr-xl), 0.0, 0.0, -(xr+xl)/(xr-xl)],
#         [0.0, 2/(yt-yb), 0.0, -(yt+yb)/(yt-yb)],
#         [0.0, 0.0, -2/(zf-zn), -(zf+zn)/(zf-zn)],
#         [0.0, 0.0, 0.0, 1.0],
#     ]

#     PM = np.array(P)

#     # inversa da matriz de prozeção
#     invP = np.linalg.inv(PM)

#     # conversão das coordenadas do mouse para NDC
#     viewport = glGetIntegerv(GL_VIEWPORT)
#     ywin = viewport[3] - y
#     xndc = (2*(x-viewport[0]))/viewport[2] -1
#     yndc = (2*(ywin-viewport[1]))/viewport[3] -1
#     zndc = 0
#     wndc = 1
#     vndc = np.array([xndc, yndc, zndc,wndc])
    
#     # transformação de projeção inversa
#     world = np.matmul(invP, vndc)

#     return world[0], world[1]

# def getWorldCoords(context, x, y):
#     from OpenGL.GL import glGetIntegerv, GL_VIEWPORT
#     import numpy as np

#     viewport = glGetIntegerv(GL_VIEWPORT)
#     print(f"Viewport real: {viewport}, Global w/h: {context.global_vars.w}, {context.global_vars.h}")

#     # Detecta escala HiDPI (Retina)
#     scale_x = viewport[2] / context.global_vars.w
#     scale_y = viewport[3] / context.global_vars.h

#     # Corrige coordenadas Qt → OpenGL
#     x *= scale_x
#     y *= scale_y
#     ywin = viewport[3] - y

#     # Parâmetros do volume de visualização
#     xr = context.global_vars.right
#     xl = context.global_vars.left
#     yt = context.global_vars.top
#     yb = context.global_vars.bottom
#     zn = 1.0
#     zf = -1.0

#     P = [
#         [2 / (xr - xl), 0.0, 0.0, -(xr + xl) / (xr - xl)],
#         [0.0, 2 / (yt - yb), 0.0, -(yt + yb) / (yt - yb)],
#         [0.0, 0.0, -2 / (zf - zn), -(zf + zn) / (zf - zn)],
#         [0.0, 0.0, 0.0, 1.0],
#     ]

#     invP = np.linalg.inv(np.array(P))

#     # Conversão das coordenadas para NDC
#     xndc = (2 * (x - viewport[0])) / viewport[2] - 1
#     yndc = (2 * (ywin - viewport[1])) / viewport[3] - 1
#     vndc = np.array([xndc, yndc, 0, 1])

#     world = np.matmul(invP, vndc)

#     return world[0], world[1]

def getWorldCoords(context, x, y):
    xr = context.global_vars.right
    xl = context.global_vars.left
    yt = context.global_vars.top
    yb = context.global_vars.bottom
    zn = 1.0
    zf = -1.0

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

    return world[0], world[1]

def px_to_world(context, axis: str = "avg") -> float:
    """
    Converte N pixels (Qt, lógicos) para unidades de mundo.
    axis: "x", "y" ou "avg" (média aritmética de x/y).
    """
    left  = context.global_vars.left
    right = context.global_vars.right
    bottom= context.global_vars.bottom
    top   = context.global_vars.top
    px    = context.global_vars.selection_tolerance_px

    _, _, vw, vh = glGetIntegerv(GL_VIEWPORT)   # em *pixels físicos*
    if vw == 0 or vh == 0:
        return 0.0

    # Fator Retina (mesmo usado em getWorldCoords)
    ratio = context.global_vars.h / vh          # lógicos → físicos

    sx = (right - left) / vw    # mundo por pixel físico (eixo X)
    sy = (top - bottom) / vh    # mundo por pixel físico (eixo Y)

    if axis == "x":
        return px * ratio * sx
    if axis == "y":
        return px * ratio * sy
    # média: boa para testes isotrópicos (círculo, distância ponto-segmento)
    return px * ratio * 0.5 * (sx + sy)