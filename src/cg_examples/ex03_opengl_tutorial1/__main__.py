from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

left = -10.0
right = 10.0
bottom = -10.0
top = 10.0


w, h = 500, 500


def configure_visualization():
    # estabelece a viewport
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # configura window (configura camera)
    glOrtho(left, right, bottom, top, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def onReshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(left, right, bottom, top, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    return


def showScreen():
    # limpa cor e profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # glLoadIdentity()
    configure_visualization()
    # configurando cor de desenho - vermelho
    glColor3f(1.0, 0.0, 0.0)
    # desenha eixo x
    glBegin(GL_LINES)
    glVertex2f(-8.0, 0.0)
    glVertex2f(8.0, 0.0)
    glEnd()
    # desemnha eixo y
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(0.0, -8.0)
    glVertex2f(0.0, 8.0)
    glEnd()
    # desenha quadrado
    # cor amarela
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(-2.0, -2.0)
    glVertex2f(-7.0, -2.0)
    glVertex2f(-7.0, -7.0)
    glVertex2f(-2.0, -7.0)
    glEnd()

    glutSwapBuffers()


def onKeyboard(key, x, y) -> None:
    """Fecha com ESC."""
    print(key, type(key))
    if key == b"\x1b":  # ESC
        try:
            glutLeaveMainLoop()  # Funciona no FreeGLUT
        except Exception:
            os._exit(0)  # Saída imediata se glutLeaveMainLoop não existir


def main():
    global wind

    # inicializa GLUT
    glutInit()
    print(chr(27))
    # dimensoes iniciais do canvas em pixels (tela)
    glutInitWindowSize(500, 500)
    # posicao inicial da minha aplicacao na tela
    glutInitWindowPosition(0, 0)
    # titulo na aplicacao
    wind = glutCreateWindow("Ex02 - GLUT Tutorial 1")
    # registro da funcao callback de redenho
    glutDisplayFunc(showScreen)
    # redesenho em estado idle
    # glutIdleFunc(showScreen)
    # registra eventos do teclado (por enquanto só ESC)
    glutKeyboardFunc(onKeyboard)

    glutReshapeFunc(onReshape)

    # dispara o loop de eventos
    glutMainLoop()


if __name__ == "__main__":
    main()
