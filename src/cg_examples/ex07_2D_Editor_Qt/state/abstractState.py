
from OpenGL.GL import GL_PROJECTION, GL_MODELVIEW, glViewport, glLoadIdentity, glMatrixMode, glOrtho
from abc import ABC, abstractmethod
from PyQt5.QtGui import QMouseEvent

# abstract state class
class State(ABC):
    def __init__(self, context) -> None:
        super().__init__()
        self.__context = context

    @property
    def context(self):
        return self.__context
    
    @context.setter
    def context(self, newcontext):
        self.__context = newcontext

    @abstractmethod
    def mousePressEvent(self, event: QMouseEvent):
        pass

    @abstractmethod
    def mouseMoveEvent(self, event: QMouseEvent):
        pass

    @abstractmethod
    def keyboard(self, key: bytes, x: int, y: int):
        pass

    @abstractmethod
    def display(self):
        pass
    
    def reshape(self, width, height):
        right = self.__context.global_vars.right
        left = self.__context.global_vars.left
        bottom = self.__context.global_vars.bottom
        top = self.__context.global_vars.top
        # Evita a divisao por zero
        if (height == 0):
            height = 1
                           
        # Especifica as dimensões da Viewport
        glViewport(0, 0, width, height)

        # Inicializa o sistema de coordenadas
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        #glOrtho(left, right, bottom, top, -1.0, 1.0)
        #Estabelece a janela de seleção (left, right, bottom, top)
        if (width <= height): 
            glOrtho(left, right, bottom, top*height/width, -1.0, 1.0)
        else: 
            glOrtho(left, right*width/height, bottom, top, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


    