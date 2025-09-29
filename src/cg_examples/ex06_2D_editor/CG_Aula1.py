from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# inicializar camera/ambiente/modelo
def init():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-10.0, 50.0, -10.0, 50.0, -1.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# ----------------------------------------------------- #
# Callback de redesenho de tela                         #
# ----------------------------------------------------- #
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    

    #desenho do eixo x
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(-8.0, 0.0)
    glVertex2f(8.0, 0.0)
    glEnd()


    #desenho do eixo x
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(0.0, -8.0)
    glVertex2f(0.0, 8.0)
    glEnd()

    # desenho de uma linha
    glColor3f(1.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex2f(-5.0, -5.0)
    glVertex2f(5.0, 5.0)
    glEnd()

    glutSwapBuffers()

# ----------------------------------------------------- #
# Funcao principal do programa                          #
# ----------------------------------------------------- #
def main():
    global wind
    glutInit()
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow("IFC - BCC - CG - 2024")
    glutDisplayFunc(showScreen)
    init()
    glutMainLoop()
    
if __name__ == "__main__":
    main()
