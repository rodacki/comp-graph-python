from OpenGL.GLUT import (
    glutDestroyWindow, 
    glutLeaveMainLoop,
)
from PyQt5.QtGui import QMouseEvent, QKeyEvent
from ..globals.settings import GlobalDefinitions
from .idleState import IdleState
from .initCircleState import InitCircleState
from .endCircleState import EndCircleState
from .initPolygonState import InitPolygonState
from .addPolygonPointState import AddPointPolygonState
from typing import Type
import os


# ----------------------------------------------------- #
#  Classe contexto do padrão de projetos State          #
# ----------------------------------------------------- #
class Context:
    def __init__(self, global_vars: GlobalDefinitions, canvas=None) -> None:
        self.__idleState = IdleState(self)
        self.__initCircleState = InitCircleState(self)
       # self.__endCircleState = EndCircleState(self)
        self.__initPolygonState = InitPolygonState(self)
        self.__addPolygonPointState = AddPointPolygonState(self)
        self.__global_vars = global_vars
        self.__currentState = self.__idleState
        self.canvas = canvas

    @property
    def currentState(self):
        return self.__currentState
    
    @currentState.setter
    def currentState(self, newState):
        self.__currentState = newState

    @property
    def global_vars(self):
        return self.__global_vars

    @property
    def idleState(self):
        return self.__idleState
    
    @property
    def initCircleState(self):
        return self.__initCircleState
    
    # @property
    # def endCircleState(self):
    #     return self.__endCircleState
    
    @property
    def initPolygonState(self):
        return self.__initPolygonState
    
    @property
    def addPolygonPointState(self):
        return self.__addPolygonPointState
    
    
    # ---------------------------------------------------------------- #
    #    Acoes (callbacks) a serem implementadas em cada estado da app #
    # ---------------------------------------------------------------- #
    # def mouse(self, button, state, x, y):
    #     self.currentState.mouse(button, state, x, y)

    # def keyboard(self, key, x, y):
    #     if key.decode() == chr(27): 
    #         self.global_vars.should_exit = True
    #         glutDestroyWindow(self.global_vars.wind)
    #         print("Exit")
    #         return

    #     self.currentState.keyboard(key,x,y)


    def keyboard(self, key: bytes, x: int, y: int) -> None:
        """Fecha com ESC."""
        if key == b'\x1b':  # ESC
            try:
                glutLeaveMainLoop()  # Funciona no FreeGLUT
            except Exception:
                os._exit(0)  # Saída imediata se glutLeaveMainLoop não existir
        self.currentState.keyboard(key,x,y)

    # def motion(self, x, y):
    #     self.currentState.motion(x, y)
    
        
    # def passiveMotion(self, x, y):
    #     self.currentState.passiveMotion(x,y)

    def display(self):
        if self.global_vars.should_exit:
            glutDestroyWindow(self.global_vars.wind)
            print("Testando exit")
            return
        self.currentState.display()

    def reshape(self, width, height):
        self.currentState.reshape(width, height)

    def mousePressEvent(self, event: QMouseEvent):
        self.currentState.mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.currentState.mouseMoveEvent(event)


