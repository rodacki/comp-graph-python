"""Estrutura de armazenamento das primitivas da cena.

O `Modelo` atua como repositório simples para polígonos e círculos, usado
pelos estados para inserir objetos e pela view para iterar/renderizar.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .circulo import Circulo
from .poligono import Poligono


@dataclass
class Modelo:
    """Container principal das primitivas geométricas do editor."""

    _poligonos: list[Poligono] = field(default_factory=list)
    _circulos: list[Circulo] = field(default_factory=list)

    # API pública (read-only)
    @property
    def poligonos(self) -> list[Poligono]:
        """Lista de polígonos da cena.

        Returns:
            list[Poligono]: Referência à lista interna de polígonos.
        """
        return self._poligonos

    @property
    def circulos(self) -> list[Circulo]:
        """Lista de círculos da cena.

        Returns:
            list[Circulo]: Referência à lista interna de círculos.
        """
        return self._circulos

    # Mutadores explícitos
    def add_poligono(self, p: Poligono) -> None:
        """Adiciona um polígono ao modelo.

        Args:
            p: Polígono a ser incluído na cena.

        Returns:
            None: Atualiza coleção interna `_poligonos`.
        """
        self._poligonos.append(p)

    def add_circulo(self, c: Circulo) -> None:
        """Adiciona um círculo ao modelo.

        Args:
            c: Círculo a ser incluído na cena.

        Returns:
            None: Atualiza coleção interna `_circulos`.
        """
        self._circulos.append(c)

    def draw(self) -> None:
        """Método legado sem uso no pipeline atual.

        Returns:
            None: Mantido para compatibilidade com versões anteriores.
        """
        pass
