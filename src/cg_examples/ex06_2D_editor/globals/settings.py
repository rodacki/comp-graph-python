# arquivo para definicao de variaveis globais do projeto
from dataclasses import dataclass, field
from typing import Any, List, Optional
from ..model.modelo import Modelo

# ----------------------------------------------------- #
#  Global variables                                     #
# ----------------------------------------------------- #
@dataclass
class GlobalDefinitions():
    contents: List[Any] = field(default_factory=list)
    should_exit: bool = False
    left: float = -500.0
    right: float = 500.0
    bottom: float = -500.0
    top: float = 500.0
    w: int = 500
    h: int = 500
    wind: Optional[Any] = None
    poligono: Optional[Any] = None
    circulo: Optional[Any] = None
    modelo: Modelo = field(default_factory=Modelo)


# class GlobalDefinitions():
    
#     def __init__(self) -> None:
#         self.__contents = [],
#         self.__left = -500.0
#         self.__right = 500.0
#         self.__bottom = -500.0
#         self.__top = 500.0
#         self.__w = 500
#         self.__h = 500
#         self.__wind = None
#         self.__poligono = None
#         self.__circulo = None
#         self.__modelo = Modelo()

    # @property
    # def contents(self):
    #     return self.__contents
    
    # @property
    # def left(self):
    #     return self.__left
    
    # @left.setter
    # def left(self, newleft):
    #     self.__left = newleft

    # @property
    # def right(self):
    #     return self.__right
    
    # @right.setter
    # def right(self, newright):
    #     self.__right = newright

    # @property
    # def top(self):
    #     return self.__top
    
    # @top.setter
    # def top(self, newtop):
    #     self.__top = newtop
    
    # @property
    # def bottom (self):
    #     return self.__bottom 

    # @bottom .setter
    # def bottom(self, newbottom ):
    #     self.__bottom  = newbottom 

    # @property
    # def w(self):
    #     return self.__w

    # @w.setter
    # def w(self, neww):
    #     self.__w = neww
    
    # @property
    # def h(self):
    #     return self.__h

    # @h.setter
    # def h(self, newh):
    #     self.__h = newh

    # @property
    # def wind(self):
    #     return self.__wind

    # @wind.setter
    # def wind(self, newwind):
    #     self.__wind = newwind

    # @property
    # def poligono(self):
    #     return self.__poligono

    # @poligono.setter
    # def poligono(self, newpoligono):
    #     self.__poligono = newpoligono

    # @property
    # def circulo(self):
    #     return self.__circulo

    # @circulo.setter
    # def circulo(self, newcirculo):
    #     self.__circulo = newcirculo

    # @property
    # def modelo(self):
    #     return self.__modelo

    # @modelo.setter
    # def modelo(self, newmodelo):
    #     self.__modelo = newmodelo


    # s = "teste"

    # for i in range(len(s)):
    #     print(s[i])

    # for elemento in s:
    #     print(elemento)
    
