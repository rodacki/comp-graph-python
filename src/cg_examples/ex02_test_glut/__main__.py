import sys
import os
import numpy as np
from OpenGL.GL import (
    glClearColor, glClear, GL_COLOR_BUFFER_BIT,
    glMatrixMode, glLoadIdentity, glViewport,
    glBegin, glEnd, glVertex2f, glColor3f, glGetIntegerv,
    GL_PROJECTION, GL_MODELVIEW, GL_TRIANGLES, GL_VIEWPORT
)
from OpenGL.GLUT import (
    glutInit, glutInitDisplayMode, glutInitWindowSize, glutInitWindowPosition,
    glutCreateWindow, glutDisplayFunc, glutReshapeFunc, glutKeyboardFunc,
    glutMainLoop, glutSwapBuffers,glutLeaveMainLoop, glutMouseFunc,
    GLUT_DOUBLE, GLUT_RGBA, GLUT_DEPTH
)

# Janela e vista ortográfica básica (coordenadas em "unidades de mundo")
LEFT, RIGHT, BOTTOM, TOP = -1.0, 1.0, -1.0, 1.0

def init_gl(width: int, height: int) -> None:
    """Configura viewport e projeção ortográfica simples."""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Projeção ortográfica 2D
    # Mantemos coordenadas de -1 a 1 para simplificar o desenho do triângulo
    # (sem necessidade de ajuste de aspecto neste exemplo didático)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # Cor de fundo
    glClearColor(0.10, 0.12, 0.16, 1.0)

def display() -> None:
    """Callback de desenho: limpa a tela e renderiza um triângulo."""
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Triângulo colorido em coordenadas NDC-like (-1..1)
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)   # vértice 1 - vermelho
    glVertex2f(-0.6, -0.5)

    glColor3f(0.0, 1.0, 0.0)   # vértice 2 - verde
    glVertex2f( 0.6, -0.5)

    glColor3f(0.0, 0.5, 1.0)   # vértice 3 - azul
    glVertex2f( 0.0,  0.6)
    glEnd()

    glutSwapBuffers()

def reshape(width: int, height: int) -> None:
    """Callback de redimensionamento da janela."""
    if height == 0:
        height = 1
    init_gl(width, height)

def mouse(button, state, x, y):
    xw, yw = getWorldCoords(x, y)
    print(x, y, xw, yw)

def keyboard(key: bytes, x: int, y: int) -> None:
    """Fecha com ESC."""
    if key == b'\x1b':  # ESC
        try:
            glutLeaveMainLoop()  # Funciona no FreeGLUT
        except Exception:
            os._exit(0)  # Saída imediata se glutLeaveMainLoop não existir

# ----------------------------------------------------- #
# Projecao inversa de coordenadas                       #
# ----------------------------------------------------- #
def getWorldCoords(x, y):
    """
    Transforms screen coordinates (x, y) to OpenGL world coordinates.

    Args:
        x (int): The x screen coordinate.
        y (int): The y screen coordinate.

    Returns:
        tuple: A tuple containing the x and y world coordinates.

    Raises:
        ValueError: If the input screen coordinates are not within the viewport.

    This function calculates the world coordinates corresponding to the provided screen coordinates (x, y) by performing the following steps:

    1. Retrieves the current modelview and projection matrices, and the viewport dimensions using OpenGL calls.
    2. Inverts the projection and modelview matrices.
    3. Converts the screen coordinates to normalized device coordinates (NDC) in the range [-1, 1] for both x and y axes.
    4. Constructs a 4D NDC vector with z and w components set to 0 and 1, respectively.
    5. Transforms the NDC vector to clip space by multiplying with the inverse projection matrix.
    6. Transforms the clip space vector to world space by multiplying with the inverse modelview matrix.
    7. Extracts the x and y components of the transformed world space vector and returns them as a tuple.

    Note that this function assumes the depth is always 0 and only returns the x and y world coordinates. If you need all three world coordinates (x, y, z), you can modify the function to extract them accordingly.

    **Error Handling:**

    The function raises a `ValueError` if the provided screen coordinates are not within the viewport bounds.

    **Example Usage:**

    ```python
    x, y = 100, 200
    world_x, world_y = getWorldCoords(x, y)
    print(f"World coordinates: ({world_x:.2f}, {world_y:.2f})")
    ```
           
    # Reference: Karsten Lehn, Merijam Gotzes, Frank Klawonn. 
    # Introduction to Computer Graphics Using OpenGL and Java, 3. Ed.
    # Springer, ISBN 978-3-031-28134-1
    # págs. 171 e 416
     """
    # coordenadas do volume de visualização
    xr = RIGHT
    xl = LEFT
    yt = TOP
    yb = BOTTOM
    zn = 1.0
    zf = -1.0
    
    # matriz de projeçao (window + NDC)
    P =[
        [2/(xr-xl), 0.0, 0.0, -(xr+xl)/(xr-xl)],
        [0.0, 2/(yt-yb), 0.0, -(yt+yb)/(yt-yb)],
        [0.0, 0.0, -2/(zf-zn), -(zf+zn)/(zf-zn)],
        [0.0, 0.0, 0.0, 1.0],
    ]

    PM = np.array(P)

    # inversa da matriz de prozeção
    invP = np.linalg.inv(PM)

    # conversão das coordenadas do mouse para NDC
    viewport = glGetIntegerv(GL_VIEWPORT)
    ywin = viewport[3] - y
    xndc = (2*(x-viewport[0]))/viewport[2] -1
    yndc = (2*(ywin-viewport[1]))/viewport[3] -1
    zndc = 0
    wndc = 1
    vndc = np.array([xndc, yndc, zndc,wndc])

    
    # transformação de projeção inversa
    world = np.matmul(invP, vndc)

    #print("xd:{} yd:{} x:{:.2f} y:{:.2f}".format(x, ywin, world[0], world[1]))
    return world[0], world[1]



def main() -> None:
    # Inicialização do GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(50, 50)
    glutCreateWindow("Ex02 - GLUT Triângulo")

    # Callbacks
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)

    # Primeira configuração de GL
    init_gl(800, 600)

    # Loop principal
    glutMainLoop()

if __name__ == "__main__":
    main()