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


# def apply_translation(objs: Iterable[object], dx: float, dy: float) -> None:
#     """Aplica translação relativa ao snapshot inicial."""
#     # circles
#     for item in snap:
#         if isinstance(item, _CircleSnapshot):
#             item.obj.xc = item.xc + dx
#             item.obj.yc = item.yc + dy
#         else:
#             poly = item.obj
#             for p, (x0, y0) in zip(poly.pontos, item.pontos, strict=False):
#                 p.x, p.y = x0 + dx, y0 + dy


def apply_translation(objs: Iterable[object], dx: float, dy: float) -> None:
    for o in objs:
        if isinstance(o, Circulo):
            o.xc += dx
            o.yc += dy
        elif isinstance(o, Poligono):
            for p in o.pontos:
                p.x += dx
                p.y += dy


# def apply_scale(
#     objs: Iterable[object],
#     sx: float,
#     sy: float,
#     pivot: Ponto,
# ) -> None:
#     """Escala relativa ao snapshot, em torno do pivô."""
#     cx, cy = pivot.x, pivot.y
#     for item in objs:
#         if isinstance(item, Circulo):
#             # centro escala como ponto; raio escala pelo fator médio |sx,sy|
#             item.obj.xc = cx + (item.xc - cx) * sx
#             item.obj.yc = cy + (item.yc - cy) * sy
#             # fator de escala do raio (média geométrica simples)
#             r_scale = (abs(sx) * abs(sy)) ** 0.5
#             item.obj.raio = item.raio * r_scale
#         else:
#             poly = item.obj
#             for p, (x0, y0) in zip(poly.pontos, item.pontos, strict=False):
#                 p.x = cx + (x0 - cx) * sx
#                 p.y = cy + (y0 - cy) * sy


def apply_scale(objs: Iterable[object], sx: float, sy: float, pivot: Ponto) -> None:
    for o in objs:
        if isinstance(o, Circulo):
            # escala uniforme em círculos: raio * média geométrica
            import math

            s = math.sqrt(abs(sx * sy))
            o.raio *= s
            # re-posiciona centro se quiser escalar em relação ao pivot:
            o.xc = pivot.x + (o.xc - pivot.x) * sx
            o.yc = pivot.y + (o.yc - pivot.y) * sy
        elif isinstance(o, Poligono):
            for p in o.pontos:
                p.x = pivot.x + (p.x - pivot.x) * sx
                p.y = pivot.y + (p.y - pivot.y) * sy


# def apply_rotation(
#     objs: Iterable[object],
#     snap: Snapshot,
#     angle: float,
#     pivot: Ponto,
# ) -> None:
#     """Rotação relativa ao snapshot, em torno do pivô (radianos)."""
#     cx, cy = pivot.x, pivot.y
#     for item in snap:
#         if isinstance(item, _CircleSnapshot):
#             x, y = _rotate_point(item.xc, item.yc, cx, cy, angle)
#             item.obj.xc, item.obj.yc = x, y
#             # raio invariante na rotação
#         else:
#             poly = item.obj
#             for p, (x0, y0) in zip(poly.pontos, item.pontos, strict=False):
#                 p.x, p.y = _rotate_point(x0, y0, cx, cy, angle)


def apply_rotation(objs: Iterable[object], ang: float, pivot: Ponto) -> None:
    import math

    c, s = math.cos(ang), math.sin(ang)
    for o in objs:
        if isinstance(o, Circulo):
            # rotacionar círculo muda apenas o centro (raio é invariante)
            dx, dy = o.xc - pivot.x, o.yc - pivot.y
            o.xc = pivot.x + (dx * c - dy * s)
            o.yc = pivot.y + (dx * s + dy * c)
        elif isinstance(o, Poligono):
            for p in o.pontos:
                dx, dy = p.x - pivot.x, p.y - pivot.y
                p.x = pivot.x + (dx * c - dy * s)
                p.y = pivot.y + (dx * s + dy * c)


def angle_from(pivot: Ponto, start: Ponto, curr: Ponto) -> float:
    """Ângulo (rad) entre os vetores pivot->start e pivot->curr."""
    x0, y0 = start.x - pivot.x, start.y - pivot.y
    x1, y1 = curr.x - pivot.x, curr.y - pivot.y
    a0 = atan2(y0, x0)
    a1 = atan2(y1, x1)
    return a1 - a0


def scale_from_vectors(
    pivot: Ponto,
    start: Ponto,
    curr: Ponto,
    axis: str | None,  # "x" | "y" | None (uniform)
) -> tuple[float, float]:
    """Retorna (sx, sy) a partir do alongamento do vetor pivot->mouse."""
    vx0, vy0 = start.x - pivot.x, start.y - pivot.y
    vx1, vy1 = curr.x - pivot.x, curr.y - pivot.y

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
