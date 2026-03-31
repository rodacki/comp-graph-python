"""Ponto de entrada do ex01 PyQt6 + OpenGL moderno."""

from __future__ import annotations

import sys

from PyQt6.QtGui import QSurfaceFormat
from PyQt6.QtWidgets import QApplication

from .mainwindow import MainWindow


def configure_surface_format() -> None:
    """Configura formato OpenGL core profile para a aplicacao.

    Returns:
        None: Define versao e perfil do contexto OpenGL.
    """
    surface_format = QSurfaceFormat()
    surface_format.setRenderableType(QSurfaceFormat.RenderableType.OpenGL)
    surface_format.setVersion(3, 3)
    surface_format.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    QSurfaceFormat.setDefaultFormat(surface_format)


def main() -> None:
    """Inicializa QApplication e exibe janela principal."""
    configure_surface_format()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec())


if __name__ == "__main__":
    main()
