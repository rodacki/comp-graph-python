from enum import Enum

# ----------------------------------------------------- #
#  FiniteState class: para nomear estados de interacao  #
# ----------------------------------------------------- #
class FiniteState(Enum):
    NONE = 0
    CREATE_POLIGONO = 1
    END_POLIGONO = 2
    ADD_POINT = 3
    DELETE = 4
    INIT_CIRCULO = 5
    END_CIRCULO = 6

# ----------------------------------------------------- #
# State Manager Singleton: gerenciar eventos de teclado #
# ----------------------------------------------------- #
class StateManagerSingleton:

    _instance = None

    def __init__(self):
        self._currentState = FiniteState.NONE

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @property
    def currentState(self):
        return self._currentState
    
    @currentState.setter
    def yc(self, state):
        self._currentState = state  
    



class MouseInteractor ( object ):
    def __init__(self):
        self._gui_state = StateManagerSingleton.instance()

    @property
    def currentState(self):
        return self._gui_state.currentState
    
    @currentState.setter
    def currentState(self, state):
        self._gui_state.currentState = state
    
