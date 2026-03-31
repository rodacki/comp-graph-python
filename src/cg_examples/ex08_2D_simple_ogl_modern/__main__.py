"""Ponto de entrada do ex08.

Configura `QSurfaceFormat` para perfil core e inicia a aplicação PyQt5.
"""

import sys

from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtWidgets import QApplication

from .mainwindow import MainWindow


def configure_surface_format() -> None:
    """Configura formato OpenGL padrão para a aplicação.

    Returns:
        None: Define versão e perfil do contexto OpenGL.

    Notes:
        O exemplo usa pipeline moderno, portanto solicita perfil core.
    """
    surface_format = QSurfaceFormat()
    surface_format.setRenderableType(QSurfaceFormat.OpenGL)
    surface_format.setVersion(3, 3)
    surface_format.setProfile(QSurfaceFormat.CoreProfile)
    QSurfaceFormat.setDefaultFormat(surface_format)


def main() -> None:
    """Inicializa app Qt e exibe a janela principal.

    Returns:
        None: Encerra processo com código retornado pelo loop Qt.
    """
    configure_surface_format()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec_())


if __name__ == "__main__":
    main()
