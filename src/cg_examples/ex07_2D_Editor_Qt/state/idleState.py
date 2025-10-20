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
from PyQt5.QtCore import Qt


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

    # def mousePressEvent(self, event: QMouseEvent):
    #     print("vvvvvvCanvas:", event.x(), event.y())
    #     viewport = glGetIntegerv(GL_VIEWPORT)
    #     print("Viewport:", viewport)
    #     x, y = getWorldCoords(self.context, event.x(), event.y())
    #     print("World : ", x, y)


    def mousePressEvent(self, event: QMouseEvent):
        print("IdleState: mouse pressed")
        xw, yw = getWorldCoords(self.context, event.x(), event.y())
        add = bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
        print(add)
        hit_obj = None
        # percorra “de trás pra frente”
        # círculos
        for c in reversed(self.context.global_vars.modelo.circulos):
            if c.hit_test(self.context, xw, yw):
                hit_obj = c
                break
        # polígonos (se ainda não bateu)
        if hit_obj is None:
            for p in reversed(self.context.global_vars.modelo.poligonos):
                if p.hit_test(self.context, xw, yw):
                    hit_obj = p
                    break

        if hit_obj is not None:
            print("Add to selection")
            self.context.select_object(hit_obj, additive=add)
        elif not add:
            print("Clear selection")
            self.context.clear_selection()

        self.context.canvas.update()


    def mouseMoveEvent(self, event: QMouseEvent):
        pass
