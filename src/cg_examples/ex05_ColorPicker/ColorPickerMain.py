import sys
from enum import Enum

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# ----------------------------------------------------- #
#  Global variables                                     #
# ----------------------------------------------------- #
left = -10.0
right = 110.0
bottom = -30.0
top = 90.0

# poligono = Poligono()
# circulo = Circulo()
w, h = 500, 500


# ----------------------------------------------------- #
#  FiniteState class: para nomear estados de interacao  #
# ----------------------------------------------------- #
class FiniteState(Enum):
    NONE = 0
    CREATE_POLIGONO = 1
    END_POLIGONO = 2
    ADD_POINT = 3
    DELETE = 4
    INIT_CIRCULO = 5
    END_CIRCULO = 6


# ----------------------------------------------------- #
# State Manager Singleton: gerenciar eventos de teclado #
# ----------------------------------------------------- #
class StateManagerSingleton:

    _instance = None

    def __init__(self):
        self.currentState = FiniteState.NONE

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def redSlider():
    glBegin(GL_QUADS)
    glColor3ub(0, 0, 0)
    glVertex2d(0, 80)
    glVertex2d(0, 70)
    glColor3ub(255, 0, 0)
    glVertex2d(100, 70)
    glVertex2d(100, 80)
    glEnd()
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glColor3ub(94, 93, 91)
    glVertex2d(0, 80)
    glVertex2d(0, 70)
    glVertex2d(100, 70)
    glVertex2d(100, 80)
    glEnd()


def greenSlider():
    glBegin(GL_QUADS)
    glColor3ub(0, 0, 0)
    glVertex2d(0, 60)
    glVertex2d(0, 50)
    glColor3ub(0, 255, 0)
    glVertex2d(100, 50)
    glVertex2d(100, 60)
    glEnd()
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glColor3ub(94, 93, 91)
    glVertex2d(0, 60)
    glVertex2d(0, 50)
    glVertex2d(100, 50)
    glVertex2d(100, 60)
    glEnd()


def blueSlider():
    glBegin(GL_QUADS)
    glColor3ub(0, 0, 0)
    glVertex2d(0, 40)
    glVertex2d(0, 30)
    glColor3ub(0, 0, 255)
    glVertex2d(100, 30)
    glVertex2d(100, 40)
    glEnd()
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glColor3ub(94, 93, 91)
    glVertex2d(0, 40)
    glVertex2d(0, 30)
    glVertex2d(100, 30)
    glVertex2d(100, 40)
    glEnd()


# ----------------------------------------------------- #
# Funcao axis: desenha eixos x e y                      #
# ----------------------------------------------------- #
def axis():
    larg = right - left
    xc = (right + left) / 2
    x1 = (xc - larg / 2) * 0.8
    x2 = (xc + larg / 2) * 0.8
    alt = top - bottom
    yc = (top + bottom) / 2
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


def init():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(left, right, bottom, top, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# ----------------------------------------------------- #
# Callback de redesenho de tela                         #
# ----------------------------------------------------- #
def showScreen():
    glClearColor(42 / 255, 40 / 255, 37 / 255, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    redSlider()
    greenSlider()
    blueSlider()
    # iterate()
    # axis()
    glColor3f(1.0, 0.0, 3.0)
    # if gui_state.currentState == FiniteState.ADD_POINT:
    #    poligono.drawOpen()
    # modelo.draw()
    glutSwapBuffers()


# ----------------------------------------------------- #
# Callback de alteracao do tamanho da janela            #
# ----------------------------------------------------- #
def reshape(width, height):
    print("reshape", width, height)
    # Evita a divisao por zero
    if height == 0:
        height = 1

    # Especifica as dimensões da Viewport
    glViewport(0, 0, width, height)

    # Inicializa o sistema de coordenadas
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # glOrtho(left, right, bottom, top, -1.0, 1.0)
    # Estabelece a janela de seleção (left, right, bottom, top)
    if width <= height:
        glOrtho(left, right, bottom, top * height / width, -1.0, 1.0)
    else:
        glOrtho(left, right * width / height, bottom, top, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# ----------------------------------------------------- #
# Callback de eventos de teclado                        #
# ----------------------------------------------------- #
def onKeyboard(key, x, y):
    print(key, type(key))
    if key.decode() == chr(27):
        glutDestroyWindow(wind)
        sys.exit(0)

    elif key.decode() == "c":
        gui_state.currentState = FiniteState.CREATE_POLIGONO
        print("create")

    elif key.decode() == "f":
        gui_state.currentState = FiniteState.END_POLIGONO

    elif key.decode() == "i":
        gui_state.currentState = FiniteState.INIT_CIRCULO

    elif key.decode() == "o":
        gui_state.currentState = FiniteState.END_CIRCULO

    print("Estado: ", gui_state.currentState)


# ----------------------------------------------------- #
# Callback de eventos click de mouse                    #
# ----------------------------------------------------- #
def onMouseButton(button, state, x, y):
    coords = getWorldCoords(x, y)
    print(x, y, coords[0], coords[1])

    # p = Ponto(coords[0], coords[1])
    global circulo
    print("Estado onMouse:", gui_state.currentState)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if gui_state.currentState == FiniteState.CREATE_POLIGONO:
            print("criando poligono")
            # global poligono
            # poligono = Poligono()
            # poligono.addPonto(p)
            gui_state.currentState = FiniteState.ADD_POINT

        elif gui_state.currentState == FiniteState.ADD_POINT:
            print("adicionando ponto")
            # poligono.addPonto(p)

        elif gui_state.currentState == FiniteState.END_POLIGONO:
            print("finalizando poligono")
            # modelo.addPoligono(poligono)
            gui_state.currentState = FiniteState.NONE

        elif gui_state.currentState == FiniteState.INIT_CIRCULO:
            print("criando circulo")
            # circulo = Circulo()
            # circulo.xc = p.x
            # circulo.yc = p.y
            gui_state.currentState = FiniteState.END_CIRCULO

        elif gui_state.currentState == FiniteState.END_CIRCULO:
            print("encerrando circulo")
            # raio = math.sqrt((p.x-circulo.xc)**2 + (p.y-circulo.yc)**2)
            # circulo.raio = raio
            # modelo.addCirculo(circulo)
            gui_state.currentState = FiniteState.NONE

    if gui_state.currentState != FiniteState.NONE:
        glutPostRedisplay()


# ----------------------------------------------------- #
# Callback de movimento de mouse                        #
# ----------------------------------------------------- #
def mouseMotion(x, y):
    print("Motion:", x, y)


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
    xr = right
    xl = left
    yt = top
    yb = bottom
    zn = 1.0
    zf = -1.0

    # matriz de projeçao (window + NDC)
    P = [
        [2 / (xr - xl), 0.0, 0.0, -(xr + xl) / (xr - xl)],
        [0.0, 2 / (yt - yb), 0.0, -(yt + yb) / (yt - yb)],
        [0.0, 0.0, -2 / (zf - zn), -(zf + zn) / (zf - zn)],
        [0.0, 0.0, 0.0, 1.0],
    ]

    PM = np.array(P)

    # inversa da matriz de prozeção
    invP = np.linalg.inv(PM)

    # conversão das coordenadas do mouse para NDC
    viewport = glGetIntegerv(GL_VIEWPORT)
    ywin = viewport[3] - y
    xndc = (2 * (x - viewport[0])) / viewport[2] - 1
    yndc = (2 * (ywin - viewport[1])) / viewport[3] - 1
    zndc = 0
    wndc = 1
    vndc = np.array([xndc, yndc, zndc, wndc])

    # transformação de projeção inversa
    world = np.matmul(invP, vndc)

    # print("xd:{} yd:{} x:{:.2f} y:{:.2f}".format(x, ywin, world[0], world[1]))
    return world[0], world[1]


# ----------------------------------------------------- #
# Funcao principal do programa                          #
# ----------------------------------------------------- #
def main():
    global wind
    global gui_state
    global modelo

    gui_state = StateManagerSingleton.instance()

    glutInit()
    print(chr(27))
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow("IFC - BCC - CG - 2024")
    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)
    glutKeyboardFunc(onKeyboard)
    glutMouseFunc(onMouseButton)
    glutReshapeFunc(reshape)
    glutMotionFunc(mouseMotion)
    init()
    glutMainLoop()


if __name__ == "__main__":
    main()
