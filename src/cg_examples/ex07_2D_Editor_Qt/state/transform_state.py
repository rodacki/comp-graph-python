# src/cg_examples/ex07_2D_Editor_Qt/state/transform_state.py
from __future__ import annotations

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QMouseEvent

from ..model.ponto import Ponto
from ..model.transform_ops import (
    angle_from,
    apply_rotation,
    apply_scale,
    apply_translation,
    restore_snapshot,
    scale_from_vectors,
    snapshot_selection,
)
from ..view.draw_utils import get_world_coords
from ..view.selection_render import compute_selection_center
from .abstract_state import State

log = logging.getLogger(__name__)


class TransformState(State):
    """Estado único para translate/scale/rotate, com submodo."""

    def __init__(self, context, mode: str, handle: dict | None = None) -> None:
        super().__init__(context)
        self.mode = mode  # "translate" | "scale" | "rotate" | "pivot"
        self.handle = handle or {}
        self._start_mouse: tuple[float, float] | None = None
        self._curr_mouse: tuple[float, float] | None = None
        self._pivot: Ponto | None = None
        self._snap = None
        self._axis_from_handle: str | None = None  # "x"|"y"|None

    def on_enter(self) -> None:
        gv = self.context.global_vars
        self._pivot = gv.pivot or compute_selection_center(gv.selected)
        if self._pivot is None:
            # nada selecionado: volte ao idle
            self.context.current_state = self.context.idle_state
            return

        self._snap = snapshot_selection(gv.selected)

        # define eixo implicado pelo handle de aresta
        if self.mode == "scale" and self.handle.get("kind") == "edge":
            idx = int(self.handle.get("index", 0)) % 4
            # edges: 0=bottom(y),1=right(x),2=top(y),3=left(x)
            self._axis_from_handle = "y" if idx in (0, 2) else "x"

    def mouse_press_event(self, event: QMouseEvent) -> None:
        self._start_mouse = get_world_coords(self.context, event.x(), event.y())

    def mouse_move_event(self, event: QMouseEvent) -> None:
        if self._start_mouse is None:
            return
        self._curr_mouse = get_world_coords(self.context, event.x(), event.y())

        gv = self.context.global_vars

        if self.mode == "translate":
            dx = self._curr_mouse[0] - self._start_mouse[0]
            dy = self._curr_mouse[1] - self._start_mouse[1]
            # Shift: restringe ao eixo dominante
            if event.modifiers() & int(Qt.KeyboardModifier.ShiftModifier):
                if abs(dx) > abs(dy):
                    dy = 0.0
                else:
                    dx = 0.0
            apply_translation(gv.selected, self._snap, dx, dy)

        elif self.mode == "scale":
            axis = self._axis_from_handle  # None => uniforme (corner)
            sx, sy = scale_from_vectors(self._pivot, self._start_mouse, self._curr_mouse, axis)
            # Shift: força uniforme
            if event.modifiers() & int(Qt.KeyboardModifier.ShiftModifier):
                s = (sx * sy) ** 0.5
                sx = sy = s
            apply_scale(gv.selected, self._snap, sx, sy, self._pivot)

        elif self.mode == "rotate":
            ang = angle_from(self._pivot, self._start_mouse, self._curr_mouse)
            # Shift: quantiza ângulo (15°)
            if event.modifiers() & int(Qt.KeyboardModifier.ShiftModifier):
                step = gv.snap_angle_deg if hasattr(gv, "snap_angle_deg") else 15
                # quantização simples:
                import math

                ang = round(ang / math.radians(step)) * math.radians(step)
            apply_rotation(gv.selected, self._snap, ang, self._pivot)

        self.context.canvas.update()

    def mouse_release_event(self, event: QMouseEvent) -> None:
        # já aplicamos in-place; apenas voltar ao idle
        self.context.current_state = self.context.idle_state

    def key_press_event(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            if self._snap is not None:
                restore_snapshot(self._snap)
            self.context.current_state = self.context.idle_state

    # overlay opcional (guias)
    def display_overlay(self) -> None:
        # se quiser, desenhe guias aqui no futuro (linha pivô->mouse, bbox fantasma etc.)
        pass
