"""Ponto de entrada do editor 2D em PyQt5 + OpenGL.

Este módulo configura logging, define o formato de superfície OpenGL
(compatibility profile para suportar pipeline fixa) e inicializa a janela principal.
"""

import logging
import os
import sys

from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtWidgets import QApplication

from .mainwindow import MainWindow


def setup_logging() -> None:
    """Configura logging global da aplicação.

    Returns:
        None: A configuração é aplicada ao logger raiz do processo.
    """
    # Ex.: LOG_LEVEL=DEBUG poetry run ex07-pyqt-opengl
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def main() -> None:
    """Inicializa QApplication, cria a janela principal e entra no loop Qt.

    Returns:
        None: A função encerra o processo com o código retornado pelo Qt.
    """
    setup_logging()
    surface_format = QSurfaceFormat()
    surface_format.setRenderableType(QSurfaceFormat.OpenGL)
    surface_format.setVersion(2, 1)
    surface_format.setProfile(QSurfaceFormat.CompatibilityProfile)
    QSurfaceFormat.setDefaultFormat(surface_format)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
