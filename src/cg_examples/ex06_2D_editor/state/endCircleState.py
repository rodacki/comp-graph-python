from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, 
    GL_DEPTH_BUFFER_BIT, 
    glClear, 
    glLoadIdentity, 
    glColor3f,
)
from OpenGL.GLUT import (
    GLUT_LEFT_BUTTON, 
    GLUT_DOWN, 
    glutSwapBuffers,
)
from .abstractState import State
from ..view.draw_utils import getWorldCoords
from ..view.draw_utils import axis
import math

class EndCircleState(State):

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
            xc = self.context.global_vars.circulo.xc
            yc = self.context.global_vars.circulo.yc
            raio = math.sqrt((wx-xc)**2 + (wy-yc)**2)
            self.context.global_vars.circulo.raio = raio
            self.context.global_vars.modelo.addCirculo(self.context.global_vars.circulo)
            self.context.global_vars.circulo = None
            self.context.currentState = self.context.idleState
            
        pass

    
    def keyboard(self, key, x, y):
        pass
        


    def motion(self, x, y):
        pass


    def passiveMotion(self, x, y):
        if self.context.global_vars.circulo != None:
            wx, wy = getWorldCoords(self.context, x, y)
            xc = self.context.global_vars.circulo.xc
            yc = self.context.global_vars.circulo.yc
            raio = math.sqrt((wx-xc)**2 + (wy-yc)**2)
            self.context.global_vars.circulo.raio = raio
            
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # type: ignore
        glLoadIdentity()
        axis(self.context)
        glColor3f(1.0, 0.0, 3.0)
        self.context.global_vars.modelo.draw()
        self.context.global_vars.circulo.drawOpen()
        glutSwapBuffers()