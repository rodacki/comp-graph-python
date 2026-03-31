"""Janela principal do ex08.

A interface é propositalmente mínima: apenas o canvas OpenGL para edição.

Objetivo didático:
- destacar a integração `QWidget + QOpenGLWidget`;
- manter foco no pipeline moderno (renderer/shaders), sem componentes extras
  de interface como toolbar e botões.
"""

from PyQt5.QtWidgets import QVBoxLayout, QWidget

from .globals.settings import GlobalDefinitions
from .model.modelo import Modelo
from .state.context import Context
from .view.glcanvas import GLCanvas


class MainWindow(QWidget):
    """Container principal com canvas único de desenho.

    Esta classe monta a composição mínima da aplicação:
    `GlobalDefinitions` -> `Context` -> `GLCanvas`.
    """

    def __init__(self) -> None:
        """Cria estado global, contexto e canvas do exemplo.

        Returns:
            None: Inicializa janela e layout.

        Side Effects:
            Cria o modelo da cena, contexto de estados e associa o canvas ao
            contexto para permitir delegação de eventos.
        """
        super().__init__()
        self.setWindowTitle("Ex08 - Segmentos 2D (OpenGL Moderno)")
        self.resize(900, 700)

        global_vars = GlobalDefinitions(modelo=Modelo())
        context = Context(global_vars=global_vars)

        canvas = GLCanvas(context=context)
        context.canvas = canvas

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(canvas)
