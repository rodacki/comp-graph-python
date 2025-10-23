# src/cg_examples/ex07_2D_Editor_Qt/state/drawPolygonState.py
from __future__ import annotations
from typing import Optional
from math import isfinite

from PyQt5.QtGui import QMouseEvent, QKeyEvent
from PyQt5.QtCore import Qt

from OpenGL.GL import (
    GL_ENABLE_BIT, GL_LINE_STIPPLE, GL_LINES,
    glPushAttrib, glPopAttrib, glEnable, glLineStipple,
    glBegin, glEnd, glVertex2f, glColor3f, glLineWidth,
)

from .abstractState import State
from ..model.poligono import Poligono
from ..model.ponto import Ponto
from ..view.draw_utils import getWorldCoords


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
        self._poly: Optional[Poligono] = None
        self._mouse_world: Optional[Ponto] = None

    # -------- lifecycle helpers --------
    def _start_if_needed(self, xw: float, yw: float) -> None:
        if self._poly is None:
            self._poly = Poligono()
            self._poly.addPonto(Ponto(xw, yw))
        else:
            self._poly.addPonto(Ponto(xw, yw))

    def finish_polygon(self) -> None:
        """Finaliza e commita (se houver ao menos 3 pontos)."""
        if self._poly and len(self._poly.pontos) >= 3:
            self.context.global_vars.modelo.addPoligono(self._poly)
        # reset
        self._poly = None
        self._mouse_world = None
        self.context.currentState = self.context.idleState
        self.context.canvas.update()

    def cancel_polygon(self) -> None:
        """Descarta e volta ao idle."""
        self._poly = None
        self._mouse_world = None
        self.context.currentState = self.context.idleState
        self.context.canvas.update()

    # -------- eventos Qt --------
    def mousePressEvent(self, event: QMouseEvent) -> None:
        xw, yw = getWorldCoords(self.context, event.x(), event.y())

        if event.button() == Qt.MouseButton.LeftButton:
            self._start_if_needed(xw, yw)
            self.context.canvas.update()

        elif event.button() == Qt.MouseButton.RightButton:
            # finalizar rápido com botão direito
            self.finish_polygon()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        # finalizar com duplo clique
        self.finish_polygon()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        xw, yw = getWorldCoords(self.context, event.x(), event.y())
        if isfinite(xw) and isfinite(yw):
            self._mouse_world = Ponto(xw, yw)
            self.context.canvas.update()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        k = event.key()
        if k in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.finish_polygon()
        elif k == Qt.Key.Key_Escape:
            self.cancel_polygon()

    # -------- overlay (pré-visualização) --------
    def display_overlay(self) -> None:
        """Desenha polígono aberto + aresta temporária."""
        if self._poly is None:
            return

        # estilo do esboço
        glColor3f(0.0, 1.0, 0.0)
        glLineWidth(2.0)
        self._poly.drawOpen()
        glLineWidth(1.0)

        # “borrachinha” da última aresta até o mouse
        if self._poly.lastPoint and self._mouse_world:
            x0, y0 = self._poly.lastPoint.x, self._poly.lastPoint.y
            x1, y1 = self._mouse_world.x, self._mouse_world.y
            glPushAttrib(GL_ENABLE_BIT)
            glLineStipple(10, 0xAAAA)
            glEnable(GL_LINE_STIPPLE)

            glBegin(GL_LINES)
            glVertex2f(x0, y0)
            glVertex2f(x1, y1)
            glEnd()

            glPopAttrib()