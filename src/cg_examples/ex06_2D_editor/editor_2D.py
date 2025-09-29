from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from enum import Enum
from state.context import Context
from globals.settings import GlobalDefinitions
from view.draw_utils import init


# ----------------------------------------------------- #
#  Global variables                                     #
# ----------------------------------------------------- #
globalVars = GlobalDefinitions()
stateContext =  Context(globalVars)

# ----------------------------------------------------- #
# Callback de redesenho de tela                         #
# ----------------------------------------------------- #
def showScreen():
    stateContext.display()
   
# ----------------------------------------------------- #
# Callback de alteracao do tamanho da janela            #
# ----------------------------------------------------- #
def reshape(width, height):
    stateContext.reshape(width, height)

# ----------------------------------------------------- #
# Callback de eventos de teclado                        #
# ----------------------------------------------------- #   
def onKeyboard(key, x, y):
    #print(key, type(key))
    stateContext.keyboard(key, x, y)
    
# ----------------------------------------------------- #
# Callback de eventos click de mouse                    #
# ----------------------------------------------------- #      
def onMouseButton(button, state, x,y):
    stateContext.mouse(button, state, x,y)
       
# ----------------------------------------------------- #
# Callback de movimento de mouse com botao              #
# ----------------------------------------------------- #      
def mouseMotion(x,y):
    stateContext.motion(x,y)

# ----------------------------------------------------- #
# Callback de movimento de mouse sem botao              #
# ----------------------------------------------------- #      
def passiveMotion(x,y):
    stateContext.passiveMotion(x,y)


# ----------------------------------------------------- #
# Funcao principal do programa                          #
# ----------------------------------------------------- #
def main():
    glutInit()
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("IFC - BCC - CG - 2024")
    stateContext.global_vars.wind = window
    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)
    glutKeyboardFunc(onKeyboard)
    glutMouseFunc(onMouseButton)
    glutReshapeFunc(reshape)
    glutMotionFunc(mouseMotion)
    glutPassiveMotionFunc(passiveMotion)
    init(stateContext)
    glutMainLoop()
    
    
if __name__ == "__main__":
    main()
