from OpenGL.GL import glColor3f
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt
from .abstractState import State
from ..view.draw_utils import getWorldCoords
from ..view.draw_utils import axis
from ..model.circulo import Circulo
from ..model.ponto import Ponto
from math import sqrt


class InitCircleState(State):
    def __init__(self, context):
        super().__init__(context)
        self.center: Ponto | None = None  # Ponto inicial (centro)
        #self.temp_circle = None

    @property
    def context(self):
        return super().context
    
    @context.setter
    def context(self, newcontext):
        super().context = newcontext

    # def mousePressEvent(self, event):
    #     # Conversão das coordenadas do clique para coordenadas do mundo
    #     #x = (event.x() - self.context.global_vars.w / 2)
    #     #y = (self.context.global_vars.h / 2 - event.y())
    #     x, y = getWorldCoords(self.context, event.x(), event.y())
    #     print(event.x(), event.y())

    #     if self.center is None:
    #         circulo = Circulo()
    #         circulo.xc = x
    #         circulo.yc = y
    #         self.context.global_vars.circulo = circulo
    #         self.center = Ponto(x, y)
    #         #print(f"Centro definido em: ({x:.2f}, {y:.2f})")
    #     else:
    #         # Segundo clique: define o raio e cria o círculo
    #         radius = sqrt((x - self.center.x) ** 2 + (y - self.center.y) ** 2)
    #         #circle = Circulo(self.center.x, self.center.y, radius)
    #         self.context.global_vars.circulo.raio = radius
    #         self.context.global_vars.modelo.addCirculo(self.context.global_vars.circulo)
    #         print(f"Círculo criado: centro=({self.center.x:.2f}, {self.center.y:.2f}), raio={radius:.2f}")
    #         self.context.global_vars.circulo = None
    #         # força redesenho
    #         self.context.canvas.update()

    #         # Reseta e volta para o estado Idle
    #         self.center = None
    #         self.context.currentState = self.context.idleState


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


    # def mouseMoveEvent(self, event):
    #     """Atualiza o círculo temporário durante o movimento do mouse."""
    #     if self.center:
    #         # x = event.x() - self.context.global_vars.w / 2
    #         # y = self.context.global_vars.h / 2 - event.y()
    #         x, y = getWorldCoords(self.context, event.x(), event.y())
    #         r = sqrt((x - self.center.x)**2 + (y - self.center.y)**2)
    #         self.context.global_vars.circulo.raio = r
    #         # força redesenho
    #         self.context.canvas.update()

    def display(self):
        """Desenha o modelo completo + círculo temporário, se existir."""
        #print("[display] Estado:", type(self).__name__)
        
        axis(self.context)  # ← desenha eixos\
        glColor3f(1.0, 0.0, 3.0)
        self.context.global_vars.modelo.draw()
        if self.context.global_vars.circulo:
            glColor3f(0.0, 1.0, 0.0)
            self.context.global_vars.circulo.drawOpen()

    def keyboard(self, key, x, y):
         pass

