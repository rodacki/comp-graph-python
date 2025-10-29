# pyright: reportIncompatibleMethodOverride=false
import logging

from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    glClear,
    glClearColor,
    glLoadIdentity,
    glViewport,
)
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QCursor, QKeyEvent, QMouseEvent
from PyQt5.QtOpenGL import QGLWidget

from ..state.context import Context
from ..view.renderers import draw_circle, draw_polygon
from .draw_utils import axis, px_to_world

log = logging.getLogger(__name__)


class GLCanvas(QGLWidget):
    def __init__(self, state_context: Context, parent=None):
        super().__init__(parent)
        self.state_context = state_context
        self.setMouseTracking(True)
        self._cross_cursor = QCursor(Qt.CursorShape.CrossCursor)
        self.setFocusPolicy(Qt.StrongFocus)  # <- importante

    def initializeGL(self):
        from ..view.draw_utils import init

        glClearColor(0.2, 0.3, 0.4, 1.0)
        init(self.state_context)  # ← importante

    def resizeGL(self, w, h):
        # Corrige para monitores HiDPI (Retina)
        ratio = self.devicePixelRatioF()
        pixel_w = int(w * ratio)
        pixel_h = int(h * ratio)

        glViewport(0, 0, pixel_w, pixel_h)

        gv = self.state_context.global_vars
        gv.w = pixel_w
        gv.h = pixel_h

        # --- cálculo do tamanho do handler em coordenadas do mundo ---
        gv.handle_size_world = px_to_world(self.state_context, gv.handle_size_px, "avg")
        # print(f"[resizeGL] Logical: ({w}, {h})  Physical: ({pixel_w}, {pixel_h})  ratio={ratio:.2f}")

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # type: ignore
        glLoadIdentity()

        ctx = self.state_context
        gv = ctx.global_vars
        m = gv.modelo

        if gv.selected:
            log.debug("selected[0] id=%s", id(gv.selected[0]))
        if m.circulos:
            log.debug("modelo.circulos[0] id=%s", id(m.circulos[0]))
        if m.poligonos:
            log.debug("modelo.poligonos[0] id=%s", id(m.poligonos[0]))

        # 1) Eixos
        axis(ctx)

        # 2) cena principal (objetos)
        for p in m.poligonos:
            # p.draw(open_strip=False)
            # cor e espessura básicos; destaque fica no overlay de seleção
            draw_polygon(p, open_strip=False, color=(1.0, 1.0, 1.0), width=1.0)
        for c in m.circulos:
            draw_circle(c, dashed=False, color=(1.0, 1.0, 1.0), width=1.0)
            # c.draw()

        # 3) seleção (decorations) — na View
        for p in m.poligonos:
            from .selection_render import draw_polygon_selection

            draw_polygon_selection(p, ctx)
        for c in m.circulos:
            from .selection_render import draw_circle_selection

            draw_circle_selection(c, ctx)

        # 4) overlay do estado (se existir)
        current = ctx.current_state
        if hasattr(current, "display_overlay"):
            current.display_overlay()  # desenha “borrachinha”, etc.

    # Eventos do mouse — delegados para o contexto
    def mousePressEvent(
        self, event: QMouseEvent
    ) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        log.debug(
            "GLCanvas.mousePressEvent: button=%s pos=(%d,%d)", event.button(), event.x(), event.y()
        )
        self.state_context.mouse_press_event(event)
        self.update()

    def mouseMoveEvent(
        self, event: QMouseEvent
    ) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        log.debug("GLCanvas.mouseMoveEvent: pos=(%d,%d)", event.x(), event.y())
        self.state_context.mouse_move_event(event)
        self.update()

    def keyPressEvent(
        self, event: QKeyEvent
    ) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        log.debug("GLCanvas.keyPressEvent: key=%s", event.key())
        self.state_context.key_press_event(event)
        self.update()

    def mouseDoubleClickEvent(
        self, event: QMouseEvent
    ) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        log.debug(
            "GLCanvas.mouseDoubleClickEvent: button=%s pos=(%d,%d)",
            event.button(),
            event.x(),
            event.y(),
        )
        """Encaminha o duplo clique ao estado atual."""
        self.state_context.mouse_double_click_event(event)
        self.update()

    # Ao entrar na área do canvas, mude o cursor
    def enterEvent(self, event: QEvent) -> None:
        self.setCursor(self._cross_cursor)

    # Ao sair, restaure para o padrão
    def leaveEvent(self, event: QEvent) -> None:
        self.unsetCursor()  # volta ao cursor do sistema/janela
