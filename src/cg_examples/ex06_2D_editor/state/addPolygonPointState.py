from OpenGL.GL import ( 
    GL_COLOR_BUFFER_BIT, 
    GL_DEPTH_BUFFER_BIT,
    GL_ENABLE_BIT,
    GL_LINE_STIPPLE,
    GL_LINES,
    glColor3f, 
    glLoadIdentity, 
    glClear, 
    glPushAttrib,
    glLineStipple,
    glEnable,
    glBegin,
    glVertex2f,
    glEnd,
    glPopAttrib,
)
from OpenGL.GLUT import (
    glutSwapBuffers, 
    GLUT_LEFT_BUTTON, 
    GLUT_DOWN
)
from .abstractState import State
from ..view.draw_utils import getWorldCoords
from ..view.draw_utils import axis
from ..model.poligono import Poligono
from ..model.ponto import Ponto

class AddPointPolygonState(State):

    def __init__(self, context) -> None:
        super().__init__(context)
        self.__lastX = None
        self.__lastY = None
   
    @property
    def context(self):
        return super().context
    
    @context.setter
    def context(self, newcontext):
        super().context = newcontext

    def mouse(self, button, state, x, y):
        
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            wx, wy = getWorldCoords(self.context, x, y)
            print("Adicionando ponto")
            p = Ponto(wx, wy)
            self.context.global_vars.poligono.addPonto(p)

            
    def keyboard(self, key, x, y):
        if key.decode() == "o":
            print("Terminando poligono")
            self.context.global_vars.modelo.addPoligono(self.context.global_vars.poligono)
            self.context.global_vars.poligono = None
            self.context.currentState = self.context.idleState
        pass

    
    def motion(self, x, y):
        pass


    def passiveMotion(self, x, y):
        wx, wy = getWorldCoords(self.context, x, y)
        self.__lastX = wx
        self.__lastY = wy
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # type: ignore
        glLoadIdentity()
        
        axis(self.context)
        glColor3f(1.0, 0.0, 3.0)
        self.context.global_vars.modelo.draw()
        if self.context.global_vars.poligono != None:
            self.context.global_vars.poligono.drawOpen()
            x = self.context.global_vars.poligono.lastPoint.x
            y = self.context.global_vars.poligono.lastPoint.y
            if self.__lastX != None and self.__lastY != None:
                glPushAttrib(GL_ENABLE_BIT)
                glLineStipple(3, 0xAAAA)  # [1]
                glEnable(GL_LINE_STIPPLE)
                glBegin(GL_LINES)
                glVertex2f(x, y)
                glVertex2f(self.__lastX, self.__lastY)
                glEnd()
                glPopAttrib()
            
        glutSwapBuffers()
