# utils/floatcmp.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import math

@dataclass(frozen=True)
class Tol:
    """Configurações de tolerância numérica.

    - abs_: tolerância absoluta (mesma unidade de a/b)
    - rel:  tolerância relativa (fração de max(|a|,|b|)); útil quando valores crescem
    """
    abs_: float = 0.0
    rel: float = 0.0

    @staticmethod
    def abs_only(eps: float) -> "Tol":
        return Tol(abs_=eps, rel=0.0)

def _mix_tol(a: float, b: float, tol: Tol) -> float:
    """Combina tolerâncias absoluta e relativa no estilo isclose."""
    return max(tol.abs_, tol.rel * max(abs(a), abs(b)))

# ---------- Igualdade / diferença aproximadas ----------

def ae(a: float, b: float, tol: Tol) -> bool:
    """Approx Equal: a == b com tolerância."""
    return math.isclose(a, b, rel_tol=tol.rel, abs_tol=tol.abs_)

def ane(a: float, b: float, tol: Tol) -> bool:
    """Approx Not Equal: a != b respeitando tolerância."""
    return not ae(a, b, tol)

# ---------- Ordenação aproximada ----------
# A semântica é:
#   - alt(a,b):  a <  b considerando que 'b - a' deve ser maior que tol combinado
#   - ale(a,b):  a <= b ~ (a < b) or (a ~= b)
#   - agt/age:   análogos para > e >=

def alt(a: float, b: float, tol: Tol) -> bool:
    return (b - a) > _mix_tol(a, b, tol)

def ale(a: float, b: float, tol: Tol) -> bool:
    return alt(a, b, tol) or ae(a, b, tol)

def agt(a: float, b: float, tol: Tol) -> bool:
    return (a - b) > _mix_tol(a, b, tol)

def age(a: float, b: float, tol: Tol) -> bool:
    return agt(a, b, tol) or ae(a, b, tol)

# ---------- Utilitários 2D comuns em CG ----------

def dist2(x1: float, y1: float, x2: float, y2: float) -> float:
    """Distância ao quadrado (evita sqrt em comparações)."""
    dx, dy = (x1 - x2), (y1 - y2)
    return dx*dx + dy*dy

def within(a: float, b: float, tol: Tol) -> bool:
    """Alias legível para 'aproximadamente igual'."""
    return ae(a, b, tol)