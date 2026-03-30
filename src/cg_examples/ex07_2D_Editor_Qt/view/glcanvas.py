# pyright: reportIncompatibleMethodOverride=false
"""Widget OpenGL responsável pelo desenho e delegação de eventos do editor.

O canvas concentra o ciclo de renderização (initializeGL/resizeGL/paintGL) e
encaminha eventos de mouse/teclado para o Context, que por sua vez delega ao
estado corrente da máquina de estados.
"""

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
from PyQt5.QtWidgets import QOpenGLWidget

from ..state.context import Context
from ..view.renderers import draw_circle, draw_polygon
from .draw_utils import axis, px_to_world

log = logging.getLogger(__name__)


class GLCanvas(QOpenGLWidget):
    """Canvas OpenGL do editor 2D."""

    def __init__(self, state_context: Context, parent=None) -> None:
        """Inicializa canvas e configurações básicas de interação.

        Args:
            state_context: Contexto com estado atual, modelo e variáveis globais.
            parent: Widget pai Qt, quando aplicável.

        Returns:
            None: Configura a instância do canvas.
        """
        super().__init__(parent)
        self.state_context = state_context
        self.setMouseTracking(True)
        self._cross_cursor = QCursor(Qt.CursorShape.CrossCursor)
        self.setFocusPolicy(Qt.StrongFocus)  # <- importante

    def initializeGL(self) -> None:
        """Configura estado inicial de OpenGL e projeção ortográfica.

        Returns:
            None: A configuração ocorre no contexto OpenGL já ativo.
        """
        from ..view.draw_utils import init

        glClearColor(0.2, 0.3, 0.4, 1.0)
        init(self.state_context)  # ← importante

    def resizeGL(self, w: int, h: int) -> None:
        """Atualiza viewport e métricas para monitores HiDPI.

        Args:
            w: Largura lógica reportada pelo Qt.
            h: Altura lógica reportada pelo Qt.

        Returns:
            None: Atualiza cache global de largura/altura e tamanho de handlers.
        """
        # Corrige para monitores HiDPI (Retina)
        ratio = self.devicePixelRatioF()
        pixel_w = int(w * ratio)
        pixel_h = int(h * ratio)

        glViewport(0, 0, pixel_w, pixel_h)

        gv = self.state_context.global_vars
        gv.w = pixel_w
        gv.h = pixel_h
        gv.device_pixel_ratio = ratio

        # --- cálculo do tamanho do handler em coordenadas do mundo ---
        gv.handle_size_world = px_to_world(self.state_context, gv.handle_size_px, "avg")
        # print(f"[resizeGL] Logical: ({w}, {h})  Physical: ({pixel_w}, {pixel_h})  ratio={ratio:.2f}")

    def paintGL(self) -> None:
        """Renderiza eixos, objetos, overlays de seleção e overlay do estado.

        Returns:
            None: O quadro é desenhado no framebuffer do QOpenGLWidget.
        """
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
        """Encaminha clique do mouse para o estado corrente.

        Args:
            event: Evento de pressionamento do mouse emitido pelo Qt.

        Returns:
            None: Solicita repaint após delegar ao contexto.
        """
        self.state_context.mouse_press_event(event)
        self.update()

    def mouseMoveEvent(
        self, event: QMouseEvent
    ) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Encaminha movimento do mouse para atualização interativa.

        Args:
            event: Evento de movimento do mouse emitido pelo Qt.

        Returns:
            None: Solicita repaint após delegar ao contexto.
        """
        self.state_context.mouse_move_event(event)
        self.update()

    def mouseReleaseEvent(
        self, event: QMouseEvent
    ) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Encaminha o release para o estado atual (ex.: término de arrasto)."""
        self.state_context.mouse_release_event(event)
        self.update()

    def keyPressEvent(
        self, event: QKeyEvent
    ) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Encaminha evento de teclado para o estado corrente.

        Args:
            event: Evento de tecla pressionada.

        Returns:
            None: Solicita repaint para refletir efeitos imediatos.
        """
        self.state_context.key_press_event(event)
        self.update()

    def mouseDoubleClickEvent(
        self, event: QMouseEvent
    ) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Encaminha duplo clique para o estado corrente.

        Args:
            event: Evento de duplo clique do mouse.

        Returns:
            None: Solicita repaint após delegar ao contexto.
        """
        log.info("mouseDoubleClick_event")
        self.state_context.mouse_double_click_event(event)
        self.update()

    # Ao entrar na área do canvas, mude o cursor
    def enterEvent(self, event: QEvent) -> None:
        """Define cursor de cruz ao entrar na área do canvas.

        Args:
            event: Evento Qt de entrada do cursor.

        Returns:
            None: Atualiza apenas o cursor local.
        """
        self.setCursor(self._cross_cursor)

    # Ao sair, restaure para o padrão
    def leaveEvent(self, event: QEvent) -> None:
        """Restaura o cursor padrão ao sair da área do canvas.

        Args:
            event: Evento Qt de saída do cursor.

        Returns:
            None: Limpa o cursor customizado do widget.
        """
        self.unsetCursor()  # volta ao cursor do sistema/janela
