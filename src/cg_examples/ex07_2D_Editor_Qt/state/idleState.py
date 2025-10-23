# from OpenGL.GL import (
#     GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, 
#     glClear, glLoadIdentity, glColor3f,
    
# )




from .abstractState import State
from ..view.draw_utils import getWorldCoords, px_to_world
from ..view.draw_utils import axis
from PyQt5.QtGui import QMouseEvent, QKeyEvent
from PyQt5.QtCore import Qt
from ..view.selection_render import draw_selection_overlays

class IdleState(State):

    def __init__(self, context) -> None:
        super().__init__(context)
        
    @property
    def context(self):
        return super().context
    
    @context.setter
    def context(self, newcontext):
        super().context = newcontext

    def mousePressEvent(self, event: QMouseEvent):
        print("IdleState: mouse pressed")
        xw, yw = getWorldCoords(self.context, event.x(), event.y())
        add = bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
        print(add)
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
            print("Add to selection")
            self.context.select_object(hit_obj, additive=add)
        elif not add:
            print("Clear selection")
            self.context.clear_selection()

        self.context.canvas.update()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None: 
        pass

    def display_overlay(self):
        # Nada a desenhar em Idle
        pass

    def mouseMoveEvent(self, event: QMouseEvent):
        pass
