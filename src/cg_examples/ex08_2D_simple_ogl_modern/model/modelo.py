"""Repositório de segmentos da cena 2D."""

from dataclasses import dataclass, field

from .segmento import Segmento


@dataclass
class Modelo:
    """Armazena os segmentos criados pelo usuário."""

    _segmentos: list[Segmento] = field(default_factory=list)

    @property
    def segmentos(self) -> list[Segmento]:
        """Retorna lista de segmentos da cena.

        Returns:
            list[Segmento]: Referência da lista interna de segmentos.
        """
        return self._segmentos

    def add_segmento(self, segmento: Segmento) -> None:
        """Adiciona um segmento ao modelo.

        Args:
            segmento: Segmento de reta a ser armazenado.

        Returns:
            None: Atualiza a coleção interna de segmentos.
        """
        self._segmentos.append(segmento)
