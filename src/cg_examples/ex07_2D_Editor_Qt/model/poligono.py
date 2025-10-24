from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..utils.floatcmp import Tol, ae, age, agt, ale, ane

# Importa sua classe Ponto, que deve ter atributos x e y (float)
from .ponto import Ponto

if TYPE_CHECKING:
    pass


@dataclass
class Poligono:
    """Representa um polígono composto por pontos no plano."""

    pontos: list[Ponto] = field(default_factory=list)
    selected: bool = False  # flag para objeto selecionado pelo usuário

    @property
    def last_point(self) -> Ponto | None:
        """Retorna o último ponto do polígono, se existir."""
        return self.pontos[-1] if self.pontos else None

    def add_ponto(self, ponto: Ponto) -> None:
        """Adiciona um novo ponto ao polígono."""
        self.pontos.append(ponto)

    def bounding_box(self) -> tuple[Ponto, Ponto]:
        xs = [p.x for p in self.pontos]
        ys = [p.y for p in self.pontos]
        p1 = Ponto(min(xs), min(ys))
        p2 = Ponto(max(xs), max(ys))
        return p1, p2

    def hit_test(self, xw: float, yw: float, tol_world: float) -> bool:
        tol = Tol.abs_only(tol_world)  # criando objeto para comparacao de floats
        x_sel = xw
        y_sel = yw
        n_int = 0
        n = len(self.pontos)
        for i in range(n):
            p1 = self.pontos[i]
            p2 = self.pontos[(i + 1) % n]
            if ane(p1.y, p2.y, tol):  # lado não horizontal
                t_int = (y_sel - p1.y) / (p2.y - p1.y)
                x_int = p1.x + t_int * (p2.x - p1.x)
                y_int = y_sel
                if ae(x_int, x_sel, tol) and t_int >= 0.0 and t_int <= 1.0:
                    return True
                elif (
                    agt(x_int, x_sel, tol)
                    and agt(y_int, min(p1.y, p2.y), tol)
                    and ale(y_int, max(p1.y, p2.y), tol)
                ):
                    n_int += 1
            elif (
                ae(y_sel, p1.y, tol)
                and age(x_sel, min(p1.x, p2.x), tol)
                and ale(x_sel, max(p1.x, p2.x), tol)
            ):
                return True

        return (n_int % 2) != 0
