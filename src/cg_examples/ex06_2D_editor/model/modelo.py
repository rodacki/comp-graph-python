from .poligono import Poligono
from .circulo import Circulo

# ----------------------------------------------------- #
# Classe Modelo: agrega todas as entidades gráficas     #
# ----------------------------------------------------- #
class Modelo:
    def __init__(self):
        self._poligonos = []
        self._circulos = []

    def addPoligono(self, poligono):
        self._poligonos.append(poligono)

    def addCirculo(self, circulo):
        self._circulos.append(circulo)

    def draw(self):
        for p in self._poligonos:
            p.draw()
        for c in self._circulos:
            c.draw()