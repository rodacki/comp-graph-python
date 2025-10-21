# cg_examples/ex07_2D_Editor_Qt/view/selection_render.py
from OpenGL.GL import (
    GL_LINE_LOOP, GL_QUADS, GL_ENABLE_BIT, GL_LINE_STIPPLE, 
    glPopAttrib, glBegin, glEnd, glVertex2f, glColor3f, 
    glLineWidth, glPushAttrib, glLineStipple, glEnable
)
from ..view.draw_utils import px_to_world  # caso precise fallback sem cache

def _draw_handle_square(cx: float, cy: float, half: float) -> None:
    glBegin(GL_QUADS)
    glVertex2f(cx - half, cy - half)
    glVertex2f(cx + half, cy - half)
    glVertex2f(cx + half, cy + half)
    glVertex2f(cx - half, cy + half)
    glEnd()

def draw_bbox(xmin: float, ymin: float, xmax: float, ymax: float) -> None:
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

def draw_polygon_selection(poly, ctx) -> None:
    """Desenha a caixa de seleção e os ‘handles’ do polígono se estiver selected."""
    if not poly.selected:
        return

    # cor/destaque da seleção
    glColor3f(1.0, 0.6, 0.0)

    # bounding box
    p1, p2 = poly.bounding_box()
    draw_bbox(p1.x, p1.y, p2.x, p2.y)

    # tamanho do handle (mundo): preferir cache em ctx.global_vars
    g = ctx.global_vars
    half = g.handle_size_world
    if half is None:
        # fallback (primeiro frame antes do resizeGL, por ex.)
        half = px_to_world(ctx, g.handle_size_px, axis="avg")
    half *= 0.5

    # “handles” nos 4 cantos
    corners = [(p1.x, p1.y), (p2.x, p1.y), (p2.x, p2.y), (p1.x, p2.y)]
    for (x, y) in corners:
        _draw_handle_square(x, y, half)

def draw_circle_selection(circle, ctx) -> None:
    """Exemplo para círculos: desenhar alça no topo + bbox opcional."""
    if not circle.selected:
        return
    glColor3f(1.0, 0.6, 0.0)

    # opcional: desenhar bbox simples do círculo
    xmin, xmax = circle.xc - circle.raio, circle.xc + circle.raio
    ymin, ymax = circle.yc - circle.raio, circle.yc + circle.raio
    draw_bbox(xmin, ymin, xmax, ymax)

    # handle no topo do círculo
    g = ctx.global_vars
    half = g.handle_size_world or px_to_world(ctx, g.handle_size_px, "avg")
    half *= 0.5
    _draw_handle_square(circle.xc, circle.yc + circle.raio, half)


def draw_selection_overlays(ctx) -> None:
    """Desenha SOMENTE as decorações de seleção (bbox/handles) para todos os objetos."""
    m = ctx.global_vars.modelo
    # se você tiver properties .poligonos / .circulos, use-as;
    # senão, troque por m._poligonos / m._circulos
    for p in getattr(m, "poligonos", m._poligonos):
        draw_polygon_selection(p, ctx)
    for c in getattr(m, "circulos", m._circulos):
        draw_circle_selection(c, ctx)