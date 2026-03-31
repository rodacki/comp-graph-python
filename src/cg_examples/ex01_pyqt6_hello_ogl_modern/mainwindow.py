"""Janela principal do exemplo ex01 PyQt6 + OpenGL moderno."""

from __future__ import annotations

from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget

from .view.glcanvas import GLCanvas


class MainWindow(QWidget):
    """Janela com layout minimo contendo apenas o canvas OpenGL."""

    def __init__(self) -> None:
        """Cria janela principal e adiciona canvas ao layout."""
        super().__init__()
        self.setWindowTitle("Ex01 - PyQt6 Hello OpenGL Modern")
        self.resize(900, 700)

        canvas = GLCanvas(parent=self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(canvas)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Encerra aplicacao ao fechar janela pela GUI."""
        app = QApplication.instance()
        if app is not None:
            app.quit()
        event.accept()
