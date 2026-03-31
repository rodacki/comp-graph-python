"""Canvas OpenGL (PyQt6) do ex01 hello moderno."""

from __future__ import annotations

from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_NO_ERROR, glClear, glClearColor, glGetError, glViewport
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent, QKeyEvent
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QApplication

from .renderer import TriangleRenderer


class GLCanvas(QOpenGLWidget):
    """Widget OpenGL responsavel por inicializar e desenhar a cena."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._renderer = TriangleRenderer()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def initializeGL(self) -> None:
        """Inicializa estado basico de renderizacao OpenGL."""
        self._drain_gl_errors()
        glClearColor(0.08, 0.1, 0.14, 1.0)
        self._renderer.initialize()

    def _drain_gl_errors(self) -> None:
        """Limpa erros OpenGL pendentes antes da primeira chamada PyOpenGL.

        Notes:
            Em alguns ambientes Qt + macOS podem existir erros legados no estado
            de erro do contexto logo apos sua criacao. A checagem automatica do
            PyOpenGL levanta excecao na chamada seguinte, mesmo sem relacao com
            ela.
        """
        while glGetError() != GL_NO_ERROR:
            pass

    def resizeGL(self, w: int, h: int) -> None:
        """Atualiza viewport quando o widget muda de tamanho."""
        glViewport(0, 0, w, h)

    def paintGL(self) -> None:
        """Desenha frame atual."""
        glClear(GL_COLOR_BUFFER_BIT)
        self._renderer.draw()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Encerra aplicacao ao pressionar Esc."""
        if event.key() == Qt.Key.Key_Escape:
            app = QApplication.instance()
            if app is not None:
                app.quit()
            return
        super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Libera recursos OpenGL antes de fechar o widget."""
        self.makeCurrent()
        self._renderer.dispose()
        self.doneCurrent()
        super().closeEvent(event)
