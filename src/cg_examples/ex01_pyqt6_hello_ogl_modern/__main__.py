"""Ponto de entrada do ex01 PyQt6 + OpenGL moderno.

Para iniciantes, este arquivo mostra duas ideias fundamentais:

1. configurar o formato do contexto OpenGL (versao/perfil) antes do app Qt;
2. criar `QApplication`, abrir a janela e iniciar o loop de eventos.
"""

from __future__ import annotations

import sys

from PyQt6.QtGui import QSurfaceFormat
from PyQt6.QtWidgets import QApplication

from .mainwindow import MainWindow


def configure_surface_format() -> None:
    """Configura formato OpenGL core profile para a aplicacao.

    Returns:
        None: Define versao e perfil do contexto OpenGL.

    Notes:
        Em macOS, a configuracao padrao deve ser definida antes de criar
        `QApplication` para evitar incompatibilidades de contexto.
    """
    surface_format = QSurfaceFormat()
    # Tipo de renderer desejado: OpenGL (nao Vulkan/Metal/etc.).
    surface_format.setRenderableType(QSurfaceFormat.RenderableType.OpenGL)
    # OpenGL 3.3 Core: pipeline moderno, sem chamadas legadas immediate mode.
    surface_format.setVersion(3, 3)
    surface_format.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    # Define esse formato como padrao para widgets OpenGL criados depois.
    QSurfaceFormat.setDefaultFormat(surface_format)


def main() -> None:
    """Inicializa QApplication, mostra janela e executa loop Qt."""
    configure_surface_format()
    # Todo app Qt precisa exatamente de uma instancia de QApplication.
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # `app.exec()` bloqueia ate o encerramento; convertimos para exit code.
    raise SystemExit(app.exec())


if __name__ == "__main__":
    main()
