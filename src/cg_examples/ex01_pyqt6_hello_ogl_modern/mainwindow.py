"""Janela principal do exemplo ex01 PyQt6 + OpenGL moderno.

O objetivo aqui e didatico: manter a GUI no minimo possivel para que o aluno
foco no fluxo OpenGL. Por isso a janela contem apenas o canvas.
"""

from __future__ import annotations

from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget

from .view.glcanvas import GLCanvas


class MainWindow(QWidget):
    """Janela com layout minimo contendo apenas o canvas OpenGL."""

    def __init__(self) -> None:
        """Cria janela principal e adiciona canvas ao layout.

        Notes:
            O layout sem margens evita bordas internas e deixa o canvas ocupar
            toda a area util da janela.
        """
        super().__init__()
        self.setWindowTitle("Ex01 - PyQt6 Hello OpenGL Modern")
        self.resize(700, 700)

        # O canvas concentra toda logica de OpenGL e de teclado (Esc).
        canvas = GLCanvas(parent=self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(canvas)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Encerra aplicacao ao fechar janela pela GUI.

        O `event.accept()` confirma para o Qt que o fechamento pode prosseguir.
        """
        app = QApplication.instance()
        if app is not None:
            app.quit()
        event.accept()
