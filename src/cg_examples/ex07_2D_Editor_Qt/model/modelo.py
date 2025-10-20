
from __future__ import annotations
from typing import List
from .poligono import Poligono
from .circulo import Circulo

# ----------------------------------------------------- #
# Classe Modelo: agrega todas as entidades gráficas     #
# ----------------------------------------------------- #
class Modelo:
    def __init__(self):
        self._poligonos: List["Poligono"] = []
        self._circulos: List["Circulo"] = []

    # --- mutação ---
    def addPoligono(self, poligono: "Poligono") -> None:
        self._poligonos.append(poligono)

    def addCirculo(self, circulo: "Circulo") -> None:
        self._circulos.append(circulo)

    # --- acesso somente-leitura ---
    @property
    def poligonos(self) -> List["Poligono"]:
        return self._poligonos

    @property
    def circulos(self) -> List["Circulo"]:
        return self._circulos

    def draw(self):
        for p in self._poligonos:
            p.draw()
        for c in self._circulos:
            c.draw()

