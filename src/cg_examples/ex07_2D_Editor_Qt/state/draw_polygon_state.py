# src/cg_examples/ex07_2D_Editor_Qt/state/drawPolygonState.py
from __future__ import annotations

import logging
from math import isfinite

from OpenGL.GL import (
    GL_ENABLE_BIT,
    GL_LINE_STIPPLE,
    GL_LINES,
    glBegin,
    glEnable,
    glEnd,
    glLineStipple,
    glPopAttrib,
    glPushAttrib,
    glVertex2f,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QMouseEvent

from ..model.poligono import Poligono
from ..model.ponto import Ponto
from ..view.draw_utils import get_world_coords
from ..view.renderers import draw_polygon
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

    def __init__(self, context) -> None:
        super().__init__(context)
        self._poly: Poligono | None = None
        self._mouse_world: Ponto | None = None

    # -------- lifecycle helpers --------
    def _start_if_needed(self, xw: float, yw: float) -> None:
        if self._poly is None:
            self._poly = Poligono()
            self._poly.add_ponto(Ponto(xw, yw))
        else:
            self._poly.add_ponto(Ponto(xw, yw))

    def finish_polygon(self) -> None:
        """Finaliza e commita (se houver ao menos 3 pontos)."""
        if self._poly and len(self._poly.pontos) >= 3:
            self.context.global_vars.modelo.add_poligono(self._poly)
        # reset
        self._poly = None
        self._mouse_world = None
        self.context.current_state = self.context.idle_state
        self.context.canvas.update()

    def cancel_polygon(self) -> None:
        """Descarta e volta ao idle."""
        self._poly = None
        self._mouse_world = None
        self.context.current_state = self.context.idle_state
        self.context.canvas.update()

    # -------- eventos Qt --------
    def mouse_press_event(self, event: QMouseEvent) -> None:
        xw, yw = get_world_coords(self.context, event.x(), event.y())

        if event.button() == Qt.MouseButton.LeftButton:
            self._start_if_needed(xw, yw)
            self.context.canvas.update()

        elif event.button() == Qt.MouseButton.RightButton:
            # finalizar rápido com botão direito
            self.finish_polygon()

    def mouse_double_click_event(self, event: QMouseEvent) -> None:
        # finalizar com duplo clique
        log.info("mouse_double_click_event")
        self.finish_polygon()

    def mouse_move_event(self, event: QMouseEvent) -> None:
        xw, yw = get_world_coords(self.context, event.x(), event.y())
        if isfinite(xw) and isfinite(yw):
            self._mouse_world = Ponto(xw, yw)
            self.context.canvas.update()

    def key_press_event(self, event: QKeyEvent) -> None:
        k = event.key()
        if k in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.finish_polygon()
        elif k == Qt.Key.Key_Escape:
            self.cancel_polygon()

    # -------- overlay (pré-visualização) --------
    def display_overlay(self) -> None:
        """Desenha polígono aberto + aresta temporária."""
        poly = self._poly
        if poly is None:
            return

        # 1️⃣ Desenha o polígono parcialmente construído (em verde)
        draw_polygon(poly, open_strip=True, color=(0.0, 1.0, 0.0), width=2.0)

        # 2️⃣ Desenha a “borrachinha” (último ponto → posição atual do mouse)
        if poly.last_point and self._mouse_world:
            x0, y0 = poly.last_point.x, poly.last_point.y
            x1, y1 = self._mouse_world.x, self._mouse_world.y

            glPushAttrib(GL_ENABLE_BIT)
            glLineStipple(10, 0xAAAA)
            glEnable(GL_LINE_STIPPLE)

            glBegin(GL_LINES)
            glVertex2f(x0, y0)
            glVertex2f(x1, y1)
            glEnd()

            glPopAttrib()

        # # estilo do esboço
        # glColor3f(0.0, 1.0, 0.0)
        # glLineWidth(2.0)
        # self._poly.drawOpen()
        # glLineWidth(1.0)

        # # “borrachinha” da última aresta até o mouse
        # if self._poly.lastPoint and self._mouse_world:
        #     x0, y0 = self._poly.lastPoint.x, self._poly.lastPoint.y
        #     x1, y1 = self._mouse_world.x, self._mouse_world.y
        #     glPushAttrib(GL_ENABLE_BIT)
        #     glLineStipple(10, 0xAAAA)
        #     glEnable(GL_LINE_STIPPLE)

        #     glBegin(GL_LINES)
        #     glVertex2f(x0, y0)
        #     glVertex2f(x1, y1)
        #     glEnd()

        #     glPopAttrib()
