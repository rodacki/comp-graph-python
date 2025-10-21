from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
    glColor3f, glLoadIdentity, glClear,
)

from .abstractState import State
from ..view.draw_utils import getWorldCoords
from ..view.draw_utils import axis
from ..model.poligono import Poligono
from ..model.ponto import Ponto
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt

class InitPolygonState(State):

    def __init__(self, context) -> None:
        super().__init__(context)

    @property
    def context(self):
        return super().context
    
    @context.setter
    def context(self, newcontext):
        super().context = newcontext

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            print("Iniciando poligono")
            wx, wy = getWorldCoords(self.context, event.x(), event.y())
            p = Ponto(wx, wy)
            poligono = Poligono()
            poligono.addPonto(p)
            
            self.context.global_vars.poligono = poligono
            self.context.currentState = self.context.addPolygonPointState
            

    def mouseMoveEvent(self, event):
        pass
    
    def keyboard(self, key, x, y):
        print("InitPolygonState.keyboard()")
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # type: ignore
        glLoadIdentity()
        
        axis(self.context)
        glColor3f(1.0, 0.0, 3.0)
        self.context.global_vars.modelo.draw()
