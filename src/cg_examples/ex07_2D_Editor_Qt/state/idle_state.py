from __future__ import annotations

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent

from ..view.draw_utils import get_world_coords, px_to_world
from ..view.selection_render import hit_test_handles
from .abstract_state import State
from .transform_state import TransformState

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

        h = hit_test_handles(self.context, xw, yw)
        # 1) tenta handles primeiro (rotate/scale/pivot)
        if h is not None:
            mode, info = h[0], h[1]
            self.context.current_state = TransformState(self.context, mode=mode, handle=info)
            # transfere o próprio evento para o novo estado (melhor UX)
            self.context.current_state.mouse_press_event(event)
            return

        # 2) interior (translate) se clicou dentro de algum selecionado
        tol_world = px_to_world(self.context, self.context.global_vars.selection_tolerance_px)
        hit_obj = None
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

        # if hit_obj is not None:
        #     self.context.select_object(hit_obj, additive=add)
        # elif not add:
        #     self.context.clear_selection()
        if hit_obj is not None:
            # se ainda não estiver selecionado, selecione
            if hit_obj not in self.context.global_vars.selected:
                self.context.select_object(hit_obj, additive=add)
            # inicia translate
            self.context.current_state = TransformState(self.context, mode="translate")
            self.context.current_state.mouse_press_event(event)
        else:
            # clique “no vazio”: limpa seleção (a não ser que SHIFT)
            if not add:
                self.context.clear_selection()

        self.context.canvas.update()
