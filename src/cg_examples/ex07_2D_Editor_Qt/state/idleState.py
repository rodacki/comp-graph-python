from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, 
    GL_DEPTH_BUFFER_BIT, 
    glClear, 
    glLoadIdentity, 
    glColor3f,
    glGetIntegerv,
    GL_VIEWPORT
)
# from OpenGL.GLUT import (
#     glutSwapBuffers,
# )
from .abstractState import State
from ..view.draw_utils import getWorldCoords
from ..view.draw_utils import axis
from PyQt5.QtGui import QMouseEvent, QKeyEvent


class IdleState(State):

    def __init__(self, context) -> None:
        super().__init__(context)
        #self.__context = context

    
    @property
    def context(self):
        return super().context
    
    @context.setter
    def context(self, newcontext):
        super().context = newcontext


    # def mouse(self, button, state, x, y):
    #     #glutPostRedisplay()
    #     pass
    
    def keyboard(self, key, x, y):
        if key.decode() == "i":
            self.context.currentState = self.context.initCircleState
        elif key.decode() == "p":
            self.context.currentState = self.context.initPolygonState

    # def motion(self, x, y):
    #     pass
    
        
    # def passiveMotion(self, x, y):
    #     pass

    def display(self):
        #from globals.settings import modelo
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # type: ignore
        glLoadIdentity()
        
        axis(self.context)
        glColor3f(1.0, 0.0, 3.0)
        #if gui_state.currentState == FiniteState.ADD_POINT:
        #settings.poligono.drawOpen()
        self.context.global_vars.modelo.draw()
        #modelo.draw()
        #glutSwapBuffers()

    def mousePressEvent(self, event: QMouseEvent):
        print("Canvas:", event.x(), event.y())
        viewport = glGetIntegerv(GL_VIEWPORT)
        print("Viewport:", viewport)
        x, y = getWorldCoords(self.context, event.x(), event.y())
        print("World : ", x, y)

    def mouseMoveEvent(self, event: QMouseEvent):
        pass
