# from __future__ import annotations
# from typing import List
# from .poligono import Poligono
# from .circulo import Circulo

# # ----------------------------------------------------- #
# # Classe Modelo: agrega todas as entidades gráficas     #
# # ----------------------------------------------------- #
# class Modelo:
#     def __init__(self):
#         self._poligonos: List["Poligono"] = []
#         self._circulos: List["Circulo"] = []

#     # --- mutação ---
#     def addPoligono(self, poligono: "Poligono") -> None:
#         self._poligonos.append(poligono)

#     def addCirculo(self, circulo: "Circulo") -> None:
#         self._circulos.append(circulo)

#     # --- acesso somente-leitura ---
#     @property
#     def poligonos(self) -> List["Poligono"]:
#         return self._poligonos

#     @property
#     def circulos(self) -> List["Circulo"]:
#         return self._circulos

#     def draw(self):
#         for p in self._poligonos:
#             p.draw()
#         for c in self._circulos:
#             c.draw()

# src/cg_examples/ex07_2D_Editor_Qt/model/modelo.py
from __future__ import annotations

from dataclasses import dataclass, field

from .circulo import Circulo
from .poligono import Poligono


@dataclass
class Modelo:
    _poligonos: list[Poligono] = field(default_factory=list)
    _circulos: list[Circulo] = field(default_factory=list)

    # API pública (read-only)
    @property
    def poligonos(self) -> list[Poligono]:
        return self._poligonos

    @property
    def circulos(self) -> list[Circulo]:
        return self._circulos

    # Mutadores explícitos
    def add_poligono(self, p: Poligono) -> None:
        self._poligonos.append(p)

    def add_circulo(self, c: Circulo) -> None:
        self._circulos.append(c)

    def draw(self):
        pass
