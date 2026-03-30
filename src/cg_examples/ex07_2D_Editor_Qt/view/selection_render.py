"""Rotinas de desenho para decorações de seleção.

Este módulo centraliza rendering de:
- bounding boxes tracejadas;
- alças (handlers) de escala;
- alça (handler) de rotação e seu comportamento durante rotação ativa.
"""

from math import cos, sin, tau

from OpenGL.GL import (
    GL_ENABLE_BIT,
    GL_LINE_LOOP,
    GL_LINE_STIPPLE,
    GL_QUADS,
    GL_TRIANGLE_FAN,
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

from ..view.draw_utils import px_to_world


def _draw_handle_square(cx: float, cy: float, half: float) -> None:
    """Desenha alça quadrada (handler) centrada em `(cx, cy)`.

    Args:
        cx: Coordenada X do centro da alça.
        cy: Coordenada Y do centro da alça.
        half: Metade do lado do quadrado em coordenadas de mundo.

    Returns:
        None: Emite vértices no pipeline OpenGL imediato.
    """
    glBegin(GL_QUADS)
    glVertex2f(cx - half, cy - half)
    glVertex2f(cx + half, cy - half)
    glVertex2f(cx + half, cy + half)
    glVertex2f(cx - half, cy + half)
    glEnd()


def _draw_handle_circle(cx: float, cy: float, radius: float, segments: int = 24) -> None:
    """Desenha alça circular (handler) preenchida.

    Args:
        cx: Coordenada X do centro.
        cy: Coordenada Y do centro.
        radius: Raio do círculo em coordenadas de mundo.
        segments: Quantidade de segmentos para aproximação da circunferência.

    Returns:
        None: Emite geometria no pipeline OpenGL imediato.
    """
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(cx, cy)
    for i in range(segments + 1):
        a = tau * i / segments
        glVertex2f(cx + radius * cos(a), cy + radius * sin(a))
    glEnd()


def handle_half_world(ctx) -> float:
    """Obtém metade do tamanho padrão das alças em coordenadas de mundo.

    Args:
        ctx: Contexto com variáveis globais do editor.

    Returns:
        float: Metade da aresta da alça quadrada.
    """
    g = ctx.global_vars
    half = g.handle_size_world
    if half is None:
        half = px_to_world(ctx, g.handle_size_px, axis="avg")
    return 0.5 * half


def polygon_bbox_corners(poly) -> list[tuple[float, float]]:
    """Retorna os quatro cantos da bbox do polígono, em sentido anti-horário.

    Args:
        poly: Polígono alvo.

    Returns:
        list[tuple[float, float]]: Lista de cantos `(x, y)` da bbox.
    """
    p1, p2 = poly.bounding_box()
    return [(p1.x, p1.y), (p2.x, p1.y), (p2.x, p2.y), (p1.x, p2.y)]


def polygon_rotation_handle_position(poly, ctx) -> tuple[float, float]:
    """Calcula posição padrão da alça de rotação acima da bbox do polígono.

    Args:
        poly: Polígono selecionado.
        ctx: Contexto da aplicação para obter escala visual de handlers.

    Returns:
        tuple[float, float]: Coordenadas `(x, y)` da alça de rotação.
    """
    p1, p2 = poly.bounding_box()
    cx = 0.5 * (p1.x + p2.x)
    half = handle_half_world(ctx)
    y = p2.y + 2.0 * half
    return cx, y


def rotation_handle_radius_world(ctx) -> float:
    """Retorna raio visual da alça de rotação em coordenadas de mundo.

    Args:
        ctx: Contexto da aplicação para obter escala visual de handlers.

    Returns:
        float: Raio da alça de rotação.
    """
    return 0.7 * handle_half_world(ctx)


def _is_polygon_being_rotated(ctx, poly) -> bool:
    """Consulta estado atual para saber se polígono está em rotação ativa.

    Args:
        ctx: Contexto da aplicação.
        poly: Polígono consultado.

    Returns:
        bool: `True` quando o polígono está sendo rotacionado neste frame.
    """
    state = ctx.current_state
    checker = getattr(state, "is_rotating_polygon", None)
    return bool(callable(checker) and checker(poly))


def _rotating_handle_position_or_default(poly, ctx) -> tuple[float, float]:
    """Obtém posição da alça de rotação respeitando rotação ativa.

    Args:
        poly: Polígono selecionado.
        ctx: Contexto da aplicação.

    Returns:
        tuple[float, float]: Posição dinâmica durante rotação, ou posição padrão.
    """
    state = ctx.current_state
    getter = getattr(state, "get_rotating_handle_position", None)
    if callable(getter):
        pos = getter(poly)
        if pos is not None:
            return pos
    return polygon_rotation_handle_position(poly, ctx)


def draw_bbox(xmin: float, ymin: float, xmax: float, ymax: float) -> None:
    """Desenha caixa de seleção tracejada alinhada aos eixos.

    Args:
        xmin: Limite mínimo em X.
        ymin: Limite mínimo em Y.
        xmax: Limite máximo em X.
        ymax: Limite máximo em Y.

    Returns:
        None: Emite linhas no pipeline OpenGL imediato.
    """
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
    """Desenha decoração de seleção de um polígono.

    Args:
        poly: Polígono alvo da decoração.
        ctx: Contexto da aplicação.

    Returns:
        None: Renderiza bbox/alças quando o polígono está selecionado.

    Notes:
        Durante rotação ativa do polígono, bbox e alças de escala são
        suprimidas, mantendo apenas a alça de rotação.
    """
    if not poly.selected:
        return

    glColor3f(1.0, 0.6, 0.0)

    half = handle_half_world(ctx)
    rotating_now = _is_polygon_being_rotated(ctx, poly)

    if not rotating_now:
        p1, p2 = poly.bounding_box()
        draw_bbox(p1.x, p1.y, p2.x, p2.y)
        for x, y in polygon_bbox_corners(poly):
            _draw_handle_square(x, y, half)

    rhx, rhy = _rotating_handle_position_or_default(poly, ctx)
    _draw_handle_circle(rhx, rhy, rotation_handle_radius_world(ctx))


def draw_circle_selection(circle, ctx) -> None:
    """Desenha decoração de seleção de um círculo.

    Args:
        circle: Círculo alvo da decoração.
        ctx: Contexto da aplicação.

    Returns:
        None: Renderiza bbox e alça superior quando selecionado.
    """
    if not circle.selected:
        return
    glColor3f(1.0, 0.6, 0.0)

    xmin, xmax = circle.xc - circle.raio, circle.xc + circle.raio
    ymin, ymax = circle.yc - circle.raio, circle.yc + circle.raio
    draw_bbox(xmin, ymin, xmax, ymax)

    g = ctx.global_vars
    half = g.handle_size_world or px_to_world(ctx, g.handle_size_px, "avg")
    half *= 0.5
    _draw_handle_square(circle.xc, circle.yc + circle.raio, half)


def draw_selection_overlays(ctx) -> None:
    """Desenha overlays de seleção para todos os objetos da cena.

    Args:
        ctx: Contexto da aplicação com acesso ao modelo.

    Returns:
        None: Itera objetos e renderiza apenas decorações de seleção.
    """
    m = ctx.global_vars.modelo
    for p in m.poligonos:
        draw_polygon_selection(p, ctx)
    for c in m.circulos:
        draw_circle_selection(c, ctx)
