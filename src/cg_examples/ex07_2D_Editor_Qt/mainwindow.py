# pyright: reportIncompatibleMethodOverride=false
"""Janela principal do editor 2D.

Este módulo define a composição da interface (canvas OpenGL + barra de botões)
e conecta as ações de UI com a máquina de estados da aplicação.
"""

import qtawesome as qta
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from .globals.settings import GlobalDefinitions
from .state.context import Context
from .view.glcanvas import GLCanvas


class MainWindow(QWidget):
    """Container principal do editor e ponto de integração View/State."""

    def __init__(self) -> None:
        """Monta widgets, contexto de estados e timer de repintura.

        Returns:
            None: Inicializa a instância da janela principal.
        """
        super().__init__()

        self.setWindowTitle("Editor 2D - PyQt + OpenGL")
        self.setGeometry(200, 200, 800, 800)
        self._cross_cursor = QCursor(Qt.CursorShape.CrossCursor)

        # Variáveis globais e contexto de estados
        self.global_vars = GlobalDefinitions()
        self.state_context = Context(self.global_vars)

        # Layout principal
        layout = QVBoxLayout()

        # Canvas OpenGL
        self.canvas = GLCanvas(self.state_context)
        self.state_context.canvas = self.canvas  # referência cruzada
        layout.addWidget(self.canvas)

        # Barra de botões
        button_layout = QHBoxLayout()

        self.btn_circle = QPushButton()
        self.btn_circle.setIcon(qta.icon("fa6.circle", color="gray"))
        self.btn_circle.setIconSize(QSize(32, 32))

        self.btn_init_poligono = QPushButton()
        self.btn_init_poligono.setIcon(qta.icon("fa6s.draw-polygon", color="gray"))
        self.btn_init_poligono.setIconSize(QSize(32, 32))

        # self.btn_end_poligono = QPushButton("End Pol")
        self.btn_exit = QPushButton()
        self.btn_exit.setIcon(qta.icon("fa6s.right-from-bracket", color="gray"))
        self.btn_exit.setIconSize(QSize(32, 32))

        # Ligações de eventos
        self.btn_circle.clicked.connect(self.on_start_circle)
        self.btn_init_poligono.clicked.connect(self.on_start_polygon)
        self.btn_exit.clicked.connect(self.on_exit)

        button_layout.addWidget(self.btn_circle)
        button_layout.addWidget(self.btn_init_poligono)
        button_layout.addWidget(self.btn_exit)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Timer para repintura contínua (~60 FPS)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.canvas.update)
        self.timer.start(16)

    # ------------------------------------------------ #
    # Ações dos botões
    # ------------------------------------------------ #

    def on_start_circle(self) -> None:
        """Ativa o estado de desenho de círculos.

        Returns:
            None: Apenas altera o estado atual do contexto.
        """
        self.state_context.current_state = self.state_context.draw_circle_state
        print("🟢 Estado: Iniciar círculo")

    def on_start_polygon(self) -> None:
        """Ativa o estado de desenho de polígonos e foca o canvas.

        Returns:
            None: O foco é transferido para receber teclas (Enter/Esc).
        """
        self.state_context.current_state = self.state_context.draw_polygon_state
        self.canvas.setFocus()  # <- garante que o canvas receba teclas
        print("🟢 Estado: Iniciar poligono")

    def on_exit(self) -> None:
        """Fecha a janela principal e solicita encerramento da aplicação.

        Returns:
            None: O loop Qt é encerrado pelo fechamento da janela.
        """
        print("Saindo...")
        self.close()
