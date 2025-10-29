# from __future__ import annotations

# from collections.abc import Iterable
# from math import hypot
# from typing import TYPE_CHECKING

# from OpenGL.GL import (
#     GL_ENABLE_BIT,
#     GL_LINE_LOOP,
#     GL_LINE_STIPPLE,
#     GL_QUADS,
#     glBegin,
#     glColor3f,
#     glEnable,
#     glEnd,
#     glLineStipple,
#     glLineWidth,
#     glPopAttrib,
#     glPushAttrib,
#     glVertex2f,
# )

# from ..model.circulo import Circulo
# from ..model.poligono import Poligono
# from ..model.ponto import Ponto
# from .draw_utils import px_to_world
# from ..state.transform_mode import TransformMode

# if TYPE_CHECKING:
#     from ..state.context import Context


# def _draw_handle_square(cx: float, cy: float, half: float) -> None:
#     glBegin(GL_QUADS)
#     glVertex2f(cx - half, cy - half)
#     glVertex2f(cx + half, cy - half)
#     glVertex2f(cx + half, cy + half)
#     glVertex2f(cx - half, cy + half)
#     glEnd()


# def draw_bbox(xmin: float, ymin: float, xmax: float, ymax: float) -> None:
#     glLineWidth(1.0)
#     glPushAttrib(GL_ENABLE_BIT)
#     glLineStipple(10, 0xAAAA)
#     glEnable(GL_LINE_STIPPLE)
#     glBegin(GL_LINE_LOOP)
#     glVertex2f(xmin, ymin)
#     glVertex2f(xmax, ymin)
#     glVertex2f(xmax, ymax)
#     glVertex2f(xmin, ymax)
#     glEnd()
#     glPopAttrib()


# def draw_polygon_selection(poly, ctx) -> None:
#     """Desenha a caixa de seleção e os ‘handles’ do polígono se estiver selected."""
#     if not poly.selected:
#         return

#     # cor/destaque da seleção
#     glColor3f(1.0, 0.6, 0.0)

#     # bounding box
#     p1, p2 = poly.bounding_box()
#     draw_bbox(p1.x, p1.y, p2.x, p2.y)

#     # tamanho do handle (mundo): preferir cache em ctx.global_vars
#     g = ctx.global_vars
#     half = g.handle_size_world
#     if half is None:
#         # fallback (primeiro frame antes do resizeGL, por ex.)
#         half = px_to_world(ctx, g.handle_size_px, axis="avg")
#     half *= 0.5

#     # “handles” nos 4 cantos
#     corners = [(p1.x, p1.y), (p2.x, p1.y), (p2.x, p2.y), (p1.x, p2.y)]
#     for x, y in corners:
#         _draw_handle_square(x, y, half)


# def draw_circle_selection(circle, ctx) -> None:
#     """Exemplo para círculos: desenhar alça no topo + bbox opcional."""
#     if not circle.selected:
#         return
#     glColor3f(1.0, 0.6, 0.0)

#     # opcional: desenhar bbox simples do círculo
#     xmin, xmax = circle.xc - circle.raio, circle.xc + circle.raio
#     ymin, ymax = circle.yc - circle.raio, circle.yc + circle.raio
#     draw_bbox(xmin, ymin, xmax, ymax)

#     # handle no topo do círculo
#     g = ctx.global_vars
#     half = g.handle_size_world or px_to_world(ctx, g.handle_size_px, "avg")
#     half *= 0.5
#     _draw_handle_square(circle.xc, circle.yc + circle.raio, half)


# def draw_selection_overlays(ctx) -> None:
#     """Desenha SOMENTE as decorações de seleção (bbox/handles) para todos os objetos."""
#     m = ctx.global_vars.modelo
#     # se você tiver properties .poligonos / .circulos, use-as;
#     # senão, troque por m._poligonos / m._circulos
#     for p in getattr(m, "poligonos", m._poligonos):
#         draw_polygon_selection(p, ctx)
#     for c in getattr(m, "circulos", m._circulos):
#         draw_circle_selection(c, ctx)


# def compute_selection_bbox(selected: Iterable[object]) -> tuple[float, float, float, float] | None:
#     """Retorna (xmin, ymin, xmax, ymax) da seleção atual.
#     Funciona para Poligono (pontos) e Circulo (centro±raio).
#     """
#     xs: list[float] = []
#     ys: list[float] = []
#     for obj in selected:
#         if isinstance(obj, Poligono):
#             for p in obj.pontos:
#                 xs.append(p.x)
#                 ys.append(p.y)
#         elif isinstance(obj, Circulo):
#             xs.extend([obj.xc - obj.raio, obj.xc + obj.raio])
#             ys.extend([obj.yc - obj.raio, obj.yc + obj.raio])

#     if not xs or not ys:
#         return None
#     return (min(xs), min(ys), max(xs), max(ys))


# def compute_selection_center(selected: Iterable[object]) -> Ponto | None:
#     """Centro geométrico simples do bbox da seleção."""
#     bbox = compute_selection_bbox(selected)
#     if bbox is None:
#         return None
#     xmin, ymin, xmax, ymax = bbox
#     return Ponto((xmin + xmax) * 0.5, (ymin + ymax) * 0.5)


# def _handle_positions_for_bbox(
#     bbox: tuple[float, float, float, float]
# ) -> dict[str, list[tuple[float, float]]]:
#     """Gera posições dos handles a partir do bbox."""
#     xmin, ymin, xmax, ymax = bbox
#     cx, cy = (xmin + xmax) * 0.5, (ymin + ymax) * 0.5
#     corners = [
#         (xmin, ymin),  # bottom-left
#         (xmax, ymin),  # bottom-right
#         (xmax, ymax),  # top-right
#         (xmin, ymax),  # top-left
#     ]
#     edges = [
#         (cx, ymin),  # bottom
#         (xmax, cy),  # right
#         (cx, ymax),  # top
#         (xmin, cy),  # left
#     ]
#     # anel de rotação (usaremos o centro; o teste é por distância ao retângulo)
#     rotate_ring_center = (cx, cy)
#     return {
#         "corners": corners,
#         "edges": edges,
#         "rotate_center": [rotate_ring_center],
#         "center": [(cx, cy)],
#     }


# def _near_point(xw: float, yw: float, px: float, py: float, tol_world: float) -> bool:
#     return hypot(xw - px, yw - py) <= tol_world


# def _near_ring(
#     xw: float, yw: float, bbox: tuple[float, float, float, float], tol_world: float
# ) -> bool:
#     """Considera 'anel' de rotação como uma coroa ao redor do bbox."""
#     xmin, ymin, xmax, ymax = bbox
#     cx, cy = (xmin + xmax) * 0.5, (ymin + ymax) * 0.5
#     # raio como 60% da maior dimensão
#     rx = (xmax - xmin) * 0.5
#     ry = (ymax - ymin) * 0.5
#     r = max(rx, ry) * 1.15
#     d = hypot(xw - cx, yw - cy)
#     return abs(d - r) <= tol_world * 1.5  # tolerância levemente maior


# def hit_test_handles(context: Context, xw: float, yw: float) -> tuple[TransformMode, dict] | None:
#     """Prioridade: rotate_ring > corner > edge > pivot > interior.

#     Retornos possíveis:
#       ("rotate", {})
#       ("scale", {"kind": "corner", "index": i})
#       ("scale", {"kind": "edge", "index": i})
#       ("pivot", {})
#       None
#     """
#     selected = context.global_vars.selected
#     if not selected:
#         return None

#     bbox = compute_selection_bbox(selected)
#     if bbox is None:
#         return None

#     tol_world = px_to_world(context, context.global_vars.selection_tolerance_px)
#     handles = _handle_positions_for_bbox(bbox)

#     # 1) rotate ring
#     if _near_ring(xw, yw, bbox, tol_world):
#         return (TransformMode.ROTATE, {})

#     # 2) corners (escala uniforme)
#     for i, (hx, hy) in enumerate(handles["corners"]):
#         if _near_point(xw, yw, hx, hy, tol_world):
#             return (TransformMode.SCALE, {"kind": "corner", "index": i})

#     # 3) edges (escala eixo)
#     for i, (hx, hy) in enumerate(handles["edges"]):
#         if _near_point(xw, yw, hx, hy, tol_world):
#             return (TransformMode.SCALE, {"kind": "edge", "index": i})

#     # 4) pivot (centro) — habilite se quiser mover o pivô no futuro
#     # (cx, cy) = handles["center"][0]
#     # if _near_point(xw, yw, cx, cy, tol_world * 0.9):
#     #     return ("pivot", {})

#     return None

# src/cg_examples/ex07_2D_Editor_Qt/view/selection_render.py
from __future__ import annotations

from collections.abc import Iterable
from math import hypot
from typing import TYPE_CHECKING

from OpenGL.GL import (
    GL_ENABLE_BIT,
    GL_LINE_LOOP,
    GL_LINE_STIPPLE,
    GL_QUADS,
    glBegin,
    glColor3f,
    glEnable,
    glEnd,
    glLineStipple,
    glLineWidth,
    glPopAttrib,
    glPushAttrib,
    glVertex2f,
)

from ..model.circulo import Circulo
from ..model.poligono import Poligono
from ..model.ponto import Ponto
from ..state.transform_mode import TransformMode
from .draw_utils import px_to_world

if TYPE_CHECKING:
    from ..state.context import Context


# -------------------------------
# Primitivas de desenho auxiliares
# -------------------------------
def _draw_handle_square(cx: float, cy: float, half: float) -> None:
    glBegin(GL_QUADS)
    glVertex2f(cx - half, cy - half)
    glVertex2f(cx + half, cy - half)
    glVertex2f(cx + half, cy + half)
    glVertex2f(cx - half, cy + half)
    glEnd()


def draw_bbox(xmin: float, ymin: float, xmax: float, ymax: float) -> None:
    """Desenha um retângulo tracejado (bbox) na cor vigente."""
    glLineWidth(1.0)
    glPushAttrib(GL_ENABLE_BIT)
    glLineStipple(10, 0xAAAA)
    glEnable(GL_LINE_STIPPLE)
    glBegin(GL_LINE_LOOP)
    glVertex2f(xmin, ymin)
    glVertex2f(xmax, ymin)
    glVertex2f(xmax, ymax)
    glVertex2f(xmin, ymax)
    glEnd()
    glPopAttrib()


# -------------------------------
# Overlays de seleção
# -------------------------------
def draw_polygon_selection(poly: Poligono, ctx: Context) -> None:
    """Desenha bbox + ‘handles’ do polígono se estiver selecionado."""
    if not getattr(poly, "selected", False):
        return

    # cor/destaque da seleção
    glColor3f(1.0, 0.6, 0.0)

    # bounding box
    p1, p2 = poly.bounding_box()
    draw_bbox(p1.x, p1.y, p2.x, p2.y)

    # tamanho do handle (em coordenadas do mundo)
    g = ctx.global_vars
    half = g.handle_size_world
    if half is None:  # fallback no 1º frame antes de resizeGL
        half = px_to_world(ctx, g.handle_size_px, axis="avg")
    half *= 0.5

    # “handles” nos 4 cantos
    corners = [(p1.x, p1.y), (p2.x, p1.y), (p2.x, p2.y), (p1.x, p2.y)]
    for x, y in corners:
        _draw_handle_square(x, y, half)


def draw_circle_selection(circle: Circulo, ctx: Context) -> None:
    """Desenha bbox + handle superior para círculo selecionado."""
    if not getattr(circle, "selected", False):
        return

    glColor3f(1.0, 0.6, 0.0)

    # bbox do círculo
    xmin, xmax = circle.xc - circle.raio, circle.xc + circle.raio
    ymin, ymax = circle.yc - circle.raio, circle.yc + circle.raio
    draw_bbox(xmin, ymin, xmax, ymax)

    # handle no topo
    g = ctx.global_vars
    half = g.handle_size_world or px_to_world(ctx, g.handle_size_px, "avg")
    half *= 0.5
    _draw_handle_square(circle.xc, circle.yc + circle.raio, half)


def draw_selection_overlays(ctx: Context) -> None:
    """Desenha SOMENTE as decorações de seleção (bbox/handles) para todos os objetos."""
    m = ctx.global_vars.modelo
    for p in m.poligonos:
        draw_polygon_selection(p, ctx)
    for c in m.circulos:
        draw_circle_selection(c, ctx)


# -------------------------------
# Cálculos geométricos auxiliares
# -------------------------------
def compute_selection_bbox(selected: Iterable[object]) -> tuple[float, float, float, float] | None:
    """Retorna (xmin, ymin, xmax, ymax) do conjunto selecionado."""
    xs: list[float] = []
    ys: list[float] = []
    for obj in selected:
        if isinstance(obj, Poligono):
            for p in obj.pontos:
                xs.append(p.x)
                ys.append(p.y)
        elif isinstance(obj, Circulo):
            xs.extend([obj.xc - obj.raio, obj.xc + obj.raio])
            ys.extend([obj.yc - obj.raio, obj.yc + obj.raio])

    if not xs or not ys:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def compute_selection_center(selected: Iterable[object]) -> Ponto | None:
    """Centro geométrico (médio) do bbox da seleção."""
    bbox = compute_selection_bbox(selected)
    if bbox is None:
        return None
    xmin, ymin, xmax, ymax = bbox
    return Ponto((xmin + xmax) * 0.5, (ymin + ymax) * 0.5)


def _handle_positions_for_bbox(
    bbox: tuple[float, float, float, float]
) -> dict[str, list[tuple[float, float]]]:
    """Gera posições dos handles a partir do bbox."""
    xmin, ymin, xmax, ymax = bbox
    cx, cy = (xmin + xmax) * 0.5, (ymin + ymax) * 0.5

    corners = [
        (xmin, ymin),  # bottom-left  (idx=0)
        (xmax, ymin),  # bottom-right (idx=1)
        (xmax, ymax),  # top-right    (idx=2)
        (xmin, ymax),  # top-left     (idx=3)
    ]
    edges = [
        (cx, ymin),  # bottom (y) idx=0
        (xmax, cy),  # right  (x) idx=1
        (cx, ymax),  # top    (y) idx=2
        (xmin, cy),  # left   (x) idx=3
    ]

    # anel de rotação (usamos centro; o teste é por distância ao retângulo)
    rotate_ring_center = (cx, cy)
    return {
        "corners": corners,
        "edges": edges,
        "rotate_center": [rotate_ring_center],
        "center": [(cx, cy)],
    }


def _near_point(xw: float, yw: float, px: float, py: float, tol_world: float) -> bool:
    return hypot(xw - px, yw - py) <= tol_world


def _near_ring(
    xw: float, yw: float, bbox: tuple[float, float, float, float], tol_world: float
) -> bool:
    """Considera 'anel' de rotação como uma coroa ao redor do bbox."""
    xmin, ymin, xmax, ymax = bbox
    cx, cy = (xmin + xmax) * 0.5, (ymin + ymax) * 0.5
    rx = (xmax - xmin) * 0.5
    ry = (ymax - ymin) * 0.5
    r = max(rx, ry) * 1.15
    d = hypot(xw - cx, yw - cy)
    return abs(d - r) <= tol_world * 1.5  # tolerância levemente maior


# ------------------------------------
# Hit-test dos handles (para Transform)
# ------------------------------------
def hit_test_handles(context: Context, xw: float, yw: float) -> tuple[TransformMode, dict] | None:
    """Prioridade: rotate_ring > corner (scale uniforme) > edge (scale eixo) > None.

    Retornos:
      (TransformMode.ROTATE, {})
      (TransformMode.SCALE, {"kind": "corner", "index": i})
      (TransformMode.SCALE, {"kind": "edge", "index": i, "axis": "x"|"y"})
      None
    """
    selected = context.global_vars.selected
    if not selected:
        return None

    bbox = compute_selection_bbox(selected)
    if bbox is None:
        return None

    tol_world = px_to_world(context, context.global_vars.selection_tolerance_px)
    handles = _handle_positions_for_bbox(bbox)

    # 1) rotate ring
    if _near_ring(xw, yw, bbox, tol_world):
        return (TransformMode.ROTATE, {})

    # 2) corners (escala uniforme)
    for i, (hx, hy) in enumerate(handles["corners"]):
        if _near_point(xw, yw, hx, hy, tol_world):
            return (TransformMode.SCALE, {"kind": "corner", "index": i})

    # 3) edges (escala uniaxial)
    for i, (hx, hy) in enumerate(handles["edges"]):
        if _near_point(xw, yw, hx, hy, tol_world):
            axis = "y" if i in (0, 2) else "x"
            return (TransformMode.SCALE, {"kind": "edge", "index": i, "axis": axis})

    # 4) (opcional) mover pivô clicando no centro — se quiser ativar futuramente:
    # (cx, cy) = handles["center"][0]
    # if _near_point(xw, yw, cx, cy, tol_world * 0.9):
    #     return (TransformMode.PIVOT, {})

    return None
