# utils/floatcmp.py
"""Utilitários de comparação robusta de números de ponto flutuante.

Este módulo evita decisões geométricas instáveis por erro numérico,
fornecendo operadores aproximados e tolerâncias configuráveis.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Tol:
    """Configurações de tolerância numérica.

    - abs_: tolerância absoluta (mesma unidade de a/b)
    - rel:  tolerância relativa (fração de max(|a|,|b|)); útil quando valores crescem
    """

    abs_: float = 0.0
    rel: float = 0.0

    @staticmethod
    def abs_only(eps: float) -> Tol:
        """Cria tolerância apenas absoluta.

        Args:
            eps: Tolerância absoluta desejada.

        Returns:
            Tol: Instância com `abs_=eps` e `rel=0.0`.
        """
        return Tol(abs_=eps, rel=0.0)


def _mix_tol(a: float, b: float, tol: Tol) -> float:
    """Combina tolerâncias absoluta e relativa no estilo `isclose`.

    Args:
        a: Primeiro valor comparado.
        b: Segundo valor comparado.
        tol: Configuração de tolerâncias.

    Returns:
        float: Tolerância combinada efetiva para o par `(a, b)`.
    """
    return max(tol.abs_, tol.rel * max(abs(a), abs(b)))


# ---------- Igualdade / diferença aproximadas ----------


def ae(a: float, b: float, tol: Tol) -> bool:
    """Compara igualdade aproximada entre dois valores.

    Args:
        a: Primeiro valor.
        b: Segundo valor.
        tol: Configuração de tolerâncias.

    Returns:
        bool: `True` quando `a` e `b` são aproximadamente iguais.
    """
    return math.isclose(a, b, rel_tol=tol.rel, abs_tol=tol.abs_)


def ane(a: float, b: float, tol: Tol) -> bool:
    """Compara diferença aproximada entre dois valores.

    Args:
        a: Primeiro valor.
        b: Segundo valor.
        tol: Configuração de tolerâncias.

    Returns:
        bool: `True` quando `a` e `b` não são aproximadamente iguais.
    """
    return not ae(a, b, tol)


# ---------- Ordenação aproximada ----------
# A semântica é:
#   - alt(a,b):  a <  b considerando que 'b - a' deve ser maior que tol combinado
#   - ale(a,b):  a <= b ~ (a < b) or (a ~= b)
#   - agt/age:   análogos para > e >=


def alt(a: float, b: float, tol: Tol) -> bool:
    """Compara `a < b` com tolerância numérica.

    Args:
        a: Primeiro valor.
        b: Segundo valor.
        tol: Configuração de tolerâncias.

    Returns:
        bool: `True` quando `b - a` excede tolerância combinada.
    """
    return (b - a) > _mix_tol(a, b, tol)


def ale(a: float, b: float, tol: Tol) -> bool:
    """Compara `a <= b` com tolerância numérica.

    Args:
        a: Primeiro valor.
        b: Segundo valor.
        tol: Configuração de tolerâncias.

    Returns:
        bool: `True` quando `a < b` aproximado ou `a ~= b`.
    """
    return alt(a, b, tol) or ae(a, b, tol)


def agt(a: float, b: float, tol: Tol) -> bool:
    """Compara `a > b` com tolerância numérica.

    Args:
        a: Primeiro valor.
        b: Segundo valor.
        tol: Configuração de tolerâncias.

    Returns:
        bool: `True` quando `a - b` excede tolerância combinada.
    """
    return (a - b) > _mix_tol(a, b, tol)


def age(a: float, b: float, tol: Tol) -> bool:
    """Compara `a >= b` com tolerância numérica.

    Args:
        a: Primeiro valor.
        b: Segundo valor.
        tol: Configuração de tolerâncias.

    Returns:
        bool: `True` quando `a > b` aproximado ou `a ~= b`.
    """
    return agt(a, b, tol) or ae(a, b, tol)


# ---------- Utilitários 2D comuns em CG ----------


def dist2(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calcula distância ao quadrado entre dois pontos 2D.

    Args:
        x1: Coordenada X do primeiro ponto.
        y1: Coordenada Y do primeiro ponto.
        x2: Coordenada X do segundo ponto.
        y2: Coordenada Y do segundo ponto.

    Returns:
        float: Distância ao quadrado entre os pontos.
    """
    dx, dy = (x1 - x2), (y1 - y2)
    return dx * dx + dy * dy


def within(a: float, b: float, tol: Tol) -> bool:
    """Alias legível para comparação de igualdade aproximada.

    Args:
        a: Primeiro valor.
        b: Segundo valor.
        tol: Configuração de tolerâncias.

    Returns:
        bool: Mesmo resultado de `ae(a, b, tol)`.
    """
    return ae(a, b, tol)
