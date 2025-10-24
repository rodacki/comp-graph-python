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
