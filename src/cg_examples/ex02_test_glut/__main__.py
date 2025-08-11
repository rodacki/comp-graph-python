import sys
import os
from OpenGL.GL import (
    glClearColor, glClear, GL_COLOR_BUFFER_BIT,
    glMatrixMode, glLoadIdentity, glViewport,
    glBegin, glEnd, glVertex2f, glColor3f,
    GL_PROJECTION, GL_MODELVIEW, GL_TRIANGLES
)
from OpenGL.GLUT import (
    glutInit, glutInitDisplayMode, glutInitWindowSize, glutInitWindowPosition,
    glutCreateWindow, glutDisplayFunc, glutReshapeFunc, glutKeyboardFunc,
    glutMainLoop, glutSwapBuffers,glutLeaveMainLoop,
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


def keyboard(key: bytes, x: int, y: int) -> None:
    """Fecha com ESC."""
    if key == b'\x1b':  # ESC
        try:
            glutLeaveMainLoop()  # Funciona no FreeGLUT
        except Exception:
            os._exit(0)  # Saída imediata se glutLeaveMainLoop não existir

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

    # Primeira configuração de GL
    init_gl(800, 600)

    # Loop principal
    glutMainLoop()

if __name__ == "__main__":
    main()