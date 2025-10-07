from OpenGL.GL import (
    glColor3f, 
)

from .abstractState import State
from ..view.draw_utils import getWorldCoords
from ..view.draw_utils import axis
from ..model.circulo import Circulo
from ..model.ponto import Ponto
from math import sqrt


class InitCircleState(State):
    def __init__(self, context):
        super().__init__(context)
        self.center = None  # Ponto inicial (centro)
        self.temp_circle = None

    @property
    def context(self):
        return super().context
    
    @context.setter
    def context(self, newcontext):
        super().context = newcontext

    def mousePressEvent(self, event):
        # Conversão das coordenadas do clique para coordenadas do mundo
        #x = (event.x() - self.context.global_vars.w / 2)
        #y = (self.context.global_vars.h / 2 - event.y())
        x, y = getWorldCoords(self.context, event.x(), event.y())
        print(event.x(), event.y())

        if self.center is None:
            circulo = Circulo()
            circulo.xc = x
            circulo.yc = y
            self.context.global_vars.circulo = circulo
            self.center = Ponto(x, y)
            #print(f"Centro definido em: ({x:.2f}, {y:.2f})")
        else:
            # Segundo clique: define o raio e cria o círculo
            radius = sqrt((x - self.center.x) ** 2 + (y - self.center.y) ** 2)
            #circle = Circulo(self.center.x, self.center.y, radius)
            self.context.global_vars.circulo.raio = radius
            self.context.global_vars.modelo.addCirculo(self.context.global_vars.circulo)
            print(f"Círculo criado: centro=({self.center.x:.2f}, {self.center.y:.2f}), raio={radius:.2f}")
            self.context.global_vars.circulo = None
            # força redesenho
            self.context.canvas.update()

            # Reseta e volta para o estado Idle
            self.center = None
            self.context.currentState = self.context.idleState

    def mouseMoveEvent(self, event):
        """Atualiza o círculo temporário durante o movimento do mouse."""
        if self.center:
            # x = event.x() - self.context.global_vars.w / 2
            # y = self.context.global_vars.h / 2 - event.y()
            x, y = getWorldCoords(self.context, event.x(), event.y())
            r = sqrt((x - self.center.x)**2 + (y - self.center.y)**2)
            self.context.global_vars.circulo.raio = r
            # força redesenho
            self.context.canvas.update()

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

