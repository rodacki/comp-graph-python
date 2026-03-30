"""Estado padrão de edição do editor 2D.

Neste estado o usuário pode:
- selecionar objetos por hit-test;
- mover objetos selecionados por arraste;
- escalar por alças (handlers) de canto (polígonos) e topo (círculos);
- rotacionar polígonos pela alça (handler) de rotação.
"""

from __future__ import annotations

import logging
from math import atan2, cos, hypot, isfinite, pi, sin
from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent

from ..model.circulo import Circulo
from ..model.poligono import Poligono
from ..view.draw_utils import get_world_coords, px_to_world
from ..view.selection_render import (
    polygon_rotation_handle_position,
    rotation_handle_radius_world,
)
from .abstract_state import State

log = logging.getLogger(__name__)


class IdleState(State):
    """Estado de seleção/edição com transformações interativas."""

    def __init__(self, context) -> None:
        """Inicializa buffers de interação para move, escala e rotação.

        Args:
            context: Contexto compartilhado da aplicação.

        Returns:
            None: Configura a sessão inicial sem interação ativa.
        """
        super().__init__(context)
        self._moving = False
        self._last_mouse_world: tuple[float, float] | None = None
        self._drag_targets: list[Any] = []
        self._scaling = False
        self._scale_target: Any | None = None
        self._scale_pivot: tuple[float, float] | None = None
        self._scale_d0: float = 0.0
        self._scale_circle_radius0: float = 0.0
        self._scale_polygon_points0: list[tuple[float, float]] = []
        self._scale_min_factor = 0.01
        self._scale_min_radius = 1e-6
        self._rotating = False
        self._rotate_target: Poligono | None = None
        self._rotate_center: tuple[float, float] | None = None
        self._rotate_points0: list[tuple[float, float]] = []
        self._rotate_handle_vec0: tuple[float, float] | None = None
        self._rotate_last_angle: float = 0.0
        self._rotate_raw_angle: float = 0.0
        self._rotate_accum_angle: float = 0.0

    @property
    def context(self) -> Any:
        """Retorna contexto associado ao estado.

        Returns:
            Any: Contexto da máquina de estados.
        """
        return super().context

    @context.setter
    def context(self, newcontext: Any) -> None:
        """Atualiza referência de contexto associada ao estado.

        Args:
            newcontext: Novo contexto compartilhado.

        Returns:
            None: Apenas substitui referência interna.
        """
        super().context = newcontext

    def mouse_press_event(self, event: QMouseEvent) -> None:
        """Trata clique para iniciar rotação, escala, seleção ou movimentação.

        Args:
            event: Evento de clique do mouse.

        Returns:
            None: Atualiza sessão de interação e solicita redraw.
        """
        if event.button() != Qt.MouseButton.LeftButton:
            return

        log.debug("mouse_press_event")
        xw, yw = get_world_coords(self.context, event.x(), event.y())

        if self._try_start_transform(xw, yw):
            self.context.canvas.update()
            return

        add = bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
        tol_world = px_to_world(self.context, self.context.global_vars.selection_tolerance_px)
        hit_obj = self._hit_test_topmost(xw, yw, tol_world)
        self._apply_selection_and_move_session(hit_obj, add, xw, yw)

        self.context.canvas.update()

    def _try_start_transform(self, xw: float, yw: float) -> bool:
        """Tenta iniciar rotação ou escala a partir da posição do clique.

        Args:
            xw: Coordenada X do clique em mundo.
            yw: Coordenada Y do clique em mundo.

        Returns:
            bool: `True` quando alguma sessão de transformação foi iniciada.
        """
        if self._try_start_rotation(xw, yw):
            return True
        if self._try_start_scale(xw, yw):
            return True
        return False

    def _hit_test_topmost(self, xw: float, yw: float, tol_world: float) -> Any | None:
        """Executa hit-test e retorna o objeto top-most sob o cursor.

        Args:
            xw: Coordenada X do ponto de consulta em mundo.
            yw: Coordenada Y do ponto de consulta em mundo.
            tol_world: Tolerância de seleção em unidades de mundo.

        Returns:
            Any | None: Objeto encontrado no topo, ou `None` quando não há hit.
        """
        for circle in reversed(self.context.global_vars.modelo.circulos):
            if circle.hit_test(xw, yw, tol_world):
                return circle

        for polygon in reversed(self.context.global_vars.modelo.poligonos):
            if polygon.hit_test(xw, yw, tol_world):
                return polygon

        return None

    def _apply_selection_and_move_session(
        self,
        hit_obj: Any | None,
        additive: bool,
        xw: float,
        yw: float,
    ) -> None:
        """Atualiza seleção e prepara sessão de movimento quando aplicável.

        Args:
            hit_obj: Objeto atingido pelo hit-test, ou `None`.
            additive: Indica se seleção deve ser aditiva (Shift).
            xw: Coordenada X do clique em mundo.
            yw: Coordenada Y do clique em mundo.

        Returns:
            None: Atualiza seleção global e estado interno de arraste.
        """
        if hit_obj is None:
            if not additive:
                self.context.clear_selection()
                self._clear_move_session()
            return

        self.context.select_object(hit_obj, additive=additive)
        self._drag_targets = list(self.context.global_vars.selected)
        self._last_mouse_world = (xw, yw)
        self._moving = len(self._drag_targets) > 0

    def mouse_move_event(self, event: QMouseEvent) -> None:
        """Atualiza transformação ativa enquanto o mouse estiver em arraste.

        Args:
            event: Evento de movimento do mouse.

        Returns:
            None: Aplica rotação, escala ou movimento incremental.
        """
        xw, yw = get_world_coords(self.context, event.x(), event.y())

        if self._rotating:
            snapping = bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
            self._update_rotation(xw, yw, snap=snapping)
            self.context.canvas.update()
            return

        if self._scaling:
            self._update_scale(xw, yw)
            self.context.canvas.update()
            return

        if not self._moving or not self._drag_targets or self._last_mouse_world is None:
            return

        last_x, last_y = self._last_mouse_world
        dx = xw - last_x
        dy = yw - last_y

        if dx == 0.0 and dy == 0.0:
            return

        for obj in self._drag_targets:
            translate = getattr(obj, "translate", None)
            if callable(translate):
                translate(dx, dy)

        self._last_mouse_world = (xw, yw)
        self.context.canvas.update()

    def mouse_release_event(self, event: QMouseEvent) -> None:
        """Finaliza interações ativas ao soltar o botão esquerdo.

        Args:
            event: Evento de soltura do mouse.

        Returns:
            None: Limpa sessões temporárias de rotação, escala e movimento.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self._clear_rotation_session()
            self._clear_scale_session()
            self._clear_move_session()

    def is_rotating_polygon(self, poly: Any) -> bool:
        """Informa se um polígono específico está em rotação ativa.

        Args:
            poly: Polígono consultado pela camada de renderização.

        Returns:
            bool: `True` quando o polígono é o alvo da rotação corrente.
        """
        return self._rotating and self._rotate_target is poly

    def get_rotating_handle_position(self, poly: Any) -> tuple[float, float] | None:
        """Retorna posição dinâmica da alça de rotação durante rotação.

        Args:
            poly: Polígono que está sendo desenhado pela camada de seleção.

        Returns:
            tuple[float, float] | None:
                Coordenada `(x, y)` da alça em arco quando rotação está ativa;
                `None` caso contrário.
        """
        if not self.is_rotating_polygon(poly):
            return None
        if self._rotate_center is None or self._rotate_handle_vec0 is None:
            return None

        cx, cy = self._rotate_center
        vx0, vy0 = self._rotate_handle_vec0
        c = cos(self._rotate_accum_angle)
        s = sin(self._rotate_accum_angle)
        hx = cx + c * vx0 - s * vy0
        hy = cy + s * vx0 + c * vy0
        return hx, hy

    def _clear_move_session(self) -> None:
        """Reseta estado temporário da sessão de movimento.

        Returns:
            None: Sessão de move fica inativa.
        """
        self._moving = False
        self._last_mouse_world = None
        self._drag_targets = []

    def _clear_scale_session(self) -> None:
        """Reseta estado temporário da sessão de escala.

        Returns:
            None: Sessão de escala fica inativa.
        """
        self._scaling = False
        self._scale_target = None
        self._scale_pivot = None
        self._scale_d0 = 0.0
        self._scale_circle_radius0 = 0.0
        self._scale_polygon_points0 = []

    def _clear_rotation_session(self) -> None:
        """Reseta estado temporário da sessão de rotação.

        Returns:
            None: Sessão de rotação fica inativa.
        """
        self._rotating = False
        self._rotate_target = None
        self._rotate_center = None
        self._rotate_points0 = []
        self._rotate_handle_vec0 = None
        self._rotate_last_angle = 0.0
        self._rotate_raw_angle = 0.0
        self._rotate_accum_angle = 0.0

    def _handle_half_world(self) -> float:
        """Calcula metade do tamanho da alça (handler) em coordenadas de mundo.

        Returns:
            float: Metade da aresta de uma alça quadrada na unidade de mundo.
        """
        g = self.context.global_vars
        size = g.handle_size_world
        if size is None:
            size = px_to_world(self.context, g.handle_size_px, axis="avg")
        return 0.5 * size

    def _is_inside_handle(self, xw: float, yw: float, hx: float, hy: float, half: float) -> bool:
        """Testa se um ponto em mundo está dentro da área de uma alça quadrada.

        Args:
            xw: Coordenada X do ponto consultado.
            yw: Coordenada Y do ponto consultado.
            hx: Coordenada X do centro da alça.
            hy: Coordenada Y do centro da alça.
            half: Metade da aresta da alça em mundo.

        Returns:
            bool: `True` quando o ponto está dentro do quadrado da alça.
        """
        return abs(xw - hx) <= half and abs(yw - hy) <= half

    def _try_start_scale(self, xw: float, yw: float) -> bool:
        """Tenta iniciar sessão de escala a partir de clique em alça.

        Args:
            xw: Coordenada X do clique em mundo.
            yw: Coordenada Y do clique em mundo.

        Returns:
            bool: `True` quando sessão de escala foi iniciada.
        """
        selected = list(self.context.global_vars.selected)
        if len(selected) != 1:
            return False

        target = selected[0]
        half = self._handle_half_world()

        if isinstance(target, Circulo):
            hx, hy = target.xc, target.yc + target.raio
            if not self._is_inside_handle(xw, yw, hx, hy, half):
                return False

            d0 = max(abs(target.raio), self._scale_min_radius)
            self._clear_move_session()
            self._scaling = True
            self._scale_target = target
            self._scale_pivot = (target.xc, target.yc)
            self._scale_d0 = d0
            self._scale_circle_radius0 = target.raio
            return True

        if isinstance(target, Poligono):
            p1, p2 = target.bounding_box()
            corners = [(p1.x, p1.y), (p2.x, p1.y), (p2.x, p2.y), (p1.x, p2.y)]

            hit_index = -1
            for i, (hx, hy) in enumerate(corners):
                if self._is_inside_handle(xw, yw, hx, hy, half):
                    hit_index = i
                    break

            if hit_index < 0:
                return False

            opp_index = (hit_index + 2) % 4
            px, py = corners[opp_index]
            hx, hy = corners[hit_index]
            d0 = hypot(hx - px, hy - py)
            if d0 <= 1e-12:
                return False

            self._clear_move_session()
            self._scaling = True
            self._scale_target = target
            self._scale_pivot = (px, py)
            self._scale_d0 = d0
            self._scale_polygon_points0 = [(p.x, p.y) for p in target.pontos]
            return True

        return False

    def _try_start_rotation(self, xw: float, yw: float) -> bool:
        """Tenta iniciar sessão de rotação na alça de rotação do polígono.

        Args:
            xw: Coordenada X do clique em mundo.
            yw: Coordenada Y do clique em mundo.

        Returns:
            bool: `True` quando sessão de rotação foi iniciada.
        """
        selected = list(self.context.global_vars.selected)
        if len(selected) != 1:
            return False

        target = selected[0]
        if not isinstance(target, Poligono):
            return False

        hx, hy = polygon_rotation_handle_position(target, self.context)
        radius = rotation_handle_radius_world(self.context)
        if hypot(xw - hx, yw - hy) > radius:
            return False

        p1, p2 = target.bounding_box()
        cx = 0.5 * (p1.x + p2.x)
        cy = 0.5 * (p1.y + p2.y)

        self._clear_move_session()
        self._clear_scale_session()
        self._rotating = True
        self._rotate_target = target
        self._rotate_center = (cx, cy)
        self._rotate_points0 = [(p.x, p.y) for p in target.pontos]
        self._rotate_handle_vec0 = (hx - cx, hy - cy)
        self._rotate_last_angle = atan2(yw - cy, xw - cx)
        self._rotate_raw_angle = 0.0
        self._rotate_accum_angle = 0.0
        return True

    def _update_scale(self, xw: float, yw: float) -> None:
        """Atualiza escala interativa do alvo corrente conforme posição do mouse.

        Args:
            xw: Coordenada X atual do mouse em mundo.
            yw: Coordenada Y atual do mouse em mundo.

        Returns:
            None: Atualiza geometria do objeto alvo (círculo ou polígono).
        """
        target = self._scale_target
        pivot = self._scale_pivot
        d0 = self._scale_d0
        if target is None or pivot is None or d0 <= 0.0:
            return

        px, py = pivot
        d = hypot(xw - px, yw - py)
        factor = d / d0
        if not isfinite(factor):
            return
        factor = max(self._scale_min_factor, factor)

        if isinstance(target, Circulo):
            target.raio = max(self._scale_min_radius, self._scale_circle_radius0 * factor)
            return

        if isinstance(target, Poligono):
            if len(self._scale_polygon_points0) != len(target.pontos):
                return
            for point, (x0, y0) in zip(target.pontos, self._scale_polygon_points0, strict=False):
                point.x = px + factor * (x0 - px)
                point.y = py + factor * (y0 - py)

    def _rotation_snap_step_radians(self) -> float:
        """Retorna passo de snap angular em radianos.

        Returns:
            float: Passo positivo em radianos, ou `0.0` quando inválido.
        """
        deg = float(getattr(self.context.global_vars, "rotation_snap_degrees", 0.0))
        if not isfinite(deg) or deg <= 0.0:
            return 0.0
        return deg * pi / 180.0

    def _update_rotation(self, xw: float, yw: float, snap: bool = False) -> None:
        """Atualiza rotação contínua do polígono alvo acompanhando o mouse.

        Args:
            xw: Coordenada X atual do mouse em mundo.
            yw: Coordenada Y atual do mouse em mundo.
            snap: Quando `True`, aplica snap angular no passo configurado.

        Returns:
            None: Atualiza os vértices do polígono por rotação acumulada.

        Notes:
            A rotação usa normalização incremental de ângulo em [-pi, pi]
            para evitar saltos ao cruzar o limite angular.
        """
        target = self._rotate_target
        center = self._rotate_center
        if target is None or center is None:
            return
        if len(self._rotate_points0) != len(target.pontos):
            return

        cx, cy = center
        current_angle = atan2(yw - cy, xw - cx)
        delta = self._normalize_angle(current_angle - self._rotate_last_angle)
        if not isfinite(delta):
            return

        self._rotate_raw_angle += delta
        self._rotate_last_angle = current_angle

        applied_angle = self._rotate_raw_angle
        if snap:
            step = self._rotation_snap_step_radians()
            if step > 0.0:
                applied_angle = round(applied_angle / step) * step
        self._rotate_accum_angle = applied_angle

        c = cos(applied_angle)
        s = sin(applied_angle)
        for point, (x0, y0) in zip(target.pontos, self._rotate_points0, strict=False):
            dx = x0 - cx
            dy = y0 - cy
            point.x = cx + c * dx - s * dy
            point.y = cy + s * dx + c * dy

    def _normalize_angle(self, a: float) -> float:
        """Normaliza ângulo para [-pi, pi], evitando saltos na rotação contínua."""
        while a > pi:
            a -= 2.0 * pi
        while a < -pi:
            a += 2.0 * pi
        return a
