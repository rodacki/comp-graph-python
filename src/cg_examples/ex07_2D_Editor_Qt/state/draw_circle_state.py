"""Estado responsável pelo desenho interativo de círculos.

Fluxo pedagógico:
- primeiro clique define o centro;
- movimento do mouse atualiza preview do raio;
- segundo clique confirma e comita o círculo no modelo.
"""

from math import sqrt
from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent

from ..model.circulo import Circulo
from ..model.ponto import Ponto
from ..view.draw_utils import get_world_coords
from ..view.renderers import draw_circle
from .abstract_state import State


class DrawCircleState(State):
    """Estado de criação de círculos por dois cliques."""

    def __init__(self, context: Any) -> None:
        """Inicializa variáveis de construção do círculo temporário.

        Args:
            context: Contexto da aplicação com acesso ao modelo e ao canvas.

        Returns:
            None: Configura estado interno inicial.
        """
        super().__init__(context)
        self.center: Ponto | None = None  # Ponto inicial (centro)

    @property
    def context(self) -> Any:
        """Retorna contexto associado ao estado.

        Returns:
            Any: Contexto compartilhado do editor.
        """
        return super().context

    @context.setter
    def context(self, newcontext: Any) -> None:
        """Atualiza referência de contexto do estado.

        Args:
            newcontext: Novo contexto compartilhado.

        Returns:
            None: Apenas substitui referência interna.
        """
        super().context = newcontext

    def mouse_press_event(self, event: QMouseEvent) -> None:
        """Processa clique para iniciar ou finalizar desenho do círculo.

        Args:
            event: Evento de clique do mouse.

        Returns:
            None: Atualiza preview, modelo e transição de estado quando necessário.

        Side Effects:
            - Cria/atualiza `global_vars.circulo` durante preview.
            - Comita círculo no modelo ao segundo clique.
            - Retorna para `idle_state` após confirmação.
        """
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

    def mouse_move_event(self, event: QMouseEvent) -> None:
        """Atualiza raio do círculo temporário durante movimento do mouse.

        Args:
            event: Evento de movimento do mouse.

        Returns:
            None: Recalcula raio e solicita redraw quando houver preview ativo.
        """
        if self.center and self.context.global_vars.circulo:
            x, y = get_world_coords(self.context, event.x(), event.y())
            r = sqrt((x - self.center.x) ** 2 + (y - self.center.y) ** 2)
            self.context.global_vars.circulo.raio = r
            # força redesenho
            self.context.canvas.update()

    # ---- somente overlay (preview) do estado ----
    def display_overlay(self) -> None:
        """Desenha apenas preview tracejado do círculo em construção.

        Returns:
            None: Renderiza no frame atual quando houver círculo temporário.
        """
        temp = self.context.global_vars.circulo
        if temp:
            draw_circle(temp, dashed=True, color=(0, 1, 0))
