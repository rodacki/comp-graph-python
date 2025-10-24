import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent

from ..view.draw_utils import get_world_coords, px_to_world
from .abstract_state import State

log = logging.getLogger(__name__)


class IdleState(State):

    def __init__(self, context) -> None:
        super().__init__(context)

    @property
    def context(self):
        return super().context

    @context.setter
    def context(self, newcontext):
        super().context = newcontext

    def mouse_press_event(self, event: QMouseEvent):
        log.debug("mouse_press_event")
        xw, yw = get_world_coords(self.context, event.x(), event.y())
        add = bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
        hit_obj = None
        tol_world = px_to_world(self.context, self.context.global_vars.selection_tolerance_px)
        # percorra “de trás pra frente”
        # círculos
        for c in reversed(self.context.global_vars.modelo.circulos):
            if c.hit_test(xw, yw, tol_world):
                hit_obj = c
                break
        # polígonos (se ainda não bateu)
        if hit_obj is None:
            for p in reversed(self.context.global_vars.modelo.poligonos):
                if p.hit_test(xw, yw, tol_world):
                    hit_obj = p
                    break

        if hit_obj is not None:
            self.context.select_object(hit_obj, additive=add)
        elif not add:
            self.context.clear_selection()

        self.context.canvas.update()
