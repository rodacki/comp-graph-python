from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, 
    GL_DEPTH_BUFFER_BIT,
    glColor3f, 
    glLoadIdentity, 
    glClear,
)
from OpenGL.GLUT import (
    glutSwapBuffers, 
    GLUT_LEFT_BUTTON, 
    GLUT_DOWN,
)
from .abstractState import State
from ..view.draw_utils import getWorldCoords
from ..view.draw_utils import axis
from ..model.circulo import Circulo

class InitCircleState(State):

    def __init__(self, context) -> None:
        super().__init__(context)   
       
        

    @property
    def context(self):
        return super().context
    
    @context.setter
    def context(self, newcontext):
        super().context = newcontext

    def mouse(self, button, state, x, y):
        
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            wx, wy = getWorldCoords(self.context, x, y)
            circulo = Circulo()
            circulo.xc = wx
            circulo.yc = wy
            self.context.global_vars.circulo = circulo
            self.context.currentState = self.context.endCircleState
            
    
    def keyboard(self, key, x, y):
        pass

    
    def motion(self, x, y):
        pass


    def passiveMotion(self, x, y):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # type: ignore
        glLoadIdentity()
        axis(self.context)
        glColor3f(1.0, 0.0, 3.0)
        self.context.global_vars.modelo.draw()
        glutSwapBuffers()
