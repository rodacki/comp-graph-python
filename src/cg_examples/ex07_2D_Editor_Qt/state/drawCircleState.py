from OpenGL.GL import glColor3f
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt
from .abstractState import State
from ..view.draw_utils import getWorldCoords
from ..view.draw_utils import axis
from ..model.circulo import Circulo
from ..model.ponto import Ponto
from math import sqrt


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

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() != Qt.MouseButton.LeftButton:
            return

        x, y = getWorldCoords(self.context, event.x(), event.y())

        if self.center is None:
            # 1º clique: define o centro e cria círculo temporário
            self.center = Ponto(x, y)
            self.context.global_vars.circulo = Circulo(self.center.x, self.center.y, 0.0)
        else:
            # 2º clique: fixa o raio e comita no modelo
            r = sqrt((x - self.center.x) ** 2 + (y - self.center.y) ** 2)
            self.context.global_vars.circulo.raio = r
            self.context.global_vars.modelo.addCirculo(self.context.global_vars.circulo)

            # limpa e volta pro Idle
            self.context.global_vars.circulo = None
            self.center = None
            self.context.currentState = self.context.idleState

        self.context.canvas.update()

    def mouseMoveEvent(self, event):
        """Atualiza o círculo temporário durante o movimento do mouse."""
        if self.center and self.context.global_vars.circulo:
            # x = event.x() - self.context.global_vars.w / 2
            # y = self.context.global_vars.h / 2 - event.y()
            x, y = getWorldCoords(self.context, event.x(), event.y())
            r = sqrt((x - self.center.x)**2 + (y - self.center.y)**2)
            self.context.global_vars.circulo.raio = r
            # força redesenho
            self.context.canvas.update()

    # ---- somente overlay (preview) do estado ----
    def display_overlay(self):
        temp = self.context.global_vars.circulo
        if self.center and temp:
            glColor3f(0.0, 1.0, 0.0)  # verde para preview
            temp.drawOpen()

