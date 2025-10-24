from math import sqrt

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent

from ..model.circulo import Circulo
from ..model.ponto import Ponto
from ..view.draw_utils import get_world_coords
from ..view.renderers import draw_circle
from .abstract_state import State


class DrawCircleState(State):
    def __init__(self, context):
        super().__init__(context)
        self.center: Ponto | None = None  # Ponto inicial (centro)

    @property
    def context(self):
        return super().context

    @context.setter
    def context(self, newcontext):
        super().context = newcontext

    def mouse_press_event(self, event: QMouseEvent):
        if event.button() != Qt.MouseButton.LeftButton:
            return

        x, y = get_world_coords(self.context, event.x(), event.y())

        if self.center is None:
            # 1º clique: define o centro e cria círculo temporário
            self.center = Ponto(x, y)
            self.context.global_vars.circulo = Circulo(self.center.x, self.center.y, 0.0)
        else:
            # 2º clique: fixa o raio e comita no modelo
            r = sqrt((x - self.center.x) ** 2 + (y - self.center.y) ** 2)
            self.context.global_vars.circulo.raio = r
            self.context.global_vars.modelo.add_circulo(self.context.global_vars.circulo)

            # limpa e volta pro Idle
            self.context.global_vars.circulo = None
            self.center = None
            self.context.current_state = self.context.idle_state

        self.context.canvas.update()

    def mouse_move_event(self, event):
        """Atualiza o círculo temporário durante o movimento do mouse."""
        if self.center and self.context.global_vars.circulo:
            # x = event.x() - self.context.global_vars.w / 2
            # y = self.context.global_vars.h / 2 - event.y()
            x, y = get_world_coords(self.context, event.x(), event.y())
            r = sqrt((x - self.center.x) ** 2 + (y - self.center.y) ** 2)
            self.context.global_vars.circulo.raio = r
            # força redesenho
            self.context.canvas.update()

    # ---- somente overlay (preview) do estado ----
    def display_overlay(self):
        temp = self.context.global_vars.circulo
        if temp:
            draw_circle(temp, dashed=True, color=(0, 1, 0))
        # if self.center and temp:
        #     glColor3f(0.0, 1.0, 0.0)  # verde para preview
        #     temp.draw_open()
