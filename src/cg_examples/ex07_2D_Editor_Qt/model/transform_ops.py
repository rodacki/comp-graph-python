# src/cg_examples/ex07_2D_Editor_Qt/model/transform_ops.py
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from math import atan2, cos, hypot, sin

from .circulo import Circulo
from .poligono import Poligono
from .ponto import Ponto


@dataclass
class _CircleSnapshot:
    obj: Circulo
    xc: float
    yc: float
    raio: float


@dataclass
class _PolySnapshot:
    obj: Poligono
    pontos: list[tuple[float, float]]  # original


Snapshot = list[_CircleSnapshot | _PolySnapshot]


def snapshot_selection(objs: Iterable[object]) -> Snapshot:
    snap: Snapshot = []
    for o in objs:
        if isinstance(o, Circulo):
            snap.append(_CircleSnapshot(o, o.xc, o.yc, o.raio))
        elif isinstance(o, Poligono):
            snap.append(_PolySnapshot(o, [(p.x, p.y) for p in o.pontos]))
    return snap


def restore_snapshot(snap: Snapshot) -> None:
    for item in snap:
        if isinstance(item, _CircleSnapshot):
            item.obj.xc = item.xc
            item.obj.yc = item.yc
            item.obj.raio = item.raio
        else:
            poly = item.obj
            orig = item.pontos
            for p, (x0, y0) in zip(poly.pontos, orig, strict=False):
                p.x, p.y = x0, y0


def _rotate_point(px: float, py: float, cx: float, cy: float, ang: float) -> tuple[float, float]:
    sx, sy = px - cx, py - cy
    c, s = cos(ang), sin(ang)
    return (cx + c * sx - s * sy, cy + s * sx + c * sy)


def apply_translation(objs: Iterable[object], snap: Snapshot, dx: float, dy: float) -> None:
    """Aplica translação relativa ao snapshot inicial."""
    # circles
    for item in snap:
        if isinstance(item, _CircleSnapshot):
            item.obj.xc = item.xc + dx
            item.obj.yc = item.yc + dy
        else:
            poly = item.obj
            for p, (x0, y0) in zip(poly.pontos, item.pontos, strict=False):
                p.x, p.y = x0 + dx, y0 + dy


def apply_scale(
    objs: Iterable[object],
    snap: Snapshot,
    sx: float,
    sy: float,
    pivot: Ponto,
) -> None:
    """Escala relativa ao snapshot, em torno do pivô."""
    cx, cy = pivot.x, pivot.y
    for item in snap:
        if isinstance(item, _CircleSnapshot):
            # centro escala como ponto; raio escala pelo fator médio |sx,sy|
            item.obj.xc = cx + (item.xc - cx) * sx
            item.obj.yc = cy + (item.yc - cy) * sy
            # fator de escala do raio (média geométrica simples)
            r_scale = (abs(sx) * abs(sy)) ** 0.5
            item.obj.raio = item.raio * r_scale
        else:
            poly = item.obj
            for p, (x0, y0) in zip(poly.pontos, item.pontos, strict=False):
                p.x = cx + (x0 - cx) * sx
                p.y = cy + (y0 - cy) * sy


def apply_rotation(
    objs: Iterable[object],
    snap: Snapshot,
    angle: float,
    pivot: Ponto,
) -> None:
    """Rotação relativa ao snapshot, em torno do pivô (radianos)."""
    cx, cy = pivot.x, pivot.y
    for item in snap:
        if isinstance(item, _CircleSnapshot):
            x, y = _rotate_point(item.xc, item.yc, cx, cy, angle)
            item.obj.xc, item.obj.yc = x, y
            # raio invariante na rotação
        else:
            poly = item.obj
            for p, (x0, y0) in zip(poly.pontos, item.pontos, strict=False):
                p.x, p.y = _rotate_point(x0, y0, cx, cy, angle)


def angle_from(pivot: Ponto, start: tuple[float, float], curr: tuple[float, float]) -> float:
    """Ângulo (rad) entre os vetores pivot->start e pivot->curr."""
    x0, y0 = start[0] - pivot.x, start[1] - pivot.y
    x1, y1 = curr[0] - pivot.x, curr[1] - pivot.y
    a0 = atan2(y0, x0)
    a1 = atan2(y1, x1)
    return a1 - a0


def scale_from_vectors(
    pivot: Ponto,
    start: tuple[float, float],
    curr: tuple[float, float],
    axis: str | None,  # "x" | "y" | None (uniform)
) -> tuple[float, float]:
    """Retorna (sx, sy) a partir do alongamento do vetor pivot->mouse."""
    vx0, vy0 = start[0] - pivot.x, start[1] - pivot.y
    vx1, vy1 = curr[0] - pivot.x, curr[1] - pivot.y

    if axis == "x":
        sx = (vx1 if vx0 != 0 else 1.0) / (vx0 if vx0 != 0 else 1.0)
        return (sx, 1.0)
    if axis == "y":
        sy = (vy1 if vy0 != 0 else 1.0) / (vy0 if vy0 != 0 else 1.0)
        return (1.0, sy)

    # uniforme: razão de normas
    n0 = max(hypot(vx0, vy0), 1e-9)
    n1 = max(hypot(vx1, vy1), 1e-9)
    s = n1 / n0
    return (s, s)
