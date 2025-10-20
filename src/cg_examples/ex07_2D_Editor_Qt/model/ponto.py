# class Ponto:
#     def __init__(self,  x = 0.0, y = 0.0):
#         self._x = x
#         self._y = y
    
#     @property
#     def x(self):
#         return self._x
    
#     @x.setter
#     def x(self, novox):
#         self._x = novox
        
#     @property
#     def y(self):
#         return self._y
    
#     @y.setter
#     def y(self, novoy):
#         self._y = novoy
        
#     def __str__(self):
#         return "({:.2f}, {:.2f})".format(self._x, self._y)  
    
from dataclasses import dataclass

@dataclass
class Ponto:
    """Representa um ponto 2D no plano cartesiano."""
    x: float = 0.0
    y: float = 0.0

    def __str__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"