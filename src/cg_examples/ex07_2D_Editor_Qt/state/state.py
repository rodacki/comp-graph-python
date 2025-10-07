# from OpenGL.GLUT import (
#     GLUT_LEFT_BUTTON,
#     GLUT_DOWN,
#     glutPostRedisplay, 
#     glutDestroyWindow, 
# )
# from abc import ABC, abstractmethod
# #from ..globals.settings import settings
# from ..model.circulo import Circulo
# from ..model.ponto import Ponto
# from ..model.poligono import Poligono
# from ..model.modelo import Modelo
# from ..state.idleState import IdleState
# from ..state.initCircleState import InitCircleState
# from ..state.endCircleState import EndCircleState
# from ..state.initPolygonState import InitPolygonState
# from ..state.addPolygonPointState import AddPointPolygonState
# from typing import Type
# import math

# # abstract state class
# class State(ABC):

#     @abstractmethod
#     def mouse(self, button, state, x, y):
#         pass

#     @abstractmethod
#     def keyboard(self, key, x, y):
#         pass

#     @abstractmethod
#     def motion(self, x, y):
#         pass
    
#     @abstractmethod
#     def passiveMotion(self, x, y):
#         pass

# class Context:
#     def __init__(self, window) -> None:
#         self.__idleState = IdleState(self)
#         self.__initCircleState = InitCircleState(self)
#         self.__endCircleState = EndCircleState(self)
#         self.__initPolygonState = InitPolygonState(self)
#         self.__addPointPolygonState = AddPointPolygonState(self)
#         self.__window = window

#         self.__currentState = self.__idleState

#     @property
#     def currentState(self):
#         return self.__currentState
    
#     @currentState.setter
#     def currentState(self, newState):
#         self.__currentState = newState

#     @property
#     def idleState(self):
#         return self.__idleState
    
#     @property
#     def initCircleState(self):
#         return self.__initCircleState
    
#     @property
#     def EndCircleState(self):
#         return self.__endCircleState
    
#     def setCurrentState(self, state: Type[State]):
#         self.__currentState = state

#     def getCurrentState(self):
#         return self.__currentState

#     def mouse(self, button, state, x, y):
#         self.currentState.mouse(button, state, x, y)

#     def keyboard(self, key, x, y):
#         if key.decode() == chr(27): 
#             glutDestroyWindow(self.__window)
#             print("Exit")

#         self.currentState.keyboard(key,x,y)
    

#     def motion(self, x, y):
#         self.currentState.motion(x, y)
    
        
#     def passiveMotion(self, x, y):
#         self.currentState.passiveMotion(x, y)




# class IdleState(State):

#     def __init__(self, context: Type[Context]) -> None:
#         super().__init__()
#         self.__context = context

#     @property
#     def context(self):
#         return self.__context
    
#     @context.setter
#     def context(self, newcontext):
#         self.__context = newcontext


#     def mouse(self, button, state, wx, wy):
#         glutPostRedisplay()
        
    
#     def keyboard(self, key, x, y):
#         print("IdleState.keyboard()")
#         if key.decode() == "i":
#             self.context.currentState = self.context.initCircleState


    
#     def motion(self):
#         pass
    
        
#     def passiveMotion(self):
#         pass

# class InitCircleState(State):

#     def __init__(self, context: Type[Context]) -> None:
#         super().__init__()
#         self.__context = context

#     @property
#     def context(self):
#         return self.__context
    
#     @context.setter
#     def context(self, newcontext):
#         self.context = newcontext

#     def mouse(self, button, state, wx, wy):
#         if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
#             print("criando circulo")
#             settings.circulo = Circulo()
#             #settings.circulo.xc = wx
#             #settings.circulo.yc = wy
#             self.context.currentState = self.context.EndCircleState
        
    
#     def keyboard(self, key, x, y):
#         print("InitCircleState.keyboard()")
#         pass

    
#     def motion(self):
#         pass


#     def passiveMotion(self):
#         pass
    
# class EndCircleState(State):

#     def __init__(self, context: Type[Context]) -> None:
#         super().__init__()
#         self.__context = context

#     @property
#     def context(self):
#         return self.__context
    
#     @context.setter
#     def xc(self, newcontext):
#         self.__context = newcontext

#     def mouse(self, button, state, wx, wy):
#         if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
#             print("encerrando circulo")
#             #raio = math.sqrt((p.x-settings.circulo.xc)**2 + (p.y-settings.circulo.yc)**2)
#             #settings.circulo.raio = raio
#             #settings.modelo.addCirculo(settings.circulo)
#             self.context.currentState = self.context.idleState
#         pass

    
#     def keyboard(self, key, x, y):
#         print("EndCircleState.keyboard()")
        


#     def motion(self):
#         pass


#     def passiveMotion(self):
#         pass