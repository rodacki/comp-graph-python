# src/cg_examples/ex07_2D_Editor_Qt/state/drawPolygonState.py
"""Estado responsável pelo desenho interativo de polígonos.

O usuário adiciona vértices com cliques esquerdos e finaliza com duplo clique,
botão direito ou tecla Enter. Durante o movimento, um segmento temporário
("borrachinha") é desenhado para guiar a próxima aresta.
"""

from __future__ import annotations

import logging
from math import isfinite
from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QMouseEvent

from ..model.poligono import Poligono
from ..model.ponto import Ponto
from ..view.draw_utils import get_world_coords
from ..view.renderers import draw_polygon, draw_segment
from .abstract_state import State

log = logging.getLogger(__name__)


class DrawPolygonState(State):
    """
    Estado único para desenhar polígonos:
      - Clique esq: inicia/adiciona ponto
      - Mover mouse: mostra aresta temporária
      - Duplo clique / botão dir / Enter: finaliza
      - Esc: cancela
    O commit é feito ao finalizar (modelo.addPoligono).
    """

    def __init__(self, context: Any) -> None:
        """Inicializa estado de construção de polígonos.

        Args:
            context: Contexto da aplicação com acesso ao modelo e canvas.

        Returns:
            None: Configura buffers temporários de construção.
        """
        super().__init__(context)
        self._poly: Poligono | None = None
        self._mouse_world: Ponto | None = None

    # -------- lifecycle helpers --------
    def _start_if_needed(self, xw: float, yw: float) -> None:
        """Cria polígono temporário ou adiciona novo vértice.

        Args:
            xw: Coordenada X em mundo do clique.
            yw: Coordenada Y em mundo do clique.

        Returns:
            None: Atualiza o polígono temporário em construção.
        """
        if self._poly is None:
            self._poly = Poligono()
            self._poly.add_ponto(Ponto(xw, yw))
        else:
            self._poly.add_ponto(Ponto(xw, yw))

    def finish_polygon(self) -> None:
        """Finaliza desenho e comita polígono válido no modelo.

        Returns:
            None: Reseta buffers temporários e retorna para o estado idle.

        Side Effects:
            Adiciona o polígono ao modelo quando possuir ao menos 3 pontos.
        """
        if self._poly and len(self._poly.pontos) >= 3:
            self.context.global_vars.modelo.add_poligono(self._poly)
        # reset
        self._poly = None
        self._mouse_world = None
        self.context.current_state = self.context.idle_state
        self.context.canvas.update()

    def cancel_polygon(self) -> None:
        """Cancela construção atual sem comitar no modelo.

        Returns:
            None: Limpa buffers temporários e retorna ao estado idle.
        """
        self._poly = None
        self._mouse_world = None
        self.context.current_state = self.context.idle_state
        self.context.canvas.update()

    # -------- eventos Qt --------
    def mouse_press_event(self, event: QMouseEvent) -> None:
        """Processa clique para adicionar vértice ou finalizar rapidamente.

        Args:
            event: Evento de clique do mouse.

        Returns:
            None: Atualiza construção ou finaliza conforme botão pressionado.
        """
        xw, yw = get_world_coords(self.context, event.x(), event.y())

        if event.button() == Qt.MouseButton.LeftButton:
            self._start_if_needed(xw, yw)
            self.context.canvas.update()

        elif event.button() == Qt.MouseButton.RightButton:
            # finalizar rápido com botão direito
            self.finish_polygon()

    def mouse_double_click_event(self, event: QMouseEvent) -> None:
        """Finaliza polígono em construção no duplo clique.

        Args:
            event: Evento de duplo clique (não usado diretamente).

        Returns:
            None: Encaminha para rotina de finalização.
        """
        log.info("mouse_double_click_event")
        self.finish_polygon()

    def mouse_move_event(self, event: QMouseEvent) -> None:
        """Atualiza posição do cursor em mundo para desenhar aresta temporária.

        Args:
            event: Evento de movimento do mouse.

        Returns:
            None: Atualiza `_mouse_world` quando coordenadas forem finitas.
        """
        xw, yw = get_world_coords(self.context, event.x(), event.y())
        if isfinite(xw) and isfinite(yw):
            self._mouse_world = Ponto(xw, yw)
            self.context.canvas.update()

    def key_press_event(self, event: QKeyEvent) -> None:
        """Trata atalhos de teclado para finalizar ou cancelar o polígono.

        Args:
            event: Evento de tecla pressionada.

        Returns:
            None: Executa ação correspondente à tecla.
        """
        k = event.key()
        log.info("KeyPressEvent, key: %s", k)
        if k in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.finish_polygon()
        elif k == Qt.Key.Key_Escape:
            self.cancel_polygon()

    # -------- overlay (pré-visualização) --------
    def display_overlay(self) -> None:
        """Desenha preview do polígono em construção.

        Returns:
            None: Renderiza polilinha aberta e segmento temporário quando houver.
        """
        poly = self._poly
        if poly is None:
            return

        # 1️⃣ Desenha o polígono parcialmente construído (em verde)
        draw_polygon(poly, open_strip=True, color=(0.0, 1.0, 0.0), width=2.0)

        # 2️⃣ Desenha a “borrachinha” (último ponto → posição atual do mouse)
        if poly.last_point and self._mouse_world:
            p0 = poly.last_point
            p1 = self._mouse_world
            draw_segment(p0.x, p0.y, p1.x, p1.y, dashed=True, color=(0.0, 1.0, 0.0), width=1.0)
